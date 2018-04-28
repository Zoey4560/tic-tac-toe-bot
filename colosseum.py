from game import Game
from occupyBot import OccupyBot
from randomBot import RandomBot
from treeBot import TreeBot
from neuralBot import NeuralBot
import random
import math


#Where bots come to duke it out
bots = []
scores = []
for i in range(100):
    bot = NeuralBot()
    bots.append(bot)
    scores.append({'win':0, 'loss':0, 'draw':0})

for t in range(1):
    for i, bot0 in enumerate(bots):
        for j, bot1 in enumerate(bots):
            game = Game(bot0, bot1)
            winner = game.runGame()
            if winner is not None:
                winnerIndex = i if winner is 0 else j
                loserIndex = i if winner is 1 else j
                scores[winnerIndex]['win'] += 1
                scores[loserIndex]['loss'] += 1
            else:
                for x in [i, j]:
                    scores[x]['draw'] += 1
    print(scores)

bestBot = None
bestWins = 0
for i, score in enumerate(scores):
    if score['win'] > bestWins:
        bestBot = bots[i]
        bestWins = score['win']
print(bestWins)
for z in range(30):
    game = Game(bestBot, RandomBot())
    winner = game.runGame()
    print('The winner is', winner)
