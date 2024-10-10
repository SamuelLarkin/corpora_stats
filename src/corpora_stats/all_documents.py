from dataclasses import dataclass, field

import dataclasses_json

from .stats import Stats


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
        self.bytes += other.byte
        self.char += other.char
        self.word += other.word

        return self
