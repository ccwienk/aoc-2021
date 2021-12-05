#!/usr/bin/env python

import collections
import dataclasses

import util

with open(util.input_file) as f:
    lines = tuple(l.strip() for l in f.readlines())


@dataclasses.dataclass(frozen=True)
class Point:
    x: int
    y: int


@dataclasses.dataclass
class Vector:
    src: Point
    tgt: Point

    def horizontal(self):
        return self.src.y == self.tgt.y

    def vertical(self):
        return self.src.x == self.tgt.x

    def orthogonal(self):
        return self.horizontal() or self.vertical()

    def iter_points(self):
        if self.horizontal():
            minx = min(self.src.x, self.tgt.x)
            maxx = max(self.src.x, self.tgt.x)

            for x in range(minx, maxx + 1):
                yield Point(x=x, y=self.src.y)
        elif self.vertical():
            miny = min(self.src.y, self.tgt.y)
            maxy = max(self.src.y, self.tgt.y)

            for y in range(miny, maxy + 1):
                yield Point(x=self.src.x, y=y)
        else:
            minx = min(self.src.x, self.tgt.x)
            maxx = max(self.src.x, self.tgt.x)

            srcx_smaller = self.src.x < self.tgt.x
            srcy_smaller = self.src.y < self.tgt.y

            for i in range(0, (maxx - minx) + 1):
                if srcx_smaller:
                    x = self.src.x + i
                else:
                    x = self.src.x - i

                if srcy_smaller:
                    y = self.src.y + i
                else:
                    y = self.src.y - i

                yield Point(x=x, y=y)


def parse_vector(line: str):
    left, right = line.split(' -> ')

    leftx, lefty = left.split(',')
    rightx, righty = right.split(',')

    left_point = Point(x=int(leftx), y=int(lefty))
    right_point = Point(x=int(rightx), y=int(righty))

    return Vector(src=left_point, tgt=right_point)


vectors = [parse_vector(line) for line in lines]

print(f'{len(vectors)=}')

coord_count = collections.defaultdict(int)

for ov in vectors:
    for point in ov.iter_points():
        coord_count[point] += 1


overlapping_points = [p for p,v in coord_count.items() if v > 1]

print(f'{len(overlapping_points)}')
