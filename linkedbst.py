"""
File: linkedbst.py
Author: Ken Lambert
"""
from abstractcollection import AbstractCollection
from bstnode import BSTNode
from linkedstack import LinkedStack
from linkedqueue import LinkedQueue
from math import log
# import math
import random
import time


class LinkedBST(AbstractCollection):
    """An link-based binary search tree implementation."""

    def __init__(self, sourceCollection=None):
        """Sets the initial state of self, which includes the
        contents of sourceCollection, if it's present."""
        self._root = None
        AbstractCollection.__init__(self, sourceCollection)

    # Accessor methods
    def __str__(self):
        """Returns a string representation with the tree rotated
        90 degrees counterclockwise."""

        def recurse(node, level):
            strin = ""
            if node != None:
                strin += recurse(node.right, level + 1)
                strin += "| " * level
                strin += str(node.data) + "\n"
                strin += recurse(node.left, level + 1)
            return strin

        return recurse(self._root, 0)

    def __iter__(self):
        """Supports a preorder traversal on a view of self."""
        if not self.isEmpty():
            stack = LinkedStack()
            stack.push(self._root)
            while not stack.isEmpty():
                node = stack.pop()
                yield node.data
                if node.right != None:
                    stack.push(node.right)
                if node.left != None:
                    stack.push(node.left)

    def preorder(self):
        """Supports a preorder traversal on a view of self."""
        return None

    def inorder(self):
        """Supports an inorder traversal on a view of self."""
        lyst = list()

        def recurse(node):
            if node != None:
                recurse(node.left)
                lyst.append(node.data)
                recurse(node.right)

        recurse(self._root)
        return iter(lyst)

    def postorder(self):
        """Supports a postorder traversal on a view of self."""
        return None

    def levelorder(self):
        """Supports a levelorder traversal on a view of self."""
        return None

    def __contains__(self, item):
        """Returns True if target is found or False otherwise."""
        return self.find(item) != None

    def find(self, item):
        """If item matches an item in self, returns the
        matched item, or None otherwise."""

        def recurse(node):
            if node is None:
                return None
            elif item == node.data:
                return node.data
            elif item < node.data:
                return recurse(node.left)
            else:
                return recurse(node.right)

        return recurse(self._root)

    # Mutator methods
    def clear(self):
        """Makes self become empty."""
        self._root = None
        self._size = 0

    def add(self, item):
        """Adds item to the tree."""

        # Helper function to search for item's position
        def recurse(node):
            # New item is less, go left until spot is found
            if item < node.data:
                if node.left == None:
                    node.left = BSTNode(item)
                else:
                    recurse(node.left)
            # New item is greater or equal,
            # go right until spot is found
            elif node.right == None:
                node.right = BSTNode(item)
            else:
                recurse(node.right)
                # End of recurse

        # Tree is empty, so new item goes at the root
        if self.isEmpty():
            self._root = BSTNode(item)
        # Otherwise, search for the item's spot
        else:
            recurse(self._root)
        self._size += 1

    def remove(self, item):
        """Precondition: item is in self.
        Raises: KeyError if item is not in self.
        postcondition: item is removed from self."""
        if not item in self:
            raise KeyError("Item not in tree.""")

        # Helper function to adjust placement of an item
        def liftMaxInLeftSubtreeToTop(top):
            # Replace top's datum with the maximum datum in the left subtree
            # Pre:  top has a left child
            # Post: the maximum node in top's left subtree
            #       has been removed
            # Post: top.data = maximum value in top's left subtree
            parent = top
            currentNode = top.left
            while not currentNode.right == None:
                parent = currentNode
                currentNode = currentNode.right
            top.data = currentNode.data
            if parent == top:
                top.left = currentNode.left
            else:
                parent.right = currentNode.left

        # Begin main part of the method
        if self.isEmpty(): return None

        # Attempt to locate the node containing the item
        itemRemoved = None
        preRoot = BSTNode(None)
        preRoot.left = self._root
        parent = preRoot
        direction = 'L'
        currentNode = self._root
        while not currentNode == None:
            if currentNode.data == item:
                itemRemoved = currentNode.data
                break
            parent = currentNode
            if currentNode.data > item:
                direction = 'L'
                currentNode = currentNode.left
            else:
                direction = 'R'
                currentNode = currentNode.right

        # Return None if the item is absent
        if itemRemoved == None: return None

        # The item is present, so remove its node

        # Case 1: The node has a left and a right child
        #         Replace the node's value with the maximum value in the
        #         left subtree
        #         Delete the maximium node in the left subtree
        if not currentNode.left == None \
                and not currentNode.right == None:
            liftMaxInLeftSubtreeToTop(currentNode)
        else:

            # Case 2: The node has no left child
            if currentNode.left == None:
                newChild = currentNode.right

                # Case 3: The node has no right child
            else:
                newChild = currentNode.left

                # Case 2 & 3: Tie the parent to the new child
            if direction == 'L':
                parent.left = newChild
            else:
                parent.right = newChild

        # All cases: Reset the root (if it hasn't changed no harm done)
        #            Decrement the collection's size counter
        #            Return the item
        self._size -= 1
        if self.isEmpty():
            self._root = None
        else:
            self._root = preRoot.left
        return itemRemoved

    def replace(self, item, newItem):
        """
        If item is in self, replaces it with newItem and
        returns the old item, or returns None otherwise."""
        probe = self._root
        while probe != None:
            if probe.data == item:
                oldData = probe.data
                probe.data = newItem
                return oldData
            elif probe.data > item:
                probe = probe.left
            else:
                probe = probe.right
        return None

    def height(self):
        '''
        Return the height of tree
        :return: int
        '''
        def height1(top):
            '''
            Helper function
            :param top:
            :return:
            '''
            if top is None:
                return -1
            left_height = height1(top.left)
            right_height = height1(top.right)
            # print(left_height, right_height)

            return 1 + max(left_height, right_height)
        return height1(self._root)


    def is_balanced(self):
        '''
        Return True if tree is balanced
        :return:
        '''
        # print(self._size)
        if self.height() < 2 * log((self._size + 1), 2) - 1:
            return True
        return False

    def range_find(self, low, high):
        '''
        Returns a list of the items in the tree, where low <= item <= high."""
        :param low:
        :param high:
        :return:
        '''
        def traverse(node, node_list):
            if node is None:
                return
            if low <= node.data <= high:
                node_list.append(node.data)
            if low < node.data:
                traverse(node.left, node_list)
            if node.data < high:
                traverse(node.right, node_list)
        node_list = []
        traverse(self._root, node_list)

        return node_list

    def rebalance(self):
        """
        Rebalances the tree.
        """
        def inorder_traversal(node):
            if node is not None:
                inorder_traversal(node.left)
                node_list.append(node.data)
                inorder_traversal(node.right)

        def create_new_tree(node_list):
            if not node_list:
                return None
            extra_node = len(node_list) // 2
            node = BSTNode(node_list[extra_node])
            node.left = create_new_tree(node_list[:extra_node])
            node.right = create_new_tree(node_list[extra_node + 1:])
            return node

        # Perform an inorder traversal to get the sorted list of nodes
        node_list = []
        inorder_traversal(self._root)

        # Clear the current tree
        self.clear()

        # Create a new tree from the sorted node list
        self._root = create_new_tree(node_list)
        return self

        # Print the rebalanced tree
        # print(self)


    def successor(self, item):
        """
        Returns the smallest item that is larger than
        item, or None if there is no such item.
        :param item:
        :type item:
        :return:
        :rtype:
        """
        node_list = []
        def traverse(node):
            if node is None:
                return
            if node.data > item:
                node_list.append(node.data)
            traverse(node.left)
            traverse(node.right)
        traverse(self._root)
        if node_list:
            return min(node_list)
        return

    def predecessor(self, item):
        """
        Returns the largest item that is smaller than
        item, or None if there is no such item.
        :param item:
        :type item:
        :return:
        :rtype:
        """
        node_list = []
        def traverse(node):
            if node is None:
                return
            if node.data < item:
                node_list.append(node.data)
            traverse(node.left)
            traverse(node.right)
        traverse(self._root)
        if node_list:
            return max(node_list)
        return

    def demo_bst(self, path):
        """
        Demonstration of efficiency binary search tree for the search tasks.
        :param path:
        :type path:
        :return:
        :rtype:
        """
        with open(path, 'r', encoding='utf-8') as file:
            file = file.readlines()
            file1 = []
            for el in file:
                file1.append(el[:-2])
            # print(file)
            random_words = random.choices(file1, k=10000)
            # print(random_words)
            # start_time1 = time.time()
            # counter1 = 0
            # for random_word in random_words:
            #     for normal_word in file1:
            #         if normal_word == random_word:
            #             counter1 += 1
            # end_time1 = time.time()
            # first_time = end_time1 - start_time1
            # print(first_time, counter1)

            new_tree = LinkedBST()
            # start_time2 = time.time()
            for word in random_words:
                # if word in file:
                new_tree.add(word)
            start_time2 = time.time()
            for rand_word in random_words:
                new_tree.find(rand_word)
            end_time2 = time.time()
            print(end_time2 - start_time2)

            new_tree2 = LinkedBST()
            print(len(file1))
            m = random.choices(random_words, k = len(file1))
            for n in m :
                new_tree2.add(n)
            start_time3 = time.time()
            for elem in random_words:
                new_tree2.find(elem)
            end_time3 = time.time()
            print(end_time3 - start_time3)

            new_tree3 = LinkedBST()
            for word in random_words:
                # if word in file:
                new_tree3.add(word)
            new_tree3 = new_tree3.rebalance()
            start_time4 = time.time()
            for elem in random_words:
                new_tree3.find(elem)
            end_time4 = time.time()
            print(end_time4 - start_time4)
            
            







