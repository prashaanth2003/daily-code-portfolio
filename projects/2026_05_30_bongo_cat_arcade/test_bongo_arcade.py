#!/usr/bin/env python3
"""
Unit Tests for Bongo Cat Coding Arcade
Uses pytest to verify core business logic, physics, scoring, and graph updates.
"""

import sys
import os

# Append project directory to sys.path to allow importing local modules
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from bongo_arcade import StreakGameEngine, EXCUSES

def test_game_engine_init():
    """Verify that the game engine initializes with correct defaults."""
    engine = StreakGameEngine(track_length=20)
    assert engine.track_length == 20
    assert engine.score == 0
    assert engine.streak == 0
    assert engine.is_running is True
    assert engine.player_pos == 1  # Starts on ground
    assert len(engine.track) == 20
    assert all(cell == " " for cell in engine.track)

def test_spawn_obstacle():
    """Verify obstacle spawning logic."""
    engine = StreakGameEngine(track_length=20)
    
    # Spawn multiple times to verify obstacles eventually spawn
    spawned = False
    for _ in range(50):
        engine.spawn_obstacle()
        if any(cell in ["B", "C", "S"] for cell in engine.track):
            spawned = True
            break
    assert spawned is True

def test_trigger_jump():
    """Verify jump physics and durations."""
    engine = StreakGameEngine(track_length=20)
    
    # Triggering jump from ground
    assert engine.trigger_jump() is True
    assert engine.player_pos == 0  # In air
    
    # Triggering jump while already in air should fail
    assert engine.trigger_jump() is False
    
    # Test gravity: should land after 3 updates
    engine.update_track()  # Frame 1 in air
    assert engine.player_pos == 0
    engine.update_track()  # Frame 2 in air
    assert engine.player_pos == 0
    engine.update_track()  # Frame 3 in air -> lands
    assert engine.player_pos == 1

def test_collision_on_ground():
    """Verify that hitting an obstacle while on the ground causes game over."""
    engine = StreakGameEngine(track_length=10)
    # Manually place an obstacle at index 4 (so after shifting it is at index 3 where Bongo Cat is)
    engine.track[4] = "B"
    engine.player_pos = 1  # On ground
    
    status = engine.update_track()
    assert status == "COLLISION"
    assert engine.is_running is False

def test_safe_jump_over_obstacle():
    """Verify that being in the air allows safe passage over obstacles and scores points."""
    engine = StreakGameEngine(track_length=10)
    # Manually place an obstacle at index 4 (so after shifting it is at index 3 where Bongo Cat is)
    engine.track[4] = "B"
    engine.player_pos = 0  # In air
    
    status = engine.update_track()
    assert status == "JUMPED"
    assert engine.is_running is True
    assert engine.score == 10
    assert engine.streak == 1

def test_contribution_graph_update():
    """Verify that contribution graph updates correctly as streak increases."""
    engine = StreakGameEngine()
    assert all(val == 0 for val in engine.contribution_grid)
    
    # Force streak to increase and trigger updates
    engine.streak = 2
    engine.update_contribution_graph()
    assert engine.contribution_grid[1] == 1
    
    engine.streak = 10
    engine.update_contribution_graph()
    assert engine.contribution_grid[5] == 1

def test_meme_excuses():
    """Verify the excuse generator returns valid reasons."""
    engine = StreakGameEngine()
    excuse = engine.get_excuse()
    assert excuse in EXCUSES
    assert len(excuse) > 10
