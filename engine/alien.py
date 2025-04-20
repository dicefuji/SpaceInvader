"""
Alien invader implementation.
"""
import random
import pygame
from engine.entity import Entity
from engine.config import (
    ALIEN_WIDTH, ALIEN_HEIGHT, ALIEN_HORIZONTAL_SPEED, 
    ALIEN_VERTICAL_SPEED, SCREEN_WIDTH, BLUE, BULLET_WIDTH, 
    BULLET_HEIGHT, ALIEN_BULLET_SPEED, RED
)

class AlienBullet(Entity):
    """Alien bullet implementation."""
    
    def __init__(self, x, y):
        """
        Initialize a new alien bullet.
        
        Args:
            x (int): X-coordinate of bullet center
            y (int): Y-coordinate of bullet top
        """
        # Center the bullet on the x coordinate
        bullet_x = x - BULLET_WIDTH // 2
        
        super().__init__(bullet_x, y, BULLET_WIDTH, BULLET_HEIGHT, RED)
        self.speed = ALIEN_BULLET_SPEED
    
    def update(self):
        """Move the bullet downward."""
        self.y += self.speed
        super().update()
        
        # Deactivate if it goes off the bottom of the screen
        if self.y > pygame.display.get_surface().get_height():
            self.deactivate()

class Alien(Entity):
    """Alien invader implementation."""
    
    # Point values based on row (top rows worth more)
    POINTS = [30, 20, 20, 10, 10]
    
    def __init__(self, x, y, row, col, alien_id=None):
        """
        Initialize a new alien.
        
        Args:
            x (int): X-coordinate of the alien
            y (int): Y-coordinate of the alien
            row (int): Row index in the alien grid
            col (int): Column index in the alien grid
            alien_id (int, optional): Unique identifier for the alien
        """
        super().__init__(x, y, ALIEN_WIDTH, ALIEN_HEIGHT, BLUE)
        self.row = row
        self.col = col
        self.direction = 1  # 1 for right, -1 for left
        self.speed = ALIEN_HORIZONTAL_SPEED
        self.id = alien_id if alien_id is not None else id(self)  # Use object id if none provided
        
        # Assign point value based on row
        if row < len(Alien.POINTS):
            self.points = Alien.POINTS[row]
        else:
            self.points = 10  # Default value
        
    def move_horizontal(self):
        """Move the alien horizontally based on current direction."""
        self.x += self.direction * self.speed
    
    def move_down(self):
        """Move the alien downward."""
        self.y += ALIEN_VERTICAL_SPEED
    
    def reverse_direction(self):
        """Reverse the alien's horizontal direction."""
        self.direction *= -1
    
    def should_reverse(self):
        """
        Check if the alien should reverse direction (hit screen edge).
        
        Returns:
            bool: True if direction should be reversed, False otherwise
        """
        return (self.x <= 0 and self.direction < 0) or \
               (self.x + self.width >= SCREEN_WIDTH and self.direction > 0)
    
    def should_fire(self, firing_chance=0.005):
        """
        Determine if the alien should fire a bullet.
        
        Args:
            firing_chance (float): Probability of firing (0.0-1.0)
            
        Returns:
            bool: True if the alien should fire, False otherwise
        """
        return random.random() < firing_chance
    
    def create_bullet(self):
        """
        Create a bullet from this alien.
        
        Returns:
            AlienBullet: The created bullet
        """
        bullet_x = self.x + self.width // 2
        bullet_y = self.y + self.height
        return AlienBullet(bullet_x, bullet_y)

class AlienGroup:
    """Manages a group of aliens."""
    
    def __init__(self, rows, cols, start_x, start_y, h_spacing, v_spacing):
        """
        Initialize a group of aliens.
        
        Args:
            rows (int): Number of rows in the alien grid
            cols (int): Number of columns in the alien grid
            start_x (int): Starting X-coordinate for the top-left alien
            start_y (int): Starting Y-coordinate for the top-left alien
            h_spacing (int): Horizontal spacing between aliens
            v_spacing (int): Vertical spacing between aliens
        """
        self.aliens = []
        self.bullets = []
        self.next_id = 1  # For generating unique IDs
        
        # Create the alien grid
        for row in range(rows):
            for col in range(cols):
                x = start_x + col * (ALIEN_WIDTH + h_spacing)
                y = start_y + row * (ALIEN_HEIGHT + v_spacing)
                
                # Create alien with unique ID
                alien = Alien(x, y, row, col, self.next_id)
                self.aliens.append(alien)
                self.next_id += 1
    
    def update(self):
        """Update all aliens and bullets."""
        # Check if any alien needs to reverse
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
                
                # Random chance to fire
                if alien.should_fire():
                    self.bullets.append(alien.create_bullet())
        
        # Update bullets
        for bullet in self.bullets[:]:
            bullet.update()
            if not bullet.active:
                self.bullets.remove(bullet)
    
    def draw(self, screen):
        """
        Draw all active aliens and bullets.
        
        Args:
            screen: Pygame surface to draw on
        """
        # Draw aliens
        for alien in self.aliens:
            if alien.active:
                alien.draw(screen)
        
        # Draw bullets
        for bullet in self.bullets:
            bullet.draw(screen)
    
    def get_active_aliens(self):
        """
        Get list of active aliens.
        
        Returns:
            list: List of active aliens
        """
        return [alien for alien in self.aliens if alien.active]
    
    def get_active_bullets(self):
        """
        Get list of active bullets.
        
        Returns:
            list: List of active bullets
        """
        return [bullet for bullet in self.bullets if bullet.active]
    
    def is_empty(self):
        """
        Check if all aliens are inactive.
        
        Returns:
            bool: True if no active aliens remain, False otherwise
        """
        return not self.get_active_aliens()
        
    def reached_bottom(self, bottom_y):
        """
        Check if any alien has reached or passed the specified bottom boundary.
        
        Args:
            bottom_y (int): Y-coordinate of the bottom boundary
            
        Returns:
            bool: True if any alien has reached bottom, False otherwise
        """
        return any(alien.y + alien.height >= bottom_y for alien in self.get_active_aliens()) 