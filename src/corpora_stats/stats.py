from dataclasses import dataclass, field
from math import sqrt
from typing import Type, TypeVar

import dataclasses_json
from dataclasses_json import config
from dataclasses_json.core import Json

A = TypeVar("A", bound="DataClassJsonMixin")


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
    min: int | None = None
    max: int = 0

    def update(self, x: int):
        self.n += 1
        self.sum += x
        self.sum_square += x * x
        if self.min is None or x < self.min:
            self.min = x
        if x > self.max:
            self.max = x

    def __iadd__(self, other: "Stats") -> "Stats":
        self.n += other.n
        self.sum += other.sum
        self.sum_square += other.sum_square
        if other.min is not None:
            if self.min is None or other.min < self.min:
                self.min = other.min
        if other.max > self.max:
            self.max = other.max

        return self

    @property
    def mean(self) -> float:
        return float(self.sum) / self.n if self.n > 0 else 0.0

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
        # NOTE: min can be None but we would like it to show as 0.
        data["min"] = data["min"] or 0
        data["count"] = data["sum"]
        del data["sum"]

        # then manually set computable properties
        data["mean"] = self.mean
        data["sdev"] = self.sdev

        return data

    @classmethod
    def from_dict(cls: Type[A], kvs: Json, *, infer_missing=False) -> A:
        a = super().from_dict(kvs, infer_missing=infer_missing)
        mean = float(kvs["mean"])
        sdev = float(kvs["sdev"])
        a.n = int(a.sum / mean)
        a.sum_square = int(sdev * sdev * (a.n - 1) + (a.sum * a.sum / a.n))

        return a


# [dataclasses_json extensions](https://github.com/lidatong/dataclasses-json?tab=readme-ov-file#extending)
# Specifying a custom encoder for Stats.
dataclasses_json.cfg.global_config.encoders[Stats] = lambda stats: stats.to_dict()
dataclasses_json.cfg.global_config.decoders[Stats] = lambda stats: Stats.from_dict(
    stats
)
