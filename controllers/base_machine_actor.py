#!/usr/bin/python3
from controllers import BaseActor


class BaseMachineActor(BaseActor):
    """
    This controller takes over during a game play when its the turn
    of a machine player. Abstract class.
    Implement for each machine strategy!
    """

    def __init__(self, name, state):
        super().__init__(name, state)

    def take_turn(self):
        """
        Called when its the turn of the actor this controller represents.
        Since there is no user interaction, no need for a loop of states.
        This method is shared amongst all child classes.
        """
        self._choose_best_option()
        self._do_draw()

    def _choose_best_option(self):
        """
        Implements the strategy of choosing the best move.
        Sets the properties _selected_pawn and _selected_move.
        Must be implemented by all child classes.
        """
