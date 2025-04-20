"""
Test script for the CLI-based Prolog bridge.
"""
import os
import sys
import traceback
from ai.cli_prolog_bridge import CLIPrologBridge
from engine.config import (
    SCREEN_WIDTH, SCREEN_HEIGHT, ALIEN_WIDTH, ALIEN_HEIGHT
)

def test_cli_prolog_bridge():
    """Test the CLI-based Prolog bridge."""
    print("=== Testing CLI Prolog Bridge ===")
    
    try:
        # Check if the Prolog file exists
        prolog_file = 'ai/invader_ai_simple.pl'
        if not os.path.exists(prolog_file):
            print(f"Error: {prolog_file} not found")
            return False
        
        # Initialize the bridge
        print("Initializing CLI Prolog Bridge...")
        bridge = CLIPrologBridge(prolog_file)
        print("Successfully initialized CLI Prolog Bridge")
        
        # Test row-based strategies
        print("\nTesting strategy mapping:")
        for row in range(3):
            strategy = bridge.get_strategy_for_row(row)
            print(f"Row {row} uses strategy {strategy}: {bridge.STRATEGY_NAMES.get(strategy, 'Unknown')}")
        
        # Test state updates
        print("\nTesting state updates and queries...")
        
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
            TestAlien(1, 400, 100),  # Directly above player
            TestAlien(2, 200, 200),
            TestAlien(3, 600, 100)
        ]
        test_barriers = [
            TestBarrier(1, 350, 400),
            TestBarrier(2, 450, 400)
        ]
        
        # Update the state
        bridge.update_state(test_player, test_aliens, test_barriers, (SCREEN_WIDTH, SCREEN_HEIGHT))
        print("Successfully updated state")
        
        # Test firing decision for the alien directly above the player (should fire)
        alien_id = 1
        decision = bridge.should_alien_fire(alien_id)
        print(f"Alien {alien_id} (direct) firing decision: {decision}")
        
        # Test firing decision for an alien not above the player (should not fire)
        alien_id = 3
        decision = bridge.should_alien_fire(alien_id)
        print(f"Alien {alien_id} (offset) firing decision: {decision}")
        
        # Test setting strategy
        print("\nTesting strategy changes...")
        bridge.set_strategy(1)  # Direct targeting for all
        
        # Now both aliens should use direct targeting
        for alien_id in [1, 3]:
            decision = bridge.should_alien_fire(alien_id)
            print(f"With strategy 1, alien {alien_id} firing decision: {decision}")
        
        # Reset to row-based
        bridge.set_strategy(None)
        print("Reset to row-based strategies")
        
        print("\nAll tests completed successfully!")
        return True
        
    except Exception as e:
        print(f"Error during test: {e}")
        print("\nDetailed traceback:")
        traceback.print_exc()
        return False

if __name__ == "__main__":
    if test_cli_prolog_bridge():
        print("\nSUCCESS: CLI Prolog bridge is working!")
        sys.exit(0)
    else:
        print("\nFAILURE: CLI Prolog bridge test failed.")
        sys.exit(1) 