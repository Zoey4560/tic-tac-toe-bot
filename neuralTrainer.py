import math
import random
import copy
import time
import pickle
import statistics
from game import Game
from neuralBot import NeuralBot
from randomBot import RandomBot

class NeuralTrainer:
    def __init__(self, populationSize, generations, mutationRate=0.05, survivalRate=0.2):
        self.bots = []
        self.populationSize = populationSize
        self.generations = generations
        self.mutationRate = mutationRate
        self.survivalRate = survivalRate

    def trainBots(self):
        self.bots = []
        self.createRandomBots(self.populationSize)
        for g in range(self.generations):
            print('Generation', g, 'of', self.generations)
            startTime = time.time()
            self.runGeneration()

    def runGeneration(self):
        fitness = self.scoreBots()
        self.pruneBots(fitness)
        self.generateChildren()

    def getBestBot(self):
        fitness = self.scoreBots()
        maxFitness = max(fitness)
        for i, bot in enumerate(self.bots):
            if fitness[i] == maxFitness:
                return bot

    def createRandomBots(self, n):
        for i in range(n):
            bot = NeuralBot()
            self.bots.append(bot)

    def pruneBots(self, fitness):
        tries = 0
        while len(self.bots) > self.populationSize * self.survivalRate:
            tries += 1
            selectedBotIndex = random.randrange(len(self.bots))
            survivalFitness = random.uniform(min(fitness), max(fitness))
            if fitness[selectedBotIndex] <= survivalFitness:
                del self.bots[selectedBotIndex]
                del fitness[selectedBotIndex]
                # del fitness to keep indexes matching

    def generateChildren(self):
        possibleParents = self.bots[:]
        while len(self.bots) < self.populationSize:
            if random.choice([True,False]):
                self.bots.append(NeuralBot())
            else:
                firstParent = random.choice(possibleParents)
                secondParent = random.choice(possibleParents)
                child = copy.deepcopy(firstParent)
                for layerIndex in range(len(child.net.layers)):
                    firstParentWeights = firstParent.net.layers[layerIndex].weights
                    firstParentBias = firstParent.net.layers[layerIndex].bias
                    secondParentWeights = secondParent.net.layers[layerIndex].weights
                    secondParentBias = secondParent.net.layers[layerIndex].bias
                    for i in range(len(firstParentWeights)):
                        for j in range(len(firstParentWeights[i])):
                            weightChoice = random.choice([firstParentWeights[i][j], secondParentWeights[i][j]])
                            child.net.layers[layerIndex].weights[i][j] = weightChoice + (self.mutationRate * (2 * random.random() - 1))
                    for i in range(len(firstParentBias)):
                        biasChoice = random.choice([firstParentBias[i], secondParentBias[i]])
                        child.net.layers[layerIndex].bias[i] = biasChoice + (self.mutationRate * (2 * random.random() - 1))
                self.bots.append(child)

    def saveBot(self, bot, name):
        f = open('trainedBots/'+name, 'wb')
        pickle.dump(bot, f)

    def loadBot(self, name):
        f = open('trainedBots/'+name, 'rb')
        return pickle.load(f)

    @classmethod
    def getBestBot(self):
        f = open('trainedBots/bestBot', 'rb')
        return pickle.load(f)


    def scoreBots(self, rounds=1000, enemy=RandomBot()):
        scores = []
        for x in self.bots:
            scores.append({'win':0, 'loss':0, 'draw':0})

        for i, bot in enumerate(self.bots):
            for r in range(rounds):
                game = Game(bot, enemy, True)
                winner = game.runGame()
                if winner is bot:
                    scores[i]['win'] += 1
                if winner is None:
                    scores[i]['draw'] += 1
                else:
                    scores[i]['loss'] += 1
        fitness = [(s['win'] + 0.5 * s['draw'])/rounds for s in scores]
        print('Max/min fitness', max(fitness), '/', min(fitness), 'wins', max([s['win'] for s in scores]))
        return fitness
