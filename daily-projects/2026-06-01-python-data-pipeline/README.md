# 📊 GitHub Streak Analyzer

**A Python CLI data engineering pipeline for analyzing git commit patterns and streak metrics.**

Built for **Monday — Python Data Engineering/AI** rotation.

---

## ✨ Features

- **🔥 Streak Metrics** — Current streak, longest streak, and total active days
- **📅 Commit Heatmap** — Commits grouped by day of week and hour of day
- **📈 Weekly Summary** — Commit counts per ISO week
- **🏆 Productivity Score** — 0-100 score based on consistency and activity
- **📤 Multiple Outputs** — Text report, JSON export, CSV export

## 🧠 Architecture (Data Pipeline)

```
Raw Git Log  →  Data Ingestion  →  Transformation  →  Analytics  →  Report
  (git log)      (get_git_log)     (compute_*)         (score)      (text/json/csv)
```

## 🚀 Installation

```bash
git clone https://github.com/prashaanth2003/daily-code-portfolio.git
cd daily-code-portfolio/daily-projects/2026-06-01-python-data-pipeline
```

## 📖 Usage

```bash
# Generate a text report for any git repo
python streak_analyzer.py --repo /path/to/your/repo

# Analyze last 90 days
python streak_analyzer.py --repo /path/to/your/repo --days 90

# Export as JSON
python streak_analyzer.py --repo /path/to/your/repo --format json

# Export weekly summary to CSV
python streak_analyzer.py --repo /path/to/your/repo --csv weekly.csv
```

### Example Output

```
============================================================
  📊 GITHUB STREAK ANALYZER REPORT
  Repository: /home/user/daily-code-portfolio
  Period: Last 365 days
============================================================

🔥 STREAK METRICS
  Current Streak:  5 day(s)
  Longest Streak:  12 day(s)
  Active Days:     45
  Productivity:    34.5/100

📅 COMMITS BY DAY OF WEEK
  Mon: ████████████████████████████████████ 38
  Tue: ████████████ 14
```

## 🧪 Running Tests

```bash
python -m pytest test_streak_analyzer.py -v
```

## 🛠 Technology Stack

| Component | Technology |
|-----------|-----------|
| Language  | Python 3.12 |
| Git       | subprocess + git log |
| Testing   | unittest / pytest |
| Output    | Text, JSON, CSV |
| Stdlib    | argparse, collections, csv, datetime, json, os, subprocess |

## 📁 Project Structure

```
2026-06-01-python-data-pipeline/
├── streak_analyzer.py       # Main CLI tool
├── test_streak_analyzer.py  # Unit tests
└── README.md                # This file
```
