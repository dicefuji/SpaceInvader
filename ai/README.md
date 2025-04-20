# Space Invaders Prolog AI

This directory contains the Prolog AI implementation for the Space Invaders game. The AI is responsible for controlling the alien invaders' firing behavior using different strategies.

## Implementation Overview

The Prolog AI system consists of:

1. **Knowledge Base** (`invader_ai.pl`): Contains facts and rules for decision-making
2. **Python-Prolog Bridge** (`prolog_bridge.py`): Handles communication between Python game engine and Prolog

## AI Strategies

The game implements multiple firing strategies that can be selected during gameplay by pressing the number keys 0-5:

### 1. Direct Targeting (Key: 1)
Aliens fire when the player is directly below them (or nearly below). This is the most straightforward targeting approach.

**Implementation**: 
```prolog
should_fire_direct(AlienID) :-
    alien(AlienID, AlienX, AlienY),
    player(PlayerX, _),
    abs(AlienX - PlayerX) < 20,  % Player is directly below (with small margin)
    random(0, 100, R),
    R < 30.  % 30% chance of firing when player is below
```

### 2. Predictive Targeting (Key: 2)
Aliens attempt to predict player movement and fire ahead of the player's position. This strategy is more effective against moving targets.

**Implementation**:
```prolog
should_fire_predictive(AlienID) :-
    alien(AlienID, AlienX, AlienY),
    player(PlayerX, _),
    % Assume player is moving toward center if far from center
    screen_size(Width, _),
    ScreenCenter is Width / 2,
    (PlayerX < ScreenCenter -> PredictedX is PlayerX + 30 ; PredictedX is PlayerX - 30),
    abs(AlienX - PredictedX) < 25,
    random(0, 100, R),
    R < 25.
```

### 3. Random Firing (Key: 3)
Aliens fire randomly with a low probability. This creates unpredictable threats for the player.

**Implementation**:
```prolog
should_fire_random(AlienID) :-
    random(0, 100, R),
    R < 1.  % 1% chance of firing randomly
```

### 4. Coordinated Firing (Key: 4)
Only aliens in the bottom row of each column fire. This concentrates fire from the aliens closest to the player.

**Implementation**:
```prolog
should_fire_coordinated(AlienID) :-
    findall(ID, (alien(ID, _, Y), \+ (alien(_, _, Y2), Y2 > Y)), BottomRow),
    member(AlienID, BottomRow),  % Only bottom row aliens fire
    random(0, 100, R),
    R < 10.
```

### 5. Barrier Avoidance (Key: 5)
Aliens avoid firing when barriers would block their shots, focusing on clear shots to the player.

**Implementation**:
```prolog
should_fire_avoiding_barriers(AlienID) :-
    alien(AlienID, AlienX, AlienY),
    player(PlayerX, _),
    abs(AlienX - PlayerX) < 30,  % Player is below
    % Check if there's no barrier in the way
    \+ (barrier(_, BarrierX, BarrierY), 
        abs(AlienX - BarrierX) < 40,
        AlienY < BarrierY),
    random(0, 100, R),
    R < 20.
```

### Mixed Strategy (Key: 0)
Each alien uses a strategy based on its ID. This creates a diverse mix of firing behaviors.

**Implementation**:
```prolog
strategy_for_alien(AlienID, Strategy) :-
    Strategy is (AlienID mod 5) + 1.
```

## Game State Representation

The Prolog knowledge base maintains facts about the current game state:

- `player(X, Y)`: Position of the player
- `alien(ID, X, Y)`: Position of each alien with its ID
- `barrier(ID, X, Y)`: Position of each barrier segment
- `screen_size(Width, Height)`: Dimensions of the game screen
- `strategy(Type)`: Currently active global strategy (if set)

## Python-Prolog Integration

The `PrologBridge` class handles:
1. Initialization of the Prolog engine
2. Updating the knowledge base with the current game state
3. Querying the Prolog engine for firing decisions
4. Setting and changing strategies during gameplay
5. Providing fallback behavior when Prolog is unavailable 