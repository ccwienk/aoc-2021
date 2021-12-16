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
    visited: bool = False

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
    if x + 1 < (rows * 5):
        yield (x + 1, y)
    # right
    if y + 1 < (cols * 5):
        yield (x, y + 1)


def neighbour_nodes(node):
    for point in neighbours(node.coords):
        yield nodes[point]


nodes = {}

for oy in range(5):
    y_offset = oy * rows
    for ox in range(5):
        x_offset = ox * cols
        # if oy == 0 and ox > 1:
        #     continue
        # if oy == 1 and ox > 2:
        #     continue
        # if oy == 2 and (ox < 1 or ox > 3):
        #     continue
        # if oy == 3 and ox < 2:
        #     continue
        # if oy == 4 and ox < 3:
        #     continue

        for y in range(cols):
            for x in range(rows):
                coord = (x_offset + x, y_offset + y)
                cost = risk((x, y)) + oy + ox
                if (cost % 9) == 0:
                    cost = 9
                else:
                    cost %= 9
                node = Node(
                    coords=coord,
                    cost=cost,
                    tentative_dist=None,
                    best_neighbour=None,
                    visited=False,
                )

                nodes[coord] = node

touched = set()
initial = nodes[0,0]
tgt = nodes[((rows * 5) - 1, (cols * 5) - 1)]
initial.tentative_dist = 0
cur = initial

print('running')
# dijkstra's algorithm (yes, I typed this after reading the wikipedia article)
while True:
    for nn in neighbour_nodes(node=cur):
        if nn.visited:
            continue
        # consider only unvisited neighbours

        # optimisation: keep in prio-set
        touched.add(nn)

        new_tentative_dist = cur.tentative_dist + nn.cost

        if nn.tentative_dist is None or nn.tentative_dist > new_tentative_dist:
            nn.tentative_dist = new_tentative_dist

    cur.visited = True
    if cur in touched:
        touched.remove(cur)
    print(len(touched))

    cur = min(
        (n for n in touched),
        key=lambda n: n.tentative_dist
    )

    if cur == tgt:
        break

print(f'{cur.tentative_dist=}')
