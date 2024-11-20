import random
import math

def update_score(game, padA, padB):
    if game.get_state != 'butA' and game.get_state != 'butB':
        return

    if game.get_state == 'butA':
        padA.score += 1
    if game.get_state == 'butB':
        padB.score += 1

    game.set_state('pause')
