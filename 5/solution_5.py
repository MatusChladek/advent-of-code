"""
--- Day 5: Binary Boarding ---
You board your plane only to discover a new problem: you dropped your boarding pass! You aren't sure which seat is yours, and all of the flight attendants are busy with the flood of people that suddenly made it through passport control.

You write a quick program to use your phone's camera to scan all of the nearby boarding passes (your puzzle input); perhaps you can find your seat through process of elimination.

Instead of zones or groups, this airline uses binary space partitioning to seat people. A seat might be specified like FBFBBFFRLR, where F means "front", B means "back", L means "left", and R means "right".

The first 7 characters will either be F or B; these specify exactly one of the 128 rows on the plane (numbered 0 through 127). Each letter tells you which half of a region the given seat is in. Start with the whole list of rows; the first letter indicates whether the seat is in the front (0 through 63) or the back (64 through 127). The next letter indicates which half of that region the seat is in, and so on until you're left with exactly one row.

For example, consider just the first seven characters of FBFBBFFRLR:

Start by considering the whole range, rows 0 through 127.
F means to take the lower half, keeping rows 0 through 63.
B means to take the upper half, keeping rows 32 through 63.
F means to take the lower half, keeping rows 32 through 47.
B means to take the upper half, keeping rows 40 through 47.
B keeps rows 44 through 47.
F keeps rows 44 through 45.
The final F keeps the lower of the two, row 44.
The last three characters will be either L or R; these specify exactly one of the 8 columns of seats on the plane (numbered 0 through 7). The same process as above proceeds again, this time with only three steps. L means to keep the lower half, while R means to keep the upper half.

For example, consider just the last 3 characters of FBFBBFFRLR:

Start by considering the whole range, columns 0 through 7.
R means to take the upper half, keeping columns 4 through 7.
L means to take the lower half, keeping columns 4 through 5.
The final R keeps the upper of the two, column 5.
So, decoding FBFBBFFRLR reveals that it is the seat at row 44, column 5.

Every seat also has a unique seat ID: multiply the row by 8, then add the column. In this example, the seat has ID 44 * 8 + 5 = 357.

Here are some other boarding passes:

BFFFBBFRRR: row 70, column 7, seat ID 567.
FFFBBBFRRR: row 14, column 7, seat ID 119.
BBFFBBFRLL: row 102, column 4, seat ID 820.
As a sanity check, look through your list of boarding passes. What is the highest seat ID on a boarding pass?
"""
from typing import Dict, Any

from utils import get_data
from math import ceil
from collections import defaultdict

file_relative_path = "data_5.txt"


def get_row(boarding_pass: str) -> int:
    lower, upper = 0, 127
    row_determinants = boarding_pass[:7]

    for determinant in row_determinants:
        if determinant == "F":
            upper -= ceil((upper - lower) / 2)
        elif determinant == "B":
            lower += ceil((upper - lower) / 2)

    return lower


def get_column(boarding_pass: str) -> int:
    lower, upper = 0, 7
    column_determinants = boarding_pass[7:]

    for determinant in column_determinants:
        if determinant == "L":
            upper -= ceil((upper - lower) / 2)
        elif determinant == "R":
            lower += ceil((upper - lower) / 2)

    return lower


if __name__ == "__main__":
    data = get_data(file_relative_path)
    max_id = 0

    d: Dict[Any, Any] = defaultdict(lambda: defaultdict(dict))

    for boarding_pass in data:
        row = get_row(boarding_pass)
        column = get_column(boarding_pass)
        seat_id = row * 8 + column

        d[row][column] = seat_id

        max_id = max(seat_id, max_id)

        print(
            f"Seat id for boarding pass <{boarding_pass}> is <{seat_id}> (row:<{row}>; column:<{column}>)."
        )

    print(f"Max id is <{max_id}>")

    for row in d.keys():
        if row > min(d.keys()) and row < max(d.keys()):
            for column in range(8):
                if column not in d[row].keys():
                    print(
                        f"Missing seat is in row:<{row}>; column:<{column}> -> {row * 8 + column}."
                    )
