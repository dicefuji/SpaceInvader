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
strategy_for_row(3, 3).  % Row 3: Coordinated firing

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

% Strategy 3: Coordinated Firing
% Only aliens in bottom row of each column fire
should_fire_coordinated(AlienID) :-
    alien(AlienID, _, AlienY),
    \+ (alien(_, _, Y), Y > AlienY),  % No aliens below this one
    random(0, 100, R),
    R < 10.

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