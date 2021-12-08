"""Simple bingo board class"""
import numpy as np


class Board:
    def __init__(self, dim, numbers):
        self.dim = dim
        self.numbers = numbers
        self.marked = np.zeros((dim, dim))

    def mark(self, number):
        """Check for the number on this Board.
           Returns True if the addition of the number resulted in a win,
           otherwise False."""
        if number not in self.numbers:
            return False
        else:
            self.marked[np.where(self.numbers == number)] = 1
            return self.check_for_win()

    def check_for_win(self):
        for i in range(self.dim):
            # check rows
            if all(self.marked[i, :] == 1):
                return True
            # check columns
            elif all(self.marked[:, i] == 1):
                return True
        return False

    def score(self):
        """Calculate score for this board (sum of unmarked numbers)."""
        if not self.check_for_win():
            return 0
        else:
            mask = self.marked == 0
            return np.sum(self.numbers[mask])

    def __str__(self):
        out = str(self.numbers) + '\n' + str(self.marked)
        return out
