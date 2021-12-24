import ast

class SnailfishNumber():
    def __init__(self, left, right, depth=0, parent=None, parent_type=None):
        self.left = left
        self.right = right
        self.parent = parent
        self.depth = depth
        self.parent_type = parent_type
        if type(self.left) == SnailfishNumber:
            self.left.set_parent(self, 'left')
        if type(self.right) == SnailfishNumber:
            self.right.set_parent(self, 'right')

    def set_parent(self, parent, parent_type):
        self.parent = parent
        self.parent_type = parent_type
        self.depth = self.parent.depth + 1
        if type(self.left) == SnailfishNumber:
            self.left.increase_depth()
        if type(self.right) == SnailfishNumber:
            self.right.increase_depth()

    def increase_depth(self):
        self.depth += 1

    def increase_left(self, num):
        print(self)
        if type(self.left) == SnailfishNumber:
            self.left.increase_left(num)
        else:
            self.left += num

    def increase_right(self, num):
        if type(self.right) == SnailfishNumber:
            self.right.increase_right(num)
        else:
            self.right += num

    def explode(self):
        if self.parent is not None and self.parent_type == 'right':
            if type(self.parent.left) == SnailfishNumber:
                self.parent.left.increase_right(self.left)
            else:
                self.parent.left += self.left
        if self.parent is not None and self.parent_type == 'left':
            if type(self.parent.right) == SnailfishNumber:
                self.parent.right.increase_left(self.right)
            else:
                self.parent.right += self.right
        if self.parent is not None:
            if self.parent_type == 'left':
                self.parent.left = 0
            else:
                self.parent.right = 0

    def reduce(self):
        # need dfs for finding leftmost pair of depth > 3
        pass

    def __add__(self, other):
        return SnailfishNumber(self, other)

    def __str__(self):
        return f'[{self.left}, {self.right}]'

    def __repr__(self):
        return f'[{self.left}, {self.right}]'


def snailnumber_from_list(input_list, parent=None):
    x, y = input_list
    if type(x) == list:
        x = snailnumber_from_list(x)
    else:
        x = int(x)
    if type(y) == list:
        y = snailnumber_from_list(y)
    else:
        y = int(y)
    return SnailfishNumber(x, y)


test = '[[[[[9,8],1],2],3],4]'
test = snailnumber_from_list(ast.literal_eval(test))
print(test)
print(test.left.left.left.left)
test.left.left.left.left.explode()
print(test)
print(test.left.left.left.left)
print(test.left.left.left.right)
