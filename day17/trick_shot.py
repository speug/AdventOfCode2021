import numpy as np
import matplotlib.pyplot as plt


def calculate_trajectory(vx, vy, target, return_trajectory=True):
    x = y = 0
    tx0, tx1 = target[0]
    ty0, ty1 = target[1]
    stop = False
    trajectory = []
    while not stop:
        x += vx
        y += vy
        if return_trajectory:
            trajectory.append((x, y))
        if abs(vx) > 0:
            vx += -1 if vx > 0 else 1
        vy += -1
        # print(f'{x}, {y}')
        stop = ((x >= tx0) and (y <= ty0)) or y < ty1 or x > tx1
    if (x <= tx1) and (y >= ty1):
        in_target = 0
    elif (x > tx1) or (y < ty1):
        in_target = 1
    else:
        in_target = -1
    if return_trajectory:
        return in_target, trajectory
    else:
        return in_target


def valid_vx(max_v, target):
    out = []
    tx0, tx1 = target[0]
    for vx0 in range(max_v, 0, -1):
        x = 0
        vx = vx0
        while (x < tx0) and (vx > 0):
            x += vx
            vx -= 1
        if (x <= tx1) and (x >= tx0):
            out.append(vx0)
        elif vx == 0:
            return out
    return out

# target area: x=56..76, y=-162..-134
target = [(56, 76), (-134, -162)]
max_v = 300
min_v = -200
valid_vxs = valid_vx(max_v, target)
print(valid_vxs)
max_y = -np.inf
best_vel = None
valid_vels = 0
for vy0 in range(max_v, min_v, -1):
    last_shot = 1
    i_vx = 0
    while (last_shot > -1) and (i_vx < len(valid_vxs)):
        last_shot, trajectory = calculate_trajectory(valid_vxs[i_vx], vy0, target)
        if last_shot == 1:
            print(f'Overshot the target with {valid_vxs[i_vx]}, {vy0} ({trajectory})')
            i_vx += 1
        elif last_shot == 0:
            print(f'In target with {valid_vxs[i_vx]}, {vy0} ({trajectory})')
            h = max([x[1] for x in trajectory])
            if h > max_y:
                max_y = h
                best_vel = (valid_vxs[i_vx], vy0)
            i_vx += 1
            valid_vels += 1
        else:
            print(f'Undershot with {valid_vxs[i_vx]}, {vy0} ({trajectory})')
            break
print(f'Best height was {max_y} (v0 = {best_vel})')
print(f'Valid velocities in search space was {valid_vels}')

# print(calculate_trajectory(6, 9, target))
