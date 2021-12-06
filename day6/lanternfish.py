import numpy as np


def update_fishes(current):
    # check how many fishes are giving birth
    births = current[0]
    # shift population counts by one to the left (day proceeds)
    current[0:-1] = current[1:]
    # add new fishes to day 8
    current[8] = births
    # add new parents back to the pool
    current[6] += births
    return current


with open('input', 'r') as f:
    lines = f.readlines()
# fish_input = np.array([3,4,3,1,2])
fish_input = np.array([int(x) for x in lines[0].split(',')], dtype=int)
fishes = np.zeros(9)
# create population count vector for to avoid allocating ever increasing array
for f in fish_input:
    fishes[f] += 1
max_t = 256
for i in range(max_t):
    # print(fishes)
    fishes = update_fishes(fishes)
print(f'Fish population by date since birth: {fishes}')
print(f'Total fishes: {np.sum(fishes)}')
