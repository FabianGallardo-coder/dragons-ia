"""
Sistema de dados estilo D&D.

Provee funciones para tirar dados de distintos tipos
y calcular modificadores según las reglas de D&D 5e.
"""

import random


def roll_dice(sides: int, count: int = 1) -> list[int]:
    """Tira `count` dados de `sides` caras. Retorna lista de resultados."""
    if sides < 2 or count < 1:
        raise ValueError("El dado debe tener al menos 2 caras y se debe tirar al menos 1.")
    return [random.randint(1, sides) for _ in range(count)]


def roll_d4(count: int = 1) -> list[int]:
    return roll_dice(4, count)


def roll_d6(count: int = 1) -> list[int]:
    return roll_dice(6, count)


def roll_d8(count: int = 1) -> list[int]:
    return roll_dice(8, count)


def roll_d10(count: int = 1) -> list[int]:
    return roll_dice(10, count)


def roll_d12(count: int = 1) -> list[int]:
    return roll_dice(12, count)


def roll_d20(count: int = 1) -> list[int]:
    return roll_dice(20, count)


def stat_modifier(stat_value: int) -> int:
    """Calcula el modificador de una stat (regla D&D 5e): (stat - 10) // 2."""
    return (stat_value - 10) // 2


def roll_stats() -> dict[str, int]:
    """Genera stats aleatorios: tira 4d6, descarta el menor, por cada stat."""
    stat_names = ["fuerza", "destreza", "constitucion", "inteligencia", "sabiduria", "carisma"]
    stats = {}
    for name in stat_names:
        rolls = roll_d6(4)
        rolls.sort()
        stats[name] = sum(rolls[1:])  # Descarta el menor
    return stats


def calculate_hp(character_class: str, constitucion: int) -> int:
    """Calcula HP máximo inicial según la clase y la constitución."""
    # Dado de vida por clase
    hit_dice = {
        "Guerrero": 10, "Paladín": 10, "Ranger": 10,
        "Mago": 6, "Hechicero": 6, "Brujo": 8,
        "Pícaro": 8, "Bardo": 8, "Monje": 8,
        "Clérigo": 8, "Druida": 8,
        "Bárbaro": 12,
    }
    base_hp = hit_dice.get(character_class, 8)
    return base_hp + stat_modifier(constitucion)
