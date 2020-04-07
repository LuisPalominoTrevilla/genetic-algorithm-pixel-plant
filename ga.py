from random import choices, randint
import numpy

def calc_pop_fitness(population):
    fitness = []
    for chromosome in population:
        fitness.append(chromosome.getScore())
    return fitness

def select_mating_pool(population, fitness, num_parents):
    parents = []
    for parent_num in range(num_parents):
        max_fitness_idx = numpy.where(fitness == numpy.max(fitness))
        max_fitness_idx = max_fitness_idx[0][0]
        parents.append(population[max_fitness_idx])
        fitness[max_fitness_idx] = -99999999999
    return parents

def crossover(parents, offspring_size):
    offspring_crossover = []
    for k in range(offspring_size):
        parent1_idx = k%len(parents)
        parent2_idx = (k+1)%len(parents)
        offspring_crossover.append(parents[parent1_idx].crossover(parents[parent2_idx]))
    return offspring_crossover

def mutation(offspring_crossover):
    for offspring in offspring_crossover:
        random_genes = choices(
            population=[offspring.NULL, offspring.LEAF, offspring.BRANCH, offspring.TRUNK],
            weights=[.1, .3, .3, .3],
            k=randint(1, 5))
        for gene in random_genes:
            pos_i, pos_j = randint(0, offspring.h-1), randint(0, offspring.w-1)
            offspring.im[pos_i][pos_j] = gene
