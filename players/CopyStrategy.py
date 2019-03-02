from random import randint
from players.Player import Player


class CopyPlayer(Player):

    def get_move(self, history):
        if len(history) > 0:
            return history[len(history) - 1][1 - self.my_index]
        else:
            return randint(0, 2)

    @staticmethod
    def get_name():
        return 'Copy player'
