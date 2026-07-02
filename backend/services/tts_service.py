"""
Dragons & IA — TTS Service

Servicio de Text-to-Speech usando Piper TTS local.
Usa el modelo es_MX-claude-high para narración del Dungeon Master.
"""

import asyncio
import io
import subprocess
from pathlib import Path

PIPER_VOICES_DIR = Path(__file__).resolve().parent.parent / "piper_voices"

DEFAULT_VOICE = "es_MX/claude/high/es_MX-claude-high"

_available = None


def is_piper_available() -> bool:
    global _available
    if _available is not None:
        return _available
    try:
        result = subprocess.run(
            ["piper", "--help"],
            capture_output=True, text=True, timeout=5
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
        raise RuntimeError("Piper TTS no está instalado. Usá: pip install piper-tts")

    model_path = get_voice_path(voice)
    if not model_path.exists():
        raise FileNotFoundError(f"Modelo de voz no encontrado: {model_path}")

    buf = io.BytesIO()
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
    }
    if available:
        model_path = get_voice_path()
        result["voice_exists"] = model_path.exists()
    return result
