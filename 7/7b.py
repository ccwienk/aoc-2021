#!/usr/bin/env python

import functools

import util

with open(util.input_file) as f:
    positions = tuple(int(num) for num in f.read().strip().split(','))

min_pos = min(positions)
max_pos = max(positions)


@functools.cache
def calc_distance_costs(distance):
    if distance < 2:
        return distance

    costs = 0

    for c in range(distance, 0, -1):
        costs += c

    return costs


def costs(positions, tgt_pos: int):
    c = 0
    for pos in positions:
        distance = abs(pos - tgt_pos)
        c += calc_distance_costs(distance=distance)

    return c


all_costs = {
    pos: costs(positions=positions, tgt_pos=pos) for pos in range(min_pos, max_pos + 1)
}

cheapest = min(all_costs.values())

print(f'{cheapest=}')
