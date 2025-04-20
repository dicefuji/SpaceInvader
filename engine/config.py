# Game window settings
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = "Space Invaders with Prolog AI"
FPS = 60  # Base frame rate for the overall game

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# Player settings
PLAYER_WIDTH = 60
PLAYER_HEIGHT = 40
PLAYER_SPEED = 40  # Adjusted for optimal player movement
PLAYER_BULLET_SPEED = 40  # Increased for faster bullets

# Alien settings
ALIEN_WIDTH = 50
ALIEN_HEIGHT = 40
ALIEN_HORIZONTAL_SPACING = 10
ALIEN_VERTICAL_SPACING = 10
ALIEN_ROWS = 5
ALIEN_COLS = 11
ALIEN_HORIZONTAL_SPEED = 10  # Kept deliberately slow for classic movement
ALIEN_VERTICAL_SPEED = 20
ALIEN_BULLET_SPEED = 10  # Kept slow for classic alien bullet movement

# Barrier settings
BARRIER_COUNT = 4
BARRIER_WIDTH = 80
BARRIER_HEIGHT = 60
BARRIER_SEGMENTS_X = 8
BARRIER_SEGMENTS_Y = 6
BARRIER_SEGMENT_SIZE = 10  # Size of each segment block

# Game area settings
GAME_AREA_TOP = 60  # Top of play area (below score/UI)
GAME_AREA_BOTTOM = 550  # Bottom of play area (above player zone)

# Bullet settings
BULLET_WIDTH = 4
BULLET_HEIGHT = 10

# Game progression
ALIEN_SPEED_INCREASE = 0.3  # Increased from 0.2 - How much to increase alien speed when aliens are destroyed 