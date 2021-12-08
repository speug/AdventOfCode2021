with open('input', 'r') as f:
    lines = f.readlines()

n_sig = len(lines)
signals = [None] * n_sig
free_digits = [1, 4, 7, 8]
len_free = [2, 4, 3, 7]
num_free = 0
for i in range(n_sig):
    line = lines[i]
    diagnostic, output = line.split(' | ')
    diagnostic = [set(x.strip()) for x in diagnostic.split(' ')]
    output = [''.join(sorted(x.strip())) for x in output.split(' ')]
    signals[i] = (diagnostic, output)
    output_counts = [len(x) for x in output]
    num_free += sum([x in len_free for x in output_counts])
print(f'Number of free digits is {num_free}')


def find_by_intersection(a, int_size, diag):
    idx_out = next(i for i, x in enumerate(diag)
                   if len(a.intersection(x)) == int_size)
    out = diag.pop(idx_out)
    return out, diag


def decode_digits(diag):
    # decoding by intersection size
    # 4 ∩ 9 => 4
    # 9 ∩ 2 => 4
    # 2 ∩ 5 => 3
    # 5 ∩ 6 => 5
    # 6 ∩ 0 => 5
    # 6 ∩ 3 => 4
    counts = {len(x): x for x in diag}
    # first, retrieve free numbers
    out = {
        1: next(v for k, v in counts.items() if k == 2),
        4: next(v for k, v in counts.items() if k == 4),
        7: next(v for k, v in counts.items() if k == 3),
        8: next(v for k, v in counts.items() if k == 7)
    }
    for v in out.values():
        diag.remove(v)
    # then, use the intersection size table above to decode the rest
    out[9], diag = find_by_intersection(out[4], 4, diag)
    out[2], diag = find_by_intersection(out[9], 4, diag)
    out[5], diag = find_by_intersection(out[2], 3, diag)
    out[6], diag = find_by_intersection(out[5], 5, diag)
    out[0], diag = find_by_intersection(out[6], 5, diag)
    out[3] = diag[0]
    out = {k: ''.join(sorted(v)) for k, v in out.items()}
    out = {v: k for k, v in out.items()}
    return out


decoded = [None] * n_sig
for i in range(n_sig):
    diag, output = signals[i]
    # print(diag)
    # print(output)
    decoder = decode_digits(diag)
    # print(decoder)
    decoded_output = int(''.join([str(decoder[x]) for x in output]))
    decoded[i] = decoded_output
print(f'Sum of decoded: {sum(decoded)}')
