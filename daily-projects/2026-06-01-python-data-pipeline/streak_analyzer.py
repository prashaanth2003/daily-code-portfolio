#!/usr/bin/env python3
"""
GitHub Streak Analyzer — A CLI tool for analyzing commit patterns and streak metrics.

This tool processes git log data to calculate:
  - Current coding streak (consecutive days with commits)
  - Longest streak ever achieved
  - Commit frequency heatmap (by day of week and hour)
  - Weekly and monthly contribution summaries
  - Productivity score based on consistency

Designed as a data engineering pipeline: raw git log → structured data → analytics → report.

Usage:
  python streak_analyzer.py --repo /path/to/repo
  python streak_analyzer.py --repo /path/to/repo --format json
  python streak_analyzer.py --repo /path/to/repo --days 90
"""

import argparse
import csv
import json
import os
import subprocess
import sys
from collections import defaultdict
from datetime import datetime, timedelta, timezone
from typing import Any, Dict, List, Optional, Tuple


# ---------------------------------------------------------------------------
# Data Ingestion Layer
# ---------------------------------------------------------------------------

def get_git_log(repo_path: str, days: int = 365) -> List[datetime]:
    """
    Runs `git log` on the specified repository and returns a list of
    timezone-aware datetime objects for each commit.
    """
    since = (datetime.now(timezone.utc) - timedelta(days=days)).strftime("%Y-%m-%d")
    cmd = [
        "git", "-C", repo_path, "log",
        f"--since={since}",
        "--format=%aI",  # ISO 8601 author date with timezone
        "--no-merges",
    ]
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True, timeout=30)
    except subprocess.CalledProcessError as e:
        print(f"Error running git log: {e.stderr}", file=sys.stderr)
        return []
    except FileNotFoundError:
        print("Error: git is not installed or not in PATH.", file=sys.stderr)
        return []

    timestamps: List[datetime] = []
    for line in result.stdout.strip().splitlines():
        line = line.strip()
        if line:
            try:
                dt = datetime.fromisoformat(line)
                timestamps.append(dt)
            except ValueError:
                continue
    return timestamps


# ---------------------------------------------------------------------------
# Analytics / Transformation Layer
# ---------------------------------------------------------------------------

def compute_streaks(dates: List[datetime]) -> Dict[str, Any]:
    """
    Computes streak metrics from a list of commit datetimes.

    Returns:
        current_streak: consecutive days up to today with at least one commit
        longest_streak: maximum consecutive days with commits
        total_active_days: number of unique days with commits
    """
    if not dates:
        return {"current_streak": 0, "longest_streak": 0, "total_active_days": 0}

    # Normalize to UTC dates (unique days)
    unique_days: List[str] = sorted({d.strftime("%Y-%m-%d") for d in dates})
    total_active_days = len(unique_days)

    # Convert to datetime objects for comparison
    day_objs: List[datetime] = sorted(
        {datetime(d.year, d.month, d.day, tzinfo=timezone.utc) for d in dates}
    )

    # Compute longest streak
    longest = 1
    current_run = 1
    for i in range(1, len(day_objs)):
        diff = (day_objs[i] - day_objs[i - 1]).days
        if diff == 1:
            current_run += 1
            longest = max(longest, current_run)
        elif diff > 1:
            current_run = 1

    # Compute current streak (counting backward from today)
    today = datetime.now(timezone.utc).replace(hour=0, minute=0, second=0, microsecond=0)
    current_streak = 0
    check_date = today
    day_set = {d.date() for d in dates}

    while check_date.date() in day_set:
        current_streak += 1
        check_date -= timedelta(days=1)

    return {
        "current_streak": current_streak,
        "longest_streak": longest,
        "total_active_days": total_active_days,
    }


def compute_heatmap(dates: List[datetime]) -> Dict[str, Any]:
    """
    Builds a commit heatmap:
      - by_day_of_week: commits per day name (Mon-Sun)
      - by_hour: commits per hour (0-23)
    """
    day_names = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    by_day: Dict[str, int] = {d: 0 for d in day_names}
    by_hour: Dict[int, int] = {h: 0 for h in range(24)}

    for dt in dates:
        by_day[day_names[dt.weekday()]] += 1
        by_hour[dt.hour] += 1

    return {"by_day_of_week": by_day, "by_hour": by_hour}


def compute_weekly_summary(dates: List[datetime]) -> List[Dict[str, Any]]:
    """
    Groups commits by ISO week and returns weekly counts.
    """
    weekly: Dict[str, int] = defaultdict(int)
    for dt in dates:
        iso_year, iso_week, _ = dt.isocalendar()
        week_key = f"{iso_year}-W{iso_week:02d}"
        weekly[week_key] += 1

    return [
        {"week": k, "commits": v}
        for k, v in sorted(weekly.items(), key=lambda x: x[0])
    ]


def compute_productivity_score(streaks: Dict[str, Any], total_days: int) -> float:
    """
    Calculates a productivity score (0-100) based on:
      - Active day ratio
      - Current streak length
      - Longest streak length
    """
    if total_days == 0:
        return 0.0

    active_ratio = streaks["total_active_days"] / total_days
    streak_bonus = min(streaks["current_streak"] / 30, 1.0) * 20  # up to 20 pts
    longest_bonus = min(streaks["longest_streak"] / 60, 1.0) * 10  # up to 10 pts

    score = (active_ratio * 70) + streak_bonus + longest_bonus
    return round(min(score, 100), 1)


# ---------------------------------------------------------------------------
# Reporting / Output Layer
# ---------------------------------------------------------------------------

def generate_report(
    repo_path: str,
    streaks: Dict[str, Any],
    heatmap: Dict[str, Any],
    weekly: List[Dict[str, Any]],
    productivity: float,
    days: int,
) -> str:
    """
    Generates a formatted text report of all analytics.
    """
    lines: List[str] = []
    lines.append("=" * 60)
    lines.append(f"  📊 GITHUB STREAK ANALYZER REPORT")
    lines.append(f"  Repository: {repo_path}")
    lines.append(f"  Period: Last {days} days")
    lines.append(f"  Generated: {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')}")
    lines.append("=" * 60)
    lines.append("")

    # Streak summary
    lines.append("🔥 STREAK METRICS")
    lines.append(f"  Current Streak:  {streaks['current_streak']} day(s)")
    lines.append(f"  Longest Streak:  {streaks['longest_streak']} day(s)")
    lines.append(f"  Active Days:     {streaks['total_active_days']}")
    lines.append(f"  Productivity:    {productivity}/100")
    lines.append("")

    # Day-of-week heatmap
    lines.append("📅 COMMITS BY DAY OF WEEK")
    for day, count in heatmap["by_day_of_week"].items():
        bar = "█" * min(count, 40)
        lines.append(f"  {day[:3]:>3}: {bar} {count}")
    lines.append("")

    # Hourly heatmap (peak hours)
    lines.append("⏰ COMMITS BY HOUR (top 5)")
    sorted_hours = sorted(heatmap["by_hour"].items(), key=lambda x: -x[1])[:5]
    for hour, count in sorted_hours:
        label = f"{hour:02d}:00"
        bar = "█" * min(count, 40)
        lines.append(f"  {label}: {bar} {count}")
    lines.append("")

    # Weekly summary (last 8 weeks)
    lines.append("📈 WEEKLY COMMIT SUMMARY (last 8 weeks)")
    for entry in weekly[-8:]:
        bar = "█" * min(entry["commits"], 40)
        lines.append(f"  {entry['week']}: {bar} {entry['commits']}")
    lines.append("")

    lines.append("=" * 60)
    return "\n".join(lines)


def export_json(
    streaks: Dict[str, Any],
    heatmap: Dict[str, Any],
    weekly: List[Dict[str, Any]],
    productivity: float,
    repo_path: str,
    days: int,
) -> str:
    """
    Exports all analytics as a JSON string.
    """
    report = {
        "repository": repo_path,
        "period_days": days,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "streaks": streaks,
        "heatmap": heatmap,
        "weekly_summary": weekly,
        "productivity_score": productivity,
    }
    return json.dumps(report, indent=2)


def export_csv(weekly: List[Dict[str, Any]], output_path: str) -> str:
    """
    Exports weekly summary to a CSV file.
    """
    with open(output_path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["week", "commits"])
        writer.writeheader()
        writer.writerows(weekly)
    return output_path


# ---------------------------------------------------------------------------
# CLI Entry Point
# ---------------------------------------------------------------------------

def parse_args(argv: Optional[List[str]] = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="GitHub Streak Analyzer — Analyze commit patterns and streak metrics.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s --repo /path/to/repo
  %(prog)s --repo /path/to/repo --format json
  %(prog)s --repo /path/to/repo --days 90 --csv weekly.csv
        """,
    )
    parser.add_argument(
        "--repo",
        required=True,
        help="Path to the git repository to analyze.",
    )
    parser.add_argument(
        "--days",
        type=int,
        default=365,
        help="Number of days of history to analyze (default: 365).",
    )
    parser.add_argument(
        "--format",
        choices=["text", "json"],
        default="text",
        help="Output format (default: text).",
    )
    parser.add_argument(
        "--csv",
        help="Optional path to export weekly summary as CSV.",
    )
    return parser.parse_args(argv)


def main(argv: Optional[List[str]] = None) -> int:
    args = parse_args(argv)

    # Validate repo path
    if not os.path.isdir(args.repo):
        print(f"Error: '{args.repo}' is not a valid directory.", file=sys.stderr)
        return 1

    git_dir = os.path.join(args.repo, ".git")
    if not os.path.isdir(git_dir):
        print(f"Error: '{args.repo}' is not a git repository.", file=sys.stderr)
        return 1

    # Pipeline: ingest -> transform -> report
    print(f"🔍 Analyzing {args.repo} over the last {args.days} days...")

    dates = get_git_log(args.repo, days=args.days)
    if not dates:
        print("No commits found in the specified period.")
        return 0

    streaks = compute_streaks(dates)
    heatmap = compute_heatmap(dates)
    weekly = compute_weekly_summary(dates)
    productivity = compute_productivity_score(streaks, args.days)

    if args.format == "json":
        output = export_json(streaks, heatmap, weekly, productivity, args.repo, args.days)
        print(output)
    else:
        output = generate_report(args.repo, streaks, heatmap, weekly, productivity, args.days)
        print(output)

    if args.csv:
        path = export_csv(weekly, args.csv)
        print(f"\n📁 Weekly summary exported to: {path}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
