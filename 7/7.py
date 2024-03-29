#!/usr/bin/env python

import util

with open(util.input_file) as f:
    positions = tuple(int(num) for num in f.read().strip().split(','))

min_pos = min(positions)
max_pos = max(positions)

def costs(positions, tgt_pos: int):
    c = 0
    for pos in positions:
        c += abs(pos - tgt_pos)

    return c


all_costs = {
    pos: costs(positions=positions, tgt_pos=pos) for pos in range(min_pos, max_pos + 1)
}

cheapest = min(all_costs.values())

print(cheapest)
