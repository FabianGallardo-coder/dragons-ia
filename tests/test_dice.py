"""Tests del sistema de dados D&D."""

import pytest

from backend.services.dice import (
    calculate_hp,
    roll_dice,
    roll_stats,
    stat_modifier,
)


class TestRollDice:

    def test_roll_d6_returns_1_to_6(self):
        for _ in range(100):
            r = roll_dice(6, 1)
            assert len(r) == 1
            assert 1 <= r[0] <= 6

    def test_roll_d20_returns_1_to_20(self):
        for _ in range(100):
            r = roll_dice(20, 1)
            assert 1 <= r[0] <= 20

    def test_roll_multiple(self):
        r = roll_dice(6, 4)
        assert len(r) == 4

    def test_invalid_sides(self):
        with pytest.raises(ValueError):
            roll_dice(1)

    def test_invalid_count(self):
        with pytest.raises(ValueError):
            roll_dice(6, 0)


class TestStatModifier:

    def test_stat_10_mod_0(self):
        assert stat_modifier(10) == 0

    def test_stat_8_mod_minus1(self):
        assert stat_modifier(8) == -1

    def test_stat_14_mod_2(self):
        assert stat_modifier(14) == 2

    def test_stat_20_mod_5(self):
        assert stat_modifier(20) == 5

    def test_stat_1_mod_minus5(self):
        assert stat_modifier(1) == -5

    def test_stat_30_mod_10(self):
        assert stat_modifier(30) == 10


class TestCalculateHP:

    def test_barbaro_max_hp(self):
        hp = calculate_hp("Bárbaro", 14)
        assert hp == 12 + stat_modifier(14)

    def test_mago_min_hp(self):
        hp = calculate_hp("Mago", 10)
        assert hp == 6 + stat_modifier(10)

    def test_guerrero(self):
        hp = calculate_hp("Guerrero", 12)
        assert hp == 10 + stat_modifier(12)

    def test_default_class(self):
        hp = calculate_hp("ClaseDesconocida", 10)
        assert hp == 8 + stat_modifier(10)

    def test_minimum_hp(self):
        hp = calculate_hp("Mago", 3)
        assert hp >= 1


class TestRollStats:

    def test_returns_six_stats(self):
        stats = roll_stats()
        assert len(stats) == 6

    def test_all_keys_present(self):
        stats = roll_stats()
        expected = {"fuerza", "destreza", "constitucion", "inteligencia", "sabiduria", "carisma"}
        assert set(stats.keys()) == expected

    def test_stats_in_range(self):
        for _ in range(10):
            stats = roll_stats()
            for name, val in stats.items():
                assert 3 <= val <= 18, f"{name}={val} fuera de rango"
