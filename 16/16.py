#!/usr/bin/env python

import dataclasses
import enum

import util

with open(util.input_file) as f:
    hexchars = f.read().strip()


def hex_to_bits(char: str):
    binary_digits = bin(int(char, base=16))[2:].zfill(4)
    #yield from (int(c) for c in binary_digits)
    yield from binary_digits


def iter_bits():
    for char in hexchars:
        yield from hex_to_bits(char)

bits = tuple((b for b in iter_bits()))


def parse_bits(bits) -> int:
    number_str = ''.join(bits)
    return int(number_str, base=2)


offset = 0
version_sum = 0


@dataclasses.dataclass
class HeaderInfo:
    version: int
    type_num: int

    def literal(self) -> bool:
        return self.type_num == 4


def parse_packet_header(bits):
    offset = 0
    version_bits = bits[offset: offset+3]
    version = parse_bits(version_bits)
    offset += 3

    type_bits = bits[offset: offset+3]
    type_num = parse_bits(type_bits)
    offset += 3

    info = HeaderInfo(
        version=version,
        type_num=type_num,
    )

    return bits[offset:], info


def parse_literal(bits):
    offset = 0
    number_bits = []
    while True:
        prefix = bits[offset]
        offset += 1
        number_bits += bits[offset: offset+4]
        offset += 4

        if prefix == '0':
            break

    number = int(''.join(number_bits), base=2)
    print(f'{number=}')

    return bits[offset:], number


def parse_operator(bits):
    offset = 0
    length_type = bits[offset]
    offset += 1

    match length_type:
        case '0':
            # next 15 bits are subpackets "immediately contained"
            subpackage_length_bits = bits[offset: offset+15]
            offset += 15
            subpackage_length_bits = int(''.join(subpackage_length_bits), base=2)
            return bits[offset:], subpackage_length_bits
        case '1':
            # next 11 bits are number of subpackets "immediately contained"
            subpackage_count_bits = bits[offset: offset+11]
            offset += 11
            subpackage_count = int(''.join(subpackage_count_bits), base=2)
            return bits[offset:], subpackage_count

version_sum = 0

while True:
    if len(bits) < 6:
        break # package-header has six bits

    bits, info = parse_packet_header(bits=bits)

    version_sum += info.version

    if not bits:
        break

    # ignore trailing zeroes
    if len(bits) < 3 and set(bits) == {'0'}:
        break

    if info.literal():
        bits, number = parse_literal(bits=bits)
        if not bits:
            break
        continue

    # operator
    bits, _ = parse_operator(bits)
    if not bits:
        break

print(version_sum)
