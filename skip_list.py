import random

class SkipListNode:
    def __init__(self, key, value, level):
        """
        Initialize a Skip List node with a key, value, and level.
        :param key: The key of the node.
        :param value: The value of the node.
        :param level: The level of the node in the Skip List.
        """
        self.key = key
        self.value = value
        self.forward = [None] * (level + 1)

class SkipList:
    def __init__(self, max_level):
        """
        Initialize the Skip List with a given maximum level.
        :param max_level: The maximum level of the Skip List.
        """
        self.max_level = max_level
        self.header = SkipListNode(None, None, max_level)  # Create a header node.
        self.level = 0  # Current level of the Skip List.

    def random_level(self):
        """
        Generate a random level for a new node based on probability.
        :return: The randomly generated level.
        """
        level = 0
        while random.random() < 0.5 and level < self.max_level:
            level += 1
        return level

    def insert(self, key, value):
        """
        Insert a new node into the Skip List.
        :param key: The key of the new node.
        :param value: The value of the new node.
        """
        update = [None] * (self.max_level + 1)  # Track nodes to update at each level.
        current = self.header

        # Traverse the Skip List to find the position to insert.
        for i in range(self.level, -1, -1):
            while current.forward[i] and current.forward[i].key < key:
                current = current.forward[i]
            update[i] = current

        level = self.random_level()  # Determine the level of the new node.

        # Update the level of the Skip List if needed.
        if level > self.level:
            for i in range(self.level + 1, level + 1):
                update[i] = self.header
            self.level = level

        new_node = SkipListNode(key, value, level)  # Create the new node.

        # Insert the new node into the Skip List.
        for i in range(level + 1):
            new_node.forward[i] = update[i].forward[i]
            update[i].forward[i] = new_node

    def delete(self, key):
        """
        Delete a node from the Skip List by key.
        :param key: The key of the node to delete.
        """
        update = [None] * (self.max_level + 1)  # Track nodes to update at each level.
        current = self.header

        # Traverse the Skip List to find the node to delete.
        for i in range(self.level, -1, -1):
            while current.forward[i] and current.forward[i].key < key:
                current = current.forward[i]
            update[i] = current

        current = current.forward[0]

        # If the node to delete is found, remove it.
        if current and current.key == key:
            for i in range(self.level + 1):
                if update[i].forward[i] != current:
                    break
                update[i].forward[i] = current.forward[i]

            # Update the level of the Skip List if needed.
            while self.level > 0 and self.header.forward[self.level] is None:
                self.level -= 1

    def search(self, key):
        """
        Search for a node by key.
        :param key: The key to search for.
        :return: The value of the node if found, otherwise None.
        """
        current = self.header
        for i in range(self.level, -1, -1):
            while current.forward[i] and current.forward[i].key < key:
                current = current.forward[i]
        current = current.forward[0]
        return current.value if current and current.key == key else None
