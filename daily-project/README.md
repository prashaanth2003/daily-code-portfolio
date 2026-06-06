# 👾 GitHub Streak Saver - Retro Web Arcade 🚀

**An interactive HTML5 Canvas arcade game to help developers keep their green commit squares and protect their coding streak against bugs, legacy code, and server outages!**

---

## 🎮 Overview & Gameplay

As developers, we know the sacred pressure of keeping our **GitHub Contribution Streak** alive. One missed day, and the streak breaks!

In **GitHub Streak Saver**, you play as a cute **Developer AI Agent (Flying Robot)** equipped with a custom rocket jetpack. Your mission is to fly through the scrolling production server room, collect shiny **Green Commit Blocks**, stock up on **Streak Freezes** (glowing shields), and dodge dangerous, fire-red **System Bugs**!

If you collide with a bug but have a **Streak Freeze** in stock, it is automatically consumed to trigger a high-voltage protection shield, vaporize the bug, and grant you temporary invincibility. If you have no freeze and hit a bug or fall into the abyss, your streak is shattered, leading to immediate corporate disappointment!

---

## ✨ Features

- 🕹️ **Responsive Web Layout**: Embedded into an arcade-cabinet design that automatically reflows to fit narrow screens (minimum 400px width) as well as wide panels.
- 🎨 **Retro Cyberpunk Visuals**: Beautiful glowing neon elements, canvas grid rendering, and customized dark/light mode integration.
- 🎵 **Custom 8-Bit Synthesizer**: Code-synthesized retro sound effects using the native **HTML5 Web Audio API** (Jump, Score, Shield, Collision) — completely self-contained with no external audio file dependencies!
- 🛡️ **Automated Streak Freeze (Shields)**: In-game inventory stores up to 3 streak freeze powerups which automatically activate on collision to save your progress.
- 📈 **Dynamic Difficulty Scaling**: The scrolling speed of system bugs and code errors automatically increases as your score gets higher.
- 🏆 **High Score Persistence**: Automatically tracks and stores your longest streak inside the browser's `localStorage`.
- 🐦 **Social Integration**: High-score tweet sharing button to brag about your streak on Twitter/X.

---

## 🛠️ Technology Stack

- **Frontend**: Standard HTML5 (Canvas API), CSS3
- **CSS Framework**: Tailwind CSS (Runtime V4)
- **Programming Language**: Vanilla JavaScript (ES6)
- **Audio Synthesis**: Native Browser Web Audio API
- **Testing**: Node.js automated assertion suite (`app.test.js`)

---

## 📦 Directory Structure

```
daily-project/
├── index.html     # Responsive arcade user interface
├── styles.css     # Critical falling styles and helper grids
├── app.js         # Canvas game engine, audio synthesis, and event listeners
├── app.test.js    # Node-runnable automated test runner
└── README.md      # Documentation and gameplay manual
```

---

## 🚀 Setup & Installation

Since the game is completely client-side and self-contained, no local server installation is required! You can run it instantly:

### Method A: Direct Browser Run
1. Clone the repository:
   ```bash
   git clone https://github.com/prashaanth2003/daily-code-portfolio.git
   ```
2. Navigate to the daily project directory:
   ```bash
   cd daily-code-portfolio/daily-project
   ```
3. Open `index.html` directly in any web browser (Chrome, Firefox, Safari, Edge):
   ```bash
   # On macOS
   open index.html
   # On Linux
   xdg-open index.html
   ```

### Method B: Run Automated Core Tests
You can run the underlying mathematics, collision check algorithms, and difficulty scaling unit tests in Node.js:
```bash
node app.test.js
```

#### Expected Test Output:
```
=== RUNNING GAME ENGINE UNIT TESTS ===
Running rect-circle collision test...
✅ Rect-Circle collision tests passed!
Running circle-circle collision test...
✅ Circle-Circle collision tests passed!
Running difficulty scaling tests...
✅ Difficulty scaling tests passed!

🎉 All 3 game-logic test suites passed successfully!
```

---

## 🕹️ Controls Guide

- **Flap / Fly Up**: Press `SPACEBAR` or `UP ARROW` (Keyboard), or **Click / Tap** on the game screen.
- **Manual Shield Active**: Press `SHIFT` or `F` (Keyboard) to manually force-activate a Streak Freeze shield if available.
- **Mute / Unmute Audio**: Click the **Sound FX** button in the control panel to toggle 8-bit sound effects.
- **Restart Game**: Click the **Reset Game** button or press the `R` key on your keyboard.
