#!/usr/bin/env python

import itertools

import util

with open(util.input_file) as f:
  numbers = [[int(c) for c in line.strip()] for line in f.readlines()]

rows = len(numbers)
cols = len(numbers[0])


def adjacent_points(x, y):
  # upper left
  if x > 0 and y > 0:
    yield (x - 1, y - 1)
  # up
  if x > 0:
    yield (x - 1, y)
  # upper right
  if x > 0 and y < cols - 1:
    yield (x - 1, y + 1)
  # left
  if y > 0:
    yield (x, y - 1)
  # lower left
  if y > 0 and x < rows - 1:
    yield (x + 1, y - 1)
  # lower
  if x < rows - 1:
    yield (x + 1, y)
  # lower right
  if x < rows - 1 and y < cols -1:
    yield (x + 1, y + 1)
  # right
  if y < cols -1:
    yield (x, y + 1)


flashed_points = set()


def flash_and_propagate(x, y):
  if (x, y) in flashed_points:
    return

  flashed_points.add((x,y))

  for point in adjacent_points(x, y):
    ax, ay = point
    numbers[ax][ay] += 1
    if numbers[ax][ay] > 9:
      if not (ax, ay) in flashed_points:
        flash_and_propagate(ax, ay)


def simulate_step() -> int:
  reached_ten = set()

  for x, y in itertools.product(range(rows), range(cols)):
    numbers[x][y] += 1
    if numbers[x][y] == 10:
      reached_ten.add((x, y))

  for x, y in reached_ten:
    flash_and_propagate(x, y)

  while True:
    remaining = set()
    for x, y in itertools.product(range(rows), range(cols)):
      if numbers[x][y] > 9 and (x,y) not in flashed_points:
        remaining.add((x, y))

    for x,y in remaining:
      flash_and_propagate(x, y)

    if not remaining:
      break

  flushes = len(flashed_points)

  # reset flashed
  for x, y in flashed_points:
    numbers[x][y] = 0

  return flushes

step = 0

while True:
  count = simulate_step()
  step += 1
  if count == rows * cols:
      break
  flashed_points.clear()

print(f'synced at {step=}')
