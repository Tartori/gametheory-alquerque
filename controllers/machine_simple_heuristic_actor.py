#!/usr/bin/python3
from controllers import BaseMachineActor
from random import random, choice
from copy import deepcopy


class MachineSimpleHeuristicActor(BaseMachineActor):
    """
    This controller takes over during a game play when its the turn
    of a machine player that follows the MachineStrategies.CLEVER.
    """

    def __init__(self, name: str, state, playerId):
        super().__init__(name, state, playerId)

    def _choose_best_option(self) -> None:
        """
        Implements the strategy of choosing the best move.
        Sets the properties _selected_pawn and _selected_move.
        """
        (_, self._selected_pawn, self._selected_move) = self.__find_best_solution_rec(
            4, deepcopy(self._state.game.engine))

    def __find_best_solution_rec(self, depth, game):
        """
        """

        if depth == 0:
            return (self.__get_heuristic(game) * game._current_player, None, None)

        alpha = -100
        alphapawn, alphamove = None, None
        for pawn in game.get_movable_pawns():
            for move in game.get_moves_for_pawn(pawn):
                movegame = deepcopy(game)
                movegame.do_move(pawn, move)
                if movegame.get_winner() is None:
                    (opp, _, _) = self.__find_best_solution_rec(depth-1, movegame)
                    sol = -opp
                else:
                    sol = 100
                if sol > alpha:
                    alphamove = move
                    alphapawn = pawn
                    alpha = sol
        return alpha, alphapawn, alphamove

    def __get_heuristic(self, game):
        return sum([sum(x) for x in game.get_bord()])
