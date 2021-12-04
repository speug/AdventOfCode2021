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

