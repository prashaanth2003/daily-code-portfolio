#!/usr/bin/env python3
import os
import sys
import json
import argparse
from datetime import datetime, timedelta

DATA_FILE = os.path.expanduser("~/.git_streak_tracker.json")

def load_data():
    if not os.path.exists(DATA_FILE):
        return {"streak": 0, "last_commit_date": "", "history": {}}
    try:
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    except Exception:
        return {"streak": 0, "last_commit_date": "", "history": {}}

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)

def update_streak(committed_today=True):
    data = load_data()
    today_str = datetime.now().strftime("%Y-%m-%d")
    yesterday_str = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")
    
    if committed_today:
        data["history"][today_str] = True
        
        last_date = data["last_commit_date"]
        if last_date == today_str:
            # Already committed today, streak stays same
            pass
        elif last_date == yesterday_str:
            # Committed yesterday as well, streak continues
            data["streak"] += 1
            data["last_commit_date"] = today_str
        else:
            # Streak broken or first commit, reset streak to 1
            data["streak"] = 1
            data["last_commit_date"] = today_str
    else:
        # Check if streak is broken because yesterday had no commit
        last_date = data["last_commit_date"]
        if last_date != today_str and last_date != yesterday_str:
            data["streak"] = 0
            
    save_data(data)
    return data

def render_contribution_graph():
    data = load_data()
    history = data.get("history", {})
    
    # Render the last 7 days contribution graph
    print("\nYour Git Contribution Weekly Graph:")
    days = []
    for i in range(6, -1, -1):
        day = datetime.now() - timedelta(days=i)
        day_str = day.strftime("%Y-%m-%d")
        days.append(day)
        
    # Print week day headers
    headers = [day.strftime("%a")[0] for day in days]
    print("  " + "  ".join(headers))
    
    # Print boxes: [■] for committed, [□] for empty
    boxes = []
    for day in days:
        day_str = day.strftime("%Y-%m-%d")
        if history.get(day_str):
            boxes.append("■")
        else:
            boxes.append("□")
    print("  " + "  ".join(boxes))
    print(f"\n🔥 Current Streak: {data['streak']} Days")
    
    if data['streak'] > 0:
        print("Keep it up! Consistency is the key to excellence. 🚀")
    else:
        print("No commits found for yesterday or today. Start a new streak today! 💪")

def main():
    parser = argparse.ArgumentParser(description="GitStreak Tracker - Stay consistent with your git contributions!")
    parser.add_argument("--commit", action="store_true", help="Record a commit for today")
    parser.add_argument("--status", action="store_true", help="Show current streak status and graph")
    
    args = parser.parse_args()
    
    if args.commit:
        data = update_streak(committed_today=True)
        print(f"🎉 Commit logged for today! Streak is now {data['streak']} days!")
        render_contribution_graph()
    elif args.status:
        update_streak(committed_today=False) # Check if streak is broken
        render_contribution_graph()
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
