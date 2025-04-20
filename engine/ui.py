"""
UI components for the Space Invaders game.
"""
import pygame
from engine.config import WHITE, BLACK, RED, GREEN

class UI:
    """User interface component for the game."""
    
    def __init__(self, screen_width, screen_height):
        """
        Initialize the UI.
        
        Args:
            screen_width (int): Width of the game screen
            screen_height (int): Height of the game screen
        """
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.font_small = pygame.font.SysFont(None, 24)
        self.font_medium = pygame.font.SysFont(None, 36)
        self.font_large = pygame.font.SysFont(None, 72)
    
    def draw_score(self, screen, score, high_score=None):
        """
        Draw the score display.
        
        Args:
            screen: Pygame surface to draw on
            score (int): Current score
            high_score (int, optional): High score to display
        """
        # Draw current score
        score_text = self.font_small.render(f"Score: {score}", True, WHITE)
        screen.blit(score_text, (20, 10))
        
        # Draw high score if provided
        if high_score is not None:
            high_score_text = self.font_small.render(f"High Score: {high_score}", True, WHITE)
            screen.blit(high_score_text, (self.screen_width - high_score_text.get_width() - 20, 10))
    
    def draw_lives(self, screen, lives):
        """
        Draw the lives indicator.
        
        Args:
            screen: Pygame surface to draw on
            lives (int): Current number of lives
        """
        lives_text = self.font_small.render(f"Lives: {lives}", True, WHITE)
        screen.blit(lives_text, (self.screen_width // 2 - lives_text.get_width() // 2, 10))
    
    def draw_menu(self, screen):
        """
        Draw the main menu.
        
        Args:
            screen: Pygame surface to draw on
        """
        # Draw game title
        title_text = self.font_large.render("SPACE INVADERS", True, WHITE)
        screen.blit(
            title_text, 
            (self.screen_width // 2 - title_text.get_width() // 2, 
             self.screen_height // 4)
        )
        
        # Draw instructions
        start_text = self.font_medium.render("Press ENTER to Start", True, GREEN)
        screen.blit(
            start_text, 
            (self.screen_width // 2 - start_text.get_width() // 2, 
             self.screen_height // 2)
        )
        
        # Draw controls info
        controls_text = self.font_small.render("Arrow Keys: Move   Space: Shoot   Q: Quit", True, WHITE)
        screen.blit(
            controls_text, 
            (self.screen_width // 2 - controls_text.get_width() // 2, 
             self.screen_height * 3 // 4)
        )
    
    def draw_game_over(self, screen, score, high_score):
        """
        Draw the game over screen.
        
        Args:
            screen: Pygame surface to draw on
            score (int): Final score
            high_score (int): High score
        """
        # Draw game over message
        game_over_text = self.font_large.render("GAME OVER", True, RED)
        screen.blit(
            game_over_text, 
            (self.screen_width // 2 - game_over_text.get_width() // 2, 
             self.screen_height // 4)
        )
        
        # Draw final score
        score_text = self.font_medium.render(f"Final Score: {score}", True, WHITE)
        screen.blit(
            score_text, 
            (self.screen_width // 2 - score_text.get_width() // 2, 
             self.screen_height // 2 - 30)
        )
        
        # Draw high score
        high_score_text = self.font_medium.render(f"High Score: {high_score}", True, WHITE)
        screen.blit(
            high_score_text, 
            (self.screen_width // 2 - high_score_text.get_width() // 2, 
             self.screen_height // 2 + 30)
        )
        
        # Draw restart instructions
        restart_text = self.font_medium.render("Press ENTER to Restart", True, GREEN)
        screen.blit(
            restart_text, 
            (self.screen_width // 2 - restart_text.get_width() // 2, 
             self.screen_height * 3 // 4)
        )
        
    def draw_win_screen(self, screen, score):
        """
        Draw the win screen when all aliens are defeated.
        
        Args:
            screen: Pygame surface to draw on
            score (int): Final score
        """
        # Draw win message
        win_text = self.font_large.render("YOU WIN!", True, GREEN)
        screen.blit(
            win_text, 
            (self.screen_width // 2 - win_text.get_width() // 2, 
             self.screen_height // 4)
        )
        
        # Draw final score
        score_text = self.font_medium.render(f"Final Score: {score}", True, WHITE)
        screen.blit(
            score_text, 
            (self.screen_width // 2 - score_text.get_width() // 2, 
             self.screen_height // 2)
        )
        
        # Draw restart instructions
        restart_text = self.font_medium.render("Press ENTER to Play Again", True, GREEN)
        screen.blit(
            restart_text, 
            (self.screen_width // 2 - restart_text.get_width() // 2, 
             self.screen_height * 3 // 4)
        ) 