#!/usr/bin/python3

from pip._vendor.colorama import init, Fore, Style
import re

# for demo state only!!!
demoboard = [
        [-1, -1, -1, -1, -1],
        [-1, -1, -1, -1, -1],
        [-1, -1, 0, 1, 1],
        [1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1],
    ]

def printScreen(positions):
    """"""
    init()
    lines = assembleComponents(positions)
    for line in lines:
        print(line)
    return

def assembleComponents(positions):
    layout = [
        ""
    ]
    screen = []
    padding = 100
    initialpadding = 0
    while initialpadding < padding:
        screen.append("")
        initialpadding = initialpadding + 1
    title = prepareTitle()
    for i in title:
        screen.append(i)
    board = prepareBoard(positions)
    for i in board:
        screen.append(i)
    renderInto(screen, 150, padding + 30, [], 0, 0, 0, 0)
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
    colLabels    = "     0   1   2   3   4"
    rowSeparator = "   +---+---+---+---+---+"
    rowConnector = "   + | ╳ | ╳ | ╳ | ╳ | +"
    conn = [
        "╲\|/",
        ""
    ]
    board = []
    board.append(colLabels)
    board.append(rowSeparator)
    for rowindex in range(0, 5):
        cells = []
        cells.append(getRowLabel(rowindex)) # one char in length
        for cellindex in range(0, 5):
            cells.append(prepareCell(positions[rowindex][cellindex])) # one char in length
        row = (" " + ' ¦ '.join(['%s']*len(cells)) + " ¦") % tuple(cells)
        board.append(row)
        board.append(rowSeparator)
    return board

def getRowLabel(rowindex):
    return chr(rowindex + 97).upper()

def prepareCell(value):
    options = {
        - 1: Fore.RED + "■" + Fore.RESET,
        0: " ",
        1: Fore.CYAN + "■" + Fore.RESET
    }
    return options.get(value, "?")


def prepareHistory():
    """"""
    return [
        "E0 to B4",
        "something",
        "K5 to W22             "
    ]

def renderInto(whole, wwidth, wheight, part, ptop, pleft, pwidth, pheight):
    """"""
    # if whole does not comply to the defined width and height, then extend or shorten
    if (len(whole) > wheight):
        whole = whole[:wheight]
    if (len(whole) < wheight):
        delta = wheight - len(whole)
        i = 0
        while i < delta:
            whole.append(".")
            i += 1
    for r, row in enumerate(whole):
        #print("row " + str(len(row)) + " wwidth " + str(wwidth))
        lenrow = len(escape_ansi(row))
        if (lenrow > wwidth):
            whole[r] = row[:wwidth]
        if (lenrow < wwidth):
            whole[r] = row + "." * (wwidth - lenrow)
    return


def escape_ansi(line):
    ansi_escape =re.compile(r'(\x9B|\x1B\[)[0-?]*[ -\/]*[@-~]')
    return ansi_escape.sub('', line)
