#!/usr/bin/python3


class BoardGame:
    """
    The base class for the board games.
    NOT REALLY IMPLEMENTED.
    """
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
