#!/usr/bin/env python

import dataclasses
import functools

import util

coords = []
fold_instructions = []


with open(util.input_file) as f:
    reading_coords = True
    for line in f.readlines():
        line = line.strip()
        if not line:
            reading_coords = False
            continue

        if reading_coords:
            coords.append(tuple((int(n) for n in line.split(','))))
        else:
            instr = line.rsplit(' ', 1)[-1]
            dim, val = instr.split('=')
            val = int(val)

            fold_instructions.append((dim, val))


max_x = max(coords, key=lambda c: c[0])[0]
max_y = max(coords, key=lambda c: c[1])[1]

print(f'{max_x=}, {max_y=}')


def purge(dim, val):
    if dim == 'x':
        values_to_purge = [v for v in coords if v[0] == val]
    elif dim == 'y':
        values_to_purge = [v for v in coords if v[1] == val]

    for v in values_to_purge:
        coords.remove(v)


def calculate_new_x(val, coord):
    x,y = coord

    if x <= val:
        return coord

    new_x = val - x + val

    return (new_x, y)


def calculate_new_y(val, coord):
    x,y = coord

    if y <= val:
        return coord

    new_y = val - y + val

    return (x, new_y)


def fold(dim, val):
    global coords

    purge(dim=dim, val=val)

    if dim == 'y':
        y_mapper = functools.partial(calculate_new_y, val=val)
        coords = [y_mapper(coord=coord) for coord in coords]
    elif dim == 'x':
        x_mapper = functools.partial(calculate_new_x, val=val)
        coords = [x_mapper(coord=coord) for coord in coords]
    else:
        raise NotImplementedError(dim)

for dim, val in fold_instructions:
    fold(dim=dim, val=val)
    break # according to requirements, we shall only fold once

# deduplicate
unique_coords = set(coords)

print(f'{len(unique_coords)=}')
