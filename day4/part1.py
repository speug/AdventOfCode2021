import numpy as np
import os
import sys
sys.path.append(os.getcwd())
from board import Board
# read bingo input
with open('input', 'r') as f:
    lines = f.readlines()

called_numbers = [int(x) for x in lines[0].split(',')]
i = 1
boards = []
num_boards = (len(lines) - 1) // 6
for bi in range(num_boards):
    start_i = bi * 6 + 2
    end_i = (bi + 1) * 6 + 1
    rel_lines = lines[start_i:end_i]
    nums = np.zeros((5, 5))
    for ri in range(5):
        nums[ri, :] = [int(x.strip()) for x in rel_lines[ri].split(' ') if x != '']
    board = Board(5, nums)
    boards.append(board)

winner = False
i = 0
while not winner:
    num = called_numbers[i]
    for board in boards:
        check = board.mark(num)
        if check:
            winner = board
    i += 1
print('Winning board:')
print(winner)
print(f'Score: {winner.score()}')
print(f'Final output = {winner.score()} * {num} = ' +
      f'{winner.score() * num}')


# print(called_numbers)
