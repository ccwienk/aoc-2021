#!/usr/bin/env python3.10

import collections

import util

with open(util.input_file) as f:
    lines = [l.strip() for l in f.readlines()]


opening_chars = ('(', '[', '{', '<')
closing_chars = (')', ']', '}', '>')


def parse_line(line: str):
    tokens = collections.deque()

    for idx,c in enumerate(line):
        match c:
            case c if c in opening_chars:
                tokens.append(c)
            case c if c in closing_chars:
                expected_token = closing_chars[opening_chars.index(tokens.pop())]
                if c == expected_token:
                    continue

                # found an illegal character - ignore line
                return 0

    # line is incomplete
    char_scores = {'(': 1, '[': 2, '{': 3, '<': 4}
    total = 0

    while tokens and (token := tokens.pop()):
        total *= 5
        total += char_scores[token]

    return total


scores = ((parse_line(line) for line in lines))
scores = sorted(s for s in scores if s > 0)


middle_score = scores[int(len(scores)/2)]

print(f'{middle_score=}')
