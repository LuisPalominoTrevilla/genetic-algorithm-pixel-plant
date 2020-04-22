import imageManipulation as img
import numpy
import ga
from pixelPlant import PixelPlant
from rulesManager import RulesManager
import sys

def main():
    if len(sys.argv) != 2 or sys.argv[1] not in ['1', '2', '3']:
        print("Please, provide an execution mode as an argument (1, 2 or 3).")
        print("Example: python3 optimal-pixel-plant.py 2")
        return

    execution_mode = int(sys.argv[1])
    rulesManager = RulesManager(execution_mode)

    pop_size = 60
    new_population = []
    for i in range(pop_size):
        new_population.append(PixelPlant(rulesManager))
        new_population[i].genRandom()

    num_generations = 2000

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


if __name__ == '__main__':
    main()
