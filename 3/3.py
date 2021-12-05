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
        raise RuntimeError('amounts are equal')

def invert(one_or_zero):
    if one_or_zero == 0:
        return 1
    elif one_or_zero == 1:
        return 0
    else:
        raise ValueError(one_or_zero)


gamma_rate_bits = [most_common_bit(lines=lines, idx=i) for i in range(cols)]
epsilon_rate_bits = [invert(most_common_bit(lines=lines, idx=i)) for i in range(cols)]

def to_decimal(binary_ints):
    number_str = ''.join(map(str, binary_ints))
    return int(number_str, base=2)

gamma_rate = to_decimal(gamma_rate_bits)
epsilon_rate = to_decimal(epsilon_rate_bits)

power = gamma_rate * epsilon_rate

print(f'{power=} {gamma_rate=} {epsilon_rate=}')
