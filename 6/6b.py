#!/usr/bin/env python3.10

import collections

import util

with open(util.input_file) as f:
    timers = [int(l) for l in f.read().strip().split(',')]

timers_dict = collections.defaultdict(int) # <timer_value>:<count>

for timer in timers:
    timers_dict[timer] += 1

def process_day(timers: dict[int, int]):
    new_timers = collections.defaultdict(int)

    for value in range(8, 0 - 1, -1):
        current_count = timers[value]

        match value:
            case 0:
                new_timers[6] += current_count # reset fish
                new_timers[8] = current_count
            case value if value > 0:
                new_timers[value - 1] = current_count
            case _:
                raise RuntimeError('should not happen')

    return new_timers


for d in range(256):
    timers_dict = process_day(timers=timers_dict)

fish_count = sum(timers_dict.values())
print(f'{fish_count=}')
