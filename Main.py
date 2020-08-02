import random
from Snake_Game import *


def cross_over(parent1, parent2):
    new_child = []
    for gen1, gen2 in zip(parent1, parent2):

        luck = random.random()

        if luck < 0.45:
            new_child.append(gen1)
        elif luck < 0.90:
            new_child.append(gen2)
        else:
            new_child.append(random.randrange(0, 6))

    return new_child


GENERATIONS = 1

population = []
population_size = 20
step_size = 1000
# 0 Up
# 1 Down
# 2 Left
# 3 Right
# 4 Distance to food
# 5 Distance to an obstacle
moves_set = [0, 1, 2, 3, 4, 5]

# First population is created.
for i in range(population_size):
    genes = random.choices(moves_set, k=step_size)
    population.append(genes)


for i in range(GENERATIONS):

    wanted = cal_fitness(population)

    # List population according to fitness values.
    Z = [population for (wanted, population) in sorted(zip(wanted, population), key=lambda pair: pair[0])]
    new_generation = []

    # Elitism
    take_ratio = int((20*population_size)/100)
    new_generation.extend(Z[:take_ratio])

    # Parents
    take_ratio = int((80*population_size)/100)
    for _ in range(take_ratio):
        parent1 = random.choice(Z[:5])
        parent2 = random.choice(Z[:5])
        new_generation.append(cross_over(parent1, parent2))

    population = new_generation
    print("------- {} Generation Ended -------".format(i+1))
    print(wanted)

pg.quit()
