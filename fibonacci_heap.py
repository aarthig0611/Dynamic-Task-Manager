class FibonacciHeapNode:
    def __init__(self, key, value):
        """
        Initialize a node in a Fibonacci Heap.
        :param key: The key of the node.
        :param value: The value of the node.
        """
        self.key = key
        self.value = value
        self.degree = 0  # Number of children.
        self.marked = False  # Whether the node is marked.
        self.parent = None
        self.child = None
        self.left = self
        self.right = self

class FibonacciHeap:
    def __init__(self):
        """
        Initialize an empty Fibonacci Heap.
        """
        self.min_node = None  # Node with the minimum key.
        self.total_nodes = 0  # Total number of nodes.

    def insert(self, key, value):
        """
        Insert a new node into the Fibonacci Heap.
        :param key: The key of the new node.
        :param value: The value of the new node.
        :return: The newly created node.
        """
        node = FibonacciHeapNode(key, value)
        if not self.min_node:
            self.min_node = node
        else:
            self._add_node(node, self.min_node)
            if node.key < self.min_node.key:
                self.min_node = node
        self.total_nodes += 1
        return node

    def _add_node(self, node, root):
        """
        Add a node to the root list of the Fibonacci Heap.
        :param node: The node to add.
        :param root: The root node to add the node to.
        """
        node.left = root
        node.right = root.right
        root.right = node
        node.right.left = node

    def extract_min(self):
        """
        Extract and return the node with the minimum key.
        :return: The node with the minimum key.
        """
        min_node = self.min_node
        if min_node:
            # Add children of min_node to the root list.
            if min_node.child:
                children = [x for x in self._iterate_list(min_node.child)]
                for child in children:
                    self._add_node(child, min_node)
                    child.parent = None
            self._remove_node(min_node)
            if min_node == min_node.right:
                self.min_node = None
            else:
                self.min_node = min_node.right
                self._consolidate()
            self.total_nodes -= 1
        return min_node

    def _remove_node(self, node):
        """
        Remove a node from the list.
        :param node: The node to remove.
        """
        node.left.right = node.right
        node.right.left = node.left

    def _consolidate(self):
        """
        Consolidate the trees in the root list to ensure no two trees have the same degree.
        """
        degree_table = [None] * (self.total_nodes + 1)
        nodes = [x for x in self._iterate_list(self.min_node)]

        for node in nodes:
            degree = node.degree
            while degree_table[degree]:
                other = degree_table[degree]
                if node.key > other.key:
                    node, other = other, node
                self._link(other, node)
                degree_table[degree] = None
                degree += 1
            degree_table[degree] = node

        self.min_node = None
        for node in degree_table:
            if node:
                if not self.min_node:
                    self.min_node = node
                else:
                    self._add_node(node, self.min_node)
                    if node.key < self.min_node.key:
                        self.min_node = node

    def _link(self, node, root):
        """
        Link a node to the child list of another node.
        :param node: The node to link.
        :param root: The root node to link the node to.
        """
        self._remove_node(node)
        node.parent = root
        if not root.child:
            root.child = node
        else:
            self._add_node(node, root.child)
        root.degree += 1
        node.marked = False

    def _iterate_list(self, head):
        """
        Iterate through a circular list starting from the head node.
        :param head: The head node of the list.
        :yield: Each node in the list.
        """
        node = head
        while True:
            yield node
            node = node.right
            if node == head:
                break
