#!/usr/bin/env  python3

import click
import sys
from xopen import xopen
from typing import Tuple
from dataclasses import dataclass, field
import dataclasses_json
from dataclasses_json import config
from math import sqrt
from multiprocessing import Pool


@dataclass
class Stats(dataclasses_json.DataClassJsonMixin):
    """
    Class to cumulate number to generate minimum, maximum, sum, mean & sdev.
    """

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


dataclasses_json.cfg.global_config.encoders[Stats] = lambda stats: stats.to_dict()


@dataclass
class Document(dataclasses_json.DataClassJsonMixin):
    """
    Per document byte, char, word & line Statistics.
    """

    filename: str
    bytes: Stats = field(default_factory=Stats)
    char: Stats = field(default_factory=Stats)
    word: Stats = field(default_factory=Stats)
    line: int = 0

    def update(self, line: str):
        self.line += 1
        self.bytes.update(len(line.encode("utf-8")))
        self.char.update(len(line))
        self.word.update(len(line.split()))

    def __str__(self) -> str:
        return f"{self.line=}\n{self.bytes=}\n{self.char=}\n{self.word=}"

    def __repr__(self) -> str:
        return str(self)

    def __iadd__(self, other: "Document") -> "Document":
        self.line += other.line
        self.bytes += other.bytes
        self.char += other.char
        self.word += other.word

        return self


@dataclass
class AllDocuments(dataclasses_json.DataClassJsonMixin):
    """
    A class to handle the overall document statistics.
    """

    bytes: Stats = field(default_factory=Stats)
    char: Stats = field(default_factory=Stats)
    word: Stats = field(default_factory=Stats)
    line: Stats = field(default_factory=Stats)

    def __iadd__(self, other: "Document") -> "AllDocuments":
        self.line.update(other.line)
        self.bytes += other.bytes
        self.char += other.char
        self.word += other.word

        return self


def create_document(filename: str) -> Document:
    """
    Helper function to process documents in parallel.
    """
    with xopen(filename) as cin:
        doc = Document(filename)
        for line in cin:
            doc.update(line)

    return doc


@click.command()
@click.argument("files", nargs=-1)
def wc(
    files: Tuple[str],
):
    """
    Claculates minimum, maximum, sum, mean & sdev for bytes, chars, words & line per document and an overall for all documents.
    """
    all_docs: AllDocuments = AllDocuments()
    with Pool() as pool:
        for doc in pool.imap(create_document, files):
            all_docs += doc
            print(doc.to_json())

    print(all_docs.to_json())


if __name__ == "__main__":
    wc()
