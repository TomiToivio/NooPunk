"""Original NoöPunk implementation of SWN Revised psychic advancement mechanics.

Mechanics cross-reference: Stars Without Number Revised (2017), Psionics,
pp. 29-31. This module does not reproduce the book's technique catalogue.
Use the authorized rulebook for individual technique prerequisites/effects.
"""
from __future__ import annotations
from dataclasses import dataclass, field

from .swn_psionics import DISCIPLINES, PsiRulesError
from .psionics import PSYCHIC_PACKAGES

FULL = "swn_psychic"
PARTIAL = "swn_partial_psychic"

#: A psychic gains the core technique of a discipline for free at this rank, and it improves with
#: the skill rather than being purchased.
CORE_TECHNIQUE_RANK = 0
#: Every improvement of a discipline buys exactly one new technique from that discipline.
PICKS_PER_IMPROVEMENT = 1
MAX_DISCIPLINE_RANK = 4
#: A Partial Psychic may master exactly one discipline.
PARTIAL_DISCIPLINE_LIMIT = 1


@dataclass
class PsychicTraining:
    """Track a character's disciplines, advancement and learned techniques.

    Learning is distinct from activating a power: resource reservations live in
    swn_psionics.Psychic. An individual catalogue entry must be supplied by the
    scenario/rulebook, rather than assumed by the engine.
    """
    package: str
    skills: dict[str, int] = field(default_factory=dict)
    techniques: dict[str, tuple[str, int]] = field(default_factory=dict)
    #: The discipline whose improvement is waiting for its technique. The rules do not allow a pick
    #: to be banked, so an advance sets this and the next learn_technique spends it.
    pending_pick: str = ""

    def __post_init__(self) -> None:
        if self.package not in PSYCHIC_PACKAGES:
            raise PsiRulesError("a psychic package is required")
        if len(self.skills) > (1 if self.package == PARTIAL else len(DISCIPLINES)):
            raise PsiRulesError("too many disciplines for psychic package")
        for name, rank in self.skills.items():
            self._check_skill(name, rank)
        for name, (discipline, minimum) in self.techniques.items():
            if not name or not self.has_prerequisite(discipline, minimum):
                raise PsiRulesError("invalid or unqualified learned technique")
        if self.pending_pick and self.pending_pick not in self.skills:
            raise PsiRulesError("a pending technique pick needs a trained discipline")

    @staticmethod
    def _check_skill(name: str, rank: int) -> None:
        if name not in DISCIPLINES or type(rank) is not int or not 0 <= rank <= 4:
            raise PsiRulesError("invalid psychic discipline or rank")

    def has_prerequisite(self, discipline: str, minimum_rank: int = 0) -> bool:
        return (discipline in self.skills and type(minimum_rank) is int
                and 0 <= minimum_rank <= 4 and self.skills[discipline] >= minimum_rank)

    def learn_discipline(self, discipline: str) -> None:
        self._check_skill(discipline, 0)
        if discipline in self.skills:
            raise PsiRulesError("discipline already known; use advance")
        if self.package == PARTIAL and self.skills:
            raise PsiRulesError("partial psychics are restricted to one discipline")
        self.skills[discipline] = 0

    def advance(self, discipline: str) -> int:
        """Improve a trained discipline by one rank, and open its technique pick.

        The pick cannot be banked: until it is spent on a technique from this discipline, no
        further improvement is allowed.
        """
        if self.pending_pick:
            raise PsiRulesError(
                f"choose the technique for {self.pending_pick} before improving again"
            )
        if discipline not in self.skills:
            raise PsiRulesError("discipline not trained")
        if self.skills[discipline] >= MAX_DISCIPLINE_RANK:
            raise PsiRulesError("discipline already at rank four")
        self.skills[discipline] += 1
        self.pending_pick = discipline
        return self.skills[discipline]

    def core_available(self, discipline: str) -> bool:
        """The core technique is free from rank 0 and improves with the skill; it never spends a pick."""
        return self.skills.get(discipline, -1) >= CORE_TECHNIQUE_RANK

    def learn_technique(self, identifier: str, discipline: str, required_rank: int) -> None:
        """Spend the open pick on a GM-approved catalogue entry from the same discipline."""
        if not identifier or identifier in self.techniques:
            raise PsiRulesError("technique identifier must be unique")
        if not self.has_prerequisite(discipline, required_rank):
            raise PsiRulesError("technique prerequisite unmet")
        if self.pending_pick != discipline:
            raise PsiRulesError(
                f"no technique pick open for {discipline}; improve it first"
            )
        self.techniques[identifier] = (discipline, required_rank)
        self.pending_pick = ""

    def technique_access(self, identifier: str) -> bool:
        if identifier not in self.techniques:
            return False
        discipline, required_rank = self.techniques[identifier]
        return self.has_prerequisite(discipline, required_rank)

    def snapshot(self) -> dict:
        return {"package": self.package, "skills": dict(self.skills),
                "pending_pick": self.pending_pick,
                "techniques": {key: [d, r] for key, (d, r) in self.techniques.items()}}

    @classmethod
    def from_snapshot(cls, data: dict) -> "PsychicTraining":
        if not isinstance(data, dict):
            raise PsiRulesError("training snapshot must be a mapping")
        raw = data.get("techniques", {})
        if not isinstance(raw, dict):
            raise PsiRulesError("invalid technique mapping")
        try:
            techniques = {}
            for key, item in raw.items():
                if not isinstance(item, (list, tuple)) or len(item) != 2:
                    raise PsiRulesError("invalid technique record")
                techniques[key] = (item[0], item[1])
            return cls(data["package"], dict(data.get("skills", {})), techniques,
                       str(data.get("pending_pick", "")))
        except (KeyError, TypeError, ValueError) as exc:
            raise PsiRulesError("invalid psychic training snapshot") from exc
