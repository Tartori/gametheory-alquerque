#!/usr/bin/python3


class States:
    """
    Do not confuse with the State as in the shared data
    amongst the controllers.
    Represents the current or next activity.
    Used for user interaction and app flow.
    """
    CHOOSE_GAME = 0
    CHOOSE_BOARD_SIZE = 1
    CHOOSE_OPP = 2
    CHOOSE_MACHINE_STRATEGY = 3
    CHOOSE_PLAYER_ORDER = 4
    START_GAME = 5
    TAKE_TURN = 6
    CHOOSE_PAWN = 7
    CHOOSE_MOVE = 8
    SWITCH_TURN = 9
    WIN = 10
    BYE = -1
    CHOOSE_STRATEGIC = 11
    END_TURN = 12
