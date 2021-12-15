#!/usr/bin/env python

import dataclasses

import util

with open(util.input_file) as f:
    numbers = [[int(c) for c in line.strip()] for line in f.readlines()]

rows = len(numbers)
cols = len(numbers[0])

start = (0, 0)
tgt = (rows, cols) # bottom right

def risk(point: tuple[int, int]):
    return numbers[point[0]][point[1]]


@dataclasses.dataclass
class Node:
    coords: tuple[int, int]
    cost: int
    tentative_dist: int # costs back to initial node
    best_neighbour: 'Node'

    def __eq__(self, other):
        return self.coords == other.coords

    def __hash__(self):
        return hash(self.coords)


def neighbours(point: tuple[int, int]):
    x, y = point
    # top
    if x > 0:
        yield (x - 1, y)
    # left
    if y > 0:
        yield (x, y - 1)
    # bottom
    if x + 1 < rows:
        yield (x + 1, y)
    # right
    if y + 1 < cols:
        yield (x, y + 1)


def neighbour_nodes(node):
    for point in neighbours(node.coords):
        yield nodes[point]


nodes = {}

for y in range(cols):
    for x in range(rows):
        coord = (x, y)
        cost = risk(coord)
        node = Node(
            coords=coord,
            cost=cost,
            tentative_dist=None,
            best_neighbour=None
        )

        nodes[coord] = node

unvisited = {n for n in nodes.values()}
initial = nodes[0,0]
tgt = nodes[(rows - 1, cols - 1)]
initial.tentative_dist = 0
cur = initial

# dijkstra's algorithm (yes, I typed this after reading the wikipedia article)
while True:
    for nn in neighbour_nodes(node=cur):
        if not nn in unvisited:
            continue
        # consider only unvisited neighbours

        new_tentative_dist = cur.tentative_dist + nn.cost

        if nn.tentative_dist is None or nn.tentative_dist > new_tentative_dist:
            nn.tentative_dist = new_tentative_dist

    unvisited.remove(cur)

    cur = min(
        (n for n in unvisited if n.tentative_dist is not None),
        key=lambda n: n.tentative_dist
    )

    if cur == tgt:
        break


print(f'{cur.tentative_dist=}')
