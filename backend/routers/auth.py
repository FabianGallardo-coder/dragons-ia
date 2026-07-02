"""
Router de autenticación — Registro, login y perfil.
"""

from datetime import datetime, timedelta, timezone

from fastapi import APIRouter, Depends, HTTPException, Request, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from slowapi import Limiter
from slowapi.util import get_remote_address

from backend.config import get_settings
from backend.database import get_db
from backend.models.reset_token import ResetToken
from backend.models.user import User
from backend.schemas.user import (
    ForgotPasswordRequest,
    ResetPasswordRequest,
    TokenResponse,
    UserLogin,
    UserRegister,
    UserResponse,
)

router = APIRouter()
settings = get_settings()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
security = HTTPBearer()

# Rate limiter específico para auth - en debug/test usa límite alto
auth_limit = "5/minute" if not settings.debug else "10000/minute"
auth_limiter = Limiter(key_func=get_remote_address, default_limits=[auth_limit])


# ── Utilidades de JWT ──────────────────────────────────────────

def create_access_token(user_id: str) -> str:
    """Genera un JWT con el user_id como subject."""
    expire = datetime.now(timezone.utc) + timedelta(minutes=settings.jwt_expiration_minutes)
    payload = {"sub": user_id, "exp": expire}
    return jwt.encode(payload, settings.jwt_secret_key, algorithm=settings.jwt_algorithm)


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: AsyncSession = Depends(get_db),
) -> User:
    """Dependency que extrae y valida el usuario actual desde el JWT."""
    token = credentials.credentials
    try:
        payload = jwt.decode(token, settings.jwt_secret_key, algorithms=[settings.jwt_algorithm])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise HTTPException(status_code=401, detail="Token inválido.")
    except JWTError:
        raise HTTPException(status_code=401, detail="Token inválido o expirado.")

    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()
    if user is None or not user.is_active:
        raise HTTPException(status_code=401, detail="Usuario no encontrado o inactivo.")
    return user


# ── Endpoints ──────────────────────────────────────────────────

@router.post("/register", response_model=TokenResponse, status_code=201)
@auth_limiter.limit(auth_limit)
async def register(request: Request, data: UserRegister, db: AsyncSession = Depends(get_db)):
    """Registra un nuevo usuario y retorna JWT."""
    # Verificar email duplicado
    result = await db.execute(select(User).where(User.email == data.email))
    if result.scalar_one_or_none():
        raise HTTPException(status_code=400, detail="El email ya está registrado.")

    # Verificar username duplicado
    result = await db.execute(select(User).where(User.username == data.username))
    if result.scalar_one_or_none():
        raise HTTPException(status_code=400, detail="El nombre de usuario ya está en uso.")

    user = User(
        email=data.email,
        username=data.username,
        password_hash=pwd_context.hash(data.password),
    )
    db.add(user)
    await db.flush()
    await db.refresh(user)

    token = create_access_token(user.id)
    return TokenResponse(
        access_token=token,
        user=UserResponse.model_validate(user),
    )


@router.post("/login", response_model=TokenResponse)
@auth_limiter.limit(auth_limit)
async def login(request: Request, data: UserLogin, db: AsyncSession = Depends(get_db)):
    """Autentica al usuario y retorna JWT."""
    result = await db.execute(select(User).where(User.email == data.email))
    user = result.scalar_one_or_none()

    if not user or not pwd_context.verify(data.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Credenciales inválidas.")

    if not user.is_active:
        raise HTTPException(status_code=403, detail="Cuenta desactivada.")

    token = create_access_token(user.id)
    return TokenResponse(
        access_token=token,
        user=UserResponse.model_validate(user),
    )


@router.post("/forgot-password")
@auth_limiter.limit(auth_limit)
async def forgot_password(
    request: Request,
    data: ForgotPasswordRequest,
    db: AsyncSession = Depends(get_db),
):
    """Solicita reset de contraseña. Genera token y lo devuelve (sin email)."""
    import uuid

    result = await db.execute(select(User).where(User.email == data.email))
    user = result.scalar_one_or_none()
    if not user:
        return {"detail": "Si el email existe, recibirás instrucciones.", "token": None}

    token = uuid.uuid4().hex
    expires = datetime.now(timezone.utc) + timedelta(minutes=15)
    reset = ResetToken(
        id=uuid.uuid4().hex,
        user_id=user.id,
        token=pwd_context.hash(token),
        expires_at=expires,
    )
    db.add(reset)

    if settings.debug:
        return {"detail": "Token generado (modo debug).", "token": token}

    return {"detail": "Si el email existe, recibirás instrucciones.", "token": None}


@router.post("/reset-password")
@auth_limiter.limit(auth_limit)
async def reset_password(
    request: Request,
    data: ResetPasswordRequest,
    db: AsyncSession = Depends(get_db),
):
    """Resetea la contraseña usando un token válido."""
    from sqlalchemy import func

    now = datetime.now(timezone.utc)
    result = await db.execute(
        select(ResetToken).where(
            ResetToken.used == False,
            ResetToken.expires_at > now,
        )
    )
    tokens = result.scalars().all()

    matched = None
    for rt in tokens:
        if pwd_context.verify(data.token, rt.token):
            matched = rt
            break

    if not matched:
        raise HTTPException(status_code=400, detail="Token inválido o expirado.")

    result = await db.execute(select(User).where(User.id == matched.user_id))
    user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=400, detail="Usuario no encontrado.")

    user.password_hash = pwd_context.hash(data.password)
    matched.used = True

    return {"detail": "Contraseña actualizada correctamente."}


@router.get("/me", response_model=UserResponse)
async def get_me(current_user: User = Depends(get_current_user)):
    """Retorna los datos del usuario autenticado."""
    return UserResponse.model_validate(current_user)
