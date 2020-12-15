"""
--- Day 9: Encoding Error ---
With your neighbor happily enjoying their video game, you turn your attention to an open data port on the little screen in the seat in front of you.

Though the port is non-standard, you manage to connect it to your computer through the clever use of several paperclips. Upon connection, the port outputs a series of numbers (your puzzle input).

The data appears to be encrypted with the eXchange-Masking Addition System (XMAS) which, conveniently for you, is an old cypher with an important weakness.

XMAS starts by transmitting a preamble of 25 numbers. After that, each number you receive should be the sum of any two of the 25 immediately previous numbers. The two numbers will have different values, and there might be more than one such pair.

For example, suppose your preamble consists of the numbers 1 through 25 in a random order. To be valid, the next number must be the sum of two of those numbers:

26 would be a valid next number, as it could be 1 plus 25 (or many other pairs, like 2 and 24).
49 would be a valid next number, as it is the sum of 24 and 25.
100 would not be valid; no two of the previous 25 numbers sum to 100.
50 would also not be valid; although 25 appears in the previous 25 numbers, the two numbers in the pair must be different.
Suppose the 26th number is 45, and the first number (no longer an option, as it is more than 25 numbers ago) was 20. Now, for the next number to be valid, there needs to be some pair of numbers among 1-19, 21-25, or 45 that add up to it:

26 would still be a valid next number, as 1 and 25 are still within the previous 25 numbers.
65 would not be valid, as no two of the available numbers sum to it.
64 and 66 would both be valid, as they are the result of 19+45 and 21+45 respectively.
Here is a larger example which only considers the previous 5 numbers (and has a preamble of length 5):

35
20
15
25
47
40
62
55
65
95
102
117
150
182
127
219
299
277
309
576
In this example, after the 5-number preamble, almost every number is the sum of two of the previous 5 numbers; the only number that does not follow this rule is 127.

The first step of attacking the weakness in the XMAS data is to find the first number in the list (after the preamble) which is not the sum of two of the 25 numbers before it. What is the first number that does not have this property?

--- Part Two ---
The final step in breaking the XMAS encryption relies on the invalid number you just found: you must find a contiguous set of at least two numbers in your list which sum to the invalid number from step 1.

Again consider the above example:

35
20
15
25
47
40
62
55
65
95
102
117
150
182
127
219
299
277
309
576
In this list, adding up all of the numbers from 15 through 40 produces the invalid number from step 1, 127. (Of course, the contiguous set of numbers in your actual list might be much longer.)

To find the encryption weakness, add together the smallest and largest number in this contiguous range; in this example, these are 15 and 47, producing 62.

What is the encryption weakness in your XMAS-encrypted list of numbers?
"""
from typing import List

from utils import get_data

file_relative_path = "data_9.txt"
preamble = 25


def is_valid(target: int, consideration_range: List[int]) -> bool:
    print(f"considered: {len(consideration_range)} len for {consideration_range}")
    for i, number_1 in enumerate(consideration_range[:-1]):
        for j, number_2 in enumerate(consideration_range[i + 1 :]):
            print(
                f"target={target}, num1={number_1}, num2={number_2}, diff={number_2 + number_1}"
            )
            if target - number_2 == number_1:
                return True
    return False


def first_invalid_number(data: List[int]):
    for i, number in enumerate(data[preamble:]):
        consideration_range = data[max(0, (i - 1)) : (i + preamble)]
        if not is_valid(target=number, consideration_range=consideration_range):
            return number


def find_sum_max_min(target: int) -> int:
    for i, start_number in enumerate(data[:-1]):
        for j, end_number in enumerate(data[i + 1 :]):
            k = i + j
            result: int = sum(data[i:k])
            if result == target:
                print(
                    f"I've got it min={min(data[i:k])}, max={max(data[i:k])}, sum={result}, range={data[i:k]}"
                )
                return int(max(data[i:k]) + min(data[i:k]))
            elif result < target:
                continue
            else:
                break

    return -1


if __name__ == "__main__":
    data: List[int] = [int(x) for x in get_data(file_relative_path)]

    result_1 = first_invalid_number(data)
    print(f"First invalid number is: {result_1}")

    target = result_1
    print(f"Part 2 result is {find_sum_max_min(target)}")
