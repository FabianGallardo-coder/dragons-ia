"""
ASCII art for Dragons & IA game.
Displays different ASCII art based on game worlds/scenarios.
"""

# Dragon art (default/fantasy)
DRAGON_ART = """
              /\\_/\\
             ( o.o )
              > ^ <
              / \\
             /   \\
            /     \\
           /       \\
          /         \\
         /           \\
        /             \\
       /               \\
      /                 \\
     /                   \\
    /                     \\
   /                       \\
  /                         \\
 /                           \\
/                             \\
"""

# Wizard staff for fantasy magic
WIZARD_STAFF_ART = """
                  __
                 /  \\
                /    \\
               /      \\
              /        \\
             /  __  __ \\
            /  /  \\/  \\ \\
           /  /        \\  \\
          /  /          \\  \\
         /  /            \\  \\
        /  /              \\  \\
       /  /                \\  \\
      /  /                  \\  \\
     /__/                    \\__\\
"""

# Spaceship for sci-fi
SPACESHIP_ART = """
                   /\\
                  /  \\
                 /    \\
                /      \\
               /        \\
              /  _____  \\
             /  /     \\  \\
            /  /       \\  \\
           /  /         \\  \\
          /  /           \\  \\
         /  /             \\  \\
        /  /               \\  \\
       /  /                 \\  \\
      /__/                   \\__\\
     _________________________
    |                         |
    |        SPACESHIP        |
    |_________________________|
"""

# Portal for isekai (another world)
PORTAL_ART = """
              .-=========-.
            .'           `.
           /             \\
          |   .-------.   |
          |   |       |   |
          |   |       |   |
          |   `-------'   |
           \\             /
            `._       _,'
              `-.....-'
"""

# Dark castle for dark fantasy
DARK_CASTLE_ART = """
              /\\_/\\
             ( o.o )
              > ^ <
              /|\\
             / | \\
            /  |  \\
           /   |   \\
          /    |    \\
         /     |     \\
        /      |      \\
       /       |       \\
      /        |        \\
     /         |         \\
    /__________|__________\\
       ||||||||||||||||
       ||||||||||||||||
       ||||||||||||||||
"""

# Game title art (shared)
GAME_TITLE_ART = """
  ____        _   _ ____  ____
 |  _ \\ _   _| |_| |  _ \\| ___|
 | |_) | | | | __| | |_) |___ \\
 |  __/|_| |_| |_| |  _ < ___) |
 |_|    \\__,_|\\__|_|_| \\_\\____/

  ____                  _   _ _____ _____ ____
 |  _ \\ ___ _ __ ___ __| |_(_)___ /|_   _|___ \\
 | |_) / _ \\ '__/ __/ _` | __| | |_ \\  | |   __) |
 |  __/  __/ | | (_| (_| | |_| | ___) | |  / __/
 |_|   \\___|_|  \\___\\__,_|\\__|_|____/ |_| |_____|
"""

def print_dragon():
    """Print the dragon ASCII art (default fantasy)."""
    print(DRAGON_ART)

def print_wizard_staff():
    """Print wizard staff ASCII art for magic/fantasy scenarios."""
    print(WIZARD_STAFF_ART)

def print_spaceship():
    """Print spaceship ASCII art for sci-fi scenarios."""
    print(SPACESHIP_ART)

def print_portal():
    """Print portal ASCII art for isekai/another world scenarios."""
    print(PORTAL_ART)

def print_dark_castle():
    """Print dark castle ASCII art for dark fantasy scenarios."""
    print(DARK_CASTLE_ART)

def print_game_title():
    """Print the game title ASCII art."""
    print(GAME_TITLE_ART)

def print_world_art(world):
    """
    Print ASCII art specific to the selected game world.

    Args:
        world (str): The world key (fantasia, ciencia_ficcion, isekai, fantasia_oscura)
    """
    world_arts = {
        'fantasia': print_dragon,  # Default to dragon for general fantasy
        'ciencia_ficcion': print_spaceship,
        'isekai': print_portal,
        'fantasia_oscura': print_dark_castle
    }

    art_func = world_arts.get(world, print_dragon)  # Default to dragon
    art_func()

def print_welcome_banner(world=None):
    """Print a welcome banner with optional world-specific art."""
    print("=" * 60)
    print("  Welcome to Dragons & IA!")
    print("=" * 60)

    if world:
        print(f"  Selected World: {world.replace('_', ' ').title()}")
        print("-" * 60)
        print_world_art(world)
        print()
    else:
        print_dragon()
        print()

    print_game_title()
    print()
    print("Get ready for an epic adventure!")
    print("=" * 60)
    print()

def print_scenario_art(scenario):
    """
    Print ASCII art for specific game scenarios.

    Args:
        scenario (str): Scenario type (start, battle, victory, defeat, etc.)
    """
    scenario_arts = {
        'start': lambda: print_welcome_banner(),
        'battle': lambda: print("***  BATTLE MODE  ***\n"),
        'victory': lambda: print("***  VICTORY!  ***\n"),
        'defeat': lambda: print("!!!  DEFEAT  !!!\n"),
        'exploration': lambda: print("***  EXPLORING...  ***\n"),
        'rest': lambda: print("***  RESTING...  ***\n")
    }

    art_func = scenario_arts.get(scenario, lambda: print(""))
    art_func()

if __name__ == "__main__":
    # Demo all world arts
    print("=== DRAGONS & IA - WORLD ASCII ART DEMO ===\n")

    worlds = ['fantasia', 'ciencia_ficcion', 'isekai', 'fantasia_oscura']
    for world in worlds:
        print(f"World: {world.replace('_', ' ').title()}")
        print("-" * 40)
        print_world_art(world)
        print("=" * 50 + "\n")

    # Demo scenario arts
    print("=== SCENARIO ART DEMO ===\n")
    scenarios = ['start', 'battle', 'victory', 'defeat', 'exploration', 'rest']
    for scenario in scenarios:
        print(f"Scenario: {scenario.upper()}")
        print("-" * 30)
        print_scenario_art(scenario)