
"""
Assignment 6: Medians and Order Statistics
Part 1: Randomized Quickselect Algorithm

Purpose:
    Find the kth smallest element using a randomly chosen pivot.

Time complexity:
    Expected: O(n)
    Worst case: O(n^2)

The original input array remains unchanged.
"""

import random


def randomized_select(values, k):
    """
    Find the kth smallest element using Randomized Quickselect.

    Parameters:
        values: A list of comparable numbers.
        k: The required position, starting from 1.

    Returns:
        The kth smallest element.

    Raises:
        ValueError: If the input is empty or k is invalid.
    """

    # An empty array has no smallest element to select.
    if not values:
        raise ValueError("Cannot select from an empty array.")

    # Reject non-integer positions, including Boolean values.
    if not isinstance(k, int) or isinstance(k, bool):
        raise ValueError("k must be an integer.")

    # A valid position must fall within the array boundaries.
    if k < 1 or k > len(values):
        raise ValueError("k must be between 1 and the array length.")

    # If there is only one element, it must be the answer.
    if len(values) == 1:
        return values[0]

    # Random pivot selection reduces dependence on input order.
    pivot = random.choice(values)

    # Separate elements into three groups relative to the pivot.
    # Three-way partitioning handles repeated values efficiently.
    smaller = []
    equal = []
    larger = []

    for value in values:
        if value < pivot:
            smaller.append(value)
        elif value > pivot:
            larger.append(value)
        else:
            equal.append(value)

    # If the desired position is in the smaller group,
    # continue searching only within that group.
    if k <= len(smaller):
        return randomized_select(smaller, k)

    # If the position falls within the equal group,
    # the selected pivot is the kth smallest element.
    if k <= len(smaller) + len(equal):
        return pivot

    # Skip the smaller and equal groups before searching
    # the larger group. Adjust k to its new local position.
    adjusted_k = k - len(smaller) - len(equal)
    return randomized_select(larger, adjusted_k)


if __name__ == "__main__":
    # This example includes negative numbers and duplicates.
    numbers = [12, 3, 5, 7, 4, 19, 26, 3, -2]

    # Find the fifth smallest element.
    k = 5

    print("Original array:", numbers)
    print("Requested order statistic (k):", k)
    print("Kth smallest element:", randomized_select(numbers, k))
    print("Original array after selection:", numbers)
