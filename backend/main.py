"""
Dragons & IA — Entry point de la aplicación FastAPI.

Monta los routers de la API, sirve el frontend estático
y gestiona el ciclo de vida de la base de datos.
"""

from contextlib import asynccontextmanager
from pathlib import Path
import secrets

from fastapi import FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, JSONResponse
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

from backend.config import get_settings
from backend.database import create_tables
from backend.routers import auth, characters, game

settings = get_settings()

FRONTEND_DIR = Path(__file__).resolve().parent.parent / "frontend"

# ── Rate Limiter ─────────────────────────────────────────────────
limiter = Limiter(key_func=get_remote_address, default_limits=["100/minute"])


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Crea las tablas de la BD al iniciar si no existen."""
    await create_tables()
    yield


app = FastAPI(
    title="Dragons & IA",
    description="Juego de rol por texto impulsado por Inteligencia Artificial.",
    version="1.0.0",
    lifespan=lifespan,
)

app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# ── Validar JWT secret en producción ────────────────────────────
if not settings.debug:
    if not settings.jwt_secret_key:
        raise RuntimeError(
            "JWT_SECRET_KEY es obligatorio en producción. "
            "Configurá la variable de entorno con al menos 32 caracteres aleatorios."
        )
    if len(settings.jwt_secret_key) < 32:
        raise RuntimeError("JWT_SECRET_KEY debe tener al menos 32 caracteres.")

# ── Security Headers Middleware ────────────────────────────────
@app.middleware("http")
async def security_headers(request: Request, call_next):
    response: Response = await call_next(request)
    # HSTS (solo en prod con HTTPS)
    if not settings.debug:
        response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
    # CSP básica
    response.headers["Content-Security-Policy"] = (
        "default-src 'self'; "
        "script-src 'self' 'unsafe-inline' https://cdn.tailwindcss.com; "
        "style-src 'self' 'unsafe-inline' https://fonts.googleapis.com; "
        "font-src 'self' https://fonts.gstatic.com; "
        "img-src 'self' data:; "
        "connect-src 'self' https://ollama.com;"
    )
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
    response.headers["Permissions-Policy"] = "geolocation=(), microphone=()"
    return response

# ── CORS ───────────────────────────────────────────────────────
_allowed_origins = [
    "http://localhost:3000",
    "http://localhost:8000",
    "http://127.0.0.1:8000",
]
if not settings.debug:
    _allowed_origins.append("https://dragons-ia.onrender.com")
else:
    _allowed_origins.append("*")

app.add_middleware(
    CORSMiddleware,
    allow_origins=_allowed_origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "DELETE"],
    allow_headers=["Content-Type", "Authorization"],
)

# ── Health Check ───────────────────────────────────────────────
@app.get("/health", include_in_schema=False)
async def health_check():
    return {"status": "ok", "service": "dragons-ia"}

@app.get("/ready", include_in_schema=False)
async def readiness_check():
    # Podría verificar conexión a DB aquí
    return {"status": "ready", "service": "dragons-ia"}

# ── Routers de la API ──────────────────────────────────────────
app.include_router(auth.router, prefix="/auth", tags=["Auth"])
app.include_router(characters.router, prefix="/characters", tags=["Characters"])
app.include_router(game.router, prefix="/game", tags=["Game"])

# ── Archivos estáticos del frontend ────────────────────────────
app.mount("/static", StaticFiles(directory=str(FRONTEND_DIR / "static")), name="static")


# ── Servir páginas HTML del frontend ───────────────────────────
@app.get("/", include_in_schema=False)
async def serve_index():
    return FileResponse(str(FRONTEND_DIR / "index.html"))


@app.get("/{page}.html", include_in_schema=False)
async def serve_page(page: str):
    """Sirve cualquier página HTML del frontend."""
    file_path = FRONTEND_DIR / f"{page}.html"
    if file_path.is_file():
        return FileResponse(str(file_path))
    return FileResponse(str(FRONTEND_DIR / "index.html"))
