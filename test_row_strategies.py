"""
Test script for analyzing the row-based strategies in the Space Invaders game.
This script visualizes the firing patterns of each row and collects statistics on their behavior.
"""
import sys
import math
import pygame
import time
import random
from collections import defaultdict

from engine.config import (
    SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE, FPS, BLACK, WHITE,
    ALIEN_ROWS, ALIEN_COLS, ALIEN_HORIZONTAL_SPACING, ALIEN_VERTICAL_SPACING,
    BARRIER_COUNT, GAME_AREA_TOP, GAME_AREA_BOTTOM
)
from engine.player import Player
from engine.barrier import BarrierGroup
from ai.cli_prolog_bridge import CLIPrologBridge as PrologBridge
from test_prolog_integration import PrologAlienGroup, PrologAlien, ALIEN_WIDTH, ALIEN_HEIGHT

# Initialize pygame
pygame.init()

# Screen settings
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Space Invaders - Row Strategy Test")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
PURPLE = (255, 0, 255)

# Strategy colors match PrologAlienGroup.ALIEN_COLORS
STRATEGY_COLORS = {
    1: (255, 0, 0),    # Red - Direct targeting
    2: (0, 255, 0),    # Green - Predictive targeting
    3: (255, 255, 0),  # Yellow - Coordinated firing
}

# Strategy names for display
STRATEGY_NAMES = {
    1: "Direct Targeting",
    2: "Predictive Targeting", 
    3: "Coordinated Firing",
}

class FiringHeatmap:
    """Class to track and visualize firing patterns over time."""
    
    def __init__(self, width, height):
        """
        Initialize heatmap data structure.
        
        Args:
            width (int): Width of screen/game area
            height (int): Height of screen/game area
        """
        self.width = width
        self.height = height
        self.shots = []  # List of (x, y, strategy) tuples
        self.max_shots = 1000  # Maximum number of shots to remember
    
    def record_shot(self, x, y, strategy):
        """
        Record a shot fired by an alien.
        
        Args:
            x (int): X coordinate of the shot
            y (int): Y coordinate of the shot
            strategy (int): The strategy used (1-3)
        """
        self.shots.append((x, y, strategy))
        # Remove oldest shots if we exceed max
        if len(self.shots) > self.max_shots:
            self.shots.pop(0)
    
    def draw_heatmap(self, surface):
        """
        Draw the heatmap on the given surface.
        
        Args:
            surface: Pygame surface to draw on
        """
        # Create a separate surface for the heatmap with alpha transparency
        heatmap = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        
        # Draw each shot as a small dot with transparency
        for x, y, strategy in self.shots:
            color = STRATEGY_COLORS.get(strategy, WHITE)
            # Add transparency to the color (alpha=40)
            color_with_alpha = (*color, 40)
            pygame.draw.circle(heatmap, color_with_alpha, (x, y), 2)
        
        # Draw the heatmap surface onto the main surface
        surface.blit(heatmap, (0, 0))
    
    def draw_strategy_patterns(self, surface):
        """
        Draw separate visualization for each strategy's pattern.
        
        Args:
            surface: Pygame surface to draw on
        """
        # Calculate positions for the strategy panels
        panel_height = 120
        panel_width = self.width // 3
        
        # Get shots for each strategy
        shots_by_strategy = {strategy: [] for strategy in STRATEGY_COLORS.keys()}
        for x, y, strategy in self.shots:
            if strategy in shots_by_strategy:
                shots_by_strategy[strategy].append((x, y))
        
        # Draw each strategy panel
        for idx, strategy in enumerate(STRATEGY_COLORS.keys()):
            panel_x = idx * panel_width
            panel_y = self.height - panel_height
            
            # Draw panel background
            panel_surface = pygame.Surface((panel_width, panel_height), pygame.SRCALPHA)
            panel_surface.fill((0, 0, 0, 180))  # Semi-transparent black
            
            # Draw title
            font = pygame.font.SysFont('Arial', 14)
            title = font.render(STRATEGY_NAMES.get(strategy, f"Strategy {strategy}"), True, STRATEGY_COLORS.get(strategy, WHITE))
            panel_surface.blit(title, (10, 10))
            
            # Draw pattern representation
            for x, y in shots_by_strategy[strategy][-50:]:  # Show last 50 shots
                # Scale the positions to fit in the panel
                scaled_x = (x / self.width) * (panel_width - 20) + 10
                scaled_y = ((y / self.height) * (panel_height - 40)) + 30
                
                color = STRATEGY_COLORS.get(strategy, WHITE)
                pygame.draw.circle(panel_surface, color, (int(scaled_x), int(scaled_y)), 2)
            
            # Add strategy number
            strat_text = font.render(f"Row {strategy - 1}", True, STRATEGY_COLORS.get(strategy, WHITE))
            panel_surface.blit(strat_text, (panel_width - 70, panel_height - 20))
            
            # Blit the panel to main surface
            surface.blit(panel_surface, (panel_x, panel_y))
    
    def clear(self):
        """Clear all recorded shots."""
        self.shots = []


class StrategyAnalyzer:
    """Class to collect and analyze statistics about each strategy's performance."""
    
    def __init__(self):
        """Initialize statistics for each strategy."""
        self.shots_fired = {strategy: 0 for strategy in STRATEGY_COLORS.keys()}
        self.shots_hit = {strategy: 0 for strategy in STRATEGY_COLORS.keys()}
        self.last_fire_time = {strategy: 0 for strategy in STRATEGY_COLORS.keys()}
        self.total_time = 0
    
    def record_shot(self, strategy):
        """Record a shot fired by an alien with the given strategy."""
        self.shots_fired[strategy] = self.shots_fired.get(strategy, 0) + 1
        self.last_fire_time[strategy] = self.total_time
    
    def record_hit(self, strategy):
        """Record a hit by an alien with the given strategy."""
        self.shots_hit[strategy] = self.shots_hit.get(strategy, 0) + 1
    
    def update(self, time_delta):
        """Update total time."""
        self.total_time += time_delta
    
    def draw_stats(self, surface):
        """Draw statistics on the given surface."""
        font = pygame.font.SysFont('Arial', 14)
        y_pos = 10
        
        for strategy in sorted(STRATEGY_COLORS.keys()):
            color = STRATEGY_COLORS.get(strategy, WHITE)
            strategy_name = STRATEGY_NAMES.get(strategy, f"Strategy {strategy}")
            
            # Calculate accuracy
            shots = self.shots_fired.get(strategy, 0)
            hits = self.shots_hit.get(strategy, 0)
            accuracy = (hits / shots * 100) if shots > 0 else 0
            
            # Calculate fire rate (shots per minute)
            fire_rate = (shots / (self.total_time / 60)) if self.total_time > 0 else 0
            
            # Render statistics
            text = font.render(
                f"{strategy_name}: Shots={shots}, Acc={accuracy:.1f}%, Rate={fire_rate:.1f}/min", 
                True, color
            )
            surface.blit(text, (10, y_pos))
            y_pos += 20


class Player:
    """Simplified player for the test environment."""
    
    def __init__(self, x, y, width=30, height=20):
        """Initialize player with position and dimensions."""
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.speed = 5
        self.rect = pygame.Rect(x, y, width, height)
    
    def update(self):
        """Update player position based on keyboard input."""
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.x = max(0, self.x - self.speed)
        if keys[pygame.K_RIGHT]:
            self.x = min(SCREEN_WIDTH - self.width, self.x + self.speed)
        
        # Update rectangle for collision detection
        self.rect.x = self.x
        self.rect.y = self.y
    
    def draw(self, surface):
        """Draw player on the given surface."""
        pygame.draw.rect(surface, GREEN, self.rect)


class Bullet:
    """Bullet fired by aliens."""
    
    def __init__(self, x, y, speed=5, strategy=None):
        """Initialize bullet with position, speed, and firing strategy."""
        self.x = x
        self.y = y
        self.width = 5
        self.height = 10
        self.speed = speed
        self.strategy = strategy
        self.rect = pygame.Rect(x, y, self.width, self.height)
    
    def update(self):
        """Update bullet position."""
        self.y += self.speed
        self.rect.y = self.y
    
    def draw(self, surface):
        """Draw bullet on the given surface."""
        color = STRATEGY_COLORS.get(self.strategy, WHITE) if self.strategy else WHITE
        pygame.draw.rect(surface, color, self.rect)


def test_single_row(row_number, prolog_bridge):
    """
    Initialize the game with only the specified row active.
    
    Args:
        row_number: Which row to test (0-4)
        prolog_bridge: PrologBridge instance
        
    Returns:
        PrologAlienGroup with only the specified row
    """
    aliens = PrologAlienGroup(
        1, ALIEN_COLS,  # Only one row
        50, GAME_AREA_TOP + 50 + row_number * (ALIEN_VERTICAL_SPACING + 30),  # Position at the specified row
        ALIEN_HORIZONTAL_SPACING, ALIEN_VERTICAL_SPACING,
        prolog_bridge
    )
    
    # Update row property for all aliens to match the strategy row
    for alien in aliens.aliens:
        alien.row = row_number
        # Update color based on row (strategy)
        strategy = row_number + 1
        if strategy <= 3:
            alien.color = STRATEGY_COLORS.get(strategy, (255, 255, 255))
    
    return aliens


def draw_debug_info(screen, font, aliens, firing_aliens, current_row):
    """
    Draw debug information for alien behavior testing.
    
    Args:
        screen: Pygame surface to draw on
        font: Font to use for text
        aliens: AlienGroup containing aliens to debug
        firing_aliens: List of alien IDs that want to fire
        current_row: Currently active row for testing
    """
    # Draw row label
    strategy_names = [
        "Direct Targeting", 
        "Predictive Targeting", 
        "Coordinated Firing",
    ]
    
    row_label = font.render(
        f"Testing Row {current_row+1}: {strategy_names[current_row]}", 
        True, 
        STRATEGY_COLORS.get(current_row+1, WHITE)
    )
    screen.blit(row_label, (20, 20))
    
    # Draw instructions
    instructions = [
        "LEFT/RIGHT: Move player",
        "UP/DOWN: Switch test row",
        "SPACE: Player shoot",
        "C: Clear heatmap data",
        "H: Toggle heatmap view",
        "Q: Quit"
    ]
    
    for i, instruction in enumerate(instructions):
        text = font.render(instruction, True, WHITE)
        screen.blit(text, (20, 60 + i*25))
    
    # Draw alien debug info
    for alien in aliens.get_active_aliens():
        # Draw alien ID
        id_text = font.render(f"ID:{alien.id}", True, WHITE)
        screen.blit(id_text, (alien.x, alien.y - 25))
        
        # Highlight aliens that want to fire
        if alien.id in firing_aliens:
            pygame.draw.circle(
                screen, 
                (255, 255, 255), 
                (alien.x + alien.width//2, alien.y + alien.height//2), 
                20, 
                2
            )


def main():
    """Main function to run the test environment."""
    # Initialize game clock
    clock = pygame.time.Clock()
    
    # Initialize player
    player = Player(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 50)
    
    # Initialize Prolog bridge
    prolog_bridge = PrologBridge()
    
    # Initialize alien group with 3 rows (for our 3 strategies) and 8 columns
    alien_group = PrologAlienGroup(3, 8, 50, 50, 20, 20, prolog_bridge)
    
    # Initialize heatmap
    heatmap = FiringHeatmap(SCREEN_WIDTH, SCREEN_HEIGHT)
    
    # Initialize strategy analyzer
    analyzer = StrategyAnalyzer()
    
    # List to store bullets
    bullets = []
    
    # Track current display mode
    show_heatmap = True
    show_strategy_panels = True
    show_stats = True
    
    # Game loop
    running = True
    while running:
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key == pygame.K_h:
                    # Toggle heatmap
                    show_heatmap = not show_heatmap
                elif event.key == pygame.K_s:
                    # Toggle strategy panels
                    show_strategy_panels = not show_strategy_panels
                elif event.key == pygame.K_t:
                    # Toggle statistics
                    show_stats = not show_stats
                elif event.key == pygame.K_c:
                    # Clear heatmap
                    heatmap.clear()
        
        # Update player
        player.update()
        
        # Update aliens in group
        for alien in alien_group.aliens:
            # Update alien
            alien.update()
            
            # Check if alien should fire
            if alien.should_fire():
                # Get strategy from alien's row
                strategy = min(alien.row + 1, 3)
                
                # Create a bullet
                bullet_x = alien.x + ALIEN_WIDTH // 2
                bullet_y = alien.y + ALIEN_HEIGHT
                bullets.append(Bullet(bullet_x, bullet_y, strategy=strategy))
                
                # Record shot for heatmap
                heatmap.record_shot(bullet_x, bullet_y, strategy)
                
                # Record shot for analyzer
                analyzer.record_shot(strategy)
        
        # Update bullets
        bullets_to_remove = []
        for idx, bullet in enumerate(bullets):
            bullet.update()
            
            # Remove bullets that go off screen
            if bullet.y > SCREEN_HEIGHT:
                bullets_to_remove.append(idx)
            
            # Check collision with player
            if bullet.rect.colliderect(player.rect):
                # Record hit for strategy
                if bullet.strategy:
                    analyzer.record_hit(bullet.strategy)
                bullets_to_remove.append(idx)
        
        # Remove bullets (in reverse order to avoid index issues)
        for idx in sorted(bullets_to_remove, reverse=True):
            if idx < len(bullets):
                bullets.pop(idx)
        
        # Update analyzer
        analyzer.update(1/60)  # Assuming 60 FPS
        
        # Draw everything
        screen.fill(BLACK)
        
        # Draw heatmap
        if show_heatmap:
            heatmap.draw_heatmap(screen)
        
        # Draw aliens
        for alien in alien_group.aliens:
            alien.draw(screen)
        
        # Draw bullets
        for bullet in bullets:
            bullet.draw(screen)
        
        # Draw player
        player.draw(screen)
        
        # Draw strategy panels
        if show_strategy_panels:
            heatmap.draw_strategy_patterns(screen)
        
        # Draw statistics
        if show_stats:
            analyzer.draw_stats(screen)
        
        # Draw legend
        font = pygame.font.SysFont('Arial', 12)
        legend_y = 10
        controls = [
            "Press H to toggle heatmap",
            "Press S to toggle strategy panels",
            "Press T to toggle statistics",
            "Press C to clear heatmap",
            "Press ESC to quit"
        ]
        for control in controls:
            text = font.render(control, True, WHITE)
            screen.blit(text, (SCREEN_WIDTH - text.get_width() - 10, legend_y))
            legend_y += 20
        
        # Update display
        pygame.display.flip()
        
        # Cap framerate
        clock.tick(60)
    
    # Clean up
    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main() 