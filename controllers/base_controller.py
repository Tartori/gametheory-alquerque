#!/usr/bin/python3

from sys import stdin

from gui import Output
from models import Commands


class BaseController:
    """

    """
    _state = None
    _gui = Output()
    _shared_options = {
        Commands.QUIT_APP: "stops app",
    }

    def __init__(self, state):
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
