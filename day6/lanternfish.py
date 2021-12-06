import numpy as np


def update_fish(current):
    # check how many fish are giving birth
    births = current[0]
    # shift population counts by one to the left (day proceeds)
    current[0:-1] = current[1:]
    # add new fish to day 8
    current[8] = births
    # add new parents back to the pool
    current[6] += births
    return current


with open('input', 'r') as f:
    lines = f.readlines()
# fish_input = np.array([3,4,3,1,2])
fish_input = np.array([int(x) for x in lines[0].split(',')], dtype=int)
fish = np.zeros(9)
# create population count vector for to avoid allocating ever increasing array
for f in fish_input:
    fish[f] += 1
max_t = 256
for i in range(max_t):
    # print(fish)
    fish = update_fish(fish)
print(f'Fish population by date since birth: {fish}')
print(f'Total fishes: {np.sum(fish)}')
