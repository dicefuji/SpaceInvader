"""
Game state management for Space Invaders.
"""
from enum import Enum, auto

class GameState(Enum):
    """Enum representing the possible game states."""
    MENU = auto()
    PLAYING = auto()
    GAME_OVER = auto()

class GameStateManager:
    """Manages transitions between game states."""
    
    def __init__(self, initial_state=GameState.MENU):
        """
        Initialize the game state manager.
        
        Args:
            initial_state (GameState): The initial game state
        """
        self.current_state = initial_state
        self.score = 0
        self.high_score = 0
    
    def change_state(self, new_state):
        """
        Change to a new game state.
        
        Args:
            new_state (GameState): The new game state
        """
        self.current_state = new_state
    
    def start_game(self):
        """Start a new game."""
        self.current_state = GameState.PLAYING
        self.score = 0
    
    def game_over(self):
        """End the current game."""
        self.current_state = GameState.GAME_OVER
        # Update high score if current score is higher
        if self.score > self.high_score:
            self.high_score = self.score
    
    def return_to_menu(self):
        """Return to the main menu."""
        self.current_state = GameState.MENU
    
    def add_score(self, points):
        """
        Add points to the current score.
        
        Args:
            points (int): The number of points to add
        """
        self.score += points
        
    def is_menu(self):
        """Check if the current state is MENU."""
        return self.current_state == GameState.MENU
    
    def is_playing(self):
        """Check if the current state is PLAYING."""
        return self.current_state == GameState.PLAYING
    
    def is_game_over(self):
        """Check if the current state is GAME_OVER."""
        return self.current_state == GameState.GAME_OVER 