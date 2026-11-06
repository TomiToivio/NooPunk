"""Dream Scenes — narrative context, never a new rules engine (#1230).

Dreams are involuntary, often ambiguous, and many nights have none. A dream can carry a memory,
a telepathic contact, a spontaneous precognitive impression or a psychic attack, but the
underlying resolution remains CWN/SWN: this module only selects and records the scene's narrative
ground truth against Tony's subjective report.
"""

from __future__ import annotations

import random
from dataclasses import dataclass
from enum import Enum


class DreamError(ValueError):
    """An invalid dream request."""


class DreamKind(str, Enum):
    NONE = "none"
    ORDINARY = "ordinary"
    LIFEPATH_MEMORY = "lifepath_memory"
    TELEPATHIC_CONTACT = "telepathic_contact"
    SPONTANEOUS_PRECOGNITION = "spontaneous_precognition"
    PSYCHIC_ATTACK = "psychic_attack"
    ONTOLOGICAL_SHOCK = "ontological_shock"


DREAM_WEIGHTS = {
    DreamKind.NONE: 40,
    DreamKind.ORDINARY: 18,
    DreamKind.LIFEPATH_MEMORY: 16,
    DreamKind.TELEPATHIC_CONTACT: 10,
    DreamKind.SPONTANEOUS_PRECOGNITION: 8,
    DreamKind.PSYCHIC_ATTACK: 5,
    DreamKind.ONTOLOGICAL_SHOCK: 3,
}


@dataclass(frozen=True)
class DreamScene:
    kind: DreamKind
    subjective_report: str
    ground_truth: str
    source: str = ""
    reliable: bool = False
    possible_future: bool = False
    mechanic: str = ""

    @property
    def is_playable_dream(self) -> bool:
        return self.kind is not DreamKind.NONE


class DreamEngine:
    """Deterministic selection by night; the GM supplies the authored detail."""

    def choose(
        self,
        night: int,
        *,
        seed: int = 0,
        forced: DreamKind | str | None = None,
        source: str = "",
        rng: random.Random | None = None,
    ) -> DreamScene:
        if night < 1:
            raise DreamError("night must be >= 1")
        kind = DreamKind(forced) if forced is not None else self._roll(night, seed, rng)
        if kind is DreamKind.NONE:
            return DreamScene(kind, "", "")
        return DreamScene(
            kind=kind,
            subjective_report="",
            ground_truth="",
            source=source,
            reliable=kind
            not in (DreamKind.SPONTANEOUS_PRECOGNITION, DreamKind.ONTOLOGICAL_SHOCK),
            possible_future=kind is DreamKind.SPONTANEOUS_PRECOGNITION,
            mechanic="SWN/CWN check only if the authored scene actually calls for one",
        )

    @staticmethod
    def _roll(night: int, seed: int, rng: random.Random | None) -> DreamKind:
        source = rng or random.Random(seed + night * 7919)
        total = sum(DREAM_WEIGHTS.values())
        pick = source.randrange(total)
        cursor = 0
        for kind, weight in DREAM_WEIGHTS.items():
            cursor += weight
            if pick < cursor:
                return kind
        return DreamKind.NONE


__all__ = ["DREAM_WEIGHTS", "DreamEngine", "DreamError", "DreamKind", "DreamScene"]
