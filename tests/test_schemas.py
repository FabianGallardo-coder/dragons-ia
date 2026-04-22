"""
Tests de schemas Pydantic — validan los modelos de datos modificados.

Cubre:
- SaveGameResponse: nuevos campos character_name y character_world opcionales
- CharacterStats: validación del total de puntos ≤ 80
- CharacterCreate: validación del campo world (valores permitidos)
- GameAction: validación de campos obligatorios y límites
"""

import pytest
from pydantic import ValidationError

from backend.schemas.game import GameAction, SaveGameResponse
from backend.schemas.character import CharacterCreate, CharacterStats


# ── SaveGameResponse ─────────────────────────────────────────────

class TestSaveGameResponseSchema:

    def test_new_fields_default_to_none(self):
        """character_name y character_world son opcionales con default None."""
        data = SaveGameResponse(
            id="abc",
            user_id="u1",
            character_id="c1",
            title="Aventura",
            turn_count=3,
            is_active=True,
            created_at="2026-01-01T00:00:00Z",
            updated_at="2026-01-01T00:00:00Z",
        )
        assert data.character_name is None
        assert data.character_world is None

    def test_new_fields_accept_string_values(self):
        """character_name y character_world se almacenan si se proveen."""
        data = SaveGameResponse(
            id="abc",
            user_id="u1",
            character_id="c1",
            title="Aventura",
            turn_count=3,
            is_active=True,
            created_at="2026-01-01T00:00:00Z",
            updated_at="2026-01-01T00:00:00Z",
            character_name="Arix",
            character_world="fantasia",
        )
        assert data.character_name == "Arix"
        assert data.character_world == "fantasia"

    def test_is_active_false_works(self):
        """is_active puede ser False para partidas terminadas."""
        data = SaveGameResponse(
            id="abc",
            user_id="u1",
            character_id="c1",
            title="Caído",
            turn_count=10,
            is_active=False,
            created_at="2026-01-01T00:00:00Z",
            updated_at="2026-01-01T00:00:00Z",
        )
        assert data.is_active is False


# ── CharacterStats ───────────────────────────────────────────────

class TestCharacterStats:

    def test_valid_stats_accepted(self):
        stats = CharacterStats(
            fuerza=10, destreza=10, constitucion=10,
            inteligencia=10, sabiduria=10, carisma=10
        )
        assert stats.fuerza == 10

    def test_total_over_80_raises(self):
        with pytest.raises(ValidationError, match="80"):
            CharacterStats(
                fuerza=18, destreza=18, constitucion=18,
                inteligencia=18, sabiduria=9, carisma=9
            )  # total = 90

    def test_total_exactly_80_accepted(self):
        stats = CharacterStats(
            fuerza=18, destreza=15, constitucion=14,
            inteligencia=13, sabiduria=11, carisma=9
        )  # total = 80
        total = (stats.fuerza + stats.destreza + stats.constitucion +
                 stats.inteligencia + stats.sabiduria + stats.carisma)
        assert total == 80

    def test_stat_below_minimum_raises(self):
        with pytest.raises(ValidationError):
            CharacterStats(fuerza=2)  # mínimo es 3

    def test_stat_above_maximum_raises(self):
        with pytest.raises(ValidationError):
            CharacterStats(fuerza=19)  # máximo es 18


# ── CharacterCreate ──────────────────────────────────────────────

class TestCharacterCreate:

    _valid = {
        "name": "Arix",
        "world": "fantasia",
        "race": "Elfo",
        "gender": "Masculino",
        "character_class": "Mago",
        "unique_object": "Tomo",
        "stats": {
            "fuerza": 8, "destreza": 14, "constitucion": 12,
            "inteligencia": 16, "sabiduria": 12, "carisma": 10,
        },
    }

    def test_valid_worlds_accepted(self):
        for world in ["fantasia", "ciencia_ficcion", "isekai", "fantasia_oscura"]:
            data = {**self._valid, "world": world}
            char = CharacterCreate(**data)
            assert char.world == world

    def test_invalid_world_raises(self):
        with pytest.raises(ValidationError):
            CharacterCreate(**{**self._valid, "world": "western"})

    def test_name_too_short_raises(self):
        with pytest.raises(ValidationError):
            CharacterCreate(**{**self._valid, "name": "A"})  # mínimo 2


# ── GameAction ───────────────────────────────────────────────────

class TestGameAction:

    def test_valid_action(self):
        action = GameAction(save_id="s1", action="Ataco al goblin")
        assert action.dice_result is None
        assert action.ai_model is None

    def test_action_empty_raises(self):
        with pytest.raises(ValidationError):
            GameAction(save_id="s1", action="")

    def test_action_too_long_raises(self):
        with pytest.raises(ValidationError):
            GameAction(save_id="s1", action="x" * 1001)

    def test_dice_result_optional(self):
        action = GameAction(save_id="s1", action="Ataco", dice_result=17)
        assert action.dice_result == 17
