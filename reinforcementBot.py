import numpy as np
import tensorflow as tf
from game import Game
from randomBot import RandomBot

class ReinforcementBot:
    def __init__(self):
        self.discountFactor = 0.9
        self.buildNet()
        self.observeGames(1000, 100)

    def buildNet(self):
        self.net = tf.keras.models.Sequential()
        self.net.add(tf.keras.layers.Dense(36, input_shape=(18,)))
        self.net.add(tf.keras.layers.Dense(18, activation='sigmoid'))
        # self.net.add(tf.keras.layers.GaussianNoise(1))
        self.net.add(tf.keras.layers.Dense(9))
        self.net.compile(optimizer=tf.keras.optimizers.SGD(0.5), loss='mse', metrics=['accuracy'])

    def observeGames(self, numberOfGames=1000, qEpochs=100):
        games = []
        states = []
        nextStates = []
        actions = []
        rewards = []
        r = RandomBot()
        for gameI in range(numberOfGames):
            print(gameI, 'observing')
            g = Game(r, r)
            g.runGame()
            winner = g.whoWon(g.board)
            reward = 1 if winner is not None else 0
            board = g.board[:]
            for move in reversed(g.moveHistory):
                nextStates.append(self.boardToInputs(board))
                board[move] = None
                states.append(self.boardToInputs(board))
                actions.append(move)
                rewards.append(reward)
                reward = None #only reward for ending move
                #None here lets us tell between `0` as:
                # "game ended in draw", and
                # "game still going, no reward--take -1 * max(q')"
                self.fire(board)
        for qEpochI in range(qEpochs):
            print(qEpochI, 'qEpoch')
            outputs = self.net.predict(np.array(states))
            for i, o in enumerate(outputs):
                r = rewards[i]
                if r is None:
                    r = -1 * self.discountFactor * max(nextStates[i])
                o[actions[i]] = r
                # np.array for acts in place
            self.net.fit(np.array(states), outputs, epochs=1)



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
        q = self.fire(board)
        maxResult = max([x for i, x in enumerate(q) if board[i] is None])
        for move, r in enumerate(q):
            if r == maxResult and board[move] is None:
                return move
        raise Exception('NO MOVE!')
