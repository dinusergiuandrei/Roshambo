import numpy as np
import pickle


def get_game_from_history(history, my_index):
    complete_game = np.full((15, 6), 1 / 3)
    for game_index in range(len(history)):
        my_move = history[game_index][my_index]
        op_move = history[game_index][1 - my_index]
        for j in range(6):
            complete_game[game_index][j] = 0
        complete_game[game_index][op_move] = 1
        complete_game[game_index][3 + my_move] = 1
    games = np.full((15, 15, 6), 1/3)
    for known in range(0, 15):
        games[known][:known] = complete_game[:known]
    return games


def get_label_from_history(history, my_index):
    complete_label = np.full((15, 3), 1 / 3)
    for game_index in range(len(history)):
        op_move = history[game_index][1 - my_index]
        for j in range(3):
            complete_label[game_index][j] = 0
        complete_label[game_index][op_move] = 1
    labels = np.full((15, 15, 3), 1/3)
    for known in range(0, 15):
        labels[known][:known+1] = complete_label[:known+1]
    return labels


def save_object(path, obj):
    with open(path, 'wb') as handle:
        pickle.dump(obj, handle, protocol=pickle.HIGHEST_PROTOCOL)


def load_object(path):
    with open(path, 'rb') as handle:
        return pickle.load(handle)
