"""
Router del juego — Acciones del jugador, nueva partida, guardar/cargar.
"""

import json
import re
from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from slowapi import Limiter
from slowapi.util import get_remote_address

from backend.config import get_settings
from backend.database import get_db
from backend.models.character import Character
from backend.models.save import SaveGame
from backend.models.user import User
from backend.routers.auth import get_current_user
from backend.schemas.game import (
    GameAction,
    GameNewRequest,
    GameResponse,
    HistoryEntry,
    SaveGameDetail,
    SaveGameResponse,
)
from backend.services.ai_service import get_ai_response
from backend.services.dungeon_master import build_system_prompt

router = APIRouter()
settings = get_settings()

game_limiter = Limiter(key_func=get_remote_address, default_limits=["30/minute"])


def _parse_history(history_str: str) -> list[dict]:
    """Parsea el historial JSON de la partida."""
    try:
        return json.loads(history_str) if history_str else []
    except json.JSONDecodeError:
        return []


def _serialize_history(history: list[dict]) -> str:
    """Serializa el historial a JSON string."""
    return json.dumps(history, ensure_ascii=False)


# Regex para parsear la línea [GAME_DATA: ...] del narrative
_GAME_DATA_RE = re.compile(
    r"\[GAME_DATA:\s*hp_change\s*=\s*(-?\d+)\s*,\s*xp_gain\s*=\s*(\d+)\s*,\s*alive\s*=\s*(true|false)\s*\]",
    re.IGNORECASE,
)

# Regex para parsear la línea [SCENE_DATA: ...] del narrative
_SCENE_DATA_RE = re.compile(
    r"\[SCENE_DATA:\s*([^\]]+)\]",
    re.IGNORECASE,
)


def _parse_scene_data(narrative: str) -> dict | None:
    """Extrae datos de escena del narrative.

    Returns:
        Diccionario con los campos de escena, o None si no se encontró.
    """
    match = _SCENE_DATA_RE.search(narrative)
    if not match:
        return None

    raw = match.group(1)
    scene_data = {}
    for pair in raw.split(","):
        pair = pair.strip()
        if "=" in pair:
            key, value = pair.split("=", 1)
            key = key.strip().lower()
            value = value.strip().lower()
            # El campo ambience puede tener múltiples valores separados por ;
            if key == "ambience" and ";" in value:
                scene_data[key] = [v.strip() for v in value.split(";")]
            else:
                scene_data[key] = value
    return scene_data if scene_data else None


def _parse_game_data(narrative: str) -> tuple[str, int, int, bool, dict | None]:
    """Extrae datos de juego y escena del narrative y los limpia.

    Returns:
        (narrative_limpio, hp_change, xp_gain, alive, scene_data)
    """
    # Parsear scene_data antes de limpiar
    scene_data = _parse_scene_data(narrative)

    match = _GAME_DATA_RE.search(narrative)
    if not match:
        # Aún así limpiar SCENE_DATA si existe
        clean = _SCENE_DATA_RE.sub("", narrative).rstrip()
        return clean, 0, 0, True, scene_data

    hp_change = int(match.group(1))
    xp_gain = int(match.group(2))
    alive = match.group(3).lower() == "true"

    # Remover ambas líneas de datos del texto visible
    clean_narrative = _SCENE_DATA_RE.sub("", narrative)
    clean_narrative = _GAME_DATA_RE.sub("", clean_narrative).rstrip()
    return clean_narrative, hp_change, xp_gain, alive, scene_data


def _apply_game_state(character: Character, hp_change: int, xp_gain: int, alive: bool) -> None:
    """Aplica cambios de estado al personaje."""
    character.hp_current = max(0, min(character.hp_max, character.hp_current + hp_change))
    character.experience += xp_gain
    if character.hp_current <= 0 or not alive:
        character.hp_current = 0
        character.is_alive = False


def _char_to_dict(char: Character) -> dict:
    """Convierte Character ORM a dict para el prompt."""
    try:
        stats = json.loads(char.stats) if isinstance(char.stats, str) else char.stats
    except json.JSONDecodeError:
        stats = {}
    return {
        "name": char.name,
        "race": char.race,
        "character_class": char.character_class,
        "unique_object": char.unique_object,
        "stats": stats,
        "hp_current": char.hp_current,
        "hp_max": char.hp_max,
        "level": char.level,
    }


@router.post("/new", response_model=GameResponse)
@game_limiter.limit("10/minute")
async def new_game(
    request: Request,
    data: GameNewRequest,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Inicia una nueva partida: crea el save y genera la escena de apertura."""
    # Buscar el personaje
    result = await db.execute(
        select(Character).where(
            Character.id == data.character_id, Character.user_id == current_user.id
        )
    )
    character = result.scalar_one_or_none()
    if not character:
        raise HTTPException(status_code=404, detail="Personaje no encontrado.")

    if not character.is_alive:
        raise HTTPException(status_code=400, detail="Este personaje ha muerto. Crea uno nuevo.")

    # Construir el system prompt
    char_dict = _char_to_dict(character)
    system_prompt = build_system_prompt(char_dict, character.world)

    messages = [{"role": "system", "content": system_prompt}]

    # Llamar a la IA para la escena de apertura
    try:
        narrative = await get_ai_response(
            messages, model=data.ai_model, api_key=data.api_key
        )
    except RuntimeError as exc:
        raise HTTPException(status_code=502, detail=str(exc))

    # Crear historial inicial
    now = datetime.now(timezone.utc).isoformat()
    history = [
        {"role": "system", "content": system_prompt, "timestamp": now, "dice_roll": None},
        {"role": "assistant", "content": narrative, "timestamp": now, "dice_roll": None},
    ]

    # Crear save game
    save = SaveGame(
        user_id=current_user.id,
        character_id=character.id,
        title=data.title,
        history=_serialize_history(history),
        turn_count=1,
    )
    db.add(save)
    await db.flush()
    await db.refresh(save)

    # Parsear scene_data de la escena de apertura
    clean_narrative, _, _, _, scene_data = _parse_game_data(narrative)

    return GameResponse(
        narrative=clean_narrative,
        save_id=save.id,
        turn_count=save.turn_count,
        character_hp=character.hp_current,
        character_hp_max=character.hp_max,
        character_alive=character.is_alive,
        character_xp=character.experience,
        scene_data=scene_data,
    )


@router.post("/action", response_model=GameResponse)
@game_limiter.limit("30/minute")
async def game_action(
    request: Request,
    data: GameAction,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Procesa una acción del jugador y genera la respuesta del DM."""
    # Buscar save game
    result = await db.execute(
        select(SaveGame).where(
            SaveGame.id == data.save_id, SaveGame.user_id == current_user.id
        )
    )
    save = result.scalar_one_or_none()
    if not save:
        raise HTTPException(status_code=404, detail="Partida no encontrada.")

    if not save.is_active:
        raise HTTPException(status_code=400, detail="Esta partida ha terminado.")

    # Buscar personaje
    result = await db.execute(select(Character).where(Character.id == save.character_id))
    character = result.scalar_one_or_none()
    if not character:
        raise HTTPException(status_code=404, detail="Personaje no encontrado.")

    # Reconstruir mensajes para la IA (solo system + últimos turnos)
    history = _parse_history(save.history)

    # Preparar el mensaje del jugador
    now = datetime.now(timezone.utc).isoformat()
    user_content = data.action
    if data.dice_result is not None:
        user_content += f"\n[Resultado del dado: {data.dice_result}]"

    history.append({
        "role": "user",
        "content": user_content,
        "timestamp": now,
        "dice_roll": data.dice_result,
    })

    # Construir mensajes para la IA (limitar contexto a últimos 20 turnos + system)
    ai_messages = []
    system_msgs = [h for h in history if h["role"] == "system"]
    if system_msgs:
        ai_messages.append({"role": "system", "content": system_msgs[-1]["content"]})

    conversation = [h for h in history if h["role"] != "system"]
    # Mantener los últimos 20 mensajes de conversación
    for msg in conversation[-20:]:
        ai_messages.append({"role": msg["role"], "content": msg["content"]})

    # Llamar a la IA
    try:
        raw_narrative = await get_ai_response(
            ai_messages, model=data.ai_model, api_key=data.api_key
        )
    except RuntimeError as exc:
        raise HTTPException(status_code=502, detail=str(exc))

    # Parsear datos de juego, escena y limpiar el narrative
    narrative, hp_change, xp_gain, alive, scene_data = _parse_game_data(raw_narrative)

    # Actualizar estado del personaje
    _apply_game_state(character, hp_change, xp_gain, alive)

    # Si el personaje muere, desactivar la partida
    if not character.is_alive:
        save.is_active = False

    # Agregar respuesta al historial
    history.append({
        "role": "assistant",
        "content": narrative,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "dice_roll": None,
    })

    # Actualizar save game
    save.history = _serialize_history(history)
    save.turn_count += 1
    save.updated_at = datetime.now(timezone.utc)

    return GameResponse(
        narrative=narrative,
        save_id=save.id,
        turn_count=save.turn_count,
        character_hp=character.hp_current,
        character_hp_max=character.hp_max,
        character_alive=character.is_alive,
        character_xp=character.experience,
        scene_data=scene_data,
    )


@router.get("/saves", response_model=list[SaveGameResponse])
async def list_saves(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
    offset: int = 0,
    limit: int = 50,
):
    """Lista las partidas del usuario con paginación."""
    result = await db.execute(
        select(SaveGame, Character.name, Character.world)
        .join(Character, SaveGame.character_id == Character.id)
        .where(SaveGame.user_id == current_user.id)
        .order_by(SaveGame.updated_at.desc())
        .offset(offset)
        .limit(limit)
    )
    rows = result.all()
    out = []
    for save, char_name, char_world in rows:
        data = SaveGameResponse.model_validate(save)
        data.character_name = char_name
        data.character_world = char_world
        out.append(data)
    return out


@router.get("/saves/{save_id}", response_model=SaveGameDetail)
async def get_save(
    save_id: str,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Obtiene una partida con su historial completo."""
    result = await db.execute(
        select(SaveGame).where(
            SaveGame.id == save_id, SaveGame.user_id == current_user.id
        )
    )
    save = result.scalar_one_or_none()
    if not save:
        raise HTTPException(status_code=404, detail="Partida no encontrada.")

    history = _parse_history(save.history)
    # Filtrar mensajes de sistema del historial visible
    visible_history = [
        HistoryEntry(**h) for h in history if h["role"] != "system"
    ]

    return SaveGameDetail(
        id=save.id,
        user_id=save.user_id,
        character_id=save.character_id,
        title=save.title,
        turn_count=save.turn_count,
        is_active=save.is_active,
        created_at=save.created_at,
        updated_at=save.updated_at,
        history=visible_history,
    )


@router.post("/saves/{save_id}/save", response_model=SaveGameResponse)
async def manual_save(
    save_id: str,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Marca explícitamente una partida como guardada (actualiza timestamp)."""
    result = await db.execute(
        select(SaveGame).where(
            SaveGame.id == save_id, SaveGame.user_id == current_user.id
        )
    )
    save = result.scalar_one_or_none()
    if not save:
        raise HTTPException(status_code=404, detail="Partida no encontrada.")

    save.updated_at = datetime.now(timezone.utc)
    return SaveGameResponse.model_validate(save)


@router.delete("/saves/{save_id}", status_code=204)
async def delete_save(
    save_id: str,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Elimina una partida guardada."""
    result = await db.execute(
        select(SaveGame).where(
            SaveGame.id == save_id, SaveGame.user_id == current_user.id
        )
    )
    save = result.scalar_one_or_none()
    if not save:
        raise HTTPException(status_code=404, detail="Partida no encontrada.")
    await db.delete(save)


@router.get("/ollama/models")
async def list_ollama_models():
    """Lista modelos instalados en Ollama Local."""
    import httpx
    settings = get_settings()
    try:
        async with httpx.AsyncClient(timeout=5.0) as client:
            resp = await client.get(f"{settings.ollama_api_base}/api/tags")
            resp.raise_for_status()
            data = resp.json()
            models = data.get("models", [])
            return [
                {"value": f"ollama/{m['name']}", "label": m['name']}
                for m in models
            ]
    except httpx.ConnectError:
        raise HTTPException(
            status_code=503,
            detail="No se pudo conectar a Ollama Local. Verificá que esté corriendo."
        )
    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=f"Error consultando Ollama: {exc}"
        )


@router.post("/ollama/models/cloud")
async def list_ollama_cloud_models(api_key: str = "", data: dict | None = None):
    """Lista modelos disponibles en Ollama Cloud usando API key."""
    import httpx
    if not api_key and data and "api_key" in data:
        api_key = data["api_key"]
    if not api_key:
        raise HTTPException(status_code=400, detail="API Key es requerida")
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            resp = await client.get(
                "https://ollama.com/v1/models",
                headers={"Authorization": f"Bearer {api_key}"}
            )
            resp.raise_for_status()
            data = resp.json()
            models = data.get("data", [])
            return [
                {"value": f"ollama/{m['id']}", "label": m['id']}
                for m in models
            ]
    except httpx.HTTPStatusError as exc:
        if exc.response.status_code == 401:
            raise HTTPException(
                status_code=401,
                detail="API Key inválida para Ollama Cloud"
            )
        raise HTTPException(
            status_code=exc.response.status_code,
            detail=f"Error de Ollama Cloud: {exc.response.text}"
        )
    except httpx.ConnectError:
        raise HTTPException(
            status_code=503,
            detail="No se pudo conectar a Ollama Cloud. Verificá tu conexión a internet."
        )
    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=f"Error consultando Ollama Cloud: {exc}"
        )
