"""Tests del Dungeon Master: construcción de prompts."""

import json

from backend.services.dungeon_master import build_system_prompt, WORLD_TONE_BLOCKS


CHARACTER_DATA = {
    "name": "Arix",
    "race": "Elfo",
    "character_class": "Mago",
    "unique_object": "Tomo antiguo",
    "stats": json.dumps({"fuerza": 8, "destreza": 14, "constitucion": 12, "inteligencia": 16, "sabiduria": 12, "carisma": 10}),
    "hp_current": 20,
    "hp_max": 20,
    "level": 1,
}


class TestBuildSystemPrompt:

    def test_returns_string(self):
        prompt = build_system_prompt(CHARACTER_DATA, "fantasia")
        assert isinstance(prompt, str)
        assert len(prompt) > 100

    def test_contains_character_name(self):
        prompt = build_system_prompt(CHARACTER_DATA, "fantasia")
        assert "Arix" in prompt

    def test_contains_world_name(self):
        prompt = build_system_prompt(CHARACTER_DATA, "fantasia")
        assert "Fantasía Medieval" in prompt

    def test_contains_scene_data_instructions(self):
        prompt = build_system_prompt(CHARACTER_DATA, "fantasia")
        assert "SCENE_DATA" in prompt

    def test_contains_game_data_instructions(self):
        prompt = build_system_prompt(CHARACTER_DATA, "fantasia")
        assert "GAME_DATA" in prompt

    def test_contains_possible_scenes(self):
        prompt = build_system_prompt(CHARACTER_DATA, "fantasia")
        assert "tavern" in prompt
        assert "forest" in prompt
        assert "dungeon" in prompt

    def test_contains_possible_weather(self):
        prompt = build_system_prompt(CHARACTER_DATA, "fantasia")
        assert "rain" in prompt
        assert "fog" in prompt
        assert "storm" in prompt

    def test_contains_possible_danger_levels(self):
        prompt = build_system_prompt(CHARACTER_DATA, "fantasia")
        assert "peaceful" in prompt
        assert "combat" in prompt
        assert "boss" in prompt
        assert "death" in prompt

    def test_contains_possible_themes(self):
        prompt = build_system_prompt(CHARACTER_DATA, "fantasia")
        assert "fantasy" in prompt
        assert "horror" in prompt
        assert "nature" in prompt
        assert "arcane" in prompt

    def test_all_worlds_have_tone_blocks(self):
        worlds = ["fantasia", "ciencia_ficcion", "isekai", "fantasia_oscura"]
        for w in worlds:
            prompt = build_system_prompt(CHARACTER_DATA, w)
            assert prompt

    def test_fantasia_tone_is_epic(self):
        prompt = build_system_prompt(CHARACTER_DATA, "fantasia")
        assert "épico" in prompt.lower() or "heroico" in prompt.lower()

    def test_fantasia_oscura_tone_is_brutal(self):
        prompt = build_system_prompt(CHARACTER_DATA, "fantasia_oscura")
        assert "muerte" in prompt or "sangre" in prompt

    def test_ciencia_ficcion_tone_is_tech(self):
        prompt = build_system_prompt(CHARACTER_DATA, "ciencia_ficcion")
        assert "tecnológica" in prompt or "tecnología" in prompt

    def test_isekai_tone_has_transport(self):
        prompt = build_system_prompt(CHARACTER_DATA, "isekai")
        assert "transportado" in prompt

    def test_world_tone_blocks_all_present(self):
        expected = ["fantasia", "ciencia_ficcion", "isekai", "fantasia_oscura"]
        for w in expected:
            assert w in WORLD_TONE_BLOCKS, f"Falta tone block: {w}"

    def test_prompt_includes_language(self):
        prompt = build_system_prompt(CHARACTER_DATA, "fantasia", "en")
        assert "en" in prompt

    def test_prompt_includes_hp(self):
        prompt = build_system_prompt(CHARACTER_DATA, "fantasia")
        assert "20" in prompt

    def test_prompt_includes_stats(self):
        prompt = build_system_prompt(CHARACTER_DATA, "fantasia")
        assert "FUE 8" in prompt
        assert "INT 16" in prompt

    def test_prompt_includes_unique_object(self):
        prompt = build_system_prompt(CHARACTER_DATA, "fantasia")
        assert "Tomo antiguo" in prompt


class TestWorldToneBlocks:

    def test_all_blocks_are_strings(self):
        for name, block in WORLD_TONE_BLOCKS.items():
            assert isinstance(block, str), f"{name} no es string"
            assert len(block) > 50, f"{name} demasiado corto"
