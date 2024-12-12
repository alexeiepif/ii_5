#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import random
import string
from dataclasses import dataclass, field
from io import StringIO
from xml.dom import minidom
from xml.etree import ElementTree as ET

from colorama import Fore, Style


@dataclass
class TreeNode:
    state: str
    parent: "TreeNode | None" = None
    children: list["TreeNode"] = field(default_factory=list)
    content: str | None = None

    def add_child(self, child: "TreeNode") -> None:
        self.children.append(child)

    def is_file(self) -> bool:
        return self.content is not None

    def __repr__(self) -> str:
        return f"<{self.state}>"

    def __hash__(self):
        return hash(self.state)

    def __len__(self) -> int:
        return len(self.children)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, TreeNode):
            return NotImplemented
        return self.state == other.state and self.children == other.children

    def __lt__(self, other: "TreeNode") -> bool:
        return len(self) < len(other)


@dataclass
class Tree:
    directory: str
    root: TreeNode = field(init=False)
    dir_count: int = field(init=False, default=0)
    file_count: int = field(init=False, default=0)

    def __post_init__(self) -> None:
        self.root = TreeNode(self.directory)
        self.create_file_tree()

    def expand(self, node: TreeNode) -> None:
        try:
            for child in node.state.iterdir():
                if not self.__should_include(child):
                    continue
                self.__increment_counts(child)
                if self.full:
                    break
                node.add_child(TreeNode(child))
        except PermissionError:
            pass

    def __format_tree(self, node: TreeNode, branch: str = "") -> str:
        result = StringIO()
        for i, child in enumerate(node.children):
            item = f"{branch}{'└── ' if i == len(node.children) - 1 else '├── '}"
            name = child.state
            color = Fore.GREEN if child.is_file() else Fore.YELLOW
            result.write(f"{item}{color}{name}{Style.RESET_ALL}\n")
            new_branch = f"{branch}{'    ' if i == len(node.children) - 1 else '│   '}"
            result.write(self.__format_tree(child, new_branch))
        return result.getvalue()

    def __str__(self) -> str:
        header = f"{Fore.BLUE}{self.root.state}{Style.RESET_ALL}\n"
        body = self.__format_tree(self.root)
        footer = f"\n{Fore.YELLOW}Directories: {self.dir_count}, "
        footer += f"{Fore.GREEN}Files: {self.file_count}{Style.RESET_ALL}"
        return header + body + footer

    def path_states(self, node: TreeNode) -> list[str]:
        states = []
        while node.parent:
            states.append(node.state)
            node = node.parent
        states.reverse()
        return states

    def generate_random_content(self, size=50):
        """Генерирует случайное содержимое файла."""
        return "".join(random.choices(string.ascii_letters + string.digits, k=size))

    def create_file_tree(self, depth=10, breadth=5, duplicate_chance=0.01):
        """Создаёт синтетическое дерево файлов."""

        # Словарь для отслеживания содержимого файлов и добавления дубликатов
        content_pool = []

        def add_children(node, current_depth, sw=True):
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

                    child = TreeNode(
                        f"file_{self.file_count}", parent=node, content=content
                    )
                    self.file_count += 1
                    if self.file_count >= 120:
                        return
                else:
                    # Создаём директорию
                    child = TreeNode(f"dir_{self.dir_count}", parent=node)
                    self.dir_count += 1

                node.add_child(child)

                if child.content is None:  # Только для директорий продолжаем рекурсию
                    add_children(child, current_depth + 1, sw)

        add_children(self.root, 0)
        return self.root

    def save_xml(self, file_path: str) -> None:
        def build_xml_element(node: TreeNode) -> ET.Element:
            is_folder = not node.is_file()
            name = f"{node.state}/" if is_folder else node.state
            # Создаём элемент для текущего узла
            if is_folder:
                element = ET.Element("node", attrib={"name": name})
            else:
                element = ET.Element(
                    "node", attrib={"name": name, "content": node.content}
                )

            # Рекурсивно добавляем детей
            for child in node.children:
                child_element = build_xml_element(child)
                element.append(child_element)

            return element

        tree = ET.ElementTree(build_xml_element(self.root))

        raw_string = ET.tostring(tree.getroot(), encoding="unicode")
        parsed = minidom.parseString(raw_string)
        formated_xml = parsed.toprettyxml(indent="  ")

        with open(file_path, "w", encoding="utf-8") as f:
            f.write(formated_xml)


# Пример использования
if __name__ == "__main__":
    tree = Tree("root")
    print(tree)
