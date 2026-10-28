#!/usr/bin/env python3
"""The paradigm-shock case (#699): a falsification test for D46–D48, not an illustration.

A character holds a belief and meets evidence that contradicts it. Both branches are played to a
conclusion, headless and deterministically, and the journal is printed. Run it twice and the output is
identical — the case has no dice, because D48 says a conviction may not turn on one.

Uses the merged model in `src/rules/mental_load.py` (#698) rather than a private one, so the case
tests the implementation the repository actually has.

    python tools/paradigm_shock_case.py [--json OUT]
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from src.rules.mental_load import CharacterMind, ParadigmShock

#: The case. Deliberately the register's own example: a ward whose files are written in the future
#: tense. Nothing here is canon; it is a test fixture that reads like a scene.
CASE = ParadigmShock(
    id="case-699-ward",
    claim="Saint Aurélien's is a psychiatric hospital: it treats people.",
    contradicts="Saint Aurélien's is a psychiatric hospital: it treats people.",
    source=(
        "The duty files for the last four admissions are written in the future tense, and one of them "
        "describes what the character will do tomorrow."
    ),
)


def play(accept: bool) -> dict[str, Any]:
    """One branch, played to its conclusion. Deterministic by construction."""
    mind = CharacterMind()
    choice = mind.present(CASE)
    state = mind.apply_choice(choice, accept=accept)
    return {
        "branch": "accept" if accept else "hold",
        "state_before": "received",
        "state_after": state.value,
        "condition": (choice.accept if accept else choice.hold).id,
        "constrains": (choice.accept if accept else choice.hold).constrains,
        "events": [
            f"layer 1 observable_event: {CASE.source}",
            "layer 2 acute_response: the claim is contradicted",
            f"layer 3 persistent_condition: {(choice.accept if accept else choice.hold).id}",
            f"layer 4 worldview_state: received -> {state.value}",
        ],
    }


def verdict(accept: dict[str, Any], hold: dict[str, Any]) -> dict[str, Any]:
    """What the mechanism actually produced, stated as findings rather than as a claim of success."""
    return {
        "d48_holds": accept["state_after"] != hold["state_after"],
        "d48_note": (
            "The branches end in different world-view states with different conditions, and the only "
            "way to reach either is an explicit accept/hold decision. No roll exists that could have "
            "chosen between them."
        ),
        "d46_exercised": False,
        "d46_note": (
            "A condition is *produced* (layer 3) and recorded, but no condition had to carry a scene: "
            "the case runs in the journal, not over play. It therefore does not yet test whether "
            "conditions can carry drama, and it must not be cited as evidence that they can."
        ),
        "d49_triggered": False,
        "d49_note": (
            "The trigger for EP-grade stress is a written case that conditions demonstrably cannot "
            "carry. None was written, so the deferral stands."
        ),
        "next": (
            "A second case in which a condition — not a belief — carries the scene: a lasting "
            "condition whose only exit is a WWN major project, across three scenes, with the player "
            "visibly choosing whether to spend them on it."
        ),
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--json", type=Path, default=None)
    args = parser.parse_args(argv)

    accept, hold = play(True), play(False)
    result = {
        "case": {"claim": CASE.claim, "source": CASE.source},
        "branches": {"accept": accept, "hold": hold},
        "diverged": accept["state_after"] != hold["state_after"],
        "conditions_differ": accept["condition"] != hold["condition"],
        "verdict": verdict(accept, hold),
    }

    print("Paradigm-shock case (#699)")
    print("=" * 62)
    print(f"claim:    {result['case']['claim']}")
    print(f"evidence: {result['case']['source']}")
    for name in ("accept", "hold"):
        branch = result["branches"][name]
        print(f"\n-- branch {name}: {branch['state_before']} -> {branch['state_after']}")
        print(f"   condition: {branch['condition']}")
        print(f"   constrains: {branch['constrains']}")
        for event in branch["events"]:
            print(f"   {event}")
    print("\nverdict")
    print(f"  diverged: {result['diverged']} | conditions differ: {result['conditions_differ']}")
    for key in ("d48", "d46", "d49"):
        print(f"  {key.upper()}: {result['verdict'][key + ('_holds' if key == 'd48' else '_exercised' if key == 'd46' else '_triggered')]}"
              f" — {result['verdict'][key + '_note']}")
    print(f"  next: {result['verdict']['next']}")

    if args.json:
        args.json.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
