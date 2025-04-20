/*
Space Invaders AI in Prolog - Simplified Version
*/

% Basic facts for game state
:- dynamic(player/2).         % player(X, Y)
:- dynamic(alien/3).          % alien(ID, X, Y)
:- dynamic(barrier/3).        % barrier(ID, X, Y)
:- dynamic(screen_size/2).    % screen_size(Width, Height)
:- dynamic(strategy/1).       % Global strategy selector

% Simple row-based strategy system
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
    Diff is abs(AlienX - PlayerX),
    Diff < 20.  % Player is directly below (with small margin)

% Strategy 2: Predictive Targeting
% Aliens try to predict where the player will be
should_fire_predictive(AlienID) :-
    alien(AlienID, AlienX, _),
    player(PlayerX, _),
    % Simple prediction logic
    PredictedX is PlayerX + 30,
    Diff is abs(AlienX - PredictedX),
    Diff < 25.

% Strategy 3: Coordinated Firing
% Bottom row aliens have priority
should_fire_coordinated(AlienID) :-
    alien(AlienID, _, AlienY),
    % Simple version to prevent errors
    AlienY > 200.  % If it's in a lower position

% Determine which strategy to use for an alien
strategy_for_alien(AlienID, Strategy) :-
    alien(AlienID, _, Y),
    alien_row(Y, Row),
    strategy_for_row(Row, Strategy).

% Main firing decision predicate with global strategy override
should_alien_fire(AlienID) :-
    % If global strategy is set, use it
    strategy(Strategy),
    should_alien_fire_with_strategy(AlienID, Strategy).

% Main firing decision predicate with row-based strategy
should_alien_fire(AlienID) :-
    % If no global strategy, use row-based
    \+ strategy(_),
    alien(AlienID, _, _),
    strategy_for_alien(AlienID, Strategy),
    should_alien_fire_with_strategy(AlienID, Strategy).

% Apply specific strategies
should_alien_fire_with_strategy(AlienID, 1) :-
    should_fire_direct(AlienID).
should_alien_fire_with_strategy(AlienID, 2) :-
    should_fire_predictive(AlienID).
should_alien_fire_with_strategy(AlienID, 3) :-
    should_fire_coordinated(AlienID).

% Simplified movement predicates
can_move_left(AlienID) :-
    alien(AlienID, X, _),
    X > 10.

can_move_right(AlienID) :-
    alien(AlienID, X, _),
    screen_size(Width, _),
    X < Width - 30.

% Action decision for an alien
next_action(AlienID, fire) :-
    should_alien_fire(AlienID).
next_action(AlienID, left) :-
    can_move_left(AlienID).
next_action(AlienID, right) :-
    can_move_right(AlienID).
next_action(_, stay). 