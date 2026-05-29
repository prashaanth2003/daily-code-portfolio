import os
import json
import pytest
from datetime import datetime, timedelta
import git_streak

def test_streak_increment(tmp_path, monkeypatch):
    # Mock data file location using monkeypatch
    temp_file = str(tmp_path / "streak.json")
    monkeypatch.setattr(git_streak, "DATA_FILE", temp_file)
    
    # Initialize first commit
    git_streak.update_streak(committed_today=True)
    data = git_streak.load_data()
    assert data["streak"] == 1
    
    # Simulate today was yesterday, and log another commit
    today_str = datetime.now().strftime("%Y-%m-%d")
    yesterday_str = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")
    
    data["last_commit_date"] = yesterday_str
    git_streak.save_data(data)
    
    # Perform new commit today
    git_streak.update_streak(committed_today=True)
    new_data = git_streak.load_data()
    assert new_data["streak"] == 2
