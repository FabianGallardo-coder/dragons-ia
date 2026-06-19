"""
Router de sistema — Endpoints de diagnóstico para el frontend.
"""

from fastapi import APIRouter
from backend.services.system_check import check_ollama_status

router = APIRouter(prefix="/api/system", tags=["system"])


@router.get("/ollama-status")
async def ollama_status():
    """
    Retorna el estado actual de Ollama: si está corriendo, qué modelos tiene,
    RAM disponible y modelo recomendado. El frontend lo consume en config.html
    para mostrar diagnóstico claro al usuario en lugar de una lista vacía sin explicación.
    """
    return await check_ollama_status()