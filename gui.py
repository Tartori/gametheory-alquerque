#!/usr/bin/python3

# for demo state only!!!
demoboard = [
        [-1, 0, -1, 0, -1, 0, -1, 0, -1],
        [0, -1, 0, -1, 0, -1, 0, -1, 0],
        [-1, 0, -1, 0, -1, 0, -1, 0, -1],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 1, 0, 1, 0, 1, 0, 1, 0],
        [1, 0, 1, 0, 1, 0, 1, 0, 1],
        [0, 1, 0, 1, 0, 1, 0, 1, 0],
    ]

def printScreen(positions):
    """"""
    lines = assembleComponents(positions)
    for line in lines:
        print(line)
    return

def assembleComponents(positions):
    screen = []
    title = prepareTitle()
    for i in title:
        screen.append(i)
    board = prepareBoard(positions)
    for i in board:
        screen.append(i)
    return screen

def prepareTitle():
    """"""
    title = [
        " _____ _                             ",
        "|  _  | |___ _ _ ___ ___ ___ _ _ ___ ",
        "|     | | . | | | -_|  _| . | | | -_|",
        "|__|__|_|_  |___|___|_| |_  |___|___|",
        "          |_|             |_|        ",
    ]
    return title

def prepareBoard(positions):
    """"""
    colLabels    = "     0   1   2   3   4   5   6   7  "
    rowSeparator = "   +---+---+---+---+---+---+---+---+"
    board = []
    board.append(colLabels)
    board.append(rowSeparator)
    for rowindex in range(0, 8):
        cells = []
        cells.append(getRowLabel(rowindex)) # one char in length
        for cellindex in range(0, 8):
            cells.append(prepareCell(positions[rowindex][cellindex])) # one char in length
        row = (" " + ' | '.join(['%s']*len(cells)) + " |") % tuple(cells)
        board.append(row)
        board.append(rowSeparator)
    return board

def getRowLabel(rowindex):
    return chr(rowindex + 97).upper()

def prepareCell(value):
    options = {
        - 1: "O",
        0: " ",
        1: "X"
    }
    return options.get(value, "?")


def prepareHistory():
    """"""
    return
