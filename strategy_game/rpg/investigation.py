"""Issue #502: small, persistent, GM-authored RPG investigation, with no strategy rules.

Fiction and choices are deliberately *illustrative*, not setting canon. The faction leader
is the PC from the first scene, and four agents are selectable scene participants.
The approved Fate engine remains responsible for any requested dice resolution;
this module does not invent difficulties, economics, missions, or political transitions.
"""
from __future__ import annotations

from dataclasses import dataclass, field
import json
from pathlib import Path
from random import Random
from typing import Any

from .fate import Action, Character
from .roster import default_seats
from .scene import check


class InvestigationError(ValueError):
    """Illegal narrative transition or malformed save data."""


# A bounded, noncanonical demo scenario; player choice, not dice, selects each consequence.
# The author/GM may replace this scenario without changing the session API.
STAGES = {
    "briefing": {
        "prompt": "A witness reports strange signals near a secured research site.",
        "choices": {"interview": "witness", "inspect": "site"},
    },
    "witness": {
        "prompt": "The witness offers a recording. Keep the source confidential?",
        "choices": {"protect": "decision", "disclose": "decision"},
    },
    "site": {
        "prompt": "A device holds an unexplained log. Preserve the original?",
        "choices": {"preserve": "decision", "copy": "decision"},
    },
    "decision": {
        "prompt": "How should your faction handle the evidence?",
        "choices": {"report": "complete", "withhold": "complete"},
    },
    "complete": {"prompt": "The case is closed. Consequences remain on record.", "choices": {}},
}


def demo_party() -> dict[str, Character]:
    """Placeholder sheets using only #482's individual skill vocabulary."""
    return {
        "leader": Character("leader", "Faction Leader", ["Responsible for the faction"], skills={"SAV": 2}),
        "agent_1": Character("agent_1", "Investigator", ["Patient observer"], skills={"COG": 2}),
        "agent_2": Character("agent_2", "Cyber Specialist", ["Local-access specialist"], skills={"INT": 2}),
        "agent_3": Character("agent_3", "PSI Specialist", ["Unusual impressions"], skills={"WIL": 2},
                             natural_psi=True, psi_abilities=["impression"]),
        "agent_4": Character("agent_4", "Field Agent", ["Keeps the party safe"], skills={"REF": 2}),
    }


@dataclass
class Investigation:
    """Persistent narrative state; no resources, scores, or faction turn rules."""

    case_id: str = "example-signal"
    stage: str = "briefing"
    participants: list[str] = field(default_factory=lambda: ["leader"])
    choices: list[str] = field(default_factory=list)
    evidence: list[str] = field(default_factory=list)
    events: list[dict[str, Any]] = field(default_factory=list)
    faction_id: str = "player-faction"
    schema_version: int = 1

    def __post_init__(self) -> None:
        if self.stage not in STAGES or not self.case_id or not self.faction_id:
            raise InvestigationError("invalid case state")
        roster = set(demo_party())
        if not self.participants or len(set(self.participants)) != len(self.participants) or any(
            actor not in roster for actor in self.participants
        ):
            raise InvestigationError("participants must be distinct roster characters")
        if self.schema_version != 1:
            raise InvestigationError("unsupported case schema")

    @property
    def finished(self) -> bool:
        return self.stage == "complete"

    def available(self) -> tuple[str, ...]:
        return tuple(STAGES[self.stage]["choices"])

    def party(self, actors: list[str]) -> None:
        """Pick scene actors from the existing leader-plus-four-agent roster."""
        roster = demo_party()
        default_seats("leader", tuple(f"agent_{i}" for i in range(1, 5)))
        if not actors or len(set(actors)) != len(actors) or any(a not in roster for a in actors):
            raise InvestigationError("select distinct characters from the faction roster")
        self.participants = list(actors)

    def choose(self, option: str) -> None:
        """Record a narrative decision and its future-facing event, without scoring it."""
        if option not in STAGES[self.stage]["choices"]:
            raise InvestigationError("choice unavailable in this scene")
        old = self.stage
        self.stage = STAGES[old]["choices"][option]
        self.choices.append(option)
        if option in ("protect", "disclose", "preserve", "copy"):
            self.evidence.append(option)
        self.events.append({
            "kind": "investigation_choice", "faction_id": self.faction_id,
            "case_id": self.case_id, "stage": old, "choice": option,
            "actor_ids": list(self.participants),
        })

    def attempt(self, actor_id: str, skill: str, difficulty: int, seed: int) -> dict[str, Any]:
        """Optional GM-permitted Fate overcome check; no automatic narrative transition.

        Difficulty and permission to attempt are table decisions, not newly invented rules.
        A roll only becomes part of the record after the participant/skill checks pass.
        """
        from .skills import INDIVIDUAL_SKILLS
        if self.finished or actor_id not in self.participants:
            raise InvestigationError("only an active participant can act in an open case")
        if skill not in INDIVIDUAL_SKILLS:
            raise InvestigationError("use an approved individual RPG skill")
        actor = demo_party()[actor_id]
        outcome = check(actor, Action.OVERCOME, skill, difficulty, rng=Random(seed)).resolution
        event = {
            "kind": "rpg_check", "faction_id": self.faction_id,
            "case_id": self.case_id, "stage": self.stage, "actor_id": actor_id,
            "skill": skill, "difficulty": difficulty, "seed": seed,
            "dice": list(outcome.dice), "total": outcome.total,
            "shifts": outcome.shifts, "outcome": outcome.outcome.value,
        }
        self.events.append(event)
        return event

    def to_dict(self) -> dict[str, Any]:
        return {
            "schema_version": self.schema_version, "case_id": self.case_id,
            "faction_id": self.faction_id, "stage": self.stage,
            "participants": list(self.participants), "choices": list(self.choices),
            "evidence": list(self.evidence), "events": list(self.events),
        }

    @classmethod
    def from_dict(cls, payload: dict[str, Any]) -> "Investigation":
        if not isinstance(payload, dict) or set(payload) != {
            "schema_version", "case_id", "faction_id", "stage",
            "participants", "choices", "evidence", "events",
        }:
            raise InvestigationError("invalid save structure")
        if any(not isinstance(payload[k], list) for k in ("participants", "choices", "evidence", "events")):
            raise InvestigationError("invalid save collections")
        instance = cls(**payload)
        # Replay narrative choices to prevent an inconsistent stage or event history.
        replay = cls(case_id=instance.case_id, faction_id=instance.faction_id)
        choices = instance.choices
        for choice in choices:
            if not isinstance(choice, str):
                raise InvestigationError("invalid saved choice")
            replay.choose(choice)
        if replay.stage != instance.stage or replay.evidence != instance.evidence:
            raise InvestigationError("save choices are inconsistent with stage or evidence")
        return instance

    def save(self, path: str | Path) -> None:
        target = Path(path)
        target.parent.mkdir(parents=True, exist_ok=True)
        temporary = target.with_name(target.name + ".tmp")
        temporary.write_text(json.dumps(self.to_dict(), indent=2), encoding="utf-8")
        temporary.replace(target)

    @classmethod
    def load(cls, path: str | Path) -> "Investigation":
        return cls.from_dict(json.loads(Path(path).read_text(encoding="utf-8")))
