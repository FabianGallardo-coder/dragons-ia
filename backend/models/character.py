"""Modelo de personaje del jugador."""

import uuid
from datetime import datetime, timezone

from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import Optional

from backend.database import Base


class Character(Base):
    __tablename__ = "characters"

    id: Mapped[str] = mapped_column(
        String(36), primary_key=True, default=lambda: str(uuid.uuid4())
    )
    user_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    world: Mapped[str] = mapped_column(String(50), nullable=False)
    race: Mapped[str] = mapped_column(String(50), nullable=False)
    gender: Mapped[str] = mapped_column(String(30), nullable=False)
    character_class: Mapped[str] = mapped_column(String(50), nullable=False)
    unique_object: Mapped[str] = mapped_column(String(200), nullable=False)
    # Stats almacenados como JSON string
    stats: Mapped[str] = mapped_column(Text, nullable=False)
    hp_max: Mapped[int] = mapped_column(Integer, nullable=False, default=20)
    hp_current: Mapped[int] = mapped_column(Integer, nullable=False, default=20)
    level: Mapped[int] = mapped_column(Integer, default=1)
    experience: Mapped[int] = mapped_column(Integer, default=0)
    is_alive: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)
    )
    updated_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True), onupdate=lambda: datetime.now(timezone.utc), nullable=True
    )

    # Relaciones
    user = relationship("User", back_populates="characters")
    save_games = relationship("SaveGame", back_populates="character", cascade="all, delete-orphan")

    def __repr__(self) -> str:
        return f"<Character {self.name} ({self.character_class}, {self.world})>"
