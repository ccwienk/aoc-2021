#!/usr/bin/env python

import util

with open(util.input_file) as f:
    numbers = [[int(c) for c in line.strip()] for line in f.readlines()]

rows = len(numbers)
cols = len(numbers[0])

risk_level_sum = 0

print(f'{rows=} {cols=}')

for x, line in enumerate(numbers):
    for y, num in enumerate(line):
        # check above
        if x > 0:
            if numbers[x-1][y] <= num:
                continue # not a "lowpoint"

        # check below
        if x < (rows - 1):
            if numbers[x+1][y] <= num:
                continue # not a "lowpoint"

        # check left
        if y > 0:
            if numbers[x][y-1] <= num:
                continue # not a "lowpoint"

        # check right
        if y < (cols - 1):
            numbers[x]
            if numbers[x][y+1] <= num:
                continue # not a "lowpoint"

        # found a "lowpoint"
        risk_level_sum += num + 1


print(f'{risk_level_sum=}')
