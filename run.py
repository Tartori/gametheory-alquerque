#!/usr/bin/python3

# TODO: snake case.
# TODO: do not import *. do "import ..." instead of "from ... import ..."

import sys
import re

from gui import *
from input import *
from bauernschach import *
from alquerque import *

ALQUERQUE = 0
BAUERNSCHACH = 1

# TODO: make Enum!
STATE_CHOOSE_GAME = 0
STATE_CHOOSE_PLAYER_ORDER = 1
STATE_CHOOSE_PAWN = 2
STATE_CHOOSE_MOVE = 3
STATE_SWITCH_TURN = 4
STATE_WIN = 5
STATE_BYE = -1

CMD_QUIT_APP = "STOP"
CMD_CHOOSE_GAME_ALQUERQUE = "A"
CMD_CHOOSE_GAME_BAUERNSCHACH = "B"
CMD_CHOOSE_FIRST_PLAYER_ME = "ME"
CMD_CHOOSE_FIRST_PLAYER_OPPONENT = "OPP"


class App:
    """
    Contains the loop of printing to screen, getting user input, and interacting with the game logic.
    Is agnostic of the specific game (as long as game implements required methods).

    Attributes:
        loopState               Contains the state as in a automaton.
        feedback                A string containing feedback to be shown to the user when entering the next state.
        game                    References the game instance that contains all game logic.
        selectedPawn            Describes the currently selected pawn in format A0.
        selectedMove            Describes the currently selected move for the selected pawn in format A0.
    """
    loopState = STATE_CHOOSE_GAME
    currentGameId = None
    feedback = None
    game = None
    history = []
    """Pawn in format A0."""
    selectedPawn = None
    selectedMove = None

    sharedOptions = {
        CMD_QUIT_APP: "stops app",
    }

    def __init__(self):
        pass

    def loop(self):
        """
        The main method of the whole application.
        Contains the loop of the user interacting with the application.

        return: void.
        """
        while True:
            try:
                if self.loopState == STATE_CHOOSE_GAME:
                    self.doStepChooseGame()
                    continue
                elif self.loopState == STATE_CHOOSE_PLAYER_ORDER:
                    self.do_step_choose_player_order()
                    continue
                elif self.loopState == STATE_CHOOSE_PAWN:
                    self.doStepChoosePawn()
                    continue
                elif self.loopState == STATE_CHOOSE_MOVE:
                    self.doStepChooseMove()
                    continue
                elif self.loopState == STATE_WIN:
                    self.doStepWin()
                    continue
                elif self.loopState == STATE_BYE:
                    self.doStepBye()
                    break
            except:
                pass

    def doStepChooseGame(self):
        params = ScreenParameters(
            bord=[],
            moveHistory=[],
            currentPlayer=None,
            feedback=self.consumeFeedback(),
            question="Hi! Which game would you like to play?",
            options=deepcopy(self.sharedOptions)
        )
        params.options.update({
            CMD_CHOOSE_GAME_ALQUERQUE: "play Alquerque",
            CMD_CHOOSE_GAME_BAUERNSCHACH: "play Bauernschach",
        })

        prefix = self.prependFeedback("Hi! Which game would you like to play?")
        printScreen([], [], getInstructions(prefix, params.options))

        input = self.readInput()

        if input == CMD_QUIT_APP:
            self.feedback = None
            self.loopState = STATE_BYE
            return

        elif input == CMD_CHOOSE_GAME_ALQUERQUE:
            self.game = Alquerque()
            self.loopState = STATE_CHOOSE_PLAYER_ORDER
            self.feedback = "You have chosen to play Alquerque."
            return

        elif input == CMD_CHOOSE_GAME_BAUERNSCHACH:
            self.game = Bauernschach(8)
            self.loopState = STATE_CHOOSE_PLAYER_ORDER
            self.feedback = "You have chosen to play Bauernschach."
            return

        else:
            self.feedback = "Bad input! "
            return

    def prependFeedback(self, prefix):
        if not self.feedback is None and len(self.feedback) > 0:
            prefix = self.feedback + " " + prefix
            self.feedback = None
        return prefix

    def consumeFeedback(self):
        if not self.feedback is None:
            return self.feedback
            self.feedback = None
        return None

    def readInput(self):
        """
        Gets the user input. Cleans out any line breaks and ensures is in upper case.
        return: String of user input.
        """
        try:
            # Remove end of line char.
            return sys.stdin.readline().strip().upper()
        except:
            return ""

    def do_step_choose_player_order(self):
        params = ScreenParameters(
            bord=[],
            moveHistory=[],
            currentPlayer=None,
            feedback=self.consumeFeedback(),
            question="Hi! Which game would you like to play?",
            options=deepcopy(self.sharedOptions)
        )
        params.options.update({
            CMD_CHOOSE_FIRST_PLAYER_ME: "if you want to start",
            CMD_CHOOSE_FIRST_PLAYER_OPPONENT: "if opponent shall start",
        })
        prefix = self.prependFeedback("Which player shall start first?")
        printScreen([], [], getInstructions(prefix, params.options))

        input = self.readInput()

        if input == CMD_QUIT_APP:
            self.feedback = None
            self.loopState = STATE_BYE
            return

        elif input == CMD_CHOOSE_FIRST_PLAYER_ME:
            self.game.start(PLAYER_USER)
            self.loopState = STATE_CHOOSE_PAWN
            self.feedback = self.whosTurnItIs()
            return

        elif input == CMD_CHOOSE_FIRST_PLAYER_OPPONENT:
            self.game.start(PLAYER_OPP)
            self.loopState = STATE_CHOOSE_PAWN
            self.feedback = self.whosTurnItIs()
            return

        else:
            self.feedback = "Bad input! "
            return

    def doStepChoosePawn(self):
        params = ScreenParameters(
            bord=self.game.getBord(),
            moveHistory=self.game.getMoveHistory(),
            currentPlayer=None,
            feedback=self.consumeFeedback(),
            question="Hi! Which game would you like to play?",
            options=deepcopy(self.sharedOptions)
        )
        params.options.update(self.getChoosableFieldsAsOptions(
            self.game.getMovablePawns()))
        prefix = self.prependFeedback("Which pawn do you want to move? ")
        printScreen(self.game.gamestate, self.game.getMoveHistory(),
                    getInstructions(prefix, params.options))

        input = self.readInput()

        if input == CMD_QUIT_APP:
            self.feedback = None
            self.loopState = STATE_BYE
            return

        elif input in params.options:
            self.selectedPawn = input
            self.loopState = STATE_CHOOSE_MOVE
            self.feedback = "You want to move pawn " + input + ". "
            return

        else:
            self.feedback = "Bad input! "
            return

    def doStepChooseMove(self):
        params = ScreenParameters(
            bord=self.game.getBord(),
            moveHistory=self.game.getMoveHistory(),
            currentPlayer=None,
            feedback=self.consumeFeedback(),
            question="Hi! Which game would you like to play?",
            options=deepcopy(self.sharedOptions)
        )
        pawnField = mapFieldTextToCoordinates(self.selectedPawn)
        params.options.update(self.getChoosableFieldsAsOptions(
            self.game.getMovesForPawn(pawnField)))
        prefix = self.prependFeedback("Where would you like to move the pawn?")
        printScreen(self.game.getBordWithMoves(
            pawnField), self.game.getMoveHistory(), getInstructions(prefix, params.options))

        input = self.readInput()

        if input == CMD_QUIT_APP:
            self.feedback = None
            self.loopState = STATE_BYE
            return

        elif input in params.options:
            self.selectedMove = input
            pawn = mapFieldTextToCoordinates(self.selectedPawn)
            move = mapFieldTextToCoordinates(input)
            self.game.doMove(pawn, move)
            self.history.append("Player " + str(self.game.currentPlayer) +
                                " moved " + self.selectedPawn + " to " + input)

            if self.game.isTerminal():
                self.loopState = STATE_WIN
                self.feedback = "Game finished. "
                self.selectedMove = None
                self.selectedPawn = None
                return
            else:
                self.game.toNextTurn()
                self.loopState = STATE_CHOOSE_PAWN
                return

        else:
            self.feedback = "Bad input! "
            return

    def doStepBye(self):
        printScreen([], [], getInstructions("Bye bye!", {}))
        return

    def doStepWin(self):
        if self.game.Player1ToWin():
            self.feedback = "You have won. Congrats! "
        else:
            self.feedback = "Opponent has won. Better luck next time. "
        self.loopState = STATE_CHOOSE_GAME

    def whosTurnItIs(self):
        if self.game.currentPlayer == PLAYER_USER:
            return "Your turn! "
        else:
            return "Opp's turn! "

    def getChoosableFieldsAsOptions(self, fields):
        fieldNames = mapFieldsCoordinatesToText(fields)
        options = {}
        for f in fieldNames:
            options[f] = ""
        return options


# Run the application.
if __name__ == "__main__":
    App().loop()
