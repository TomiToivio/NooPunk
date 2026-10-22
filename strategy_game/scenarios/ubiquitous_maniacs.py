"""The Ubiquitous Maniacs material, unified with the current NoöPunk RPG.

**Status: authored scenario content, not canon.** The frame is canon and nothing more: the
2045 campaign present, the UNSA Helsinki Field Office, the Academy, the post-Crisis network.
The incident, its people and its outcome are fiction written for this scenario.

**What this is.** The Ubiquitous Maniacs corpus — the author's own earlier prototype, imported
as reference material under ``legacy/ubiquitous_maniacs/`` and ``archive/ubiquitous-maniacs-2026-10/``
— describes a two-day scenario at a clinic that trades treatment for access to memory. That
scenario is now playable **on the current RPG engine**, with the current Fate resolver, the
current six-skill vocabulary and the current character model. The corpus's own engine is not
invoked; it is a superseded prototype kept as a reference implementation.

**What is anchored to canon, and why it matters.** The corpus predates this repository's canon
and contradicts it in several places. The migration map
(``archive/ubiquitous-maniacs-2026-10/MIGRATION_MAP.md``) records twelve such conflicts
(C1–C12). Three of them are load-bearing here, and this scenario is built so that it does not
contradict canon:

* **C5 — the institution.** The corpus's setting is *UFAB*, a Nordic psychiatric and
  psychotronic research complex. **UFAB appears in none of this repository's 57 canon rulebook
  files.** Canon has the UNSA (254 mentions), the Academy, Eurodef, the Supo and Ö-Mappi. So
  the scenario is anchored to the **UNSA Helsinki Field Office** and its Academy wing, and the
  corpus's clinic becomes a **scenario-local** facility run under that frame rather than a
  competing institution. It is labelled as such, and it does not claim to be canon.
* **C3 — the name.** The corpus's protagonist is *Emil* Romppainen, a Jungian psychoanalyst.
  Canon's is *Dr. Harri S. Romppainen* ("Dirty Harry"), a veteran of Ö-Mappi. **These are
  different men with the same name**, and the migration map names this as one of the two most
  dangerous rows precisely because it is not obvious. So the scenario uses the **canon**
  Romppainen, and the corpus's persona-phase structure is not smuggled in under his name.
* **C4 — the other collision.** The corpus's *Lotta Kallio* is a person; canon's *Kallio* is a
  **district**. This scenario takes place in neither, and does not use the name at all.

**C2 — the date.** Canon writes future dates as ``20XX`` unless the author says otherwise
(``AGENTS.md`` §6), and the corpus deliberately uses relative chronology. This scenario is
therefore set in the canonical present *without* a year in its prose, and the ``20XX`` frame is
carried by the module's own metadata rather than by the narration.

**The corpus's distinctive contribution, kept.** What the corpus has that the current game did
not is the **memory-as-currency** premise and the **persona-phase** structure of a protagonist
whose professional detachment and compulsive appetite are two faces of one Jungian shadow. The
first is a scenario premise; the second is a playable character trait on the canon Romppainen,
stated as a trait rather than as a rewrite of who he is.
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


#: The canonical frame, in the terms canon uses. No year appears in the prose: `AGENTS.md` §6
#: reserves exact future dates for the author.
FRAME = "UNSA Helsinki Field Office, 20XX"

#: The scenario-local facility. It is NOT canon: UFAB, the corpus's own institution, appears in
#: none of the canon rulebook files, so the clinic is placed under the canon institution as a
#: contracted site rather than as a rival one.
FACILITY = "The UNSA Helsinki Field Office's contracted memory-therapy site, one floor below the operations floor"

# All prose below is newly authored for this adapter.
SCENES = {
    "arrival": {
        "day": 1,
        "text": (
            "The site offers treatment in exchange for access to memory. A printer keeps "
            "producing consent forms for patients who have not arrived. The Field Office has "
            "sent three agents; the site's own clinician has sent a records clerk."
        ),
        "choices": {"read_form": "reception", "ask_questions": "reception"},
    },
    "reception": {
        "day": 1,
        "text": (
            "A sealed door opens onto a test chamber that is occupied, although the attendance "
            "ledger is blank. The clinician on duty is Elin Dahl, and she answers the ledger "
            "question before anyone asks it."
        ),
        "choices": {"enter_chamber": "test", "inspect_ledger": "test"},
    },
    "test": {
        "day": 1,
        "text": (
            "A third trace appears on the monitoring display. The site's own instruments have "
            "two sensors. Romppainen is reading the display the way he reads everything: as "
            "something that will be explained later, by someone else, in a room he will not "
            "be invited to."
        ),
        "choices": {"retain_record": "night", "report_anomaly": "night"},
    },
    "night": {
        "day": 1,
        "text": (
            "The first session ends. A dream transcript prints before anyone enters the dream. "
            "Dahl asks who the third party is, and asks it of the transcript rather than of the "
            "room."
        ),
        "choices": {"continue": "dream"},
    },
    "dream": {
        "day": 2,
        "text": (
            "The participant awakes inside a fabricated police inquiry. Inconsistent memories "
            "have been filed as evidence, and the filing officer's name is on every page. "
            "Someone with standing in this building built a room out of it."
        ),
        "choices": {"follow_clue": "conclusion", "confront_simulation": "conclusion"},
    },
    "conclusion": {
        "day": 2,
        "text": (
            "An independent witness can confirm one thing only: the site's records now disagree "
            "with its own machines, and the disagreement began before the Field Office arrived. "
            "The case is not solved. It is bounded, which is what the Field Office can carry "
            "upstairs."
        ),
        "choices": {},
    },
}


def cast() -> dict[str, Character]:
    """Character sheets use the current six-skill RPG vocabulary.

    The cast is the canon party. Romppainen and Falk are canon characters with canon
    identities; the corpus's *Emil* Romppainen and *Ingrid* Falk are **not** used, because
    canon has different men and women under those names (migration map C3, C4). The site
    clinician is the corpus's Elin Dahl, who is new to this scenario and claims no canon
    status.

    The ratings are **playtest placeholders**, not canon sheets, in the same sense as the
    Kallio case's four agents: the numbers exist so a check has something to resolve against,
    and they are the scenario's, not the rulebook's.
    """
    return {
        "romppainen": Character(
            "romppainen",
            "Dr. Harri Romppainen (Dirty Harry)",
            [
                "Resigned to a quiet post and never once behaved like it",
                "Reads a case the way other people read a room: waiting to be told what it means",
            ],
            skills={"SAV": 2, "WIL": 1},
        ),
        "falk": Character(
            "falk",
            "Laura Falk (Minerva)",
            [
                "Academy newcomer, and reads the site's paperwork better than the site does",
                "Wants the record to hold up somewhere that is not this building",
            ],
            skills={"COG": 2, "SAV": 1},
        ),
        "dahl": Character(
            "dahl",
            "Elin Dahl",
            [
                "Clinic protocol officer who answers questions with protocol",
                "Has filed every anomaly in the same order, which is its own kind of confession",
            ],
            skills={"INT": 2, "SAV": 1},
        ),
    }


@dataclass
class UbiquitousManiacs:
    """Bounded narrative session. The current RPG engine owns all dice resolution."""
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
    def from_dict(cls, payload: dict[str, Any]) -> UbiquitousManiacs:
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
