"""
--- Day 1: Report Repair ---
After saving Christmas five years in a row, you've decided to take a vacation at a nice resort on a tropical island. Surely, Christmas will go on without you.

The tropical island has its own currency and is entirely cash-only. The gold coins used there have a little picture of a starfish; the locals just call them stars. None of the currency exchanges seem to have heard of them, but somehow, you'll need to find fifty of these coins by the time you arrive so you can pay the deposit on your room.

To save your vacation, you need to get all fifty stars by December 25th.

Collect stars by solving puzzles. Two puzzles will be made available on each day in the Advent calendar; the second puzzle is unlocked when you complete the first. Each puzzle grants one star. Good luck!

Before you leave, the Elves in accounting just need you to fix your expense report (your puzzle input); apparently, something isn't quite adding up.

Specifically, they need you to find the two entries that sum to 2020 and then multiply those two numbers together.

For example, suppose your expense report contained the following:

1721
979
366
299
675
1456
In this list, the two entries that sum to 2020 are 1721 and 299. Multiplying them together produces 1721 * 299 = 514579, so the correct answer is 514579.

Of course, your expense report is much larger. Find the two entries that sum to 2020; what do you get if you multiply them together?
"""
from typing import Tuple, Optional, List
from functools import reduce


if __name__=='__main__':
    file_relative_path = 'data.txt'
    target_number = 2020

    def get_numbers() -> Optional[List[int]]:
        with open(file_relative_path, 'r') as f:
            numbers = [int(line.rstrip()) for line in f]
            return numbers

    def two_sum(numbers: List[int] = get_numbers(), target: int = target_number) -> Tuple[int, int]:
        for i, number in enumerate(numbers[:-1]):
            complementary = target - number
            if complementary in numbers[i+1:]:
                print(f"Solution Found: {number} and {complementary}")
                return (number, complementary)

        print(f"No solutions exists for target=<{target}>.")
        return None

    def three_sum(numbers: List[int] = get_numbers(), target: int = target_number) -> Optional[Tuple[int, int, int]]:
        for i, number in enumerate(numbers[:-2]):
            rest = target_number - number
            print(rest)
            complement_result = two_sum(numbers[i+1:], rest)

            if complement_result is not None:
                print(f"Solution Found: {number} and {complement_result[0]} and {complement_result[1]}")
                return (number, complement_result[0], complement_result[1])
        return None

    def multiply_tuple_items(t: Tuple) -> int:
        return reduce(lambda x, y: x*y, t)

    x = multiply_tuple_items(two_sum())
    print(x)

    y = multiply_tuple_items(three_sum())
    print(y)