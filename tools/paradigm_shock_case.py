#!/usr/bin/env python3
"""The paradigm-shock case (#699): a falsification test for D46–D48, not an illustration.

A character holds a belief and meets evidence that contradicts it. Both branches are played to a
conclusion, headless and deterministically, and the tool prints the journal. Run it twice and the
output is identical — the case has no dice, because D48 says a conviction may not turn on one.

    python tools/paradigm_shock_case.py [--json OUT]
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from src.rules.mental_load import (
    Choice,
    ParadigmShock,
    WorldviewState,
    resolve_shock,
)

#: The case. Deliberately the register's own example: a psychiatric ward whose patients' files are
#: written in the future tense. Nothing here is canon; it is a test fixture that reads like a scene.
CASE = ParadigmShock(
    belief="Saint Aurélien's is a psychiatric hospital: it treats people.",
    evidence=(
        "The duty files for the last four admissions are written in the future tense, and one of them "
        "describes what the character will do tomorrow."
    ),
    choices=(
        Choice(
            id="accept",
            label="Accept the reframe",
            cost="The ward is something else, and the character has been working inside it.",
            resulting_state=WorldviewState.REFRAMED,
        ),
        Choice(
            id="hold",
            label="Hold the belief",
            cost="Denial: one band against Medicine inside the building, until the file is explained.",
            resulting_state=WorldviewState.FRACTURED,
        ),
    ),
)


def play(choice_id: str) -> dict[str, Any]:
    """One branch, played to its conclusion. Deterministic by construction."""
    record = resolve_shock(CASE, choice_id=choice_id)
    return record.as_dict()


def play_both() -> dict[str, Any]:
    accept, hold = play("accept"), play("hold")
    return {
        "case": {"belief": CASE.belief, "evidence": CASE.evidence},
        "branches": {"accept": accept, "hold": hold},
        "diverged": accept["state_after"] != hold["state_after"],
        "costs_differ": accept["cost"] != hold["cost"],
        "verdict": verdict(accept, hold),
    }


def verdict(accept: dict[str, Any], hold: dict[str, Any]) -> dict[str, Any]:
    """What the mechanism actually produced, stated as findings rather than as a claim of success."""
    return {
        "d48_holds": accept["state_after"] != hold["state_after"],
        "d48_note": (
            "The two branches end in different world-view states with different costs, and no roll "
            "exists that could have chosen between them."
        ),
        "d46_exercised": False,
        "d46_note": (
            "This case is carried entirely by layer 4 (world view). No condition was required to hold "
            "a scene together, so the case does NOT test D46 and must not be cited as evidence for "
            "it. It also does not trigger D49, because conditions were never asked to carry more than "
            "they can."
        ),
        "next": (
            "A second case is needed in which a *condition* — not a belief — carries the scene: "
            "e.g. a lasting condition whose only exit is a WWN project, over three scenes, with the "
            "player choosing to spend those scenes on it or not."
        ),
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--json", type=Path, default=None)
    args = parser.parse_args(argv)

    result = play_both()
    print("Paradigm-shock case (#699)")
    print("=" * 60)
    print(f"belief:   {result['case']['belief']}")
    print(f"evidence: {result['case']['evidence']}")
    for name in ("accept", "hold"):
        branch = result["branches"][name]
        print(f"\n-- branch {name}: {branch['chosen']}")
        print(f"   {branch['state_before']} -> {branch['state_after']}")
        print(f"   cost: {branch['cost']}")
        for event in branch["events"]:
            print(f"   {event}")
    print("\nverdict")
    print(f"  diverged: {result['diverged']} | costs differ: {result['costs_differ']}")
    print(f"  D48 holds: {result['verdict']['d48_holds']} — {result['verdict']['d48_note']}")
    print(f"  D46 exercised: {result['verdict']['d46_exercised']} — {result['verdict']['d46_note']}")
    print(f"  next: {result['verdict']['next']}")

    if args.json:
        args.json.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
