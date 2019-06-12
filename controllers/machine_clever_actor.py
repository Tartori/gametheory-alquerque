#!/usr/bin/python3
from controllers import BaseMachineActor
from random import random, choice
from copy import deepcopy


class MachineCleverActor(BaseMachineActor):
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
        return sum([sum(x) for x in game.get_bord()])
        wins = 0
        for pawn in game.get_movable_pawns():
            for move in game.get_moves_for_pawn(pawn):
                movegame = deepcopy(game)
                movegame.do_move(pawn, move)
                movegame.to_next_turn()
                wins -= self.__monte_carlo(game)
        return wins

    def __monte_carlo(self, game):
        pawn = choice(list(game.get_movable_pawns()))
        move = choice(game.get_moves_for_pawn(pawn))
        game.do_move(pawn, move)
        game.to_next_turn()
        if game.get_winner() is not None:
            return 1
        else:
            return self.__monte_carlo(game)
