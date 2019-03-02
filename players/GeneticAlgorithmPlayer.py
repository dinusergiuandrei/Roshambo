from random import randint
from players.Player import Player
import numpy
from utils import *


class GAPlayer(Player):

    def __init__(self, index, data=None, train=False):
        super().__init__(index)
        if data is None:
            data = load_object('games')
        (train_games, train_labels) = data
        if train:
            self.best_individual = self.train(train_games, train_labels)
        else:
            self.best_individual = load_object('ga_best_player')

    @staticmethod
    def train(train_games, train_labels):
        sol_per_pop = 30
        crossover_rate = 0.7
        mutation_rate = 0.1

        num_weights = 15 * 6
        num_parents_mating = int(crossover_rate * sol_per_pop)

        pop_size = (sol_per_pop, 3, num_weights)
        new_population = numpy.random.uniform(low=0.0, high=1.0, size=pop_size)
        num_generations = 30

        for generation in range(num_generations):
            print("Generation : ", generation)
            fitness = compute_pop_fitness(train_games, train_labels, new_population)
            parents = select_mating_pool(new_population, fitness, num_parents_mating)
            offspring_crossover = crossover(parents, offspring_size=(pop_size[0] - parents.shape[0], 3, num_weights))
            offspring_mutation = mutation(offspring_crossover, mutation_rate)
            new_population[0:parents.shape[0], :] = parents
            new_population[parents.shape[0]:, :] = offspring_mutation

        fitness = compute_pop_fitness(train_games, train_labels, new_population)
        best_match_idx = numpy.where(fitness == numpy.max(fitness))

        best_individual = new_population[best_match_idx]
        best_individual = best_individual[0]
        best_score = fitness[best_match_idx]
        print("Best solution : ", best_individual)
        print("Best solution fitness : ", best_score)
        return best_individual

    def get_move(self, history):
        if len(history) < 2:
            return randint(0, 2)
        ind = self.best_individual
        game = get_game_from_history(history, self.my_index)

        predicting = len(history) + 1
        params = game.flatten()[:(6 * predicting)]
        ws = np.zeros(3)
        for wi in range(3):
            weights = ind[wi]
            weights = weights[-(6 * predicting):]
            score = numpy.sum(params * weights)
            ws[wi] = score
        pred = np.argmax(ws)
        return (pred + 1) % 3

    @staticmethod
    def get_name():
        return 'Genetic algorithm'


def compute_pop_fitness(train_games, train_labels, pop):
    fitness = numpy.zeros(len(pop))
    for game_index in range(len(train_games)):
        game = train_games[game_index]
        for predicting in range(1, 16):
            params = game.flatten()[:(6 * predicting)]

            for i in range(len(pop)):
                ws = np.zeros(3)
                for wi in range(3):
                    weights = pop[i][wi][-(6 * predicting):]
                    score = numpy.sum(params * weights)
                    ws[wi] = score

                pred = np.argmax(ws)
                r = train_labels[game_index][predicting - 1][pred]
                fitness[i] += r
    fitness = fitness / numpy.max(fitness)
    return fitness


def select_mating_pool(pop, fitness, num_parents):
    parents = numpy.empty((num_parents, pop.shape[1], pop.shape[2]))
    for parent_num in range(num_parents):
        max_fitness_idx = numpy.where(fitness == numpy.max(fitness))
        max_fitness_idx = max_fitness_idx[0]
        p = pop[max_fitness_idx][0]
        parents[parent_num] = p
        fitness[max_fitness_idx] = -99999
    return parents


def crossover(parents, offspring_size):
    offspring = numpy.empty(offspring_size)
    crossover_point = numpy.uint8(offspring_size[2] / 2)

    for k in range(offspring_size[0]):
        parent1_idx = k % parents.shape[0]
        parent2_idx = (k + 1) % parents.shape[0]
        offspring[k, 0:crossover_point] = parents[parent1_idx, 0:crossover_point]
        offspring[k, crossover_point:] = parents[parent2_idx, crossover_point:]
    return offspring


def mutation(offspring_crossover, mutation_rate):
    for idx in range(offspring_crossover.shape[0]):
        for idy in range(offspring_crossover.shape[1]):
            for ws in range(3):
                v = numpy.random.uniform(0, 1.0, 1)
                if v < mutation_rate:
                    random_value = numpy.random.uniform(0.0, 1.0, 1)
                    offspring_crossover[idx][ws][idy] = (offspring_crossover[idx][ws][idy] + random_value) / 2
    return offspring_crossover

