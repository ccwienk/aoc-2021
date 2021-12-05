#!/usr/bin/env python

import util

with open(util.input_file) as f:
    lines = [l.strip() for l in f.readlines()]

cols = len(lines[0])


def most_common_bit(lines, idx):
    zeros = 0
    ones = 0
    for l in lines:
        c = int(l[idx])
        if c == 0:
            zeros += 1
        elif c == 1:
            ones += 1
        else:
            raise NotImplemented(c)

    if zeros > ones:
        return 0
    elif zeros < ones:
        return 1
    else:
        return None # equal amount


def invert(one_or_zero):
    if one_or_zero == 0:
        return 1
    elif one_or_zero == 1:
        return 0
    else:
        raise ValueError(one_or_zero)


def to_decimal(binary_ints):
    number_str = ''.join(map(str, binary_ints))
    return int(number_str, base=2)


def oxygen_gen_line(lines):
    lines = tuple(lines) # cp to not destroy values
    oxygen_line = None

    for i in range(cols):
        most_common = most_common_bit(lines=lines, idx=i)
        if most_common is None:
            most_common = 1

        lines = [l for l in lines if int(l[i]) == most_common]
        if len(lines) == 1:
            oxygen_line = lines[0]
            print('found oxygen_line')
            return oxygen_line
    else:
        raise RuntimeError('did not find oxygen-line')


def co2scrubber_gen_line(lines):
    lines = tuple(lines) # cp to not destroy values
    co2scrubber_line = None

    for i in range(cols):
        most_common = most_common_bit(lines=lines, idx=i)
        if most_common is None:
            least_common = 0
        else:
            least_common = invert(most_common)

        lines = [l for l in lines if int(l[i]) == least_common]
        if len(lines) == 1:
            co2scrubber_line = lines[0]
            print('found scrubber_line')
            return co2scrubber_line
    else:
        raise RuntimeError('did not find scrubber-line')


oxy_line = oxygen_gen_line(lines=lines)
co2_line = co2scrubber_gen_line(lines=lines)

oxy = int(oxy_line, base=2)
co2 = int(co2_line, base=2)

life_support = oxy * co2

print(f'{life_support=}')
