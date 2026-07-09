"""Tests del servicio TTS (Piper)."""

from unittest.mock import AsyncMock, patch

import pytest
from httpx import AsyncClient


class TestTTSStatus:

    async def test_status_endpoint_returns_json(self, client: AsyncClient, auth):
        resp = await client.get("/api/tts/status")
        assert resp.status_code == 200
        data = resp.json()
        assert "available" in data
        assert "voice" in data
        assert isinstance(data.get("voice", ""), str)


class TestTTSSpeak:

    async def test_speak_endpoint_returns_audio_on_success(self, client: AsyncClient, auth):
        mock_wav = b"\x00" * 44
        with patch(
            "backend.routers.tts.generate_speech",
            new=AsyncMock(return_value=mock_wav),
        ):
            resp = await client.post("/api/tts", json={"text": "Hola mundo"})
        assert resp.status_code == 200
        assert resp.headers["content-type"] == "audio/wav"

    async def test_speak_returns_503_when_unavailable(self, client: AsyncClient, auth):
        with patch(
            "backend.routers.tts.generate_speech",
            new=AsyncMock(side_effect=RuntimeError("TTS no disponible")),
        ):
            resp = await client.post("/api/tts", json={"text": "Hola"})
        assert resp.status_code == 503

    async def test_speak_requires_text(self, client: AsyncClient, auth):
        resp = await client.post("/api/tts", json={})
        assert resp.status_code == 422

    async def test_speak_empty_text_returns_400(self, client: AsyncClient, auth):
        resp = await client.post("/api/tts", json={"text": ""})
        assert resp.status_code == 400


class TestTTSAuth:

    async def test_status_requires_no_auth(self, client: AsyncClient):
        resp = await client.get("/api/tts/status")
        assert resp.status_code == 200
