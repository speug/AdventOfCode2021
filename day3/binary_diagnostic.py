import numpy as np

# get input
with open('input', 'r') as f:
    bins = f.readlines()

#bins = [
    #'00100',
    #'11110',
    #'10110',
    #'10111',
    #'10101',
    #'01111',
    #'00111',
    #'11100',
    #'10000',
    #'11001',
    #'00010',
    #'01010',
#]


def get_ratios(bins):
    bits = len(bins[0].strip())  # have to strip the newline
    n_bins = len(bins)
    one_counts = np.zeros(bits)

    for b in bins:
        b = int(b.strip(), 2)  # get binary repr
        for i in range(bits):
            shifted = b >> i
            one_counts[i] += shifted & 1

    ratios = list(reversed([x/n_bins for x in one_counts]))
    return ratios


ratios = get_ratios(bins)
gamma = ''.join(['0' if x < 0.5 else '1' for x in ratios])
epsilon = ''.join(['0' if x > 0.5 else '1' for x in ratios])
print('Part 1:')
print(f'Gamma: {gamma} ({int(gamma, 2)}), epsilon: {epsilon} ({int(epsilon, 2)})')
print(f'Product: {int(gamma, 2) * int(epsilon, 2)}')

# part 2
# the ratios are nice


def filter_list(bins, type):
    ri = 0
    while len(bins) > 1:
        ratios = get_ratios(bins)
        del_indices = []
        for i in range(len(bins)):
            bit_at_pos = bins[i][ri]
            if type == 'O2':
                if (ratios[ri] >= 0.5) and (bit_at_pos == '0'):
                    del_indices.append(i)
                elif (ratios[ri] < 0.5) and (bit_at_pos == '1'):
                    del_indices.append(i)
            elif type == 'CO2':
                if (ratios[ri] >= 0.5) and (bit_at_pos == '1'):
                    del_indices.append(i)
                elif (ratios[ri] < 0.5) and (bit_at_pos == '0'):
                    del_indices.append(i)
        for di in reversed(del_indices):
            del bins[di]
        ri += 1
    return bins[0]


O2 = filter_list(bins.copy(), 'O2')
CO2 = filter_list(bins.copy(), 'CO2')
print(f'O2 rating: {O2} ({int(O2, 2)}, CO2 rating: {CO2} ({int(CO2, 2)})')
print(f'Product of ratings: {int(O2, 2) * int(CO2, 2)}')
