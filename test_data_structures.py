
"""
MSCS-532 Assignment 6
Part 2: Comprehensive Data Structure Tests

This test suite checks:
1. Arrays: insertion, deletion, access, and boundaries
2. Matrices: row operations, access, and dimensions
3. Stacks: LIFO behavior and empty-stack errors
4. Queues: FIFO behavior, wraparound, and resizing
5. Linked lists: insertion, deletion, search, and traversal

Each test uses assertions to verify expected behavior.
"""


from arrays_matrices import ArrayOperations, MatrixOperations
from stacks_queues import ArrayStack, ArrayQueue
from linked_list import SinglyLinkedList


def expect_error(error_type, operation):
    """Verify that an invalid operation raises the expected error."""

    try:
        operation()

    except error_type:
        # The expected exception means validation works.
        return

    except Exception as error:
        raise AssertionError(
            f"Expected {error_type.__name__}, "
            f"but received {type(error).__name__}."
        ) from error

    raise AssertionError(
        f"Expected {error_type.__name__}, but no error occurred."
    )


def test_arrays():
    """Test array operations and boundary conditions."""

    checks = 0

    # Begin with an empty array and insert the first value.
    array = ArrayOperations()
    array.insert(0, 10)
    assert array.display() == [10]
    checks += 1

    # Test insertion at the beginning, middle, and end.
    array.insert(0, 5)
    array.insert(1, 7)
    array.insert(3, 15)
    assert array.display() == [5, 7, 10, 15]
    checks += 1

    # Confirm constant-time indexed access returns
    # the correct element.
    assert array.access(2) == 10
    checks += 1

    # Verify deletion shifts the remaining values correctly.
    assert array.delete(1) == 7
    assert array.display() == [5, 10, 15]
    checks += 1

    # Repeated values must remain separate array elements.
    array.insert(2, 10)
    assert array.display() == [5, 10, 10, 15]
    checks += 1

    # Reject indexes outside valid array boundaries.
    for operation in [
        lambda: array.access(-1),
        lambda: array.access(100),
        lambda: array.delete(100),
        lambda: array.insert(-1, 99),
        lambda: array.insert(100, 99),
        lambda: array.access(True),
    ]:
        expect_error(IndexError, operation)
        checks += 1

    # Ensure an empty array cannot be accessed or deleted.
    empty = ArrayOperations()
    expect_error(IndexError, lambda: empty.access(0))
    checks += 1

    expect_error(IndexError, lambda: empty.delete(0))
    checks += 1

    # Confirm the constructor copies the original list.
    original = [1, 2, 3]
    copied = ArrayOperations(original)
    copied.insert(1, 99)
    assert original == [1, 2, 3]
    checks += 1

    return checks


def test_matrices():
    """Test matrix dimensions and row operations."""

    checks = 0

    matrix = MatrixOperations([[1, 2], [3, 4]])

    # Access elements using zero-based row/column indexes.
    assert matrix.access(0, 1) == 2
    checks += 1

    # Insert a row while maintaining equal column counts.
    matrix.insert_row(1, [5, 6])
    assert matrix.display() == [[1, 2], [5, 6], [3, 4]]
    checks += 1

    # Remove a row and verify the remaining order.
    assert matrix.delete_row(0) == [1, 2]
    assert matrix.display() == [[5, 6], [3, 4]]
    checks += 1

    # Invalid matrix dimensions must be rejected.
    expect_error(
        ValueError,
        lambda: MatrixOperations([[1, 2], [3]])
    )
    checks += 1

    expect_error(
        ValueError,
        lambda: matrix.insert_row(1, [9])
    )
    checks += 1

    # Invalid row and column indexes must be rejected.
    for operation in [
        lambda: matrix.access(-1, 0),
        lambda: matrix.access(0, 10),
        lambda: matrix.access(True, 0),
        lambda: matrix.delete_row(10),
        lambda: matrix.insert_row(-1, [7, 8]),
    ]:
        expect_error(IndexError, operation)
        checks += 1

    # An empty matrix must support insertion of its first row.
    empty = MatrixOperations()
    empty.insert_row(0, [10, 20])
    assert empty.display() == [[10, 20]]
    checks += 1

    # Ensure the constructor does not modify source rows.
    original = [[1, 2], [3, 4]]
    copied = MatrixOperations(original)
    copied.insert_row(1, [5, 6])
    assert original == [[1, 2], [3, 4]]
    checks += 1

    return checks


def test_stacks():
    """Verify LIFO ordering and empty-stack behavior."""

    checks = 0

    stack = ArrayStack()

    # A newly created stack should contain no elements.
    assert stack.is_empty()
    assert stack.size() == 0
    checks += 1

    # Empty-stack operations must raise an error.
    expect_error(IndexError, stack.pop)
    checks += 1

    expect_error(IndexError, stack.peek)
    checks += 1

    # Push several values and verify their order.
    for value in [10, 20, 30]:
        stack.push(value)

    assert stack.display() == [10, 20, 30]
    checks += 1

    # Peek must not remove the top element.
    assert stack.peek() == 30
    assert stack.size() == 3
    checks += 1

    # LIFO requires the last inserted element to leave first.
    assert [stack.pop(), stack.pop(), stack.pop()] == [
        30, 20, 10
    ]
    checks += 1

    assert stack.is_empty()
    checks += 1

    # Test duplicate values and None as valid stack elements.
    stack.push(None)
    stack.push(None)
    assert stack.pop() is None
    assert stack.pop() is None
    checks += 1

    return checks


def test_queues():
    """Verify FIFO ordering, wraparound, and dynamic resizing."""

    checks = 0

    # Small capacity forces the queue to wrap and resize.
    queue = ArrayQueue(initial_capacity=3)

    assert queue.is_empty()
    checks += 1

    expect_error(IndexError, queue.dequeue)
    checks += 1

    expect_error(IndexError, queue.front)
    checks += 1

    # Fill the queue to its initial capacity.
    for value in [10, 20, 30]:
        queue.enqueue(value)

    assert queue.display() == [10, 20, 30]
    checks += 1

    # Removing the first element advances the front index.
    assert queue.dequeue() == 10
    checks += 1

    # Enqueue after dequeue to exercise circular wraparound.
    queue.enqueue(40)
    assert queue.display() == [20, 30, 40]
    checks += 1

    # Adding another element forces capacity expansion.
    queue.enqueue(50)
    assert queue.display() == [20, 30, 40, 50]
    checks += 1

    # Front must return the oldest value without removing it.
    assert queue.front() == 20
    assert queue.size() == 4
    checks += 1

    # Dequeue all values and verify FIFO order.
    assert [queue.dequeue() for _ in range(4)] == [
        20, 30, 40, 50
    ]
    checks += 1

    assert queue.is_empty()
    checks += 1

    # The queue must remain reusable after becoming empty.
    queue.enqueue(99)
    assert queue.dequeue() == 99
    checks += 1

    # Verify invalid initial capacities are rejected.
    for capacity in [0, -1, True, 1.5]:
        expect_error(
            ValueError,
            lambda c=capacity: ArrayQueue(c)
        )
        checks += 1

    # None is a valid stored value, not an empty-queue marker.
    queue.enqueue(None)
    assert queue.front() is None
    assert queue.dequeue() is None
    checks += 1

    return checks


def test_linked_lists():
    """Verify linked-list operations and pointer updates."""

    checks = 0

    linked = SinglyLinkedList()

    # Check behavior before any nodes are inserted.
    assert linked.is_empty()
    assert linked.size() == 0
    assert linked.traverse() == []
    checks += 1

    assert linked.search(10) == -1
    assert linked.delete_by_value(10) is False
    checks += 1

    expect_error(
        IndexError,
        lambda: linked.delete_at_position(0)
    )
    checks += 1

    # Insert nodes at the beginning and end.
    linked.insert_at_beginning(20)
    linked.insert_at_beginning(10)
    linked.insert_at_end(30)

    assert linked.traverse() == [10, 20, 30]
    checks += 1

    # Insert into the middle without losing existing nodes.
    linked.insert_at_position(1, 15)
    assert linked.traverse() == [10, 15, 20, 30]
    checks += 1

    # Verify searching returns the first matching position.
    assert linked.search(20) == 2
    checks += 1

    # Test duplicate values and deletion of the first match.
    linked.insert_at_end(20)
    assert linked.delete_by_value(20) is True
    assert linked.traverse() == [10, 15, 30, 20]
    checks += 1

    # Delete the head node and confirm traversal.
    assert linked.delete_at_position(0) == 10
    assert linked.traverse() == [15, 30, 20]
    checks += 1

    # Delete the tail node and verify tail maintenance.
    assert linked.delete_at_position(2) == 20
    assert linked.traverse() == [15, 30]
    checks += 1

    # Reject invalid insertion and deletion positions.
    for operation in [
        lambda: linked.insert_at_position(-1, 99),
        lambda: linked.insert_at_position(100, 99),
        lambda: linked.delete_at_position(-1),
        lambda: linked.delete_at_position(100),
        lambda: linked.insert_at_position(True, 99),
    ]:
        expect_error(IndexError, operation)
        checks += 1

    # Remove the remaining nodes.
    assert linked.delete_by_value(15)
    assert linked.delete_by_value(30)
    assert linked.is_empty()
    checks += 1

    # Reinsert after clearing the list to verify
    # that head and tail references remain valid.
    linked.insert_at_end(100)
    assert linked.traverse() == [100]
    assert linked.size() == 1
    checks += 1

    return checks


def main():
    """Execute all data structure tests and summarize results."""

    test_groups = [
        ("Arrays", test_arrays),
        ("Matrices", test_matrices),
        ("Stacks", test_stacks),
        ("Queues", test_queues),
        ("Singly Linked Lists", test_linked_lists),
    ]

    total_checks = 0

    print("\nASSIGNMENT 6 - DATA STRUCTURE TEST SUITE")
    print("-" * 50)

    for name, test_function in test_groups:
        # An assertion or unexpected exception stops execution,
        # ensuring that failures are not silently ignored.
        passed = test_function()
        total_checks += passed

        print(f"{name}: PASSED ({passed} checks)")

    print("-" * 50)
    print("All data structure tests passed successfully.")
    print(f"Total checks passed: {total_checks}")


if __name__ == "__main__":
    main()
