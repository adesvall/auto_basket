import pickle
from population import Population
from bot import Bot

if __name__ == "__main__":
    f = open("population.pkl", "rb")
    population = pickle.load(f)
    f.close()
    population.population[0].game()