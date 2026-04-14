"""
Dragons & IA — Conexión async a base de datos con SQLAlchemy 2.0.

Detecta automáticamente si se usa SQLite (desarrollo) o PostgreSQL (producción)
y configura el engine de forma acorde.
"""

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase

from backend.config import get_settings

settings = get_settings()

# Argumentos del engine según el tipo de base de datos
engine_kwargs: dict = {"echo": settings.debug}
if settings.is_sqlite:
    # SQLite necesita check_same_thread=False para async
    engine_kwargs["connect_args"] = {"check_same_thread": False}

engine = create_async_engine(settings.database_url, **engine_kwargs)

async_session = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


class Base(DeclarativeBase):
    """Clase base para todos los modelos SQLAlchemy."""
    pass


async def get_db() -> AsyncSession:
    """Dependency de FastAPI que provee una sesión de base de datos."""
    async with async_session() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()


async def create_tables() -> None:
    """Crea todas las tablas (útil en desarrollo con SQLite)."""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
