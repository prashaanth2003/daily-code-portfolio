# Day 1 Project: GitStreak Tracker 🚀

A command-line tool built in Python to help developers measure, visualize, and sustain their daily Git commit streaks. This tool keeps you motivated and ensures that you maintain your green-dot contributions on GitHub!

## Features
- **Streak Tracker**: Calculates your consecutive active contribution days.
- **ASCII Weekly Contribution Graph**: Visualizes your activity over the past 7 days (`■` for active days, `□` for empty days).
- **Gamified Motivation**: Displays helpful encouragement and status alerts to prevent breaking your streak.
- **Persistent Storage**: Stores history locally in a lightweight JSON database.

## Installation
No external packages are required! To use the tool, clone the repository and run:

```bash
chmod +x git_streak.py
```

## Usage

### 1. Log a Commit for Today
When you make a commit, run:
```bash
python3 git_streak.py --commit
```
**Output**:
```
🎉 Commit logged for today! Streak is now 1 days!

Your Git Contribution Weekly Graph:
  S  M  T  W  T  F  S
  □  □  □  □  □  ■  □

🔥 Current Streak: 1 Days
Keep it up! Consistency is the key to excellence. 🚀
```

### 2. Check Streak Status
To check your streak anytime without modifying records:
```bash
python3 git_streak.py --status
```

## Running Tests
This project includes standard unit tests to verify streak calculation behaviors. To execute:
```bash
pytest test_git_streak.py
```
