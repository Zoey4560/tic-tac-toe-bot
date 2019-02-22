import random
import tensorflow
import numpy as np
import tensorflow as tf
from game import Game

class QNetworkBot:
    def __init__(self):
        self.minibatchSize = 16
        self.discountFactor = 0.8
        self.maxMemorySize = 1000
        self.replayMemory = []

        self.net = tf.keras.models.Sequential()
        self.net.add(tf.keras.layers.Dense(32, input_shape=(18,), activation='sigmoid'))
        self.net.add(tf.keras.layers.Dense(12, activation='relu'))
        self.net.add(tf.keras.layers.Dense(9, activation='sigmoid'))
        self.net.compile(optimizer='sgd', loss='mse')

    def fire(self, board, whichPlayerAmI):
        return self.net.predict(np.array([self.boardToInputs(board, whichPlayerAmI)]))[0]

    @staticmethod
    def boardToInputs(board, whichPlayerAmI):
        inputList = []
        for space in board:
            inputList.append(1 if whichPlayerAmI is space else 0)
            inputList.append(1 if 1 - whichPlayerAmI is space else 0)
        return inputList

    def getMove(self, board, whichPlayerAmI):
        if random.random() > min(0.95, len(self.replayMemory)/self.maxMemorySize):
            while True:
                randomPosition = random.randint(0,8)
                if Game.isMoveValid(board, randomPosition):
                    return randomPosition
        q = self.fire(board, whichPlayerAmI)
        maxResult = max([x for i, x in enumerate(q) if board[i] is None])
        for move, r in enumerate(q):
            if r == maxResult and board[move] is None:
                return move
        raise Exception('NO MOVE!')

    def reportGame(self, game):
        winner = game.whoWon(game.board)
        if winner is None:
            self.reportDraw(game)
        else:
            self.reportWin(game, winner)
        self.trainMiniBatch()

    def reportWin(self, game, winner):
        self.reportReward(game, winner, 1)

    def reportDraw(self, game):
        self.reportReward(game, 0, 0) # player 0 always plays last move in a draw.

    def reportReward(self, game, whichPlayerAmI, reward):
        moves = game.moveHistory
        board = game.board[:]
        isTerminal = True
        for move in reversed(moves):
            board[move] = None
            self.storeReplay(board, move, whichPlayerAmI, reward, isTerminal)
            isTerminal = False
            reward = 0 # only reward for winning move
            whichPlayerAmI = 1 - whichPlayerAmI # alternate turns

    def trainMiniBatch(self):
        minibatch = random.sample(self.replayMemory, min(len(self.replayMemory), self.minibatchSize))
        inputs = []
        desiredOutputs = []
        for replay in minibatch:
            inputs.append(self.boardToInputs(replay.state, replay.playerIndicator))
            q = self.qSolve(replay)
            existingQ = self.fire(replay.state, replay.playerIndicator)
            existingQ[replay.action] += q
            desiredOutputs.append(existingQ)
        inputs = np.array(inputs)
        desiredOutputs = np.array(desiredOutputs)
        if desiredOutputs.size != 0:
            self.net.train_on_batch(inputs, desiredOutputs)

    def qSolve(self, replay):
        # q = r + γQ∗(s', a')
        r = replay.reward
        if replay.isTerminal:
            return r
        else:
            maxQ = max(self.fire(replay.nextState, replay.playerIndicator)) # this is never a game state that we get to act on. storage for future expected reward
            oponentMaxQ =  max(self.fire(replay.nextState, 1 - replay.playerIndicator)) # best oponent can do with state we give them
            return r + self.discountFactor * (maxQ - oponentMaxQ)

    def storeReplay(self, board, move, whichPlayerAmI, reward, isTerminal):
        currentBoard = board[:]
        nextBoard = board[:]
        nextBoard[move] = whichPlayerAmI
        self.replayMemory.append(Replay(currentBoard, move, whichPlayerAmI, reward, nextBoard, isTerminal))
        if len(self.replayMemory) > self.maxMemorySize:
            self.replayMemory.pop(0)

class Replay:
    def __init__(self, state, action, playerIndicator, reward, nextState, isTerminal):
        self.state = state
        self.action = action
        self.playerIndicator = playerIndicator
        self.reward = reward
        self.nextState = nextState
        self.isTerminal = isTerminal

    def pr(self):
        print(self.state, self.action, self.reward, self.nextState, isTerminal)
