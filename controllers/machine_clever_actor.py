#!/usr/bin/python3
from controllers import BaseMachineActor
from random import random, choice


class MachineCleverActor(BaseMachineActor):
    """
    This controller takes over during a game play when its the turn
    of a machine player that follows the MachineStrategies.CLEVER.
    """

    def __init__(self, name: str, state):
        super().__init__(name, state)

    def _choose_best_option(self) -> None:
        """
        Implements the strategy of choosing the best move.
        Sets the properties _selected_pawn and _selected_move.
        """

        # TODO: Jules, find best pawn and move!
        raise NotImplementedError("Implement me!")

        # TODO: Jules, assign pawn and move!
        self._selected_pawn = None
        self._selected_move = None
