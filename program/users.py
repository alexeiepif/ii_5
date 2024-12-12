#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from tree import Problem, iterative_deepening_search


class BinaryTreeNode:
    def __init__(self, value, left=None, right=None):
        self.value = value
        self.left = left
        self.right = right

    def add_children(self, left, right):
        self.left = left
        self.right = right

    def __repr__(self):
        return f"<{self.value}>"


class UsersProblem(Problem):
    def __init__(self, initial, goal):
        super().__init__(initial)
        self.goal = goal

    def actions(self, state):
        left = state.left
        right = state.right
        if left:
            yield left
        if right:
            yield right

    def result(self, state, action):
        return action

    def is_goal(self, state):
        return state.value == self.goal


def solve(root, goal):
    problem = UsersProblem(root, goal)
    return iterative_deepening_search(problem)


if __name__ == "__main__":
    root = BinaryTreeNode(1)
    left_child = BinaryTreeNode(2)
    right_child = BinaryTreeNode(3)
    root.add_children(left_child, right_child)
    right_child.add_children(BinaryTreeNode(4), BinaryTreeNode(5))
    # Целевое значение
    goal = 4

    r = solve(root, goal)
    print("Первое дерево-пример: ", bool(r))

    root2 = BinaryTreeNode(1)
    left_child = BinaryTreeNode(2)
    right_child = BinaryTreeNode(3)
    root2.add_children(left_child, right_child)
    right_child.add_children(BinaryTreeNode(4), BinaryTreeNode(5))
    left_child.add_children(BinaryTreeNode(6), BinaryTreeNode(7))
    # Целевое значение
    goal = 7

    r = solve(root2, goal)
    print("Второе дерево: ", bool(r))
