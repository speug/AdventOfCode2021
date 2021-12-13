import numpy as np

with open('input', 'r') as f:
    dots_str = f.readlines()
dot_locs = [x for x in dots_str if ('fold' not in x) and (x not in ['', '\n'])]
dot_locs = [(int(x.split(',')[0]), int(x.split(',')[1])) for x in dot_locs]
max_x = np.max([x[0] for x in dot_locs])
max_y = np.max([x[1] for x in dot_locs])
fold_instructions = [x for x in dots_str if 'fold' in x]
dots = np.zeros((max_y+1, max_x+1), dtype=int)
for c, r in dot_locs:
    dots[r, c] = 1


def fold(dot_grid, instruction):
    instruction = instruction.split('fold along ')[1]
    axis, index = instruction.split('=')
    index = int(index.strip())
    if axis == 'x':
        to_mirror = dot_grid[:, index+1:]
        dot_grid = dot_grid[:, :index]
        to_mirror = np.fliplr(to_mirror)
        if to_mirror.shape != dot_grid.shape:
            to_mirror = np.hstack([np.zeros(dot_grid.shape[0]), to_mirror])
        dot_grid = np.logical_or(dot_grid, to_mirror).astype(int)
    else:
        to_mirror = dot_grid[index+1:, :]
        dot_grid = dot_grid[:index, :]
        to_mirror = np.flipud(to_mirror)
        if to_mirror.shape != dot_grid.shape:
            to_mirror = np.vstack([np.zeros(dot_grid.shape[1]), to_mirror])
        dot_grid = np.logical_or(dot_grid, to_mirror).astype(int)
    return dot_grid


dots = fold(dots, fold_instructions[0])
print(f'Sum of part 1 dots: {np.sum(dots)}')

for i in range(1, len(fold_instructions)):
    print(fold_instructions[i])
    print(dots.shape)
    dots = fold(dots, fold_instructions[i])

print('------------FINAL OUTPUT------------')
for r in range(dots.shape[0]):
    line = dots[r, :]
    l_str = ''.join([' ' if x == 0 else '#' for x in line])
    print(l_str)
