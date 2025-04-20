"""
Sprite management for Space Invaders.
"""
import os
import pygame

# Global sprite dictionary to avoid reloading
SPRITES = {}

def load_sprite(path, scale=None):
    """
    Load a sprite from a file path and optionally scale it.
    
    Args:
        path (str): Path to the image file
        scale (tuple, optional): (width, height) to scale the image
    
    Returns:
        pygame.Surface: The loaded and processed image surface
    """
    # Check if sprite is already loaded
    if path in SPRITES:
        sprite = SPRITES[path]
    else:
        # Ensure path exists
        if not os.path.exists(path):
            raise ValueError(f"Sprite path not found: {path}")
        
        # Load the image
        sprite = pygame.image.load(path).convert_alpha()
        SPRITES[path] = sprite
    
    # Scale if requested
    if scale and (scale[0] != sprite.get_width() or scale[1] != sprite.get_height()):
        return pygame.transform.scale(sprite, scale)
    
    return sprite

# Predefined sprite paths
ALIEN_SPRITES = {
    1: "assets/Graphics/alien_1.png",  # Row 0 - Top row
    2: "assets/Graphics/alien_2.png",  # Row 1 - Middle row
    3: "assets/Graphics/alien_3.png",  # Row 2 - Bottom row
}

SPACESHIP_SPRITE = "assets/Graphics/spaceship.png"
MYSTERY_SPRITE = "assets/Graphics/mystery.png" 