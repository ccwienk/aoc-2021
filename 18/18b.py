#!/usr/bin/env python

import copy
import itertools
import math
import typing

import util

with open(util.input_file) as f:
    numbers = [eval(l.strip()) for l in f.readlines()]


def add(a, b):
    return [a, b]


def element(numbers: list, index_path: typing.Iterable[int]):
    if len(index_path) == 1:
        return numbers[index_path[0]]
    elif len(index_path) == 0:
        return numbers

    return element(numbers[index_path[0]], index_path[1:])


def set_element(numbers: list, index_path: typing.Iterable[int], value):
    parent_list = element(numbers, index_path[:-1])
    parent_list[index_path[-1]] = value


def add_to_element(numbers: list, index_path: typing.Iterable[int], value: int):
    tgt_value = element(numbers, index_path) + value

    set_element(numbers=numbers, index_path=index_path, value=tgt_value)

    return tgt_value


def iter_element_paths(numbers, path=()):
    '''
    yields all paths to regular numbers (skipping over nested lists)
    '''
    if not path:
        root = numbers
    else:
        root = element(numbers, path)

    for idx, value in enumerate(root):
        if isinstance(value, int):
            yield path + (idx,)
        else:
            yield from iter_element_paths(numbers, path + (idx,))


def find_number_path_to_left(numbers, path):
    all_paths = reversed(tuple(iter_element_paths(numbers=numbers, path=())))

    reached_path = False
    for p in all_paths:
        if reached_path:
            return p

        if p != path:
            continue
        else:
            reached_path = True


def find_number_path_to_right(numbers, path):
    all_paths = iter_element_paths(numbers=numbers, path=())

    reached_path = False
    for p in all_paths:
        if reached_path:
            return p

        if p != path:
            continue
        else:
            reached_path = True


def first_pair_nested_4(numbers):
    for p in iter_element_paths(numbers, path=()):
        if len(p) == 5:
            break
    else:
        return None

    return p[:-1]


def explode(numbers):
    explosions = 0

    while (path_to_nested := first_pair_nested_4(numbers)):
        left, right = element(numbers, path_to_nested)
        parent_path = path_to_nested[:-1]
        parent = element(numbers, parent_path)

        # add to first sibling to the left
        if (left_path := find_number_path_to_left(numbers, path=path_to_nested + (0,))):
            add_to_element(numbers, index_path=left_path, value=left)

        # add to first sibling to the right
        if (right_path := find_number_path_to_right(numbers, path=path_to_nested + (1,))):
            add_to_element(numbers, index_path=right_path, value=right)

        # replace ourselves w/ 0
        set_element(numbers, path_to_nested, 0)

        explosions += 1

    return numbers


def split(numbers):
    # find first regular number >= 10
    for path in iter_element_paths(numbers):
        value = element(numbers, path)
        if value < 10:
            continue
        break
    else:
        return numbers, False # no number >= 10

    def new_element(number):
        return [int(number / 2), math.ceil(number/2)]

    set_element(numbers, path, new_element(value))
    return numbers, True


def reduce(numbers):
    while True:
        # explode will explode until there is nothing more to explode
        numbers = explode(numbers)

        numbers, did_split = split(numbers)
        if did_split:
            continue
        else:
            break # if nothig was split, there are no more explosions tbd

    return numbers


def magnitude(pair_or_number):
    match pair_or_number:
        case left, right:
            return (3 * magnitude(left)) + (2 * magnitude(right))
        case single:
            return single


max_magnitude = 0

for left, right in itertools.combinations(numbers, 2):
    lplusr = reduce(add(copy.deepcopy(left), copy.deepcopy(right)))
    rplusl = reduce(add(copy.deepcopy(right), copy.deepcopy(left)))

    lmag = magnitude(lplusr)
    rmag = magnitude(rplusl)

    max_magnitude = max(max_magnitude, lmag, rmag)


print(max_magnitude)
