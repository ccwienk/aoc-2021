#!/usr/bin/env python3.10

import dataclasses
import enum

import util

with open(util.input_file) as f:
    lines = f.readlines()


class Direction(enum.Enum):
    FWD = 'forward'
    DWN = 'down'
    UP = 'up'


@dataclasses.dataclass
class Instruction:
    direction: Direction
    value: int


def parse_line(line):
    direction, value = line.strip().split(' ')

    return Instruction(
        direction=Direction(direction),
        value=int(value)
    )

parsed_lines = [parse_line(line) for line in lines]

horizontal_pos = 0
depth = 0
aim = 0

for instruction in parsed_lines:
    match instruction.direction:
        case Direction.FWD:
            horizontal_pos += instruction.value
            depth += ( aim * instruction.value )
        case Direction.DWN:
            aim += instruction.value
        case Direction.UP:
            aim -= instruction.value


print(f'{horizontal_pos=} {depth=}')
