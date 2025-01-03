#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from pathlib import Path
from typing import Generator, Optional

from files_tree import Tree
from tree import Problem, iterative_deepening_search

# Решить задачу с использованием алгоритма итеративного углубления и синтетического
# набора данных. Номер варианта определяется по согласованию с преподавателем.
# Найдите два разных файла в файловом дереве, которые имеют одинаковое содержимое
# (по побайтовому сравнению), используя итеративное углубление. Дерево более ста
# файлов, и их глубина может достигать 10 уровней.


class DuplicateProblem(Problem):
    def __init__(self, initial: Optional[Path] = None, goal: None = None) -> None:
        super().__init__(initial, goal)
        self.content_hashes: dict[int, Path] = {}
        self.duplicate: Optional[tuple[Path, Path]] = None

    def actions(self, state: Path) -> Generator[Path, None, None]:
        if state.is_file():
            h = hash(state.read_bytes())
            if h in self.content_hashes.keys():
                if (
                    state != self.content_hashes[h]
                    and state.read_bytes() == self.content_hashes[h].read_bytes()
                ):
                    self.duplicate = (state, self.content_hashes[h])
            else:
                self.content_hashes[h] = state
            return
        yield from state.iterdir()

    def result(self, state: Path, action: Path) -> Path:
        return action


def solve(tree: Tree) -> tuple[tuple[Path, Path], tuple[str, ...]] | None:
    problem = DuplicateProblem(tree.root)
    iterative_deepening_search(problem)
    dupl = problem.duplicate
    if dupl is None:
        return None
    dupl_contents = tuple(map(lambda x: x.read_text(), dupl))
    return dupl, dupl_contents


if __name__ == "__main__":
    tree = Tree("root")
    print(tree)
    para = solve(tree)
    if para:
        files = tuple(map(lambda x: str(x.relative_to("temp")), para[0]))
        content = para[1]
        print(files, "\n", content)
    else:
        print("Нет дубликатов")
