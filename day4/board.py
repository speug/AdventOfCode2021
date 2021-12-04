"""Simple bingo board class"""
import numpy as np


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
