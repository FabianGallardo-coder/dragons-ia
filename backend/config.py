"""
Dragons & IA — Configuración centralizada.

Lee variables de entorno desde .env y expone la configuración
como un singleton de Pydantic Settings.
"""

from functools import lru_cache
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Configuración de la aplicación cargada desde variables de entorno."""

    # --- Base de datos ---
    database_url: str = "sqlite+aiosqlite:///./dragons_ia.db"

    # --- JWT ---
    jwt_secret_key: str = "cambia-esto-por-un-secreto-largo-y-aleatorio"
    # IMPORTANTE: En producción, configurar JWT_SECRET_KEY como variable de entorno
    # con al menos 32 caracteres aleatorios.
    jwt_algorithm: str = "HS256"
    jwt_expiration_minutes: int = 1440  # 24 horas

    # --- IA ---
    default_ai_model: str = "claude-3-haiku-20240307"
    anthropic_api_key: str = ""
    ollama_api_base: str = "http://localhost:11434"
    ollama_api_key: str = ""

    # --- Servidor ---
    host: str = "0.0.0.0"
    port: int = 8000
    debug: bool = True

    # --- Donaciones ---
    paypal_donate_link: str = "https://www.paypal.com/donate/?hosted_button_id=XCAMDQPB9GMC4"
    mercadopago_donate_link: str = "https://link.mercadopago.com.ar/dragonsandia"

    model_config = {"env_file": ".env", "env_file_encoding": "utf-8"}

    @property
    def is_sqlite(self) -> bool:
        """Detecta si se está usando SQLite."""
        return "sqlite" in self.database_url

    @property
    def async_database_url(self) -> str:
        """Convierte la URL de BD al formato async correspondiente.

        Render provee `postgresql://...` pero SQLAlchemy async necesita
        `postgresql+asyncpg://...`. Esta propiedad hace la conversión automática.
        """
        url = self.database_url
        if url.startswith("postgres://"):
            url = url.replace("postgres://", "postgresql+asyncpg://", 1)
        elif url.startswith("postgresql://"):
            url = url.replace("postgresql://", "postgresql+asyncpg://", 1)
        return url


@lru_cache()
def get_settings() -> Settings:
    """Retorna la instancia singleton de configuración."""
    return Settings()
