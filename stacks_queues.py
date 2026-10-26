
"""
MSCS-532 Assignment 6
Part 2: Stack and Queue Implementations

Stack: Last In, First Out (LIFO)
Queue: First In, First Out (FIFO)

Both structures use Python lists as array storage.

Stack operations: O(1) amortized push, O(1) pop and peek.
Queue operations: O(1) amortized enqueue,
                  O(1) dequeue and front.
"""


class ArrayStack:
    """Implement a stack using an array-backed Python list."""

    def __init__(self):
        # Initially, the stack contains no elements.
        self._data = []

    def push(self, value):
        """Add a new element to the top of the stack."""

        # Appending to the end is efficient because no
        # existing elements need to be shifted.
        self._data.append(value)

    def pop(self):
        """Remove and return the top element."""

        # Removing from an empty stack is not allowed.
        if self.is_empty():
            raise IndexError("Cannot pop from an empty stack.")

        # The final array element is the stack's top.
        return self._data.pop()

    def peek(self):
        """Return the top element without removing it."""

        if self.is_empty():
            raise IndexError("Cannot peek at an empty stack.")

        return self._data[-1]

    def is_empty(self):
        """Check whether the stack has any elements."""
        return len(self._data) == 0

    def size(self):
        """Return the number of elements in the stack."""
        return len(self._data)

    def display(self):
        """Return a copy of the stack from bottom to top."""
        return self._data.copy()


class ArrayQueue:
    """Implement a FIFO queue using a circular array."""

    def __init__(self, initial_capacity=4):
        # Capacity must be a positive integer.
        if (
            not isinstance(initial_capacity, int)
            or isinstance(initial_capacity, bool)
            or initial_capacity < 1
        ):
            raise ValueError("Initial capacity must be positive.")

        # Preallocate storage for the circular queue.
        self._data = [None] * initial_capacity
        self._capacity = initial_capacity

        # Front points to the oldest queued element.
        self._front = 0

        # Count tracks how many positions are occupied.
        self._count = 0

    def enqueue(self, value):
        """Add a value to the rear of the queue."""

        # Expand the array when every position is occupied.
        if self._count == self._capacity:
            self._resize(self._capacity * 2)

        # Modular arithmetic wraps the rear index around
        # to the beginning of the underlying array.
        rear = (self._front + self._count) % self._capacity

        self._data[rear] = value
        self._count += 1

    def dequeue(self):
        """Remove and return the oldest queued element."""

        if self.is_empty():
            raise IndexError("Cannot dequeue from an empty queue.")

        # Retrieve the oldest element before advancing front.
        value = self._data[self._front]

        # Clear the unused slot to release its reference.
        self._data[self._front] = None

        # Move front forward, wrapping around if necessary.
        self._front = (self._front + 1) % self._capacity
        self._count -= 1

        return value

    def front(self):
        """Return the oldest element without removing it."""

        if self.is_empty():
            raise IndexError("Cannot access an empty queue.")

        return self._data[self._front]

    def is_empty(self):
        """Check whether the queue contains no elements."""
        return self._count == 0

    def size(self):
        """Return the number of queued elements."""
        return self._count

    def _resize(self, new_capacity):
        """Expand storage while preserving FIFO ordering."""

        # Copy elements in logical queue order, even when
        # their physical positions have wrapped around.
        new_data = [None] * new_capacity

        for i in range(self._count):
            old_index = (self._front + i) % self._capacity
            new_data[i] = self._data[old_index]

        # After copying, the first element starts at index 0.
        self._data = new_data
        self._capacity = new_capacity
        self._front = 0

    def display(self):
        """Return queue elements in FIFO order."""

        # Logical order can differ from physical array order
        # because the circular buffer may have wrapped around.
        return [
            self._data[(self._front + i) % self._capacity]
            for i in range(self._count)
        ]


if __name__ == "__main__":
    print("STACK OPERATIONS")
    print("-" * 40)

    stack = ArrayStack()

    # Push three values onto the stack.
    stack.push(10)
    stack.push(20)
    stack.push(30)

    print("Stack after pushes:", stack.display())
    print("Top element:", stack.peek())

    # LIFO means the most recently inserted value leaves first.
    print("Popped element:", stack.pop())
    print("Stack after pop:", stack.display())
    print("Stack size:", stack.size())

    print("\nQUEUE OPERATIONS")
    print("-" * 40)

    queue = ArrayQueue()

    # Enqueue three values in arrival order.
    queue.enqueue(10)
    queue.enqueue(20)
    queue.enqueue(30)

    print("Queue after enqueues:", queue.display())
    print("Front element:", queue.front())

    # FIFO means the earliest inserted value leaves first.
    print("Dequeued element:", queue.dequeue())
    print("Queue after dequeue:", queue.display())

    # Add more values to demonstrate circular positioning
    # and automatic capacity expansion.
    queue.enqueue(40)
    queue.enqueue(50)
    queue.enqueue(60)

    print("Queue after more enqueues:", queue.display())
    print("Queue size:", queue.size())
