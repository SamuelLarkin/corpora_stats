from dataclasses import dataclass, field

import dataclasses_json

from .stats import Stats


@dataclass
class Document(dataclasses_json.DataClassJsonMixin):
    """
    Per document byte, char, word & line Statistics.
    """

    filename: str
    line: int = 0  # We want the line count to appear next to the file name.
    byte: Stats = field(default_factory=Stats)
    char: Stats = field(default_factory=Stats)
    word: Stats = field(default_factory=Stats)

    def update(self, line: bytes):
        self.line += 1
        self.byte.update(len(line))
        self.char.update(len(line.decode("utf-8")))
        self.word.update(len(line.split()))

    def __str__(self) -> str:
        return f"{self.line=}\n{self.byte=}\n{self.char=}\n{self.word=}"

    def __repr__(self) -> str:
        return str(self)

    def __iadd__(self, other: "Document") -> "Document":
        self.line += other.line
        self.byte += other.byte
        self.char += other.char
        self.word += other.word

        return self
