"""
Enhanced player with smoother movement that updates multiple times per frame.
"""
import pygame
from engine.player import Player, Bullet
from engine.config import (
    PLAYER_WIDTH, PLAYER_HEIGHT, PLAYER_SPEED,
    SCREEN_WIDTH, GREEN, BULLET_WIDTH, BULLET_HEIGHT,
    PLAYER_BULLET_SPEED
)

class SmoothBullet(Bullet):
    """Enhanced bullet with smoother movement."""
    
    def __init__(self, x, y, subframes=60):
        """Initialize a bullet with smoother movement."""
        super().__init__(x, y)
        self.subframes = subframes
        # Store original speed
        self.base_speed = PLAYER_BULLET_SPEED
        # Use float for position to allow for smoother subpixel movement
        self.x = float(self.x)
        self.y = float(self.y)
        # We use the full speed rather than dividing to ensure bullets move fast enough
        self.speed = self.base_speed
    
    def update(self):
        """Update bullet position with smoother movement."""
        # Use smoother movement with a fraction of the full speed
        self.y -= self.speed / self.subframes
        # Update rectangle for collision detection
        self.rect.y = int(self.y)
        
        # Deactivate if it goes off the top of the screen
        if self.y + self.height < 0:
            self.deactivate()

class SmoothPlayer(Player):
    """Player with smoother movement that updates at a higher rate than aliens."""
    
    def __init__(self, x, y, lives=3, subframes=10):
        """
        Initialize the smooth player spaceship.
        
        Args:
            x (int): X-coordinate of the ship's center
            y (int): Y-coordinate of the ship's top
            lives (int): Number of lives
            subframes (int): Number of updates per game frame
        """
        super().__init__(x, y, lives)
        self.subframes = subframes
        # Store base speed
        self.base_speed = PLAYER_SPEED
        # Use float for precise movement
        self.x = float(self.x)
        self.y = float(self.y)
        # We use full speed to make movement more responsive
        self.speed = self.base_speed
        self.moving_left = False
        self.moving_right = False
        # Lower the cooldown time to make shooting more responsive
        self.cooldown_time = 3
    
    def start_move_left(self):
        """Begin moving left."""
        self.moving_left = True
    
    def start_move_right(self):
        """Begin moving right."""
        self.moving_right = True
    
    def stop_move_left(self):
        """Stop moving left."""
        self.moving_left = False
    
    def stop_move_right(self):
        """Stop moving right."""
        self.moving_right = False
    
    def update_smooth(self):
        """Update player position at a higher rate for smoother movement."""
        # Apply movement if keys are pressed
        if self.moving_left:
            # Apply a fraction of the movement per subframe for smoother motion
            self.x = max(0, self.x - (self.speed / self.subframes))
        if self.moving_right:
            # Apply a fraction of the movement per subframe for smoother motion
            self.x = min(SCREEN_WIDTH - self.width, self.x + (self.speed / self.subframes))
        
        # Update rectangle for collision detection
        self.rect.x = int(self.x)
        self.rect.y = int(self.y)
    
    def update(self):
        """Regular update method called once per frame."""
        # Update bullets and cooldowns
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
    
    def move_left(self):
        """Legacy method for compatibility."""
        self.start_move_left()
    
    def move_right(self):
        """Legacy method for compatibility."""
        self.start_move_right()
        
    def shoot(self):
        """Fire a bullet if cooldown allows."""
        if self.cooldown == 0:
            # Create smoother bullet at the center-top of the player
            bullet_x = self.x + self.width // 2
            bullet_y = self.y
            
            self.bullets.append(SmoothBullet(bullet_x, bullet_y, self.subframes))
            self.cooldown = self.cooldown_time 