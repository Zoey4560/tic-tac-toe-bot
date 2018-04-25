import math

class Game:
    def __init__(self, player0, player1):
        self.board = [
            [None,None,None],
            [None,None,None],
            [None,None,None]
        ]
        self.players = [player0, player1]
        self.winner = None

        self.isTurnPlayer0 = True

    def startGame(self):
        while self.whoWon() is None and self.spacesAreOpen():
            self.doTurn()
        return self.whoWon()

    def doTurn(self):
        position = self.currentPlayer().getMove(self.board, self.currentPlayerIndex())
        if self.isMoveValid(self.board, position):
            self.makeMove(position)
            self.nextPlayer()
        else:
            print('Illegal move!', position)

    def makeMove(self, position):
        self.board[position[0]][position[1]] = self.currentPlayerIndex()

    def currentPlayer(self):
        return self.players[self.currentPlayerIndex()]

    def currentPlayerIndex(self):
        return 0 if self.isTurnPlayer0 else 1

    def nextPlayer(self):
        self.isTurnPlayer0 = not self.isTurnPlayer0

    def spacesAreOpen(self):
        for row in self.board:
            for item in row:
                if item is None:
                    return True

    def whoWon(self):
        players = [0,1]
        for player in players:
            #check each row
            for row in self.board:
                if row[0] == player and row[1] == player and row[2] == player:
                    return player
            #check each column
            for rowNum in [0,1,2]:
                if self.board[0][rowNum] == player and self.board[1][rowNum] == player and self.board[2][rowNum] == player:
                    return player
            #check each cross
            if self.board[0][0] == player and self.board[1][1] == player and self.board[2][2] == player:
                return player
            if self.board[0][2] ==  player and self.board[1][1] == player and self.board[2][0] == player:
                return player
        return None



    @staticmethod
    def isMoveValid(board, position):
        if not (0 <= position[0] <= 2 and 0 <= position[1] <= 2):
            return False
        return board[position[0]][position[1]] is None

    #for transfroming between [x,y] board coordinates and 0-8 position
    @staticmethod
    def positionToNumeral(position):
        return (position[0])*3 + position[1]

    @staticmethod
    def numeralToPosition(numeral):
        return [math.floor(numeral/3), numeral % 3]
