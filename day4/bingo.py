import numpy as np
# read bingo input
with open('input', 'r') as f:
    lines = f.readlines()


class Board:
    def __init__(self, dim, numbers):
        self.dim = dim
        self.numbers = numbers
        self.marked = np.zeros((dim, dim))

    def mark(self, number):
        if number not in self.numbers:
            return False
        else:
            self.marked[np.where(self.numbers == number)] = 1
            return self.check_for_win()

    def check_for_win(self):
        # check rows
        for i in range(self.dim):
            if all(self.marked[i, :] == 1):
                return True
            elif all(self.marked[:, i] == 1):
                return True
        return False

    def score(self):
        if not self.check_for_win():
            return 0
        else:
            mask = 1 - self.marked
            mask = mask == 1
            return np.sum(self.numbers[mask])

    def __str__(self):
        out = str(self.numbers) + '\n' + str(self.marked)
        return out


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
