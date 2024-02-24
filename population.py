import random
import numpy as np
from pprint import pprint
import pickle
import time
from multiprocessing import Pool
from bot import Bot

def fitness(arg):
    bot, seed = arg
    random.seed(seed)
    return (bot.evaluate_fitness(), bot)

class Population:
    def __init__(self, population_size):
        self.population = []
        for _ in range(population_size):
            self.population.append(Bot())

    def select(self, n):
        seed = random.random()
        with Pool(14) as p:
            fitnesses = p.map(fitness, zip(self.population, [seed] * len(self.population)))
        random.seed(time.time())

        fitnesses.sort(reverse=True, key=lambda x: x[0])
        self.population = [x for _, x in fitnesses]
        self.population = self.population[:n]
        print("\tBest :", fitnesses[0][0])
        print("\tLast Selected :", fitnesses[n-1][0])
        print("\tMoyenne :", sum(f[0] for f in fitnesses) / len(fitnesses))

    def make_children(self, n, mutation_rate):
        pop = self.population[:]
        for _ in range(n):
            parent = pop[np.random.choice(range(len(pop)), 1, range(len(pop), 0, -1))[0]]
            child = Bot(parent.params)
            child.mutate(mutation_rate)
            self.population.append(child)

    def evolve(self, num_parents, num_offspring, mutation_rate):
        self.select(num_parents)
        self.make_children(num_offspring, mutation_rate)

    # def game(self):
    #     game = Game()

if __name__ == "__main__":
    num_generations = 50
    population_size = 200
    num_parents = 90
    num_offspring = population_size - num_parents
    mutation_rate = 0.00001

    # population = Population(population_size)
    f = open("population.pkl", "rb")
    population = pickle.load(f)
    f.close()
    for generation in range(num_generations):
        print(f"Generation {generation}/{num_generations} - {num_parents}/{len(population.population)}")
        # print(population.population[0].params)
        population.evolve(num_parents, num_offspring, mutation_rate)
    print(f"Generation {num_generations} - {len(population.population)}")
    pprint(population.population[0].params.tolist())
    f = open("population.pkl", "wb")
    pickle.dump(population, f)
    f.close()
    population.population[0].game()