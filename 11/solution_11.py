"""
--- Day 11: Seating System ---
Your plane lands with plenty of time to spare. The final leg of your journey is a ferry that goes directly to the tropical island where you can finally start your vacation. As you reach the waiting area to board the ferry, you realize you're so early, nobody else has even arrived yet!

By modeling the process people use to choose (or abandon) their seat in the waiting area, you're pretty sure you can predict the best place to sit. You make a quick map of the seat layout (your puzzle input).

The seat layout fits neatly on a grid. Each position is either floor (.), an empty seat (L), or an occupied seat (#). For example, the initial seat layout might look like this:

L.LL.LL.LL
LLLLLLL.LL
L.L.L..L..
LLLL.LL.LL
L.LL.LL.LL
L.LLLLL.LL
..L.L.....
LLLLLLLLLL
L.LLLLLL.L
L.LLLLL.LL
Now, you just need to model the people who will be arriving shortly. Fortunately, people are entirely predictable and always follow a simple set of rules. All decisions are based on the number of occupied seats adjacent to a given seat (one of the eight positions immediately up, down, left, right, or diagonal from the seat). The following rules are applied to every seat simultaneously:

If a seat is empty (L) and there are no occupied seats adjacent to it, the seat becomes occupied.
If a seat is occupied (#) and four or more seats adjacent to it are also occupied, the seat becomes empty.
Otherwise, the seat's state does not change.
Floor (.) never changes; seats don't move, and nobody sits on the floor.

After one round of these rules, every seat in the example layout becomes occupied:

#.##.##.##
#######.##
#.#.#..#..
####.##.##
#.##.##.##
#.#####.##
..#.#.....
##########
#.######.#
#.#####.##
After a second round, the seats with four or more occupied adjacent seats become empty again:

#.LL.L#.##
#LLLLLL.L#
L.L.L..L..
#LLL.LL.L#
#.LL.LL.LL
#.LLLL#.##
..L.L.....
#LLLLLLLL#
#.LLLLLL.L
#.#LLLL.##
This process continues for three more rounds:

#.##.L#.##
#L###LL.L#
L.#.#..#..
#L##.##.L#
#.##.LL.LL
#.###L#.##
..#.#.....
#L######L#
#.LL###L.L
#.#L###.##
#.#L.L#.##
#LLL#LL.L#
L.L.L..#..
#LLL.##.L#
#.LL.LL.LL
#.LL#L#.##
..L.L.....
#L#LLLL#L#
#.LLLLLL.L
#.#L#L#.##
#.#L.L#.##
#LLL#LL.L#
L.#.L..#..
#L##.##.L#
#.#L.LL.LL
#.#L#L#.##
..L.L.....
#L#L##L#L#
#.LLLLLL.L
#.#L#L#.##
At this point, something interesting happens: the chaos stabilizes and further applications of these rules cause no seats to change state! Once people stop moving around, you count 37 occupied seats.

Simulate your seating area by applying the seating rules repeatedly until no seats change state. How many seats end up occupied?
"""
from typing import List, Tuple

from utils import get_data

file_relative_path = "data_11.txt"
test1_path = "test_11.txt"

floor = "."
empty_seat = "L"
occupied_seat = "#"

adjacent_seats: List[Tuple[int, int]] = [
    (-1, 0),
    (1, 0),
    (0, 1),
    (0, -1),
    (-1, -1),
    (-1, 1),
    (1, 1),
    (1, -1),
]


def set_to_value(row: str, idx: int, val: str) -> str:
    new_row = list(row)
    new_row[idx] = val

    return "".join(new_row)


def get_value(row: str, idx: int) -> str:
    new_row = list(row)
    return new_row[idx]


def occupied_count(state: List[str], row: int, col: int) -> int:
    counter = 0
    valid_row = range(len(state))
    valid_col = range(len(state[0]))

    for adjacent_seat in adjacent_seats:
        next_row = row + adjacent_seat[0]
        next_col = col + adjacent_seat[1]

        if next_row in valid_row and next_col in valid_col:
            adjacent_seat_value = list(state[row + adjacent_seat[0]])[
                col + adjacent_seat[1]
            ]
            if adjacent_seat_value == occupied_seat:
                counter += 1
        else:
            continue

    return counter


def get_new_state(current_state: List[str]) -> List[str]:
    next_state = current_state.copy()
    for row_id, row in enumerate(current_state):
        for col_id, seat in enumerate(row):
            if seat == floor:
                continue
            elif seat == empty_seat:
                if occupied_count(current_state, row_id, col_id) == 0:
                    next_state[row_id] = set_to_value(
                        next_state[row_id], col_id, occupied_seat
                    )
            elif seat == occupied_seat:
                if occupied_count(current_state, row_id, col_id) >= 4:
                    next_state[row_id] = set_to_value(
                        next_state[row_id], col_id, empty_seat
                    )
    return next_state


def is_occupied_in_direction(
    direction: Tuple[int, int], state: List[str], row: int, col: int
) -> bool:
    valid_row = range(len(state))
    valid_col = range(len(state[0]))

    next_row = row + direction[0]
    next_col = col + direction[1]

    while next_row in valid_row and next_col in valid_col:
        adjacent_seat_value = list(state[next_row])[next_col]
        if adjacent_seat_value == occupied_seat:
            return True
        if adjacent_seat_value == empty_seat:
            return False
        elif adjacent_seat_value == floor:
            next_row += direction[0]
            next_col += direction[1]

    return False


def occupied_count_considering_floor(state: List[str], row: int, col: int) -> int:
    counter = 0

    for adjacent_seat in adjacent_seats:
        counter += is_occupied_in_direction(adjacent_seat, state, row, col)

    return counter


def get_new_state_considering_floor(current_state: List[str]) -> List[str]:
    next_state = current_state.copy()

    for row_id, row in enumerate(current_state):
        for col_id, seat in enumerate(row):
            if seat == floor:
                continue
            elif seat == empty_seat:
                if occupied_count_considering_floor(current_state, row_id, col_id) == 0:
                    next_state[row_id] = set_to_value(
                        next_state[row_id], col_id, occupied_seat
                    )
            elif seat == occupied_seat:
                if occupied_count_considering_floor(current_state, row_id, col_id) >= 5:
                    next_state[row_id] = set_to_value(
                        next_state[row_id], col_id, empty_seat
                    )
    return next_state


def driver(path: str):
    rows: List[str] = get_data(path)
    current_state: List[str] = rows

    while True:
        next_state = get_new_state(current_state)
        if current_state == next_state:
            break
        current_state = next_state.copy()

    result = "".join(current_state).count(occupied_seat)
    print(f"There is {result} occupied seats after convergence.")

    return result


def driver_2(path: str):
    rows: List[str] = get_data(path)
    current_state: List[str] = rows

    while True:
        next_state = get_new_state_considering_floor(current_state)
        if current_state == next_state:
            break
        current_state = next_state.copy()

    result = "".join(current_state).count(occupied_seat)
    print(f"There is {result} occupied seats after convergence for part 2.")

    return result


if __name__ == "__main__":
    assert driver(test1_path) == 37
    driver(file_relative_path)

    assert driver_2(test1_path) == 26
    driver_2(file_relative_path)
