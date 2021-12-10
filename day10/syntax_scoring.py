from statistics import median
correct_pairs = {
    '(': ')',
    '[': ']',
    '{': '}',
    '<': '>'
    }


def check_line(line, pairs):
    if not any(x in line for x in pairs.values()):
        return 'OK'
    for i in range(len(line) - 1):
        curr, next = (line[i], line[i+1])
        if (curr in pairs) and (next in pairs.values()):
            if next != pairs[curr]:
                return next
    return None


# lines = """[({(<(())[]>[[{[]{<()<>>
# [(()[<>])]({[<{<<[]>>(
# {([(<{}[<>[]}>{[]{[(<()>
# (((({<>}<{<{<>}{[]{[]{}
# [[<[([]))<([[{}[[()]]]
# [{[{({}]{}}([{[{{{}}([]
# {<[[]]>}<{[{[{[]{()[[[]
# [<(<(<(<{}))><([]([]()
# <{([([[(<>()){}]>(<<{{
# <{([{{}}[<[[[<>{}]]]>[]]
# """.split('\n')
with open('input', 'r') as f:
    lines = f.readlines()
errors = []
bad_lines = []
for i in range(len(lines)):
    line = lines[i]
    check = check_line(line, correct_pairs)
    while check is None:
        for op, clo in correct_pairs.items():
            pair = op + clo
            line = line.replace(pair, '')
            check = check_line(line, correct_pairs)
    if check != 'OK':
        errors.append(check)
        bad_lines.append(i)

scores = {')': 3, ']': 57, '}': 1197, '>': 25137}
error_scores = [scores[x] for x in errors]
print(f'Syntax score: {sum(error_scores)}')

# part 2
# filter out erroneous lines from above
lines = [x for i, x in enumerate(lines) if i not in bad_lines]
corrections = []
for i in range(len(lines)):
    # For each line:
    # 1. search all opening character indices
    # 2. for each opening character, look for the first closing pair.
    #    Remove that closing character from the set of available closing chars
    #    and move to the next opening character
    # 3. If no closing character was found, append the correct closing char
    #    to list of corrections.
    line = lines[i]
    opening_indices = [i for i in range(len(line)) if line[i] in correct_pairs]
    line_corrections = []
    used_closings = []
    for op_idx in reversed(opening_indices):
        has_closing = False
        for i in range(op_idx, len(line)):
            opening = line[op_idx]
            if (line[i] == correct_pairs[opening]) and (i not in used_closings):
                used_closings.append(i)
                has_closing = True
                break
        if not has_closing:
            line_corrections.append(correct_pairs[opening])
    if line_corrections:
        corrections.append(line_corrections)


def calculate_corr_score(corrs, corr_scores):
    score = 0
    for c in corrs:
        score *= 5
        score += corr_scores[c]
    return score


char_scores = {')': 1, ']': 2, '}': 3, '>': 4}
corr_scores = [calculate_corr_score(x, char_scores) for x in corrections]
print(f'Median correction score: {median(corr_scores)}')
