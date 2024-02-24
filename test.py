from multiprocessing import Pool
import random

def    rand(arg):
    random.seed(arg)
    return random.randint(0, 2000000000)

with Pool(15) as p:
    print(p.map(rand, [random.random()] * 15))

print(".".join("abcde"))
