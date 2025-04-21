/*
Space Invaders AI Strategy Test File
*/

% Dynamic facts for game state
:- dynamic player/2.         % player(X, Y)
:- dynamic alien/3.          % alien(ID, X, Y)
:- dynamic bullet/3.         % bullet(Owner, X, Y)
:- dynamic barrier/3.        % barrier(ID, X, Y)
:- dynamic screen_size/2.    % screen_size(Width, Height)
:- dynamic strategy/1.       % Global strategy selector (what well use for tests)
:- dynamic last_player_x/1.  % Track the last player position
:- dynamic player_direction/1. % Track player movement direction

% Strategy 1: Direct Targeting
% Aliens fire when the player is directly below them
should_fire_direct(AlienID) :-
    alien(AlienID, AlienX, _),
    player(PlayerX, _),
    abs(AlienX - PlayerX) < 20,  % Player is directly below (with small margin)
    random(0, 100, R),
    R < 80.  % Increased from 30% to 80% chance of firing when player is below

% Strategy 2: Improved Predictive Targeting
% Aliens try to predict where the player will be based on movement direction
should_fire_predictive(AlienID) :-
    alien(AlienID, AlienX, _),
    player(PlayerX, _),
    
    % Determine player movement direction based on last position
    (last_player_x(LastX) -> 
        (PlayerX > LastX -> Direction = 1 ; 
         PlayerX < LastX -> Direction = -1 ; 
         Direction = 0),
        retract(last_player_x(_)),
        assert(last_player_x(PlayerX)),
        % Only update direction if we detect movement
        (Direction \= 0 -> 
            (retract(player_direction(_)) -> true ; true),
            assert(player_direction(Direction))
            ; true)
        ;
        % Initialize if not yet set
        assert(last_player_x(PlayerX)),
        assert(player_direction(0))
    ),
    
    % Use the stored direction for prediction
    player_direction(StoredDirection),
    
    % Calculate predicted position with larger offset (100 pixels)
    % If no movement detected, predict based on position relative to center
    (StoredDirection \= 0 -> 
        PredictedX is PlayerX + (StoredDirection * 150)
        ;
        % Fallback if no direction detected
        screen_size(Width, _),
        ScreenCenter is Width / 2,
        (PlayerX < ScreenCenter -> PredictedX is PlayerX + 150 ; PredictedX is PlayerX - 150)
    ),
    
    % Ensure prediction is within screen bounds
    screen_size(Width, _),
    BoundedPredictedX is max(50, min(Width - 50, PredictedX)),
    
    % Alien aims at the predicted position
    abs(AlienX - BoundedPredictedX) < 40,  % Widened targeting area
    
    % Debug output
    % write('Player at '), write(PlayerX), 
    % write(', Direction: '), write(StoredDirection),
    % write(', Predicted: '), write(BoundedPredictedX), nl,
    
    random(0, 100, R),
    R < 70.  % Slightly reduced to balance the better targeting

% Strategy 3: Crossfire Trap Pattern
% Bottom row aliens coordinate to create a trap zone around the player
should_fire_coordinated(AlienID) :-
    alien(AlienID, AlienX, AlienY),
    player(PlayerX, _),
    
    % Only bottom-row aliens participate in coordinated firing
    \+ (alien(_, _, Y), Y > AlienY),  % No aliens below this one
    
    % Get screen dimensions
    screen_size(Width, _),
    
    % Determine player movement direction
    (last_player_x(LastX) -> 
        (PlayerX > LastX -> Direction = 1 ; 
         PlayerX < LastX -> Direction = -1 ; 
         Direction = 0),
        true  % Just use for calculation, don't update here
        ;
        Direction = 0,  % Default if no previous position
        assert(last_player_x(PlayerX))
    ),
    
    % Define the trap zone positions
    % Central position is the player's current position
    CenterPos = PlayerX,
    % Left and right trap positions are offset from player
    % Wider on the direction of movement to catch the player
    LeftOffset is 60 + (Direction * -20),  % Wider if moving left
    RightOffset is 60 + (Direction * 20),  % Wider if moving right
    LeftPos is PlayerX - LeftOffset,
    RightPos is PlayerX + RightOffset,
    
    % Ensure trap positions are within screen bounds
    BoundedLeftPos is max(50, LeftPos),
    BoundedRightPos is min(Width - 50, RightPos),
    
    % Assign aliens to different positions in the trap
    % Based on their position relative to the player
    (
        % Aliens directly above player target the player
        (abs(AlienX - PlayerX) < 100, TargetPos = CenterPos)
        ;
        % Aliens to the left set the left trap
        (AlienX < PlayerX, TargetPos = BoundedLeftPos)
        ;
        % Aliens to the right set the right trap
        (AlienX > PlayerX, TargetPos = BoundedRightPos)
    ),
    
    % Only fire if the alien is in a reasonable position to hit its target
    abs(AlienX - TargetPos) < 80,  % Wider targeting zone for the trap pattern
    
    % Add timing element based on position to create a coordinated trap
    % Aliens closer to the center fire slightly earlier
    DistanceToPlayer = abs(AlienX - PlayerX),
    TimingFactor is DistanceToPlayer mod 3,
    random(0, 3, R1),
    R1 =:= TimingFactor,  % Stagger timing for trap effect
    
    % Firing probability
    random(0, 100, R2),
    R2 < 70.  % High probability for testing

% Main firing decision predicate - for testing well always use the global strategy
should_alien_fire(AlienID) :-
    strategy(Strategy),  % Get the global strategy were testing
    alien(AlienID, _, _),  % Alien must exist
    should_alien_fire_with_strategy(AlienID, Strategy).

% Apply a specific strategy for firing decision
should_alien_fire_with_strategy(AlienID, 1) :-
    should_fire_direct(AlienID).
should_alien_fire_with_strategy(AlienID, 2) :-
    should_fire_predictive(AlienID).
should_alien_fire_with_strategy(AlienID, 3) :-
    should_fire_coordinated(AlienID).

% Helper predicates
abs(X, X) :- X >= 0, !.
abs(X, Y) :- Y is -X.

% Movement predicates (simplified)
can_move_left(AlienID) :-
    alien(AlienID, X, _),
    X > 10.  % Basic boundary check

can_move_right(AlienID) :-
    alien(AlienID, X, _),
    screen_size(Width, _),
    X < Width - 30.  % Basic boundary check

% Action decision for an alien
next_action(AlienID, fire) :-
    should_alien_fire(AlienID), !.

next_action(AlienID, left) :-
    can_move_left(AlienID),
    random(0, 2, 0), !.

next_action(AlienID, right) :-
    can_move_right(AlienID),
    random(0, 2, 1), !.

next_action(_, stay). 