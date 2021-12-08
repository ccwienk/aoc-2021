#!/usr/bin/env python3.10

import dataclasses
import itertools

import util

with open(util.input_file) as f:
    lines = [l.strip() for l in f.readlines()]


@dataclasses.dataclass
class Entry:
    patterns: list[str]
    output: list[str]

    def iter_all(self):
        yield from self.patterns
        yield from self.output


def parse_entry(line: str):
    patterns, output = line.split(' | ')
    patterns = patterns.split(' ')
    output = output.split(' ')

    return Entry(
        patterns=patterns,
        output=output,
    )


def is_one_of_1_4_7_8(pattern: str):
    return len(pattern) in (2, 4, 3, 7)

#  000
# 1   2
# 1   2
#  333
# 4   5
# 4   5
#  666

S_0 = {0, 1, 2,    4, 5, 6} # 6
S_1 = {      2,       5   } # 2
S_2 = {0,    2, 3, 4,    6} # 5
S_3 = {0,    2, 3,    5, 6} # 5
S_4 = {1, 2, 3,       5   } # 4
S_5 = {0, 1,    3,    5, 6} # 5
S_6 = {0, 1,    3, 4, 5, 6} # 6
S_7 = {0, 2,          5   } # 3
S_8 = {0, 1, 2, 3, 4, 5, 6} # 7
S_9 = {0, 1, 2, 3,    5, 6} # 6

valid_patterns = (S_0, S_1, S_2, S_3, S_4, S_5, S_6, S_7, S_8, S_9)

entries = [parse_entry(line) for line in lines]

print(f'{len(entries)=}')

def determine_value(entry: Entry):
    candidates = {
        'a': {0, 1, 2, 3, 4, 5, 6},
        'b': {0, 1, 2, 3, 4, 5, 6},
        'c': {0, 1, 2, 3, 4, 5, 6},
        'd': {0, 1, 2, 3, 4, 5, 6},
        'e': {0, 1, 2, 3, 4, 5, 6},
        'f': {0, 1, 2, 3, 4, 5, 6},
        'g': {0, 1, 2, 3, 4, 5, 6},
    }

    for pattern in entry.iter_all():
        match len(pattern):
            case 2:
                first, second = pattern
                # displayed digit is a `one`
                candidates[first] &= S_1
                candidates[second] &= S_1
            case 3:
                first, second, third = pattern
                # displayed digit is a `seven`
                candidates[first] &= S_7
                candidates[second] &= S_7
                candidates[third] &= S_7
            case 4:
                first, second, third, fourth = pattern
                # displayed digit is a `four`
                candidates[first] &= S_4
                candidates[second] &= S_4
                candidates[third] &= S_4
                candidates[fourth] &= S_4


    candidates_for_one = set()

    for k,v in candidates.items():
        if len(v) == 2:
            candidates_for_one |= set(v)

    if not len(candidates_for_one) == 2:
        raise ValueError(f'xxx {candidates_for_one=} in {pattern=}')

    for k,v in candidates.items():
        if v == candidates_for_one:
            continue
        # since we have exactly two candidates for `one` (sections 2,5) they
        # cannot be mapped differently
        v -= candidates_for_one

    # filter out entries where there is already a unique mapping (only one candidate)
    for k,v in candidates.items():
        if not len(v) == 1:
            continue

        for ik,iv in candidates.items():
            if iv == v:
                continue
            iv -= v

    pairs = [v for v in candidates.values() if len(v) == 2]

    for pair in pairs:
        if len([p for p in pairs if p == pair]) < 2:
            continue

        # as pair is complementary, the contained candidates cannot be candidates elsewhere
        for k,v in candidates.items():
            if v == pair:
                continue
            else:
                v -= pair

    found_conflict = False

    for a,b,c,d,e,f,g in itertools.product(*candidates.values()):
        if len(set((a,b,c,d,e,f,g))) < 7:
            continue

        # check whether all patterns are valid
        mapping = {
        'a': a,
        'b': b,
        'c': c,
        'd': d,
        'e': e,
        'f': f,
        'g': g,
        }

        for pattern in entry.iter_all():
            segments = {mapping[c] for c in pattern}

            if not segments in valid_patterns:
                found_conflict = True
                break

        if found_conflict:
            found_conflict = False
            continue

        break # found it
    else:
        raise ValueError('xx did not find any valid mapping')

    def to_number(pattern):
        segment_ids = {mapping[char] for char in pattern}
        if segment_ids == S_0:
            return 0
        if segment_ids == S_1:
            return 1
        if segment_ids == S_2:
            return 2
        if segment_ids == S_3:
            return 3
        if segment_ids == S_4:
            return 4
        if segment_ids == S_5:
            return 5
        if segment_ids == S_6:
            return 6
        if segment_ids == S_7:
            return 7
        if segment_ids == S_8:
            return 8
        if segment_ids == S_9:
            return 9

    value = 0
    for i, pattern in enumerate(reversed(entry.output)):
        value += to_number(pattern) * (10 ** i)

    return value

total = sum((determine_value(entry) for entry in entries))

print(f'{total=}')
