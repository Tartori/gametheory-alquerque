#!/usr/bin/python3
from controllers import BaseMachineActor
from random import random, choice


class MachineRandomActor(BaseMachineActor):
    """
    This controller takes over during a game play when its the turn
    of a machine player that follows the MachineStrategies.RANDOM.
    """

    def __init__(self, name: str, state, playerId):
        super().__init__(name, state, playerId)

    def _choose_best_option(self) -> None:
        """
        Implements the strategy of choosing the best move.
        Sets the properties _selected_pawn and _selected_move.
        """
        pawn = choice(list(self._state.game.engine.get_movable_pawns()))
        move = choice(self._state.game.engine.get_moves_for_pawn(pawn))
        self._selected_pawn = pawn
        self._selected_move = move
