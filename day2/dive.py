# get input
with open('input', 'r') as f:
    instructions = f.readlines()


def move(instruction, x0, y0):
    command, value = instruction.split(' ')
    value = int(value)
    if command == 'forward':
        return x0 + value, y0
    elif command == 'up':
        return x0, y0 - value
    elif command == 'down':
        return x0, y0 + value
    else:
        raise NotImplementedError(f'Command {command} not available!')


def move_with_aim(instruction, x0, y0, aim):
    command, value = instruction.split(' ')
    value = int(value)
    if command == 'forward':
        return x0 + value, y0 + value * aim, aim
    elif command == 'up':
        return x0, y0, aim - value
    elif command == 'down':
        return x0, y0, aim + value
    else:
        raise NotImplementedError(f'Command {command} not available!')


# init position
x = 0
y = 0
aim = 0

for i in instructions:
    # print(f'Current pos: {x} {y}, next instruction: {i}')
    # x, y = move(i, x, y)
    x, y, aim = move_with_aim(i, x, y, aim)

print(f'Final position: {x}, {y} (x*y = {x*y})')
