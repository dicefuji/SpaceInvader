"""
Base entity class for all game objects.
"""
import pygame
from engine.config import BLACK

class Entity:
    """Base class for all game entities."""
    
    def __init__(self, x, y, width, height, color=BLACK):
        """
        Initialize a new entity.
        
        Args:
            x (int): X-coordinate of top-left corner
            y (int): Y-coordinate of top-left corner
            width (int): Width of the entity
            height (int): Height of the entity
            color (tuple): RGB color tuple
        """
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.rect = pygame.Rect(x, y, width, height)
        self.active = True  # Whether entity is active in the game
        self.image = None  # Placeholder for entity image
    
    def update(self):
        """Update entity state. To be overridden by subclasses."""
        # Update the rectangle to match current position
        self.rect.x = self.x
        self.rect.y = self.y
    
    def draw(self, screen):
        """
        Draw the entity on the screen.
        
        Args:
            screen: Pygame surface to draw on
        """
        if not self.active:
            return
            
        if self.image:
            screen.blit(self.image, self.rect)
        else:
            pygame.draw.rect(screen, self.color, self.rect)
    
    def collides_with(self, other):
        """
        Check if this entity collides with another entity.
        
        Args:
            other (Entity): The other entity to check collision with
            
        Returns:
            bool: True if entities collide, False otherwise
        """
        if not self.active or not other.active:
            return False
        return self.rect.colliderect(other.rect)
    
    def deactivate(self):
        """Deactivate the entity (remove from game)."""
        self.active = False 