"""
Test script to verify the CLI-based Prolog bridge integration with Space Invaders.
"""
import sys
import pygame
from ai.cli_prolog_bridge import CLIPrologBridge
from engine.config import (
    SCREEN_WIDTH, SCREEN_HEIGHT, ALIEN_WIDTH, ALIEN_HEIGHT
)

def test_cli_integration():
    """Test the CLI bridge integration with the game."""
    print("=== Testing CLI Prolog Bridge Integration ===")
    
    try:
        # Initialize the bridge
        print("Initializing CLI Prolog Bridge...")
        prolog_file = 'ai/invader_ai_simple.pl'  # Use the simplified Prolog file
        bridge = CLIPrologBridge(prolog_file)
        print("Successfully initialized CLI Prolog Bridge")
        
        # Test row-based strategies
        print("\nTesting strategy mapping:")
        for row in range(3):
            strategy = bridge.get_strategy_for_row(row)
            print(f"Row {row} uses strategy {strategy}: {bridge.STRATEGY_NAMES.get(strategy, 'Unknown')}")
        
        # Create test game objects
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
        
        # Test setting global strategy
        print("\nTesting strategy changes...")
        bridge.set_strategy(1)  # Direct targeting for all
        print("Set global strategy to 1 (Direct Targeting)")
        
        # Test action decisions
        for alien_id in [1, 2, 3]:
            action = bridge.get_alien_action(alien_id)
            print(f"Alien {alien_id} action: {action}")
        
        print("\nAll tests completed successfully!")
        return True
        
    except Exception as e:
        print(f"Error during test: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    if test_cli_integration():
        print("\nSUCCESS: CLI Prolog bridge integration is working!")
        sys.exit(0)
    else:
        print("\nFAILURE: CLI Prolog bridge integration test failed.")
        print("Please check the error message above for details.")
        sys.exit(1) 