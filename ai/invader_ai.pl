/*
Space Invaders AI in Prolog
*/

% Dynamic facts for game state
:- dynamic player/2.         % player(X, Y)
:- dynamic alien/3.          % alien(ID, X, Y)
:- dynamic bullet/3.         % bullet(Owner, X, Y)
:- dynamic barrier/3.        % barrier(ID, X, Y)
:- dynamic screen_size/2.    % screen_size(Width, Height)
:- dynamic strategy/1.       % Global strategy selector (for backward compatibility)
:- dynamic last_player_x/1.  % Track the last player position
:- dynamic player_direction/1. % Track player movement direction

% Row-based strategy system
% Each row uses a specific strategy based on its position
strategy_for_row(1, 1).  % Row 1: Direct targeting
strategy_for_row(2, 2).  % Row 2: Predictive targeting  
strategy_for_row(3, 3).  % Row 3: Crossfire Trap Pattern

% Helper predicate to determine row number based on y-coordinate
alien_row(Y, 1) :- Y =< 150, !.
alien_row(Y, 2) :- Y =< 250, !.
alien_row(_, 3).

% Strategy 1: Direct Targeting
% Aliens fire when the player is directly below them
should_fire_direct(AlienID) :-
    alien(AlienID, AlienX, _),
    player(PlayerX, _),
    abs(AlienX - PlayerX) < 20,  % Player is directly below (with small margin)
    random(0, 100, R),
    R < 30.  % 30% chance of firing when player is below

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
    
    % Calculate predicted position with larger offset (150 pixels)
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
    
    random(0, 100, R),
    R < 25.  % Keep original 25% chance to avoid making it too difficult

% Strategy 3: Crossfire Trap Pattern
% Bottom row aliens coordinate to create a trap zone around the player
should_fire_coordinated(AlienID) :-
    alien(AlienID, AlienX, AlienY),
    player(PlayerX, _),
    
    % Only bottom-row aliens participate in coordinated firing
    \+ (alien(_, _, Y), Y > AlienY),  % No aliens below this one
    
    % Track player movement direction for smarter prediction
    (last_player_x(LastX) -> 
        (PlayerX > LastX + 2 -> Direction = 1 ; 
         PlayerX < LastX - 2 -> Direction = -1 ; 
         Direction = 0),
        retract(last_player_x(_)),
        assert(last_player_x(PlayerX))
        ;
        Direction = 0,  % Default if no previous position
        assert(last_player_x(PlayerX))
    ),
    
    % Define the trap zone positions (computationally efficient)
    % Center position is always the players current position
    CenterPos = PlayerX,
    
    % Left and right trap positions with variable offset based on movement
    % More aggressive trap in the direction the player is moving
    LeftOffset is 50 + (Direction * -15),  % Wider if moving left
    RightOffset is 50 + (Direction * 15),  % Wider if moving right
    LeftPos is PlayerX - LeftOffset,
    RightPos is PlayerX + RightOffset,
    
    % Ensure trap positions are within screen bounds
    screen_size(Width, _),
    BoundedLeftPos is max(40, LeftPos),
    BoundedRightPos is min(Width - 40, RightPos),
    
    % Calculate distance from alien to each trap point to determine best target
    DistToCenter is abs(AlienX - CenterPos),
    DistToLeft is abs(AlienX - BoundedLeftPos),
    DistToRight is abs(AlienX - BoundedRightPos),
    
    % Assign target based on position - choose the closest target point
    (DistToCenter =< DistToLeft, DistToCenter =< DistToRight -> TargetPos = CenterPos;
     DistToLeft =< DistToRight -> TargetPos = BoundedLeftPos;
     TargetPos = BoundedRightPos),
    
    % Only fire if alien is reasonably positioned to hit the target
    abs(AlienX - TargetPos) < 60,
    
    % Add timing element for coordinated firing (computationally simple)
    % Use alien ID modulo 3 as a timing factor to create a wave-like pattern
    TimingFactor is AlienID mod 3,
    random(0, 3, R1),
    R1 =:= TimingFactor,  % Stagger timing based on alien ID
    
    % Base chance is still 10% to maintain game balance
    random(0, 100, R2),
    R2 < 90.

% Determine which strategy to use for an alien
% Now uses row-based strategy assignment
strategy_for_alien(AlienID, Strategy) :-
    alien(AlienID, _, Y),
    alien_row(Y, Row),
    strategy_for_row(Row, Strategy).

% Main firing decision predicate
should_alien_fire(AlienID) :-
    strategy(Strategy),  % If global strategy is set (backward compatibility)
    should_alien_fire_with_strategy(AlienID, Strategy), !.

should_alien_fire(AlienID) :-
    \+ strategy(_),        % No global strategy is set
    alien(AlienID, _, _),  % Alien must exist
    strategy_for_alien(AlienID, Strategy),  % Use row-based strategy
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