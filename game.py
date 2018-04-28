import math

class Game:
    def __init__(self, player0, player1):
        self.board = [
            None, None, None,
            None, None, None,
            None, None, None
        ]
        self.players = [player0, player1]
        self.winner = None

        self.isTurnPlayer0 = True

    WIN_CONDITIONS = [
        [0,1,2], #rows
        [3,4,5],
        [6,7,8],
        [0,3,6], #columns
        [1,4,7],
        [2,5,8],
        [0,4,8], #crosses
        [2,4,6]
    ]

    def runGame(self):
        while self.whoWon(self.board) is None and self.spacesAreOpen(self.board):
            self.doTurn()
        return self.whoWon(self.board)

    def doTurn(self):
        boardIndex = self.currentPlayer().getMove(self.board, self.currentPlayerIndex())
        if self.isMoveValid(self.board, boardIndex):
            self.makeMove(boardIndex)
            self.nextPlayer()
        else:
            print('Illegal move!', boardIndex)

    def makeMove(self, boardIndex):
        self.board[boardIndex] = self.currentPlayerIndex()

    def currentPlayer(self):
        return self.players[self.currentPlayerIndex()]

    def currentPlayerIndex(self):
        return 0 if self.isTurnPlayer0 else 1

    def nextPlayer(self):
        self.isTurnPlayer0 = not self.isTurnPlayer0

    @staticmethod
    def spacesAreOpen(board):
        for space in board:
            if space is None:
                return True
        return False

    @staticmethod
    def whoWon(board):
        for winCondition in Game.WIN_CONDITIONS:
            winner = Game.evalWinCondition(board, winCondition)
            if winner is not None:
                return winner

    @staticmethod
    def evalWinCondition(board, winCondition):
        if board[winCondition[0]] is not None and \
            board[winCondition[0]] == board[winCondition[1]] and \
            board[winCondition[0]] == board[winCondition[2]]:
            return board[winCondition[0]]
        return None

    @staticmethod
    def isMoveValid(board, boardIndex):
        try:
            if not (0 <= boardIndex <= 8):
                return False
            return board[boardIndex] is None
        except:
            return False

    @staticmethod
    def printBoard(board):
        string = ''
        for i, space in enumerate(board):
            string += str(space)+' ' if space is not None else '_ '
            if i % 3 == 2:
                print(string)
                string = ''
