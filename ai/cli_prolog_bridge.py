"""
Command-line interface bridge for Space Invaders AI.
This alternative implementation uses subprocess to call SWI-Prolog
directly instead of using PySwip, avoiding compatibility issues.
"""
import os
import sys
import tempfile
import subprocess
import re
import time
import shutil
from pathlib import Path

class CLIPrologBridge:
    """Bridge class to interface between Python game state and Prolog AI using CLI."""
    
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
        self.current_strategy = None
        self.temp_dir = tempfile.mkdtemp(prefix="space_invaders_prolog_")
        self.state_file = os.path.join(self.temp_dir, "game_state.pl")
        self.query_file = os.path.join(self.temp_dir, "query.pl")
        self.result_file = os.path.join(self.temp_dir, "result.txt")
        
        # Check if swipl is available
        if not self._check_swipl():
            raise RuntimeError("SWI-Prolog not found in PATH. Please install SWI-Prolog and ensure 'swipl' is in your PATH.")
            
        # Make sure the file exists
        if not os.path.exists(prolog_file):
            raise FileNotFoundError(f"Prolog file not found: {prolog_file}")
        
        # Copy the Prolog file to the temp directory
        self.temp_prolog_file = os.path.join(self.temp_dir, os.path.basename(prolog_file))
        shutil.copy2(prolog_file, self.temp_prolog_file)
        
        print(f"Initialized CLI Prolog bridge using file: {prolog_file}")
        print(f"Temporary directory: {self.temp_dir}")
        
        # Initialize with empty state
        self._write_state_file([])
    
    def __del__(self):
        """Clean up temporary files when the object is destroyed."""
        try:
            shutil.rmtree(self.temp_dir)
            print(f"Removed temporary directory: {self.temp_dir}")
        except Exception as e:
            print(f"Warning: Failed to clean up temporary directory: {e}")
    
    def _check_swipl(self):
        """Check if SWI-Prolog is available."""
        try:
            result = subprocess.run(
                ['swipl', '--version'], 
                capture_output=True, 
                text=True, 
                check=False
            )
            if result.returncode == 0:
                print(f"Found SWI-Prolog: {result.stdout.strip()}")
                return True
            return False
        except Exception:
            return False
    
    def _write_state_file(self, facts):
        """Write the current state facts to a file."""
        with open(self.state_file, 'w') as f:
            for fact in facts:
                f.write(f"{fact}.\n")
    
    def _write_query_file(self, query, extra_code=None):
        """Write a query to a file."""
        with open(self.query_file, 'w') as f:
            # Load the main Prolog file
            f.write(f":- consult('{self.temp_prolog_file}').\n")
            # Load the state file
            f.write(f":- consult('{self.state_file}').\n")
            
            # Add any extra code if provided
            if extra_code:
                f.write(f"{extra_code}\n")
            
            # Write the query that writes results to the result file
            f.write(f"main :- {query}, open('{self.result_file}', write, S), write(S, 'true'), close(S).\n")
            f.write(f"main :- open('{self.result_file}', write, S), write(S, 'false'), close(S).\n")
            f.write(":- main, halt.\n")
    
    def _execute_query(self, query, extra_code=None):
        """Execute a Prolog query and return the result."""
        # Write the query file
        self._write_query_file(query, extra_code)
        
        # Execute the query
        try:
            result = subprocess.run(
                ['swipl', '-q', '-f', self.query_file], 
                capture_output=True, 
                text=True,
                check=False
            )
            
            # Check for errors
            if result.returncode != 0 and result.stderr:
                print(f"Prolog error: {result.stderr}")
                return False
            
            # Read the result
            if os.path.exists(self.result_file):
                with open(self.result_file, 'r') as f:
                    content = f.read().strip()
                return content == 'true'
            return False
            
        except Exception as e:
            print(f"Error executing query: {e}")
            return False
    
    def set_strategy(self, strategy):
        """
        Set the global firing strategy for all aliens.
        
        Args:
            strategy (int or None): Strategy number (1-5) or None for row-based strategies
        """
        self.current_strategy = strategy
        
        # Add or remove strategy fact
        current_facts = []
        if strategy is not None:
            current_facts.append(f"strategy({strategy})")
            print(f"Set global firing strategy to: {strategy}")
        else:
            print("Using row-based strategies")
        
        # Write the updated state
        self._write_state_file(current_facts)
    
    def update_state(self, player, aliens, barriers, screen_size):
        """
        Update the Prolog knowledge base with the current game state.
        
        Args:
            player: Player entity
            aliens: List of alien entities
            barriers: List of barrier entities
            screen_size: Tuple of (width, height)
        """
        # Build facts list
        facts = []
        
        # Add player
        player_x = player.x + player.width // 2
        player_y = player.y
        facts.append(f"player({player_x}, {player_y})")
        
        # Add aliens
        for alien in aliens:
            if alien.active:
                alien_x = alien.x + alien.width // 2
                alien_y = alien.y
                facts.append(f"alien({alien.id}, {alien_x}, {alien_y})")
        
        # Add barriers
        for i, barrier in enumerate(barriers):
            if barrier.active:
                barrier_x = barrier.x + barrier.width // 2
                barrier_y = barrier.y
                facts.append(f"barrier({i+1}, {barrier_x}, {barrier_y})")
        
        # Add screen size
        facts.append(f"screen_size({screen_size[0]}, {screen_size[1]})")
        
        # Add strategy if set
        if self.current_strategy is not None:
            facts.append(f"strategy({self.current_strategy})")
        
        # Write to file
        self._write_state_file(facts)
    
    def should_alien_fire(self, alien_id):
        """
        Check if an alien should fire according to Prolog rules.
        
        Args:
            alien_id: ID of the alien
            
        Returns:
            bool: True if the alien should fire, False otherwise
        """
        query = f"should_alien_fire({alien_id})"
        return self._execute_query(query)
    
    def get_alien_action(self, alien_id):
        """
        Get the next action for a specific alien from Prolog.
        
        Args:
            alien_id: ID of the alien
            
        Returns:
            str: Action to take ('left', 'right', 'down', 'fire', 'stay')
        """
        # For this query, we need to capture the result variable
        # We'll modify our approach
        action_file = os.path.join(self.temp_dir, "action.txt")
        
        extra_code = f"""
            get_action(AlienID, Action) :-
                next_action(AlienID, Action),
                open('{action_file}', write, S),
                write(S, Action),
                close(S).
        """
        
        query = f"get_action({alien_id}, _)"
        success = self._execute_query(query, extra_code)
        
        if success and os.path.exists(action_file):
            with open(action_file, 'r') as f:
                action = f.read().strip()
                
            # Convert atom to Python string
            if action in ['left', 'right', 'down', 'fire', 'stay']:
                return action
        
        return 'stay'  # Default if no solution found
    
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
    bridge = CLIPrologBridge()
    
    # Test row-based strategies
    for row in range(5):
        strategy = bridge.get_strategy_for_row(row)
        print(f"Row {row} uses strategy {strategy}: {bridge.STRATEGY_NAMES[strategy]}") 