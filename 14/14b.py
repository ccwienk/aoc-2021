#!/usr/bin/env python

import collections

import util


with open(util.input_file) as f:
    lines = [l.strip() for l in f.readlines()]

    sequence = [c for c in lines[0]]

    rules = {}
    pair_counts = collections.defaultdict(int)

    for i in range(len(sequence) - 1):
        c, n = sequence[i], sequence[i+1]
        pair_counts[c + n] += 1

    for line in lines[2:]:
        seq, c = line.split(' -> ')
        rules[seq] = c


char_quantities = collections.defaultdict(int)

for c in sequence:
    char_quantities[c] += 1


def process_step(pair_counts):
    global char_quantities

    new_pair_counts = pair_counts.copy()

    for pair, count in pair_counts.items():
        new_char = rules[pair]
        char_quantities[new_char] += count

        new_pair_counts[pair[0] + new_char] += count
        new_pair_counts[new_char + pair[1]] += count
        new_pair_counts[pair] -= count

    return new_pair_counts


def calc_diff(count, pair_counts):
    for i in range(count):
        # print(f'step {i} {len(sequence)=}')
        pair_counts = process_step(pair_counts)

    quantities = collections.defaultdict(int)

    max_count = max(char_quantities.values())
    min_count = min(char_quantities.values())

    print(f'{max_count=} {min_count=}')

    diff = max_count - min_count

    return diff, max_count + min_count

# diff = calc_diff(40, sequence)
# print(diff)

diff, s = calc_diff(count=40, pair_counts=pair_counts)
print(f'{diff=} {s=}')
