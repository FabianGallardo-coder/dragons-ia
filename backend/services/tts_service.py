"""
Dragons & IA — TTS Service

Servicio de Text-to-Speech usando Piper TTS.
Soporta modo local (subprocess) y remoto (HTTP vía TTS_URL).
"""

import asyncio
import io
import os
import subprocess
from pathlib import Path

import httpx

PIPER_VOICES_DIR = Path(__file__).resolve().parent.parent / "piper_voices"
DEFAULT_VOICE = os.getenv("TTS_VOICE", "es_MX/claude/high/es_MX-claude-high")
TTS_URL = os.getenv("TTS_URL", "")
TTS_ENABLED = os.getenv("TTS_ENABLED", "").lower() in ("true", "1", "yes")

_available = None


def is_piper_available() -> bool:
    global _available
    if _available is not None:
        return _available
    if not TTS_ENABLED:
        _available = False
        return False
    if TTS_URL:
        _available = True
        return True
    try:
        result = subprocess.run(
            ["piper", "--help"],
            capture_output=True, text=True, timeout=5,
        )
        _available = result.returncode == 0
    except (FileNotFoundError, subprocess.TimeoutExpired):
        _available = False
    return _available


def get_voice_path(voice: str | None = None) -> Path:
    voice = voice or DEFAULT_VOICE
    return PIPER_VOICES_DIR / f"{voice}.onnx"


async def generate_speech(text: str, voice: str | None = None) -> bytes:
    if not is_piper_available():
        raise RuntimeError("TTS no está disponible. Configurá TTS_ENABLED=true y TTS_URL o instalá piper-tts")

    voice = voice or DEFAULT_VOICE

    if TTS_URL:
        return await _generate_via_http(text, voice)

    return await _generate_via_subprocess(text, voice)


async def _generate_via_http(text: str, voice: str) -> bytes:
    async with httpx.AsyncClient(base_url=TTS_URL, timeout=30) as client:
        resp = await client.post("/synthesize", json={"text": text, "voice": voice})
        resp.raise_for_status()
        return resp.content


async def _generate_via_subprocess(text: str, voice: str) -> bytes:
    model_path = get_voice_path(voice)
    if not model_path.exists():
        raise FileNotFoundError(f"Modelo de voz no encontrado: {model_path}")

    proc = await asyncio.create_subprocess_exec(
        "piper",
        "--model", str(model_path),
        "--output-raw",
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    stdout, stderr = await proc.communicate(input=text.encode("utf-8"))
    if proc.returncode != 0:
        raise RuntimeError(f"Piper TTS error: {stderr.decode()}")
    return stdout


async def get_piper_status() -> dict:
    available = is_piper_available()
    result = {
        "available": available,
        "voice": DEFAULT_VOICE,
        "voice_path": str(get_voice_path()),
        "mode": "http" if TTS_URL else "local",
        "tts_enabled": TTS_ENABLED,
    }
    if available and not TTS_URL:
        model_path = get_voice_path()
        result["voice_exists"] = model_path.exists()
    return result
