"""Original optional crisis and NHI-contact procedures for NoöPunk (#564/#572).

These are social-world consequences, not damage tracks or moral alignments.
No third-party setting, rules text, network services, or random engine required.
"""
from dataclasses import dataclass


def clamp(value: int, minimum: int = 0, maximum: int = 6) -> int:
    return max(minimum, min(maximum, value))


@dataclass
class LocalCrisis:
    scarcity: int = 0
    trust: int = 3
    exposure: int = 0

    def __post_init__(self) -> None:
        if not all(isinstance(value, int) and 0 <= value <= 6
                   for value in (self.scarcity, self.trust, self.exposure)):
            raise ValueError("local crisis tracks must be integer 0..6")

    def apply(self, *, lost_supplies: int = 0, cooperation: int = 0,
              hazard: int = 0) -> None:
        self.scarcity = clamp(self.scarcity + lost_supplies)
        self.trust = clamp(self.trust + cooperation)
        self.exposure = clamp(self.exposure + hazard)

    def to_dict(self) -> dict:
        return vars(self).copy()

    @classmethod
    def from_dict(cls, payload: dict) -> "LocalCrisis":
        return cls(**payload)


@dataclass
class NHIContact:
    reciprocity: int = 0
    autonomy: int = 3

    def __post_init__(self) -> None:
        if not isinstance(self.reciprocity, int) or not -6 <= self.reciprocity <= 6:
            raise ValueError("reciprocity must be -6..6")
        if not isinstance(self.autonomy, int) or not 0 <= self.autonomy <= 6:
            raise ValueError("autonomy must be 0..6")

    def exchange(self, *, mutual_benefit: int = 0, imposed_dependency: int = 0) -> None:
        self.reciprocity = clamp(self.reciprocity + mutual_benefit, -6, 6)
        self.autonomy = clamp(self.autonomy - imposed_dependency)

    def to_dict(self) -> dict:
        return vars(self).copy()

    @classmethod
    def from_dict(cls, payload: dict) -> "NHIContact":
        return cls(**payload)
