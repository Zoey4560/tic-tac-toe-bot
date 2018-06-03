from game import Game
from occupyBot import OccupyBot
from randomBot import RandomBot
from treeBot import TreeBot
from neuralBot import NeuralBot
from geneticTrainer import GeneticTrainer
import random
import math


#Where bots come to duke it out
trainer = GeneticTrainer(100, 10000, 0.1, 0.4)
trainer.trainBots()
bestBot = trainer.getBestBot()
lastBot = trainer.loadBot('bestBot')
trainer.saveBot(lastBot, 'lastBot')

for enemy in [lastBot, RandomBot(), OccupyBot(), TreeBot()]:
    vsEnemy = {'w':0, 'l':0, 'd':0}
    for z in range(100):
        game = Game(bestBot, enemy, True)
        winner = game.runGame()
        if winner is None:
            vsEnemy['d'] += 1
        elif winner is bestBot:
            vsEnemy['w'] += 1
        else:
            vsEnemy['l'] += 1
    print('vs:', enemy.__class__.__name__)
    print('wins', vsEnemy['w'])
    print('losses', vsEnemy['l'])
    print('draws', vsEnemy['d'])

    if enemy is lastBot and (vsEnemy['w'] - vsEnemy['l']) > 0:
        # We bested lastBot! We're the true bestBot!
        trainer.saveBot(bestBot, 'bestBot')
        print('New bestBot!')
