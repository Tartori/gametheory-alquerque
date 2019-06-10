#!/usr/bin/python3
from copy import deepcopy
from models import Player, FieldValue


class BoardGame:
    """
    The base class for the board games.
    NOT REALLY IMPLEMENTED.
    """

    # The minimum width and height of the board.
    _MINIMUM_BOARD_SIZE = 4

    # The width and height of the board.
    _size = 0

    # The current player, i.e. Player.USER or Player.OPP
    _current_player = 0

    # The board, i.e. the collection of fields.
    _board = []

    # All moves possible currently.
    _possible_moves = {}

    # The player that has won.
    _winner = None

    gamestateHistory = []
    moveHistory = []

    def __init__(self, player, size):
        self._size = size
        self._current_player = player
        self._set_start_state()
        self._find_all_moves()

    def to_next_turn(self):
        """
        Switches the player and prepares him for playing.
        """
        self._current_player *= -1
        self._find_all_moves()

    def get_bord(self):
        """Returns the bord as an array."""
        return self._board

    def get_bord_with_moves(self, pawn):
        bordWithMoves = deepcopy(self._board)
        movesForPawn = self.get_moves_for_pawn(pawn)
        for m in movesForPawn:
            bordWithMoves[m[0]][m[1]] = FieldValue.POSSIBLE_MOVE
        return bordWithMoves

    def get_movable_pawns(self):
        return self._possible_moves.keys()

    def get_moves_for_pawn(self, pawn):
        return self._possible_moves.get(pawn)

    def do_move(self, pawn, move):
        """
        Updates the board by performing the move with the pawn.
        Saves the previous board and the move in the respective history.

        pawn: (i, j) where i is rowindex and j is colindex referencing
        the field of a pawn.

        move: (i, j) where i is rowindex and j is colindex referencing
        the field where the pawn wants to move to.

        return: void.
        """
        self.gamestateHistory.append(deepcopy(self._board))
        self.moveHistory.append((deepcopy(pawn), deepcopy(move)))
        self._board[pawn[0]][pawn[1]] = 0
        self._board[move[0]][move[1]] = self._current_player
        self._check_for_winner()

    def undo_move(self, mv):
        raise NotImplementedError("You should have implemented this")

    def is_terminal(self):
        """
        Checks if there has been a winner found.
        """
        return self._winner is not None

    def _check_for_winner(self):
        """
        Checks if the current player has just won the game.
        Must assign the Player to self._winner.
        """
        raise NotImplementedError("Override in child class.")

    def get_move_history(self):
        return self.moveHistory

    def get_state_history(self):
        return self.gamestateHistory

    def get_winner(self):
        return self._winner

    def _set_start_state(self):
        """
        Initializes the board.
        Void.
        """
        raise NotImplementedError("Override in child class.")

    def _find_all_moves(self):
        """
        For each pawn of the current player, finds all possible moves.
        return: void. (sets field)
        """
        raise NotImplementedError("Override in child class.")

    def _field_occupied(self, field):
        return self._board[field[0]][field[1]] in [-1, 1]

    def _field_occupied_by_current_player(self, field):
        return self._board[field[0]][field[1]] == self._current_player

    def _field_occupiedByOpponent(self, field):
        """
        Checks if a field on the board is occupied by a pawn owned by the
        opposing player.
        field: (i, j) where i is rowindex and j is colindex.
        return: bool.
        """
        if self._current_player == Player.USER:
            opponent = Player.OPP
        elif self._current_player == Player.OPP:
            opponent = Player.USER
        return self._board[field[0]][field[1]] == opponent

    def _field_on_bord(self, field):
        """
        Checks if the field is in the boundaries of the bord.
        field: (i, j) where i is rowindex and j is colindex.
        return: bool.
        """
        size = len(self._board)
        return field[0] in range(0, size) and field[1] in range(0, size)

    def _can_be_moved(self, pawn):
        return pawn in self.get_movable_pawns()

    def _possible_move(self, pawn, move):
        """
        Checks if a pawn can move to a certain field.

        pawn: (i, j) where i is rowindex and j is colindex referencing
        the field of a pawn.

        move: (i, j) where i is rowindex and j is colindex referencing
        the field where the pawn wants to move to.

        return: bool.
        """
        raise NotImplementedError("Override in child class.")

    def has_next_move(self):
        """
        Checks if the current player can make any move.
        return: bool.
        """
        return len(self._possible_moves) > 0

    def peek(self):
        """
        Creates a copy of the current game engine and moves to the next turn.
        """
        gameCopy = deepcopy(self)
        gameCopy.to_next_turn()
        return gameCopy

    # def _get_next_move(self):
    #    raise NotImplementedError("You should have implemented this")

    def _get_left(self, rowIndex, numberOfFields=1):
        return rowIndex + self._current_player * -1

    def _get_right(self, rowIndex, numberOfFields=1):
        return rowIndex + self._current_player

    def _get_advance(self, colIndex, numberOfFields=1):
        return colIndex + self._current_player * -1

    def _get_back(self, colIndex, numberOfFields=1):
        return colIndex + self._current_player

    def _left(self, fieldTuple, numberOfFields=1):
        r = fieldTuple[0] + self._current_player * -1 * numberOfFields
        c = fieldTuple[1]
        return (r, c)

    def _right(self, fieldTuple, numberOfFields=1):
        r = fieldTuple[0] + self._current_player * numberOfFields
        c = fieldTuple[1]
        return (r, c)

    def _front(self, fieldTuple, numberOfFields=1):
        r = fieldTuple[0]
        c = fieldTuple[1] + self._current_player * -1 * numberOfFields
        return (r, c)

    def _back(self, fieldTuple, numberOfFields=1):
        r = fieldTuple[0]
        c = fieldTuple[1] + self._current_player * numberOfFields
        return (r, c)
