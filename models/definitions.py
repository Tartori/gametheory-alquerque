#!/usr/bin/python3


class Player:
    USER = 1
    OPP = -1


class FieldValue:
    USER = 1
    OPP = -1
    EMPTY = 0
    POSSIBLE_MOVE = 2


class Games:
    ALQUERQUE = 0
    BAUERNSCHACH = 1


class States:
    CHOOSE_GAME = 0
    CHOOSE_BOARD_SIZE = 1
    CHOOSE_OPP_HUMAN_OR_MACHINE = 2
    CHOOSE_MACHINE_STRATEGY = 3
    CHOOSE_PLAYER_ORDER = 4
    START_GAME = 5
    TAKE_TURN = 6
    CHOOSE_PAWN = 7
    CHOOSE_MOVE = 8
    SWITCH_TURN = 9
    WIN = 10
    BYE = -1


class Commands:
    QUIT_APP = "X"
    CHOOSE_GAME_ALQUERQUE = "A"
    CHOOSE_GAME_BAUERNSCHACH = "B"
    CHOOSE_FIRST_PLAYER_ME = "M"
    CHOOSE_FIRST_PLAYER_OPPONENT = "P"
    CHOOSE_OPP_AS_HUMAN = "H"
    CHOOSE_OPP_AS_MACHINE = "C"
    CHOOSE_MACHINE_STRATEGY_RANDOM = "R"
