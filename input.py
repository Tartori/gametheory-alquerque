#!/usr/bin/python3
import sys


def map_field_text_to_coordinates(field):
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


def read_input():
    """
    Gets the user input. Cleans out any line breaks
    and ensures is in upper case.
    return: String of user input.
    """
    try:
        # Remove end of line char.
        return sys.stdin.readline().strip().upper()
    except:
        return ""
