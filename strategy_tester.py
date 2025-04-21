"""
Space Invaders AI Strategy Tester

Tests individual alien firing strategies with configurable player movement patterns.
"""
import sys
import os
import pygame
import time
import random
import math
from collections import defaultdict

from engine.config import (
    SCREEN_WIDTH, SCREEN_HEIGHT, FPS, BLACK, WHITE, GREEN, RED, BLUE, YELLOW,
    ALIEN_WIDTH, ALIEN_HEIGHT, GAME_AREA_TOP, GAME_AREA_BOTTOM
)
from engine.player import Player
from engine.alien import Alien, AlienBullet
from test_prolog_integration import PrologAlienGroup
from ai.cli_prolog_bridge import CLIPrologBridge

# Create a special Prolog bridge for strategy testing
class StrategyTestPrologBridge(CLIPrologBridge):
    """Special Prolog bridge for strategy testing with direct strategy control."""
    
    def __init__(self):
        """Initialize the bridge with the test Prolog file."""
        super().__init__(prolog_file="ai/strategy_test.pl")
        self.current_strategy = 1
        self.set_strategy(self.current_strategy)
        self.debug = True
    
    def set_strategy(self, strategy_id):
        """Set the strategy to test in Prolog."""
        self.current_strategy = strategy_id
        
        # First retract any existing strategy
        self._execute_query("retractall(strategy(_))")
        
        # Then assert the new strategy
        result = self._execute_query(f"assert(strategy({strategy_id}))")
        return result
    
    def get_strategy(self):
        """Get the currently active strategy."""
        return self.current_strategy
    
    def should_alien_fire(self, alien_id):
        """Override to add debugging."""
        result = super().should_alien_fire(alien_id)
        if self.debug and result:
            print(f"Alien {alien_id} should fire (Strategy {self.current_strategy})")
        return result

# Create modified alien with shorter cooldown
class TestAlien(Alien):
    """Alien with reduced cooldown for testing - completely static."""
    
    def __init__(self, x, y, row, col, alien_id=None):
        super().__init__(x, y, row, col, alien_id)
        self.firing_cooldown = 0
        self.firing_cooldown_time = 10  # Reduced from original for more frequent firing
        self.should_reverse_flag = False  # Don't use the standard movement reversal
        
        # Store original position
        self.original_x = x
        self.original_y = y
    
    def should_reverse(self):
        """Override to prevent standard reversal."""
        return False
        
    def move_horizontal(self):
        """Override to disable movement."""
        # No movement - aliens stay in place
        pass
        
    def move_down(self):
        """Override to disable vertical movement."""
        # No movement - aliens stay in place
        pass
        
    def update(self):
        """Override to ensure position remains fixed."""
        # Reset position to original if it somehow changed
        self.x = self.original_x
        self.y = self.original_y
        self.rect.x = self.x
        self.rect.y = self.y

# Create modified alien group for testing
class TestPrologAlienGroup(PrologAlienGroup):
    """Modified Alien Group for testing with improved debugging."""
    
    def __init__(self, rows, cols, start_x, start_y, h_spacing, v_spacing, prolog_bridge):
        # Initialize aliens array and other properties
        self.aliens = []
        self.bullets = []
        self.next_id = 1
        self.prolog_bridge = prolog_bridge
        self.active_strategy = 1
        self.debug = True
        self.movement_range = 0  # Set to 0 to make aliens static
        self.initial_x = start_x  # Store initial position
        self.direction = 0  # Set to 0 to prevent movement
        self.speed = 0  # Set to 0 to prevent movement
        
        # Create the alien grid
        for row in range(rows):
            for col in range(cols):
                x = start_x + col * (ALIEN_WIDTH + h_spacing)
                y = start_y + row * (ALIEN_HEIGHT + v_spacing)
                
                # Create test alien with short cooldown
                alien = TestAlien(x, y, row, col, self.next_id)
                alien.firing_cooldown_time = 10  # Short cooldown
                alien.firing_cooldown = random.randint(0, 10)  # Stagger initial cooldowns
                self.aliens.append(alien)
                self.next_id += 1
    
    def update(self, player=None, barriers=None, stats_tracker=None):
        """Override update to add better debugging and ensure firing checks happen."""
        # Update Prolog knowledge base with current game state
        if player:
            screen_size = (SCREEN_WIDTH, SCREEN_HEIGHT)
            self.prolog_bridge.update_state(player, self.aliens, barriers or [], screen_size)
        
        # No movement code here - aliens are static
        
        # Update all active aliens
        for alien in self.aliens:
            if alien.active:
                # No movement applied, aliens stay in place
                
                # Update cooldown
                if alien.firing_cooldown > 0:
                    alien.firing_cooldown -= 1
                
                # Check if alien should fire
                if alien.firing_cooldown == 0:
                    should_fire = self.prolog_bridge.should_fire(alien.id) if hasattr(self.prolog_bridge, 'should_fire') else self.prolog_bridge.should_alien_fire(alien.id)
                    if should_fire:
                        # Create bullet
                        bullet = AlienBullet(
                            alien.x + alien.width // 2,
                            alien.y + alien.height
                        )
                        self.bullets.append(bullet)
                        
                        # Record shot in stats tracker if provided
                        if stats_tracker:
                            stats_tracker.record_shot(bullet.x, bullet.y)
                        
                        # Reset cooldown
                        alien.firing_cooldown = alien.firing_cooldown_time
                        
                        if self.debug:
                            print(f"Alien {alien.id} fired a bullet at x={bullet.x}, y={bullet.y}")
        
        # Update bullets
        for bullet in self.bullets[:]:
            bullet.update()
            # Remove bullets that are off-screen or deactivated
            if not bullet.active or bullet.y > SCREEN_HEIGHT:
                self.bullets.remove(bullet)

# Strategy names
STRATEGY_NAMES = {
    1: "Direct Targeting",
    2: "Predictive Targeting",
    3: "Crossfire Trap"
}

# Player movement patterns
MOVEMENT_PATTERNS = {
    1: "Static",
    2: "Left-Right Sweep",
    3: "Random",
    4: "Manual Control"
}

class StatTracker:
    """Tracks and displays statistics for strategy testing."""
    
    def __init__(self):
        self.shots_fired = 0
        self.hits = 0
        self.time_started = time.time()
        self.shots_over_time = []  # (time, x, y) for each shot
        self.player_positions = []  # (time, x) for player positions
        self.hits_positions = []  # (time, x) for each hit
        self.last_reset_time = time.time()  # Time of last reset
    
    def reset(self):
        """Reset all statistics."""
        self.shots_fired = 0
        self.hits = 0
        self.time_started = time.time()
        self.shots_over_time = []
        self.player_positions = []
        self.hits_positions = []
        self.last_reset_time = time.time()
    
    def record_shot(self, x, y):
        """Record a shot fired at position."""
        self.shots_fired += 1
        self.shots_over_time.append((time.time() - self.time_started, x, y))
    
    def record_hit(self, x):
        """Record a hit at position."""
        self.hits += 1
        self.hits_positions.append((time.time() - self.time_started, x))
    
    def record_player_position(self, x):
        """Record the player's position."""
        self.player_positions.append((time.time() - self.time_started, x))
    
    def get_hit_rate(self):
        """Calculate hit rate."""
        if self.shots_fired == 0:
            return 0
        return self.hits / self.shots_fired * 100
    
    def get_shots_per_second(self):
        """Calculate shots per second."""
        elapsed = time.time() - self.time_started
        if elapsed == 0:
            return 0
        return self.shots_fired / elapsed
    
    def get_recent_stats(self, window_seconds=5):
        """Get statistics for the last few seconds."""
        current_time = time.time()
        recent_time = current_time - window_seconds
        
        # Count recent shots
        recent_shots = sum(1 for t, _, _ in self.shots_over_time 
                         if t > recent_time - self.time_started)
        
        # Count recent hits
        recent_hits = sum(1 for t, _ in self.hits_positions 
                         if t > recent_time - self.time_started)
        
        # Calculate recent hit rate
        recent_hit_rate = 0
        if recent_shots > 0:
            recent_hit_rate = recent_hits / recent_shots * 100
            
        # Calculate recent shots per second
        recent_shots_per_second = recent_shots / min(window_seconds, current_time - self.last_reset_time)
        
        return {
            'shots': recent_shots,
            'hits': recent_hits,
            'hit_rate': recent_hit_rate,
            'shots_per_second': recent_shots_per_second
        }

    def draw_stats(self, screen, font, y_start=10):
        """Draw statistics on screen."""
        elapsed = time.time() - self.time_started
        
        # Get recent stats (last 5 seconds)
        recent = self.get_recent_stats(5)
        
        stats = [
            f"Test Duration: {elapsed:.1f}s",
            f"Total Shots: {self.shots_fired}",
            f"Total Hits: {self.hits}",
            f"Overall Hit Rate: {self.get_hit_rate():.1f}%",
            f"Overall Shots/Sec: {self.get_shots_per_second():.2f}",
            "",
            f"Last 5s Shots: {recent['shots']}",
            f"Last 5s Hits: {recent['hits']}",
            f"Last 5s Hit Rate: {recent['hit_rate']:.1f}%",
            f"Last 5s Shots/Sec: {recent['shots_per_second']:.2f}"
        ]
        
        y = y_start
        for stat in stats:
            text = font.render(stat, True, WHITE)
            screen.blit(text, (SCREEN_WIDTH - text.get_width() - 10, y))
            y += 25

class StrategyTester:
    """Test environment for alien firing strategies."""
    
    def __init__(self):
        """Initialize the tester."""
        # Initialize pygame
        pygame.init()
        
        # Create the screen
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Alien Strategy Tester")
        
        # Set up clock
        self.clock = pygame.time.Clock()
        
        # Load fonts
        font_path = os.path.join('assets', 'Font', 'monogram.ttf')
        try:
            self.font = pygame.font.Font(font_path, 24)
            self.title_font = pygame.font.Font(font_path, 36)
        except FileNotFoundError:
            print("Could not load custom font, falling back to system font")
            self.font = pygame.font.SysFont(None, 24)
            self.title_font = pygame.font.SysFont(None, 36)
        
        # Create specialized prolog bridge for testing
        self.prolog_bridge = StrategyTestPrologBridge()
        
        # Default test settings
        self.current_strategy = 1  # Direct targeting
        self.current_movement = 2  # Left-right sweep
        self.player_auto_speed = 5
        self.random_move_counter = 0
        self.direction = 1  # 1 for right, -1 for left
        self.debug_mode = False  # Debug mode toggle
        
        # Create stats tracker
        self.stats = StatTracker()
        
        # Add recent hits visualization
        self.recent_hits = []  # List of (x, y, time) for recent hits
        
        # Initialize game objects
        self.init_game_objects()
    
    def init_game_objects(self):
        """Initialize game objects based on current settings."""
        # Create player
        self.player = Player(SCREEN_WIDTH // 2, GAME_AREA_BOTTOM)
        
        # Create alien group with just the specific strategy
        rows = 1
        cols = 7
        alien_start_x = 100
        alien_start_y = GAME_AREA_TOP + 100
        h_spacing = 60
        v_spacing = 50
        
        # Set strategy in Prolog
        self.prolog_bridge.set_strategy(self.current_strategy)
        
        self.aliens = TestPrologAlienGroup(
            rows, cols,
            alien_start_x, alien_start_y,
            h_spacing, v_spacing,
            self.prolog_bridge
        )
        
        # Set active strategy in alien group too (for display)
        self.aliens.active_strategy = self.current_strategy
        
        # Set player auto speed based on strategy for better testing
        if self.current_strategy == 2:  # Predictive targeting works better with faster player
            self.player_auto_speed = 8  # Faster movement for predictive strategy
        else:
            self.player_auto_speed = 5  # Normal speed for other strategies
        
        # Reset stats
        self.stats.reset()
        self.recent_hits = []
    
    def handle_events(self):
        """Handle pygame events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return False
                elif event.key == pygame.K_1:
                    self.current_strategy = 1
                    self.init_game_objects()
                elif event.key == pygame.K_2:
                    self.current_strategy = 2
                    self.init_game_objects()
                elif event.key == pygame.K_3:
                    self.current_strategy = 3
                    self.init_game_objects()
                elif event.key == pygame.K_a:
                    self.current_movement = 1  # Static
                elif event.key == pygame.K_s:
                    self.current_movement = 2  # Left-Right sweep
                elif event.key == pygame.K_d:
                    self.current_movement = 3  # Random
                elif event.key == pygame.K_f:
                    self.current_movement = 4  # Manual
                elif event.key == pygame.K_r:
                    self.init_game_objects()
                    self.stats.reset()  # Reset stats when resetting game
                elif event.key == pygame.K_b:
                    # Toggle debug mode
                    self.debug_mode = not self.debug_mode
                    self.prolog_bridge.debug = self.debug_mode
        
        return True
    
    def update_player_position(self):
        """Update player position based on selected movement pattern."""
        # Record current position for stats
        self.stats.record_player_position(self.player.x)
        
        if self.current_movement == 1:  # Static
            # Player stays in the middle
            self.player.x = SCREEN_WIDTH // 2
        
        elif self.current_movement == 2:  # Left-Right Sweep
            # Move player back and forth
            self.player.x += self.player_auto_speed * self.direction
            
            # Reverse direction at edges
            if self.player.x <= 50:
                self.direction = 1
            elif self.player.x >= SCREEN_WIDTH - 50:
                self.direction = -1
        
        elif self.current_movement == 3:  # Random
            # Occasionally change direction
            self.random_move_counter -= 1
            if self.random_move_counter <= 0:
                self.direction = random.choice([-1, 1])
                self.random_move_counter = random.randint(30, 70)  # Longer movements for better prediction
            
            # Move player randomly
            self.player.x += self.player_auto_speed * self.direction
            
            # Stay within boundaries
            if self.player.x <= 50:
                self.player.x = 50
                self.direction = 1
            elif self.player.x >= SCREEN_WIDTH - 50:
                self.player.x = SCREEN_WIDTH - 50
                self.direction = -1
        
        elif self.current_movement == 4:  # Manual Control
            # Get pressed keys for manual movement
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT]:
                self.player.move_left()
            if keys[pygame.K_RIGHT]:
                self.player.move_right()
        
        # Update player rect
        self.player.rect.x = self.player.x
    
    def update(self):
        """Update game state."""
        # Update player position based on movement pattern
        self.update_player_position()
        
        # Update the player (for bullets)
        self.player.update()
        
        # Update aliens with our player for targeting, passing stats tracker
        self.aliens.update(self.player, None, self.stats)
        
        # Check for hits
        # Alien bullets hitting player
        for bullet in self.aliens.get_active_bullets():
            # We're now recording shots when they're created, not here
            
            if bullet.collides_with(self.player):
                self.stats.record_hit(self.player.x)
                # Add hit to recent hits list with current time
                self.recent_hits.append((bullet.x, bullet.y, time.time()))
                bullet.deactivate()
        
        # Clean up old hit visualizations after 1.5 seconds
        current_time = time.time()
        self.recent_hits = [hit for hit in self.recent_hits if current_time - hit[2] < 1.5]
    
    def draw(self):
        """Draw the game state."""
        # Fill the background
        self.screen.fill(BLACK)
        
        # Draw game objects
        self.player.draw(self.screen)
        self.aliens.draw(self.screen)
        
        # Draw bullet paths more visibly
        for bullet in self.aliens.get_active_bullets():
            # Draw a more visible bullet
            pygame.draw.rect(
                self.screen,
                RED,
                pygame.Rect(bullet.x - 2, bullet.y - 2, 4, 15)
            )
            # Draw a tail for visibility
            pygame.draw.line(
                self.screen,
                (255, 100, 100),  # Light red
                (bullet.x, bullet.y),
                (bullet.x, bullet.y - 10),
                1
            )
        
        # Draw recent hits with explosion effect
        for hit_x, hit_y, hit_time in self.recent_hits:
            # Calculate size based on age (shrinks over time)
            age = time.time() - hit_time
            size = int(20 * (1.5 - age))
            if size > 0:
                pygame.draw.circle(
                    self.screen,
                    YELLOW,
                    (hit_x, hit_y),
                    size
                )
                pygame.draw.circle(
                    self.screen,
                    RED,
                    (hit_x, hit_y),
                    size // 2
                )
        
        # Draw title with debug indicator and static alien note
        title_text = f"Static Aliens - Strategy Test: {STRATEGY_NAMES.get(self.current_strategy)}"
        if self.debug_mode:
            title_text += " [DEBUG ON]"
            
        title = self.title_font.render(title_text, True, YELLOW)
        self.screen.blit(title, (20, 10))
        
        # Draw movement pattern
        movement = self.font.render(f"Movement: {MOVEMENT_PATTERNS.get(self.current_movement)}", True, GREEN)
        self.screen.blit(movement, (20, 50))
        
        # Draw strategy-specific visualizations
        if self.current_strategy == 1:  # Direct Targeting
            # Draw vertical targeting lines under each alien
            for alien in self.aliens.aliens:
                if alien.active:
                    # Draw direct target line
                    pygame.draw.line(
                        self.screen,
                        (50, 150, 255),  # Light blue for direct targeting
                        (alien.x + alien.width // 2, alien.y + alien.height),
                        (alien.x + alien.width // 2, GAME_AREA_BOTTOM),
                        1
                    )
        
        elif self.current_strategy == 2:  # Predictive Targeting
            # Draw the player's current position
            pygame.draw.circle(
                self.screen, 
                WHITE, 
                (self.player.x, self.player.y), 
                6, 
                1
            )
            
            # Calculate player's movement direction
            if not hasattr(self, 'last_player_x'):
                self.last_player_x = self.player.x
                self.player_direction = 0
            
            # Determine player direction
            if self.player.x > self.last_player_x + 5:
                self.player_direction = 1  # Moving right
            elif self.player.x < self.last_player_x - 5:
                self.player_direction = -1  # Moving left
            
            # Calculate predicted position (150 pixels in direction of movement)
            if self.player_direction != 0:
                predicted_x = self.player.x + (self.player_direction * 150)
            else:
                # Fallback if no direction detected
                screen_center = SCREEN_WIDTH // 2
                if self.player.x < screen_center:
                    predicted_x = self.player.x + 150
                else:
                    predicted_x = self.player.x - 150
            
            # Ensure prediction is within bounds
            predicted_x = max(50, min(SCREEN_WIDTH - 50, predicted_x))
            
            # Store last player position for next frame
            self.last_player_x = self.player.x
            
            # Draw the predicted position
            pygame.draw.circle(
                self.screen, 
                GREEN, 
                (int(predicted_x), self.player.y), 
                8, 
                1
            )
            
            # Draw arrow indicating prediction direction
            pygame.draw.line(
                self.screen,
                GREEN,
                (self.player.x, self.player.y),
                (predicted_x, self.player.y),
                2
            )
            # Add arrowhead
            arrow_size = 8
            if predicted_x > self.player.x:
                # Arrow pointing right
                pygame.draw.polygon(
                    self.screen,
                    GREEN,
                    [
                        (predicted_x - arrow_size, self.player.y - arrow_size//2),
                        (predicted_x, self.player.y),
                        (predicted_x - arrow_size, self.player.y + arrow_size//2)
                    ]
                )
            else:
                # Arrow pointing left
                pygame.draw.polygon(
                    self.screen,
                    GREEN,
                    [
                        (predicted_x + arrow_size, self.player.y - arrow_size//2),
                        (predicted_x, self.player.y),
                        (predicted_x + arrow_size, self.player.y + arrow_size//2)
                    ]
                )
            
            # Draw direction indicator
            dir_text = f"Direction: {'Right' if self.player_direction > 0 else 'Left' if self.player_direction < 0 else 'None'}"
            dir_surface = self.font.render(dir_text, True, GREEN)
            self.screen.blit(dir_surface, (self.player.x - 50, self.player.y - 30))
            
            # Draw vertical lines from aliens to show targeting areas
            for alien in self.aliens.aliens:
                if alien.active:
                    # Draw alien center line
                    pygame.draw.line(
                        self.screen,
                        (80, 80, 80),  # Dark gray for alien center
                        (alien.x + alien.width // 2, alien.y + alien.height),
                        (alien.x + alien.width // 2, GAME_AREA_BOTTOM),
                        1
                    )
                    
                    # Check if predicted position is within firing range of this alien
                    alien_center_x = alien.x + alien.width // 2
                    if abs(alien_center_x - predicted_x) < 40:
                        # Draw highlighting for aliens that would fire at predicted position
                        pygame.draw.rect(
                            self.screen,
                            (0, 255, 0, 128),  # Transparent green
                            pygame.Rect(
                                alien.x - 5, 
                                alien.y - 5, 
                                alien.width + 10, 
                                alien.height + 10
                            ),
                            2
                        )
                        
                        # Draw prediction target zone
                        pygame.draw.line(
                            self.screen,
                            (0, 255, 0),  # Bright green for hit zone
                            (alien_center_x, alien.y + alien.height),
                            (predicted_x, GAME_AREA_BOTTOM),
                            1
                        )
                    
                    # Draw targeting margin (40 pixels on each side)
                    left_margin = alien_center_x - 40
                    right_margin = alien_center_x + 40
                    pygame.draw.line(
                        self.screen,
                        (50, 255, 100, 128),  # Transparent green
                        (left_margin, alien.y + alien.height),
                        (left_margin, GAME_AREA_BOTTOM),
                        1
                    )
                    pygame.draw.line(
                        self.screen,
                        (50, 255, 100, 128),  # Transparent green
                        (right_margin, alien.y + alien.height),
                        (right_margin, GAME_AREA_BOTTOM),
                        1
                    )
        
        elif self.current_strategy == 3:  # Crossfire Trap Pattern
            # Highlight the "bottom row" aliens which are the ones that will fire
            bottom_aliens = []
            for alien in self.aliens.aliens:
                if alien.active:
                    # Check if it's a bottom alien (no aliens below it)
                    is_bottom = True
                    for other in self.aliens.aliens:
                        if other.active and other.col == alien.col and other.row > alien.row:
                            is_bottom = False
                            break
                    
                    if is_bottom:
                        bottom_aliens.append(alien)
            
            # Draw highlight for bottom aliens
            for alien in bottom_aliens:
                pygame.draw.rect(
                    self.screen,
                    (255, 255, 0, 128),  # Transparent yellow
                    pygame.Rect(
                        alien.x - 5, 
                        alien.y - 5, 
                        alien.width + 10, 
                        alien.height + 10
                    ),
                    2
                )
            
            # Visualize the crossfire trap pattern
            if hasattr(self, 'player_direction') and bottom_aliens:
                # Get player position and direction
                player_x = self.player.x
                direction = self.player_direction
                
                # Calculate trap zone positions
                # Central position is the player's current position
                center_pos = player_x
                
                # Left and right trap positions with dynamic sizing based on movement direction
                left_offset = 60 + (direction * -20)  # Wider if moving left
                right_offset = 60 + (direction * 20)  # Wider if moving right
                left_pos = max(50, player_x - left_offset)
                right_pos = min(SCREEN_WIDTH - 50, player_x + right_offset)
                
                # Draw trap zones
                # Center trap zone (player position)
                pygame.draw.circle(
                    self.screen,
                    (255, 0, 0),  # Red for center/player position
                    (center_pos, self.player.y),
                    10,
                    2
                )
                
                # Left trap zone
                pygame.draw.circle(
                    self.screen,
                    (255, 165, 0),  # Orange for left trap
                    (int(left_pos), self.player.y),
                    15,
                    2
                )
                
                # Right trap zone
                pygame.draw.circle(
                    self.screen,
                    (255, 165, 0),  # Orange for right trap
                    (int(right_pos), self.player.y),
                    15,
                    2
                )
                
                # Draw trap zone connecting lines
                pygame.draw.line(
                    self.screen,
                    (255, 100, 100),  # Light red
                    (center_pos, self.player.y),
                    (int(left_pos), self.player.y),
                    1
                )
                pygame.draw.line(
                    self.screen,
                    (255, 100, 100),  # Light red
                    (center_pos, self.player.y),
                    (int(right_pos), self.player.y),
                    1
                )
                
                # Draw trap widths to show dynamic sizing
                # Add directional indicator to show trap expansion
                if direction != 0:
                    arrow_length = 15
                    arrow_width = 10
                    
                    # Direction indicator at right position
                    if direction > 0:  # Moving right
                        pygame.draw.polygon(
                            self.screen,
                            (255, 200, 100),
                            [
                                (int(right_pos) - arrow_width, self.player.y),
                                (int(right_pos) + arrow_length, self.player.y),
                                (int(right_pos), self.player.y + arrow_width),
                            ]
                        )
                    else:  # Moving left
                        pygame.draw.polygon(
                            self.screen,
                            (255, 200, 100),
                            [
                                (int(left_pos) + arrow_width, self.player.y),
                                (int(left_pos) - arrow_length, self.player.y),
                                (int(left_pos), self.player.y + arrow_width),
                            ]
                        )
                
                # Assign and visualize firing zones for each bottom alien
                for alien in bottom_aliens:
                    alien_center_x = alien.x + alien.width // 2
                    
                    # Determine target position for this alien
                    if abs(alien_center_x - player_x) < 100:
                        # Aliens near center target the player directly
                        target_pos = center_pos
                        color = (255, 0, 0)  # Red
                    elif alien_center_x < player_x:
                        # Aliens to the left set the left trap
                        target_pos = left_pos
                        color = (255, 140, 0)  # Dark orange
                    else:
                        # Aliens to the right set the right trap
                        target_pos = right_pos
                        color = (255, 140, 0)  # Dark orange
                    
                    # Check if alien is well-positioned to hit assigned target
                    if abs(alien_center_x - target_pos) < 80:
                        # Draw targeting line from this alien to its assigned target
                        pygame.draw.line(
                            self.screen,
                            color,
                            (alien_center_x, alien.y + alien.height),
                            (int(target_pos), self.player.y),
                            2
                        )
                        
                        # Highlight this alien with its targeting color
                        pygame.draw.rect(
                            self.screen,
                            color,
                            pygame.Rect(
                                alien.x - 7, 
                                alien.y - 7, 
                                alien.width + 14, 
                                alien.height + 14
                            ),
                            3
                        )
        
        # Draw controls help
        controls = [
            "Controls:",
            "1-3: Change strategy",
            "A: Static position",
            "S: Left-right sweep",
            "D: Random movement",
            "F: Manual control",
            "R: Reset test",
            "B: Toggle debug mode",
            "ESC: Quit"
        ]
        
        y = 100
        for control in controls:
            text = self.font.render(control, True, WHITE)
            self.screen.blit(text, (20, y))
            y += 30
        
        # Draw strategy description
        strategy_descriptions = {
            1: "Direct Targeting: Aliens fire when player is directly below (±20px)",
            2: "Predictive Targeting: Aliens aim 150px ahead in player's movement direction",
            3: "Crossfire Trap: Aliens create a trap zone that's harder to escape as you move"
        }
        
        if self.current_strategy in strategy_descriptions:
            desc = self.font.render(strategy_descriptions[self.current_strategy], True, YELLOW)
            self.screen.blit(desc, (20, y + 20))
        
        # Draw statistics
        self.stats.draw_stats(self.screen, self.font)
        
        # Draw special indicators for movement patterns
        if self.current_movement == 1:  # Static
            # Draw target zone
            pygame.draw.line(
                self.screen, RED, 
                (self.player.x, GAME_AREA_BOTTOM - 20), 
                (self.player.x, GAME_AREA_TOP), 
                1
            )
        
        elif self.current_movement == 2:  # Left-Right sweep
            # Draw sweep zone
            pygame.draw.line(
                self.screen, GREEN, 
                (50, GAME_AREA_BOTTOM - 30), 
                (SCREEN_WIDTH - 50, GAME_AREA_BOTTOM - 30), 
                2
            )
        
        # Update the display
        pygame.display.flip()
    
    def run(self):
        """Run the main loop."""
        running = True
        while running:
            running = self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(FPS)
        
        # Quit pygame
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    tester = StrategyTester()
    tester.run() 