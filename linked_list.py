
"""
MSCS-532 Assignment 6
Part 2: Singly Linked List Implementation

A singly linked list consists of nodes. Each node stores
a value and a reference to the next node.

Implemented operations:
1. Insert at beginning
2. Insert at end
3. Insert at a specified position
4. Delete by value
5. Delete at a specified position
6. Search for a value
7. Traverse the list

Time complexity:
Insert at beginning: O(1)
Insert at end: O(1), using a tail reference
Insert at position: O(n)
Delete by value: O(n)
Delete at position: O(n)
Search: O(n)
Traversal: O(n)

Auxiliary space per operation: O(1), except traversal
when creating an output list, which requires O(n).
"""


class Node:
    """Represent one element in a singly linked list."""

    def __init__(self, value):
        # Store the actual data in the node.
        self.value = value

        # The next reference is initially empty.
        self.next = None


class SinglyLinkedList:
    """Manage nodes using head and tail references."""

    def __init__(self):
        # Head points to the first node.
        self.head = None

        # Tail points to the final node.
        self.tail = None

        # Maintain the number of nodes for efficient size checks.
        self._size = 0

    def is_empty(self):
        """Return True if the list contains no nodes."""
        return self._size == 0

    def size(self):
        """Return the number of nodes."""
        return self._size

    def insert_at_beginning(self, value):
        """Insert a new node before the current head."""

        new_node = Node(value)

        # Link the new node to the previous first node.
        new_node.next = self.head

        # Update head to reference the new first node.
        self.head = new_node

        # In an empty list, the new node is also the tail.
        if self.tail is None:
            self.tail = new_node

        self._size += 1

    def insert_at_end(self, value):
        """Append a new node to the end of the list."""

        new_node = Node(value)

        if self.is_empty():
            # The first inserted node becomes head and tail.
            self.head = new_node
            self.tail = new_node
        else:
            # Connect the previous tail to the new node.
            self.tail.next = new_node

            # Update the tail reference.
            self.tail = new_node

        self._size += 1

    def insert_at_position(self, index, value):
        """Insert a node at a specified zero-based position."""

        # Insertion is valid from index 0 through size.
        if (
            not isinstance(index, int)
            or isinstance(index, bool)
            or index < 0
            or index > self._size
        ):
            raise IndexError("Insertion index out of range.")

        if index == 0:
            self.insert_at_beginning(value)
            return

        if index == self._size:
            self.insert_at_end(value)
            return

        # Find the node immediately before the insertion point.
        previous = self.head

        for _ in range(index - 1):
            previous = previous.next

        new_node = Node(value)

        # Preserve the remaining nodes before updating links.
        new_node.next = previous.next
        previous.next = new_node

        self._size += 1

    def delete_by_value(self, value):
        """Delete the first matching value, if present."""

        # An empty list has no nodes to remove.
        if self.is_empty():
            return False

        # Handle deletion of the first node separately.
        if self.head.value == value:
            self.head = self.head.next
            self._size -= 1

            # If the last node was removed, clear the tail.
            if self.head is None:
                self.tail = None

            return True

        previous = self.head
        current = self.head.next

        # Traverse until the first matching node is found.
        while current is not None:
            if current.value == value:
                # Bypass the matching node.
                previous.next = current.next

                # Update tail if the final node was deleted.
                if current is self.tail:
                    self.tail = previous

                self._size -= 1
                return True

            previous = current
            current = current.next

        # Return False if no matching value exists.
        return False

    def delete_at_position(self, index):
        """Remove and return the value at a given index."""

        if (
            not isinstance(index, int)
            or isinstance(index, bool)
            or index < 0
            or index >= self._size
        ):
            raise IndexError("Deletion index out of range.")

        if index == 0:
            # Move head forward to remove the first node.
            removed_value = self.head.value
            self.head = self.head.next
            self._size -= 1

            if self.head is None:
                self.tail = None

            return removed_value

        # Locate the node before the target position.
        previous = self.head

        for _ in range(index - 1):
            previous = previous.next

        target = previous.next
        removed_value = target.value

        # Bypass the node being deleted.
        previous.next = target.next

        # Maintain the correct tail reference.
        if target is self.tail:
            self.tail = previous

        self._size -= 1

        return removed_value

    def search(self, value):
        """Return the first matching index, or -1 if absent."""

        current = self.head
        index = 0

        # Follow next references until a match is found.
        while current is not None:
            if current.value == value:
                return index

            current = current.next
            index += 1

        return -1

    def traverse(self):
        """Return all node values in their current order."""

        values = []
        current = self.head

        # Visit every node exactly once.
        while current is not None:
            values.append(current.value)
            current = current.next

        return values


if __name__ == "__main__":
    print("SINGLY LINKED LIST OPERATIONS")
    print("-" * 45)

    linked_list = SinglyLinkedList()

    # Add three nodes at the end.
    linked_list.insert_at_end(10)
    linked_list.insert_at_end(20)
    linked_list.insert_at_end(30)

    print("Original linked list:", linked_list.traverse())

    # Insert a new first node.
    linked_list.insert_at_beginning(5)
    print("After inserting 5 at beginning:", linked_list.traverse())

    # Insert a value between existing nodes.
    linked_list.insert_at_position(2, 15)
    print("After inserting 15 at index 2:", linked_list.traverse())

    # Find the index of a particular value.
    print("Index of value 20:", linked_list.search(20))

    # Delete the first occurrence of a value.
    print("Delete value 15:", linked_list.delete_by_value(15))
    print("After deleting 15:", linked_list.traverse())

    # Delete a node using its index.
    print("Deleted value at index 0:", linked_list.delete_at_position(0))
    print("After deleting first node:", linked_list.traverse())

    # Display the total number of remaining nodes.
    print("Linked list size:", linked_list.size())
