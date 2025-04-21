# Crossfire Trap Pattern Strategy

## Overview

The Crossfire Trap Pattern is an advanced alien firing strategy implemented in the Space Invaders game. It creates a coordinated firing pattern where bottom-row aliens work together to form a "trap zone" around the player, making it significantly harder to dodge incoming bullets.

## How It Works

The Crossfire Trap Pattern operates on these key principles:

1. **Multi-Target Coverage**: Instead of firing only at the player's current position, aliens target three strategic locations:
   - The player's current position (center trap)
   - An area to the player's left (left trap)
   - An area to the player's right (right trap)

2. **Dynamic Trap Sizing**: The trap zone adapts to player movement, becoming larger in the direction the player is moving:
   - When moving right, the right trap zone expands
   - When moving left, the left trap zone expands
   - This creates a "closing door" effect that's harder to escape from

3. **Intelligent Target Assignment**: Each alien chooses the closest of the three trap positions to target based on its position, ensuring optimal coverage:
   ```prolog
   % Calculate distance to each trap point 
   DistToCenter is abs(AlienX - CenterPos),
   DistToLeft is abs(AlienX - BoundedLeftPos),
   DistToRight is abs(AlienX - BoundedRightPos),
   
   % Choose the closest target
   (DistToCenter =< DistToLeft, DistToCenter =< DistToRight -> TargetPos = CenterPos;
    DistToLeft =< DistToRight -> TargetPos = BoundedLeftPos;
    TargetPos = BoundedRightPos)
   ```

4. **Coordinated Timing**: A simple but effective timing mechanism staggers alien firing based on their ID, creating a wave-like pattern:
   ```prolog
   TimingFactor is AlienID mod 3,
   random(0, 3, R1),
   R1 =:= TimingFactor
   ```

## Computational Efficiency

The Crossfire Trap Pattern is designed to be lightweight for game performance:

1. **Minimal State Tracking**: Only tracks the player's last position and movement direction
2. **Simple Calculations**: Uses basic math operations (addition, subtraction, modulo)
3. **Efficient Target Selection**: Direct comparison of distances without sorting or complex algorithms
4. **Bounded Checks**: Ensures all calculated positions stay within screen boundaries
5. **Maintains Game Balance**: Keeps the original 10% base chance of firing

## Game Balance Considerations

To ensure the strategy remains challenging but fair:

- Only bottom-row aliens participate in the coordinated firing pattern
- Aliens only fire if they are reasonably positioned to hit their target (within 60px)
- The base chance of firing remains at 10%, the same as the original game
- Timing factors ensure not all aliens fire simultaneously, giving players a chance to react

## Strategic Advantage

The Crossfire Trap Pattern creates a more intelligent and challenging enemy behavior:

1. **Harder to Dodge**: The trap zones make simple left-right dodging less effective
2. **Punishes Predictable Movement**: The expanding trap in the direction of movement makes constant movement in one direction dangerous
3. **Natural-Looking AI**: The staggered firing creates a more organic, coordinated look to alien attacks
4. **No Dead Zones**: With three target areas and intelligent target assignment, there are fewer safe spots for the player

## Implementation Details

The strategy is implemented in the third row of aliens in the game's AI system, complementing the Direct Targeting (row 1) and Predictive Targeting (row 2) strategies used by other rows.

```prolog
strategy_for_row(1, 1).  % Row 1: Direct targeting
strategy_for_row(2, 2).  % Row 2: Predictive targeting  
strategy_for_row(3, 3).  % Row 3: Crossfire Trap Pattern
``` 