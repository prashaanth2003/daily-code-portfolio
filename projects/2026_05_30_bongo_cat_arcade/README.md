# 🐾 Bongo Cat Coding Arcade: The Streak Runner

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python: 3.8+](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Tests: Pytest](https://img.shields.io/badge/Tests-Pytest-green.svg)](https://docs.pytest.org/)

An interactive, terminal-based retro scrolling game where you play as **Bongo Cat**, typing and jumping over bugs, merge conflicts, and missing semicolons to keep your green contribution streak alive! 

Designed as a humorous, nostalgic, and creative weekend project to keep developer spirits high and contribution graphs bright.

---

## 🎮 Game Modes

1. **🤖 Spectator / Simulator Mode (Default)**:
   Watch Bongo Cat auto-code and play the game using a simple heuristic AI! Perfect for background entertainment or running in headless/CI environments.
2. **🕹️ Playable Interactive Mode**:
   Take full control of Bongo Cat! Use non-blocking real-time keyboard inputs to trigger jumps exactly when obstacles close in.

---

## ✨ Features & Use Cases

- **🐱 Live ASCII Mascot Animation**: Bongo Cat taps its left and right paws alternately as it "types" and runs, and raises both paws when jumping!
- **🏃 Dynamic Side-Scrolling Engine**: Obstacles (`🪲 BUG`, `💥 CONFLICT`, `📝 SEMICOLON`) scroll from right to left at rapid speeds.
- **🟩 Live Contribution Grid**: A 3x7 ASCII contribution graph that turns from gray to bright green as your score and streak increase!
- **💬 Sarcastic Dev Excuse Generator**: When a collision occurs, Bongo Cat prints a hilarious and relatable developer excuse.
- **🧪 Fully Unit-Tested**: Includes a full test suite verifying game mechanics, scoring, collision physics, and graph scaling.

---

## 🛠️ Technology Stack

- **Primary Language**: Python 3 (using standard libraries)
- **Input System**: Native Unix raw terminal binding (`tty`, `termios`, `select`) for non-blocking key capture
- **Testing Framework**: `pytest` for game-loop state validation

---

## 🚀 Installation & Setup

No external dependencies are required! The game runs completely on standard library components.

### 1. Clone the Portfolio Repo
```bash
git clone https://github.com/prashaanth2003/daily-code-portfolio.git
cd daily-code-portfolio/projects/2026_05_30_bongo_cat_arcade
```

### 2. Run the Game

**To run the auto-coder simulator (default):**
```bash
python3 bongo_arcade.py --simulate --steps 100
```

**To play interactively yourself (Unix/Linux/macOS):**
```bash
python3 bongo_arcade.py --interactive
```

### 3. Run the Unit Tests
```bash
pytest test_bongo_arcade.py
```

---

## 📺 Expected Terminal Output

```text
🐾  BONGO CAT ARCADE: THE STREAK RUNNER 🐾
========================================
 Score: 0040   |   Current Streak: 4 Days 🔥
========================================

     /\_/\    
    ( o.o )   
   _/|   |\_  
  /  |   |  \_
 (__|___|____)
   ---------------------

 JUMP:     🐱                                   
 RUN:  💥      🪲                                
========================================
 Controls: Press [Space] or [Enter] to JUMP!

[Contribution Graph - Keep it green!]
  ░ ░ ▒ ░ ░ ░ ░ 
  ░ ░ ░ ░ ░ ░ ░ 
  ░ ░ ░ ░ ░ ░ ░ 
```
