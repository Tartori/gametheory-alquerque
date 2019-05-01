#!/usr/bin/python3

PLAYER_USER = 1
PLAYER_OPP = -1
EMPTYCELL = 0
POSSIBLE_MOVE = 2

class ScreenParameters:
    """
    Pass parameters from game loop to screen rendering:
    - bord: 2D array for rows and cells/cols.
    - moveHistory: array of 2-tuples of 2-tuples [((fromRow, fromCol), (toRow, toCol)), ...].
    - currentPlayer: int constant identifying the player.
    - feedback: feedback from executing the previous user input.
    - question: instruction for the user.
    - options: dictionary of possible cli-inputs and a matching description.
    """

    def __init__(self, bord, moveHistory, currentPlayer, question, options, feedback):
        self.bord = bord
        self.moveHistory = moveHistory
        self.currentPlayer = currentPlayer
        self.question = question
        self.options = options
        self.feedback = feedback
