#!/usr/bin/env  python3

import click
import sys
from xopen import xopen
from typing import Tuple
from dataclasses import dataclass, field
import dataclasses_json
from dataclasses_json import config
from math import sqrt


@dataclass
class Stats(dataclasses_json.DataClassJsonMixin):
    n: int = field(
        default_factory=int,
        metadata=config(exclude=lambda x: True),
    )
    sum: int = 0
    sum_square: int = field(
        default_factory=int,
        metadata=config(exclude=lambda x: True),
    )
    min: int = sys.maxsize
    max: int = 0

    def update(self, x: int):
        self.n += 1
        self.sum += x
        self.sum_square += x * x
        if x < self.min:
            self.min = x
        if x > self.max:
            self.max = x

    def __iadd__(self, other: "Stats") -> "Stats":
        self.n += other.n
        self.sum += other.sum
        self.sum_square += other.sum_square
        if other.min < self.min:
            self.min = other.min
        if other.max > self.max:
            self.max = other.max

        return self

    @property
    def mean(self) -> float:
        return float(self.sum) / self.n if self.n >= 0 else 0.0

    @property
    def variance(self) -> float:
        if self.n > 1:
            return (float(self.sum_square) - float(self.sum * self.sum) / self.n) / (
                self.n - 1
            )
        else:
            return 0.0

    @property
    def sdev(self) -> float:
        return sqrt(self.variance)

    def to_dict(
        self,
        encode_json: bool = False,
    ) -> dict[str, dataclasses_json.core.Json]:
        """
        Override the method in order to add computable properties to JSON
        https://github.com/lidatong/dataclasses-json/issues/176
        """

        # first call the parent method to get non-computable properties
        data = super().to_dict(encode_json=encode_json)

        # then manually set computable properties
        data["mean"] = self.mean
        data["sdev"] = self.sdev

        return data


@dataclass
class Document(dataclasses_json.DataClassJsonMixin):
    filename: str
    char_count: Stats = field(default_factory=Stats)
    unicode_count: Stats = field(default_factory=Stats)
    word_count: Stats = field(default_factory=Stats)
    line_count: int = 0

    def update(self, line: str):
        self.line_count += 1
        self.char_count.update(len(line.encode("utf-8")))
        self.unicode_count.update(len(line))
        self.word_count.update(len(line.split()))

    def __str__(self) -> str:
        return f"{self.line_count=}\n{self.char_count=}\n{self.unicode_count=}\n{self.word_count=}"

    def __repr__(self) -> str:
        return str(self)

    def __iadd__(self, other: "Document") -> "Document":
        self.line_count += other.line_count
        self.char_count += other.char_count
        self.unicode_count += other.unicode_count
        self.word_count += other.word_count

        return self


@dataclass
class AllDocuments(dataclasses_json.DataClassJsonMixin):
    char_count: Stats = field(default_factory=Stats)
    unicode_count: Stats = field(default_factory=Stats)
    word_count: Stats = field(default_factory=Stats)
    line_count: Stats = field(default_factory=Stats)

    def __iadd__(self, other: "Document") -> "AllDocuments":
        self.line_count.update(other.line_count)
        self.char_count += other.char_count
        self.unicode_count += other.unicode_count
        self.word_count += other.word_count

        return self


@click.command()
@click.argument("files", nargs=-1)
def wc(
    files: Tuple[str],
):
    # line_per_doc: Stats = Stats()
    all_docs: AllDocuments = AllDocuments()
    for filename in files:
        with xopen(filename) as cin:
            doc = Document(filename)
            for line in cin:
                doc.update(line)
            # line_per_doc.update(doc.line_count)
            all_docs += doc

        print(doc.to_json())

    # print(line_per_doc.to_json())
    print(all_docs.to_json())


if __name__ == "__main__":
    wc()
