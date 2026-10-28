"""The investigative layer: GUMSHOE's core-clue principle on the CWN chassis (#704).

The single rule this module exists to enforce:

    **Finding information is not a roll. Interpreting it is not a roll. Acting on it is.**

A competent investigator does not fail to *see* the thing that matters; the die decides
danger, time and quality, not whether the plot exists. NoöPunk keeps that and puts the CWN
`2d6` check exactly where it belongs: on the action that follows, and on the risks taken to
get there.

Three separations, and they are the design:

* **Discovery** is automatic when the character holds the relevant competency. No check, no
  difficulty, no failure. A clue may offer an alternative route (an unlisted but plausible
  method), which the referee grants rather than rolls.
* **Interpretation** belongs to the player. The module can say what supports and what
  contradicts a hypothesis; it may never set the player's confidence or announce a verdict.
  A wrong hypothesis is a legal game state, and an anomaly may have an ordinary explanation.
* **Action** is where CWN lives: forcing a door, tailing a suspect, keeping a patient calm.
  Those roll, and they cost time, Strain or danger.

Two decisions are load-bearing and easy to get wrong:

* **Competence is presence, not a positive number.** The Without Number baseline rates skills
  0-4 and untrained is the *absence* of rank 0, so `Heal 0` is a trained investigator. A layer
  that demanded a positive rating would quietly disqualify every starting character.
* **There is no investigative point economy.** GUMSHOE buys extra information with spends from
  investigative pools; NoöPunk already has one pool (SWN Effort) and refuses a second currency,
  so a *benefit* here names the CWN cost it takes instead: a check under pressure, a scene of
  time, a favour, credits. The module exposes the cost; it never charges it, and it never
  touches a skill rank.

No text from the GUMSHOE SRD is reproduced. It is CC BY 3.0 and the attribution it requires is
recorded in `docs/rules/GUMSHOE_INVESTIGATION_LAYER.md`.
"""
from __future__ import annotations

import json
from collections.abc import Iterable, Mapping
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from typing import Any


class InvestigationError(ValueError):
    """Raised when a case is malformed or a call breaks the discovery rule."""


class ClueKind(str, Enum):
    CORE = "core"          # required to leave the scene
    OPTIONAL = "optional"  # enriches, never blocks


@dataclass(frozen=True, slots=True)
class Clue:
    """A fact the world contains. Not a conclusion."""

    id: str
    scene_id: str
    kind: ClueKind
    competency: str
    fact: str
    leads_to: tuple[str, ...] = ()
    obscure: bool = False   # a core clue may not rest on this alone
    passive: bool = False   # obvious on entering; needs no declared search
    benefit: str = ""       # extra information, available for a price
    benefit_cost: str = ""  # that price, in CWN terms -- a check, a scene, a favour, credits

    def __post_init__(self) -> None:
        if not self.id or not self.fact:
            raise InvestigationError("a clue needs an id and a fact")
        if not self.competency.strip():
            raise InvestigationError(f"clue {self.id!r} needs a competency")
        if self.benefit and not self.benefit_cost.strip():
            raise InvestigationError(f"clue {self.id!r}: a benefit must name its CWN cost")
        if self.benefit_cost and not self.benefit:
            raise InvestigationError(f"clue {self.id!r}: a cost with no benefit")


@dataclass(frozen=True, slots=True)
class Benefit:
    """Extra information and the price it takes. The referee charges it, not this module."""

    clue_id: str
    text: str
    cost: str


@dataclass(frozen=True, slots=True)
class Scene:
    """A location or encounter that a case passes through."""

    id: str
    title: str
    clues: tuple[Clue, ...] = ()

    def core_clues(self) -> tuple[Clue, ...]:
        return tuple(c for c in self.clues if c.kind is ClueKind.CORE)

    def passive_clues(self) -> tuple[Clue, ...]:
        return tuple(c for c in self.clues if c.passive)


@dataclass(frozen=True, slots=True)
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

        A scene with no core clue is a dead end; a scene whose only core clue needs an
        obscure competency is a dead end for any table that did not bring it; a lead to a
        scene that does not exist is a broken graph.
        """
        if not self.scenes:
            raise InvestigationError("a case needs at least one scene")
        ids = {scene.id for scene in self.scenes}
        if len(ids) != len(self.scenes):
            raise InvestigationError("duplicate scene id")
        for scene in self.scenes:
            core = scene.core_clues()
            if not core:
                raise InvestigationError(f"scene {scene.id!r} has no core clue; it is a dead end")
            if all(clue.obscure for clue in core):
                raise InvestigationError(
                    f"scene {scene.id!r} gates its only exit behind an obscure competency"
                )
            for clue in scene.clues:
                if clue.scene_id != scene.id:
                    raise InvestigationError(
                        f"clue {clue.id!r} is filed under {scene.id!r} but claims {clue.scene_id!r}"
                    )
                for target in clue.leads_to:
                    if target not in ids:
                        raise InvestigationError(
                            f"clue {clue.id!r} leads to unknown scene {target!r}"
                        )


@dataclass(frozen=True, slots=True)
class Investigator:
    """A character's investigative competencies, read off an ordinary CWN sheet.

    Competence is the *presence* of the skill entry, because rank 0 is trained. ``ratings`` is
    kept for the one place the rules still compare characters -- the inconspicuous clue, where
    the SRD sends it to whoever has the highest current pool. Nothing spends them.
    """

    name: str
    ratings: Mapping[str, int] = field(default_factory=dict)

    @classmethod
    def from_sheet(cls, name: str, skills: Mapping[str, int]) -> Investigator:
        """Map a character sheet's skills to competencies: every listed skill counts."""
        return cls(name=name, ratings={skill: int(rank) for skill, rank in skills.items()})

    def __post_init__(self) -> None:
        for competency, rank in self.ratings.items():
            if rank < 0:
                raise InvestigationError(f"{self.name}: {competency} rank cannot be negative")

    def is_competent(self, competency: str) -> bool:
        return competency in self.ratings

    def highest(self, competencies: Iterable[str]) -> int:
        """The best listed rank among the given competencies, or 0."""
        return max((self.ratings[c] for c in competencies if c in self.ratings), default=0)


@dataclass(frozen=True, slots=True)
class Discovery:
    """What a scene yields to a given investigator, and why."""

    scene_id: str
    clues: tuple[Clue, ...]
    granted_by: str                 # "competency" | "alternative_method" | "none"
    can_leave: bool
    benefits: tuple[Benefit, ...] = ()

    @property
    def clue_ids(self) -> tuple[str, ...]:
        return tuple(clue.id for clue in self.clues)


def discover(
    case: Case,
    scene_id: str,
    investigator: Investigator,
    *,
    alternative_method: bool = False,
) -> Discovery:
    """Yield the clues a competent investigator simply *gets*.

    No roll and no difficulty: competency buys the information. Core clues are granted for the
    competencies the investigator actually holds, so a medically trained character does not also
    read the network log for free; the scene stays leavable because every scene is required to
    hold a core clue that an ordinary competency reaches, and the party is expected to cover them.

    ``alternative_method`` is the referee granting a plausible approach no listed competency
    covers -- the SRD is explicit that the designated ability is "just one possibility, not a
    straight jacket" (we quote the idea, not the page).
    """
    scene = case.scene(scene_id)
    granted = (
        list(scene.clues) if alternative_method
        else [clue for clue in scene.clues if investigator.is_competent(clue.competency)]
    )
    return Discovery(
        scene_id=scene_id,
        clues=tuple(granted),
        granted_by=("alternative_method" if alternative_method
                    else "competency" if granted else "none"),
        can_leave=any(clue.kind is ClueKind.CORE for clue in granted),
        benefits=tuple(
            Benefit(clue_id=clue.id, text=clue.benefit, cost=clue.benefit_cost)
            for clue in granted if clue.benefit
        ),
    )


def inconspicuous_finder(scene: Scene, investigators: Iterable[Investigator]) -> Investigator | None:
    """Who notices the clue nobody asked about.

    The SRD's rule for a clue in a place the party is merely passing through: the character with
    the highest current pool in the ability finds it, without anyone declaring a search. Ties go
    to the higher rank, then to the name. A table with nobody competent finds nothing.
    """
    passive = scene.passive_clues()
    competent = [person for person in investigators
                 if any(person.is_competent(clue.competency) for clue in passive)]
    if not competent:
        return None
    return max(competent, key=lambda person: (
        person.highest(clue.competency for clue in passive),
        sum(1 for clue in passive if person.is_competent(clue.competency)),
        person.name,
    ))


class Stance(str, Enum):
    """How a clue bears on a hypothesis. The system classifies evidence, not truth."""

    SUPPORTS = "supports"
    CONTRADICTS = "contradicts"
    NEUTRAL = "neutral"


@dataclass
class Hypothesis:
    """A player's theory. Confidence is set by the player and by nothing else.

    This is the guard against a system that solves the mystery for the table: the model may say
    which facts bear on the theory, but never whether the theory is right.
    """

    id: str
    statement: str
    family: str = "unclassified"    # mundane / anomalous / psychological / deliberate
    confidence: int = 0             # 0-100, the player's own estimate
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


def hypotheses_remain_open(hypotheses: Iterable[Hypothesis]) -> bool:
    """A case is not solved by the model.

    If a future refactor adds a path that resolves a case automatically, this function is where
    the intent is recorded and where a reviewer will look.
    """
    return True


# --------------------------------------------------------------------------- #
# The case graph on disk
# --------------------------------------------------------------------------- #

CASE_GRAPH_FORMAT = "noopunk-case-graph"


def _clue(raw: Mapping[str, Any], scene_id: str) -> Clue:
    return Clue(
        id=raw["id"],
        scene_id=scene_id,
        kind=ClueKind(raw.get("kind", "optional")),
        competency=raw.get("competency", ""),
        fact=raw.get("fact", ""),
        leads_to=tuple(raw.get("leads_to", ())),
        obscure=bool(raw.get("obscure", False)),
        passive=bool(raw.get("passive", False)),
        benefit=raw.get("benefit", ""),
        benefit_cost=raw.get("benefit_cost", ""),
    )


@dataclass(frozen=True, slots=True)
class CaseGraph:
    """A case plus the hypotheses the table may hold about it."""

    case: Case
    hypotheses: tuple[Hypothesis, ...]
    source_case: str = ""

    def families(self) -> set[str]:
        return {hypothesis.family for hypothesis in self.hypotheses}

    def validate(self) -> None:
        """A mystery with one explanation is a corridor, not a case."""
        self.case.validate()
        if len(self.hypotheses) < 2:
            raise InvestigationError("a case graph needs at least two hypotheses")
        if "mundane" not in self.families():
            raise InvestigationError("no mundane hypothesis: an anomaly must have an ordinary reading")
        if "anomalous" not in self.families():
            raise InvestigationError("no anomalous hypothesis: the anomaly must be statable")
        ids = [hypothesis.id for hypothesis in self.hypotheses]
        if len(set(ids)) != len(ids):
            raise InvestigationError("duplicate hypothesis id")


def load_case_graph(path: str | Path) -> CaseGraph:
    """Load and validate a case graph. Malformed data raises; it never resolves as a miss."""
    raw = json.loads(Path(path).read_text(encoding="utf-8"))
    if raw.get("format") != CASE_GRAPH_FORMAT:
        raise InvestigationError(f"not a {CASE_GRAPH_FORMAT} file: {raw.get('format')!r}")
    graph = CaseGraph(
        case=Case(
            id=raw.get("case_id", ""),
            scenes=tuple(
                Scene(
                    id=scene_raw["id"],
                    title=scene_raw.get("title", scene_raw["id"]),
                    clues=tuple(_clue(clue, scene_raw["id"]) for clue in scene_raw.get("clues", ())),
                )
                for scene_raw in raw.get("scenes", ())
            ),
        ),
        hypotheses=tuple(
            Hypothesis(id=h["id"], statement=h.get("statement", ""),
                       family=h.get("family", "unclassified"))
            for h in raw.get("hypotheses", ())
        ),
        source_case=raw.get("source_case", ""),
    )
    graph.validate()
    return graph
