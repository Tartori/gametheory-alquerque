#!/usr/bin/python3
from models import Player, FieldValue
from games.board_game import BoardGame
from math import floor


class Alquerque(BoardGame):
    """
    The game engine to play Alquerque.
    NOT REALLY IMPLEMENTED.
    """

    def __init__(self, player, size=7):
        super().__init__(player, size)

    def _set_start_state(self):
        """
        Initializes the board.
        Void.
        """
        if(self._size < self._MINIMUM_BOARD_SIZE):
            self._size = self._MINIMUM_BOARD_SIZE

        mid_index = floor(self._size / 2)
        self._board = [[Player.OPP for col in range(self._size)]
                       for row in range(mid_index)]
        middle_row = [Player.OPP for col in range(mid_index)]
        middle_row.extend([FieldValue.EMPTY])
        middle_row.extend([Player.USER for col in range(mid_index)])
        self._board.extend([middle_row])
        self._board.extend(
            [[Player.USER for col in range(self._size)]
             for row in range(mid_index)]
        )

    def _find_all_moves(self):
        """
        For each pawn of the current player, finds all possible moves.
        return: void. (sets field)
        """
        self._possible_moves = {}
        for r in range(0, self._size):
            for c in range(0, self._size):
                movesForPawn = []

                pawn = (r, c)

                # check if any pawn.
                if not self._field_occupied_by_current_player(pawn):
                    continue

                moveFront = self._front(pawn)
                moveFrontTwo = self._front(pawn, 2)
                moveFrontLeft = self._front(self._left(pawn))
                moveFrontLeftTwo = self._front(self._left(pawn, 2), 2)
                moveFrontRight = self._front(self._right(pawn))
                moveFrontRightTwo = self._front(self._right(pawn, 2), 2)
                moveLeft = self._left(pawn)
                moveLeftTwo = self._left(pawn, 2)
                moveRight = self._right(pawn)
                moveRightTwo = self._right(pawn)
                moveBack = self._back(pawn)
                moveBackTwo = self._back(pawn, 2)
                moveBackLeft = self._back(self._left(pawn))
                moveBackLeftTwo = self._back(self._left(pawn, 2), 2)
                moveBackRight = self._back(self._right(pawn))
                moveBackRightTwo = self._back(self._right(pawn, 2), 2)

                if self._can_move_one_field(pawn, moveFront):
                    movesForPawn.append(moveFront)
                if self._can_move_one_field(pawn, moveLeft):
                    movesForPawn.append(moveLeft)
                if self._can_move_one_field(pawn, moveRight):
                    movesForPawn.append(moveRight)
                if self._can_move_one_field(pawn, moveBack):
                    movesForPawn.append(moveBack)
                if self._can_move_one_field(pawn, moveFrontLeft):
                    movesForPawn.append(moveFrontLeft)
                if self._can_move_one_field(pawn, moveFrontRight):
                    movesForPawn.append(moveFrontRight)
                if self._can_move_one_field(pawn, moveBackLeft):
                    movesForPawn.append(moveBackLeft)
                if self._can_move_one_field(pawn, moveBackRight):
                    movesForPawn.append(moveBackRight)
                if self._can_move_two_fields(pawn, moveFront, moveFrontTwo):
                    movesForPawn.append(moveFrontTwo)
                if self._can_move_two_fields(pawn, moveLeft, moveLeftTwo):
                    movesForPawn.append(moveLeftTwo)
                if self._can_move_two_fields(pawn, moveRight, moveRightTwo):
                    movesForPawn.append(moveRightTwo)
                if self._can_move_two_fields(pawn, moveBack, moveBackTwo):
                    movesForPawn.append(moveBackTwo)
                if self._can_move_two_fields(pawn, moveFrontLeft, moveFrontLeftTwo):
                    movesForPawn.append(moveFrontLeftTwo)
                if self._can_move_two_fields(pawn, moveFrontRight, moveFrontRightTwo):
                    movesForPawn.append(moveFrontRightTwo)
                if self._can_move_two_fields(pawn, moveBackLeft, moveBackLeftTwo):
                    movesForPawn.append(moveBackLeftTwo)
                if self._can_move_two_fields(pawn, moveBackRight, moveBackRightTwo):
                    movesForPawn.append(moveBackRightTwo)

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
        diffRow = move[0] - pawn[0]
        deltaRow = abs(diffRow)
        dirRow = 1
        if diffRow < 0:
            dirRow = -1
        diffCol = move[1] - pawn[1]
        deltaCol = abs(diffCol)
        dirCol = 1
        if diffCol < 0:
            dirCol = -1
        validOneField = deltaRow == 0 and deltaCol == 1 or \
            deltaRow == 1 and deltaCol == 1 or \
            deltaRow == 1 and deltaCol == 0
        validTwoFields = deltaRow == 0 and deltaCol == 2 or \
            deltaRow == 2 and deltaCol == 2 or \
            deltaRow == 2 and deltaCol == 0

        if validOneField:
            if self._can_move_one_field(pawn, move):
                return True
        if validTwoFields:
            if deltaRow == 2:
                intermRow = 1 * dirRow
            else:
                intermRow = 0
            if deltaCol == 2:
                intermCol = 1 * dirCol
            else:
                intermCol = 0
            interm = (pawn[0] + intermRow, pawn[1] + intermCol)
            if self._can_move_two_fields(pawn, interm, move):
                return True
        return False

    def _can_move_one_field(self, pawn, targetField):
        """
        Checks if a pawn can move to the neighbouring field on the bord.
        pawn: (i, j) where i is rowindex and j is colindex referencing the
        field of a pawn.
        targetField: (i, j) where i is rowindex and j is colindex referencing
        the field where the pawn wants to move to.
        return: bool.
        """
        if not self._field_on_bord(targetField):
            return False
        if self._field_occupied(targetField):
            return False
        return True

    def _can_move_two_fields(self, pawn, intermediateField, targetField):
        """
        Checks if a pawn can move to the next to neighbouring field
        on the bord.
        pawn: (i, j) where i is rowindex and j is colindex referencing the
        field of a pawn.
        intermediateField: (i, j) where i is rowindex and j is colindex
        referencing the field the pawn needs to jump.
        targetField: (i, j) where i is rowindex and j is colindex referencing
        the field where the pawn wants to move to.
        return: bool.
        """
        if not self._field_on_bord(targetField):
            return False
        if not self._field_occupiedByOpponent(intermediateField):
            return False
        if self._field_occupied(targetField):
            return False
        return True

    def _handle_kill(self, pawn, move):
        """
        Removes killed pawns.
        """
        vector_x = move[0] - pawn[0]
        vector_y = move[1] - pawn[1]
        if abs(vector_x) == 2 or abs(vector_y) == 2:
            kill_x = pawn[0]
            if abs(vector_x) > 0:
                kill_x += int(vector_x / abs(vector_x))
            kill_y = pawn[1]
            if abs(vector_y) > 0:
                kill_y += int(vector_y / abs(vector_y))
            self._board[kill_x][kill_y] = FieldValue.EMPTY

    def _check_for_winner(self):
        """
        Checks if the current player has just won the game.
        Must assign the Player to self._winner.
        """
        peekInitialStateOfNextTurn = self.peek()
        if not peekInitialStateOfNextTurn.has_next_move():
            self._winner = self._current_player
        del peekInitialStateOfNextTurn
