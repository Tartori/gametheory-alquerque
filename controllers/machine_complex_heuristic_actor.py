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
        usr_now_blocked = [False] * size
        opp_now_blocked = [False] * size

        for r in range(size - 1, -1, -1):
            for c in range(size):
                # row indices for both perspectives.
                r_opp = r
                r_usr = size - 1 - r

                # Perspective of user.
                if board[r_usr][c] == Player.OPP:
                    usr_now_blocked[c] = True
                elif board[r_usr][c] == Player.USER:
                    # best row is at the "top" of the board
                    adv_board[r_usr][c] *= (r_usr - 1) * (r_usr - 1)

                    if not usr_now_blocked[c]:
                        adv_board[r_usr][c] *= 10  # TODO: choose best weight

                # Perspective of opp.
                if board[r_opp][c] == Player.USER:
                    opp_now_blocked[c] = True
                elif board[r_opp][c] == Player.OPP:
                    # best row is at the "bottom" of the board
                    # -1 to prevent the first move to always be two steps.
                    # squared weight
                    adv_board[r_opp][c] *= (r_opp - 1) * (r_opp - 1)

                    if not opp_now_blocked[c]:
                        adv_board[r_opp][c] *= 10  # TODO: choose best weight

        adv_delta = self._get_fields_delta(adv_board, player)

        # A pawn that has an unblocked path to the finish line is great

        return adv_delta + count_delta
