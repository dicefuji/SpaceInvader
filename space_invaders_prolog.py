"""
Space Invaders game with Prolog AI.
"""
import sys
import pygame

from engine.config import (
    SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE, FPS, BLACK, WHITE,
    ALIEN_ROWS, ALIEN_COLS, ALIEN_HORIZONTAL_SPACING, ALIEN_VERTICAL_SPACING,
    BARRIER_COUNT, GAME_AREA_TOP, GAME_AREA_BOTTOM
)
from engine.player import Player
from engine.alien import Alien
from engine.barrier import BarrierGroup
from engine.game_state import GameStateManager, GameState
from engine.ui import UI
from test_prolog_integration import PrologAlienGroup
from ai.prolog_bridge import PrologBridge

# Define strategy names for display
STRATEGY_NAMES = {
    None: "Row-Based",
    1: "Direct Targeting",
    2: "Predictive",
    3: "Random",
    4: "Coordinated",
    5: "Barrier Avoiding"
}

def draw_strategy_legend(screen, font):
    """
    Draw a legend explaining the alien colors and strategies.
    
    Args:
        screen: Pygame surface to draw on
        font: Pygame font to use for text
    """
    strategies = [
        ("RED: Row 1 - Direct Targeting", (255, 0, 0)),
        ("GREEN: Row 2 - Predictive Targeting", (0, 255, 0)),
        ("BLUE: Row 3 - Random Firing", (0, 0, 255)),
        ("YELLOW: Row 4 - Coordinated Firing", (255, 255, 0)),
        ("PURPLE: Row 5 - Barrier Avoidance", (255, 0, 255))
    ]
    
    y_pos = SCREEN_HEIGHT - 140
    for desc, color in strategies:
        text = font.render(desc, True, color)
        screen.blit(text, (20, y_pos))
        y_pos += 20

def initialize_game_objects(prolog_bridge):
    """
    Initialize and return the game objects.
    
    Args:
        prolog_bridge: PrologBridge instance for alien AI
    """
    # Create the player
    player_x = SCREEN_WIDTH // 2
    player_y = GAME_AREA_BOTTOM
    player = Player(player_x, player_y)
    
    # Create alien group with Prolog integration
    alien_start_x = 50
    alien_start_y = GAME_AREA_TOP + 50
    aliens = PrologAlienGroup(
        ALIEN_ROWS, ALIEN_COLS, 
        alien_start_x, alien_start_y,
        ALIEN_HORIZONTAL_SPACING, ALIEN_VERTICAL_SPACING,
        prolog_bridge
    )
    
    # Create barrier group
    barrier_y = GAME_AREA_BOTTOM - 100
    barriers = BarrierGroup(BARRIER_COUNT, 0, SCREEN_WIDTH, barrier_y)
    
    return player, aliens, barriers

def main():
    """Main function for the Space Invaders game with Prolog AI."""
    # Initialize pygame
    pygame.init()
    
    # Create the screen
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption(SCREEN_TITLE + " - Prolog AI")
    
    # Create a clock for controlling the frame rate
    clock = pygame.time.Clock()
    
    # Create game state manager
    game_state = GameStateManager()
    
    # Create UI
    ui = UI(SCREEN_WIDTH, SCREEN_HEIGHT)
    
    # Create Prolog bridge
    prolog_bridge = PrologBridge()
    
    # Initialize game objects
    player, aliens, barriers = initialize_game_objects(prolog_bridge)
    
    # Set up Prolog-specific UI elements
    prolog_status_text = ""
    if prolog_bridge.initialized:
        prolog_status_text = f"Prolog AI: Active - Using Row-Based Strategies"
    else:
        prolog_status_text = "Prolog AI: Not available (using default behavior)"
    
    # Game loop
    running = True
    game_won = False
    
    while running:
        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    running = False
                elif event.key == pygame.K_RETURN:
                    if game_state.is_menu():
                        # Start game from menu
                        game_state.start_game()
                        player, aliens, barriers = initialize_game_objects(prolog_bridge)
                        game_won = False
                    elif game_state.is_game_over() or game_won:
                        # Restart game from game over or win screen
                        game_state.start_game()
                        player, aliens, barriers = initialize_game_objects(prolog_bridge)
                        game_won = False
                elif event.key == pygame.K_SPACE and game_state.is_playing():
                    player.shoot()
                
                # Strategy keys no longer used for global strategy
                # Now only used to toggle back to row-based mode
                elif event.key == pygame.K_0:
                    # Reset to row-based strategy mode
                    prolog_bridge.set_strategy(None)
                    prolog_status_text = f"Prolog AI: Active - Using Row-Based Strategies"
        
        # Clear the screen
        screen.fill(BLACK)
        
        # Handle different game states
        if game_state.is_menu():
            # Draw menu
            ui.draw_menu(screen)
            
            # Draw Prolog status
            font = pygame.font.SysFont(None, 24)
            status = font.render(prolog_status_text, True, WHITE)
            screen.blit(status, (20, SCREEN_HEIGHT - 30))
            
            # Draw strategy legend
            draw_strategy_legend(screen, pygame.font.SysFont(None, 24))
            
        elif game_state.is_playing():
            # Get pressed keys for continuous movement
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT]:
                player.move_left()
            if keys[pygame.K_RIGHT]:
                player.move_right()
            
            # Update game objects
            player.update()
            aliens.update(player, barriers.barriers)  # Pass player and barriers for Prolog
            barriers.update()
            
            # Check collisions
            
            # Player bullets hitting aliens
            for bullet in player.get_active_bullets():
                for alien in aliens.get_active_aliens():
                    if bullet.collides_with(alien):
                        bullet.deactivate()
                        alien.deactivate()
                        game_state.add_score(alien.points)
                        break
            
            # Alien bullets hitting player
            for bullet in aliens.get_active_bullets():
                if bullet.collides_with(player):
                    bullet.deactivate()
                    if player.take_damage():
                        # Player is out of lives
                        game_state.game_over()
            
            # Bullets hitting barriers
            for bullet in player.get_active_bullets():
                if barriers.check_collision(bullet):
                    bullet.deactivate()
            
            for bullet in aliens.get_active_bullets():
                if barriers.check_collision(bullet):
                    bullet.deactivate()
            
            # Check if player won (all aliens destroyed)
            if aliens.is_empty():
                game_won = True
            
            # Check if aliens reached the bottom (game over)
            if aliens.reached_bottom(GAME_AREA_BOTTOM):
                game_state.game_over()
            
            # Draw game objects
            player.draw(screen)
            aliens.draw(screen)
            barriers.draw(screen)
            
            # Draw UI elements
            ui.draw_score(screen, game_state.score, game_state.high_score)
            ui.draw_lives(screen, player.lives)
            
            # Draw Prolog status
            font = pygame.font.SysFont(None, 18)
            status = font.render(prolog_status_text, True, WHITE)
            screen.blit(status, (20, SCREEN_HEIGHT - 160))
            
            # Draw the strategy legend
            draw_strategy_legend(screen, pygame.font.SysFont(None, 16))
            
        elif game_state.is_game_over():
            # Draw game over screen
            ui.draw_game_over(screen, game_state.score, game_state.high_score)
        
        # Draw win screen if player won
        if game_won and game_state.is_playing():
            ui.draw_win_screen(screen, game_state.score)
        
        # Update the display
        pygame.display.flip()
        
        # Control the frame rate
        clock.tick(FPS)
    
    # Quit pygame
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main() 