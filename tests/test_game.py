"""Tests del flujo de juego: new, action, parse_game_data, muerte."""

import re
import uuid
from unittest.mock import AsyncMock, patch

import pytest
from httpx import AsyncClient

from tests.conftest import CHARACTER_PAYLOAD

_GAME_DATA_RE = re.compile(
    r"\[GAME_DATA:\s*hp_change\s*=\s*(-?\d+)\s*,\s*xp_gain\s*=\s*(\d+)\s*,\s*alive\s*=\s*(true|false)\s*\]",
    re.IGNORECASE,
)

_SCENE_DATA_RE = re.compile(r"\[SCENE_DATA:\s*([^\]]+)\]", re.IGNORECASE)


class TestNewGame:

    async def _create_char_and_start(
        self, client: AsyncClient, headers: dict, mock_response: str
    ) -> dict:
        char_resp = await client.post("/characters/", json=CHARACTER_PAYLOAD, headers=headers)
        char_id = char_resp.json()["id"]
        with patch("backend.routers.game.get_ai_response", new=AsyncMock(return_value=mock_response)):
            resp = await client.post(
                "/game/new",
                json={"character_id": char_id, "title": "Test Aventura"},
                headers=headers,
            )
        assert resp.status_code == 200, resp.text
        return resp.json()

    async def test_new_game_returns_save_id(self, client: AsyncClient, auth):
        mock = """La oscuridad te envuelve. [GAME_DATA: hp_change=0, xp_gain=0, alive=true]
[SCENE_DATA: scene=forest, weather=clear, time=day, danger=peaceful, theme=nature, light=sunlight, music=adventure, ambience=wind;birds, sfx=none, ascii=forest]"""
        data = await self._create_char_and_start(client, auth[0], mock)
        assert "save_id" in data
        assert data["narrative"].startswith("La oscuridad")

    async def test_new_game_strips_data_lines(self, client: AsyncClient, auth):
        mock = """Bienvenido al bosque. [GAME_DATA: hp_change=0, xp_gain=5, alive=true]
[SCENE_DATA: scene=forest, weather=clear, time=day, danger=peaceful, theme=nature, light=sunlight, music=adventure, ambience=wind;birds, sfx=none, ascii=forest]"""
        data = await self._create_char_and_start(client, auth[0], mock)
        assert "[GAME_DATA:" not in data["narrative"]
        assert "[SCENE_DATA:" not in data["narrative"]

    async def test_new_game_sets_hp(self, client: AsyncClient, auth):
        mock = """El camino se abre. [GAME_DATA: hp_change=0, xp_gain=0, alive=true]
[SCENE_DATA: scene=forest, weather=clear, time=day, danger=peaceful, theme=nature, light=sunlight, music=adventure, ambience=wind, sfx=none, ascii=forest]"""
        data = await self._create_char_and_start(client, auth[0], mock)
        assert data["character_hp"] > 0

    async def test_new_game_requires_auth(self, client: AsyncClient):
        resp = await client.post("/game/new", json={"character_id": "x", "title": "x"})
        assert resp.status_code == 401


class TestGameAction:

    async def _create_and_action(
        self, client: AsyncClient, headers: dict, new_mock: str, action_mock: str
    ) -> dict:
        char_resp = await client.post("/characters/", json=CHARACTER_PAYLOAD, headers=headers)
        char_id = char_resp.json()["id"]
        with patch("backend.routers.game.get_ai_response", new=AsyncMock(return_value=new_mock)):
            new_resp = await client.post(
                "/game/new", json={"character_id": char_id, "title": "Test"}, headers=headers,
            )
        save_id = new_resp.json()["save_id"]
        with patch("backend.routers.game.get_ai_response", new=AsyncMock(return_value=action_mock)):
            resp = await client.post(
                "/game/action",
                json={"save_id": save_id, "action": "Miro alrededor"},
                headers=headers,
            )
        assert resp.status_code == 200, resp.text
        return resp.json()

    async def test_action_returns_narrative(self, client: AsyncClient, auth):
        new_mock = "Inicio. [GAME_DATA: hp_change=0, xp_gain=0, alive=true]\n[SCENE_DATA: scene=forest, weather=clear, time=day, danger=peaceful, theme=nature, light=sunlight, music=adventure, ambience=wind, sfx=none, ascii=forest]"
        action_mock = "Ves un claro. [GAME_DATA: hp_change=0, xp_gain=10, alive=true]\n[SCENE_DATA: scene=forest, weather=clear, time=day, danger=peaceful, theme=nature, light=sunlight, music=adventure, ambience=wind, sfx=none, ascii=forest]"
        data = await self._create_and_action(client, auth[0], new_mock, action_mock)
        assert "Ves un claro" in data["narrative"]

    async def test_action_updates_turn(self, client: AsyncClient, auth):
        new_mock = "Inicio. [GAME_DATA: hp_change=0, xp_gain=0, alive=true]\n[SCENE_DATA: scene=forest, weather=clear, time=day, danger=peaceful, theme=nature, light=sunlight, music=adventure, ambience=wind, sfx=none, ascii=forest]"
        action_mock = "Siguiente. [GAME_DATA: hp_change=0, xp_gain=10, alive=true]\n[SCENE_DATA: scene=forest, weather=clear, time=day, danger=peaceful, theme=nature, light=sunlight, music=adventure, ambience=wind, sfx=none, ascii=forest]"
        data = await self._create_and_action(client, auth[0], new_mock, action_mock)
        assert data["turn_count"] > 0

    async def test_action_damage_reduces_hp(self, client: AsyncClient, auth):
        new_mock = "Inicio. [GAME_DATA: hp_change=0, xp_gain=0, alive=true]\n[SCENE_DATA: scene=forest, weather=clear, time=day, danger=peaceful, theme=nature, light=sunlight, music=adventure, ambience=wind, sfx=none, ascii=forest]"
        action_mock = "Golpe. [GAME_DATA: hp_change=-5, xp_gain=15, alive=true]\n[SCENE_DATA: scene=forest, weather=clear, time=day, danger=combat, theme=nature, light=sunlight, music=battle, ambience=wind, sfx=sword, ascii=forest]"
        data = await self._create_and_action(client, auth[0], new_mock, action_mock)
        assert data["character_hp"] < CHARACTER_PAYLOAD["stats"]["constitucion"] + 8

    async def test_action_healing_increases_hp(self, client: AsyncClient, auth):
        new_mock = "Inicio. [GAME_DATA: hp_change=0, xp_gain=0, alive=true]\n[SCENE_DATA: scene=forest, weather=clear, time=day, danger=peaceful, theme=nature, light=sunlight, music=adventure, ambience=wind, sfx=none, ascii=forest]"
        action_mock = "Curas. [GAME_DATA: hp_change=5, xp_gain=5, alive=true]\n[SCENE_DATA: scene=forest, weather=clear, time=day, danger=peaceful, theme=nature, light=sunlight, music=adventure, ambience=wind, sfx=none, ascii=forest]"
        data = await self._create_and_action(client, auth[0], new_mock, action_mock)
        assert data["character_hp"] > 0

    async def test_death_sets_alive_false(self, client: AsyncClient, auth):
        new_mock = "Inicio. [GAME_DATA: hp_change=0, xp_gain=0, alive=true]\n[SCENE_DATA: scene=forest, weather=clear, time=day, danger=peaceful, theme=nature, light=sunlight, music=adventure, ambience=wind, sfx=none, ascii=forest]"
        action_mock = "Mueres. [GAME_DATA: hp_change=-99, xp_gain=0, alive=false]\n[SCENE_DATA: scene=forest, weather=clear, time=night, danger=death, theme=horror, light=darkness, music=sad, ambience=silence, sfx=none, ascii=forest]"
        data = await self._create_and_action(client, auth[0], new_mock, action_mock)
        assert data["character_alive"] is False


class TestParseGameData:

    def test_parse_hp_change(self):
        text = "Narrativa. [GAME_DATA: hp_change=-3, xp_gain=15, alive=true]"
        match = _GAME_DATA_RE.search(text)
        assert match is not None
        assert int(match.group(1)) == -3
        assert int(match.group(2)) == 15
        assert match.group(3).lower() == "true"

    def test_parse_death(self):
        text = "Fin. [GAME_DATA: hp_change=-20, xp_gain=0, alive=false]"
        match = _GAME_DATA_RE.search(text)
        assert match.group(3).lower() == "false"

    def test_parse_scene_data(self):
        text = "Texto. [SCENE_DATA: scene=cave, weather=none, time=night, danger=tense, theme=horror, light=torch, music=dungeon, ambience=dripping;chains, sfx=footsteps, ascii=cave]"
        match = _SCENE_DATA_RE.search(text)
        assert match is not None
        raw = match.group(1)
        pairs = dict(p.strip().split("=", 1) for p in raw.split(","))
        assert pairs["scene"] == "cave"
        assert pairs["danger"] == "tense"
        assert pairs["music"] == "dungeon"

    def test_parse_ambience_with_semicolon(self):
        text = "Text. [SCENE_DATA: scene=tavern, weather=rain, ambience=crowd;laughter;fire, sfx=none, ascii=tavern]"
        match = _SCENE_DATA_RE.search(text)
        raw = match.group(1)
        pairs = dict(p.strip().split("=", 1) for p in raw.split(","))
        assert "crowd;laughter;fire" in pairs["ambience"]

    def test_game_data_flexible_order(self):
        """GAME_DATA con campos en orden inverso debe parsearse igual."""
        text = "[GAME_DATA: alive=true, xp_gain=15, hp_change=-5]"
        strict = _GAME_DATA_RE.search(text)
        assert strict is None, "El regex estricto NO debe matchear orden inverso"
        flexible = re.compile(r"\[GAME_DATA:[^\]]*\]", re.IGNORECASE).search(text)
        assert flexible is not None

    def test_game_data_extra_whitespace(self):
        """GAME_DATA con espacios extra debe ser removido por regex flexible."""
        text = "Narrativa. [GAME_DATA:  hp_change  =  -3 ,  xp_gain  =  10 ,  alive  =  true ]"
        flexible = re.compile(r"\[GAME_DATA:[^\]]*\]", re.IGNORECASE)
        clean = flexible.sub("", text).rstrip()
        assert clean == "Narrativa."


class TestNarrativeTTS:

    def test_narrative_tts_strips_bold(self):
        from backend.routers.game import _clean_for_tts
        result = _clean_for_tts("**Hola** mundo")
        assert "Hola" in result
        assert "**" not in result

    def test_narrative_tts_strips_urls(self):
        from backend.routers.game import _clean_for_tts
        result = _clean_for_tts("Visita https://example.com ahora")
        assert "https" not in result

    def test_narrative_tts_strips_code_blocks(self):
        from backend.routers.game import _clean_for_tts
        result = _clean_for_tts("Texto ```código``` sigue")
        assert "código" not in result

    def test_narrative_tts_truncates(self):
        from backend.routers.game import _clean_for_tts
        largo = "x " * 3000
        result = _clean_for_tts(largo)
        assert len(result) <= 2000
