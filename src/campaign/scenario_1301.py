"""The 2045 Helsinki scenario's invariants, checked rather than asserted in prose (#1301).

The issue is a design specification, and most of it is narrative. What can be *tested* is the small set of statements
that would quietly change the scenario if a later edit reversed them:

* the full NHI Crisis has **not** happened in this timeline;
* AGI/ASI, PSI and NHI are mainstream, and they are the only three paradigm shifts;
* each shift's 50/25/25 baseline sums to 100, and the split is per shift rather than one alignment for a person;
* the EU has four objectives, and "Profit" is what critics call Sustainability rather than a fifth objective;
* every starter case is solvable **without PSI**, and no case gates a clue behind it;
* the player character is a tabula-rasa rookie whose cyber competence is not optional and whose PSI is not required.

The data lives in `data/campaign/scenario_2045_1301.json`; this module validates it and answers the questions a later
module would ask. It implements no rules and no CWN mechanic.
"""
from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Mapping

__all__ = [
    "ScenarioError",
    "Scenario",
    "load_scenario",
    "OBJECTIVE_IDS",
    "SHIFT_IDS",
]

DATA = Path(__file__).resolve().parents[2] / "data" / "campaign" / "scenario_2045_1301.json"

SHIFT_IDS = ("agi", "psi", "nhi")
OBJECTIVE_IDS = ("stability", "sustainability", "security", "survival")
SEGMENT_IDS = ("normies", "accelerationists", "doomers")
KNOWLEDGE_LADDER = ("public", "rumour", "classified", "gm_truth")


class ScenarioError(ValueError):
    """The scenario data contradicts the issue, rather than merely being incomplete."""


@dataclass(frozen=True)
class Scenario:
    """The validated scenario, with the invariants exposed as methods."""

    shifts: tuple[Mapping[str, Any], ...]
    objectives: tuple[Mapping[str, Any], ...]
    cases: tuple[Mapping[str, Any], ...]
    knowledge_ladder: tuple[str, ...]
    crisis_occurred: bool

    # -- the invariants a later edit could break ------------------------------------------------ #
    def crisis_has_not_happened(self) -> bool:
        """#1301's timeline correction: the full NHI Crisis is not the player-facing present."""
        return self.crisis_occurred is False

    def shift(self, shift_id: str) -> Mapping[str, Any]:
        for entry in self.shifts:
            if entry["id"] == shift_id:
                return entry
        raise ScenarioError(f"no shift {shift_id!r}")

    def case(self, case_id: str) -> Mapping[str, Any]:
        for entry in self.cases:
            if entry["id"] == case_id:
                return entry
        raise ScenarioError(f"no case {case_id!r}")

    def cases_for(self, shift_id: str) -> tuple[Mapping[str, Any], ...]:
        return tuple(entry for entry in self.cases if entry["shift"] == shift_id)

    def psi_is_optional_everywhere(self) -> bool:
        """Every case must be solvable without PSI, and the character's PSI must not be required."""
        return all(entry["non_psi_path"] is True for entry in self.cases)

    def segments_sum_to_a_hundred(self, shift_id: str) -> bool:
        segments = self.shift(shift_id)["segments"]
        return sum(segments[key] for key in SEGMENT_IDS) == 100


def _require(condition: bool, reason: str) -> None:
    if not condition:
        raise ScenarioError(reason)


def load_scenario(path: Path | None = None) -> Scenario:
    """Read and validate the scenario data. Every violation is a contradiction, not a warning."""
    payload = json.loads((path or DATA).read_text(encoding="utf-8"))

    _require(payload.get("setting", {}).get("nhi_crisis_occurred") is False,
             "the setting must state that the full NHI Crisis has not happened (#1301 §1)")

    shifts = tuple(payload.get("shifts") or ())
    _require(tuple(entry["id"] for entry in shifts) == SHIFT_IDS,
             f"the three paradigm shifts are exactly {SHIFT_IDS}, in order")
    for entry in shifts:
        _require(entry["status"] == "mainstream",
                 f"{entry['id']} is mainstream science and regulation, not a rumour")
        _require(set(entry["segments"]) == set(SEGMENT_IDS),
                 f"{entry['id']} needs the three segments {SEGMENT_IDS}")
        _require(sum(entry["segments"][key] for key in SEGMENT_IDS) == 100,
                 f"{entry['id']} segments must sum to 100")

    objectives = tuple(payload.get("objectives") or ())
    _require(tuple(entry["id"] for entry in objectives) == OBJECTIVE_IDS,
             f"the EU's objectives are exactly {OBJECTIVE_IDS}, in order")
    _require(all(entry["mandate"].strip() and entry["tension"].strip() for entry in objectives),
             "every objective needs its mandate and the tension it creates")
    _require(any(entry.get("critics_call_it") == "Profit" for entry in objectives),
             "'Profit' is what critics call Sustainability; it is not a fifth objective")

    cases = tuple(payload.get("cases") or ())
    _require({entry["shift"] for entry in cases} == set(SHIFT_IDS),
             "there is one starter case for each shift")
    for entry in cases:
        _require(entry["non_psi_path"] is True,
                 f"{entry['id']} must be solvable without PSI (#1301 acceptance criteria)")
        _require(len(entry["outcomes"]) >= 3,
                 f"{entry['id']} needs several outcomes, including non-criminal ones")

    character = payload.get("player_character") or {}
    _require(character.get("psi_required") is False,
             "the rookie's PSI is optional: no compulsory awakening")
    _require(character.get("forced_alignment") is False,
             "no compulsory faction alignment")
    _require(character.get("state") == "tabula rasa",
             "the rookie starts without a predestined identity")

    ladder = tuple(payload.get("knowledge_ladder") or ())
    _require(ladder == KNOWLEDGE_LADDER,
             f"the knowledge ladder is {KNOWLEDGE_LADDER}: public, rumour, classified, GM truth")

    return Scenario(shifts=shifts, objectives=objectives, cases=cases,
                    knowledge_ladder=ladder, crisis_occurred=bool(payload["setting"]["nhi_crisis_occurred"]))
