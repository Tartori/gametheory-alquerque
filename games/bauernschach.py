#!/usr/bin/python3

from copy import deepcopy

from models import Player, FieldValue
from games.board_game import BoardGame


class Bauernschach(BoardGame):
    """
    The game engine to play Bauernschach.
    """

    def __init__(self, player, size=8):
        super().__init__(player, size)

    def _set_start_state(self):
        """
        Initializes the board.
        Void.
        """
        if(self._size < self._MINIMUM_BOARD_SIZE):
            self._size = self._MINIMUM_BOARD_SIZE
        # https://stackoverflow.com/questions/9459337/assign-value-to-an-individual-cell-in-a-two-dimensional-python-array
        self._board = [
            [0 for col in range(self._size)] for row in range(self._size)]
        self._board[1] = [Player.OPP for col in range(self._size)]
        self._board[self._size - 2] = \
            [Player.USER for col in range(self._size)]

    def _find_all_moves(self):
        """
        For each pawn of the current player, finds all possible moves.
        return: void. (sets field)
        """
        self._possible_moves = {}
        for r in range(0, self._size):
            for c in range(0, self._size):
                movesForPawn = []

                isFinalRow = r == 0 or r == len(self._board) - 1
                anyPlayer = [Player.USER, Player.OPP]
                isOccupied = self._board[r][c] in anyPlayer
                if (isFinalRow and isOccupied):
                    raise Exception("Game is finished.")

                pawn = (r, c)

                # check if any pawn.
                if not self._field_occupied_by_current_player(pawn):
                    continue

                moveFront = (self._get_advance(r), c)
                moveFrontTwo = (self._get_advance(self._get_advance(r)), c)
                moveFrontLeft = (self._get_advance(r), self._get_left(c))
                moveFrontRight = (self._get_advance(r), self._get_right(c))
                moveLeftEnPassant = (r, self._get_left(c))
                moveRightEnPassant = (r, self._get_right(c))

                if self._can_move_front(pawn, moveFront):
                    movesForPawn.append(moveFront)
                if self._can_move_front_two(pawn, moveFrontTwo):
                    movesForPawn.append(moveFrontTwo)
                if self._can_move_front_side_with_kill(pawn, moveFrontLeft):
                    movesForPawn.append(moveFrontLeft)
                if self._can_move_front_side_with_kill(pawn, moveFrontRight):
                    movesForPawn.append(moveFrontRight)
                if self._can_move_en_passant(pawn, moveLeftEnPassant):
                    movesForPawn.append(moveLeftEnPassant)
                if self._can_move_en_passant(pawn, moveRightEnPassant):
                    movesForPawn.append(moveRightEnPassant)

                if len(movesForPawn) > 0:
                    self._possible_moves[pawn] = movesForPawn
        return

    def _possible_move(self, pawn, move):
        """
        Checks if a pawn can move to a certain field.

        pawn: (i, j) where i is rowindex and j is colindex referencing
        the field of a pawn.

        move: (i, j) where i is rowindex and j is colindex referencing
        the field where the pawn wants to move to.

        return: bool.
        """
        canFront = self._can_move_front(pawn, move)
        canFrontTwo = self._can_move_front_two(pawn, move)
        canSide = self._can_move_front_side_with_kill(pawn, move)
        canEnPassant = self._can_move_en_passant(pawn, move)
        return canFront or canFrontTwo or canSide or canEnPassant

    def _can_move_front(self, pawn, move):
        """
        Checks if a pawn can move to the neighbouring field straight ahead on
        the bord.
        pawn: (i, j) where i is rowindex and j is colindex referencing the
        field of a pawn.
        move: (i, j) where i is rowindex and j is colindex referencing the
        field where the pawn wants to move to.
        return: bool.
        """
        return self._field_on_bord(move) and not self._field_occupied(move)

    def _can_move_front_two(self, pawn, move):
        """
        Checks if a pawn can jump two field ahead on the bord. (only if has
        not yet moved, and both fields ahead unoccupied.)
        pawn: (i, j) where i is rowindex and j is colindex referencing the
        field of a pawn.
        move: (i, j) where i is rowindex and j is colindex referencing the
        field where the pawn wants to move to.
        return: bool.
        """
        isFirstMovementForPiece = False
        if self._current_player == Player.USER:
            isFirstMovementForPiece = pawn[0] == len(self._board) - 2
        if self._current_player == Player.OPP:
            isFirstMovementForPiece = pawn[0] == 1
        if not isFirstMovementForPiece:
            return False
        if not self._field_on_bord(move):
            return False
        if self._field_occupied((self._get_back(move[0]), move[1])):
            return False
        if self._field_occupied(move):
            return False
        return True

    def _can_move_front_side_with_kill(self, pawn, move):
        """
        Checks if a pawn can move to the field diagonally left/right ahead by
        killing an opponent pawn.

        pawn: (i, j) where i is rowindex and j is colindex referencing the
        field of a pawn.

        move: (i, j) where i is rowindex and j is colindex referencing the
        field where the pawn wants to move to.

        return: bool.
        """
        if not self._field_on_bord(move):
            return False
        if not self._field_occupiedByOpponent(move):
            return False
        return True

    def _can_move_en_passant(self, pawn, move):
        """
        Checks if en-passant move to the left is possible.
        This is only possible if A has moved a pawn two cells from initial
        position in A's latest turn
        and if B has a pawn to the right/left of A's moved pawn.

        pawn: (i, j) where i is rowindex and j is colindex referencing the
        field of a pawn.

        move: (i, j) where i is rowindex and j is colindex referencing the
        field where the pawn wants to move to.

        return: bool.
        """
        if not self._field_on_bord(move):
            return False
        if not self._field_occupiedByOpponent(move):
            return False
        if not len(self.moveHistory) > 0:
            return False
        if not self.moveHistory[-1][1] == move:
            return False
        deltaOppPawnMove = self.moveHistory[-1][1][0] - \
            self.moveHistory[-1][0][0]
        if not abs(deltaOppPawnMove) == 2:
            return False
        return True

    def _check_for_winner(self):
        """
        Checks if the current player has just won the game.
        Must assign the Player to self._winner.
        """
        userWins = Player.USER in self._board[0]
        oppWins = Player.OPP in self._board[self._size - 1]
        if userWins:
            self._winner = Player.USER
        elif oppWins:
            self._winner = Player.OPP
