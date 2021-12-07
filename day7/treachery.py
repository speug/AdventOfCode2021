import numpy as np

# positions = np.array([16,1,2,0,4,2,7,1,2,14], dtype=int)
with open('input', 'r') as f:
    lines = f.readlines()
positions = np.array([int(x) for x in lines[0].split(',')], dtype=int)
max_x = np.max(positions)
num_crabs = len(positions)
distances = np.zeros((max_x+1, num_crabs), dtype=int)
distances2 = np.copy(distances)
dist_range = np.arange(0, max_x+1)


def increasing_cost(n):
    # the fuel cost is just the triangular number of distance
    return n * (n + 1) // 2


for i in range(num_crabs):
    d_i = np.abs(dist_range - positions[i])
    distances[:, i] = d_i
    vector_cost = np.vectorize(increasing_cost)
    distances2[:, i] = vector_cost(d_i)

opt_pos1 = np.argmin(distances.sum(axis=1))
opt_pos2 = np.argmin(distances2.sum(axis=1))
print(f'Part 1 min fuel: {np.sum(distances[opt_pos1])} ' +
      f'(optimal position: {opt_pos1})')
print(f'Part 2 min fuel: {np.sum(distances2[opt_pos2])} ' +
      f'(optimal position: {opt_pos2})')
