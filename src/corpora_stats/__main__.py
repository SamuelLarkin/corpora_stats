#!/usr/bin/env  python3

import sys
from dataclasses import dataclass, field
from math import sqrt
from multiprocessing import Pool
from typing import Optional, Tuple

import click
import dataclasses_json
from dataclasses_json import config
from tabulate import tabulate
from xopen import xopen


@dataclass
class Stats(dataclasses_json.DataClassJsonMixin):
    """
    Class to cumulate number to generate minimum, maximum, sum, mean & sdev.
    """

    n: int = field(
        default_factory=int,
        metadata=config(exclude=lambda _: True),
    )
    sum: int = 0
    sum_square: int = field(
        default_factory=int,
        metadata=config(exclude=lambda _: True),
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


# [dataclasses_json extensions](https://github.com/lidatong/dataclasses-json?tab=readme-ov-file#extending)
# Specifying a custom encoder for Stats.
dataclasses_json.cfg.global_config.encoders[Stats] = lambda stats: stats.to_dict()


@dataclass
class Document(dataclasses_json.DataClassJsonMixin):
    """
    Per document byte, char, word & line Statistics.
    """

    filename: str
    line: int = 0  # We want the line count to appear next to the file name.
    bytes: Stats = field(default_factory=Stats)
    char: Stats = field(default_factory=Stats)
    word: Stats = field(default_factory=Stats)

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

    line: Stats = field(default_factory=Stats)
    bytes: Stats = field(default_factory=Stats)
    char: Stats = field(default_factory=Stats)
    word: Stats = field(default_factory=Stats)

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
@click.option(
    "-j",
    "--json",
    "do_json",
    type=bool,
    is_flag=True,
    default=False,
    show_default=True,
    help="output in json",
)
@click.option(
    "-f",
    "--tablefmt",
    "tablefmt",
    type=str,
    default="github",
    show_default=True,
    help="Table format (latex, github)",
)
def wc(
    files: Tuple[str],
    do_json: bool,
    tablefmt: str,
):
    """
    Calculates minimum, maximum, sum, mean & sdev for bytes, chars, words &
    line per document and an overall for all documents.

    \b
    corpora-stats --json MY_CORPORA \\
    | head -n -1 \\
    | mlr --ijson --opprint --barred cat
    """
    json_indent: int = 2
    all_docs: AllDocuments = AllDocuments()
    docs = []
    with Pool() as pool:
        for doc in pool.imap(create_document, files):
            all_docs += doc
            docs.append(doc)
            if do_json:
                print(doc.to_json(indent=json_indent))

    if do_json:
        print(all_docs.to_json(indent=json_indent))
    else:
        data = {
            "line": [doc.line for doc in docs],
            "filename": [doc.filename for doc in docs],
        }
        for unit in ("bytes", "char", "word"):
            for metric in ("sum", "min", "max", "mean", "sdev"):
                data[f"{unit}_{metric}"] = [
                    getattr(getattr(doc, unit), metric) for doc in docs
                ]
        print(tabulate(data, headers=data.keys(), tablefmt=tablefmt), "\n")

        all_docs = all_docs.to_dict()
        data = [[k] + list(v.values()) for k, v in all_docs.items()]
        print(
            tabulate(
                data,
                headers=["OVERALL"] + list(all_docs["bytes"].keys()),
                floatfmt="0.2f",
                tablefmt=tablefmt,
            )
        )


if __name__ == "__main__":
    wc()
