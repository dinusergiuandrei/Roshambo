from random import randint
from players.Player import Player


class MinMaxPlayer(Player):
    """
    function minimax(node, depth, maximizingPlayer) is
    if depth = 0 or node is a terminal node then
        return the heuristic value of node
    if maximizingPlayer then
        value := −∞
        for each child of node do
            value := max(value, minimax(child, depth − 1, FALSE))
        return value
    else (* minimizing player *)
        value := +∞
        for each child of node do
            value := min(value, minimax(child, depth − 1, TRUE))
        return value
    """

    def mini_max(self, depth, maximizing):
        if depth == 0:  # or not is terminal node
            return

    def get_move(self, history):
        if len(history) > 0:
            return history[len(history) - 1][1 - self.my_index]
        else:
            return randint(0, 2)

    @staticmethod
    def get_name():
        return 'Min Max'
