import os
from collections import namedtuple
from copy import copy
from datetime import datetime
from time import sleep

Map = namedtuple("Map", "height width numbers")
Point = namedtuple("Point", "x y")
Line = namedtuple("Line", "p1 p2")
StackElem = namedtuple("StackElem", "last_point first_path lines")
Number = namedtuple("Number", "p number")

maps = [
    Map(height=2, width=2,
        numbers=[
            Number(Point(0, 1), 3),
            Number(Point(1, 0), 3),
            Number(Point(1, 1), 2),
        ]),

    Map(height=2, width=3,
        numbers=[
            Number(Point(1, 0), 3),
            Number(Point(0, 1), 3),
            Number(Point(2, 1), 3),
        ]),

    Map(height=5, width=5,
        numbers=[
            Number(Point(1, 0), 3),
            Number(Point(4, 0), 1),
            Number(Point(0, 1), 0),
            Number(Point(3, 1), 2),
            Number(Point(4, 1), 1),
            Number(Point(1, 2), 2),
            Number(Point(3, 2), 2),
            Number(Point(2, 3), 3),
            Number(Point(4, 3), 1),
            Number(Point(0, 4), 1),
            Number(Point(2, 4), 2),
        ]),

    Map(height=6, width=6,
        numbers=[
            Number(Point(0, 0), 1),
            Number(Point(4, 0), 3),
            Number(Point(1, 1), 2),
            Number(Point(5, 1), 1),
            Number(Point(0, 2), 0),
            Number(Point(3, 2), 2),
            Number(Point(0, 3), 0),
            Number(Point(2, 3), 1),
            Number(Point(5, 3), 1),
            Number(Point(0, 4), 2),
            Number(Point(2, 4), 1),
            Number(Point(1, 5), 1),
            Number(Point(3, 5), 3),
            Number(Point(4, 5), 2),
        ]),

    Map(height=6, width=6,
        numbers=[
            Number(Point(2, 0), 3),
            Number(Point(3, 0), 3),
            Number(Point(0, 1), 2),
            Number(Point(1, 1), 2),
            Number(Point(3, 1), 1),
            Number(Point(2, 2), 2),
            Number(Point(3, 2), 2),
            Number(Point(5, 2), 1),
            Number(Point(0, 3), 0),
            Number(Point(3, 3), 2),
            Number(Point(2, 4), 1),
            Number(Point(5, 4), 3),
            Number(Point(0, 5), 3),
            Number(Point(4, 5), 2),
            Number(Point(5, 5), 1),
        ]),

    Map(height=6, width=6,
        numbers=[
            Number(Point(0, 0), 0),
            Number(Point(3, 0), 1),
            Number(Point(4, 0), 3),
            Number(Point(1, 1), 2),
            Number(Point(4, 1), 2),
            Number(Point(5, 1), 0),
            Number(Point(0, 2), 3),
            Number(Point(3, 2), 2),
            Number(Point(5, 2), 1),
            Number(Point(0, 3), 2),
            Number(Point(4, 3), 2),
            Number(Point(2, 4), 0),
            Number(Point(5, 4), 1),
            Number(Point(1, 5), 2),
            Number(Point(2, 5), 3),
            Number(Point(3, 5), 2),
        ]),

    Map(height=6, width=6,
        numbers=[
            Number(Point(2, 0), 0),
            Number(Point(5, 0), 3),
            Number(Point(0, 1), 0),
            Number(Point(2, 1), 1),
            Number(Point(4, 1), 2),
            Number(Point(2, 2), 2),
            Number(Point(4, 2), 1),
            Number(Point(5, 2), 2),
            Number(Point(1, 3), 2),
            Number(Point(3, 3), 3),
            Number(Point(0, 4), 2),
            Number(Point(5, 4), 1),
            Number(Point(1, 5), 2),
            Number(Point(2, 5), 1),
            Number(Point(4, 5), 2),
        ]),

    Map(height=6, width=6,
        numbers=[
            Number(Point(0, 0), 1),
            Number(Point(2, 0), 2),
            Number(Point(3, 0), 1),
            Number(Point(4, 0), 3),
            Number(Point(1, 1), 1),
            Number(Point(3, 1), 2),
            Number(Point(0, 2), 3),
            Number(Point(2, 2), 2),
            Number(Point(5, 2), 1),
            Number(Point(3, 3), 3),
            Number(Point(4, 3), 1),
            Number(Point(0, 4), 1),
            Number(Point(3, 4), 3),
            Number(Point(4, 4), 1),
            Number(Point(5, 4), 3),
            Number(Point(1, 5), 2),
        ]),
]

DIRECT = [
    (1, 0),
    (0, 1),
    (-1, 0),
    (0, -1),
]

SQUARE = [
    Line(Point(0, 0), Point(0, 1)),
    Line(Point(0, 1), Point(1, 1)),
    Line(Point(1, 1), Point(1, 0)),
    Line(Point(1, 0), Point(0, 0)),
]

CHECK_FAILED = 0
CHECK_SUCCESS = 1
CHECK_CONTINUE = 2


def debug_print(*s):
    pass
    # print(s)


def lineToPoints(lines):
    return [lines[0].p1] + [l.p2 for l in lines] if lines else []


def check(lines, line, map):
    path_points = lineToPoints(lines)
    if line.p2 in path_points:
        if line.p2 != lines[0].p1 or line.p2 == lines[-1].p1:
            return CHECK_FAILED

    exact = True
    for number in map.numbers:
        interset_len = count_line(lines + [line], number)
        if interset_len > number.number:
            return CHECK_FAILED
        if interset_len < number.number:
            exact = False

    if not exact and (lines and line.p2 == lines[0].p1):
        return CHECK_FAILED

    if exact and line.p2 == lines[0].p1:
        return CHECK_SUCCESS

    return CHECK_CONTINUE


def count_line(lines, number):
    p = number.p
    squares = [Line(Point(p.x + l.p1.x, p.y + l.p1.y),
                    Point(p.x + l.p2.x, p.y + l.p2.y)) for l in SQUARE]
    return len([1 for s in squares for li in lines
                if (s.p1 == li.p1 and s.p2 == li.p2) or (s.p2 == li.p1 and s.p1 == li.p2)])


def splash(map, path):
    os.system('cls' if os.name == 'nt' else 'clear')
    print_map(map, path)
    sleep(0.2)


def solve_task(args):
    map, stack = args
    task_id = "(" + str(stack[0].last_point.x) + \
        "," + str(stack[0].last_point.y) + ")"
    print("TASK " + str(task_id) + " STARED")
    while stack:
        p1 = stack[-1].last_point
        last_path = stack[-1].lines
        ok = False
        debug_print("For", p1, stack[-1].first_path,
                    "================", last_path)
        first_path = True
        for delta_x, delta_y in DIRECT:
            p2 = Point(p1.x + delta_x, p1.y + delta_y)
            if p2.x < 0 or p2.y < 0 or p2.x > map.width or p2.y > map.height:
                continue

            debug_print("   Check", p2)
            line = Line(p1, p2)
            check_result = check(last_path, line, map)
            debug_print('Checking', lineToPoints(last_path + [line]))

            splash(map, last_path + [line])

            if check_result == CHECK_CONTINUE:
                ok = True
                new_lines = copy(last_path)
                new_lines.append(line)
                debug_print('   Pushing', p2, first_path, new_lines)
                stack.append(StackElem(p2, first_path, new_lines))
                first_path = False
            elif check_result == CHECK_FAILED:
                pass
            elif check_result == CHECK_SUCCESS:
                debug_print('Found', last_path + [line])
                print_map(map, last_path + [line])
                print("TASK " + str(task_id) + " SUCCESS")
                return True
        if not ok:
            p = stack.pop()
            debug_print("Poping", p)
            while p.first_path and stack:
                debug_print("Poping parents:", p)
                p = stack.pop()

        debug_print("End for", p1, "==================", last_path)
    print("TASK " + str(task_id) + " FAILED")
    return False


def solve(map):
    for x in range(map.width + 1):
        for y in range(map.height + 1):
            solve_task((map, [StackElem(Point(x, y), True, [])]))


def solve_mp(map, pool_size=32):
    from multiprocessing import Pool
    tasks = [(map, [StackElem(Point(x, y), True, [])])
             for x in range(map.width + 1) for y in range(map.height + 1)]

    pool = Pool(pool_size)
    pool.map(solve_task, tasks)


def print_map(map, lines, size=5):
    pic = []  # array of string
    xline = bytearray()
    yline = bytearray()
    for j in range(map.width * (size + 1) + 1):
        xline += '-'
        if j % (size + 1) == 0:
            yline += '|'
        else:
            yline += ' '

    for i in range(map.height * (size + 1) + 1):
        if i % (size + 1) == 0:
            pic.append(copy(xline))
        else:
            pic.append(copy(yline))

    for line in lines:
        xr = line.p1.x - line.p2.x
        if xr == 0:  # vertical
            p = line.p1 if line.p2.y > line.p1.y else line.p2
            for s in range(size):
                pic[p.y * (size + 1) + 1 + s][p.x * (size + 1)] = 'x'
        else:
            p = line.p1 if line.p2.x > line.p1.x else line.p2
            for s in range(size):
                pic[p.y * (size + 1)][p.x * (size + 1) + 1 + s] = 'x'

    for num in map.numbers:
        pic[num.p.y * (size + 1) + (size + 1) / 2][num.p.x *
                                                   (size + 1) + (size + 1) / 2] = str(num.number)

    print("\n".join([str(l) for l in pic]))

if __name__ == "__main__":
    map = maps[-1]
    print_map(map, [])
    now = datetime.now()
    #solve_mp(map)
    solve(map)
    print("Time =", datetime.now() - now)
