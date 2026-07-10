"""Schemas Pydantic para personajes."""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field, model_validator


class CharacterStats(BaseModel):
    """Stats del personaje estilo D&D 5e."""
    fuerza: int = Field(ge=3, le=18, default=10)
    destreza: int = Field(ge=3, le=18, default=10)
    constitucion: int = Field(ge=3, le=18, default=10)
    inteligencia: int = Field(ge=3, le=18, default=10)
    sabiduria: int = Field(ge=3, le=18, default=10)
    carisma: int = Field(ge=3, le=18, default=10)

    @model_validator(mode="after")
    def validate_total(self):
        total = self.fuerza + self.destreza + self.constitucion + self.inteligencia + self.sabiduria + self.carisma
        if total > 80:
            raise ValueError(f"Total de stats ({total}) supera el máximo permitido de 80.")
        return self


class CharacterCreate(BaseModel):
    """Schema para crear un personaje."""
    name: str = Field(min_length=2, max_length=100)
    world: str = Field(pattern=r"^(fantasia|ciencia_ficcion|isekai|fantasia_oscura)$")
    race: str = Field(min_length=2, max_length=50)
    gender: str = Field(min_length=1, max_length=30)
    character_class: str = Field(min_length=2, max_length=50)
    unique_object: str = Field(min_length=2, max_length=200)
    stats: CharacterStats


class CharacterResponse(BaseModel):
    """Schema de respuesta de personaje."""
    id: str
    user_id: str
    name: str
    world: str
    race: str
    gender: str
    character_class: str
    unique_object: str
    stats: CharacterStats
    hp_max: int
    hp_current: int
    level: int
    experience: int
    is_alive: bool
    created_at: datetime

    model_config = {"from_attributes": True}


class CharacterEditRequest(BaseModel):
    """Schema para editar datos públicos del personaje."""
    name: Optional[str] = Field(None, min_length=2, max_length=100)
    world: Optional[str] = Field(None, pattern=r"^(fantasia|ciencia_ficcion|isekai|fantasia_oscura)$")
    race: Optional[str] = Field(None, min_length=2, max_length=50)
    gender: Optional[str] = Field(None, min_length=1, max_length=30)
    character_class: Optional[str] = Field(None, min_length=2, max_length=50)
    unique_object: Optional[str] = Field(None, min_length=2, max_length=200)
    stats: Optional[CharacterStats] = None
