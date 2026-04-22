"""Schemas Pydantic para el juego y partidas."""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class GameAction(BaseModel):
    """Acción del jugador enviada al DM."""
    save_id: str
    action: str = Field(min_length=1, max_length=1000)
    dice_result: Optional[int] = None
    # Configuración de IA opcional por acción
    ai_model: Optional[str] = None
    api_key: Optional[str] = None


class GameNewRequest(BaseModel):
    """Solicitud para iniciar una nueva partida."""
    character_id: str
    title: str = Field(min_length=1, max_length=200, default="Nueva Aventura")
    # Configuración de IA opcional por partida
    ai_model: Optional[str] = None
    api_key: Optional[str] = None


class HistoryEntry(BaseModel):
    """Una entrada en el historial de la partida."""
    role: str  # "user", "assistant", "system"
    content: str
    timestamp: str
    dice_roll: Optional[int] = None


class GameResponse(BaseModel):
    """Respuesta del DM a una acción."""
    narrative: str
    save_id: str
    turn_count: int
    character_hp: int
    character_hp_max: int
    character_alive: bool
    character_xp: int = 0


class SaveGameResponse(BaseModel):
    """Schema de respuesta de partida guardada."""
    id: str
    user_id: str
    character_id: str
    title: str
    turn_count: int
    is_active: bool
    created_at: datetime
    updated_at: datetime
    character_name: str | None = None
    character_world: str | None = None

    model_config = {"from_attributes": True}


class SaveGameDetail(SaveGameResponse):
    """Partida guardada con historial completo."""
    history: list[HistoryEntry]
