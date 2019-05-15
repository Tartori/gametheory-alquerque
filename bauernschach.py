#!/usr/bin/python3

from definitions import Field, Player, FieldValue
from copy import deepcopy


class Bauernschach:

    gamestate = []
    gamestateHistory = []
    moveHistory = []
    currentPlayer = Player.USER
    currentlyPossibleMoves = []

    def __init__(self, size=8):
        self.size = size

    def start(self, player):
        self.moveHistory = []
        self.gamestateHistory = []
        self.set_start_state()
        self.currentPlayer = player
        self.findAllMoves()

    def toNextTurn(self):
        self.currentPlayer *= -1
        self.findAllMoves()

    def set_start_state(self):
        """Initializes the gamestate. Void."""
        if(self.size < 4):
            self.size = 4
        # https://stackoverflow.com/questions/9459337/assign-value-to-an-individual-cell-in-a-two-dimensional-python-array
        self.gamestate = [
            [0 for col in range(self.size)] for row in range(self.size)]
        self.gamestate[1] = [Player.OPP for col in range(self.size)]
        self.gamestate[self.size-2] = [Player.USER for col in range(self.size)]

    def getBord(self):
        """Returns the bord as an array."""
        return self.gamestate

    def getBordWithMoves(self, pawn):
        bordWithMoves = deepcopy(self.gamestate)
        movesForPawn = self.getMovesForPawn(pawn)
        for m in movesForPawn:
            bordWithMoves[m[0]][m[1]] = FieldValue.POSSIBLE_MOVE
        return bordWithMoves

    def findAllMoves(self):
        """
        For each pawn of the current player, finds all possible moves.
        return: void. (sets field)
        """
        self.currentlyPossibleMoves = {}
        for r in range(0, 8):
            for c in range(0, 8):
                movesForPawn = []

                isFinalRow = r == 0 or r == len(self.gamestate) - 1
                anyPlayer = [Player.USER, Player.OPP]
                isOccupied = self.gamestate[r][c] in anyPlayer
                if (isFinalRow and isOccupied):
                    raise Exception("Game is finished.")

                pawn = (r, c)

                # check if any pawn.
                if not self.fieldOccupiedByCurrentPlayer(pawn):
                    continue

                moveFront = (self.getAdvance(r), c)
                moveFrontTwo = (self.getAdvance(self.getAdvance(r)), c)
                moveFrontLeft = (self.getAdvance(r), self.getLeft(c))
                moveFrontRight = (self.getAdvance(r), self.getRight(c))

                # check if can move one straight ahead
                if self.canMoveFront(pawn, moveFront):
                    movesForPawn.append(moveFront)
                # check if can move two fields ahead
                if self.canMoveFrontTwo(pawn, moveFrontTwo):
                    movesForPawn.append(moveFrontTwo)
                # check if can jump an opp pawn to front-left
                if self.canMoveLeft(pawn, moveFrontLeft):
                    movesForPawn.append(moveFrontLeft)
                # check if can jump an opp pawn to front-right
                if self.canMoveRight(pawn, moveFrontRight):
                    movesForPawn.append(moveFrontRight)

                if len(movesForPawn) > 0:
                    self.currentlyPossibleMoves[pawn] = movesForPawn
        return

    def fieldOccupied(self, field):
        return self.gamestate[field[0]][field[1]] in [-1, 1]

    def fieldOccupiedByCurrentPlayer(self, field):
        return self.gamestate[field[0]][field[1]] == self.currentPlayer

    def fieldOccupiedByOpponent(self, field):
        """
        Checks if a field on the board is occupied by a pawn owned by the
        opposing player.
        field: (i, j) where i is rowindex and j is colindex.
        return: bool.
        """
        if self.currentPlayer == Player.USER:
            opponent = Player.OPP
        elif self.currentPlayer == Player.OPP:
            opponent = Player.USER
        return self.gamestate[field[0]][field[1]] == opponent

    def fieldOnBord(self, field):
        """
        Checks if the field is in the boundaries of the bord.
        field: (i, j) where i is rowindex and j is colindex.
        return: bool.
        """
        size = len(self.gamestate)
        return field[0] in range(0, size) and field[1] in range(0, size)

    def canMoveFront(self, pawn, move):
        """
        Checks if a pawn can move to the neighbouring field straight ahead on
        the bord.
        pawn: (i, j) where i is rowindex and j is colindex referencing the
        field of a pawn.
        move: (i, j) where i is rowindex and j is colindex referencing the
        field where the pawn wants to move to.
        return: bool.
        """
        return self.fieldOnBord(move) and not self.fieldOccupied(move)

    def canMoveFrontTwo(self, pawn, move):
        """
        Checks if a pawn can jump two field ahead on the bord. (only if has
        not yet moved, and both fields ahead unoccupied.)
        pawn: (i, j) where i is rowindex and j is colindex referencing the
        field of a pawn.
        move: (i, j) where i is rowindex and j is colindex referencing the
        field where the pawn wants to move to.
        return: bool.
        """
        isFirstMovementForPiece = False
        if self.currentPlayer == Player.USER:
            isFirstMovementForPiece = pawn[0] == len(self.gamestate) - 2
        if self.currentPlayer == Player.OPP:
            isFirstMovementForPiece = pawn[0] == 1
        bothFieldsFree = not self.fieldOccupied(
            (self.getBack(move[0]), move[1])) and not self.fieldOccupied(move)
        return self.fieldOnBord(move) and isFirstMovementForPiece and bothFieldsFree

    def canMoveLeft(self, pawn, move):
        """
        Checks if a pawn can move to the field diagonally left ahead by
        killing an opponent pawn.
        pawn: (i, j) where i is rowindex and j is colindex referencing the
        field of a pawn.
        move: (i, j) where i is rowindex and j is colindex referencing the
        field where the pawn wants to move to.
        return: bool.
        """
        return self.fieldOnBord(move) and self.fieldOccupiedByOpponent(move)

    def canMoveRight(self, pawn, move):
        """
        Checks if a pawn can move to the field diagonally right ahead by
        killing an opponent pawn.
        pawn: (i, j) where i is rowindex and j is colindex referencing the
        field of a pawn.
        move: (i, j) where i is rowindex and j is colindex referencing the
        field where the pawn wants to move to.
        return: bool.
        """
        return self.fieldOnBord(move) and self.fieldOccupiedByOpponent(move)

    def getMovablePawns(self):
        return self.currentlyPossibleMoves.keys()

    def getMovesForPawn(self, pawn):
        moves = self.currentlyPossibleMoves.get(pawn)
        return moves

    def canBeMoved(self, pawn):
        return pawn in self.getMovablePawns()

    def possibleMove(self, pawn, move):
        """
        Checks if a pawn can move to a certain field.
        pawn: (i, j) where i is rowindex and j is colindex referencing the field of a pawn.
        move: (i, j) where i is rowindex and j is colindex referencing the field where the pawn wants to move to.
        return: bool.
        """
        return self.canMoveFront(pawn, move) or self.canMoveLeft(pawn, move) or self.canMoveRight(pawn, move)

    def hasNextMove(self):
        """
        Checks if the current player can make any move.
        return: bool.
        """
        return len(self.currentlyPossibleMoves) > 0

    def getNextMove(self):
        raise NotImplementedError("You should have implemented this")

    def doMove(self, pawn, move):
        """
        Updates the gamestate by performing the move with the pawn. Saves the previous gamestate and the move in the respective history.
        pawn: (i, j) where i is rowindex and j is colindex referencing the field of a pawn.
        move: (i, j) where i is rowindex and j is colindex referencing the field where the pawn wants to move to.
        return: void.
        """
        if self.possibleMove(pawn, move):
            self.gamestateHistory.append(deepcopy(self.gamestate))
            self.moveHistory.append((deepcopy(pawn), deepcopy(move)))
            self.gamestate[pawn[0]][pawn[1]] = 0
            self.gamestate[move[0]][move[1]] = self.currentPlayer

    def undoMove(self, mv):
        raise NotImplementedError("You should have implemented this")

    def isTerminal(self):
        return self.Player1ToWin() or self.Player2ToWin()

    def Player1ToWin(self):
        return Player.USER in self.gamestate[0]

    def Player2ToWin(self):
        return Player.OPP in self.gamestate[7]

    def getMoveHistory(self):
        return self.moveHistory

    def getStateHistory(self):
        return self.gamestateHistory

    def getLeft(self, rowIndex):
        return rowIndex + self.currentPlayer * -1

    def getRight(self, rowIndex):
        return rowIndex + self.currentPlayer

    def getAdvance(self, colIndex):
        return colIndex + self.currentPlayer * -1

    def getBack(self, colIndex):
        return colIndex + self.currentPlayer
