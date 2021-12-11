import numpy as np

grid_lines = """5483143223
2745854711
5264556173
6141336146
6357385478
4167524645
2176841721
6882881134
4846848554
5283751526
""".split('\n')
with open('input', 'r') as f:
    grid_lines = f.readlines()
rows = len(grid_lines)
cols = len(grid_lines[0].strip())
grid = np.zeros((rows, cols), dtype=int)
for i in range(len(grid_lines)):
    if grid_lines[i] != '':
        grid[i, :] = [int(x) for x in grid_lines[i].strip()]
# copy the initial grid for part 2
grid2 = np.copy(grid)
print('----------INIT-----------')
print(grid)


def get_from_grid(grid, i, j, max_i, max_j):
    if (i >= 0) and (i < max_i):
        if (j >= 0) and (j < max_j):
            return (grid[i, j], (i, j))
    return None, None


def get_neighbours(grid, i, j, max_i, max_j):
    out = [None] * 8
    ijs = [(1, -1), (1, 0), (1, 1),
           (0, -1), (0, 1),
           (-1, -1), (-1, 0), (-1, 1)]
    for idx in range(8):
        i_off, j_off = ijs[idx]
        out[idx] = get_from_grid(grid, i+i_off, j+j_off, max_i, max_j)
    return out


def advance_octopi(grid, max_i, max_j):
    """Flash octopi."""

    def flash(i, j):
        if grid[i, j] != 0:
            grid[i, j] += 1
        if grid[i, j] > 9:
            grid[i, j] = 0
            neighs = get_neighbours(grid, i, j, max_i, max_j)
            neighs = [x for x in neighs if x[0] is not None]
            while neighs:
                n = neighs.pop(0)
                flash(n[1][0], n[1][1])
        else:
            return

    grid += 1
    flashing = np.where(grid > 9)
    while len(flashing[0]) >= 1:
        start_i = flashing[0][0]
        start_j = flashing[1][0]
        flash(start_i, start_j)
        flashing = np.where(grid > 9)
    flashes = np.sum(grid == 0)
    return grid, flashes


print(grid)
total_flashes = 0
for i in range(100):
    grid, flashes = advance_octopi(grid, rows, cols)
    total_flashes += flashes
print(grid)
print(f'Total amount of flashes after 100 rounds was {total_flashes}')

not_synchronized = True
step = 0
# copy initial grid back
grid = grid2
print(grid)
while not_synchronized:
    grid, flashes = advance_octopi(grid, rows, cols)
    not_synchronized = np.sum(grid) != 0
    step += 1
    # print(grid)
print(grid)
print(f'Synchronized step was {step}')
