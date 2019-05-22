#!/usr/bin/python3

import unittest


class Player:
    USER = 1
    OPP = -1


class FieldValue:
    USER = 1
    OPP = -1
    EMPTY = 0
    POSSIBLE_MOVE = 2


class Field:
    """
    Represents a field on the game board.
    Better than a mere tuple since can be created from:
    - coordinates (row, col), e.g. (1, 2)
    - text (text), e.g. ("B2")
    """

    row = None
    col = None
    text = None
    rowText = None
    colText = None
    coords = None
    value = None

    def __init__(self, *args):
        """
        You can use either set of arguments:
        - Field(row, col) where row and col are integers starting at 0.
        - Field(text) where text is a string of length 2 where
            - first char is a letter representing the row
            - second char is number representing the col
        """
        # Create Field from text, e.g. 'B2'.
        if (len(args) == 1):
            self.text = args[0]
            if not len(self.text) == 2:
                raise Exception(
                    "Field must be specified by two chars, e.g. 'A0'.")
            self.rowText = self.text[0].upper()
            self.colText = self.text[1]
            self.row = ord(self.rowText) - 65
            self.col = int(self.colText)
        # Create Field from row and col indices.
        elif (len(args) == 2):
            self.row = args[0]
            self.col = args[1]
            self.text = chr(self.row + 97).upper() + str(self.col)
            self.rowText = self.text[0]
            self.colText = self.text[1]
        else:
            raise Exception("Pass either col and row or text.")

        self.coords = (self.row, self.col)


class TestField(unittest.TestCase):
    def test__init__with_indices(self):
        cases = [
            [0, 0, "A0", "A", "0", (0, 0)],
            [1, 2, "B2", "B", "2", (1, 2)],
        ]

        for params in cases:

            actual = Field(params[0], params[1])
            self.assertEqual(actual.row, params[0])
            self.assertEqual(actual.col, params[1])
            self.assertEqual(actual.text, params[2])
            self.assertEqual(actual.rowText, params[3])
            self.assertEqual(actual.colText, params[4])
            self.assertEqual(actual.coords, params[5])


if __name__ == "__main__":
    unittest.main()
