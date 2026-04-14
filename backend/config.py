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
    jwt_algorithm: str = "HS256"
    jwt_expiration_minutes: int = 1440  # 24 horas

    # --- IA ---
    default_ai_model: str = "gpt-4o-mini"
    openai_api_key: str = ""
    anthropic_api_key: str = ""
    ollama_api_base: str = "http://localhost:11434"

    # --- Servidor ---
    host: str = "0.0.0.0"
    port: int = 8000
    debug: bool = True

    # --- Donaciones ---
    paypal_donate_link: str = ""
    mercadopago_donate_link: str = ""

    model_config = {"env_file": ".env", "env_file_encoding": "utf-8"}

    @property
    def is_sqlite(self) -> bool:
        """Detecta si se está usando SQLite."""
        return "sqlite" in self.database_url


@lru_cache()
def get_settings() -> Settings:
    """Retorna la instancia singleton de configuración."""
    return Settings()
