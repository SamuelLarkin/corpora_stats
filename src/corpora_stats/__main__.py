#!/usr/bin/env  python3

import click
import sys
from xopen import xopen
from typing import Tuple
from dataclasses import dataclass


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


@click.command()
@click.argument("files", nargs=-1)
def wc(
    files: Tuple[str],
):
    line_per_doc = Count()
    for filename in files:
        with xopen(filename) as cin:
            char_count = Count()
            unicode_count = Count()
            word_count = Count()
            line_count = 0
            for line in cin:
                line_count += 1
                char_count.update(len(line.encode("utf-8")))
                unicode_count.update(len(line))
                word_count.update(len(line.split()))

        line_per_doc.update(line_count)
        print(f"{char_count=}")
        print(f"{unicode_count=}")
        print(f"{word_count=}")
        print(f"{line_count=}")
        print(f"{line_per_doc=}")


if __name__ == "__main__":
    wc()
