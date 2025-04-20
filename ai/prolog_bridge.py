"""
Python-Prolog bridge for Space Invaders AI.
"""
import os
try:
    from pyswip import Prolog
    PROLOG_AVAILABLE = True
except ImportError:
    PROLOG_AVAILABLE = False
    print("Warning: pyswip not available. Falling back to default AI behavior.")

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
        self.prolog = None
        self.initialized = False
        self.current_strategy = None  # Kept for backward compatibility
        
        if PROLOG_AVAILABLE:
            try:
                # Make sure the file exists
                if not os.path.exists(prolog_file):
                    print(f"Prolog file not found: {prolog_file}")
                    return
                
                # Create and initialize Prolog instance
                self.prolog = Prolog()
                # Use full path to avoid path issues
                full_path = os.path.abspath(prolog_file)
                # Fix slashes for Windows if necessary
                prolog_path = full_path.replace('\\', '/')
                self.prolog.consult(prolog_path)
                
                self.initialized = True
                print(f"Successfully loaded Prolog knowledge base: {prolog_file}")
                
                # Initialize row-based strategies
                self.initialize_row_strategies()
            except Exception as e:
                print(f"Error initializing Prolog: {e}")
                self.initialized = False
    
    def initialize_row_strategies(self):
        """Initialize the row-based strategy system."""
        if not self.initialized:
            return
            
        try:
            # Clear any existing strategy setup
            self.prolog.retractall('strategy(_)')
            print("Initialized row-based strategy system")
        except Exception as e:
            print(f"Error initializing row strategies: {e}")
    
    def set_strategy(self, strategy):
        """
        Set the global firing strategy for all aliens.
        Kept for backward compatibility.
        
        Args:
            strategy (int or None): Strategy number (1-5) or None for row-based strategies
        """
        self.current_strategy = strategy
        
        if not self.initialized:
            return
            
        try:
            # Clear any existing strategy
            self.prolog.retractall('strategy(_)')
            
            # Set new strategy if provided
            if strategy is not None:
                self.prolog.assertz(f'strategy({strategy})')
                print(f"Set global firing strategy to: {strategy}")
            else:
                print("Using row-based strategies")
        except Exception as e:
            print(f"Error setting strategy: {e}")
    
    def update_state(self, player, aliens, barriers, screen_size):
        """
        Update the Prolog knowledge base with the current game state.
        
        Args:
            player: Player entity
            aliens: List of alien entities
            barriers: List of barrier entities
            screen_size: Tuple of (width, height)
        """
        if not self.initialized:
            return
        
        try:
            # Clear previous state
            self.prolog.retractall('player(_, _)')
            self.prolog.retractall('alien(_, _, _)')
            self.prolog.retractall('barrier(_, _, _)')
            self.prolog.retractall('screen_size(_, _)')
            
            # Add new state
            self.prolog.assertz(f'player({player.x + player.width // 2}, {player.y})')
            
            # Add aliens
            for alien in aliens:
                if alien.active:
                    self.prolog.assertz(
                        f'alien({alien.id}, {alien.x + alien.width // 2}, {alien.y})'
                    )
            
            # Add barriers (simplified to just barrier locations)
            for i, barrier in enumerate(barriers):
                if barrier.active:
                    self.prolog.assertz(
                        f'barrier({i+1}, {barrier.x + barrier.width // 2}, {barrier.y})'
                    )
            
            # Set screen size
            self.prolog.assertz(f'screen_size({screen_size[0]}, {screen_size[1]})')
        except Exception as e:
            print(f"Error updating Prolog state: {e}")
    
    def should_alien_fire(self, alien_id):
        """
        Check if an alien should fire according to Prolog rules.
        
        Args:
            alien_id: ID of the alien
            
        Returns:
            bool: True if the alien should fire, False otherwise
        """
        if not self.initialized:
            # Provide simple fallback behavior if Prolog is not available
            import random
            return random.random() < 0.005  # 0.5% chance to fire
        
        try:
            # Query Prolog for firing decision
            query = f"should_alien_fire({alien_id})"
            solutions = list(self.prolog.query(query, maxresult=1))
            
            # Return True if the query succeeds (meaning the alien should fire)
            return bool(solutions)
        except Exception as e:
            print(f"Error querying Prolog for firing decision: {e}")
            return False
    
    def get_alien_action(self, alien_id):
        """
        Get the next action for a specific alien from Prolog.
        This method is kept for backward compatibility but not used in the new design.
        
        Args:
            alien_id: ID of the alien
            
        Returns:
            str: Action to take ('left', 'right', 'down', 'fire', 'stay')
        """
        if not self.initialized:
            # Provide simple fallback behavior if Prolog is not available
            import random
            actions = ['left', 'right', 'stay']
            # Small chance to fire
            if random.random() < 0.01:
                return 'fire'
            return random.choice(actions)
        
        try:
            # Query Prolog for the next action
            query = f"next_action({alien_id}, Action)"
            solutions = list(self.prolog.query(query, maxresult=1))
            
            if solutions:
                return solutions[0]['Action']
            return 'stay'  # Default if no solution found
        except Exception as e:
            print(f"Error querying Prolog: {e}")
            return 'stay'  # Default on error
    
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
    
    # Test if bridge initialized correctly
    print(f"Bridge initialized: {bridge.initialized}")
    
    # Test row-based strategies
    for row in range(5):
        strategy = bridge.get_strategy_for_row(row)
        print(f"Row {row} uses strategy {strategy}: {bridge.STRATEGY_NAMES[strategy]}") 