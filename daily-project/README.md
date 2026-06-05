# 🔥 Daily Coding Streak Dashboard

**Date:** June 5, 2026 (Friday)  
**Language:** JavaScript / TypeScript (Vanilla JS)  
**Category:** Web App / Frontend

---

## Overview

An interactive single-page dashboard that tracks daily coding progress with visual streak tracking. Built as part of the automated daily coding automation pipeline.

## Features

- **📊 Stats Cards** — Current streak, active days this month, completion rate, and total problems solved
- **📅 Streak Calendar** — GitHub-style contribution heatmap for the current month with hover tooltips
- **📝 Today's Challenges** — Displays the current day's LeetCode and HackerRank challenges
- **⚡ Activity Log** — Shows today's completed activities with timestamps
- **🌙 Dark Mode** — Automatic OS-level dark mode detection and switching
- **💾 Local Persistence** — Streak data saved to browser LocalStorage across sessions

## Technology Stack

| Component | Technology |
|-----------|------------|
| Structure  | HTML5 Semantic Markup |
| Styling    | CSS3 with CSS Variables & Tailwind CDN |
| Logic      | Vanilla JavaScript (ES6+) |
| Persistence| Web LocalStorage API |
| Fonts      | Inter (Google Fonts) |
| Icons      | Unicode/Emoji |

## How to Run

Simply open `index.html` in any modern web browser:

```bash
open index.html
# or
xdg-open index.html
# or serve locally
python3 -m http.server 8080
# then visit http://localhost:8080
```

## Project Structure

```
daily-project/
├── index.html          # Main HTML page
├── styles.css          # All styling (with dark mode support)
├── app.js              # Application logic and data management
└── README.md           # This file
```

## Code Architecture

### `app.js` — Application Logic

The app follows a modular IIFE pattern with clearly separated responsibilities:

| Function | Purpose |
|----------|---------|
| `loadStreakData()` | Retrieves streak data from LocalStorage or generates seed data |
| `saveStreakData()` | Persists streak data to LocalStorage |
| `generateSeedData()` | Creates realistic mock data for demonstration |
| `calculateStats()` | Computes current streak, active days, completion rate, total solved |
| `renderStats()` | Updates stat card DOM elements |
| `renderStreakCalendar()` | Builds the GitHub-style contribution grid dynamically |
| `renderChallenges()` | Shows today's LeetCode & HackerRank challenges |
| `renderActivityLog()` | Displays today's activity timeline |
| `markTodayActive()` | Records today's activity when the page loads |

### Design Choices

- **CSS Variables** for theming — enables seamless dark/light mode switching
- **IIFE pattern** — avoids polluting the global namespace
- **Progressive enhancement** — works with or without LocalStorage
- **Semantic HTML** — accessibility-friendly structure with proper heading hierarchy

## Expected Output

When opened in a browser, the dashboard displays:
1. **4 stat cards** showing current streak count, active days, completion percentage, and total problems solved
2. **A 7-column heatmap calendar** for the current month with color-coded activity levels
3. **Challenge cards** for today's LeetCode (Hard) and HackerRank (Easy) problems
4. **Activity timeline** showing today's logged coding activities

---

*Part of the daily-code-portfolio automation — Keeping the contribution graph active, one commit at a time.*