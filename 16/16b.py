#!/usr/bin/env python

import dataclasses
import enum
import operator

import util

with open(util.input_file) as f:
    hexchars = f.read().strip()


def hex_to_bits(char: str):
    binary_digits = bin(int(char, base=16))[2:].zfill(4)
    #yield from (int(c) for c in binary_digits)
    yield from binary_digits


def iter_bits(hexchars=hexchars):
    for char in hexchars:
        yield from hex_to_bits(char)

bits = tuple((b for b in iter_bits()))


def parse_bits(bits) -> int:
    number_str = ''.join(bits)
    return int(number_str, base=2)


offset = 0
version_sum = 0

# type-ids:
# 0: sum(*)
# 1: product(*)
# 2: min(*)
# 3: max(*)
# 4: - literal
# 5: a > b? -  1 if a > b else 0
# 6: a < b?
# 7: a == b?


@dataclasses.dataclass
class HeaderInfo:
    version: int
    type_num: int

    def literal(self) -> bool:
        return self.type_num == 4

    def __str__(self):
        match self.type_num:
            case 0:
                return 'sum('
            case 1:
                return 'product('
            case 2:
                return 'min('
            case 3:
                return 'max('
            case 4:
                return 'literal'
            case 5:
                return 'gt('
            case 6:
                return 'lt('
            case 7:
                return 'eq('

    def __repr__(self):
        return self.__str__()


@dataclasses.dataclass
class OperatorInfo:
    length_type: str # '0': length in bits, '1' number of subpackets
    argleng: int # semantics depends on type


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
            op_info = OperatorInfo(
                length_type='0',
                argleng=subpackage_length_bits,
            )
            return bits[offset:], op_info
        case '1':
            # next 11 bits are number of subpackets "immediately contained"
            subpackage_count_bits = bits[offset: offset+11]
            offset += 11
            subpackage_count = int(''.join(subpackage_count_bits), base=2)
            op_info = OperatorInfo(
                length_type='1',
                argleng=subpackage_count,
            )
            return bits[offset:], op_info

version_sum = 0

cmd_str = ''

# 0: sum(*)
# 1: product(*)
# 2: min(*)
# 3: max(*)
# 4: - literal
# 5: a > b? -  1 if a > b else 0
# 6: a < b?
# 7: a == b?

typecodes = {
    '0': 'sum',
    '1': 'mult',
    '2': 'min',
    '3': 'max',
    '4': 'literal',
    '5': 'gt',
    '6': 'lt',
    '7': 'eq',
}


def opfunc(info: HeaderInfo):
    match info.type_num:
        case 0:
            op = sum
        case 1:
            def op(args):
                p = 1
                for a in args:
                    p *= a
                return p
        case 2:
            op = min
        case 3:
            op = max
        case 4:
            op = None # literal
        case 5:
            op = lambda a_b : 1 if a_b[0] > a_b[1] else 0
        case 6:
            op = lambda a_b : 1 if a_b[0] < a_b[1] else 0
        case 7:
            op = lambda a_b : 1 if a_b[0] == a_b[1] else 0

    return op


def read_one_package(bits):
    bits, info = parse_packet_header(bits=bits)
    print(f'{len(bits)=} {info=}')

    if info.literal():
        bits, value = parse_literal(bits=bits)
        print(f'literal: {value=}')

        return bits, value

    bits, op_info = parse_operator(bits)

    op_fnc = opfunc(info)

    if op_info.length_type == '0':
        subpackage_bits = bits[:op_info.argleng]

        bits = bits[op_info.argleng:]

        args = []
        while True:
            subpackage_bits, value = read_one_package(bits=subpackage_bits)
            args.append(value)

            if not subpackage_bits:
                break

            # ignore trailing zeroes
            if len(subpackage_bits) < 3 and set(subpackage_bits) == {'0'}:
                break

        print(f'{args=}')
        return bits, op_fnc(args)

    # length_type '1' - n packages
    args = []
    for _ in range(op_info.argleng):
        bits, value = read_one_package(bits)
        args.append(value)

        # ignore trailing zeroes
        if len(bits) < 3 and set(bits) == {'0'}:
            break

    return bits, op_fnc(args)


_, result = read_one_package(bits=bits)

print(result)
