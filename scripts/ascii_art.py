"""
ASCII art for Dragons & IA game.
Prints a dragon or game-related ASCII art.
"""

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

GAME_ART = """
  ____        _   _ ____  ____
 |  _ \\ _   _| |_| |  _ \\| ___|
 | |_) | | | | __| | |_) |___ \\
 |  __/| |_| | |_| |  _ < ___) |
 |_|    \\__,_|\\__|_|_| \\_\\____/

  ____                  _   _
 |  _ \\ ___ _ __ ___ __| |_(_) ___  _ __
 | |_) / _ \\ '__/ __/ _` | __| |/ _ \\| '_ \\
 |  __/  __/ | | (_| (_| | |_| | (_) | | | |
 |_|   \\___|_|  \\___\\__,_|\\__|_|\\___/|_| |_|
"""

def print_dragon():
    """Print dragon ASCII art."""
    print(DRAGON_ART)

def print_game_header():
    """Print game header ASCII art."""
    print(GAME_ART)

def print_welcome():
    """Print welcome message with ASCII art."""
    print("=" * 50)
    print("  Welcome to Dragons & IA!")
    print("=" * 50)
    print_dragon()
    print("\nGet ready for an epic adventure!\n")

if __name__ == "__main__":
    print_welcome()