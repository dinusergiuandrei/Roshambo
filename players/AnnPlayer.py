from random import randint
from players.Player import Player
import tensorflow as tf
from tensorflow import keras
import numpy as np
import matplotlib.pyplot as plt
from utils import *


class AnnPlayer(Player):

    def __init__(self, index, train_data=None, train=False):
        super().__init__(index)
        if train_data is None and train:
            train_data = load_object('games')
        self.model = keras.Sequential([
            keras.layers.Flatten(input_shape=(15, 6)),  # 15 rounds. 3 probabilities for each op/my hand.
            keras.layers.Dense(128, activation=tf.nn.relu),
            keras.layers.Dense(15 * 3, activation=tf.nn.softmax)  # 15 rounds. 3 predictions as probabilities
        ])

        self.model.compile(optimizer=tf.train.AdamOptimizer(),
                           loss='categorical_crossentropy',
                           metrics=['accuracy'])
        if train:
            self.train(train_data)
            self.model.save_weights('data/weights')
        else:
            self.model.load_weights('data/weights')

    def train(self, data):
        (train_games, train_labels) = data
        computed_labels = []
        for label in train_labels:
            computed_labels.append(label.flatten())
        computed_labels = np.array(computed_labels)
        self.model.fit(train_games, computed_labels, epochs=10)

    def get_move(self, history):
        if len(history) < 2:
            return randint(0, 2)
        game = get_game_from_history(history, self.my_index)
        # game = (np.expand_dims(game, 0))
        prediction = self.model.predict(game)[0]
        prediction = prediction.reshape((15, 3))
        if len(history) > len(prediction):
            print("Isn't the game supposed to be over? Check if the model has the correct output shape.")
        predicted_move = np.argmax(prediction[len(history)])
        return (predicted_move + 1) % 3

    @staticmethod
    def get_name():
        return 'Artificial neuronal network'
