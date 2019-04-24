import math
from copy import deepcopy
# http://www.python-kurs.eu/deep_copy.php


# class GameTreeAlgorithms:

# Testprogramm
def testSearch():
    #    read(n)
    n = 9
    print(n)
    gs = Nimstate()
    gs1 = gs.copyState()
    gs2 = gs.copyState()
    gs3 = gs.copyState()

    eval = NimEvaluator()

    print("Test minimax1")
    gs.setStartState(n, False)
    gs.print()
    # fuellen sie die liste
    f = minimax([])
    print("minimax value:", f)
    print("number of generated states:", gs.genStates)
    print("stateHistory:", gs.stateHistory)


#  Minimax-Verfahren:
#  Spiebaum wird als verschachtelte Listenstruktur uebergeben
def minimax(l):
    if (type(l) == list):
        a = -100
        n = len(l)
        print(range(n))
        for i in range(n):
            print(i)
            f = - minimax(l[i])
            if f > a:
                a = f
        return a
    else:
        return l


class Gamestate:

    def setStartState(self):
        raise NotImplementedError("You should have implemented this")

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


class Evaluator:

    def heuristicValue(self, gs):
        raise NotImplementedError("Not implemented")

    def simpleHeuristicValue(self, gs):
        raise NotImplementedError("Not implemented")

    def getMinValue(self):
        raise NotImplementedError("Not implemented")

    def getMaxValue(self):
        raise NotImplementedError("Not implemented")

    def exactValue(self, gs):
        raise NotImplementedError("Not implemented")

    def evaluate(self, gs):
        raise NotImplementedError("Not implemented")


class Nimstate(Gamestate):

    num = 0
    lastChildMv = 0
    nextChildMv = 1
    firstPlayerToMove = True
    history = []
    root = None
    stateHistory = []
    genStates = 0

    def _init_(self, x):
        self.num = x
        self.firstPlayerToMove = True

    def setStartState(self, x, firstPlayer):
        self.genStates = 1
        self.num = x
        self.lastChildMv = 0
        self.nextChildMv = 1
        self.firstPlayerToMove = firstPlayer
        self.history = []
        self.root = self
        self.stateHistory.append([])
        self.genStates = 1

    def getAllMoves(self):
        ls = []
        while self.hasNextMove():
            ls.append(self.getNextMove())
        return ls

    def possibleMove(self, mv):
        if 0 < mv and mv <= 3 and mv <= self.num:
            return True
        else:
            return False

    def hasNextMove(self):
        if (self.possibleMove(self.nextChildMv)):
            return True
        else:
            return False

    def getNextMove(self):
        if (self.hasNextMove()):
            self.lastChildMv += 1
            self.nextChildMv += 1
            return self.lastChildMv
        else:
            raise Exception(
                "Invalid Argument Exception: no admissible move available")

    def doMove(self, mv):
        if self.possibleMove(mv):
            self.genStates += 1
            self.num -= mv
            self.lastChildMv = 0
            self.nextChildMv = 1
            self.firstPlayerToMove = not self.firstPlayerToMove
            self.history.append(mv)
            self.stateHistory.append(deepcopy(self.history))
#             print(self.stateHistory)
            if not (self == self.root):
                self.root.genStates += 1
                self.root.stateHistory.append(deepcopy(self.history))

        else:
            raise Exception("Invalid Argument Exception: no possible move")

    def doNextMove(self):
        self.doMove(self.nextChildMv)

    def undoMove(self):
        if 0 < len(self.history):
            mv = self.history.pop()
            self.num += mv
            self.lastChildMv = mv
            self.nextChildMv = self.lastChildMv + 1
            self.firstPlayerToMove = not self.firstPlayerToMove
        else:
            raise Exception("Invalid Argument Exception: history is empty")

    def getAllChildStates(self):
        mvList = self.getAllMoves()
        childList = []
        n = len(mvList)
        for i in range(n):
            childList.append(self.childState(mvList[i]))
        return childList

    def hasNextChild(self):
        return self.hasNextMove()

    def getNextChild(self):
        mv = self.getNextMove()
        return self.childState(mv)

    def getChild(self, mv):
        if self.possibleMove(mv):
            return self.childState(mv)
        else:
            raise Exception("Invalid Argument Exception: no possible move")

    def getFirstPlayerToMove(self):
        return self.firstPlayerToMove

    def secondPlayerToMove(self):
        return not self.firstPlayerToMove

    def isTerminal(self):
        if (self.num == 0):
            return True
        else:
            return False

    def firstPlayerToWin(self):
        return not self.firstPlayerToMove()

    def secondPlayerToWin(self):
        return self.firstPlayerToMove()

    def draw(self):
        return False

    def getMoveHistory(self):
        return self.history  # without copy

    def getStateHistory(self):
        return self.stateHistory  # without copy

    def copyState(self):
        gs = Nimstate()
        gs.num = self.num
        gs.lastChildMv = self.lastChildMv
        gs.nextChildMv = self.nextChildMv
        gs.firstPlayerToMove = self.firstPlayerToMove
#        gs.history = deepcopy(self.history)   #deep copy
        gs.history = self.history[:]  # shallow copy
        gs.stateHistory = deepcopy(self.stateHistory)
        gs.root = self.root
        return gs

    def childState(self, mv):
        if self.possibleMove(mv):
            child = self.copyState()
            child.doMove(mv)
            return child
        else:
            return None

    def equalState(self, other):
        if not self.num == other.num:
            return False
        elif not self.lastChildMv == other.lastChildMv:
            return False
        elif not self.nextChildMv == other.nextChildMv:
            return False
        elif not self.firstPlayerToMove == other.firstPlayerToMove:
            return False
        elif not self.equalList(self.history, other.history):
            return False
        else:
            return True

    def print(self):
        print(self)
        print(self.num)
        print(self.lastChildMv)
        print(self.nextChildMv)
        print(self.firstPlayerToMove)
        print(self.history)
        print(self.stateHistory)
        print(self.root)

    def equalList(self, l1, l2):
        if not len(l1) == len(l2):
            return False
        else:
            n = len(l1)
            for i in range(n):
                if not l1[i] == l2[i]:
                    return False
            return True


class NimEvaluator(Evaluator):

    def heuristicValue(self, gs):
        if not (isinstance(gs, Nimstate)):
            raise Exception("Illegal Argument")
        else:
            if (gs.num % 4 == 0):
                return -1
            else:
                return 1

    def getMinValue(self):
        return -1

    def getMaxValue(self):
        return 1

    def exactValue(self, gs):
        if not (isinstance(gs, Nimstate)):
            raise Exception("Illegal Argument")
        else:
            if (gs.num % 4 == 0):
                return -1
            else:
                return 1

    def evaluate(self, gs):
        if not (isinstance(gs, Nimstate)):
            raise Exception("Illegal Argument")
        else:
            if (gs.num % 4 == 0):
                return -1
            else:
                return 1
