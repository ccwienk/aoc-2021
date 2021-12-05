#!/usr/bin/env python

import util

with open(util.input_file) as f:
    data = [int(l.strip()) for l in f.readlines()]

increments = 0
last_sum = None

for i in range(2, len(data)):
    a = data[i-2]
    b = data[i-1]
    c = data[i]
    new_sum = a + b + c

    if last_sum is None:
        last_sum = new_sum
        print('init' + str(i))
        continue

    if new_sum > last_sum:
        increments += 1

    last_sum = new_sum

print(f'{increments=}')
