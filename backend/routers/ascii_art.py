"""
Router de arte ASCII — Sirve banners figlet y arte temático al frontend.
"""

from fastapi import APIRouter, Query

from backend.services.ascii_art import get_ascii_art

router = APIRouter()


@router.get("/ascii/art")
async def ascii_art(
    event: str = Query(default="new_game", description="Tipo de evento"),
    world: str = Query(default="fantasia", description="Mundo del personaje"),
):
    """Retorna arte ASCII temático para un evento y mundo dados."""
    return get_ascii_art(world, event)
