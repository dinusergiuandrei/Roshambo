import os

from players.CliPlayer import CliPlayer
from players.CopyStrategy import CopyPlayer
from players.RandomPlayer import RandomPlayer
from players.RnPlayer import AnnPlayer
from players.GeneticAlgorithmPlayer import GAPlayer
from utils import *
import random

rock = 0
paper = 1
scissors = 2
names = ['rock', 'paper', 'scissors']


class Roshambo:

    def __init__(self):
        self.history = []

        self.states = None
        self.labels = None

    def play(self, player1, player2, rounds=15):
        score = np.zeros(2)
        self.history = []
        for _ in range(rounds):
            winner = self.game(player1, player2)
            # while winner is None:
            #     winner = self.game(player1, player2)
            if winner is not None:
                score[winner] += 1
            print('Score: {} - {}'.format(score[0], score[1]))

        print('{} : {}'.format(player1.get_name(), score[0]))
        print('{} : {}'.format(player2.get_name(), score[1]))

        c_game = get_game_from_history(self.history, 1)
        c_label = get_label_from_history(self.history, 1)

        if self.states is not None:
            self.states = [*self.states, *c_game]
        else:
            self.states = c_game
        if self.labels is not None:
            self.labels = [*self.labels, *c_label]
        else:
            self.labels = c_label
        return score

    def game(self, player1, player2):
        r1 = player1.get_move(self.history)
        r2 = player2.get_move(self.history)

        winner_index = self.get_winner(r1, r2)

        self.history.append((r1, r2, winner_index))

        if winner_index is not None:
            winner = list([player1, player2])[winner_index]
        else:
            winner = None
        if winner_index is not None:
            print('{} : {}, {} : {}. Winner : {}'
                  .format(player1.get_name(), names[r1], player2.get_name(), names[r2], winner.get_name()))
        else:
            print('{} : {}, {} : {}. Equality'
                  .format(player1.get_name(), names[r1], player2.get_name(), names[r2]))
        return winner_index

    @staticmethod
    def get_winner(r1, r2):
        if r1 == r2:
            return None

        if r1 == rock and r2 == scissors:
            return 0

        if r2 == rock and r1 == scissors:
            return 1

        if r1 < r2:
            return 1
        else:
            return 0


def generate_games():
    l_game = Roshambo()
    player1 = CopyPlayer(0)
    player2 = RandomPlayer(1)
    game_count = 300
    for _ in range(game_count):
        l_game.play(player1, player2)
    states = np.array(l_game.states)
    labels = np.array(l_game.labels)
    save_object('games', (states, labels))


def train(games=15):
    game = Roshambo()
    print('loading ga player')

    ga_path = 'ga_best_player'
    # train_data = load_object('games')
    t_games = []
    t_labels = []
    for root, dirs, files in os.walk('tgames2'):
        for file in files:
            fp = os.path.join(root, file)
            game_data = load_object(fp)
            (train_games, train_labels) = game_data
            t_games.extend(train_games)
            t_labels.extend(train_labels)
            # train_data[0].extend(train_games)
            # train_data[1].extend(train_labels)

    # train_data[0] = np.array(train_data[0])
    # train_data[1] = np.array(train_data[1])
    t_games = np.array(t_games)
    t_labels = np.array(t_labels)
    train_data = (t_games, t_labels)

    p1 = AnnPlayer(0, train_data)

    obj = GAPlayer(1, train=True, data=train_data)
    save_object(ga_path, obj.best_individual)
    # p2 = load_object(ga_path)
    p2 = obj

    total_score = np.zeros(2)
    score = np.zeros(2)
    print('starting games')
    for _ in range(games):
        score = score + game.play(p1, p2)
        total_score = total_score + score
        print(score)
    print(total_score)


def tournament(rounds=15):
    players = np.array([RandomPlayer, CopyPlayer, GAPlayer, AnnPlayer])
    scores = np.zeros((4, 4))
    sets = np.zeros((4, 4))
    for i1 in range(4):
        for i2 in range(i1):
            for r in range(rounds):
                p1 = players[i1](0)
                p2 = players[i2](1)
                game = Roshambo()
                print(p1.get_name() + ' vs ' + p2.get_name())
                score = game.play(p1, p2)
                result = score[1]-score[0]
                scores[i2][i1] += result
                scores[i1][i2] -= result

                if result > 0:
                    sets[i2][i1] += 1
                    sets[i1][i2] -= 1
                elif result < 0:
                    sets[i2][i1] -= 1
                    sets[i1][i2] += 1

                states = np.array(game.states)
                labels = np.array(game.labels)
                save_object('tgames2/game'+str(i1)+str(i2)+str(r), (states, labels))
                print(str(score[0]) + ' - ' + str(score[1]))

    t_result = dict()
    for i in range(len(players)):
        t_result[players[i].get_name()] = sum(scores[i])

    s_result = dict()
    for i in range(len(players)):
        s_result[players[i].get_name()] = sum(sets[i])

    return scores, t_result, sets, s_result


if __name__ == '__main__':
    # generate_games()
    # train()
    t = tournament()
    print(t[0])  # hands difference
    print(t[1])  # easy read
    print(t[2])  # rounds of 15 won
    print(t[3])  # easy read


