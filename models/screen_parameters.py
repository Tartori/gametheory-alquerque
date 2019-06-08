#!/usr/bin/python3

# TODO: could be refactored and fused with the State. Maybe?


class ScreenParameters:
    """
    Pass parameters from game loop to screen rendering:
    - bord: 2D array for rows and cells/cols.
    - moveHistory: array of 2-tuples of 2-tuples
      [((fromRow, fromCol), (toRow, toCol)), ...].
    - currentPlayer: int constant identifying the player.
    - feedback: feedback from executing the previous user input.
    - question: instruction for the user.
    - options: dictionary of possible cli-inputs and a matching description.
    """

    game = None
    board = []
    moveHistory = []
    player = ""
    feedback = ""
    instruction = ""
    options = {}
