# Row-Based Strategy Implementation

## Overview

This document outlines the implementation of the row-based strategy system in Space Invaders. Instead of a single global strategy for all aliens, each row of aliens now employs a distinct strategy, providing more diverse and visually distinctive gameplay.

## Key Implementation Components

### 1. Prolog Knowledge Base Changes

The Prolog AI knowledge base (`invader_ai.pl`) was updated to support row-based strategies:

- Added `strategy_for_row/2` predicate mapping row positions to strategies
- Implemented `alien_row/2` to determine an alien's row based on Y-coordinate
- Updated `strategy_for_alien/2` to derive strategy based on row position
- Modified `should_alien_fire/1` to use row-based strategies when no global strategy is set

### 2. PrologBridge Enhancements

The Python-Prolog bridge (`prolog_bridge.py`) was enhanced to support row-based strategies:

- Added `initialize_row_strategies` method to clear global strategies
- Modified `set_strategy` to support toggling between global and row-based behavior
- Added `get_strategy_for_row` helper method

### 3. Visual Strategy Indicators

The PrologAlien class (`test_prolog_integration.py`) was updated to visually indicate strategies:

- Added color mapping with `STRATEGY_COLORS` to differentiate strategies
- Modified alien initialization to set color based on row
- Overrode the `draw` method to use strategy-specific colors

### 4. Fallback AI Behavior

To ensure robust operation even if Prolog initialization fails:

- Added fallback firing methods in `PrologAlien` to match Prolog strategies
- Implemented player position tracking for targeting strategies
- Added barrier awareness for the barrier avoidance strategy
- Ensured the PrologAlienGroup passes necessary state information to aliens

### 5. User Interface Updates

The main game interface (`space_invaders_prolog.py`) was updated:

- Added a strategy legend explaining the color coding
- Removed the global strategy selection keys (1-5)
- Added a clear indication of the row-based strategy mode

## Strategy Implementations

Each strategy is implemented with both Prolog logic and Python fallback:

### Strategy 1: Direct Targeting (Red Aliens)
- Fires when player is directly below (within 20 pixels)
- 30% chance to fire when condition is met
- Prolog: `should_fire_direct/1`
- Python: `should_fire_fallback` case 1

### Strategy 2: Predictive Targeting (Green Aliens)
- Predicts player movement (30 pixels ahead in direction of movement)
- 25% chance to fire when prediction is good
- Prolog: `should_fire_predictive/1`
- Python: `should_fire_fallback` case 2

### Strategy 3: Random Firing (Blue Aliens)
- Simple 1% random chance to fire
- Prolog: `should_fire_random/1`
- Python: `should_fire_fallback` case 3

### Strategy 4: Coordinated Firing (Yellow Aliens)
- Only bottom-most aliens in each column fire
- 10% chance when eligible
- Prolog: `should_fire_coordinated/1`
- Python: `should_fire_fallback` case 4

### Strategy 5: Barrier Avoidance (Purple Aliens)
- Fires only when no barrier is in the way
- 20% chance when path is clear
- Prolog: `should_fire_avoiding_barriers/1`
- Python: `should_fire_fallback` case 5

## Testing Tools

A specialized testing script was created (`test_row_strategies.py`):

- Row isolation for testing individual strategies
- Real-time firing visualization (heatmap)
- Statistical tracking of strategy effectiveness
- Auto-test mode for consistent evaluation
- Debug visualization showing firing decisions

## Visual System Benefits

The row-based color coding provides several gameplay benefits:

1. **Enhanced Readability**: Players can easily identify which aliens use which strategy
2. **Visual Progression**: As rows are destroyed, the strategic challenges change
3. **Learning Aid**: Players can learn how each strategy works through visual association
4. **Aesthetic Variation**: More colorful and visually interesting enemy formations

## Future Enhancements

Potential improvements to the row-based strategy system:

- Add level-specific strategy layouts (different rows could use different strategies per level)
- Implement adaptive strategies that change based on player performance
- Create complex formations with mixed strategies within rows
- Allow individual aliens to change strategies during gameplay

## Implementation Challenges

Several challenges were addressed during implementation:

1. **Prolog Integration**: Ensured fallback behavior when Prolog initialization fails
2. **Strategy Coordination**: Balanced the effectiveness of different strategies
3. **Visual Clarity**: Ensured color coding was distinct and meaningful
4. **Performance**: Maintained good performance with more complex alien behavior
5. **Backwards Compatibility**: Kept support for global strategy mode

## Conclusion

The row-based strategy system significantly enhances the game's tactical depth and visual appeal. By assigning distinct strategies to each row and color-coding the aliens, players can more easily understand and adapt to the varied attack patterns. The fallback implementation ensures these behaviors work even without Prolog, though the Prolog version provides a more elegant logical representation of the strategies. 