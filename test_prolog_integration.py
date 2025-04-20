"""
Test script for the Prolog AI integration with the core components.
"""
import sys
import pygame
from engine.config import (
    SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE, FPS, BLACK, WHITE,
    ALIEN_ROWS, ALIEN_COLS, ALIEN_HORIZONTAL_SPACING, ALIEN_VERTICAL_SPACING,
    BARRIER_COUNT, GAME_AREA_TOP, GAME_AREA_BOTTOM, ALIEN_WIDTH, ALIEN_HEIGHT
)
from engine.player import Player
from engine.alien import AlienGroup, Alien, AlienBullet
from engine.barrier import BarrierGroup
from engine.sprites import load_sprite, ALIEN_SPRITES
from ai.cli_prolog_bridge import CLIPrologBridge as PrologBridge

class PrologAlien(Alien):
    """Alien that uses Prolog for firing decision making."""
    
    def __init__(self, x, y, row, col, prolog_bridge, alien_id=None):
        """
        Initialize an alien with Prolog integration.
        
        Args:
            x (int): X-coordinate of the alien
            y (int): Y-coordinate of the alien
            row (int): Row index in the alien grid
            col (int): Column index in the alien grid
            prolog_bridge: PrologBridge instance
            alien_id (int, optional): Unique identifier for the alien
        """
        super().__init__(x, y, row, col, alien_id)
        self.prolog_bridge = prolog_bridge
        self.firing_cooldown = 0
        self.firing_cooldown_time = 30  # Reduced from 30 for more frequent firing opportunities
        
        # Determine alien type based on row (we have 3 alien types)
        alien_type = min(row + 1, 3)  # Ensure we don't exceed available sprites
        
        # Load the appropriate sprite
        sprite_path = ALIEN_SPRITES[alien_type]
        self.image = load_sprite(sprite_path, (ALIEN_WIDTH, ALIEN_HEIGHT))
    
    def update(self):
        """Update alien's state - only handling cooldown here."""
        # Default update to keep rect in sync with position
        super().update()
        
        # Decrease firing cooldown
        if self.firing_cooldown > 0:
            self.firing_cooldown -= 1
            
    def should_fire(self, firing_chance=None):
        """
        Determine if the alien should fire using Prolog.
        
        Args:
            firing_chance: Not used, decision comes from Prolog
            
        Returns:
            bool: True if the alien should fire, False otherwise
        """
        # Only check if cooldown allows
        if self.firing_cooldown > 0:
            return False
        
        # Use Prolog for decision
        return self.prolog_bridge.should_alien_fire(self.id)

class PrologAlienGroup(AlienGroup):
    """Group of aliens with Prolog-controlled firing behavior."""
    
    def __init__(self, rows, cols, start_x, start_y, h_spacing, v_spacing, prolog_bridge):
        """
        Initialize a group of aliens with Prolog-controlled firing.
        
        Args:
            rows (int): Number of rows in the alien grid
            cols (int): Number of columns in the alien grid
            start_x (int): Starting X-coordinate for the top-left alien
            start_y (int): Starting Y-coordinate for the top-left alien
            h_spacing (int): Horizontal spacing between aliens
            v_spacing (int): Vertical spacing between aliens
            prolog_bridge: PrologBridge instance
        """
        # Initialize aliens array and other properties
        self.aliens = []
        self.bullets = []
        self.next_id = 1
        self.prolog_bridge = prolog_bridge
        
        # Limit rows to 3 for our three strategies
        actual_rows = min(rows, 3)
        
        # Create the alien grid
        for row in range(actual_rows):
            for col in range(cols):
                x = start_x + col * (ALIEN_WIDTH + h_spacing)
                y = start_y + row * (ALIEN_HEIGHT + v_spacing)
                
                # Create alien with unique ID and Prolog bridge
                alien = PrologAlien(x, y, row, col, prolog_bridge, self.next_id)
                self.aliens.append(alien)
                self.next_id += 1
    
    def update(self, player=None, barriers=None):
        """
        Update all aliens - standard movement with Prolog-based firing.
        
        Args:
            player: Player entity for Prolog to access
            barriers: List of barriers for Prolog to access
        """
        # Update Prolog knowledge base with current game state
        if player and barriers is not None:
            screen_size = (SCREEN_WIDTH, SCREEN_HEIGHT)
            self.prolog_bridge.update_state(player, self.aliens, barriers, screen_size)
        
        # Standard movement logic - same as in the original AlienGroup
        should_reverse = any(alien.should_reverse() for alien in self.get_active_aliens())
        should_move_down = False
        
        if should_reverse:
            should_move_down = True
            for alien in self.aliens:
                if alien.active:
                    alien.reverse_direction()
        
        # Update all active aliens
        for alien in self.aliens:
            if alien.active:
                if should_move_down:
                    alien.move_down()
                alien.move_horizontal()
                alien.update()
                
                # Use Prolog for firing decision
                if alien.should_fire():
                    self.bullets.append(alien.create_bullet())
                    alien.firing_cooldown = alien.firing_cooldown_time
        
        # Update bullets
        for bullet in self.bullets[:]:
            bullet.update()
            if not bullet.active:
                self.bullets.remove(bullet)
    
    def reached_bottom(self, bottom_y):
        """
        Check if any alien has reached or passed the specified bottom boundary.
        
        Args:
            bottom_y (int): Y-coordinate of the bottom boundary
            
        Returns:
            bool: True if any alien has reached bottom, False otherwise
        """
        return any(alien.y + alien.height >= bottom_y for alien in self.get_active_aliens())

def main():
    """Main function to test the Prolog integration."""
    # Initialize pygame
    pygame.init()
    
    # Create the screen
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption(SCREEN_TITLE)
    
    # Create a clock for controlling the frame rate
    clock = pygame.time.Clock()
    
    # Create Prolog bridge
    prolog_bridge = PrologBridge()
    
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
                elif event.key == pygame.K_q:
                    running = False
        
        # Get pressed keys for continuous movement
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            player.move_left()
        if keys[pygame.K_RIGHT]:
            player.move_right()
        
        # Update game objects
        player.update()
        aliens.update(player, barriers.barriers)
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