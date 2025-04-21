# Space Invaders with Intelligent AI Strategies

A recreation of the classic Space Invaders game with advanced AI opponents controlled through Prolog-driven strategies.

## Project Overview

This project enhances the classic Space Invaders game with:
- A Python/Pygame-based game engine with smooth graphics
- Prolog-driven AI with three distinct intelligent strategies
- Comprehensive testing tools to evaluate and visualize AI behavior
- Cross-platform compatibility through CLI-based Prolog integration
- Detailed statistical analysis of AI performance
- Row-based strategy assignment for varied gameplay experience

## AI Strategy System

The game features three distinct AI strategies for alien firing behavior:

1. **Direct Targeting**: Top-row aliens fire when the player is directly below them, creating a reactive but predictable pattern.

2. **Predictive Targeting**: Middle-row aliens predict where the player will be based on movement direction, creating a more challenging experience for players who move consistently.

3. **Crossfire Trap Pattern**: Bottom-row aliens coordinate to create a trap zone around the player that dynamically adjusts based on movement, making it difficult to escape bullets by using standard dodging techniques.

## Links to Demos

Game: https://drive.google.com/file/d/1tbgtli5ac3EbDxKi75CZNdCqFaZh9gAX/view?usp=drive_link

Testing: https://drive.google.com/file/d/1tG3lIvL6kpQf17icKUFWJs1EX7mN84R2/view?usp=drive_link

## Project Structure

- `space_invaders.py`: Main game script
- `strategy_tester.py`: Specialized tool for testing and analyzing AI strategies
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
  - `invader_ai.pl`: Main Prolog knowledge base with all three strategies
  - `strategy_test.pl`: Specialized Prolog file for testing strategies in isolation
  - `invader_ai_simple.pl`: Simplified Prolog knowledge base for beginners
  - `cli_prolog_bridge.py`: CLI-based Prolog bridge for cross-platform compatibility
  - `prolog_bridge.py`: Python-Prolog integration with PySwip (alternative method)
  
- `assets/`: Game assets (images, sounds)
  - `Graphics/`: Sprite images for aliens and player
  - `Font/`: Game fonts

- `test_prolog_integration.py`: Test script for PySwip Prolog bridge
- `test_cli_integration.py`: Test script for CLI-based Prolog bridge
- `CROSSFIRE_TRAP_STRATEGY.md`: Documentation for the Crossfire Trap Pattern
- `AI_STRATEGY_REPORT.md`: Comprehensive report on the AI strategies and testing results

## Game Features

- Classic Space Invaders gameplay with authentic sprites
- Ultra-smooth player movement with subframe updates
- Three distinct AI strategies with different behaviors and challenges
- Statistical tracking of strategy performance
- Full game state management (menu, playing, game over)
- Lives system and scoring
- Barriers that can be damaged and destroyed
- Win and lose conditions
- Visual effects for hits, explosions, and bullet paths
- Cross-platform compatibility for macOS (including Apple Silicon), Windows, and Linux

## Recent Enhancements

1. **Advanced AI Strategy System**:
   - Three distinct AI strategies with different targeting methods
   - Row-based strategy assignment to create varied gameplay
   - Dynamic trap zones for coordinated alien firing
   - Player movement prediction for anticipatory targeting

2. **Strategy Testing Environment**:
   - Dedicated testing tool with visual feedback
   - Statistical analysis of hit rates and performance
   - Real-time visualization of strategy behavior
   - Configurable player movement patterns
   - Interactive strategy switching and parameter tuning

3. **Enhanced Visuals and Feedback**:
   - Improved bullet visibility with visual trails
   - Hit impact visualization with explosion effects
   - Color-coded targeting indicators in test mode
   - Real-time statistical display

4. **Performance Optimizations**:
   - Optimized Prolog queries for better performance
   - Efficient collision detection
   - Minimal computational overhead for AI strategies
   - Time-based movement calculations

## Requirements

- Python 3.8+
- Pygame 2.0+
- SWI-Prolog 8.2.0+

## Setup

1. Create a virtual environment:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. Install dependencies:
   ```
   pip install pygame
   ```

3. Install SWI-Prolog from Homebrew
   ```
   brew install swi-prolog
   ```
   - Ensure the SWI-Prolog executable is in your system PATH

   For other: https://www.swi-prolog.org/download/stable

## Running the Game

### Main Game
To play the game with all three AI strategies:
```
python space_invaders_prolog.py
```

### Strategy Tester
To analyze and test individual strategies with visual feedback:
```
python strategy_tester.py
```

## Controls

### Main Game
- Left/Right Arrow: Move player
- Space: Shoot
- R: Reset game
- Q: Quit game

### Strategy Tester
- Left/Right Arrow: Move player (in manual mode)
- 1-3: Switch between strategies (1: Direct, 2: Predictive, 3: Crossfire Trap)
- A-D: Change player movement pattern (A: Static, B: Left-Right, C: Random, D: Manual)
- R: Reset statistics
- B: Toggle debug mode
- ESC: Quit tester

## Strategy Testing Instructions

The Strategy Tester tool provides a specialized environment for analyzing and comparing the three AI strategies:

1. **Select a Strategy**: Press 1, 2, or 3 to select Direct Targeting, Predictive Targeting, or Crossfire Trap Pattern.
2. **Choose Movement Pattern**: Press A, S, D, or F to select Static, Left-Right Sweep, Random, or Manual movement.
3. **Observe Statistics**: Watch the real-time statistics on hit rates, shots fired, and performance.
4. **Analyze Visualizations**: Each strategy shows different visual indicators:
   - Direct Targeting: Simple vertical lines
   - Predictive Targeting: Direction arrows and predicted positions
   - Crossfire Trap: Color-coded trap zones and targeting assignments
5. **Reset and Compare**: Press R to reset statistics and compare different strategies.

## Prolog AI Implementation

The Prolog implementation is divided into two parts:

1. **Main Game Knowledge Base** (`ai/invader_ai.pl`):
   - Implementation of all three strategies
   - Row-based strategy assignment
   - Player movement tracking and prediction
   - Spatial reasoning for coordinated firing

2. **Testing Knowledge Base** (`ai/strategy_test.pl`):
   - Enhanced versions of strategies for testing
   - Configurable parameters for fine-tuning
   - Debug predicates for visualization
   - Statistical data generation

The CLI-based Prolog bridge handles communication between Python and Prolog via command-line interface, ensuring cross-platform compatibility.

## Future Enhancements

- Additional AI strategies based on different targeting principles
- Machine learning integration for adaptive difficulty
- Enhanced visual effects for strategy visualization
- Multiple levels with progressive strategy complexity
- Player skill tracking to adjust strategy parameters
- Cooperative alien behavior with group formations
- Sound effects responsive to different strategies