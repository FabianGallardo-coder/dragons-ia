"""
Router de personajes — CRUD completo.
"""

import json

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.database import get_db
from backend.models.character import Character
from backend.models.user import User
from backend.routers.auth import get_current_user
from backend.schemas.character import CharacterCreate, CharacterEditRequest, CharacterResponse, CharacterStats
from backend.services.dice import calculate_hp

router = APIRouter()


def _character_to_response(char: Character) -> CharacterResponse:
    """Convierte un modelo Character a su schema de respuesta."""
    stats_data = json.loads(char.stats) if isinstance(char.stats, str) else char.stats
    return CharacterResponse(
        id=char.id,
        user_id=char.user_id,
        name=char.name,
        world=char.world,
        race=char.race,
        gender=char.gender,
        character_class=char.character_class,
        unique_object=char.unique_object,
        stats=CharacterStats(**stats_data),
        hp_max=char.hp_max,
        hp_current=char.hp_current,
        level=char.level,
        experience=char.experience,
        is_alive=char.is_alive,
        created_at=char.created_at,
    )


@router.post("/", response_model=CharacterResponse, status_code=201)
async def create_character(
    data: CharacterCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Crea un nuevo personaje para el usuario autenticado."""
    stats_dict = data.stats.model_dump()
    hp = calculate_hp(data.character_class, stats_dict["constitucion"])

    character = Character(
        user_id=current_user.id,
        name=data.name,
        world=data.world,
        race=data.race,
        gender=data.gender,
        character_class=data.character_class,
        unique_object=data.unique_object,
        stats=json.dumps(stats_dict),
        hp_max=hp,
        hp_current=hp,
    )
    db.add(character)
    await db.flush()
    await db.refresh(character)
    return _character_to_response(character)


@router.get("/", response_model=list[CharacterResponse])
async def list_characters(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Lista todos los personajes del usuario."""
    result = await db.execute(
        select(Character).where(Character.user_id == current_user.id)
    )
    characters = result.scalars().all()
    return [_character_to_response(c) for c in characters]


@router.get("/{character_id}", response_model=CharacterResponse)
async def get_character(
    character_id: str,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Obtiene un personaje específico del usuario."""
    result = await db.execute(
        select(Character).where(
            Character.id == character_id, Character.user_id == current_user.id
        )
    )
    character = result.scalar_one_or_none()
    if not character:
        raise HTTPException(status_code=404, detail="Personaje no encontrado.")
    return _character_to_response(character)


@router.put("/{character_id}", response_model=CharacterResponse)
async def update_character(
    character_id: str,
    data: CharacterEditRequest,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Actualiza los datos públicos de un personaje."""
    result = await db.execute(
        select(Character).where(
            Character.id == character_id, Character.user_id == current_user.id
        )
    )
    character = result.scalar_one_or_none()
    if not character:
        raise HTTPException(status_code=404, detail="Personaje no encontrado.")

    update_data = data.model_dump(exclude_unset=True)
    if "stats" in update_data and update_data["stats"] is not None:
        update_data["stats"] = json.dumps(update_data["stats"].model_dump())

    for field, value in update_data.items():
        setattr(character, field, value)

    return _character_to_response(character)


@router.delete("/{character_id}", status_code=204)
async def delete_character(
    character_id: str,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Elimina un personaje del usuario."""
    result = await db.execute(
        select(Character).where(
            Character.id == character_id, Character.user_id == current_user.id
        )
    )
    character = result.scalar_one_or_none()
    if not character:
        raise HTTPException(status_code=404, detail="Personaje no encontrado.")
    await db.delete(character)
