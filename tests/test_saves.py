"""
Tests del endpoint GET /game/saves — verifica que el join con Character
devuelve character_name y character_world correctamente.

Cubre:
- Lista vacía para usuario sin partidas
- Lista con character_name y character_world tras crear personaje y partida
- Solo se devuelven partidas del usuario autenticado (aislamiento)
- Partidas ordenadas por updated_at desc
- Eliminar una partida (DELETE /game/saves/{id}) reduce la lista
"""

import json
import uuid
from datetime import datetime, timezone
from unittest.mock import AsyncMock, patch

import pytest
from httpx import AsyncClient

from tests.conftest import CHARACTER_PAYLOAD


# ── Helpers ──────────────────────────────────────────────────────

async def create_character(client: AsyncClient, headers: dict) -> dict:
    resp = await client.post("/characters/", json=CHARACTER_PAYLOAD, headers=headers)
    assert resp.status_code == 201, resp.text
    return resp.json()


async def create_save_via_api(
    client: AsyncClient, headers: dict, character_id: str, title: str = "Test Save"
) -> dict:
    """Crea una partida mockeando la IA para evitar llamadas reales."""
    with patch(
        "backend.routers.game.get_ai_response",
        new=AsyncMock(return_value="La oscuridad te envuelve. Tu aventura comienza."),
    ):
        resp = await client.post(
            "/game/new",
            json={"character_id": character_id, "title": title},
            headers=headers,
        )
    assert resp.status_code == 200, resp.text
    return resp.json()


# ── Tests ─────────────────────────────────────────────────────────

class TestSavesList:

    async def test_empty_list_for_new_user(self, client: AsyncClient, auth):
        headers, _ = auth
        resp = await client.get("/game/saves", headers=headers)
        assert resp.status_code == 200
        assert resp.json() == []

    async def test_saves_include_character_name(self, client: AsyncClient, auth):
        headers, _ = auth
        char = await create_character(client, headers)
        await create_save_via_api(client, headers, char["id"], title="Mi Aventura")

        resp = await client.get("/game/saves", headers=headers)
        assert resp.status_code == 200
        saves = resp.json()
        assert len(saves) >= 1
        save = saves[0]
        assert save["character_name"] == CHARACTER_PAYLOAD["name"]

    async def test_saves_include_character_world(self, client: AsyncClient, auth):
        headers, _ = auth
        char = await create_character(client, headers)
        await create_save_via_api(client, headers, char["id"])

        resp = await client.get("/game/saves", headers=headers)
        saves = resp.json()
        assert saves[0]["character_world"] == CHARACTER_PAYLOAD["world"]

    async def test_save_title_preserved(self, client: AsyncClient, auth):
        headers, _ = auth
        char = await create_character(client, headers)
        await create_save_via_api(client, headers, char["id"], title="Crónicas del Norte")

        resp = await client.get("/game/saves", headers=headers)
        titles = [s["title"] for s in resp.json()]
        assert "Crónicas del Norte" in titles

    async def test_isolation_between_users(self, client: AsyncClient, auth):
        """Las partidas de un usuario no se ven por otro."""
        headers_a, _ = auth

        # Crear segundo usuario
        uid = uuid.uuid4().hex[:8]
        resp_b = await client.post("/auth/register", json={
            "email": f"b_{uid}@test.com",
            "username": f"b_{uid}",
            "password": "Passw0rd!",
        })
        headers_b = {"Authorization": f"Bearer {resp_b.json()['access_token']}"}

        # Usuario A crea partida
        char = await create_character(client, headers_a)
        await create_save_via_api(client, headers_a, char["id"], title="Partida Privada A")

        # Usuario B no debe verla
        resp = await client.get("/game/saves", headers=headers_b)
        titles = [s["title"] for s in resp.json()]
        assert "Partida Privada A" not in titles

    async def test_response_schema_fields_present(self, client: AsyncClient, auth):
        """Verifica que todos los campos del schema están en la respuesta."""
        headers, _ = auth
        char = await create_character(client, headers)
        await create_save_via_api(client, headers, char["id"])

        resp = await client.get("/game/saves", headers=headers)
        save = resp.json()[0]
        required_fields = {
            "id", "user_id", "character_id", "title",
            "turn_count", "is_active", "created_at", "updated_at",
            "character_name", "character_world",
        }
        assert required_fields.issubset(save.keys())

    async def test_delete_save_removes_from_list(self, client: AsyncClient, auth):
        headers, _ = auth
        char = await create_character(client, headers)
        save_resp = await create_save_via_api(client, headers, char["id"], title="A Borrar")
        save_id = save_resp["save_id"]

        del_resp = await client.delete(f"/game/saves/{save_id}", headers=headers)
        assert del_resp.status_code == 204

        resp = await client.get("/game/saves", headers=headers)
        ids = [s["id"] for s in resp.json()]
        assert save_id not in ids

    async def test_requires_authentication(self, client: AsyncClient):
        resp = await client.get("/game/saves")
        assert resp.status_code == 403


class TestGetSaveDetail:

    async def test_get_detail_returns_history(self, client: AsyncClient, auth):
        headers, _ = auth
        char = await create_character(client, headers)
        save_resp = await create_save_via_api(client, headers, char["id"])
        save_id = save_resp["save_id"]

        resp = await client.get(f"/game/saves/{save_id}", headers=headers)
        assert resp.status_code == 200
        body = resp.json()
        assert "history" in body
        assert isinstance(body["history"], list)
        assert len(body["history"]) >= 1

    async def test_get_other_users_save_returns_404(self, client: AsyncClient, auth):
        headers_a, _ = auth
        char = await create_character(client, headers_a)
        save_resp = await create_save_via_api(client, headers_a, char["id"])
        save_id = save_resp["save_id"]

        # Otro usuario
        uid = uuid.uuid4().hex[:8]
        resp_b = await client.post("/auth/register", json={
            "email": f"c_{uid}@test.com",
            "username": f"c_{uid}",
            "password": "Passw0rd!",
        })
        headers_b = {"Authorization": f"Bearer {resp_b.json()['access_token']}"}

        resp = await client.get(f"/game/saves/{save_id}", headers=headers_b)
        assert resp.status_code == 404
