#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from tree import Problem, iterative_deepening_search, path_states

# Рассмотрим задачу поиска информации в иерархических структурах данных,
# например, в файловой системе, где каждый каталог может содержать подкаталоги
# и файлы. Алгоритм итеративного углубления идеально подходит для таких задач,
# поскольку он позволяет исследовать структуру данных постепенно, углубляясь на
# один уровень за раз и возвращаясь, если целевой узел не найден. Для этого
# необходимо:
# Построить дерево, где каждый узел представляет каталог в файловой
# системе, а цель поиска — определенный файл.
# Найти путь от корневого каталога до каталога (или файла), содержащего
# искомый файл, используя алгоритм итеративного углубления.


class TreeNode:
    def __init__(self, value):
        self.value = value
        self.children = []

    def add_child(self, child):
        self.children.append(child)

    def add_children(self, *args):
        for child in args:
            self.add_child(child)

    def __repr__(self):
        return f"<{self.value}>"


class FileSearchProblem(Problem):
    def __init__(self, initial, goal):
        super().__init__(initial)
        self.goal = goal

    def actions(self, state):
        yield from state.children

    def result(self, state, action):
        return action

    def is_goal(self, state):
        return state.value == self.goal


def solve(root, goal):
    problem = FileSearchProblem(root, goal)
    r = iterative_deepening_search(problem)
    if not r:
        return "Цель не найдена"
    states = path_states(r)
    str_path = " -> ".join(map(lambda x: x.value, states))
    return str_path


if __name__ == "__main__":
    root = TreeNode("dir1")
    root.add_child(TreeNode("dir2"))
    root.add_child(TreeNode("dir3"))
    root.children[0].add_child(TreeNode("file4"))
    root.children[1].add_child(TreeNode("file5"))
    root.children[1].add_child(TreeNode("file6"))
    # Цель поиска
    goal = "file5"

    r = solve(root, goal)
    print("Первое дерево-пример:", r)

    root2 = TreeNode("dir1")
    root2.add_child(TreeNode("dir2"))
    root2.add_child(TreeNode("dir3"))
    root2.children[1].add_child(TreeNode("file4"))
    root2.children[1].add_child(TreeNode("dir4"))
    root2.children[1].children[1].add_child(TreeNode("file5"))
    root2.children[1].children[1].add_child(TreeNode("file6"))
    # Цель поиска
    goal = "dir4"
    goal2 = "file7"

    r = solve(root2, goal)
    print("Второе дерево:", r)

    r = solve(root2, goal2)
    print("Второе дерево, поиск file7:", r)
