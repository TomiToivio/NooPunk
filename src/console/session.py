"""A playable case session over the canonical investigation rules.

State is deliberately small and versioned: scene, visited scenes, discovered clues, the player's
theory with the evidence attached to it, the turn counter and the dice generator's exact position.
That set is what makes a save file portable between the console, a future Evennia adapter and a
scripted test, and it is why `to_dict()` never contains engine objects.

Two invariants are enforced here rather than documented and hoped for:

* **The session never decides the truth of a theory.** `conclude()` records the player's answer and
  the evidence they attached; no method compares a theory to a hidden solution, because there is no
  hidden solution field to compare against.
* **A save that cannot be resumed is refused.** An unknown `state_version`, a scene that is not in
  the case, or a clue that is not in the case raises instead of loading a half-valid game.
"""
from __future__ import annotations

import json
import random
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from rules.investigation import (
    CaseGraph,
    Clue,
    InvestigationError,
    Investigator,
    Stance,
    discover,
)

STATE_VERSION = 1

#: Skills the case graph may demand; a session refuses to start with an empty sheet, because an
#: investigator with no competencies can enter every scene and leave none of them.
REQUIRED_NOTE = "an investigator needs at least one competency"

#: How much evidence a conclusion needs before the console calls it "supported" in its own summary.
#: This is a presentation threshold for the *player's* summary line, not a verdict on the theory.
EVIDENCE_FOR_SUMMARY = 2


class SessionError(RuntimeError):
    """The session cannot continue: bad command, bad save, or a case that does not fit."""


def _to_tuple(value: Any) -> Any:
    """JSON gives lists; ``random.setstate`` wants tuples."""
    if isinstance(value, list):
        return tuple(_to_tuple(item) for item in value)
    return value


@dataclass
class CaseSession:
    """One player, one case, one deterministic stream of dice."""

    graph: CaseGraph
    investigator: Investigator
    scene_id: str
    seed: int = 0
    visited: list[str] = field(default_factory=list)
    discovered: dict[str, str] = field(default_factory=dict)      # clue id -> scene id
    evidence: dict[str, dict[str, str]] = field(default_factory=dict)  # hypothesis -> clue -> stance
    theory_id: str = ""
    turns: int = 1
    concluded: bool = False
    conclusion: dict[str, Any] = field(default_factory=dict)
    events: list[dict[str, Any]] = field(default_factory=list)
    _rng: random.Random | None = field(default=None, repr=False)

    # ------------------------------------------------------------------ #
    # Construction
    # ------------------------------------------------------------------ #

    def __post_init__(self) -> None:
        if not self.investigator.ratings:
            raise SessionError(REQUIRED_NOTE)
        self.graph.validate()
        if self.scene_id not in {scene.id for scene in self.graph.case.scenes}:
            raise SessionError(f"no scene {self.scene_id!r} in this case")
        if self._rng is None:
            self._rng = random.Random(self.seed)
        if not isinstance(self._rng, random.Random):
            raise SessionError("the dice generator must be a random.Random")
        if self.scene_id not in self.visited:
            self.visited.append(self.scene_id)
            self._record("enter", scene=self.scene_id)
            self._look(automatic=True)

    @classmethod
    def start(cls, graph: CaseGraph, investigator: Investigator, *, seed: int = 0) -> CaseSession:
        return cls(graph=graph, investigator=investigator, scene_id=graph.case.scenes[0].id,
                   seed=seed)

    # ------------------------------------------------------------------ #
    # Queries used by the console
    # ------------------------------------------------------------------ #

    def scene(self):
        return self.graph.case.scene(self.scene_id)

    def hypothesis(self, hypothesis_id: str):
        for hypothesis in self.graph.hypotheses:
            if hypothesis.id == hypothesis_id:
                return hypothesis
        raise SessionError(f"no hypothesis {hypothesis_id!r} in this case")

    def theory(self):
        return self.hypothesis(self.theory_id) if self.theory_id else None

    def clue(self, clue_id: str) -> Clue:
        for scene in self.graph.case.scenes:
            for clue in scene.clues:
                if clue.id == clue_id:
                    return clue
        raise SessionError(f"no clue {clue_id!r} in this case")

    def exits(self) -> tuple[str, ...]:
        """Scenes a discovered lead points at, deduplicated in case order."""
        order = {scene.id: index for index, scene in enumerate(self.graph.case.scenes)}
        targets = {
            target
            for clue_id in self.discovered
            for target in self.clue(clue_id).leads_to
        }
        return tuple(sorted(targets, key=lambda scene_id: order.get(scene_id, 0)))

    def open_clues(self) -> tuple[str, ...]:
        """Clues in the current scene this investigator has not yet taken."""
        return tuple(
            clue.id for clue in self.scene().clues if clue.id not in self.discovered
        )

    # ------------------------------------------------------------------ #
    # Actions
    # ------------------------------------------------------------------ #

    def _record(self, kind: str, **payload: Any) -> None:
        self.events.append({"turn": self.turns, "kind": kind, **payload})

    def _look(self, *, automatic: bool = False,
              declared: tuple[str, ...] = ()) -> list[str]:
        """Grant what the rules say is simply seen here. No roll, no difficulty.

        ``declared`` is the inquiry the player has announced. An automatic look declares nothing,
        because a clue that needs a search must not arrive just for walking in.
        """
        scene = self.scene()
        result = discover(self.graph.case, scene.id, self.investigator, inquiry=declared)
        granted: list[str] = []
        for clue in result.clues:
            if clue.id in self.discovered:
                continue
            self.discovered[clue.id] = scene.id
            granted.append(clue.id)
        if granted:
            self._record("discover", scene=scene.id, clues=granted, automatic=automatic,
                         granted_by=result.granted_by)
        return granted

    def look(self) -> dict[str, Any]:
        """Look around again, declaring a search for anything that needs one."""
        self.turns += 1
        granted = self._look(declared=("search", "interview", "records", "observe"))
        return {
            "scene": self.scene().id,
            "title": self.scene().title,
            "clues": [self.clue(clue_id) for clue_id in self.open_clues()],
            "granted": granted,
            "withheld": [
                self.clue(clue_id) for clue_id in
                discover(self.graph.case, self.scene_id, self.investigator).withheld_ids
                if clue_id not in self.discovered
            ],
        }

    def travel(self, scene_id: str) -> dict[str, Any]:
        if self.concluded:
            raise SessionError("the case is concluded; start a new session to keep playing")
        if scene_id not in {scene.id for scene in self.graph.case.scenes}:
            raise SessionError(f"no scene {scene_id!r} in this case")
        allowed = set(self.exits()) | {self.scene_id}
        if scene_id not in allowed:
            raise SessionError(
                f"no discovered lead to {scene_id!r}; leads now: {', '.join(self.exits()) or 'none'}"
            )
        self.turns += 1
        self.scene_id = scene_id
        if scene_id not in self.visited:
            self.visited.append(scene_id)
        self._record("travel", scene=scene_id)
        granted = self._look(automatic=True)
        return {"scene": scene_id, "title": self.scene().title, "granted": granted}

    def take(self, clue_id: str) -> Clue:
        """Explicitly examine a clue in the current scene.

        Discovery is not a roll, so this never fails on the dice; it fails only when the clue is
        not here, or when the investigator is not competent to read it.
        """
        clue = self.clue(clue_id)
        if clue.scene_id != self.scene_id:
            raise SessionError(f"clue {clue_id!r} is not in {self.scene_id!r}")
        if clue_id in self.discovered:
            self.turns += 1
            self._record("examine", clue=clue_id, already_known=True)
            return clue
        if not self.investigator.is_competent(clue.competency):
            raise SessionError(
                f"{self.investigator.name} has no {clue.competency!r} competency; a scene mate "
                "with it can read this"
            )
        self.turns += 1
        self.discovered[clue_id] = self.scene_id
        self._record("examine", clue=clue_id, already_known=False)
        return clue

    def attach(self, hypothesis_id: str, clue_id: str, stance: str) -> dict[str, Any]:
        """Record how the player reads a clue against one theory. The player, not the program."""
        hypothesis = self.hypothesis(hypothesis_id)
        if clue_id not in self.discovered:
            raise SessionError(f"clue {clue_id!r} has not been found yet")
        try:
            reading = Stance(stance)
        except ValueError as exc:
            raise SessionError(f"stance must be supports, contradicts or neutral: {stance!r}") from exc
        hypothesis.consider(self.clue(clue_id), reading)
        self.evidence.setdefault(hypothesis_id, {})[clue_id] = reading.value
        self.turns += 1
        self._record("attach", hypothesis=hypothesis_id, clue=clue_id, stance=reading.value)
        return {"hypothesis": hypothesis_id, "clue": clue_id, "stance": reading.value}

    def choose_theory(self, hypothesis_id: str) -> str:
        self.hypothesis(hypothesis_id)
        self.theory_id = hypothesis_id
        self.turns += 1
        self._record("theory", hypothesis=hypothesis_id)
        return hypothesis_id

    def risk(self, difficulty: int, skill: str = "") -> dict[str, Any]:
        """A CWN ``2d6`` check under pressure, plus the character's rank when they hold it.

        The die decides danger, time and quality, never whether a clue exists -- that is what makes
        this a separate action from discovery.
        """
        if difficulty < 2:
            raise SessionError("a CWN check difficulty is 8, 10 or 12; below 2 is not a check")
        if skill and not self.investigator.is_competent(skill):
            raise SessionError(f"{self.investigator.name} has no {skill!r} competency")
        assert self._rng is not None
        dice = (self._rng.randint(1, 6), self._rng.randint(1, 6))
        rank = self.investigator.ratings.get(skill, 0) if skill else 0
        total = sum(dice) + rank
        self.turns += 1
        result = {"dice": dice, "rank": rank, "total": total, "difficulty": difficulty,
                  "success": total >= difficulty, "skill": skill}
        self._record("risk", **result)
        return result

    def conclude(self, hypothesis_id: str, note: str = "") -> dict[str, Any]:
        """The player's answer. The program records it; it does not grade it."""
        hypothesis = self.hypothesis(hypothesis_id)
        readings = self.evidence.get(hypothesis_id, {})
        supports = sum(1 for stance in readings.values() if stance == "supports")
        contradicts = sum(1 for stance in readings.values() if stance == "contradicts")
        self.concluded = True
        self.turns += 1
        self.conclusion = {
            "hypothesis": hypothesis_id,
            "family": hypothesis.family,
            "statement": hypothesis.statement,
            "supports": supports,
            "contradicts": contradicts,
            "unread": len(self.discovered) - len(readings),
            "note": note,
            "verdict": "recorded by the player; the console does not decide the truth of the theory",
            "case_solved_by_program": False,
        }
        self._record("conclude", hypothesis=hypothesis_id)
        return self.conclusion

    # ------------------------------------------------------------------ #
    # Persistence
    # ------------------------------------------------------------------ #

    def to_dict(self) -> dict[str, Any]:
        return {
            "state_version": STATE_VERSION,
            "case_id": self.graph.case.id,
            "investigator": {"name": self.investigator.name,
                             "ratings": dict(self.investigator.ratings)},
            "scene": self.scene_id,
            "seed": self.seed,
            "visited": list(self.visited),
            "discovered": dict(self.discovered),
            "evidence": {key: dict(value) for key, value in self.evidence.items()},
            "theory": self.theory_id,
            "turns": self.turns,
            "concluded": self.concluded,
            "conclusion": dict(self.conclusion),
            "events": list(self.events),
            "rng_state": list(self._rng.getstate()) if self._rng else [],
        }

    def save(self, path: str | Path) -> Path:
        target = Path(path)
        target.write_text(json.dumps(self.to_dict(), indent=2) + "\n", encoding="utf-8")
        return target

    @classmethod
    def from_dict(cls, graph: CaseGraph, data: dict[str, Any]) -> CaseSession:
        version = data.get("state_version")
        if version != STATE_VERSION:
            raise SessionError(
                f"save state_version {version!r} is not {STATE_VERSION!r}; this console will not "
                "guess how to migrate it")
        if data.get("case_id") and graph.case.id and data["case_id"] != graph.case.id:
            raise SessionError(
                f"save is for case {data['case_id']!r}, this case is {graph.case.id!r}")
        investigator = Investigator(
            name=data["investigator"]["name"],
            ratings={key: int(value) for key, value in data["investigator"]["ratings"].items()})
        rng = random.Random(data.get("seed", 0))
        if data.get("rng_state"):
            rng.setstate(_to_tuple(data["rng_state"]))
        session = cls(
            graph=graph,
            investigator=investigator,
            scene_id=data["scene"],
            seed=int(data.get("seed", 0)),
            visited=list(data.get("visited", [])),
            discovered={key: value for key, value in data.get("discovered", {}).items()},
            evidence={key: dict(value) for key, value in data.get("evidence", {}).items()},
            theory_id=data.get("theory", ""),
            turns=int(data.get("turns", 1)),
            concluded=bool(data.get("concluded", False)),
            conclusion=dict(data.get("conclusion", {})),
            events=list(data.get("events", [])),
            _rng=rng,
        )
        return session


def save_session(session: CaseSession, path: str | Path) -> Path:
    return session.save(path)


def load_session(graph: CaseGraph, path: str | Path) -> CaseSession:
    raw = Path(path).read_text(encoding="utf-8")
    try:
        data = json.loads(raw)
    except json.JSONDecodeError as exc:
        raise SessionError(f"{path} is not a save file: {exc}") from exc
    try:
        return CaseSession.from_dict(graph, data)
    except KeyError as exc:
        raise SessionError(f"{path} is missing {exc}") from exc
    except InvestigationError as exc:
        raise SessionError(f"{path} does not fit this case: {exc}") from exc
