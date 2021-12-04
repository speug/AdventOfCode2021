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
    # print(board)

i = 0
winners = np.ones(len(boards))
while np.sum(winners) != 1:
    num = called_numbers[i]
    for bi in range(len(boards)):
        if winners[bi] == 1:
            board = boards[bi]
            check = board.mark(num)
            if check:
                winners[bi] = 0
    i += 1

loser = boards[np.where(winners == 1)[0][0]]
# keep playing the losing board
loser_has_won = False
while not loser_has_won:
    num = called_numbers[i]
    loser_has_won = loser.mark(num)
    i += 1
print('Losing board:')
print(loser)
print(f'Score: {loser.score()}')
print(f'Final output = {loser.score()} * {num} = ' +
      f'{loser.score() * num}')


# print(called_numbers)
