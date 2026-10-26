
"""
Assignment 6: Medians and Order Statistics
Part 1: Deterministic Selection (Median of Medians)

This program finds the kth smallest element in an array
using a deterministic selection algorithm.

Time complexity: O(n) in the worst case.
The original input array is not modified.
"""


def insertion_sort(values):
    """
    Sort a small group of values using insertion sort.

    Groups contain at most five elements, so sorting
    each group takes constant time.
    """
    result = values.copy()

    # Start with the second element and insert it into
    # its correct position among the preceding elements.
    for i in range(1, len(result)):
        current = result[i]
        j = i - 1

        # Shift larger elements one position to the right.
        while j >= 0 and result[j] > current:
            result[j + 1] = result[j]
            j -= 1

        result[j + 1] = current

    return result


def median_of_medians(values):
    """
    Choose a deterministic pivot using groups of five.
    """

    # A group of five or fewer elements can be sorted
    # directly to identify its median.
    if len(values) <= 5:
        sorted_values = insertion_sort(values)
        return sorted_values[len(sorted_values) // 2]

    medians = []

    # Divide the input into groups of at most five.
    for i in range(0, len(values), 5):
        group = values[i:i + 5]

        # Find the median of each small group.
        sorted_group = insertion_sort(group)
        group_median = sorted_group[len(sorted_group) // 2]
        medians.append(group_median)

    # Recursively select the median of the group medians.
    # This pivot guarantees balanced-enough partitions
    # for worst-case linear-time selection.
    return deterministic_select(medians, (len(medians) + 1) // 2)


def deterministic_select(values, k):
    """
    Return the kth smallest element (1-based indexing).

    For example:
        deterministic_select([8, 3, 5], 1) returns 3.
        deterministic_select([8, 3, 5], 2) returns 5.

    Raises ValueError for an empty array or invalid k.
    """

    # Reject empty inputs and positions outside the array.
    if not values:
        raise ValueError("Cannot select from an empty array.")

    if not isinstance(k, int) or isinstance(k, bool):
        raise ValueError("k must be an integer.")

    if k < 1 or k > len(values):
        raise ValueError("k must be between 1 and the array length.")

    # One element requires no partitioning.
    if len(values) == 1:
        return values[0]

    # Choose a pivot without using randomness.
    pivot = median_of_medians(values)

    # Three-way partitioning correctly handles duplicates.
    # Each value is placed below, equal to, or above pivot.
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

    # If k falls in the smaller partition, search there.
    if k <= len(smaller):
        return deterministic_select(smaller, k)

    # If k falls among the pivot duplicates, the answer
    # is the pivot itself.
    if k <= len(smaller) + len(equal):
        return pivot

    # Otherwise, search the larger partition and adjust
    # k to account for the elements already excluded.
    new_k = k - len(smaller) - len(equal)
    return deterministic_select(larger, new_k)


if __name__ == "__main__":
    # Sample dataset includes duplicates and negative values.
    numbers = [12, 3, 5, 7, 4, 19, 26, 3, -2]

    # The fifth smallest value should be 5.
    k = 5

    print("Original array:", numbers)
    print("Requested order statistic (k):", k)
    print("Kth smallest element:", deterministic_select(numbers, k))
    print("Original array after selection:", numbers)
