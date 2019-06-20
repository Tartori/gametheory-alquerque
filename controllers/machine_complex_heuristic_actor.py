#!/usr/bin/python3
from controllers import MachineABPruningActor
from copy import deepcopy
from models import Player


class MachineComplexHeuristicActor(MachineABPruningActor):
    """
    This controller takes over during a game play when its the turn
    of a machine player that follows the MachineStrategies.COMPLEX_HEURISTIC.
    """

    def __init__(self, name: str, state, playerId):
        super().__init__(name, state, playerId)

    def _get_heuristic(self, game):
        board = game._get_bord()
        player = game._current_player
        size = game._size

        # The more pawns one has compared to the number of pawns
        # the opponent has, the better.
        count_delta = self._get_fields_delta(board, player)

        # The further advanced a pawn, the better.
        adv_board = deepcopy(board)
        top_field_value = [0] * size
        btm_field_value = [0] * size

        for r in range(size):
            for c in range(size):
                if adv_board[r][c] == Player.OPP:
                    # best row is at the "bottom" of the board
                    # -1 to prevent the first move to always be two steps.
                    # squared weight
                    adv_board[r][c] *= (r - 1) * (r - 1)

                    if top_field_value[c] == 0:
                        top_field_value[c] = Player.OPP
                    btm_field_value[c] = Player.OPP
                elif adv_board[r][c] == Player.USER:
                    # best row is at the "top" of the board
                    adv_board[r][c] *= (size - 1 - r - 1) * (size - 1 - r - 1)

                    if top_field_value[c] == 0:
                        top_field_value[c] == Player.USER
                    btm_field_value[c] = Player.USER

        adv_delta = self._get_fields_delta(adv_board, player)

        # A pawn that has an unblocked path to the finish line is great
        count_free_cols_usr = 0
        count_free_cols_opp = 0
        for p in top_field_value:
            if p == Player.USER:
                count_free_cols_usr += Player.USER
        for p in btm_field_value:
            if p == Player.OPP:
                count_free_cols_opp += Player.OPP

        free_row_delta = (count_free_cols_opp + count_free_cols_usr) * 10

        return adv_delta + count_delta + free_row_delta
