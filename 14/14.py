#!/usr/bin/env python

import collections

import util


with open(util.input_file) as f:
    lines = [l.strip() for l in f.readlines()]

    sequence = [c for c in lines[0]]

    def parse_rule(line):
        return line.split(' -> ')

    rules = tuple((parse_rule(line) for line in lines[2:]))


def process_step():
    offset = 0
    for i in range(len(sequence) - 1):
        current = sequence[i + offset]
        next_char = sequence[i + offset + 1]

        current_seq = current + next_char
        for seq, insertion_char in rules:
            if not seq == current_seq:
                continue
            sequence.insert(i + offset + 1, insertion_char)
            offset += 1


for _ in range(10):
    process_step()


quantities = collections.defaultdict(int)

for c in sequence:
    quantities[c] += 1

max_count = max(quantities.values())
min_count = min(quantities.values())

diff = max_count - min_count

print(f'{max_count=} {min_count=} {diff=}')
