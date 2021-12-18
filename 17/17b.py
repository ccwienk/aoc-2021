#!/usr/bin/env python

# hardcode values from input, since there is not a lot of point in parsing..

tgt_x_min = 155
tgt_x_max = 215
tgt_y_min = -132
tgt_y_max = -72


def velocity_step(v: tuple[int, int]):
    x, y = v
    if x < 0:
        new_x = x + 1
    elif x > 0:
        new_x = x - 1
    else: # == 0
        new_x = x

    return (new_x, y - 1)


def iter_path(p: tuple[int, int], v:tuple[int, int]):
    px, py = p
    vx, vy = v

    while True:
        px, py = (px + vx, py + vy)
        vx, vy = velocity_step((vx, vy))
        yield (px, py)


def within_tgt(p: tuple[int, int]):
    x,y = p

    if x > tgt_x_max or x < tgt_x_min:
        return False
    if y > tgt_y_max or y < tgt_y_min:
        return False

    return True


allowed_x_range = (18, 215) # < 18 will never reach, > 215 will "overshoot"
allowed_y_range = (131, -65) # must not "overshoot"

ok_sum = 0

for initial_x in range(18, 400 + 1):
    for initial_y in range(-400, 300 +1):
        for p in iter_path(p=(0,0), v=(initial_x, initial_y)):
            x, y = p

            if y < tgt_y_min:
                #print(f'{x=},{y=} {initial_x=} too deep, already')
                break

            if x > tgt_x_max:
                # print('too far, already')
                break

            if within_tgt(p):
                #print(f'okay {initial_x=}')
                ok_sum += 1
                break


print(f'{ok_sum=}')
