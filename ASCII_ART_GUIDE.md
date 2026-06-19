# ASCII Art Guide for Dragons & IA

This guide explains how to use and customize the ASCII art system for the Dragons & IA game.

## Overview

The ASCII art system provides various art options for different game worlds and scenarios, enhancing the textual RPG experience with visual elements.

## File Structure

- `scripts/game_ascii_art.py` - Main ASCII art module with functions for different worlds and scenarios
- `scripts/demo_ascii_integration.py` - Demo showing how to integrate ASCII art into game flow
- `scripts/game_ascii_art.py` (original) - Still available for basic dragon art

## Available ASCII Arts

### World-Specific Arts
Each game world has its own thematic ASCII art:

1. **Fantasia** (fantasia) - Dragon art (default fantasy theme)
2. **Ciencia Ficcion** (ciencia_ficcion) - Spaceship art
3. **Isekai** (isekai) - Portal/magical gateway art
4. **Fantasía Oscura** (fantasia_oscura) - Dark castle/gothic art

### Scenario Arts
Arts for specific game moments:

- **Start** - Welcome banner with dragon
- **Battle** - Crossed swords notification
- **Victory** - Trophy/celebration art
- **Defeat** - Skull/grave art
- **Exploration** - Looking glass/compass art
- **Rest** - Campfire/moon art

## How to Use

### In Python Code

Import and use the functions from `scripts.game_ascii_art`:

```python
from scripts.game_ascii_art import (
    print_welcome_banner,
    print_world_art,
    print_scenario_art,
    print_dragon,
    print_wizard_staff,
    print_spaceship,
    print_portal,
    print_dark_castle
)

# Show welcome banner (defaults to dragon art)
print_welcome_banner()

# Show welcome banner with specific world art
print_welcome_banner(world="ciencia_ficcion")

# Show just world-specific art
print_world_art("fantasia_oscura")  # Dark castle

# Show scenario art
print_scenario_art("battle")  # ⚔️  BATTLE MODE  ⚔️

# Use specific art functions directly
print_dragon()
print_wizard_staff()
print_spaceship()
print_portal()
print_dark_castle()
```

### Integration Points

The ASCII art can be integrated at various points in the game flow:

1. **Game Startup** - Show welcome banner when launching the game
2. **World Selection** - Display art for the selected world when player chooses
3. **Character Creation** - Use magical/wizard-themed art during character creation
4. **Scene Transitions** - Show scenario art when entering different game states
5. **Combat** - Display battle art when combat begins
6. **Victory/Defeat** - Show appropriate art for game outcomes

## Customization

### Adding New World Arts

To add ASCII art for a new world:

1. Define the art as a multi-line string at the top of `game_ascii_art.py`:
   ```python
   NEW_WORLD_ART = """
       YOUR ASCII ART HERE
   """
   ```

2. Add a function to print it:
   ```python
   def print_new_world_art():
       """Print ASCII art for the new world."""
       print(NEW_WORLD_ART)
   ```

3. Add it to the `world_arts` dictionary in `print_world_art()`:
   ```python
   world_arts = {
       # ... existing worlds ...
       'new_world_key': print_new_world_art
   }
   ```

### Adding New Scenario Arts

To add ASCII art for a new scenario:

1. Define the art as a multi-line string or lambda function
2. Add it to the `scenario_arts` dictionary in `print_scenario_art()`:
   ```python
   scenario_arts = {
       # ... existing scenarios ...
       'new_scenario': lambda: print("YOUR ASCII ART HERE\n")
   }
   ```

## Example Integration in Game Flow

Here's how you might integrate this into the actual game code (example):

```python
# In your game initialization or world selection code
from scripts.game_ascii_art import print_world_art, print_scenario_art

def select_world():
    # ... world selection logic ...
    selected_world = get_player_world_choice()
    
    # Show art for selected world
    print(f"You have entered the {selected_world} realm!")
    print_world_art(selected_world)
    
    return selected_world

def start_battle():
    print_scenario_art('battle')
    # ... battle logic ...
    
def end_battle(victorious):
    if victorious:
        print_scenario_art('victory')
    else:
        print_scenario_art('defeat')
```

## Running the Demo

To see all available ASCII arts in action:

```bash
python scripts/game_ascii_art.py
```

To see a demo of how they could be integrated into game flow:

```bash
python scripts/demo_ascii_integration.py
```

## Styling Notes

- All arts are designed to work well with monospace fonts (terminal/console)
- Arts use common ASCII characters that display correctly across platforms
- Arts are sized to fit reasonably in standard terminal windows (typically <60 characters wide)
- For best results, use a terminal with UTF-8 support and a good monospace font

## Future Enhancements

- Color support using ANSI escape codes (for terminals that support it)
- Animated ASCII art for certain scenarios (using time delays)
- Integration with the game's actual world selection system
- Optional art display (configurable in settings for players who prefer minimal UI)