"""The investigative layer: GUMSHOE's core-clue principle on the CWN chassis (#704).

The single rule this module exists to enforce:

    **Finding information is not a roll. Interpreting it is not a roll. Acting on it is.**

GUMSHOE's insight is that a competent investigator does not fail to *see* the thing that
matters; the die decides danger, time and quality, not whether the plot exists. NoöPunk
keeps that and puts the CWN `2d6` check exactly where it belongs: on the action that
follows, and on the risks taken to get there.

Three separations, and they are the design:

* **Discovery** is automatic when the character holds the relevant competency. No check,
  no difficulty, no failure. A clue may offer an alternative route (an unlisted but
  plausible method), which the GM grants rather than rolls.
* **Interpretation** belongs to the player. The module can list what supports and what
  contradicts a hypothesis; it may never set the player's confidence or announce a verdict.
  A wrong hypothesis is a legal game state, and an anomaly may have an ordinary explanation.
* **Action** is where CWN lives: forcing a door, tailing a suspect, keeping a patient calm.
  Those roll, and they cost time, Strain or danger.

No text from the GUMSHOE SRD is reproduced. The SRD is CC BY 3.0 and its attribution
requirements are recorded in `docs/rules/GUMSHOE_INVESTIGATION_LAYER.md`.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum


class InvestigationError(ValueError):
    """Raised when a case is malformed or a call breaks the discovery rule."""


class ClueKind(str, Enum):
    CORE = "core"          # required to leave the scene
    OPTIONAL = "optional"  # enriches, never blocks


@dataclass(frozen=True)
class Clue:
    """A fact the world contains. Not a conclusion."""

    id: str
    scene_id: str
    kind: ClueKind
    competency: str
    fact: str
    leads_to: tuple[str, ...] = ()
    obscure: bool = False   # a core clue may not depend on this alone

    def __post_init__(self) -> None:
        if not self.id or not self.fact:
            raise InvestigationError("a clue needs an id and a fact")


@dataclass(frozen=True)
class Scene:
    """A location or encounter that a case passes through."""

    id: str
    title: str
    clues: tuple[Clue, ...] = ()

    def core_clues(self) -> tuple[Clue, ...]:
        return tuple(c for c in self.clues if c.kind is ClueKind.CORE)


@dataclass(frozen=True)
class Case:
    """A mystery graph whose exits must not be gated behind luck."""

    id: str
    scenes: tuple[Scene, ...]

    def scene(self, scene_id: str) -> Scene:
        for scene in self.scenes:
            if scene.id == scene_id:
                return scene
        raise InvestigationError(f"no scene {scene_id!r} in case {self.id!r}")

    def validate(self) -> None:
        """Every scene must be leavable, and every lead must point somewhere real.

        A scene with no core clue is a dead end; a core clue that only one obscure
        competency can reach is a dead end for any table that did not bring it.
        """
        if not self.scenes:
            raise InvestigationError("a case needs at least one scene")
        ids = {scene.id for scene in self.scenes}
        for scene in self.scenes:
            core = scene.core_clues()
            if not core:
                raise InvestigationError(f"scene {scene.id!r} has no core clue; it is a dead end")
            if all(clue.obscure for clue in core):
                raise InvestigationError(
                    f"scene {scene.id!r} gates its only exit behind an obscure competency"
                )
            for clue in scene.clues:
                for target in clue.leads_to:
                    if target not in ids:
                        raise InvestigationError(
                            f"clue {clue.id!r} leads to unknown scene {target!r}"
                        )


@dataclass
class Investigator:
    """Ratings above zero mean competent; the number is a spend, not a chance to fail."""

    name: str
    ratings: dict[str, int] = field(default_factory=dict)

    def is_competent(self, competency: str) -> bool:
        return self.ratings.get(competency, 0) > 0

    def spend(self, competency: str, amount: int = 1) -> int:
        """Spend from a rating for extra information. Never for permission to find a clue."""
        if amount < 1:
            raise InvestigationError("a spend is at least one point")
        available = self.ratings.get(competency, 0)
        if available < amount:
            raise InvestigationError(f"{self.name} cannot spend {amount} from {competency}")
        self.ratings[competency] = available - amount
        return self.ratings[competency]


@dataclass(frozen=True)
class Discovery:
    """What a scene yields to a given investigator, and why."""

    scene_id: str
    clues: tuple[Clue, ...]
    granted_by: str            # "competency" or "alternative_method"
    can_leave: bool


def discover(
    case: Case,
    scene_id: str,
    investigator: Investigator,
    *,
    alternative_method: bool = False,
) -> Discovery:
    """Yield the clues a competent investigator simply *gets*.

    No roll, and no difficulty: GUMSHOE's principle is that competency buys the
    information. ``alternative_method`` is the GM granting a plausible approach that no
    listed ability covers - the SRD is explicit that the designated ability is "just one
    possibility, not a straight jacket".
    """
    scene = case.scene(scene_id)
    core = scene.core_clues()
    has_competency = any(investigator.is_competent(clue.competency) for clue in core)

    if not (has_competency or alternative_method):
        return Discovery(scene_id=scene_id, clues=(), granted_by="none", can_leave=False)

    # A competent investigator receives the core clue *and* every optional clue their
    # own competencies cover. Optional clues they cannot cover stay in the world.
    granted = [clue for clue in core]
    granted.extend(
        clue for clue in scene.clues
        if clue.kind is ClueKind.OPTIONAL and investigator.is_competent(clue.competency)
    )
    return Discovery(
        scene_id=scene_id,
        clues=tuple(granted),
        granted_by="competency" if has_competency else "alternative_method",
        can_leave=True,
    )


class Stance(str, Enum):
    """How a clue bears on a hypothesis. The system classifies evidence, not truth."""

    SUPPORTS = "supports"
    CONTRADICTS = "contradicts"
    NEUTRAL = "neutral"


@dataclass
class Hypothesis:
    """A player's theory. Confidence is set by the player and by nothing else.

    This is the guard against a system that solves the mystery for the table: the model may
    say which facts bear on the theory, but never whether the theory is right.
    """

    id: str
    statement: str
    confidence: int = 0            # 0-100, player's own estimate
    evidence: dict[str, Stance] = field(default_factory=dict)

    def consider(self, clue: Clue, stance: Stance) -> None:
        self.evidence[clue.id] = stance

    def support_count(self) -> int:
        return sum(1 for stance in self.evidence.values() if stance is Stance.SUPPORTS)

    def contradiction_count(self) -> int:
        return sum(1 for stance in self.evidence.values() if stance is Stance.CONTRADICTS)

    def set_confidence(self, value: int) -> None:
        """Only a player calls this. No function here derives confidence from evidence."""
        if not 0 <= value <= 100:
            raise InvestigationError("confidence is a percentage")
        self.confidence = value


def hypotheses_remain_open(hypotheses: list[Hypothesis]) -> bool:
    """A case is not solved by the model. This always returns True; it exists to be called.

    If a future refactor adds a path that resolves a case automatically, this function is
    the place the intent is recorded and the place a reviewer will look.
    """
    return True
