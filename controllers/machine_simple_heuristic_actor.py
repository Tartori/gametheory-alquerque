#!/usr/bin/python3
from controllers import MachineABPruningActor
from random import random, choice
from copy import deepcopy


class MachineSimpleHeuristicActor(MachineABPruningActor):
    """
    This controller takes over during a game play when its the turn
    of a machine player that follows the MachineStrategies.SIMPLE_HEURISTIC.
    """

    def __init__(self, name: str, state, playerId):
        super().__init__(name, state, playerId)

        return sum([sum(x) for x in game.get_bord()]) * game._current_player
    def _get_heuristic(self, game):
