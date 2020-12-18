"""
--- Day 12: Rain Risk ---
Your ferry made decent progress toward the island, but the storm came in faster than anyone expected. The ferry needs to take evasive actions!

Unfortunately, the ship's navigation computer seems to be malfunctioning; rather than giving a route directly to safety, it produced extremely circuitous instructions. When the captain uses the PA system to ask if anyone can help, you quickly volunteer.

The navigation instructions (your puzzle input) consists of a sequence of single-character actions paired with integer input values. After staring at them for a few minutes, you work out what they probably mean:

Action N means to move north by the given value.
Action S means to move south by the given value.
Action E means to move east by the given value.
Action W means to move west by the given value.
Action L means to turn left the given number of degrees.
Action R means to turn right the given number of degrees.
Action F means to move forward by the given value in the direction the ship is currently facing.
The ship starts by facing east. Only the L and R actions change the direction the ship is facing. (That is, if the ship is facing east and the next instruction is N10, the ship would move north 10 units, but would still move east if the following action were F.)

For example:

F10
N3
F7
R90
F11
These instructions would be handled as follows:

F10 would move the ship 10 units east (because the ship starts by facing east) to east 10, north 0.
N3 would move the ship 3 units north to east 10, north 3.
F7 would move the ship another 7 units east (because the ship is still facing east) to east 17, north 3.
R90 would cause the ship to turn right by 90 degrees and face south; it remains at east 17, north 3.
F11 would move the ship 11 units south to east 17, south 8.
At the end of these instructions, the ship's Manhattan distance (sum of the absolute values of its east/west position and its north/south position) from its starting position is 17 + 8 = 25.

Figure out where the navigation instructions lead. What is the Manhattan distance between that location and the ship's starting position?

--- Part Two ---
Before you can give the destination to the captain, you realize that the actual action meanings were printed on the back of the instructions the whole time.

Almost all of the actions indicate how to move a waypoint which is relative to the ship's position:

Action N means to move the waypoint north by the given value.
Action S means to move the waypoint south by the given value.
Action E means to move the waypoint east by the given value.
Action W means to move the waypoint west by the given value.
Action L means to rotate the waypoint around the ship left (counter-clockwise) the given number of degrees.
Action R means to rotate the waypoint around the ship right (clockwise) the given number of degrees.
Action F means to move forward to the waypoint a number of times equal to the given value.
The waypoint starts 10 units east and 1 unit north relative to the ship. The waypoint is relative to the ship; that is, if the ship moves, the waypoint moves with it.

For example, using the same instructions as above:

F10 moves the ship to the waypoint 10 times (a total of 100 units east and 10 units north), leaving the ship at east 100, north 10. The waypoint stays 10 units east and 1 unit north of the ship.
N3 moves the waypoint 3 units north to 10 units east and 4 units north of the ship. The ship remains at east 100, north 10.
F7 moves the ship to the waypoint 7 times (a total of 70 units east and 28 units north), leaving the ship at east 170, north 38. The waypoint stays 10 units east and 4 units north of the ship.
R90 rotates the waypoint around the ship clockwise 90 degrees, moving it to 4 units east and 10 units south of the ship. The ship remains at east 170, north 38.
F11 moves the ship to the waypoint 11 times (a total of 44 units east and 110 units south), leaving the ship at east 214, south 72. The waypoint stays 4 units east and 10 units south of the ship.
After these operations, the ship's Manhattan distance from its starting position is 214 + 72 = 286.

Figure out where the navigation instructions actually lead. What is the Manhattan distance between that location and the ship's starting position?
"""
import re

from math import cos, sin, radians
from typing import Tuple, List

from utils import get_data

from dataclasses import dataclass

file_relative_path = "data_12.txt"
test1_path = "test_12.txt"

# I see only 90 degree rotations I will keep it rounded
@dataclass
class Direction:
    v1: int
    v2: int


@dataclass
class State:
    x: int
    y: int
    direction: Direction


N = Direction(0, 1)
S = Direction(0, -1)
E = Direction(1, 0)
W = Direction(-1, 0)


def rotate(theta: int, d: Direction, is_left: bool) -> Direction:
    if not is_left:
        theta = -theta
    return Direction(
        round(d.v1 * cos(radians(theta)) - d.v2 * sin(radians(theta))),
        round(d.v1 * sin(radians(theta)) + d.v2 * cos(radians(theta))),
    )


def move(d: Direction, factor: int, state: State) -> State:
    return State(state.x + factor * d.v1, state.y + factor * d.v2, state.direction)


def get_position(path):
    data = get_data(path)

    p = re.compile("^([E-W])([0-9]+)$")
    instructions: List[Tuple[str, int]] = [
        (p.match(line).group(1), int(p.match(line).group(2))) for line in data
    ]

    start: State = State(0, 0, E)
    current_state = start

    for cmd, factor in instructions:
        if cmd in "NSEW":
            direction = eval(cmd)
            current_state = move(d=direction, factor=factor, state=current_state)
        elif cmd == "F":
            current_state = move(
                current_state.direction, factor=factor, state=current_state
            )
        elif cmd in "RL":
            if cmd == "R":
                is_left = False
            else:
                is_left = True
            current_state.direction = rotate(
                theta=factor, d=current_state.direction, is_left=is_left
            )
        else:
            raise NotImplementedError

    print(f"Final state is: {current_state}")
    return current_state


def get_position_2(path):
    data = get_data(path)
    p = re.compile("^([E-W])([0-9]+)$")
    instructions: List[Tuple[str, int]] = [
        (p.match(line).group(1), int(p.match(line).group(2))) for line in data
    ]

    start: State = State(0, 0, E)
    current_state = start
    waypoint = Direction(10, 1)

    for cmd, factor in instructions:
        if cmd in "NSEW":
            direction = eval(cmd)
            s = move(
                d=direction,
                factor=factor,
                state=State(waypoint.v1, waypoint.v2, Direction(0, 0)),
            )
            waypoint = Direction(s.x, s.y)
        elif cmd == "F":
            current_state = move(waypoint, factor=factor, state=current_state)
        elif cmd in "RL":
            if cmd == "R":
                is_left = False
            else:
                is_left = True
            waypoint = rotate(theta=factor, d=waypoint, is_left=is_left)
        else:
            raise NotImplementedError

    print(f"Final state is: {current_state}")
    return current_state


if __name__ == "__main__":

    test = get_position(test1_path)
    assert test.x == 17
    assert test.y == -8

    r = get_position(file_relative_path)
    man_dist = abs(r.x) + abs(r.y)
    print(f"Part 1 Manhattan distance is: {man_dist}")

    test = get_position_2(test1_path)
    assert test.x == 214
    assert test.y == -72

    r = get_position_2(file_relative_path)
    man_dist = abs(r.x) + abs(r.y)
    print(f"Part 2 Manhattan distance is: {man_dist}")
