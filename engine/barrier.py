"""
Barrier implementation for defensive structures.
"""
import pygame
from engine.entity import Entity
from engine.config import (
    BARRIER_WIDTH, BARRIER_HEIGHT, BARRIER_SEGMENTS_X, 
    BARRIER_SEGMENTS_Y, BARRIER_SEGMENT_SIZE, GREEN
)

class BarrierSegment(Entity):
    """Individual segment of a barrier."""
    
    def __init__(self, x, y, size, barrier_id=None, segment_id=None):
        """
        Initialize a barrier segment.
        
        Args:
            x (int): X-coordinate of the segment
            y (int): Y-coordinate of the segment
            size (int): Size of the segment (width/height)
            barrier_id (int, optional): ID of the parent barrier
            segment_id (int, optional): Unique identifier for the segment
        """
        super().__init__(x, y, size, size, GREEN)
        self.barrier_id = barrier_id
        self.segment_id = segment_id if segment_id is not None else id(self)
        self.health = 3  # Number of hits the segment can take
    
    def take_damage(self):
        """
        Reduce health when hit by bullet.
        
        Returns:
            bool: True if segment was destroyed, False otherwise
        """
        self.health -= 1
        
        # Adjust color based on damage
        if self.health == 2:
            self.color = (150, 150, 0)  # Darkened green
        elif self.health == 1:
            self.color = (100, 100, 0)  # Even darker green
        
        if self.health <= 0:
            self.deactivate()
            return True
        return False

class Barrier:
    """Defensive barrier structure made up of segments."""
    
    def __init__(self, x, y, barrier_id=None):
        """
        Initialize a barrier at the given position.
        
        Args:
            x (int): X-coordinate of the barrier's center
            y (int): Y-coordinate of the barrier's top
            barrier_id (int, optional): Unique identifier for the barrier
        """
        self.x = x - BARRIER_WIDTH // 2  # Center the barrier on x
        self.y = y
        self.width = BARRIER_WIDTH
        self.height = BARRIER_HEIGHT
        self.id = barrier_id if barrier_id is not None else id(self)
        self.segments = []
        self.active = True
        
        self._create_segments()
    
    def _create_segments(self):
        """Create the barrier segments in the classic Space Invaders shape."""
        segment_count = 0
        
        # Calculate the size of each segment
        segment_size = BARRIER_SEGMENT_SIZE
        
        # Create the main body of the barrier
        for row in range(BARRIER_SEGMENTS_Y):
            for col in range(BARRIER_SEGMENTS_X):
                # Skip the top corners to create the invader shape
                if (row == 0 and (col == 0 or col == BARRIER_SEGMENTS_X - 1)):
                    continue
                
                # Skip the bottom middle to create the notch
                middle_width = 2
                middle_start = (BARRIER_SEGMENTS_X - middle_width) // 2
                if (row >= BARRIER_SEGMENTS_Y * 2 // 3 and 
                    col >= middle_start and 
                    col < middle_start + middle_width):
                    continue
                
                segment_x = self.x + col * segment_size
                segment_y = self.y + row * segment_size
                
                segment = BarrierSegment(
                    segment_x, segment_y, segment_size, 
                    self.id, segment_count
                )
                self.segments.append(segment)
                segment_count += 1
    
    def update(self):
        """Update the barrier state."""
        # Remove destroyed segments
        self.segments = [segment for segment in self.segments if segment.active]
        
        # Deactivate barrier if all segments are gone
        if not self.segments:
            self.active = False
    
    def draw(self, screen):
        """
        Draw all active segments of the barrier.
        
        Args:
            screen: Pygame surface to draw on
        """
        if not self.active:
            return
            
        for segment in self.segments:
            segment.draw(screen)
    
    def check_collision(self, bullet):
        """
        Check if a bullet collides with any segment and handle damage.
        
        Args:
            bullet: The bullet entity to check collision with
            
        Returns:
            bool: True if collision occurred, False otherwise
        """
        if not self.active or not bullet.active:
            return False
            
        for segment in self.segments:
            if segment.collides_with(bullet):
                segment.take_damage()
                return True
                
        return False

class BarrierGroup:
    """Manages a group of barriers."""
    
    def __init__(self, count, start_x, width, y):
        """
        Initialize a group of barriers.
        
        Args:
            count (int): Number of barriers to create
            start_x (int): X-coordinate to start placing barriers
            width (int): Total width to distribute barriers across
            y (int): Y-coordinate for all barriers
        """
        self.barriers = []
        
        # Calculate spacing to distribute barriers evenly
        spacing = width // count
        
        for i in range(count):
            # Position barriers evenly across the width
            x = start_x + i * spacing + spacing // 2
            barrier = Barrier(x, y, i + 1)
            self.barriers.append(barrier)
    
    def update(self):
        """Update all barriers."""
        for barrier in self.barriers:
            if barrier.active:
                barrier.update()
    
    def draw(self, screen):
        """
        Draw all active barriers.
        
        Args:
            screen: Pygame surface to draw on
        """
        for barrier in self.barriers:
            if barrier.active:
                barrier.draw(screen)
    
    def check_collision(self, bullet):
        """
        Check if a bullet collides with any barrier and handle damage.
        
        Args:
            bullet: The bullet entity to check collision with
            
        Returns:
            bool: True if collision occurred, False otherwise
        """
        for barrier in self.barriers:
            if barrier.active and barrier.check_collision(bullet):
                return True
        return False 