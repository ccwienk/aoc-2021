#!/usr/bin/env python

import collections
import itertools
import string

import util

with open(util.input_file) as f:
    lines = [l.strip() for l in f.readlines()]


def iter_nodes():
    for line in lines:
        left, right = line.split('-')
        if left not in ('start', 'end'):
            yield left
        if right not in ('start', 'end'):
            yield right

nodes = set(iter_nodes())
small = {n for n in nodes if n[0] in string.ascii_lowercase}
large = {n for n in nodes if n[0] in string.ascii_uppercase}

available_tgts = collections.defaultdict(set)

for line in lines:
    left, right = line.split('-')
    # start starts w/ lowercase, so it is never valid to go back to it
    # end must be at the end, and must only be visited once
    if right != 'start' and left != 'end':
        available_tgts[left].add(right)
    if left != 'start':
        available_tgts[right].add(left)


# each path is a tuple of visited nodes (first, second, .. last)
initial_path = 'start',

def iter_paths(path: tuple[str], double_visit_small_cave:str):
    current = path[-1]
    # available tgts are all accessible nodes w/o visited "small" ones, as those must only be
    # visited at most once
    available = available_tgts[current] - {n for n in small if n in path}
    if len(tuple(c for c in path if c == double_visit_small_cave)) < 2 and \
        double_visit_small_cave in available_tgts[current]:
        available.add(double_visit_small_cave)

    for next_node in available:
        new_path = path + (next_node,)
        if next_node == 'end':
            yield new_path
        else:
            yield from iter_paths(path=new_path, double_visit_small_cave=double_visit_small_cave)


all_paths = set()

for double_cave in small:
    all_paths |= set(iter_paths(path=initial_path, double_visit_small_cave=double_cave))

print(f'{len(all_paths)=}')
