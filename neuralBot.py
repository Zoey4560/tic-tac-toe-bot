import numpy as np
from functools import reduce

class NeuralBot:
    def __init__(self):
        # assuming this is a good structure
        # 16 inputs, for 8 spaces: do I own, does enemy own
        # hidden layer of 8 nodes, 1 for each winning condition?
        # output of preference for move
        #   filters out invalid moves,
        #   so no incentive to not make illegal moves
        self.net = NeuralNetwork([18, 8, 9])

    def getMove(self, board, whichPlayerAmI):
        inputList = []
        for space in board:
            inputList.append(1 if whichPlayerAmI is space else 0)
            inputList.append(1 if 1 - whichPlayerAmI is space else 0)
        inputs = np.array(inputList)
        result = self.net.fire(inputs)
        maxResult = max([x for i, x in enumerate(result) if board[i] is None])
        for move, r in enumerate(result):
            if r == maxResult:
                return move

class NeuralNetwork:
    def __init__(self, layerList):
        self.layers = []
        for i in range(len(layerList)-1):
            layer = NeuralLayer(layerList[i], layerList[i+1])
            self.layers.append(layer)

    def fire(self, inputs):
        return reduce(lambda input, layer: layer.fire(input), self.layers, inputs)

class NeuralLayer:
    def __init__(self, numInputs, numNeurons):
        self.weights = np.random.random((numInputs,numNeurons))
        self.bias = np.random.random(numNeurons)

    def fire(self, inputs):
        return self.sigmoid(inputs @ self.weights * self.bias)

    @staticmethod
    def sigmoid(x):
        return 1 / (1 + np.exp(-x))
