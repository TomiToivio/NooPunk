"""CWN 6.3 — The Graced (issue #1068).

A Graced buys permanent arts with art points. The two rules that matter and that a naive implementation gets
wrong:

* **Points are per level and accumulate** — 2 at 1st, then 1, 1, 2, 0, 1, 0, 2, 1, 1 for levels 2-10. They are
  saved, not reset.
* **Arts are permanent.** Once bought, an art cannot be traded in. The single exception is the Alacrity series,
  where a lower version may be upgraded later.

Graced characters **cannot** take the Spellcaster or Summoner Edges: their magic is already manifesting physically,
and the cyberware prohibition that comes with those Edges has no value for a knack that does not use it.

The arts catalogue below is deliberately partial: it holds the entries whose cost the SRD states plainly
(1- and 2-point arts). The full catalogue is a transcription job, and inventing entries would be worse than
admitting the gap.
"""
from __future__ import annotations

from dataclasses import dataclass, field

#: Art points granted at each character level (CWN 6.3.1 table). They accumulate.
ART_POINTS_BY_LEVEL = {1: 2, 2: 1, 3: 1, 4: 2, 5: 0, 6: 1, 7: 0, 8: 2, 9: 1, 10: 1}

#: Verified arts: id -> (cost, upgradeable).
ARTS = {
    "arcane_skill": (1, False),
    "blades_of_will": (1, False),
    "brazen_thews": (1, False),
    "faultless_grace": (1, False),
    "flying_steps": (1, False),
    "hand_of_doom": (1, False),
    "hundred_faces": (2, False),
    "basic_alacrity": (2, True),
}

#: Edges a Graced may never take (6.3.0).
FORBIDDEN_EDGES = ("Spellcaster", "Summoner")


class GracedError(ValueError):
    """A rule was about to be broken."""


def art_points(level: int) -> int:
    """Cumulative art points available at a level; points are saved, never reset."""
    if level < 1:
        raise GracedError("level starts at 1")
    total, spent = 0, 0
    for lvl in range(1, level + 1):
        total += ART_POINTS_BY_LEVEL.get(lvl, 0)
    return total


@dataclass
class Graced:
    level: int = 1
    arts: list[str] = field(default_factory=list)
    _spent: int = 0

    def __post_init__(self):
        if self.level < 1:
            raise GracedError("level starts at 1")

    @property
    def available(self) -> int:
        return art_points(self.level) - self._spent

    def buy(self, art: str) -> None:
        if art not in ARTS:
            raise GracedError(f"unknown art {art!r}")
        cost, _ = ARTS[art]
        if art in self.arts:
            raise GracedError("an art is permanent: it cannot be bought twice")
        if cost > self.available:
            raise GracedError(f"{art} costs {cost}, only {self.available} points available")
        self.arts.append(art)
        self._spent += cost

    def upgrade(self, old: str, new: str) -> None:
        """The Alacrity exception: a lower version may be upgraded, nothing else may."""
        if old not in self.arts:
            raise GracedError(f"{old} is not owned")
        if not ARTS.get(old, (0, False))[1]:
            raise GracedError(f"{old} is not an upgradeable art")
        cost_new, _ = ARTS[new]
        cost_old, _ = ARTS[old]
        difference = cost_new - cost_old
        if difference > self.available:
            raise GracedError("not enough points for the upgrade")
        self.arts.remove(old)
        self.arts.append(new)
        self._spent += difference


def may_take_edge(edge: str) -> bool:
    return edge not in FORBIDDEN_EDGES
