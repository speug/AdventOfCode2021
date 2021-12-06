import numpy as np

with open('input', 'r') as f:
    lines = f.readlines()

n_lines = len(lines)
coords = np.zeros((2, 2, n_lines), dtype=int)
for i in range(len(lines)):
    xy1, xy2 = lines[i].split(' -> ')
    coords[0, :, i] = [int(x) for x in xy1.strip().split(',')]
    coords[1, :, i] = [int(x) for x in xy2.strip().split(',')]

mask = np.logical_or((coords[0, 0, :] == coords[1, 0, :]),
                     (coords[0, 1, :] == coords[1, 1, :]))
part1_coords = coords[:, :, np.where(mask)].squeeze()
part2_coords = coords[:, :, np.where(np.logical_not(mask))].squeeze()
field = np.zeros((np.max(coords[:, 0, :])+1,
                  np.max(coords[:, 1, :])+1))

for i in range(part1_coords.shape[2]):
    x1, y1 = part1_coords[0, :, i]
    x2, y2 = part1_coords[1, :, i]
    x1, x2 = (x1, x2) if x1 < x2 else (x2, x1)
    y1, y2 = (y1, y2) if y1 < y2 else (y2, y1)
    #print(f'{x1}, {y1} -> {x2}, {y2}')
    #print(field)
    #print(field[x1:x2+1, y1:y2+1])
    field[x1:x2+1, y1:y2+1] += 1
print('Field after pt1:')
print(field.T)
sum = np.sum(field >= 2)
print(f'Part 1 sum: {sum}')

for i in range(part2_coords.shape[2]):
    x1, y1 = part2_coords[0, :, i]
    x2, y2 = part2_coords[1, :, i]
    print(f'{x1}, {y1} -> {x2}, {y2}')
    # x1, x2 = (x1, x2) if x1 < x2 else (x2, x1)
    # y1, y2 = (y1, y2) if y1 < y2 else (y2, y1)
    x_step = 1 if x1 < x2 else -1
    y_step = 1 if y1 < y2 else -1
    x_indices = range(x1, x2+x_step, x_step)
    y_indices = range(y1, y2+y_step, y_step)
    #print(list(x_indices))
    #print(list(y_indices))
    field[x_indices, y_indices] += 1
print('Field after pt2:')
print(field.T)
sum = np.sum(field >= 2)
print(f'Part 2 sum: {sum}')
