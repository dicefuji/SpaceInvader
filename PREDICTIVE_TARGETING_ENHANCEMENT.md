# Enhanced Predictive Targeting AI

## Overview

The Space Invaders game now features an improved predictive targeting system for the aliens. This enhancement makes the game more challenging and dynamic by having aliens intelligently predict where the player will be based on their movement patterns.

## How It Works

The enhanced predictive targeting strategy:

1. **Tracks Player Movement Direction**
   - Monitors how the player is moving (left or right)
   - Remembers the direction between frames
   - Adapts predictions when player changes direction

2. **Looks Further Ahead**
   - Predicts player position 150 pixels ahead in their current movement direction
   - Creates a more challenging experience that rewards anticipation and strategy
   - Forces players to think about their movement patterns

3. **Has Fallback Intelligence**
   - If player isn't moving, predicts based on screen position
   - Ensures aliens still make smart targeting decisions even with stationary players

4. **Features Improved Targeting Range**
   - Wider targeting area (40 pixels vs. the original 25)
   - More realistic "aim" that isn't too precise or too loose

## Alien Strategy Assignment

The aliens use different strategies based on their row:

- **Top Row (Row 1)**: Direct Targeting - Fires directly at player's current position
- **Middle Row (Row 2)**: Predictive Targeting - Uses the enhanced prediction system
- **Bottom Row (Row 3)**: Coordinated Firing - Only bottom-most aliens in each column fire

## Testing Results

Testing with the new strategy showed:
- Higher hit rates when players move in predictable patterns
- More challenging gameplay that rewards erratic movement
- Better visual distinction between the different firing strategies

## Implementation Notes

The predictive targeting is handled by tracking player position between game frames in Prolog:

```prolog
% Calculate predicted position with directional awareness
(StoredDirection \= 0 -> 
    PredictedX is PlayerX + (StoredDirection * 150)
    ;
    % Fallback if no direction detected
    screen_size(Width, _),
    ScreenCenter is Width / 2,
    (PlayerX < ScreenCenter -> PredictedX is PlayerX + 150 ; PredictedX is PlayerX - 150)
)
```

This represents a significant improvement over the original implementation, which only looked 30 pixels ahead and always assumed movement toward center without tracking actual direction. 