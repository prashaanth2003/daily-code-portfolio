#!/usr/bin/env python3
"""
Unit tests for the GitHub Streak Analyzer.
Tests the analytics pipeline: streak computation, heatmap, weekly summary, and productivity score.
"""

import unittest
from datetime import datetime, timezone, timedelta
from streak_analyzer import (
    compute_streaks,
    compute_heatmap,
    compute_weekly_summary,
    compute_productivity_score,
)


class TestComputeStreaks(unittest.TestCase):
    """Tests for streak computation logic."""

    def test_empty_dates(self):
        result = compute_streaks([])
        self.assertEqual(result["current_streak"], 0)
        self.assertEqual(result["longest_streak"], 0)
        self.assertEqual(result["total_active_days"], 0)

    def test_single_day(self):
        now = datetime.now(timezone.utc)
        result = compute_streaks([now])
        self.assertEqual(result["total_active_days"], 1)
        self.assertGreaterEqual(result["current_streak"], 1)

    def test_consecutive_days(self):
        today = datetime.now(timezone.utc)
        dates = [
            today - timedelta(days=2),
            today - timedelta(days=1),
            today,
        ]
        result = compute_streaks(dates)
        self.assertEqual(result["total_active_days"], 3)
        self.assertGreaterEqual(result["current_streak"], 1)

    def test_gap_breaks_streak(self):
        today = datetime.now(timezone.utc)
        dates = [
            today - timedelta(days=5),
            today - timedelta(days=3),
            today,
        ]
        result = compute_streaks(dates)
        self.assertEqual(result["total_active_days"], 3)
        self.assertGreaterEqual(result["longest_streak"], 1)

    def test_longest_streak_correct(self):
        today = datetime.now(timezone.utc)
        dates = [
            today - timedelta(days=10),
            today - timedelta(days=9),
            today - timedelta(days=8),
            today - timedelta(days=5),
            today - timedelta(days=4),
        ]
        result = compute_streaks(dates)
        self.assertEqual(result["total_active_days"], 5)
        self.assertGreaterEqual(result["longest_streak"], 2)


class TestComputeHeatmap(unittest.TestCase):
    """Tests for heatmap computation."""

    def test_heatmap_keys(self):
        now = datetime.now(timezone.utc)
        result = compute_heatmap([now])
        self.assertIn("by_day_of_week", result)
        self.assertIn("by_hour", result)
        self.assertEqual(len(result["by_day_of_week"]), 7)
        self.assertEqual(len(result["by_hour"]), 24)

    def test_heatmap_counts(self):
        monday_10am = datetime(2026, 6, 1, 10, 0, 0, tzinfo=timezone.utc)
        result = compute_heatmap([monday_10am])
        self.assertEqual(result["by_day_of_week"]["Monday"], 1)
        self.assertEqual(result["by_hour"][10], 1)


class TestComputeWeeklySummary(unittest.TestCase):
    """Tests for weekly summary."""

    def test_weekly_grouping(self):
        now = datetime.now(timezone.utc)
        dates = [now, now - timedelta(days=1), now - timedelta(days=7)]
        result = compute_weekly_summary(dates)
        self.assertGreater(len(result), 0)
        total = sum(entry["commits"] for entry in result)
        self.assertEqual(total, 3)


class TestProductivityScore(unittest.TestCase):
    """Tests for productivity score calculation."""

    def test_zero_days(self):
        score = compute_productivity_score(
            {"current_streak": 0, "longest_streak": 0, "total_active_days": 0}, 0
        )
        self.assertEqual(score, 0.0)

    def test_perfect_score(self):
        score = compute_productivity_score(
            {"current_streak": 30, "longest_streak": 60, "total_active_days": 365}, 365
        )
        self.assertGreater(score, 80)

    def test_low_activity(self):
        score = compute_productivity_score(
            {"current_streak": 0, "longest_streak": 1, "total_active_days": 5}, 365
        )
        self.assertLess(score, 20)


if __name__ == "__main__":
    unittest.main()
