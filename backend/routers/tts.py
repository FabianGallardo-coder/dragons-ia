"""
Dragons & IA — Router TTS

Endpoints para Text-to-Speech usando Piper TTS local.
"""

from fastapi import APIRouter, HTTPException
from fastapi.responses import Response
from pydantic import BaseModel

from backend.services.tts_service import generate_speech, get_piper_status

router = APIRouter(prefix="/api/tts", tags=["tts"])


class TTSRequest(BaseModel):
    text: str
    voice: str | None = None


@router.get("/status")
async def tts_status():
    """
    Retorna el estado del servicio TTS (si Piper está disponible).
    """
    return await get_piper_status()


@router.post("")
async def text_to_speech(req: TTSRequest):
    """
    Genera audio WAV a partir de texto usando Piper TTS.
    """
    if not req.text.strip():
        raise HTTPException(status_code=400, detail="El texto no puede estar vacío")

    try:
        audio_bytes = await generate_speech(req.text, req.voice)
        return Response(content=audio_bytes, media_type="audio/wav")
    except RuntimeError as e:
        raise HTTPException(status_code=503, detail=str(e))
    except FileNotFoundError as e:
        raise HTTPException(status_code=500, detail=str(e))
