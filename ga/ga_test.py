from ga.GA import *

sol_per_pop = 30
crossover_rate = 0.7
mutation_rate = 0.01
equation_inputs = [4, -2, 3.5, 5, -11, -4.7]

num_weights = len(equation_inputs)
num_parents_mating = int(crossover_rate*sol_per_pop)

pop_size = (sol_per_pop, num_weights)
new_population = numpy.random.uniform(low=-4.0, high=4.0, size=pop_size)
print(new_population)
num_generations = 20

for generation in range(num_generations):
    print("Generation : ", generation)
    fitness = compute_pop_fitness(equation_inputs, new_population)
    parents = select_mating_pool(new_population, fitness, num_parents_mating)
    offspring_crossover = crossover(parents, offspring_size=(pop_size[0] - parents.shape[0], num_weights))
    offspring_mutation = mutation(offspring_crossover)
    new_population[0:parents.shape[0], :] = parents
    new_population[parents.shape[0]:, :] = offspring_mutation
    print("Best result : ", numpy.max(numpy.sum(new_population * equation_inputs, axis=1)))

fitness = compute_pop_fitness(equation_inputs, new_population)
best_match_idx = numpy.where(fitness == numpy.max(fitness))
print("Best solution : ", new_population[best_match_idx])
print("Best solution fitness : ", fitness[best_match_idx])
