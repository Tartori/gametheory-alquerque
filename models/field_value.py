#!/usr/bin/python3


class FieldValue:
    """
    Indicates whether a field is empty or occupied or targetable.
    Used for game logic (engine) and for UI logic.
    Thus DO NOT CHANGE!
    """
    USER = 1
    OPP = -1
    EMPTY = 0
    POSSIBLE_MOVE = 2
