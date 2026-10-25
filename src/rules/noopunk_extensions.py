"""Original NoöPunk extension kernel: ubiquitous networks and learnable natural PSI.

Opt-in subsystem, not a replacement for the existing tabletop 1d10 or Fate resolvers.
All operations are deterministic, offline, and serializable. No publisher prose.
"""
from __future__ import annotations

from dataclasses import dataclass, field

CHANNELS = frozenset({"wired", "radio", "mesh", "bci", "courier", "psychic", "psychotronic"})
DISCIPLINES = frozenset({"telepathy", "perception", "precognition", "influence", "psychokinesis", "healing", "shielding"})


@dataclass(frozen=True)
class Link:
    source: str
    target: str
    channel: str
    operational: bool = True
    authorized: bool = False

    def __post_init__(self):
        if self.channel not in CHANNELS:
            raise ValueError("unknown channel")
        if not self.source or not self.target:
            raise ValueError("endpoints required")


@dataclass(frozen=True)
class Reach:
    reachable: bool
    channel_path: tuple[str, ...] = ()
    reason: str = ""


def reach(links: tuple[Link, ...], source: str, target: str,
          *, channels: frozenset[str] = CHANNELS,
          require_authorization: bool = False) -> Reach:
    """Enumerate actual hops, not inferred social ties or a magical omninet.

    Ubiquitous means heterogeneous reachable devices and media can form a mesh;
    neither physical air gaps nor psychic ability automatically provide TCP access.
    """
    if source == target:
        return Reach(True, (), "local")
    if not source or not target:
        return Reach(False, (), "unknown endpoint")
    queue = [(source, ())]
    seen = {source}
    for node, path in queue:
        for link in links:
            if (not link.operational or link.channel not in channels
                    or (require_authorization and not link.authorized)
                    or link.source != node or link.target in seen):
                continue
            new_path = path + (link.channel,)
            if link.target == target:
                return Reach(True, new_path, "connected")
            seen.add(link.target)
            queue.append((link.target, new_path))
    return Reach(False, (), "no concrete route")


@dataclass
class NaturalPsi:
    """Learning requires practice, not a class, mutation, virus or equipment.

    Discipline ratings 0..4 are an *optional* extension profile. Effort is
    committed to named effects and restored by releasing the effect or resting.
    """
    aptitude: bool = True
    disciplines: dict[str, int] = field(default_factory=dict)
    capacity: int = 1
    commitments: dict[str, int] = field(default_factory=dict)

    def __post_init__(self):
        if self.capacity < 0 or any(k not in DISCIPLINES or not 0 <= v <= 4
                                   for k, v in self.disciplines.items()):
            raise ValueError("invalid PSI sheet")
        if any(v <= 0 for v in self.commitments.values()) or self.used > self.capacity:
            raise ValueError("invalid PSI commitments")

    @property
    def used(self) -> int:
        return sum(self.commitments.values())

    @property
    def available(self) -> int:
        return self.capacity - self.used

    def learn(self, discipline: str) -> int:
        if not self.aptitude or discipline not in DISCIPLINES:
            raise ValueError("natural aptitude and known discipline required")
        current = self.disciplines.get(discipline, -1)
        if current >= 4:
            raise ValueError("already mastered")
        self.disciplines[discipline] = current + 1
        return current + 1

    def commit(self, effect_id: str, discipline: str, cost: int = 1) -> None:
        if not effect_id or effect_id in self.commitments:
            raise ValueError("unique effect ID required")
        if discipline not in self.disciplines:
            raise ValueError("discipline not learned")
        if cost <= 0 or cost > self.available:
            raise ValueError("insufficient Effort")
        self.commitments[effect_id] = cost

    def release(self, effect_id: str) -> None:
        if effect_id not in self.commitments:
            raise KeyError(effect_id)
        del self.commitments[effect_id]

    def rest(self) -> None:
        self.commitments.clear()

    def to_dict(self) -> dict:
        return {"aptitude": self.aptitude, "disciplines": dict(self.disciplines),
                "capacity": self.capacity, "commitments": dict(self.commitments)}

    @classmethod
    def from_dict(cls, data: dict) -> "NaturalPsi":
        return cls(**data)
