#!/usr/bin/python3
from controllers import BaseMachineActor
from random import random, choice
from copy import deepcopy


class MachineABPruningActor(BaseMachineActor):
    """
    This controller ist the base for all actions of a machine player
    where the machine player uses alpha beta pruning for traversing
    the game tree.
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

    def __find_best_solution_rec(self, depth, game, alpha=-100):
        """
        """

        if depth == 0:
            return (self.__get_heuristic(game), None, None)

        alphapawn, alphamove = None, None
        for pawn in game.get_movable_pawns():
            for move in game.get_moves_for_pawn(pawn):
                movegame = deepcopy(game)
                movegame.do_move(pawn, move)
                movegame.to_next_turn()
                if movegame.get_winner() is not None:
                    return 100, pawn, move
                (opp, _, _) = self.__find_best_solution_rec(
                    depth-1, movegame, alpha)
                sol = -opp
                if(sol < alpha):
                    break
                alphamove = move
                alphapawn = pawn
                alpha = sol
        return alpha, alphapawn, alphamove

    def __get_heuristic(self, game):
        raise NotImplementedError("Abstract method.")
