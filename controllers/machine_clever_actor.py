#!/usr/bin/python3
from controllers import MachineABPruningActor
from random import random, choice
from copy import deepcopy


class MachineCleverActor(MachineABPruningActor):
    """
    This controller takes over during a game play when its the turn
    of a machine player that follows the MachineStrategies.CLEVER.
    """

    def __init__(self, name: str, state, playerId):
        super().__init__(name, state, playerId)

    def __get_heuristic(self, game):
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
