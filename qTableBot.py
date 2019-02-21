import numpy as np
from game import Game

class QTableBot:
    def __init__(self):
        self.learningRate = .4
        self.discountFactor = .75
        self.qTable = np.zeros([19682,9])
        #? right number of states? huge gains for symetry here. (-1 for zero index)
        # -> 3^9  None,0,1 / base 3 -- 00,01,02,10,11,12,20,21,22... No symetry.
        #    2^18 (IsMine, IsTheirs)
        noveltyFactor = .5  # random weight for unexplored moves
        self.noveltyTable = self.qTable[:] + noveltyFactor # how novel a move is. More novelty invites more noise
        self.noveltyDiminishment = .05
        self.noiseFactorBoost = .08
        self.nonPerfectLeak = .01

    def getMove(self, board, whichPlayerAmI):
        currentState = self.getState(board)
        noise = np.random.randn(9)
        noise *= self.getNoveltyState(board) + self.noiseFactorBoost # nFB so there's always some noise
        weightedActions = currentState + noise

        # print('state', currentState)
        # print('novelty', self.getNoveltyState(board))
        # print('noise', noise)
        # print('weighted', weightedActions)

        maxAction = max([x for i, x in enumerate(weightedActions) if board[i] is None])
        for move, score in enumerate(weightedActions):
            if score == maxAction:
                return move

    def reportGame(self, game):
        winner = game.whoWon(game.board)
        if winner is None:
            self.reportDraw(game)
        else:
            self.reportWin(game, winner)
            # inherently reports loss for previous move of previous player, game can never end on a losing move

    def reportWin(self, game, winner):
        self.reportReward(game, winner, 1)
        # input('winReported')

    def reportDraw(self, game):
        self.reportReward(game, 0, 0) # player 0 always plays last move in a draw

    def reportReward(self, game, whichPlayerAmI, reward):
        moves = game.moveHistory
        board = game.board[:]
        for move in reversed(moves):
            board[move] = None
            self.updateQTable(board, move, whichPlayerAmI, reward)
            # reward = 0 #only count reward for first move? let minmax propogate the rest
            reward = -1 * self.discountFactor * reward # invert for minmax
            whichPlayerAmI = 1 - whichPlayerAmI # alternate turns

    def updateQTable(self, board, move, whichPlayerAmI, reward):
        self.visitNoveltyTable(board, move)
        nextBoard = board[:]
        nextBoard[move] = whichPlayerAmI
        nextBoardState = self.getState(nextBoard)
        legalNextBoardState = [x for i,x in enumerate(nextBoardState) if board[i] is None]
        existingQ = self.getState(board)[move]
        nextReward = (max(legalNextBoardState) + np.mean(legalNextBoardState) * self.nonPerfectLeak)
        # inverse, since giving oponent chance to take reward. Leaks non-perfect play.
        newQ = ((1 - self.learningRate)* existingQ) + self.learningRate*(reward - self.discountFactor*nextReward)
        # existingQ + (current state - discounted oponents next reward)
        # print('qChange', self.qTable[self.getBoardIndex(board)][move], newQ)
        self.qTable[self.getBoardIndex(board)][move] = newQ

    def visitNoveltyTable(self, board, move):
        self.noveltyTable[self.getBoardIndex(board), move]  /= 1 + self.noveltyDiminishment

    @staticmethod
    def getBoardIndex(board):
        ternaryIndexString = ''
        for space in board:
            ternaryIndexString += '0' if space is None else str(space + 1) # +1 to change players 0,1 to 1,2
        return int(ternaryIndexString, 3) # string base 3 to int base 10 index

    def getState(self, board):
        stateIndex = self.getBoardIndex(board)
        return self.qTable[stateIndex]

    def getNoveltyState(self, board):
        stateIndex = self.getBoardIndex(board)
        return self.noveltyTable[stateIndex]

    def playSelf(self, rounds=10000):
        print('training for', rounds, 'rounds')
        for i in range(0,rounds):
            if i%(rounds/(rounds/500)) == 0:
                print((i/rounds)*100, '% done')
                print('solution space', np.sum(np.abs(self.qTable)))
                print('novelty space', np.sum(self.noveltyTable))
                print(self.qTable[0])
                print(self.noveltyTable[0])
            game = Game(self, self)
            winner = game.runGame()
            self.reportGame(game)
