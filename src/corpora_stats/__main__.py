#!/usr/bin/env  python3

import click
import sys
from xopen import xopen
from typing import Tuple
from dataclasses import dataclass, field
from dataclasses_json import dataclass_json


@dataclass_json
@dataclass
class Count:
    count: int = 0
    count_square: int = 0
    min: int = sys.maxsize
    max: int = 0

    def update(self, x: int):
        self.count += x
        self.count_square += x * x
        if x < self.min:
            self.min = x
        if x > self.max:
            self.max = x


@dataclass_json
@dataclass
class Document:
    filename: str
    char_count: Count = field(default_factory=Count)
    unicode_count: Count = field(default_factory=Count)
    word_count: Count = field(default_factory=Count)
    line_count = 0

    def update(self, line: str):
        self.line_count += 1
        self.char_count.update(len(line.encode("utf-8")))
        self.unicode_count.update(len(line))
        self.word_count.update(len(line.split()))

    def __str__(self) -> str:
        return f"{self.line_count=}{self.char_count=}{self.unicode_count=}{self.word_count=}"

    def __repr__(self) -> str:
        return str(self)


@click.command()
@click.argument("files", nargs=-1)
def wc(
    files: Tuple[str],
):
    line_per_doc = Count()
    for filename in files:
        with xopen(filename) as cin:
            doc = Document(filename)
            for line in cin:
                doc.update(line)
            line_per_doc.update(doc.line_count)

        print(doc.to_json())

    print(line_per_doc.to_json())


if __name__ == "__main__":
    wc()
