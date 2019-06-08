#!/usr/bin/python3


class Alquerque:
    """
    The game engine to play Alquerque.
    NOT REALLY IMPLEMENTED.
    """

    gamestate = []
    initialGamestate = [
        [-1, -1, -1, -1, -1],
        [-1, -1, -1, -1, -1],
        [-1, -1, 0, 1, 1],
        [1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1],
    ]
    gamestateHistory = []
    moveHistory = []

    def __init__(self):
        self.setStartState()

    def setStartState(self):
        """Initializes the gamestate. Void."""
        self.gamestate = self.initialGamestate
        return

    def getBord(self):
        """Returns the bord as an array."""
        return self.gamestate

    def getAllMoves(self):
        raise NotImplementedError("You should have implemented this")

    def possibleMove(self, mv):
        raise NotImplementedError("You should have implemented this")

    def hasNextMove(self):
        raise NotImplementedError("You should have implemented this")

    def getNextMove(self):
        raise NotImplementedError("You should have implemented this")

    def doMove(self, mv):
        raise NotImplementedError("You should have implemented this")

    def undoMove(self, mv):
        raise NotImplementedError("You should have implemented this")

    def getAllChildStates(self):
        raise NotImplementedError("You should have implemented this")

    def hasNextChild(self):
        raise NotImplementedError("You should have implemented this")

    def getNextChild(self):
        raise NotImplementedError("You should have implemented this")

    def getChild(self, mv):
        raise NotImplementedError("You should have implemented this")

    def firstPlayerToMove(self):
        raise NotImplementedError("You should have implemented this")

    def secondPlayerToMove(self):
        raise NotImplementedError("You should have implemented this")

    def isTerminal(self):
        raise NotImplementedError("You should have implemented this")

    def firstPlayerToWin(self):
        raise NotImplementedError("You should have implemented this")

    def secondPlayerToWin(self):
        raise NotImplementedError("Not implemented")

    def draw(self):
        raise NotImplementedError("Not implemented")

    def getMoveHistory(self):
        raise NotImplementedError("Not implemented")

    def getStateHistory(self):
        raise NotImplementedError("Not implemented")

    def printGameState(self):
        """
        3x3 field:
        +-+-+
        |\|/|
        +-+-+
        |/|\|
        +-+-+
        general:
        if (x+y)%2==1:
            "
                +-+
                |/|
                +-+
            "
        else:
            "
                +-+
                |\|
                +-+
            "

        one player -> x
        sec player -> o
        example start:
        x-x-x
        |\|/|
        x-+-o
        |/|\|
        o-o-o
        """
