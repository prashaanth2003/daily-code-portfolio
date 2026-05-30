#!/usr/bin/env python3
"""
🐾 BONGO CAT CODING ARCADE 🐾
A terminal-based retro scrolling game where you play as Bongo Cat,
jumping over bugs and merge conflicts to keep your contribution streak alive!

Features:
- Live ASCII Bongo Cat animation (tapping paws to typing!).
- Scrolling terminal game loop with obstacles ([BUG], [MERGE_CONFLICT]).
- Automated Coder Simulation (Spectator mode) + Playable Interactive mode.
- ASCII contribution graph visualizer that updates with your score.
- Humorous, sarcastic developer excuses for broken streaks.
- Non-blocking keyboard input (safe for Unix systems).
"""

import os
import sys
import time
import random
import argparse

# --- ASCII Graphics & Frames ---

BONGO_CAT_FRAMES = {
    "idle": [
        "    /\\_/\\    ",
        "   ( o.o )   ",
        "   /|   |\\_  ",
        "  / |   |  \\ ",
        " (__|___|___)"
    ],
    "left_down": [
        "    /\\_/\\    ",
        "   ( o.o )   ",
        "  _/|   |\\_  ",
        " /  |   |  \\ ",
        " (__|___|___)"
    ],
    "right_down": [
        "    /\\_/\\    ",
        "   ( o.o )   ",
        "   /|   |\\_  ",
        "  / |   |  \\_",
        " (__|___|____)"
    ],
    "both_down": [
        "    /\\_/\\    ",
        "   ( o.o )   ",
        "  _/|   |\\_  ",
        " /  |   |  \\_",
        " (__|___|____)"
    ]
}

# --- Meme Excuse Generator ---

EXCUSES = [
    "A stray cat sat on my keyboard and committed a bug.",
    "My local ISP was digested by a stray AI agent.",
    "I was updating documentation and accidentally refactored the universe.",
    "ChatGPT told me that bugs are just features waiting for love.",
    "My coffee machine broke, rendering me incapable of syntax compilation.",
    "Git merge conflict arose because I committed to my dreams too fast.",
    "A rogue semicolon hid behind an imports statement.",
    "My computer went to sleep and had a nightmare about memory leaks."
]

# --- Unix Non-Blocking Keyboard Input ---

class NonBlockingKeyReader:
    """Read keys from standard input without blocking in Unix environments."""
    def __init__(self):
        self.enabled = False
        try:
            import select
            import tty
            import termios
            self.enabled = True
        except ImportError:
            self.enabled = False

    def __enter__(self):
        if self.enabled:
            import tty
            import termios
            self.old_settings = termios.tcgetattr(sys.stdin)
            tty.setcbreak(sys.stdin.fileno())
        return self

    def __exit__(self, type, value, traceback):
        if self.enabled:
            import termios
            termios.tcsetattr(sys.stdin, termios.TCSADRAIN, self.old_settings)

    def get_key(self):
        if not self.enabled:
            return None
        import select
        if select.select([sys.stdin], [], [], 0)[0]:
            return sys.stdin.read(1)
        return None

# --- Game Engine ---

class StreakGameEngine:
    """Manages game state, scoring, obstacle generation, and contribution graph."""
    def __init__(self, track_length=40):
        self.track_length = track_length
        self.score = 0
        self.streak = 0
        self.is_running = True
        self.player_pos = 1  # 0: Air, 1: Ground
        self.jump_duration = 0
        self.track = [" "] * track_length
        self.obstacle_types = ["BUG", "CONFLICT", "SEMICOLON"]
        self.contribution_grid = [0] * 21  # 3 rows of 7 days representing a contribution graph

    def spawn_obstacle(self):
        """Randomly spawns an obstacle at the end of the track."""
        if random.random() < 0.25:
            # Avoid putting obstacles too close to each other
            if "B" not in self.track[-4:] and "C" not in self.track[-4:]:
                obs = random.choice(self.obstacle_types)
                if obs == "BUG":
                    self.track[-1] = "B"
                elif obs == "CONFLICT":
                    self.track[-1] = "C"
                else:
                    self.track[-1] = "S"

    def update_track(self):
        """Moves the track left by one unit and handles player/obstacle updates."""
        # Handle jump mechanics
        if self.player_pos == 0:
            self.jump_duration += 1
            if self.jump_duration >= 3:
                self.player_pos = 1
                self.jump_duration = 0

        # Extract current tile before moving
        passed_tile = self.track[0]
        
        # Shift everything left
        self.track = self.track[1:] + [" "]
        
        # Check collision at position 3 (where Bongo Cat is positioned)
        player_tile = self.track[3]
        if player_tile in ["B", "C", "S"] and self.player_pos == 1:
            # Collision!
            self.is_running = False
            return "COLLISION"
        
        # Successful pass
        if player_tile in ["B", "C", "S"] and self.player_pos == 0:
            # Successfully jumped over obstacle!
            self.score += 10
            self.streak += 1
            self.update_contribution_graph()
            return "JUMPED"
            
        # Give periodic score just for running
        if random.random() < 0.1:
            self.score += 1
            
        return "OK"

    def trigger_jump(self):
        """Causes the player to jump."""
        if self.player_pos == 1:
            self.player_pos = 0
            self.jump_duration = 0
            return True
        return False

    def update_contribution_graph(self):
        """Adds a contribution block to our 3x7 ASCII grid as score increases."""
        index = min(self.streak // 2, len(self.contribution_grid) - 1)
        self.contribution_grid[index] = min(self.contribution_grid[index] + 1, 4)

    def render_contribution_graph(self):
        """Renders an ASCII representation of the GitHub contribution graph."""
        colors = ["░", "▒", "▓", "█", "💚"]
        output = ["\n[Contribution Graph - Keep it green!]"]
        for row in range(3):
            line_str = "  "
            for col in range(7):
                idx = row * 7 + col
                level = self.contribution_grid[idx]
                char = colors[level] if level < 4 else colors[4]
                line_str += f"{char} "
            output.append(line_str)
        return "\n".join(output)

    def get_excuse(self):
        """Returns a humorous, sarcastic excuse."""
        return random.choice(EXCUSES)

# --- CLI Render Helper ---

def render_frame(mascot, engine, cat_frame="idle"):
    """Composes and prints a full terminal UI screen."""
    # Clear screen (portable ANSI escape code)
    sys.stdout.write("\033[H\033[J")
    
    # 1. Header
    sys.stdout.write("🐾  BONGO CAT ARCADE: THE STREAK RUNNER 🐾\n")
    sys.stdout.write("========================================\n")
    sys.stdout.write(f" Score: {engine.score:04d}   |   Current Streak: {engine.streak} Days 🔥\n")
    sys.stdout.write("========================================\n\n")

    # 2. Render Cat Mascot with dynamic paws
    cat_lines = BONGO_CAT_FRAMES[cat_frame]
    for line in cat_lines:
        sys.stdout.write(f" {line}\n")
    sys.stdout.write("   ---------------------\n\n")

    # 3. Render Scrolling Track with obstacles
    # Player row vs Obstacles row
    player_row = [" "] * engine.track_length
    obstacle_row = list(engine.track)
    
    # Position player at index 3
    if engine.player_pos == 0:
        player_row[3] = "🐱"
    else:
        obstacle_row[3] = "🐱"

    # Replace character markers with emojis for beautiful console display
    obs_mapping = {"B": "🪲", "C": "💥", "S": "📝", " ": " "}
    track_str = "".join(obs_mapping.get(char, char) for char in obstacle_row)
    player_str = "".join(player_row)

    sys.stdout.write(f" JUMP: {player_str}\n")
    sys.stdout.write(f" RUN:  {track_str}\n")
    sys.stdout.write("=" * engine.track_length + "\n")
    sys.stdout.write(" Controls: Press [Space] or [Enter] to JUMP!\n")

    # 4. Render Contribution Graph
    sys.stdout.write(engine.render_contribution_graph() + "\n")
    sys.stdout.flush()

# --- Main Game Runner ---

def run_simulation(max_steps=50):
    """Headless/Simulated spectator mode that runs automatically."""
    engine = StreakGameEngine()
    print("--- STARTING AUTO-SIMULATION SPECTATOR MODE ---")
    time.sleep(1)
    
    steps = 0
    while engine.is_running and steps < max_steps:
        engine.spawn_obstacle()
        
        # Simple AI helper: Jump if obstacle is closing in (at index 4, 5, or 6)
        should_jump = False
        for i in [4, 5, 6]:
            if i < len(engine.track) and engine.track[i] in ["B", "C", "S"]:
                should_jump = True
                break
                
        cat_frame = "idle"
        if should_jump:
            if engine.trigger_jump():
                cat_frame = "both_down"
        else:
            # Alternating paws for typing simulation
            cat_frame = "left_down" if steps % 2 == 0 else "right_down"
            
        status = engine.update_track()
        if status == "COLLISION":
            break
            
        render_frame(None, engine, cat_frame)
        time.sleep(0.15)
        steps += 1
        
    print("\n💥 COLLISION DETECTED! Streak broken!")
    print(f"Bongo Cat Says: \"{engine.get_excuse()}\"")
    print(f"Final Score: {engine.score} | Streak Achieved: {engine.streak} Days")
    return engine

def run_interactive():
    """Playable interactive mode using Unix non-blocking input."""
    engine = StreakGameEngine()
    
    print("Press Enter to Start the Game...")
    input()
    
    with NonBlockingKeyReader() as reader:
        steps = 0
        while engine.is_running:
            engine.spawn_obstacle()
            
            # Read input
            key = reader.get_key()
            cat_frame = "idle"
            
            if key == " " or key == "\n":
                if engine.trigger_jump():
                    cat_frame = "both_down"
            else:
                cat_frame = "left_down" if steps % 2 == 0 else "right_down"
                
            status = engine.update_track()
            if status == "COLLISION":
                break
                
            render_frame(None, engine, cat_frame)
            time.sleep(0.15)
            steps += 1
            
    print("\n💥 COLLISION DETECTED! Streak broken!")
    print(f"Bongo Cat Says: \"{engine.get_excuse()}\"")
    print(f"Final Score: {engine.score} | Streak Achieved: {engine.streak} Days")
    return engine

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Bongo Cat Coding Arcade")
    parser.add_argument("--interactive", action="store_true", help="Play the game interactively")
    parser.add_argument("--simulate", action="store_true", help="Watch Bongo Cat code automatically")
    parser.add_argument("--steps", type=int, default=50, help="Number of steps to simulate")
    
    args = parser.parse_args()
    
    if args.interactive:
        run_interactive()
    else:
        # Default to simulate in background/headless environments
        run_simulation(args.steps)
