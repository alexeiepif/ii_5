#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import random
import shutil
import string
from dataclasses import dataclass, field
from io import StringIO
from pathlib import Path

from colorama import Fore, Style


@dataclass
class Tree:
    directory: str
    root: Path = field(init=False)
    dir_count: int = field(init=False, default=0)
    file_count: int = field(init=False, default=0)

    def __post_init__(self) -> None:
        path = Path("temp") / self.directory
        if path.exists():
            shutil.rmtree(path)

        path.mkdir()
        self.root = path
        self.create_file_tree()

    def __format_tree(self, node: Path, branch: str = "") -> str:
        result = StringIO()
        if node.is_file():
            return ""
        # Преобразуем итератор в список
        children = list(node.iterdir())
        children.sort()
        for i, child in enumerate(children):
            item = f"{branch}{'└── ' if i == len(children) - 1 else '├── '}"
            name = child.name
            color = Fore.GREEN if child.is_file() else Fore.YELLOW
            result.write(f"{item}{color}{name}{Style.RESET_ALL}\n")
            new_branch = f"{branch}{'    ' if i == len(children) - 1 else '│   '}"
            result.write(self.__format_tree(child, new_branch))
        return result.getvalue()

    def __str__(self) -> str:
        header = f"{Fore.BLUE}{self.root.name}{Style.RESET_ALL}\n"
        body = self.__format_tree(self.root)
        footer = f"\n{Fore.YELLOW}Directories: {self.dir_count}, "
        footer += f"{Fore.GREEN}Files: {self.file_count}{Style.RESET_ALL}"
        return header + body + footer

    def generate_random_content(self, size=50):
        """Генерирует случайное содержимое файла."""
        return "".join(random.choices(string.ascii_letters + string.digits, k=size))

    def create_file_tree(
        self, depth: int = 10, breadth: int = 5, duplicate_chance: float = 0.01
    ) -> None:
        """Создаёт синтетическое дерево файлов."""

        # Словарь для отслеживания содержимого файлов и добавления дубликатов
        content_pool = []

        def add_children(node: Path, current_depth: int, sw: bool = True) -> None:
            if current_depth >= depth or self.file_count + self.dir_count >= 300:
                return

            for _ in range(random.randint(1, breadth)):
                if current_depth:
                    is_file = random.choice([True, False])
                else:
                    is_file = False
                if is_file:
                    # Создаём файл
                    if random.random() < duplicate_chance and content_pool and sw:
                        # Создаём дубликат
                        content = random.choice(content_pool)
                        sw = False
                    else:
                        # Создаём уникальное содержимое
                        content = self.generate_random_content()
                        content_pool.append(content)

                    child = node / f"file_{self.file_count}.txt"
                    child.write_text(content)
                    self.file_count += 1
                    if self.file_count >= 120:
                        return
                else:
                    # Создаём директорию
                    child = node / f"dir_{self.dir_count}"
                    child.mkdir()
                    self.dir_count += 1

                if child.is_dir():  # Только для директорий продолжаем рекурсию
                    add_children(child, current_depth + 1, sw)

        add_children(self.root, 0)


# Пример использования
if __name__ == "__main__":
    tree = Tree("root")
    print(tree)
