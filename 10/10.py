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

                # found an illegal character
                match c:
                    case ')':
                        return 3
                    case ']':
                        return 57
                    case '}':
                        return 1197
                    case '>':
                        return 25137
    else:
        return 0 # line was incomplete


total_score = sum((parse_line(line) for line in lines))

print(f'{total_score=}')
