#!/usr/bin/python3
from controllers import MachineABPruningActor


class MachineComplexHeuristicActor(MachineABPruningActor):
    """
    This controller takes over during a game play when its the turn
    of a machine player that follows the MachineStrategies.CLEVER.
    """

    def __init__(self, name: str, state, playerId):
        super().__init__(name, state, playerId)

    def __get_heuristic(self, game):
        # TODO: implement heuristic!!!
        pass
