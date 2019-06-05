#!/usr/bin/python3

from definitions import Player, FieldValue
from copy import deepcopy


class BoardGame:
    def get_bord(self):
        pass

    def get_move_history(self):
        pass

    def get_movable_pawns(self):
        pass

    def get_moves_for_pawn(self, pawnField):
        pass

    def get_bord_with_moves(self, pawnField):
        pass

    def do_move(self, pawn, move):
        pass

    def is_terminal(self):
        pass

    def to_next_turn(self):
        pass

    def player_1_to_win(self):
        pass

    currentPlayer = None


class Bauernschach(BoardGame):

    gamestate = []
    gamestateHistory = []
    moveHistory = []
    currentPlayer = Player.USER
    currentlyPossibleMoves = []

    def __init__(self, player, size=8):
        self.size = size
        self.moveHistory = []
        self.gamestateHistory = []
        self._set_start_state()
        self.currentPlayer = player
        self._find_all_moves()

    def to_next_turn(self):
        self.currentPlayer *= -1
        self._find_all_moves()

    def _set_start_state(self):
        """Initializes the gamestate. Void."""
        if(self.size < 4):
            self.size = 4
        # https://stackoverflow.com/questions/9459337/assign-value-to-an-individual-cell-in-a-two-dimensional-python-array
        self.gamestate = [
            [0 for col in range(self.size)] for row in range(self.size)]
        self.gamestate[1] = [Player.OPP for col in range(self.size)]
        self.gamestate[self.size-2] = [Player.USER for col in range(self.size)]

    def get_bord(self):
        """Returns the bord as an array."""
        return self.gamestate

    def get_bord_with_moves(self, pawn):
        bordWithMoves = deepcopy(self.gamestate)
        movesForPawn = self.get_moves_for_pawn(pawn)
        for m in movesForPawn:
            bordWithMoves[m[0]][m[1]] = FieldValue.POSSIBLE_MOVE
        return bordWithMoves

    def _find_all_moves(self):
        """
        For each pawn of the current player, finds all possible moves.
        return: void. (sets field)
        """
        self.currentlyPossibleMoves = {}
        for r in range(0, self.size):
            for c in range(0, self.size):
                movesForPawn = []

                isFinalRow = r == 0 or r == len(self.gamestate) - 1
                anyPlayer = [Player.USER, Player.OPP]
                isOccupied = self.gamestate[r][c] in anyPlayer
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
                    self.currentlyPossibleMoves[pawn] = movesForPawn
        return

    def _field_occupied(self, field):
        return self.gamestate[field[0]][field[1]] in [-1, 1]

    def _field_occupied_by_current_player(self, field):
        return self.gamestate[field[0]][field[1]] == self.currentPlayer

    def _field_occupiedByOpponent(self, field):
        """
        Checks if a field on the board is occupied by a pawn owned by the
        opposing player.
        field: (i, j) where i is rowindex and j is colindex.
        return: bool.
        """
        if self.currentPlayer == Player.USER:
            opponent = Player.OPP
        elif self.currentPlayer == Player.OPP:
            opponent = Player.USER
        return self.gamestate[field[0]][field[1]] == opponent

    def _field_on_bord(self, field):
        """
        Checks if the field is in the boundaries of the bord.
        field: (i, j) where i is rowindex and j is colindex.
        return: bool.
        """
        size = len(self.gamestate)
        return field[0] in range(0, size) and field[1] in range(0, size)

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
        if self.currentPlayer == Player.USER:
            isFirstMovementForPiece = pawn[0] == len(self.gamestate) - 2
        if self.currentPlayer == Player.OPP:
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
        return self._field_on_bord(move) and self._field_occupiedByOpponent(move)

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

    def get_movable_pawns(self):
        return self.currentlyPossibleMoves.keys()

    def get_moves_for_pawn(self, pawn):
        moves = self.currentlyPossibleMoves.get(pawn)
        return moves

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
        canFront = self._can_move_front(pawn, move)
        canFrontTwo = self._can_move_front_two(pawn, move)
        canSide = self._can_move_front_side_with_kill(pawn, move)
        canEnPassant = self._can_move_en_passant(pawn, move)
        return canFront or canFrontTwo or canSide or canEnPassant

    def _has_next_move(self):
        """
        Checks if the current player can make any move.
        return: bool.
        """
        return len(self.currentlyPossibleMoves) > 0

    def _get_next_move(self):
        raise NotImplementedError("You should have implemented this")

    def do_move(self, pawn, move):
        """
        Updates the gamestate by performing the move with the pawn.
        Saves the previous gamestate and the move in the respective history.

        pawn: (i, j) where i is rowindex and j is colindex referencing
        the field of a pawn.

        move: (i, j) where i is rowindex and j is colindex referencing
        the field where the pawn wants to move to.

        return: void.
        """
        if self._possible_move(pawn, move):
            self.gamestateHistory.append(deepcopy(self.gamestate))
            self.moveHistory.append((deepcopy(pawn), deepcopy(move)))
            self.gamestate[pawn[0]][pawn[1]] = 0
            self.gamestate[move[0]][move[1]] = self.currentPlayer

    def undo_move(self, mv):
        raise NotImplementedError("You should have implemented this")

    def is_terminal(self):
        return self.player_1_to_win() or self.player_2_to_win()

    def player_1_to_win(self):
        return Player.USER in self.gamestate[0]

    def player_2_to_win(self):
        return Player.OPP in self.gamestate[self.size - 1]

    def get_move_history(self):
        return self.moveHistory

    def get_state_history(self):
        return self.gamestateHistory

    def _get_left(self, rowIndex):
        return rowIndex + self.currentPlayer * -1

    def _get_right(self, rowIndex):
        return rowIndex + self.currentPlayer

    def _get_advance(self, colIndex):
        return colIndex + self.currentPlayer * -1

    def _get_back(self, colIndex):
        return colIndex + self.currentPlayer
