#!/usr/bin/env python

import dataclasses

import util

with open(util.input_file) as f:
    lines = [l.strip() for l in f.readlines()]


@dataclasses.dataclass
class Entry:
    patterns: list[str]
    output: list[str]


def parse_entry(line: str):
    patterns, output = line.split(' | ')
    patterns = patterns.split(' ')
    output = output.split(' ')

    return Entry(
        patterns=patterns,
        output=output,
    )


def is_one_of_1_4_7_8(pattern: str):
    return len(pattern) in (2, 4, 3, 7)


entries = [parse_entry(line) for line in lines]

print(f'{len(entries)=}')

unique_numbers = 0

for entry in entries:
    for output in entry.output:
        print(output)
        if is_one_of_1_4_7_8(output):
            unique_numbers += 1


print(f'{unique_numbers=}')
