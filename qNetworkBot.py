import random
import tensorflow
import numpy as np
import tensorflow as tf
from game import Game

class QNetworkBot:
    def __init__(self):
        self.minibatchSize = 128
        self.trainingEpochs = 2
        self.discountFactor = 0.5
        self.maxMemorySize = 10000
        self.replayMemory = []

        self.net = tf.keras.models.Sequential()
        self.net.add(tf.keras.layers.Dense(8, input_shape=(18,) ))
        self.net.add(tf.keras.layers.Dense(9, activation='sigmoid'))
        self.net.compile(optimizer='sgd', loss='mse')

    def fire(self, board):
        return self.net.predict(np.array([self.boardToInputs(board)]))[0]

    @staticmethod
    def boardToInputs(board):
        inputList = []
        for space in board: #code even, odd inputs to each player
            inputList.append(1 if 0 is space else 0)
            inputList.append(1 if 1 is space else 0)
        return inputList

    def getMove(self, board, whichPlayerAmI):
        if random.random() > min(0.95, len(self.replayMemory)/self.maxMemorySize):
            while True:
                randomPosition = random.randint(0,8)
                if Game.isMoveValid(board, randomPosition):
                    return randomPosition
        q = self.fire(board)
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
        self.reportReward(game, 0, 0.5) # player 0 always plays last move in a draw. Give partial value (better than loss)

    def reportReward(self, game, whichPlayerAmI, reward):
        moves = game.moveHistory
        board = game.board[:]
        for move in reversed(moves):
            board[move] = None
            self.storeReplay(board, move, whichPlayerAmI, reward)
            reward = 0 # only reward for winning move
            whichPlayerAmI = 1 - whichPlayerAmI # alternate turns

    def trainMiniBatch(self):
        minibatch = random.sample(self.replayMemory, min(len(self.replayMemory), self.minibatchSize))
        inputs = []
        desiredOutputs = []
        for replay in minibatch:
            inputs.append(self.boardToInputs(replay.state))
            # q = r + γQ∗(s', a')
            r = replay.reward
            maxQ = max(self.fire(replay.nextState))
            q = r + self.discountFactor * maxQ
            existingQ = self.fire(replay.state)
            existingQ[replay.action] += q
            desiredOutputs.append(existingQ)
        inputs = np.array(inputs)
        desiredOutputs = np.array(desiredOutputs)
        if desiredOutputs.size != 0:
            self.net.fit(inputs, desiredOutputs, epochs=self.trainingEpochs)


    def storeReplay(self, board, move, whichPlayerAmI, reward):
        currentBoard = board[:]
        nextBoard = board[:]
        nextBoard[move] = whichPlayerAmI
        self.replayMemory.append(Replay(currentBoard, move, reward, nextBoard))
        if len(self.replayMemory) > self.maxMemorySize:
            self.replayMemory.pop(0)

class Replay:
    def __init__(self, state, action, reward, nextState):
        self.state = state
        self.action = action
        self.reward = reward
        self.nextState = nextState

    def pr(self):
        print(self.state, self.action, self.reward, self.nextState)
