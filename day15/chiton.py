import numpy as np
import heapq


class Vertex:

    def __init__(self, weight, coords, is_start=False):
        self.weight = weight
        self.coords = coords
        self.distance = np.inf
        self.predecessor = None
        self.is_start = is_start

    def set_distance(self, distance):
        self.distance = distance
        return self.distance

    def set_predecessor(self, predecessor):
        self.predecessor = predecessor
        return self.predecessor

    def __str__(self):
        return str(self.weight)

    def __repr__(self):
        return str(self.weight)

    def __lt__(self, other):
        if self.coords[0] != other.coords[0]:
            return self.coords[0] < other.coords[0]
        else:
            return self.coords[1] < other.coords[1]


grid_str = """1163751742
1381373672
2136511328
3694931569
7463417111
1319128137
1359912421
3125421639
1293138521
2311944581
""".split('\n')

with open('input', 'r') as f:
    grid_str = f.readlines()
grid_str = [x.strip() for x in grid_str]

grid_str = [x for x in grid_str if x not in ['', '\n']]
rows = len(grid_str)
cols = len(grid_str[0])
grid = np.empty((rows, cols), dtype=object)
for i in range(rows):
    if grid_str[i] != '':
        grid[i, :] = [Vertex(int(grid_str[i][j]), (i, j))
                      for j in range(len(grid_str[i]))
                      if grid_str[i] not in ['', '\n']]

print(grid)


def get_neighbours(grid, i, j, max_i, max_j):
    out = [None] * 4
    if (i != 0):
        out[0] = grid[i-1, j]
    if (i < max_i-1):
        out[1] = grid[i+1, j]
    if (j != 0):
        out[2] = grid[i, j-1]
    if (j < max_j-1):
        out[3] = grid[i, j+1]
    out = [x for x in out if x is not None]
    return out


def find_optimal_path(grid, rows, cols):
    # Basic Djikstra's algorithm with priority queue (= heapq)
    visited = set()
    Q = []
    grid[0, 0].set_distance(0)
    heapq.heappush(Q, (0, grid[0, 0]))

    while Q:
        dist_u, u = heapq.heappop(Q)
        i, j = u.coords
        neighs = get_neighbours(grid, i, j, rows, cols)
        neighs = [v for v in neighs if v.coords not in visited]
        for v in neighs:
            alt = dist_u + v.weight
            if alt < v.distance:
                v.set_distance(alt)
                v.set_predecessor(u)
                heapq.heappush(Q, (v.distance, v))
            if v.coords == (rows-1, cols-1):
                return v.distance
        visited.add(u.coords)


print(f'Part 1 optimal path risk: {find_optimal_path(grid, rows, cols)}')

# part 2 grid construction
grid_nums = np.zeros((rows, cols), dtype=int)
for i in range(rows):
    if grid_str[i] != '':
        grid_nums[i, :] = [int(grid_str[i][j])
                           for j in range(len(grid_str[i]))
                           if grid_str[i] not in ['', '\n']]

# create first "row" of new tiling
tiled_grid = grid_nums.copy()
for i in range(4):
    grid_nums += 1
    grid_nums[np.where(grid_nums > 9)] = 1
    tiled_grid = np.hstack((tiled_grid, grid_nums))

# create the rest of the rows
grid_nums = tiled_grid.copy()
for j in range(4):
    grid_nums += 1
    grid_nums[np.where(grid_nums > 9)] = 1
    tiled_grid = np.vstack((tiled_grid, grid_nums))
rows *= 5
cols *= 5
grid = np.empty((rows, cols), dtype=object)
for i in range(rows):
    grid[i, :] = [Vertex(tiled_grid[i][j], (i, j))
                  for j in range(len(tiled_grid[i, :]))]

print(grid)
print(f'Part 2 optimal path risk: {find_optimal_path(grid, rows, cols)}')
