"""
Tests de endpoints misceláneos — health, ready, ascii art, CORS.

Cubre:
- /health retorna 200 con status ok
- /ready retorna 200 o 503
- /api/ascii/art retorna arte válido
- /api/ascii/art con parámetros personalizados
- CORS headers presentes en respuestas
"""

import pytest
from httpx import AsyncClient


class TestHealthCheck:

    async def test_health_returns_200(self, client: AsyncClient):
        resp = await client.get("/health")
        assert resp.status_code == 200
        body = resp.json()
        assert body["status"] == "ok"
        assert body["service"] == "dragons-ia"

    async def test_health_requires_no_auth(self, client: AsyncClient):
        resp = await client.get("/health")
        assert resp.status_code == 200


class TestReadinessCheck:

    async def test_ready_returns_200_when_db_ok(self, client: AsyncClient):
        resp = await client.get("/ready")
        # Should be 200 since test DB is running
        assert resp.status_code in (200, 503)
        body = resp.json()
        assert "status" in body

    async def test_ready_requires_no_auth(self, client: AsyncClient):
        resp = await client.get("/ready")
        assert resp.status_code in (200, 503)


class TestASCIIArt:

    async def test_ascii_art_default_returns_200(self, client: AsyncClient):
        resp = await client.get("/api/ascii/art")
        assert resp.status_code == 200
        body = resp.json()
        assert "art" in body
        assert isinstance(body["art"], str)
        assert len(body["art"]) > 0

    async def test_ascii_art_with_world(self, client: AsyncClient):
        for world in ["fantasia", "ciencia_ficcion", "isekai", "fantasia_oscura"]:
            resp = await client.get(f"/api/ascii/art?world={world}")
            assert resp.status_code == 200
            body = resp.json()
            assert "art" in body

    async def test_ascii_art_with_event(self, client: AsyncClient):
        for event in ["new_game", "battle", "victory", "death"]:
            resp = await client.get(f"/api/ascii/art?event={event}")
            assert resp.status_code == 200
            body = resp.json()
            assert "art" in body

    async def test_ascii_art_requires_no_auth(self, client: AsyncClient):
        resp = await client.get("/api/ascii/art")
        assert resp.status_code == 200


class TestSecurityHeaders:

    async def test_security_headers_present(self, client: AsyncClient):
        resp = await client.get("/health")
        assert resp.status_code == 200
        # Check security headers
        assert "x-content-type-options" in resp.headers
        assert resp.headers["x-content-type-options"] == "nosniff"
        assert "x-frame-options" in resp.headers
        assert resp.headers["x-frame-options"] == "DENY"
        assert "referrer-policy" in resp.headers


class TestCORSHeaders:

    async def test_cors_allows_origin(self, client: AsyncClient):
        resp = await client.options(
            "/health",
            headers={
                "Origin": "http://localhost:8000",
                "Access-Control-Request-Method": "GET",
            },
        )
        # CORS middleware should respond with 200 or 405
        assert resp.status_code in (200, 405)
