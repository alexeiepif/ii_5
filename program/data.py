#!/usr/bin/env python3
# -*- coding: utf-8 -*-


from files_tree import Tree
from tree import Problem, iterative_deepening_search


class DuplicateProblem(Problem):
    def __init__(self, initial=None, goal=None):
        super().__init__(initial, goal)
        self.content_hashes = {}
        self.duplicate = None

    def actions(self, state):
        if state.is_file():
            h = hash(state.content)
            if h in self.content_hashes.keys():
                if state != self.content_hashes[h]:
                    self.duplicate = (state, self.content_hashes[h])
            else:
                self.content_hashes[h] = state
        yield from state.children

    def result(self, state, action):
        return action


def solve(tree):
    problem = DuplicateProblem(tree.root)
    iterative_deepening_search(problem)
    dupl = problem.duplicate
    if dupl is None:
        return []
    dupl_files = tuple(map(tree.path_states, dupl))
    dupl_contents = tuple(map(lambda x: x.content, dupl))
    return dupl_files, dupl_contents


if __name__ == "__main__":
    tree = Tree("root")
    tree.save_xml("XML/tree.xml")
    print(tree)
    para = solve(tree)
    if para:
        files = tuple(map(lambda x: "/".join(x), para[0]))
        content = para[1]
        print(files, "\n", content)
    else:
        print("Нет дубликатов")
