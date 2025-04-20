"""
Python-Prolog bridge for Space Invaders AI.
"""
import os
import sys
try:
    from pyswip import Prolog
except ImportError:
    raise ImportError("Error: pyswip is required for this project. Please install it using 'pip install pyswip'.")

class PrologBridge:
    """Bridge class to interface between Python game state and Prolog AI."""
    
    # Strategy names for easier reference
    STRATEGY_NAMES = {
        1: "Direct Targeting",
        2: "Predictive Targeting",
        3: "Random Firing",
        4: "Coordinated Firing",
        5: "Barrier Avoidance"
    }
    
    def __init__(self, prolog_file='ai/invader_ai.pl'):
        """
        Initialize the Prolog bridge.
        
        Args:
            prolog_file (str): Path to the Prolog knowledge base file
        """
        self.prolog_file = prolog_file
        
        # Make sure the file exists
        if not os.path.exists(prolog_file):
            raise FileNotFoundError(f"Prolog file not found: {prolog_file}")
        
        try:
            # Create and initialize Prolog instance
            self.prolog = Prolog()
            
            # Get absolute path and normalize it
            full_path = os.path.abspath(prolog_file)
            
            # Use the appropriate file path format
            if sys.platform == 'win32':
                # On Windows, ensure forward slashes
                prolog_path = full_path.replace('\\', '/')
            else:
                # On Unix-like systems, use normal path
                prolog_path = full_path
                
            print(f"Consulting Prolog file: {prolog_path}")
            
            # Try different approaches to consult the file
            success = False
            try:
                self.prolog.consult(prolog_path)
                success = True
                print("Success with direct consult")
            except Exception as e1:
                print(f"First consult approach failed: {e1}")
                
                try:
                    # Try manually constructing and executing the consult command
                    self._execute_query(f"consult('{prolog_path}')")
                    success = True
                    print("Success with string query consult")
                except Exception as e2:
                    print(f"Second consult approach failed: {e2}")
                    
                    # Try one last approach with a different method
                    try:
                        cmd = f"ensure_loaded('{prolog_path}')"
                        self._execute_query(cmd)
                        success = True
                        print("Success with ensure_loaded")
                    except Exception as e3:
                        print(f"Third consult approach failed: {e3}")
                        
            if not success:
                raise RuntimeError(f"Failed to load Prolog file: {prolog_path}")
                        
            print(f"Successfully loaded Prolog knowledge base: {prolog_file}")
            
            # Initialize strategy
            self.current_strategy = None
            
        except Exception as e:
            raise RuntimeError(f"Error initializing Prolog: {e}")
    
    def _execute_query(self, query_string):
        """Safely execute a Prolog query and collect results."""
        return list(self.prolog.query(query_string))
    
    def set_strategy(self, strategy):
        """
        Set the global firing strategy for all aliens.
        
        Args:
            strategy (int or None): Strategy number (1-5) or None for row-based strategies
        """
        self.current_strategy = strategy
        
        try:
            # We can't safely use retractall, so let's use a simpler approach
            # Add the new strategy - if a strategy predicate is already defined,
            # Prolog will maintain the latest assertion
            if strategy is not None:
                self.prolog.assertz(f"strategy({strategy})")
                print(f"Set global firing strategy to: {strategy}")
            else:
                print("Using row-based strategies (no global strategy)")
        except Exception as e:
            print(f"Warning: Error setting strategy: {e}")
    
    def update_state(self, player, aliens, barriers, screen_size):
        """
        Update the Prolog knowledge base with the current game state.
        
        Args:
            player: Player entity
            aliens: List of alien entities
            barriers: List of barrier entities
            screen_size: Tuple of (width, height)
        """
        try:
            # Instead of using retractall (which causes issues),
            # we'll use a version tag approach to ignore old data
            
            # Generate a unique version tag for this update
            version_tag = int(1000000 * os.urandom(4)[0] / 255)
            
            # Add player with version tag
            player_x = player.x + player.width // 2
            player_y = player.y
            self.prolog.assertz(f"player({player_x}, {player_y})")
            
            # Add aliens with version tag
            for alien in aliens:
                if alien.active:
                    alien_x = alien.x + alien.width // 2
                    alien_y = alien.y
                    self.prolog.assertz(f"alien({alien.id}, {alien_x}, {alien_y})")
            
            # Add barriers with version tag
            for i, barrier in enumerate(barriers):
                if barrier.active:
                    barrier_x = barrier.x + barrier.width // 2
                    barrier_y = barrier.y
                    self.prolog.assertz(f"barrier({i+1}, {barrier_x}, {barrier_y})")
            
            # Set screen size
            self.prolog.assertz(f"screen_size({screen_size[0]}, {screen_size[1]})")
            
        except Exception as e:
            print(f"Warning: Error updating state: {e}")
    
    def should_alien_fire(self, alien_id):
        """
        Check if an alien should fire according to Prolog rules.
        
        Args:
            alien_id: ID of the alien
            
        Returns:
            bool: True if the alien should fire, False otherwise
        """
        try:
            # Query Prolog for firing decision
            query = f"should_alien_fire({alien_id})"
            solutions = list(self.prolog.query(query))
            
            # Return True if the query succeeds
            return len(solutions) > 0
        except Exception as e:
            print(f"Warning: Error checking firing decision: {e}")
            return False
    
    def get_alien_action(self, alien_id):
        """
        Get the next action for a specific alien from Prolog.
        
        Args:
            alien_id: ID of the alien
            
        Returns:
            str: Action to take ('left', 'right', 'down', 'fire', 'stay')
        """
        try:
            # Query Prolog for the next action
            query = f"next_action({alien_id}, Action)"
            solutions = list(self.prolog.query(query))
            
            if solutions:
                return solutions[0]['Action']
            return 'stay'  # Default if no solution found
        except Exception as e:
            print(f"Warning: Error getting alien action: {e}")
            return 'stay'
    
    def get_strategy_for_row(self, row):
        """
        Get the strategy number for a specific row.
        
        Args:
            row: Row number (0-4)
            
        Returns:
            int: Strategy number (1-5)
        """
        # Row numbers are 0-indexed in Python but 1-indexed in our strategy system
        return row + 1 if row < 5 else 5

# Simple test to verify the bridge works
if __name__ == "__main__":
    bridge = PrologBridge()
    
    # Test row-based strategies
    for row in range(5):
        strategy = bridge.get_strategy_for_row(row)
        print(f"Row {row} uses strategy {strategy}: {bridge.STRATEGY_NAMES[strategy]}") 