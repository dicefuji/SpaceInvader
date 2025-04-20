# Space Invaders with Prolog AI

A recreation of the classic Space Invaders game with AI opponents controlled through Prolog logic.

## Project Overview

This project features:
- A Python/Pygame-based Space Invaders game engine
- Prolog-driven AI for alien invaders
- Python-Prolog integration via pyswip
- Multiple AI strategies with row-based strategy system
- Visual strategy indicators with distinct colors

## Project Structure

- `engine/`: Core game engine components
  - `entity.py`: Base entity class for all game objects
  - `player.py`: Player spaceship implementation
  - `alien.py`: Alien invaders implementation
  - `barrier.py`: Defensive barriers implementation
  - `config.py`: Game configuration and constants
  - `game_state.py`: Game state management
  - `ui.py`: User interface elements
  
- `ai/`: Prolog AI integration
  - `invader_ai.pl`: Prolog knowledge base for alien behaviors
  - `prolog_bridge.py`: Python-Prolog integration
  
- `assets/`: Game assets (images, sounds)
  - `images/`: Sprite images
  - `sounds/`: Sound effects

- `test_row_strategies.py`: Tool for testing and analyzing row-based strategies

## Game Features

- Classic Space Invaders gameplay
- Full game state management (menu, playing, game over)
- Lives system and scoring
- Barriers that can be damaged and destroyed
- Win and lose conditions
- Standard arcade-style UI
- Prolog-driven alien behavior with Python fallback
- Row-based strategy system with 5 distinct strategies

## Row-Based Strategy System

Each row of aliens employs a different firing strategy, visually identified by color:

1. **Row 1 (Red)**: Direct Targeting - Fires when player is directly below
2. **Row 2 (Green)**: Predictive Targeting - Predicts player movement and fires ahead
3. **Row 3 (Blue)**: Random Firing - Random chance to fire with no targeting
4. **Row 4 (Yellow)**: Coordinated Firing - Only bottom aliens in each column fire
5. **Row 5 (Purple)**: Barrier Avoidance - Avoids firing when barriers would block shots

This creates a more dynamic and visually distinctive gameplay experience where players must adapt to different threats simultaneously.

## Setup

1. Create a virtual environment:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Install SWI-Prolog from: https://www.swi-prolog.org/download/stable

## Running the Game

### Standard Version (Python-only)
To play the standard version with hardcoded AI:
```
python space_invaders.py
```

### Prolog AI Version
To play with Prolog-driven AI (requires SWI-Prolog and pyswip):
```
python space_invaders_prolog.py
```

### Testing the Strategies
To analyze and test individual row strategies:
```
python test_row_strategies.py
```

The test tool provides:
- Individual row/strategy testing
- Shot pattern visualization
- Strategy performance statistics
- Auto-test mode for consistent analysis

### Test Scripts
For testing specific components:
```
python test_components.py       # Test basic game components
python test_prolog_integration.py   # Test Prolog integration
```

## Controls
- Left/Right Arrow: Move player
- Space: Shoot
- Enter: Start game / Restart
- 0: Toggle between row-based and global strategies
- Q: Quit game

## Gameplay Instructions

1. Press Enter on the main menu to start the game
2. Use the arrow keys to move and Space to shoot
3. Destroy all aliens to win
4. Avoid alien bullets and don't let aliens reach the bottom
5. Use barriers for protection (they can be destroyed)
6. The game is over when you run out of lives or aliens reach the bottom
7. Note the different alien colors indicating their strategy

## Strategy Tips

- **Against Red aliens (Direct Targeting)**: Keep moving, don't stay under them
- **Against Green aliens (Predictive)**: Change direction frequently to break prediction
- **Against Blue aliens (Random)**: Always be ready for unexpected shots
- **Against Yellow aliens (Coordinated)**: Prioritize destroying bottom aliens
- **Against Purple aliens (Barrier Avoidance)**: Use barriers as shields when possible

## Prolog AI Implementation

The Prolog implementation uses a knowledge base (`ai/invader_ai.pl`) that contains:
- Facts about the current game state (player position, alien positions, etc.)
- Rules for alien movement decisions
- Rules for alien firing decisions with different strategies
- Helper predicates for decision-making
- Row-based strategy assignment system

The Python-Prolog bridge (`ai/prolog_bridge.py`) handles:
- Communication between Python and Prolog
- Serializing game state to Prolog facts
- Querying Prolog for alien decisions
- Translating Prolog outputs to game actions
- Fallback behavior when Prolog initialization fails

## Future Enhancements

See `NEXT_STEPS.md` for planned enhancements and `AI_STRATEGY_TESTING_RESULTS.md` for strategy analysis.