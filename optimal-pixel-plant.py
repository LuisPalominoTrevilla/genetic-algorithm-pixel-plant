import imageManipulation as img
import numpy
import ga
from pixelPlant import PixelPlant

pop_size = 30
new_population = []
for i in range(pop_size):
    new_population.append(PixelPlant())
    new_population[i].genRandom()

num_generations = 1000

fittestPixelPlant = None

for gen in range(num_generations):
    print("Generation", gen+1)
    fitness = ga.calc_pop_fitness(new_population)
    parents = ga.select_mating_pool(
        new_population, fitness, len(new_population)//2)
    offspring_crossover = ga.crossover(parents, pop_size-len(parents))
    ga.mutation(offspring_crossover)

    new_population[0:len(parents)] = parents
    new_population[len(parents):] = offspring_crossover
    print("Best result after generation", gen+1, ":", parents[0].getScore())
    fittestPixelPlant = parents[0]

# Show fittest result
img.showTree(fittestPixelPlant.toImage())
