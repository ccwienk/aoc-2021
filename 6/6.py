#!/usr/bin/env python

import util

with open(util.input_file) as f:
    timers = [int(l) for l in f.read().strip().split(',')]


def process_day(timers: list[int]):
    appended_fish = []

    for value in timers:
        if value > 0:
            yield value - 1
        elif value == 0: # will become 0 -> emit an additional "fish"
            yield 6
            appended_fish.append(8)

    yield from appended_fish


for d in range(80):
    timers = process_day(timers=timers)

print(f'{len(tuple(timers))}')
