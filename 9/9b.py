#!/usr/bin/env python

import util

with open(util.input_file) as f:
    numbers = [[int(c) for c in line.strip()] for line in f.readlines()]

rows = len(numbers)
cols = len(numbers[0])

risk_level_sum = 0
low_points: set[tuple[int, int]] = set()

print(f'{rows=} {cols=}')

for x, line in enumerate(numbers):
    for y, num in enumerate(line):
        # check above
        if x > 0:
            if numbers[x-1][y] <= num:
                continue # not a "lowpoint"

        # check below
        if x < (rows - 1):
            if numbers[x+1][y] <= num:
                continue # not a "lowpoint"

        # check left
        if y > 0:
            if numbers[x][y-1] <= num:
                continue # not a "lowpoint"

        # check right
        if y < (cols - 1):
            numbers[x]
            if numbers[x][y+1] <= num:
                continue # not a "lowpoint"

        # found a "lowpoint"
        risk_level_sum += num + 1
        low_points.add((x, y))


print(f'{risk_level_sum=}')
print(f'{len(low_points)=}')


iterations = 0

def iter_neighbours(point: tuple[int, int], visited_points: set[tuple[int, int]]):
    x, y = point

    global iterations
    iterations += 1
    #print(iterations)

    neighbours = set()

    # top neighbour
    if x > 0:
        p = (x - 1, y)
        if not p in visited_points and numbers[p[0]][p[1]] < 9:
            neighbours.add(p)
            yield p

    # bottom neighbour
    if x < (rows - 1):
        p = (x + 1, y)
        if not p in visited_points and numbers[p[0]][p[1]] < 9:
            neighbours.add(p)
            yield p


    # left neighbour
    if y > 0:
        p = (x , y - 1)
        if not p in visited_points and numbers[p[0]][p[1]] < 9:
            neighbours.add(p)
            yield p

    # right neighbour
    if y < (cols - 1):
        p = (x, y + 1)
        if not p in visited_points and numbers[p[0]][p[1]] < 9:
            neighbours.add(p)
            yield p

    for neighbour in neighbours:
        visited_points |= neighbours
        yield from iter_neighbours(point=neighbour, visited_points=visited_points)


basin_sizes = set()

for idx, point in enumerate(low_points):
    visited = set()
    size = len(set(iter_neighbours(point=point, visited_points=visited)))
    basin_sizes.add(size)

basin_sizes = sorted(basin_sizes)[-3:]

multiplied_sizes = basin_sizes[0] * basin_sizes[1] * basin_sizes[2]

print(f'{basin_sizes=} {len(basin_sizes)=} {multiplied_sizes=}')
