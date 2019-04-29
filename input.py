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

def getInput(options):
    command = sys.stdin.readline()
    cleaned = command.replace("\n", "")
    if not cleaned in options.keys():
        raise "Invalid input. "
    return cleaned

def isBordField(input):
    if len(input) == 2:
        p = re.compile('[A-Ea-e][0-4]')
        if p.match(input) is not None:
            return True
    return False
