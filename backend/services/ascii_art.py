"""
ASCII Art Service — Banners figlet + arte temático por mundo y evento.

Genera arte ASCII con la librería `art` (figlet fonts) y piezas
personalizadas según el mundo de la partida y el tipo de evento.
"""

from art import text2art

# ── Fonts figlet por mundo ───────────────────────────────────────
WORLD_FONTS: dict[str, str] = {
    "fantasia": "block",
    "ciencia_ficcion": "cyberlarge",
    "isekai": "banner4",
    "fantasia_oscura": "starwars",
}

# ── Títulos de evento (se pasan a figlet) ────────────────────────
EVENT_TITLES: dict[str, str] = {
    "new_game": "Nueva Aventura",
    "battle": "Combate",
    "victory": "Victoria",
    "death": "Has Muerto",
    "scene": "Cambio de Escena",
    "rest": "Descanso",
}

# ── Separadores decorativos por mundo ────────────────────────────
SEPARATORS: dict[str, str] = {
    "fantasia": "~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~",
    "ciencia_ficcion": "= = = = = = = = = = = = = = =",
    "isekai": "* * * * * * * * * * * * * * *",
    "fantasia_oscura": "# # # # # # # # # # # # # # #",
}

# ── Piezas de arte ASCII por mundo × evento ─────────────────────
WORLD_ART: dict[str, dict[str, str]] = {
    "fantasia": {
        "new_game": (
            "              _--._            _.--_          \n"
            "             /    _\\\\\\      ///_    \\         \n"
            "            /   _//.-.\\\\  //.-.\\\\_   \\        \n"
            "           |   | |__| |  || |__| |   |       \n"
            "            \\  \\\\___//    \\\\___//  /        \n"
            "             \"-._   \"-..-..-\"   _.-\"         \n"
            "                 \"-._  \"\"\"\"  _.-\"            \n"
            "                     \"\"--\"\"                \n"
        ),
        "battle": (
            "           \\                               \n"
            "            \\    |\\_______________/|       \n"
            "            /    | |  ___________  |        \n"
            "           /_    | | |           | |        \n"
            "          /  |   | | |    EPIC    | |       \n"
            "         /   |   | | |   BATTLE   | |       \n"
            "        /    |   | | |___________| |        \n"
            "             |  /|________________/|        \n"
            "              \\/                        \n"
        ),
        "victory": (
            "         __                                   \n"
            "        / _| VICTORY AWAITS                   \n"
            "   __ _| |_                                  \n"
            "  / _` |  _|                                 \n"
            " | (_| | |                                   \n"
            "  \\__,_|_|                                   \n"
        ),
        "death": (
            "         _____                               \n"
            "        /     \\                              \n"
            "       |  RIP  |                             \n"
            "       |  _  | |                             \n"
            "       | | | | |                             \n"
            "       | |_| | |                             \n"
            "       |      |                              \n"
            "       |______|                              \n"
        ),
        "scene": (
            "          .'''''''.                          \n"
            "        .'         '.                        \n"
            "       /             \\                       \n"
            "      |   THE WORLD  |                       \n"
            "       \\   AWAITS   /                       \n"
            "        '.         .'                        \n"
            "          '.......'                          \n"
        ),
        "rest": (
            "                                              \n"
            "           (   )                              \n"
            "        (         )                           \n"
            "       (   ====   )                          \n"
            "        (  ====  )                           \n"
            "          (    )                              \n"
            "           /===\\                             \n"
            "          /     \\                            \n"
        ),
    },
    "ciencia_ficcion": {
        "new_game": (
            "          /\\                                  \n"
            "         /  \\     ___________________        \n"
            "        / /\\ \\   |  SYSTEM ONLINE     |      \n"
            "       / /__\\ \\  | NEW GAME INITIATED |     \n"
            "      /________\\ |___________________|      \n"
            "       |    |                                \n"
            "       |____|                                \n"
        ),
        "battle": (
            "       _______________                        \n"
            "      |               |                       \n"
            "      |  COMBAT MODE  |                       \n"
            "      |   INITIATED   |                       \n"
            "      |_______________|                       \n"
            "             ||                               \n"
            "             ||                               \n"
        ),
        "victory": (
            "       ><>   ><>   ><>                       \n"
            "      VICTORY SEQUENCE COMPLETE              \n"
            "       ><>   ><>   ><>                       \n"
        ),
        "death": (
            "      [  SYSTEM FAILURE  ]                   \n"
            "      [  CHARACTER KIA   ]                   \n"
            "      [__________________]                   \n"
        ),
        "scene": (
            "      >>> TRANSMISSION <<<                    \n"
            "      _____________________                   \n"
        ),
        "rest": (
            "     [ STASIS CHAMBER ]                      \n"
            "     [   CHARGING...   ]                     \n"
        ),
    },
    "isekai": {
        "new_game": (
            "          \\    |    /                         \n"
            "           \\   |   /                          \n"
            "        ----(((|)))----                       \n"
            "           /   |   \\                          \n"
            "          /    |    \\                         \n"
            "               |                               \n"
            "         PORTAL OPENED                        \n"
        ),
        "battle": (
            "        ✦ ✦ ✦ ✦ ✦ ✦ ✦                      \n"
            "        ✦  MAGIC BATTLE  ✦                    \n"
            "        ✦ ✦ ✦ ✦ ✦ ✦ ✦                      \n"
        ),
        "victory": (
            "      ✦  ✦  ✦  ✦  ✦                         \n"
            "      ✦  VICTORY!  ✦                         \n"
            "      ✦  ✦  ✦  ✦  ✦                         \n"
        ),
        "death": (
            "             .  .  .                          \n"
            "          .           .                       \n"
            "        .    RETURN    .                      \n"
            "          .   HOME   .                       \n"
            "             .  .  .                          \n"
        ),
        "scene": (
            "        ✦  A new world ✦                     \n"
            "        ✦  unfolds...  ✦                     \n"
        ),
        "rest": (
            "        (￣ω￣)                               \n"
            "        ～ Healing... ～                      \n"
        ),
    },
    "fantasia_oscura": {
        "new_game": (
            "                                              \n"
            "      .    .    .    .    .                   \n"
            "    .    .    .    .    .    .                \n"
            "      .    THE DARKNESS                     \n"
            "    .    .  AWAKENS  .    .                  \n"
            "      .    .    .    .    .                   \n"
        ),
        "battle": (
            "           BLOOD MOON RISES                  \n"
            "                                              \n"
            "           \\\\\\///                          \n"
            "          ///( )\\\\\\                         \n"
            "             | |                               \n"
            "            /   \\                             \n"
        ),
        "victory": (
            "          T H E   A B Y S S                  \n"
            "          H A S   F A L L E N                \n"
        ),
        "death": (
            "         ╔══════════════╗                    \n"
            "         ║  T H E   E N D║                   \n"
            "         ╚══════════════╝                    \n"
            "         HERE LIES YOUR SOUL                 \n"
        ),
        "scene": (
            "          T H E   V O I D                    \n"
            "          C A L L S   Y O U                  \n"
        ),
        "rest": (
            "       \\\\\\\\  BLOOD REST  ////             \n"
            "        \\\\\\\\  ////                         \n"
        ),
    },
}


def _get_font(world: str) -> str:
    """Retorna la fuente figlet para el mundo dado."""
    return WORLD_FONTS.get(world, "standard")


def _get_separator(world: str) -> str:
    """Retorna el separador decorativo para el mundo dado."""
    return SEPARATORS.get(world, "- - - - - - - - - - - - - - -")


def get_ascii_art(world: str, event: str) -> dict[str, str]:
    """Genera el arte ASCII completo para un evento en un mundo.

    Args:
        world: Clave del mundo (fantasia, ciencia_ficcion, isekai, fantasia_oscura).
        event: Clave del evento (new_game, battle, victory, death, scene, rest).

    Returns:
        Diccionario con:
          - "figlet": Banner figlet del título del evento.
          - "art":    Pieza de arte ASCII temática.
          - "separator": Separador decorativo.
          - "combined": Todo combinado en un solo string.
    """
    font = _get_font(world)
    title = EVENT_TITLES.get(event, event.replace("_", " ").title())
    separator = _get_separator(world)

    figlet_banner = text2art(title, font=font)

    world_events = WORLD_ART.get(world, {})
    art_piece = world_events.get(event, "")

    combined = "\n".join([
        separator,
        figlet_banner.rstrip("\n"),
        art_piece.rstrip("\n"),
        separator,
    ])

    return {
        "figlet": figlet_banner,
        "art": art_piece,
        "separator": separator,
        "combined": combined,
    }
