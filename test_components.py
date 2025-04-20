"""
Simple test script to visualize the core components of the Space Invaders game.
"""
import sys
import pygame
from engine.config import (
    SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE, FPS, BLACK, WHITE,
    ALIEN_ROWS, ALIEN_COLS, ALIEN_HORIZONTAL_SPACING, ALIEN_VERTICAL_SPACING,
    BARRIER_COUNT, GAME_AREA_TOP, GAME_AREA_BOTTOM
)
from engine.player import Player
from engine.alien import AlienGroup
from engine.barrier import BarrierGroup

def main():
    """Main function to test core components."""
    # Initialize pygame
    pygame.init()
    
    # Create the screen
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption(SCREEN_TITLE)
    
    # Create a clock for controlling the frame rate
    clock = pygame.time.Clock()
    
    # Create the player
    player_x = SCREEN_WIDTH // 2
    player_y = GAME_AREA_BOTTOM
    player = Player(player_x, player_y)
    
    # Create alien group
    alien_start_x = 50
    alien_start_y = GAME_AREA_TOP + 50
    aliens = AlienGroup(
        ALIEN_ROWS, ALIEN_COLS, 
        alien_start_x, alien_start_y,
        ALIEN_HORIZONTAL_SPACING, ALIEN_VERTICAL_SPACING
    )
    
    # Create barrier group
    barrier_y = GAME_AREA_BOTTOM - 100
    barriers = BarrierGroup(BARRIER_COUNT, 0, SCREEN_WIDTH, barrier_y)
    
    # Game loop
    running = True
    while running:
        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    player.shoot()
        
        # Get pressed keys for continuous movement
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            player.move_left()
        if keys[pygame.K_RIGHT]:
            player.move_right()
        
        # Update game objects
        player.update()
        aliens.update()
        barriers.update()
        
        # Check collisions
        
        # Player bullets hitting aliens
        for bullet in player.get_active_bullets():
            for alien in aliens.get_active_aliens():
                if bullet.collides_with(alien):
                    bullet.deactivate()
                    alien.deactivate()
                    break
        
        # Alien bullets hitting player
        for bullet in aliens.get_active_bullets():
            if bullet.collides_with(player):
                bullet.deactivate()
                # In a real game, player would lose a life here
        
        # Bullets hitting barriers
        for bullet in player.get_active_bullets():
            if barriers.check_collision(bullet):
                bullet.deactivate()
        
        for bullet in aliens.get_active_bullets():
            if barriers.check_collision(bullet):
                bullet.deactivate()
        
        # Drawing
        screen.fill(BLACK)
        
        # Draw game objects
        player.draw(screen)
        aliens.draw(screen)
        barriers.draw(screen)
        
        # Add simple instructions text
        font = pygame.font.SysFont(None, 24)
        instructions = font.render(
            "Arrow keys to move, Space to shoot, Q to quit", 
            True, WHITE
        )
        screen.blit(instructions, (20, 20))
        
        # Update the display
        pygame.display.flip()
        
        # Control the frame rate
        clock.tick(FPS)
    
    # Quit pygame
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()