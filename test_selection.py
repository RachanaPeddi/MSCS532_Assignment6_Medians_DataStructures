
"""
MSCS-532 Assignment 6
Part 1: Selection Algorithm Test Suite

Tests:
    1. Deterministic Median of Medians
    2. Randomized Quickselect

The tests verify correct results, boundary conditions,
duplicate handling, invalid inputs, and data integrity.
"""

import random

from deterministic_selection import deterministic_select
from randomized_selection import randomized_select


# Store both algorithms so the same tests can be
# applied consistently to each implementation.
ALGORITHMS = [
    ("Deterministic Median of Medians", deterministic_select),
    ("Randomized Quickselect", randomized_select),
]


def test_valid_inputs(name, algorithm):
    """Verify the kth smallest value for different arrays."""

    # Each test contains an input array and a valid k.
    test_cases = [
        ([5], 1),
        ([3, 1, 2], 1),
        ([3, 1, 2], 2),
        ([3, 1, 2], 3),
        ([1, 2, 3, 4, 5], 3),
        ([5, 4, 3, 2, 1], 3),
        ([7, 7, 7, 7], 2),
        ([4, 2, 4, 1, 2, 4], 4),
        ([-5, -1, -10, 0, 3], 2),
        ([0, 0, -1, 1, 0], 3),
        ([12, 3, 5, 7, 4, 19, 26, 3, -2], 5),
        ([2.5, -1.5, 3.0, 2.5], 2),
    ]

    passed = 0

    for values, k in test_cases:
        # Sorting is used only as a correctness reference.
        # The selection algorithms themselves do not sort
        # the complete array to find the answer.
        expected = sorted(values)[k - 1]

        # Preserve the original input for a mutation check.
        original = values.copy()

        # Run the algorithm and compare with the reference.
        actual = algorithm(values, k)

        assert actual == expected, (
            f"{name}: Incorrect result for {values}, k={k}. "
            f"Expected {expected}, received {actual}."
        )

        # Verify the implementation did not change the input.
        assert values == original, (
            f"{name}: Original input was modified."
        )

        passed += 1

    print(f"  Valid input tests passed: {passed}")
    return passed


def test_invalid_inputs(name, algorithm):
    """Verify that invalid inputs raise ValueError."""

    invalid_cases = [
        ([], 1),             # Empty array
        ([1, 2, 3], 0),      # k below valid range
        ([1, 2, 3], -1),     # Negative k
        ([1, 2, 3], 4),      # k above valid range
        ([1, 2, 3], 1.5),    # Non-integer k
        ([1, 2, 3], "2"),    # String instead of integer
        ([1, 2, 3], True),   # Boolean should not be a position
        ([1, 2, 3], None),   # Missing position
    ]

    passed = 0

    for values, k in invalid_cases:
        try:
            algorithm(values, k)

        except ValueError:
            # A ValueError is the expected result.
            passed += 1

        else:
            raise AssertionError(
                f"{name}: Expected ValueError for "
                f"values={values}, k={k!r}."
            )

    print(f"  Invalid input tests passed: {passed}")
    return passed


def test_randomized_datasets(name, algorithm):
    """Test many arrays against Python's sorted reference."""

    # A fixed seed makes the generated datasets repeatable.
    generator = random.Random(532)

    passed = 0

    # Include different sizes and input distributions.
    for size in [1, 2, 5, 10, 25, 50, 100, 250]:
        for distribution in [
            "random",
            "sorted",
            "reverse_sorted",
            "duplicates",
        ]:
            # Generate data with negative and positive values.
            values = [
                generator.randint(-1000, 1000)
                for _ in range(size)
            ]

            if distribution == "sorted":
                values.sort()

            elif distribution == "reverse_sorted":
                values.sort(reverse=True)

            elif distribution == "duplicates":
                # A narrow range creates repeated values.
                values = [
                    generator.randint(-3, 3)
                    for _ in range(size)
                ]

            # Test the smallest, middle, and largest positions.
            positions = sorted(set([
                1,
                (size + 1) // 2,
                size,
            ]))

            expected_order = sorted(values)
            original = values.copy()

            for k in positions:
                expected = expected_order[k - 1]
                actual = algorithm(values, k)

                assert actual == expected, (
                    f"{name}: Failed {distribution} dataset "
                    f"of size {size} at k={k}."
                )

                assert values == original, (
                    f"{name}: Input modified during testing."
                )

                passed += 1

    print(f"  Dataset tests passed: {passed}")
    return passed


def main():
    """Execute every test for both selection algorithms."""

    total_passed = 0

    for name, algorithm in ALGORITHMS:
        print(f"\nTesting: {name}")

        total_passed += test_valid_inputs(name, algorithm)
        total_passed += test_invalid_inputs(name, algorithm)
        total_passed += test_randomized_datasets(
            name, algorithm
        )

        print("  Status: PASSED")

    print("\nAll selection tests completed successfully.")
    print(f"Total test cases passed: {total_passed}")


if __name__ == "__main__":
    main()
