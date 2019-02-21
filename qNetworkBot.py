import random
import tensorflow
import numpy as np
import tensorflow as tf
from game import Game

class QNetworkBot:
    def __init__(self):
        self.minibatchSize = 5
        self.traningEpochs = 10
        self.discountFactor = 0.5
        self.maxMemorySize = 1000
        self.replayMemory = []

        self.net = tf.keras.models.Sequential()
        self.net.add(tf.keras.layers.Dense(8, input_shape=(18,) ))
        self.net.add(tf.keras.layers.Dense(9))
        self.net.compile(optimizer='sgd', loss='mse')

    def fire(self, board):
        inputList = []
        for space in board: #code even, odd inputs to each player
            inputList.append(1 if 0 is space else 0)
            inputList.append(1 if 1 is space else 0)
        inputs = np.array([inputList])
        return self.net.predict(inputs)[0]

    def getMove(self, board, whichPlayerAmI):
        while True:
            randomPosition = random.randint(0,8)
            if Game.isMoveValid(board, randomPosition):
                return randomPosition

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
        self.reportReward(game, 0, 0) # player 0 always plays last move in a draw

    def reportReward(self, game, whichPlayerAmI, reward):
        moves = game.moveHistory
        board = game.board[:]
        for move in reversed(moves):
            board[move] = None
            self.storeReplay(board, move, whichPlayerAmI, reward)
            reward = 0 # only reward for winning move
            whichPlayerAmI = 1 - whichPlayerAmI # alternate turns

    def trainMiniBatch(self):
        minibatch = random.sample(self.replayMemory, self.minibatchSize)
        inputs = []
        desired_outputs = []
        for replay in minibatch:
            inputs.append(replay.state)
            # q = r + γQ∗(s', a')
            r = replay.reward
            q = self.fire(replay.nextState)
            print('r,q: ',r,q, r+q)
            input()
            


    def storeReplay(self, board, move, whichPlayerAmI, reward):
        nextBoard = board[:]
        nextBoard[move] = whichPlayerAmI
        self.replayMemory.append(Replay(board, move, reward, nextBoard))
        if len(self.replayMemory) > self.maxMemorySize:
            self.replayMemory.pop(0)

class Replay:
    def __init__(self, state, action, reward, nextState):
        self.state = state
        self.action = action
        self.reward = reward
        self.nextState = nextState