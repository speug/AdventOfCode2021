import numpy as np
# remove the cheating function, implement own!
# from scipy.ndimage import label

# grid_str = """2199943210
# 3987894921
# 9856789892
# 8767896789
# 9899965678
# """
with open('input', 'r') as f:
    grid_str = f.read()
lines = grid_str.split('\n')
max_j = len(lines[0])
max_i = len(lines) - 1 # -1 needed with actual input to avoid empty final line
grid = np.zeros((max_i, max_j), dtype=int)
for i in range(max_i):
    grid[i, :] = [int(x) for x in lines[i]]


def get_neighbours(grid, i, j, max_i, max_j):
    out = [(np.inf, (-1, -1))] * 4
    if (i != 0):
        out[0] = (grid[i-1, j], (i-1, j))
    if (i != max_i):
        out[1] = (grid[i+1, j], (i+1, j))
    if (j != 0):
        out[2] = (grid[i, j-1], (i, j-1))
    if (j != max_j):
        out[3] = (grid[i, j+1], (i, j+1))
    return out


low_points = []
for i in range(max_i):
    for j in range(max_j):
        neighs = get_neighbours(grid, i, j, max_i-1, max_j-1)
        if all(grid[i, j] < x[0] for x in neighs):
            low_points.append(grid[i, j])
print(f'Found low_points with heights {low_points}.')
print(f'Risk level is {sum([x+1 for x in low_points])}')

# print(grid)
grid_borders = grid == 9
# init bordered grid so that 9 => 0 and all other are -1 ("uncolored")
flood_borders = grid_borders - 1


def color_grid(grid, max_i, max_j):
    """Color each continuous grid segment. Each element checks if it is
       uncolored (has a value of -1), colors itself and recursively calls
       its neighbours to do the same. If element is zero, it returns from
       the recursion. When one area is colored, increment color number
       and move to the next."""
    i_label = 1

    def inner(i, j, i_label):
        if grid[i, j] == -1:
            grid[i, j] = i_label
            neighs = get_neighbours(grid, i, j, max_i-1, max_j-1)
            neighs = [x for x in neighs if not x[0] in [np.inf, i_label]]
            for n in neighs:
                inner(n[1][0], n[1][1], i_label)
        else:
            return

    uncolored = np.where(grid == -1)
    while len(uncolored[0]) >= 1:
        start_i = uncolored[0][0]
        start_j = uncolored[1][0]
        inner(start_i, start_j, i_label)
        i_label += 1
        uncolored = np.where(grid == -1)
    return grid, i_label - 1


# print(flood_borders)
labelled, areas = color_grid(flood_borders, max_i, max_j)
# print(labelled)
area_sizes = sorted([np.sum(labelled == i) for i in range(1, areas+1)])
# print(labelled)
print(area_sizes[-3:])
print(f'Product of three biggest: {np.product(area_sizes[-3:])}')
