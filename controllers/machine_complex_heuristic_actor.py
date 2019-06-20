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

        for r in range(size):
            for c in range(size):
                # row indices for both perspectives.
                r_opp = r
                r_usr = size - 1 - r

                opp_blocked = False
                usr_blocked = False


#                for preview in range(0, size):
#                    if not usr_blocked and preview < r and board[r][c] == Player.OPP:
#                        usr_blocked = True
#                    elif not opp_blocked and preview > r and board[r][c] == Player.USR:
#                        opp_blocked = True

                if adv_board[r_opp][c] == Player.OPP:
                    # check if blocked
                    for preview in range(r + 1, size - 1):
                        if board[preview][c] == Player.USER:
                            opp_blocked = True
                            break

                    if not opp_blocked:
                        adv_board[r_opp][c] *= 10  # TODO: choose best weight

                    # best row is at the "bottom" of the board
                    # -1 to prevent the first move to always be two steps.
                    # squared weight
                    adv_board[r_opp][c] *= (r_opp - 1) * (r_opp - 1)

                elif adv_board[r_usr][c] == Player.USER:
                    # check if blocked
                    for preview in range(1, r - 1):
                        if board[preview][c] == Player.OPP:
                            usr_blocked = True
                            break

                    if not usr_blocked:
                        adv_board[r_usr][c] *= 10  # TODO: choose best weight

                    # best row is at the "top" of the board
                    adv_board[r_usr][c] *= (r_usr - 1) * (r_usr - 1)

        adv_delta = self._get_fields_delta(adv_board, player)

        # A pawn that has an unblocked path to the finish line is great

        return adv_delta + count_delta
