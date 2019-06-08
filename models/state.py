#!/usr/bin/python3
from models import CurrentGame


class State:
    """
    The State contains the data shared amongst all controllers.
    (The terminus is taken from Front End Development.)
    Do not confuse with the States as in state machine.
    """

    # This is the current state as in state machine.
    # We require activities because of the user interaction.
    activity: int = None

    # This is where feedback as text can be passed from
    # one controller to the other. Used to render results
    # to the console.
    feedback: str = ""

    # This contains the CurrentGame data and engine.
    game: CurrentGame = None
