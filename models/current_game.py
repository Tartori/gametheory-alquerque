#!/usr/bin/python3


class CurrentGame:
    """
    Part of the application State as shared data.
    Contains data used to configure a new game.
    Contains the actors of the current game.
    Contains the game engine!
    Contains the textual history of moves.
    """
    # Game setup.

    # The size of the square game board.
    board_size: int = 4

    # The chosen Game to play.
    game_choice: int = None

    # The machine strategy to be used
    # if the opponent is a machine.
    machine: int = None

    # The Player that may take the first step.
    player_to_start: int = None

    # Game engine.
    engine = None

    # The actor that is to move now.
    current_actor = None

    # The other actor that cannot move now.
    waiting_actor = None

    # The moves as text.
    history = []
