import numpy as np
from game import Game

class QTableBot:
    def __init__(self):
        self.learningRate = .2
        self.discountFactor = .9
        self.noiseFactor = 100
        self.qTable = np.zeros([19682,9])
        #? right number of states? huge gains for symetry here. (-1 for zero index)
        # -> 3^9  None,0,1 / base 3 -- 00,01,02,10,11,12,20,21,22... No symetry.
        #    2^18 (IsMine, IsTheirs)


    def getMove(self, board, whichPlayerAmI):
        currentState = self.getState(board)
        ignoranceFactor = self.noiseFactor / (np.sum(np.abs(self.qTable)) + 1) # Less noise as table gets filled in
        noise = np.random.randn(9)
        noise *= ignoranceFactor

        # print('qsum', np.sum(np.abs(self.qTable)))
        # print('state', currentState)
        # print('ignorance', ignoranceFactor)
        # print('noise', noise)

        weightedActions = currentState + noise
        maxAction = max([x for i, x in enumerate(weightedActions) if board[i] is None])
        for move, score in enumerate(weightedActions):
            if score == maxAction:
                return move

    def updateQTable(self, board, move, whichPlayerAmI, reward):
        nextBoard = board[:]
        nextBoard[move] = whichPlayerAmI
        if Game.whoWon(nextBoard) == whichPlayerAmI:
            newQ = 1
        else:
            existingQ = self.getState(board)[move]
            futureReward = -1 * max(self.getState(nextBoard)) # inverse, since giving oponent chance to take reward
            newQ = ((1 - self.learningRate)* existingQ) + self.learningRate*(reward + self.discountFactor*futureReward)
            # current state - discounted oponents reward
        self.qTable[self.getBoardIndex(board)][move] = newQ

    def reportWin(self, game, whichPlayerAmI):
        self.reportReward(game, whichPlayerAmI, 1)

    def reportLoss(self, game, whichPlayerAmI):
        self.reportReward(game, whichPlayerAmI, -1)

    def reportDraw(self, game, whichPlayerAmI):
        self.reportReward(game, whichPlayerAmI, 0)

    def reportReward(self, game, whichPlayerAmI, reward):
        moves = game.moveHistory
        board = game.board[:]
        for move in reversed(moves):
            board[move] = None
            self.updateQTable(board, move, whichPlayerAmI, reward)
            reward = -1 * self.discountFactor * reward # invert for minmax
            whichPlayerAmI = 1 - whichPlayerAmI # is this right?
        # or never invert, play all the way through with same reward? then re-run for opponents moves
        # I think inversion is needed, since I only care about a score for the user that has agency.
        #       score for move where whichPlayerAmI can't make move is useless.

    @staticmethod
    def getBoardIndex(board):
        ternaryIndexString = ''
        for space in board:
            ternaryIndexString += '0' if space is None else str(space + 1) # +1 to change players 0,1 to 1,2
        return int(ternaryIndexString, 3) # string base 3 to int base 10 index

    def getState(self, board):
        stateIndex = self.getBoardIndex(board)
        return self.qTable[stateIndex]

    def playSelf(self, rounds=10000):
        print('training for', rounds, 'rounds')
        for i in range(0,rounds):
            if i%(rounds/(rounds/500)) == 0:
                print((i/rounds)*100, '% done')
                print('solution space', np.sum(np.abs(self.qTable)))
                print(self.noiseFactor / (np.sum(np.abs(self.qTable)) + 1))
                print(self.qTable[0])
            game = Game(self, self, True)
            winner = game.runGame()
            if winner is None:
                self.reportDraw(game,0)
                self.reportDraw(game,1)
            else:
                winnerIndex = game.whoWon(game.board)
                self.reportWin(game, winnerIndex)
                self.reportLoss(game, 1 - winnerIndex)
