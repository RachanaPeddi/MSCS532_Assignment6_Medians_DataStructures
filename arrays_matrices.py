
"""
MSCS-532 Assignment 6
Part 2: Arrays and Matrices

This program implements:
1. Array insertion, deletion, and access
2. Matrix insertion, deletion, and access

Python lists are used as the underlying storage.
The operations are implemented explicitly to demonstrate
how elementary data structures work.

Complexity:
Array access: O(1)
Array insertion/deletion: O(n) in the worst case
Matrix element access: O(1)
Matrix row insertion/deletion: O(r * c) in the worst case
when copying a matrix with r rows and c columns.
"""


class ArrayOperations:
    """Implement basic operations on a one-dimensional array."""

    def __init__(self, values=None):
        # Create an independent copy to avoid changing
        # the list provided by the caller.
        self.data = list(values) if values is not None else []

    def insert(self, index, value):
        """Insert a value at a specified valid position."""

        # Valid insertion positions range from 0 to length.
        if not isinstance(index, int) or isinstance(index, bool):
            raise IndexError("Array index must be an integer.")

        if index < 0 or index > len(self.data):
            raise IndexError("Array insertion index out of range.")

        # Extend the array by one position.
        self.data.append(None)

        # Shift elements to the right to create space.
        for i in range(len(self.data) - 1, index, -1):
            self.data[i] = self.data[i - 1]

        # Place the new value in the requested position.
        self.data[index] = value

    def delete(self, index):
        """Remove and return the element at a valid index."""

        self._validate_existing_index(index)

        removed_value = self.data[index]

        # Shift subsequent elements one position left.
        for i in range(index, len(self.data) - 1):
            self.data[i] = self.data[i + 1]

        # Remove the duplicated final position.
        self.data.pop()

        return removed_value

    def access(self, index):
        """Return the element at the specified index."""

        self._validate_existing_index(index)
        return self.data[index]

    def _validate_existing_index(self, index):
        """Reject invalid or out-of-range indexes."""

        if not isinstance(index, int) or isinstance(index, bool):
            raise IndexError("Array index must be an integer.")

        if index < 0 or index >= len(self.data):
            raise IndexError("Array index out of range.")

    def display(self):
        """Return a copy of the current array."""
        return self.data.copy()


class MatrixOperations:
    """Implement basic operations on a rectangular matrix."""

    def __init__(self, rows=None):
        # Copy every row so changes do not affect the
        # original matrix provided by the caller.
        self.data = [list(row) for row in rows] if rows is not None else []

        # Every row must contain the same number of columns.
        if self.data:
            column_count = len(self.data[0])

            if any(len(row) != column_count for row in self.data):
                raise ValueError("Matrix rows must have equal lengths.")

    def access(self, row, column):
        """Return the value at a specified matrix position."""

        self._validate_position(row, column)
        return self.data[row][column]

    def insert_row(self, index, values):
        """Insert a new row while preserving matrix dimensions."""

        if not isinstance(index, int) or isinstance(index, bool):
            raise IndexError("Row index must be an integer.")

        if index < 0 or index > len(self.data):
            raise IndexError("Row insertion index out of range.")

        new_row = list(values)

        # All rows in a rectangular matrix must have
        # the same number of columns.
        if self.data and len(new_row) != len(self.data[0]):
            raise ValueError("New row has an incorrect column count.")

        # Create space for the new row by shifting rows.
        self.data.append([])

        for i in range(len(self.data) - 1, index, -1):
            self.data[i] = self.data[i - 1]

        self.data[index] = new_row

    def delete_row(self, index):
        """Delete and return an existing matrix row."""

        if not isinstance(index, int) or isinstance(index, bool):
            raise IndexError("Row index must be an integer.")

        if index < 0 or index >= len(self.data):
            raise IndexError("Row index out of range.")

        removed_row = self.data[index]

        # Shift subsequent rows to the left in the outer list.
        for i in range(index, len(self.data) - 1):
            self.data[i] = self.data[i + 1]

        self.data.pop()
        return removed_row

    def _validate_position(self, row, column):
        """Ensure both matrix indexes refer to an existing value."""

        for index in (row, column):
            if not isinstance(index, int) or isinstance(index, bool):
                raise IndexError("Matrix indexes must be integers.")

        if row < 0 or row >= len(self.data):
            raise IndexError("Matrix row index out of range.")

        if column < 0 or column >= len(self.data[row]):
            raise IndexError("Matrix column index out of range.")

    def display(self):
        """Return a copy of the current matrix."""
        return [row.copy() for row in self.data]


if __name__ == "__main__":
    print("ARRAY OPERATIONS")
    print("-" * 40)

    # Create an array and demonstrate element insertion.
    array = ArrayOperations([10, 20, 30, 40])
    print("Original array:", array.display())

    array.insert(2, 25)
    print("After inserting 25 at index 2:", array.display())

    # Access an element using its zero-based index.
    print("Element at index 2:", array.access(2))

    # Delete the element at index 1.
    removed = array.delete(1)
    print("Deleted element:", removed)
    print("Array after deletion:", array.display())

    print("\nMATRIX OPERATIONS")
    print("-" * 40)

    # Create a rectangular matrix with two rows.
    matrix = MatrixOperations([
        [1, 2, 3],
        [4, 5, 6],
    ])

    print("Original matrix:", matrix.display())

    # Insert another row with the same column count.
    matrix.insert_row(1, [7, 8, 9])
    print("After row insertion:", matrix.display())

    # Access a matrix element using row and column indexes.
    print("Element at row 1, column 2:", matrix.access(1, 2))

    # Remove the first row and display the result.
    removed_row = matrix.delete_row(0)
    print("Deleted row:", removed_row)
    print("Matrix after deletion:", matrix.display())
