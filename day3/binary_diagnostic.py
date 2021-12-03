import numpy as np

# get input
with open('input', 'r') as f:
    bins = f.readlines()

bins = [
    '00100',
    '11110',
    '10110',
    '10111',
    '10101',
    '01111',
    '00111',
    '11100',
    '10000',
    '11001',
    '00010',
    '01010',
]

bits = len(bins[0].strip())  # have to strip the newline
n_bins = len(bins)
one_counts = np.zeros(bits)

for b in bins:
    b = int(b.strip(), 2)  # get binary repr
    for i in range(bits):
        shifted = b >> i
        one_counts[i] += shifted & 1

ratios = list(reversed([x/n_bins for x in one_counts]))
gamma = ''.join(['0' if x < 0.5 else '1' for x in ratios])
epsilon = ''.join(['0' if x > 0.5 else '1' for x in ratios])
print('Part 1:')
print(f'Gamma: {gamma} ({int(gamma, 2)}), epsilon: {epsilon} ({int(epsilon, 2)})')
print(f'Product: {int(gamma, 2) * int(epsilon, 2)}')

# part 2
# the ratios are nice


# solution: build some sort of tree, then we can just walk the tree
class Node:
    def __init__(self, number, depth, is_root=False):
        self.left = None
        self.right = None
        self.number = number
        self.children = 0
        self.depth = depth
        self.is_root = is_root

    def insert(self, number, max_depth):
        #self.PrintTree()
        if self.depth >= max_depth:
            return None
        bit_at_depth = number >> self.depth
        self.children += 1
        if bit_at_depth & 1:
            if self.right is not None:
                self.right.insert(number, max_depth)
            else:
                self.right = Node(bit_at_depth & 1, self.depth+1)
        else:
            if self.left is not None:
                self.children += 1
                self.left.insert(number, max_depth)
            else:
                self.left = Node(bit_at_depth & 1, self.depth+1)

    def PrintTree(self):
        if self.left:
            self.left.PrintTree()
        print(f'{self.number}: {self.children}'),
        if self.right:
            self.right.PrintTree()


root_node = Node(-1, 0, True)
for b in bins:
    b = int(b.strip(), 2)
    root_node.insert(b, bits)

root_node.PrintTree()

# traverse
O2 = ''
curr_node = root_node
for ratio in ratios:
    if ratio >= 0.5:
        curr_node = curr_node.right
    else:
        curr_node = curr_node.left
    O2 += str(curr_node.number)
    if curr_node.children in [0, 1]:
        break
# continue traversal
while (curr_node.left is not None) or (curr_node.right is not None):
    if curr_node.left is not None:
        curr_node = curr_node.left
    else:
        curr_node = curr_node.right
    O2 += str(curr_node.number)

print(O2)
