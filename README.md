# Space Invaders with Prolog AI

A recreation of the classic Space Invaders game with AI opponents controlled through Prolog logic.

## Project Overview

This project features:
- A Python/Pygame-based Space Invaders game engine
- Prolog-driven AI for alien invaders
- CLI-based Prolog bridge for cross-platform compatibility
- Smooth player movement with dual update system
- Sprite-based graphics with classic Space Invaders look
- Multiple AI strategies with different alien behaviors

## Project Structure

- `engine/`: Core game engine components
  - `entity.py`: Base entity class for all game objects
  - `player.py`: Player spaceship implementation
  - `smooth_player.py`: Enhanced player with smoother movement
  - `alien.py`: Alien invaders implementation
  - `barrier.py`: Defensive barriers implementation
  - `config.py`: Game configuration and constants
  - `game_state.py`: Game state management
  - `ui.py`: User interface elements
  - `sprites.py`: Sprite management for game graphics
  
- `ai/`: Prolog AI integration
  - `invader_ai.pl`: Prolog knowledge base for alien behaviors
  - `invader_ai_simple.pl`: Simplified Prolog knowledge base
  - `prolog_bridge.py`: Python-Prolog integration with PySwip
  - `cli_prolog_bridge.py`: CLI-based Prolog bridge for better compatibility
  
- `assets/`: Game assets (images, sounds)
  - `Graphics/`: Sprite images for aliens and player
  - `Font/`: Game fonts

- `test_cli_integration.py`: Test script for CLI-based Prolog bridge
- `test_row_strategies.py`: Tool for testing and analyzing row-based strategies

## Game Features

- Classic Space Invaders gameplay with authentic sprites
- Ultra-smooth player movement with subframe updates
- Full game state management (menu, playing, game over)
- Lives system and scoring
- Barriers that can be damaged and destroyed
- Win and lose conditions
- Standard arcade-style UI
- Prolog-driven alien behavior
- Enhanced visual effects for bullets and shots
- Cross-platform compatibility for macOS, Windows, and Linux

## Recent Enhancements

1. **Smooth Player Movement**:
   - Implemented a dual update system for smooth player controls
   - Player updates at 60fps with sub-frame precision
   - Maintains classic frame-by-frame alien movement while player moves smoothly

2. **Sprite-Based Graphics**:
   - Classic Space Invaders sprites for aliens and player
   - Three types of aliens with different appearances
   - Enhanced bullet visuals with distinctive designs
   - Proper sprite scaling and management

3. **Cross-Platform Compatibility**:
   - CLI-based Prolog bridge for macOS (including Apple Silicon) compatibility
   - No more dependency on PySwip for Apple Silicon users
   - Improved error handling and robustness

4. **Performance Optimizations**:
   - Enhanced game speed and responsiveness
   - Optimized collision detection
   - Sprite caching for better performance
   - Time-based movement calculations

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
To play with Prolog-driven AI (requires SWI-Prolog):
```
python space_invaders_prolog.py
```

### Testing the Strategies
To analyze and test individual row strategies:
```
python test_row_strategies.py
```

### Test Scripts
For testing specific components:
```
python test_prolog_integration.py   # Test Prolog integration
python test_cli_integration.py      # Test CLI-based Prolog bridge
```

## Controls
- Left/Right Arrow: Move player
- Space: Shoot
- Enter: Start game / Restart
- Q: Quit game

## Gameplay Instructions

1. Press Enter on the main menu to start the game
2. Use the arrow keys to move and Space to shoot
3. Destroy all aliens to win
4. Avoid alien bullets and don't let aliens reach the bottom
5. Use barriers for protection (they can be destroyed)
6. The game is over when you run out of lives or aliens reach the bottom

## Prolog AI Implementation

The Prolog implementation uses a knowledge base (`ai/invader_ai.pl`) that contains:
- Facts about the current game state (player position, alien positions, etc.)
- Rules for alien movement decisions
- Rules for alien firing decisions with different strategies
- Helper predicates for decision-making
- Row-based strategy assignment system

The CLI-based Prolog bridge (`ai/cli_prolog_bridge.py`) handles:
- Communication between Python and Prolog via command-line interface
- Serializing game state to Prolog facts
- Querying Prolog for alien decisions
- Translating Prolog outputs to game actions
- Cross-platform compatibility without PySwip

## Future Enhancements

- Sound effects and music
- Additional levels with increasing difficulty
- More alien types and behaviors
- Power-ups and special weapons
- High score saving system