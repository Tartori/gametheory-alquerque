#!/usr/bin/python3

import sys

from gui import *

def run():
    board = demoboard
    history = demohistory

    initialInstruction = "Hi! Enter your command:"
    printScreen(board, history, initialInstruction)

    going = True
    while going:
        command = sys.stdin.readline()
        cleaned = command.replace("\n", "")
        instruction = ""
        if (cleaned == "stop"):
            instruction = "Bye bye!"
            going = False
        else:
            if(len(history) > 3):
                history.pop(0)
            history.append(cleaned)
            instruction = "OK. Next one."
        printScreen(board, history, instruction)


run()
