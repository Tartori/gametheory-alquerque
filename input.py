#!/usr/bin/python3

import sys
import re

demooptions = {
    "a1": "select coin on a1",
    "stop": "quit the game"
}

def getInstructions(prefix, options = {}):
    instruction = prefix
    if (len(options) > 0):
        instruction = instruction + "\nChoose: "
        for key, value in options.items():
            instruction = instruction + "  [" + key + "]: " + value
    return instruction


def isBordField(input):
    if len(input) == 2:
        p = re.compile('[A-Ea-e][0-4]')
        if p.match(input) is not None:
            return True
    return False

def mapFieldTextToCoordinates(field):
    """
    Converts a string of two chars to coordinates.
    field: e.g. "A2" or "a2".
    return: e.g. (0, 2).
    """
    if not len(field) == 2:
        "Field must be specified by two chars."
    row = ord(field[0].upper()) - 97
    return (row, field[1])

def isAlquerque(input):
    if len(input) == 1:
        p = re.compile('[A-Ea-e][0-4]')
        if p.match(input) is not None:
            return True
    return False
