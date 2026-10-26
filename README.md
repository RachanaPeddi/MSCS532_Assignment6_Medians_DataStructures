# Assignment 6: Medians and Order Statistics & Elementary Data Structures

**Course:** MSCS-532 — Algorithms and Data Structures  
**University:** University of the Cumberlands  
**Programming Language:** Python

## Project Overview

This project explores selection algorithms and elementary data structures through Python implementations, theoretical complexity analysis, automated testing, and empirical performance evaluation.

The assignment consists of two parts:

- **Part 1:** Deterministic Median of Medians and Randomized Quickselect.
- **Part 2:** Arrays, matrices, array-backed stacks, circular-array queues, and singly linked lists.

## Part 1: Selection Algorithms

### Deterministic Median of Medians

Implemented in `deterministic_selection.py`.

This algorithm finds the kth smallest element by dividing the input into groups of at most five elements, sorting the groups, selecting a pivot recursively from their medians, and partitioning the input.

- Worst-case time complexity: **O(n)**
- Auxiliary space complexity: **O(n)** for this partition-based implementation

### Randomized Quickselect

Implemented in `randomized_selection.py`.

This algorithm selects a random pivot, partitions the input into smaller, equal, and larger elements, and recursively processes the partition containing the desired rank.

- Expected time complexity: **O(n)**
- Worst-case time complexity: **O(n²)**
- Auxiliary space complexity: **O(n)** for this partition-based implementation

Both algorithms support duplicate values, validate the requested rank, and preserve the original input list.

## Part 2: Elementary Data Structures

### Arrays and Matrices

`arrays_matrices.py`

Implements array insertion, deletion, and indexed access, along with matrix row insertion, row deletion, and cell access.

### Array-Backed Stack and Queue

`stacks_queues.py`

Implements:

- A stack with push, pop, and peek operations.
- A circular-array queue with enqueue, dequeue, front access, and automatic capacity doubling.

### Singly Linked List

`linked_list.py`

Implements insertion, deletion, searching, and traversal using nodes and head/tail references.

## Project Files

| File | Description |
|---|---|
| `deterministic_selection.py` | Median of Medians implementation |
| `randomized_selection.py` | Randomized Quickselect implementation |
| `test_selection.py` | Selection algorithm tests |
| `performance_analysis.py` | Performance benchmarking |
| `performance_results.csv` | Recorded benchmark results |
| `arrays_matrices.py` | Array and matrix operations |
| `stacks_queues.py` | Stack and circular queue implementations |
| `linked_list.py` | Singly linked list implementation |
| `test_data_structures.py` | Data structure tests |
| `MSCS532_Assignment6.pdf` | Assignment report |

## Requirements

- Python 3
- No third-party Python libraries required

## How to Run

Open a terminal in the project directory.

### Test the selection algorithms

```bash
python test_selection.py
```

Expected result: **208 passing checks**.

### Test the data structures

```bash
python test_data_structures.py
```

Expected result: **66 passing checks**.

### Run the performance benchmarks

```bash
python performance_analysis.py
```

This benchmarks both selection algorithms on four input sizes and four input distributions, prints the timing results, and generates `performance_results.csv`.

### Run individual implementations

```bash
python deterministic_selection.py
python randomized_selection.py
python arrays_matrices.py
python stacks_queues.py
python linked_list.py
```

## Testing and Validation

A total of **274 checks passed** during development:

- 208 selection algorithm checks.
- 66 data structure checks.

Testing covers valid and invalid inputs, duplicate values, empty structures, boundary conditions, queue wraparound and resizing, and linked-list head/tail updates.

## Empirical Performance Analysis

The benchmark compares deterministic and randomized selection using:

- Input sizes: 100, 500, 1,000, and 5,000.
- Distributions: random, sorted, reverse sorted, and duplicate heavy.
- Seven timing repetitions per configuration.
- Median execution time measured in milliseconds.

Randomized Quickselect was faster in all 16 measured configurations. However, these empirical measurements do not establish asymptotic complexity guarantees.

## Practical Applications

Selection algorithms can identify medians, percentiles, and ranked elements without fully sorting a dataset.

Arrays and matrices support indexed and tabular data. Stacks are useful for undo operations and expression evaluation. Queues support first-in-first-out task processing, while linked lists support sequences requiring efficient insertion at the beginning.

## Reference

Cormen, T. H., Leiserson, C. E., Rivest, R. L., & Stein, C. (2022). *Introduction to algorithms* (4th ed.). MIT Press.