import numpy


def compute_pop_fitness(equation_inputs, pop):
    fitness = numpy.sum(pop * equation_inputs, axis=1)
    return fitness


def select_mating_pool(pop, fitness, num_parents):
    parents = numpy.empty((num_parents, pop.shape[1]))
    for parent_num in range(num_parents):
        max_fitness_idx = numpy.where(fitness == numpy.max(fitness))
        max_fitness_idx = max_fitness_idx[0]
        p = pop[max_fitness_idx][0]
        parents[parent_num] = p
        fitness[max_fitness_idx] = -99999
    return parents


def crossover(parents, offspring_size):
    offspring = numpy.empty(offspring_size)
    crossover_point = numpy.uint8(offspring_size[1] / 2)

    for k in range(offspring_size[0]):
        parent1_idx = k % parents.shape[0]
        parent2_idx = (k + 1) % parents.shape[0]
        offspring[k, 0:crossover_point] = parents[parent1_idx, 0:crossover_point]
        offspring[k, crossover_point:] = parents[parent2_idx, crossover_point:]
    return offspring


def mutation(offspring_crossover):
    for idx in range(offspring_crossover.shape[0]):
        for idy in range(offspring_crossover.shape[1]):
            random_value = numpy.random.uniform(-1.0, 1.0, 1)
            offspring_crossover[idx, idy] = offspring_crossover[idx, idy] + random_value
    return offspring_crossover
