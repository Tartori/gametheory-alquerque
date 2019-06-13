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

    def __get_heuristic(self, game):
        return sum([sum(x) for x in game.get_bord()]) * game._current_player
