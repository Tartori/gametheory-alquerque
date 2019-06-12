#!/usr/bin/python3

"""
You can either create a Field by giving row and column
>>> Field(row=1,column=2)
Field(row=1,column=2,)

Or by entering a Text
>>> Field(text="B3")
Field(row=1,column=3,)

You need to do either or else you'll get an exception
>>> Field()
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
  File "/Users/julian/school/gametheory-alquerque/definitions.py", line 59,
    in __init__
    raise Exception("Pass either col and row or text.")
Exception: Pass either col and row or text.

"""
import re
import unittest


class Field:
    """
    Represents a field on the game board.
    Better than a mere tuple since can be created from:
    - coordinates (row, col), e.g. (1, 2)
    - text (text), e.g. ("B2")
    """

    def __init__(self, row=-1, column=-1, text=""):
        """
        You can use either set of arguments:
        - Field(row, col) where row and col are integers starting at 0.
        - Field(text) where text is a string of length 2 where
            - first char is a letter representing the row
            - second char is number representing the col
        """
        # Create Field from text, e.g. 'B2'.
        if (text):
            if not re.match('^([a-zA-Z]){1}[0-9]{1}$', text):
                raise Exception(
                    "Field must be specified by two chars, e.g. 'A0'.")
            self.row = ord(text[0]) - 65
            self.column = int(text[1])
        # Create Field from row and col indices.
        elif (row >= 0 and column >= 0):
            self.row = row
            self.column = column
        else:
            raise Exception("Pass either col and row or text.")

        self.coords = (self.row, self.column)

    def __repr__(self):
        return ('Field('
                f'row={self.row},'
                f'column={self.column},'
                ')')


if __name__ == '__main__':
    import doctest
    doctest.testmod()
