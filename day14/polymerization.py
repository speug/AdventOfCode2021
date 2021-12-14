from collections import defaultdict
import numpy as np
input_str = """NNCB

CH -> B
HH -> N
CB -> H
NH -> C
HB -> C
HC -> B
HN -> C
NN -> C
BH -> H
NC -> B
NB -> B
BN -> B
BB -> N
BC -> B
CC -> N
CN -> C
""".split('\n')

with open('input', 'r') as f:
    input_str = f.readlines()

initial_state_str = input_str[0].strip()
state = defaultdict(int)
for i in range(len(initial_state_str) - 1):
    pair = initial_state_str[i:i+2]
    state[pair] += 1
insertion_rules = input_str[2:]
insertion_rules = [(x.split(' -> ')[0], x.split(' -> ')[1].strip('\n'))
                   for x in insertion_rules if x not in ['', '\n']]


def do_insertions(state, insertion_rules):
    new_state = state.copy()
    additions = defaultdict(int)
    for target, injection in insertion_rules:
        if target in state:
            num_original_pair = state[target]
            pair1 = target[0] + injection
            pair2 = injection + target[1]
            additions[pair1] += num_original_pair
            additions[pair2] += num_original_pair
            new_state[target] = 0
    for k, v in additions.items():
        new_state[k] += v
    return new_state


def count_appearances(state):
    apps = defaultdict(int)
    pairs_present = {k: v for k, v in state.items() if v != 0}
    for pair, number in pairs_present.items():
        apps[pair[0]] += number
        apps[pair[1]] += number
    apps = {k: v // 2 if v % 2 == 0 else v // 2 + 1 for k, v in apps.items()}
    return apps


def score(state):
    apps = count_appearances(state)
    max_count = 0
    min_count = np.inf
    for elem_count in apps.values():
        if elem_count > max_count:
            max_count = elem_count
        elif elem_count < min_count:
            min_count = elem_count
    score = max_count - min_count
    return score


for i in range(40):
    state = do_insertions(state, insertion_rules)
    if i == 9:
        print(f'step {i+1}: {count_appearances(state)} (score {score(state)})')

print(f'step 40: {count_appearances(state)} (score {score(state)})')
