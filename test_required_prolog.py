"""
Test script to verify the Prolog integration is working correctly.
This script tests the integration and makes sure Prolog is a hard requirement.
"""
import sys
import os
import traceback
import pygame
from ai.cli_prolog_bridge import CLIPrologBridge as PrologBridge
from engine.config import (
    SCREEN_WIDTH, SCREEN_HEIGHT, ALIEN_WIDTH, ALIEN_HEIGHT
)

def prolog_version_check():
    """Check SWI-Prolog version for debugging purposes."""
    try:
        import subprocess
        result = subprocess.run(['swipl', '--version'], 
                                capture_output=True, text=True, check=False)
        if result.returncode == 0:
            return f"SWI-Prolog found: {result.stdout.strip()}"
        else:
            return "SWI-Prolog not found in PATH"
    except Exception as e:
        return f"Error checking SWI-Prolog version: {e}"

def check_prolog_file(file_path):
    """Check if the Prolog file exists and is readable."""
    try:
        file_info = {
            "exists": os.path.exists(file_path),
            "is_file": os.path.isfile(file_path),
            "size": os.path.getsize(file_path) if os.path.exists(file_path) else 0,
            "absolute_path": os.path.abspath(file_path),
            "readable": os.access(file_path, os.R_OK) if os.path.exists(file_path) else False
        }
        
        if file_info["exists"] and file_info["is_file"] and file_info["readable"]:
            # Get the first few lines of the file to check for syntax
            with open(file_path, 'r') as f:
                first_lines = [f.readline() for _ in range(10)]
            file_info["first_lines"] = first_lines
            
        return file_info
    except Exception as e:
        return {"error": str(e)}

def test_prolog_bridge():
    """Test the Prolog bridge initialization and basic queries."""
    print("=== Prolog Environment Information ===")
    print(prolog_version_check())
    print("\n=== Checking Prolog File ===")
    prolog_file = 'ai/invader_ai.pl'
    file_info = check_prolog_file(prolog_file)
    for key, value in file_info.items():
        if key != "first_lines":
            print(f"{key}: {value}")
    
    if "first_lines" in file_info:
        print("\nFirst 10 lines of the Prolog file:")
        for i, line in enumerate(file_info["first_lines"], 1):
            print(f"{i}: {line.strip()}")
    
    print("\n=== Testing PrologBridge ===")
    try:
        # Initialize Prolog bridge
        print("Initializing PrologBridge...")
        bridge = PrologBridge(prolog_file)
        print("Successfully initialized PrologBridge")
        
        # Test a simple query to make sure it works
        print("\nTesting strategy mapping:")
        for row in range(5):
            strategy = bridge.get_strategy_for_row(row)
            print(f"Row {row} uses strategy {strategy}: {bridge.STRATEGY_NAMES[strategy]}")
        
        # Test the knowledge base update and query
        print("\nTesting knowledge base update and query...")
        
        # Create test data
        class TestPlayer:
            def __init__(self):
                self.x = 400
                self.y = 500
                self.width = 30
                self.height = 20
        
        class TestAlien:
            def __init__(self, alien_id, x, y):
                self.id = alien_id
                self.x = x
                self.y = y
                self.width = ALIEN_WIDTH
                self.height = ALIEN_HEIGHT
                self.active = True
        
        class TestBarrier:
            def __init__(self, barrier_id, x, y):
                self.id = barrier_id
                self.x = x
                self.y = y
                self.width = 40
                self.height = 30
                self.active = True
        
        # Create test objects
        test_player = TestPlayer()
        test_aliens = [
            TestAlien(1, 100, 100),
            TestAlien(2, 200, 100),
            TestAlien(3, 300, 100)
        ]
        test_barriers = [
            TestBarrier(1, 150, 400),
            TestBarrier(2, 350, 400)
        ]
        
        # Update the knowledge base
        bridge.update_state(test_player, test_aliens, test_barriers, (SCREEN_WIDTH, SCREEN_HEIGHT))
        print("Successfully updated knowledge base")
        
        # Test firing decision
        for alien in test_aliens:
            decision = bridge.should_alien_fire(alien.id)
            print(f"Alien {alien.id} firing decision: {decision}")
        
        print("\nAll tests passed successfully!")
        return True
        
    except ImportError as e:
        print(f"Error: {e}")
        print("This test confirms that Prolog is a hard requirement for the project.")
        return False
        
    except Exception as e:
        print(f"Error during test: {e}")
        print("\nDetailed traceback:")
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_prolog_bridge()
    sys.exit(0 if success else 1) 