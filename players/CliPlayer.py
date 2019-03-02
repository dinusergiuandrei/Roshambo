from players.Player import Player


class CliPlayer(Player):

    @staticmethod
    def get_move(history):
        return CliPlayer.ask_move()

    @staticmethod
    def ask_move():
        move = None
        while move not in [0, 1, 2]:
            try:
                move = input('0 = rock, 1 = paper, 2 = scissors. What is your move? ')
                move = int(move)
            except TypeError:
                continue
        return move

    @staticmethod
    def get_name():
        return 'Cli player'
