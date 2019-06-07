#!/usr/bin/python3
from controllers import BaseController
from models import ScreenParameters
from copy import deepcopy


class BaseActor(BaseController):
    """
    Defines the common functionality that all types of player
    share. An actor is anyone who interacts with the gui and the game.
    Can be a human or machine player.
    """
    _name = None

    def __init__(self, name, current):
        super().__init__(current)
        self._name = name

    def take_turn(self):
        pass

    def _prepare_values_to_be_rendered(self):
        """
        Helper function that initializes a new screen parameter object
        with default values.
        """
        values = ScreenParameters()
        if self._current.game is not None:
            values.game = self._current.game
            values.board = self._current.game.get_bord()
            values.moveHistory = self._current.game.get_move_history()
        if self._feedback is not None:
            values.feedback = self._feedback
            self._feedback = None
        if self._name is not None:
            values.player = self._name
        values.options = deepcopy(self._shared_options)
        return values

    def _get_choosable_fields_as_options(self, fields):
        """
        Helper function that converts fields to options.
        """
        fieldNames = self._gui.map_fields_coordinates_to_text(fields)
        options = {}
        for f in fieldNames:
            options[f] = ""
        return options
