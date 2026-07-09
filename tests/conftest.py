"""
Fixtures compartidas para todos los tests.

Usa SQLite en memoria + override de dependencia get_db,
sin tocar la base de datos de desarrollo.
"""

# ── ParcheAR slowapi ANTES de importar la app ───────────────────
# Esto deshabilita el rate limiting en todos los endpoints.
# El parche debe ir antes de cualquier import de backend.*
import slowapi.extension as _slow_ext

_original_init = _slow_ext.Limiter.__init__
_original_limit = _slow_ext.Limiter.limit


def _patched_init(self, *args, **kwargs):
    kwargs.setdefault("default_limits", ["10000/minute"])
    _original_init(self, *args, **kwargs)
    self.enabled = False


def _patched_limit(self, limit_value):
    def decorator(func):
        return func
    return decorator


_slow_ext.Limiter.__init__ = _patched_init
_slow_ext.Limiter.limit = _patched_limit

# ── Ahora importar la app ─────────────────────────────────────
import pytest_asyncio
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from backend.database import Base, get_db
from backend.main import app

# ── Base de datos exclusiva para tests ──────────────────────────
TEST_DB_URL = "sqlite+aiosqlite:///./test_dragons_tmp.db"

test_engine = create_async_engine(
    TEST_DB_URL,
    connect_args={"check_same_thread": False},
)
test_session_factory = async_sessionmaker(
    test_engine, class_=AsyncSession, expire_on_commit=False
)


async def override_get_db():
    """Reemplaza get_db con la sesión del engine de test."""
    async with test_session_factory() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()


app.dependency_overrides[get_db] = override_get_db


# ── Ciclo de vida de la BD de test ──────────────────────────────
@pytest_asyncio.fixture(scope="session", autouse=True)
async def _create_test_tables():
    """Crea las tablas antes de la sesión y las elimina al terminar."""
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
    await test_engine.dispose()


# ── Cliente HTTP de test ─────────────────────────────────────────
@pytest_asyncio.fixture
async def client():
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as c:
        yield c


# ── Usuario autenticado ──────────────────────────────────────────
@pytest_asyncio.fixture
async def auth(client: AsyncClient):
    """Registra un usuario de test y devuelve (headers, user_data)."""
    import uuid
    uid = uuid.uuid4().hex[:8]
    payload = {
        "email": f"test_{uid}@example.com",
        "username": f"tester_{uid}",
        "password": "Passw0rd!",
    }
    resp = await client.post("/auth/register", json=payload)
    assert resp.status_code == 201, resp.text
    token = resp.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    return headers, resp.json()["user"]


# ── Personaje de test ────────────────────────────────────────────
CHARACTER_PAYLOAD = {
    "name": "Arix",
    "world": "fantasia",
    "race": "Elfo",
    "gender": "Masculino",
    "character_class": "Mago",
    "unique_object": "Tomo antiguo",
    "stats": {
        "fuerza": 8,
        "destreza": 14,
        "constitucion": 12,
        "inteligencia": 16,
        "sabiduria": 12,
        "carisma": 10,
    },
}
