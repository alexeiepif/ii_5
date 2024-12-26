#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from typing import Any, Generator, Optional

from tree import Problem, iterative_deepening_search

# Представьте себе систему управления доступом, где каждый пользователь представлен
# узлом в дереве. Каждый узел содержит уникальный идентификатор пользователя.
# Ваша задача — разработать метод поиска, который позволит проверить существование
# пользователя с заданным идентификатором в системе, используя структуру
# дерева и алгоритм итеративного углубления.


class BinaryTreeNode:
    def __init__(
        self,
        value: int,
        left: Optional["BinaryTreeNode"] = None,
        right: Optional["BinaryTreeNode"] = None,
    ) -> None:
        self.value = value
        self.left = left
        self.right = right

    def add_children(self, left: "BinaryTreeNode", right: "BinaryTreeNode") -> None:
        self.left = left
        self.right = right

    def __repr__(self) -> str:
        return f"<{self.value}>"


class UsersProblem(Problem):
    def __init__(self, initial: BinaryTreeNode, goal: int) -> None:
        super().__init__(initial)
        self.goal = goal

    def actions(self, state: BinaryTreeNode) -> Generator[BinaryTreeNode, None, None]:
        left = state.left
        right = state.right
        if left:
            yield left
        if right:
            yield right

    def result(self, state: BinaryTreeNode, action: BinaryTreeNode) -> BinaryTreeNode:
        return action

    def is_goal(self, state: BinaryTreeNode) -> bool:
        return state.value == self.goal


def solve(root: BinaryTreeNode, goal: int) -> Any:
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
