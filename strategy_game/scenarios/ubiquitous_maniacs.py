"""Original Ubiquitous Maniacs two-day scenario for the current NoöPunk RPG.

This is a new scenario adapter, not the legacy standalone game's rules or code.
No television transcripts or third-party scripts are bundled.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from random import Random
from typing import Any

from strategy_game.rpg.fate import Action, Character
from strategy_game.rpg.scene import check
from strategy_game.rpg.skills import INDIVIDUAL_SKILL_NAMES


class ScenarioError(ValueError):
    """Invalid choice, saved state or RPG operation."""


# All prose below is newly authored for this adapter.
SCENES = {
    "arrival": {
        "day": 1,
        "text": "The UFAB clinic offers treatment in exchange for access to memories. A printer keeps producing consent forms for patients who have not arrived.",
        "choices": {"read_form": "reception", "ask_questions": "reception"},
    },
    "reception": {
        "day": 1,
        "text": "Elin Dahl opens a sealed door. Behind it the test chamber is occupied, although the attendance ledger is blank.",
        "choices": {"enter_chamber": "test", "inspect_ledger": "test"},
    },
    "test": {
        "day": 1,
        "text": "A third trace appears on the monitoring display. Staff insist the machine has only two sensors.",
        "choices": {"retain_record": "night", "report_anomaly": "night"},
    },
    "night": {
        "day": 1,
        "text": "The first session ends. A dream transcript prints before anyone enters the dream.",
        "choices": {"continue": "dream"},
    },
    "dream": {
        "day": 2,
        "text": "The participant awakes inside a fabricated police inquiry. Inconsistent memories have been filed as evidence.",
        "choices": {"follow_clue": "conclusion", "confront_simulation": "conclusion"},
    },
    "conclusion": {
        "day": 2,
        "text": "An independent witness can confirm only one thing: the clinic's records now disagree with its own machines.",
        "choices": {},
    },
}


def cast() -> dict[str, Character]:
    """Character sheets use the current six-skill RPG vocabulary."""
    return {
        "romppainen": Character("romppainen", "Sven-Olof Romppainen", ["Reluctant test participant"], skills={"SAV": 2, "WIL": 1}),
        "ingrid": Character("ingrid", "Ingrid Falk", ["Observant and skeptical"], skills={"COG": 2, "SAV": 1}),
        "dahl": Character("dahl", "Elin Dahl", ["Clinic protocol officer"], skills={"INT": 2, "SAV": 1}),
    }


@dataclass
class UbiquitousManiacs:
    """Bounded narrative session. Current RPG engine owns all dice resolution."""
    stage: str = "arrival"
    decisions: list[str] = field(default_factory=list)
    checks: list[dict[str, Any]] = field(default_factory=list)

    def __post_init__(self) -> None:
        if self.stage not in SCENES:
            raise ScenarioError("unknown scene")

    @property
    def day(self) -> int:
        return SCENES[self.stage]["day"]

    @property
    def finished(self) -> bool:
        return not SCENES[self.stage]["choices"]

    def view(self) -> dict[str, Any]:
        return {"stage": self.stage, "day": self.day, "text": SCENES[self.stage]["text"],
                "choices": tuple(SCENES[self.stage]["choices"]), "finished": self.finished}

    def choose(self, decision: str) -> str:
        choices = SCENES[self.stage]["choices"]
        if decision not in choices:
            raise ScenarioError("unavailable choice")
        self.stage = choices[decision]
        self.decisions.append(decision)
        return self.stage

    def attempt(self, actor_id: str, skill: str, difficulty: int, seed: int) -> dict[str, Any]:
        """GM-approved optional overcome check; it never dictates the plot outcome."""
        if self.finished or actor_id not in cast() or skill not in INDIVIDUAL_SKILL_NAMES:
            raise ScenarioError("invalid RPG attempt")
        if type(difficulty) is not int or type(seed) is not int:
            raise ScenarioError("difficulty and seed must be integers")
        outcome = check(cast()[actor_id], Action.OVERCOME, skill, difficulty,
                        rng=Random(seed)).resolution
        event = {"stage": self.stage, "actor": actor_id, "skill": skill,
                 "difficulty": difficulty, "seed": seed, "dice": list(outcome.dice),
                 "total": outcome.total, "outcome": outcome.outcome.value}
        self.checks.append(event)
        return event

    def to_dict(self) -> dict[str, Any]:
        return {"schema": 1, "stage": self.stage, "decisions": list(self.decisions),
                "checks": [dict(x) for x in self.checks]}

    @classmethod
    def from_dict(cls, payload: dict[str, Any]) -> "UbiquitousManiacs":
        if not isinstance(payload, dict) or set(payload) != {"schema", "stage", "decisions", "checks"}:
            raise ScenarioError("invalid save structure")
        if payload["schema"] != 1 or not isinstance(payload["decisions"], list) or not isinstance(payload["checks"], list):
            raise ScenarioError("invalid save schema")
        session = cls()
        pending = list(payload["checks"])
        for decision in payload["decisions"]:
            if not isinstance(decision, str):
                raise ScenarioError("invalid saved choice")
            while pending and pending[0].get("stage") == session.stage:
                event = pending.pop(0)
                if not isinstance(event, dict) or set(event) != {"stage", "actor", "skill", "difficulty", "seed", "dice", "total", "outcome"}:
                    raise ScenarioError("invalid saved check")
                if session.attempt(event["actor"], event["skill"], event["difficulty"], event["seed"]) != event:
                    raise ScenarioError("saved Fate roll failed replay")
            session.choose(decision)
        while pending and pending[0].get("stage") == session.stage:
            event = pending.pop(0)
            if not isinstance(event, dict) or set(event) != {"stage", "actor", "skill", "difficulty", "seed", "dice", "total", "outcome"}:
                raise ScenarioError("invalid saved check")
            if session.attempt(event["actor"], event["skill"], event["difficulty"], event["seed"]) != event:
                raise ScenarioError("saved Fate roll failed replay")
        if pending or session.stage != payload["stage"]:
            raise ScenarioError("inconsistent scene/check history")
        return session


def demo(seed: int = 42) -> dict[str, Any]:
    session = UbiquitousManiacs()
    first_check = session.attempt("romppainen", "SAV", 1, seed)
    while not session.finished:
        session.choose(next(iter(session.view()["choices"])))
    return {"scenario": "ubiquitous_maniacs", "completed": session.finished,
            "day": session.day, "decisions": list(session.decisions),
            "first_check": first_check, "replay_valid": UbiquitousManiacs.from_dict(session.to_dict()).finished}


if __name__ == "__main__":
    import json
    print(json.dumps(demo(), indent=2))
