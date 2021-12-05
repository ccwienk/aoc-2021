#!/usr/bin/env python

import util

with open(util.input_file) as f:
    lines = [l.strip() for l in f.readlines()]

numbers_line = lines[0]
numbers = [int(n) for n in numbers_line.split(',')]

bingo_lines = lines[2:] # omit first two lines
bingo_columns = 5 # 5x5

drawn_numbers = set()

class BingoBoard:
    def __init__(self, rows):
        if not len(rows) == 5:
            raise ValueError(rows)

        def row_to_ints(row):
            row = row.replace('  ', ' ')
            return [int(e) for e in row.split(' ')]

        self.rows = [row_to_ints(row) for row in rows]

    def row_and_column_sets(self):
        for row in self.rows:
            yield set(row)

        for i in range(bingo_columns):
            yield set(row[i] for row in self.rows)

    def bingo(self):
        for numberset in self.row_and_column_sets():
            if (numberset & drawn_numbers) == numberset:
                return True
        return False

    def unmarked_sum(self):
        all_numbers = set()
        for row in self.rows:
            all_numbers |= set(row)

        all_numbers -= drawn_numbers

        return sum(all_numbers)



boards = []

for idx in range(0, len(bingo_lines), 6):
    bb = BingoBoard(bingo_lines[idx: idx+5])
    boards.append(bb)

print(len(boards))

score = None

for number in numbers:
    drawn_numbers.add(number)

    for board in boards:
        if not board.bingo():
            continue
        score = board.unmarked_sum() * number
        break
    if score:
        break


print(f'{score=}')
