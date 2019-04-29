#!/usr/bin/python3

import sys

from gui import *
from input import *

def run():
    """Starts the game loop."""
    board = demoboard
    history = []

    currentOptions = {"stop": "stops app", "me": "if you want to start the game", "you": "if i shall start the game", }
    currentInstruction = getInstructions("Hi!", currentOptions)
    currentInput = ""
    printScreen(board, history, currentInstruction)

    going = True
    while going:
        try:
            input = getInput(currentOptions)
            currentInput = input
            if (currentInput == "stop"):
                currentInstruction = "Bye bye!"
                going = False
            else:
                if isBordField(currentInput):
                    currentInstruction = getInstructions("OK. You selected field " + currentInput + ".", currentOptions)
                else:
                    currentInstruction = getInstructions("OK.", currentOptions)
                history = addCommandToVisibleCommandHistory(history, currentInput)
        except:
            currentInstruction = getInstructions("Bad input!", currentOptions)
        finally:
            printScreen(board, history, currentInstruction)

run()
