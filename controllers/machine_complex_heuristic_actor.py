#!/usr/bin/python3
from controllers import MachineABPruningActor
from copy import deepcopy
from models import Player


class MachineComplexHeuristicActor(MachineABPruningActor):
    """
    This controller takes over during a game play when its the turn
    of a machine player that follows the MachineStrategies.COMPLEX_HEURISTIC.
    This means, the board is evaluated based on the sum of pawns and their
    position on the board.
    """

    def __init__(self, name: str, state, playerId):
        super().__init__(name, state, playerId)

    def _get_heuristic(self, game):
        """ This evaluates the board based on a custom heuristic.

        Considerations taken into account are:
        - The further advanced a pawn, the better.
        - If a pawns path is unblocked by enemy pawns, this is great.
        - Having more pawns than the player is great. (But secondary
          to the previous factors)

        Arguments:
            game {BoardGame} -- any game engine.

        Returns:
            integer -- an indication of the current player's preference
                for the current board.
        """
        board = game._get_bord()
        player = game._current_player
        size = game._size

        # [1] The more pawns one has compared to the number of pawns
        # the opponent has, the better.

        count_delta = self._get_fields_delta(board, player)

        # [2] The further advanced a pawn, the better.
        # Free paths are great.

        adv_board = deepcopy(board)
        usr_now_blocked = [False] * size
        opp_now_blocked = [False] * size

        # Traversal of board backwards for performance reasons.
        # (free paths flags)
        # Of course this could also be done by flipping calculation of
        # the row indices. But that seems counterintuitive.
        for r in range(size - 1, -1, -1):
            for c in range(size):
                # Row indices for both perspectives.
                # We will be travelling the board from both ends
                # at the same time.
                r_opp = r
                r_usr = size - 1 - r

                # Perspective of Player.USER.
                if board[r_usr][c] == Player.OPP:
                    # If this field is occupied by the Player.OPP
                    # and since we are travelling the board from the final row
                    # a pawn of the Player.USER can reach,
                    # we can set a flag to remember, that this col is now
                    # blocked for all Player.USER's pawns less advanced.
                    usr_now_blocked[c] = True
                elif board[r_usr][c] == Player.USER:
                    # Evaluate the position of the Player.USER's pawn:
                    # - the further advanced (given as value in r_usr),
                    #   the better.
                    # - if the column ahead is free from Player.OPP's pawns,
                    #   gets a bonus.
                    # To prevent each pawn from taking 2 fields as a first
                    # step, subtracted 1 from value.
                    adv_board[r_usr][c] *= (r_usr - 1) * (r_usr - 1)

                    if not usr_now_blocked[c]:
                        adv_board[r_usr][c] *= 10  # TODO: choose best weight

                # Perspective of Player.OPP.
                if board[r_opp][c] == Player.USER:
                    # If this field is occupied by the Player.USER
                    # and since we are travelling the board from the final row
                    # a pawn of the Player.OPP can reach,
                    # we can set a flag to remember, that this col is now
                    # blocked for all Player.OPP's pawns less advanced.
                    opp_now_blocked[c] = True
                elif board[r_opp][c] == Player.OPP:
                    # Evaluate the position of the Player.USER's pawn:
                    # - the further advanced (given as value in r_usr),
                    #   the better.
                    # - if the column ahead is free from Player.OPP's pawns,
                    #   gets a bonus.
                    # To prevent each pawn from taking 2 fields as a first
                    # step, subtracted 1 from value.
                    adv_board[r_opp][c] *= (r_opp - 1) * (r_opp - 1)

                    if not opp_now_blocked[c]:
                        adv_board[r_opp][c] *= 10  # TODO: choose best weight

        adv_delta = self._get_fields_delta(adv_board, player)

        # We refrain from adjusting weights of both aspects. Could be
        # optimized by collecting data.
        return adv_delta + count_delta
