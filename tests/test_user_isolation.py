"""Tests de aislamiento entre usuarios: datos de un usuario no visibles por otro."""

import uuid
from unittest.mock import AsyncMock, patch

from httpx import AsyncClient

from tests.conftest import CHARACTER_PAYLOAD

ISOLATION_SCENES = [
    "characters", "game/saves",
]


async def _register_user(client: AsyncClient, tag: str):
    uid = uuid.uuid4().hex[:8]
    resp = await client.post("/auth/register", json={
        "email": f"{tag}_{uid}@test.com",
        "username": f"{tag}_{uid}",
        "password": "Passw0rd!",
    })
    token = resp.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


class TestUserIsolation:

    async def _ensure_scene_isolation(self, client, endpoint, tag_a, tag_b):
        headers_a = await _register_user(client, tag_a)
        headers_b = await _register_user(client, tag_b)

        char = (await client.post("/characters/", json=CHARACTER_PAYLOAD, headers=headers_a)).json()
        with patch("backend.routers.game.get_ai_response", new=AsyncMock(return_value="Inicio. [GAME_DATA: hp_change=0, xp_gain=0, alive=true]\n[SCENE_DATA: scene=forest, weather=clear, time=day, danger=peaceful, theme=nature, light=sunlight, music=adventure, ambience=wind, sfx=none, ascii=forest]")):
            await client.post("/game/new", json={"character_id": char["id"], "title": "Privada"}, headers=headers_a)

        resp = await client.get(f"/{endpoint}", headers=headers_b)
        assert resp.status_code == 200
        data = resp.json()
        if isinstance(data, list):
            assert len(data) == 0, f"{endpoint}: B ve datos de A"

    async def test_characters_isolation(self, client: AsyncClient):
        headers_a = await _register_user(client, "ca")
        headers_b = await _register_user(client, "cb")
        await client.post("/characters/", json=CHARACTER_PAYLOAD, headers=headers_a)
        resp = await client.get("/characters/", headers=headers_b)
        assert resp.status_code == 200
        assert len(resp.json()) == 0

    async def test_saves_isolation(self, client: AsyncClient):
        await self._ensure_scene_isolation(client, "game/saves", "sa", "sb")

    async def test_character_detail_isolation(self, client: AsyncClient):
        headers_a = await _register_user(client, "cda")
        headers_b = await _register_user(client, "cdb")

        created = (await client.post("/characters/", json=CHARACTER_PAYLOAD, headers=headers_a)).json()
        resp = await client.get(f"/characters/{created['id']}", headers=headers_b)
        assert resp.status_code == 404

    async def test_save_detail_isolation(self, client: AsyncClient):
        headers_a = await _register_user(client, "sda")
        headers_b = await _register_user(client, "sdb")

        char = (await client.post("/characters/", json=CHARACTER_PAYLOAD, headers=headers_a)).json()
        with patch("backend.routers.game.get_ai_response", new=AsyncMock(return_value="Inicio. [GAME_DATA: hp_change=0, xp_gain=0, alive=true]\n[SCENE_DATA: scene=forest, weather=clear, time=day, danger=peaceful, theme=nature, light=sunlight, music=adventure, ambience=wind, sfx=none, ascii=forest]")):
            save = await client.post("/game/new", json={"character_id": char["id"], "title": "Privada"}, headers=headers_a)

        resp = await client.get(f"/game/saves/{save.json()['save_id']}", headers=headers_b)
        assert resp.status_code == 404
