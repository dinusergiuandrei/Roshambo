from random import randint

from players.Player import Player


class RandomPlayer(Player):

    @staticmethod
    def get_move(history):
        return randint(0, 2)

    @staticmethod
    def get_name():
        return 'Random player'
