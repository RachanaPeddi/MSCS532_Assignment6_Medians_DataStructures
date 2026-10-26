
"""
MSCS-532 Assignment 6
Part 1: Empirical Performance Analysis

This program benchmarks two selection algorithms:
1. Deterministic Median of Medians
2. Randomized Quickselect

It measures execution time across different input sizes
and distributions, verifies correctness, and exports
the results to a CSV file for further analysis.
"""

import csv
import random
import statistics
import time

from deterministic_selection import deterministic_select
from randomized_selection import randomized_select


# Test different input sizes to examine how running time
# changes as the number of elements increases.
INPUT_SIZES = [100, 500, 1000, 5000]

# Different distributions help reveal how the algorithms
# respond to input order and repeated values.
DISTRIBUTIONS = [
    "Random",
    "Sorted",
    "Reverse Sorted",
    "Duplicate Heavy",
]

# Repeating each test reduces the influence of occasional
# system delays on the reported execution time.
TRIALS = 7

# A fixed seed makes dataset generation reproducible.
DATA_GENERATOR = random.Random(532)


def generate_dataset(size, distribution):
    """Create a dataset with the requested distribution."""

    if distribution == "Duplicate Heavy":
        # A small value range creates many repeated elements.
        return [
            DATA_GENERATOR.randint(-10, 10)
            for _ in range(size)
        ]

    # Generate the same underlying type of values for
    # random, sorted, and reverse-sorted distributions.
    values = [
        DATA_GENERATOR.randint(-100000, 100000)
        for _ in range(size)
    ]

    if distribution == "Sorted":
        values.sort()

    elif distribution == "Reverse Sorted":
        values.sort(reverse=True)

    return values


def measure_execution_time(algorithm, values, k):
    """Measure one execution and verify its result."""

    # perf_counter provides a high-resolution timer.
    start_time = time.perf_counter()

    result = algorithm(values, k)

    end_time = time.perf_counter()

    # Calculate elapsed execution time in milliseconds.
    elapsed_ms = (end_time - start_time) * 1000

    return result, elapsed_ms


def benchmark_algorithm(algorithm, values, k, expected):
    """Run multiple trials and return the median time."""

    measurements = []

    for _ in range(TRIALS):
        # Copy the input so every trial receives equivalent
        # data and no previous run affects another run.
        trial_values = values.copy()

        result, elapsed_ms = measure_execution_time(
            algorithm, trial_values, k
        )

        # Verify correctness before accepting a measurement.
        if result != expected:
            raise AssertionError(
                "Algorithm returned an incorrect result."
            )

        # Ensure the algorithm did not modify its input.
        if trial_values != values:
            raise AssertionError(
                "Algorithm unexpectedly modified the input."
            )

        measurements.append(elapsed_ms)

    # The median is less sensitive to timing outliers
    # than the arithmetic mean.
    return statistics.median(measurements)


def run_benchmarks():
    """Compare both algorithms and save benchmark results."""

    results = []

    algorithms = [
        ("Deterministic Median of Medians", deterministic_select),
        ("Randomized Quickselect", randomized_select),
    ]

    print("\nASSIGNMENT 6 - SELECTION ALGORITHM BENCHMARK")
    print("-" * 85)

    for size in INPUT_SIZES:
        for distribution in DISTRIBUTIONS:
            # Both algorithms receive the same dataset.
            values = generate_dataset(size, distribution)

            # Select the median-ranked element.
            # k uses one-based indexing.
            k = (size + 1) // 2

            # Python's sorted function is used only to
            # determine the expected answer for validation.
            expected = sorted(values)[k - 1]

            timing_results = {}

            for name, algorithm in algorithms:
                median_time = benchmark_algorithm(
                    algorithm, values, k, expected
                )

                timing_results[name] = median_time

                # Store measurements for the final report.
                results.append({
                    "Input Size": size,
                    "Distribution": distribution,
                    "Algorithm": name,
                    "K": k,
                    "Median Time (ms)": round(median_time, 6),
                    "Trials": TRIALS,
                })

            deterministic_time = timing_results[
                "Deterministic Median of Medians"
            ]

            randomized_time = timing_results[
                "Randomized Quickselect"
            ]

            print(
                f"Size: {size:5d} | "
                f"Distribution: {distribution:15s} | "
                f"Deterministic: {deterministic_time:10.4f} ms | "
                f"Randomized: {randomized_time:10.4f} ms"
            )

    # Write all benchmark measurements to a CSV file.
    # This allows results to be reviewed independently.
    filename = "performance_results.csv"

    with open(filename, "w", newline="", encoding="utf-8") as file:
        fieldnames = [
            "Input Size",
            "Distribution",
            "Algorithm",
            "K",
            "Median Time (ms)",
            "Trials",
        ]

        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(results)

    print("-" * 85)
    print(f"Benchmark completed successfully.")
    print(f"Results saved to: {filename}")
    print(f"Total benchmark configurations: {len(results)}")


if __name__ == "__main__":
    run_benchmarks()
