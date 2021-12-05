#!/usr/bin/env python

import util

with open(util.input_file) as f:
    data = [int(l.strip()) for l in f.readlines()]

last = None
increments = 0

for d in data:
    if not last:
        last = d
        continue

    if last < d:
        increments += 1

    last = d

print(f'{increments=}')
