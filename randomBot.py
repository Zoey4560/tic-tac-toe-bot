import random
from game import Game

class RandomBot:
    def getMove(self, board, whichPlayerAmI):
        while True:
            randomPosition = random.randint(0,8)
            if Game.isMoveValid(board, randomPosition):
                return randomPosition
