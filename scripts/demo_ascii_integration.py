"""
Demo script showing how ASCII art could be integrated into the Dragons & IA game flow.
This is an example of how the game_ascii_art.py module might be used.
"""

import time
import sys
import os

# Add the scripts directory to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__), '.'))

from game_ascii_art import (
    print_welcome_banner,
    print_world_art,
    print_scenario_art,
    print_dragon,
    print_wizard_staff
)

def demo_game_flow():
    """Demonstrate how ASCII art could be used in different game moments."""

    print("=== Dragons & IA ASCII Art Integration Demo ===\n")

    # 1. Game startup - show welcome banner with dragon (default)
    print_scenario_art('start')
    time.sleep(1)

    # 2. World selection - show art for selected world
    selected_world = "ciencia_ficcion"  # Example: player chose sci-fi world
    print(f"Player has selected the {selected_world.replace('_', ' ').title()} world!")
    print_world_art(selected_world)
    time.sleep(1)

    # 3. Character creation - show wizard staff (magic theme)
    print_scenario_art('exploration')
    print("Creating your character...")
    print_wizard_staff()  # Using wizard staff for character creation magic theme
    time.sleep(1)

    # 4. Battle starts
    print_scenario_art('battle')
    print("A wild dragon appears! Prepare for battle!")
    time.sleep(1)

    # 5. Victory!
    print_scenario_art('victory')
    print("You have defeated the dragon! Glory awaits!")
    time.sleep(1)

    # 6. Resting at camp
    print_scenario_art('rest')
    print("You rest by the campfire, recovering your strength...")
    time.sleep(1)

    # 7. Game over / return to main menu
    print_scenario_art('start')
    print("Return to the main menu to choose a new adventure!")

    print("\n=== Demo Complete ===")

if __name__ == "__main__":
    demo_game_flow()