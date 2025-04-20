"""
Player spaceship implementation.
"""
import pygame
from engine.entity import Entity
from engine.config import (
    PLAYER_WIDTH, PLAYER_HEIGHT, PLAYER_SPEED,
    SCREEN_WIDTH, GREEN, BULLET_WIDTH, BULLET_HEIGHT,
    PLAYER_BULLET_SPEED, RED
)

class Bullet(Entity):
    """Player bullet implementation."""
    
    def __init__(self, x, y):
        """
        Initialize a new bullet.
        
        Args:
            x (int): X-coordinate of bullet center
            y (int): Y-coordinate of bullet bottom
        """
        # Center the bullet on the x coordinate
        bullet_x = x - BULLET_WIDTH // 2
        # Position the bullet at the top of the shooter
        bullet_y = y - BULLET_HEIGHT
        
        super().__init__(bullet_x, bullet_y, BULLET_WIDTH, BULLET_HEIGHT, RED)
        self.speed = PLAYER_BULLET_SPEED
    
    def update(self):
        """Move the bullet upward."""
        self.y -= self.speed
        super().update()
        
        # Deactivate if it goes off the top of the screen
        if self.y + self.height < 0:
            self.deactivate()

class Player(Entity):
    """Player spaceship implementation."""
    
    def __init__(self, x, y, lives=3):
        """
        Initialize the player spaceship.
        
        Args:
            x (int): X-coordinate of the ship's center
            y (int): Y-coordinate of the ship's top
            lives (int): Number of lives
        """
        # Center the player on the provided x coordinate
        player_x = x - PLAYER_WIDTH // 2
        
        super().__init__(player_x, y, PLAYER_WIDTH, PLAYER_HEIGHT, GREEN)
        self.speed = PLAYER_SPEED
        self.bullets = []
        self.cooldown = 0  # Shooting cooldown
        self.cooldown_time = 15  # Frames between shots
        self.lives = lives
        self.invulnerable = False
        self.invulnerable_time = 0
        self.invulnerable_duration = 60  # Invulnerability frames after being hit
    
    def update(self):
        """Update player state and bullets."""
        super().update()
        
        # Update bullets
        for bullet in self.bullets[:]:
            bullet.update()
            if not bullet.active:
                self.bullets.remove(bullet)
        
        # Decrease cooldown
        if self.cooldown > 0:
            self.cooldown -= 1
            
        # Update invulnerability
        if self.invulnerable:
            self.invulnerable_time -= 1
            if self.invulnerable_time <= 0:
                self.invulnerable = False
    
    def draw(self, screen):
        """
        Draw the player and its bullets.
        
        Args:
            screen: Pygame surface to draw on
        """
        # If invulnerable, flash the player (visible on even frames)
        if self.invulnerable and self.invulnerable_time % 4 >= 2:
            pass  # Skip drawing to create flashing effect
        else:
            super().draw(screen)
        
        # Draw bullets
        for bullet in self.bullets:
            bullet.draw(screen)
    
    def move_left(self):
        """Move the player left."""
        self.x = max(0, self.x - self.speed)
    
    def move_right(self):
        """Move the player right."""
        self.x = min(SCREEN_WIDTH - self.width, self.x + self.speed)
    
    def shoot(self):
        """Fire a bullet if cooldown allows."""
        if self.cooldown == 0:
            # Create bullet at the center-top of the player
            bullet_x = self.x + self.width // 2
            bullet_y = self.y
            
            self.bullets.append(Bullet(bullet_x, bullet_y))
            self.cooldown = self.cooldown_time
    
    def get_active_bullets(self):
        """
        Get list of active bullets.
        
        Returns:
            list: List of active bullets
        """
        return [bullet for bullet in self.bullets if bullet.active]
    
    def take_damage(self):
        """
        Reduce player lives when hit.
        
        Returns:
            bool: True if player is out of lives, False otherwise
        """
        if self.invulnerable:
            return False
            
        self.lives -= 1
        
        if self.lives <= 0:
            self.deactivate()
            return True
        else:
            # Make player invulnerable for a short time
            self.invulnerable = True
            self.invulnerable_time = self.invulnerable_duration
            return False
    
    def reset(self, x, y):
        """
        Reset the player to initial state for a new game.
        
        Args:
            x (int): X-coordinate of the ship's center
            y (int): Y-coordinate of the ship's top
        """
        self.x = x - PLAYER_WIDTH // 2
        self.y = y
        self.bullets = []
        self.cooldown = 0
        self.active = True
        self.invulnerable = False
        self.invulnerable_time = 0 