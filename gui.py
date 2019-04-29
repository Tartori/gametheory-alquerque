#!/usr/bin/python3

from pip._vendor.colorama import init, Fore, Style
import re
import os
from definitions import *

# for demo state only!!!
demoboard = [
        [-1, -1, -1, -1, -1],
        [-1, -1, -1, -1, -1],
        [-1, -1, 0, 1, 1],
        [1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1],
    ]


clear = lambda: os.system('cls' if os.name=='nt' else 'clear')


def printScreen(positions, history, instruction):
    """Renders one screen to the console."""
    init()
    clear()
    lines = assembleComponents(positions, history, instruction)
    for line in lines:
        print(line)
    return


def assembleComponents(positions, history, instruction):
    """For one screen to be rendered, combines all components based on the given data."""
    layout = [
        ""
    ]
    screen = []
    padding = 20
    initialpadding = 0
    while initialpadding < padding:
        screen.append("")
        initialpadding = initialpadding + 1
    renderInto(screen, 150, padding + 20, [], 0, 0, 0, 0)
    # insert from top to bottom and from right to left, because of escaped chars counting problems!
    renderInto(screen, 150, padding + 20, prepareTitle(), padding + 0, 0, 40, 5)
    renderInto(screen, 150, padding + 20, prepareHistory(history), padding + 6, 40, 40, 15)
    renderInto(screen, 150, padding + 20, prepareBoard(positions), padding + 6, 0, 40, 15)
    renderInto(screen, 150, padding + 20, prepareInstruction(instruction), padding + 19, 0, 40, 1)
    return screen


def prepareTitle():
    """Shows the game title. Returns a list of lines to be rendered."""
    title = [
        " _____ _                             ",
        "|  _  | |___ _ _ ___ ___ ___ _ _ ___ ",
        "|     | | . | | | -_|  _| . | | | -_|",
        "|__|__|_|_  |___|___|_| |_  |___|___|",
        "          |_|             |_|   " + Fore.LIGHTBLACK_EX + "by Julian Stampfli and Marc Rey 2019" + Fore.RESET,
    ]
    return title


def prepareBoard(positions):
    """Shows the Alquerque/Checkers board. Returns a list of lines to be rendered."""
    colLabels    = "     0   1   2   3   4"
    rowSeparator = "   +---+---+---+---+---+"
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
    """Returns the letter (A-E) for the desired row."""
    return chr(rowindex + 97).upper()


def prepareCell(value):
    """Returns the coin in the color of the respective player."""
    options = {
        PLAYER2: getPlayersColor(PLAYER2) + "■" + Fore.RESET,
        0: " ",
        PLAYER1: getPlayersColor(PLAYER1) + "■" + Fore.RESET
    }
    return options.get(value, "?")


def prepareHistory(steps):
    """Returns some lines containing the game history."""
    history = [
        "HISTORY:",
        "----------------",
    ]
    history.extend(steps)
    return history

def prepareInstruction(instruction):
    """Returns an instruction to the user formatted."""
    result = Fore.YELLOW + instruction + Fore.RESET
    return [result]


def renderInto(whole, wwidth, wheight, part, ptop, pleft, pwidth, pheight):
    """Define the size of a canvas to be rendered and place some lines of content at a specific position."""
    # if whole does not comply to the defined width and height, then extend or shorten
    if (len(whole) > wheight):
        whole = whole[:wheight]
    if (len(whole) < wheight):
        delta = wheight - len(whole)
        i = 0
        while i < delta:
            whole.append(" ")
            i += 1
    for r, row in enumerate(whole):
        #print("row " + str(len(row)) + " wwidth " + str(wwidth))
        lenrow = len(escape_ansi(row))
        if (lenrow > wwidth):
            whole[r] = row[:wwidth]
        if (lenrow < wwidth):
            whole[r] = row + " " * (wwidth - lenrow)
    # Insert the partial component.
    if (pwidth > 0 and pheight > 0 and len(part) > 0):
        for r, row in enumerate(whole):
            if (r >= ptop and r < ptop + pheight and len(part) > r - ptop):
                newRow = insertIntoString(row, part[r - ptop], pleft)
                whole[r] = newRow

    return


def escape_ansi(line):
    """If we have some escape characters in a string, they would be counted by len() but not shown. Thus strip before getting len()."""
    ansi_escape =re.compile(r'(\x9B|\x1B\[)[0-?]*[ -\/]*[@-~]')
    return ansi_escape.sub('', line)


def insertIntoString(fullString, newPart, startingAt):
    """Insert a string into another string starting at a specific index. Takes into account that there might be esc chars."""
    prefix = fullString[:startingAt]
    postfix = fullString[(startingAt + len(escape_ansi(newPart))) :]
    newString = "".join([prefix, newPart, postfix])
    return newString


def addCommandToVisibleCommandHistory(history, command):
    """Adds the last user input to the cli-rendered history of commands."""
    if(len(history) > 3):
        history.pop(0)
    history.append(command)
    return history


def getPlayersColor(player):
    """Returns the color for PLAYER1 and PLAYER2."""
    print(player)
    if not (player == PLAYER1 or player == PLAYER2):
        raise "Player does not exist"
    if player == PLAYER1:
        return Fore.BLUE
    if player == PLAYER2:
        return Fore.RED
