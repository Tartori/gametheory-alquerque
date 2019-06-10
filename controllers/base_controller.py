#!/usr/bin/python3

from sys import stdin
from copy import deepcopy

from gui import Output
from models import Commands, ScreenParameters, States, CurrentGame


class BaseController:
    """
    This app is build on the idea of MVC.
    This is the controller all other controllers inherit from.
    """
    # Contains the global state store of the app.
    # Is shared amongst all controllers.
    _state = None

    # The name of this actor so we know who is doing what.
    _name = None

    # Produces the screen rendering.
    _gui = Output()

    # Input options that are used in all controllers.
    _shared_options = {
        Commands.QUIT_APP: "stops app",
        Commands.ABORT_GAME_START_FRESH: "abort game"
    }

    def __init__(self, name, state):
        self._name = name
        self._state = state
        pass

    def _map_field_text_to_coordinates(self, field):
        """
        Converts a string of two chars to coordinates.
        field: e.g. "A2" or "a2".
        return: e.g. (0, 2).
        """
        if not len(field) == 2:
            "Field must be specified by two chars."
        row = ord(field[0].upper()) - 65
        col = int(field[1])
        return (row, col)

    def _read_input(self):
        """
        Gets the user input. Cleans out any line breaks
        and ensures is in upper case.
        return: String of user input.
        """
        try:
            # Remove end of line char.
            return stdin.readline().strip().upper()
        except:
            return ""

    def _prepare_values_to_be_rendered(self):
        """
        Helper function that initializes a new screen parameter object
        with default values.
        """
        values = ScreenParameters()
        if self._state.game is not None and \
                self._state.game.engine is not None:
            values.game = self._state.game.engine
            values.board = self._state.game.engine.get_bord()
            values.moveHistory = self._state.game.engine.get_move_history()
        if self._state.feedback is not None:
            values.feedback = self._state.feedback
            self._state.feedback = None
        if self._name is not None:
            values.player = self._name
        values.options = deepcopy(self._shared_options)
        return values

    def _handle_common_inputs(self, input, allOptions):
        """
        Handles inputs that are common amongst all promts.
        Handles bad input.
        If has handled input, returns True. Else False.
        """
        if input in self._shared_options:
            if input == Commands.QUIT_APP:
                self._state.feedback = None
                self._state.activity = States.BYE
            elif input == Commands.ABORT_GAME_START_FRESH:
                self._state.feedback = "You aborted the game. Start a new one."
                self._state.game = CurrentGame()
                self._state.activity = States.CHOOSE_GAME
            elif input not in allOptions:
                self._state.feedback = "Bad input! "
            return True
        else:
            return False
