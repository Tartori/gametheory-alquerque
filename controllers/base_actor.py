#!/usr/bin/python3
from controllers.base_controller import BaseController
from models import States
from copy import deepcopy


class BaseActor(BaseController):
    """
    Defines the common functionality that all types of player
    share. An actor is anyone who interacts with the gui and the game.
    Can be a human or machine player.
    """

    _player_id = None

    # Describes the currently selected pawn
    _selected_pawn = None

    # Describes the currently selected move for the selected pawn
    _selected_move = None

    def __init__(self, name, state, playerId):
        super().__init__(name, state)
        self._player_id = playerId

    def take_turn(self):
        """
        The action a player does, when it is his turn.
        """
        raise NotImplementedError("Abstract method.")

    def get_name(self):
        return self._name

    def _do_draw(self):
        """
        Once the pawn and move have been selected,
        this method executes the draw.
        Must be used by inheriting classes.
        """
        self._state.game.engine.do_move(self._selected_pawn,
                                        self._selected_move)
        pawnText = self._gui \
            ._map_field_coordinates_to_text(self._selected_pawn)
        moveText = self._gui \
            ._map_field_coordinates_to_text(self._selected_move)
        history_text = "Player " + self._name + " moved " + \
            pawnText + " to " + moveText
        self._state.feedback = history_text
        self._state.game.history.append(history_text)

        self._state.activity = States.TAKE_TURN

    def _get_choosable_fields_as_options(self, fields):
        """
        Helper function that converts fields to options.
        """
        fieldNames = self._gui.map_fields_coordinates_to_text(fields)
        options = {}
        for f in fieldNames:
            options[f] = ""
        return options
