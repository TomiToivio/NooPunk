"""Deterministic noncanonical NoöPunk RPG playtest (#516, #482, #461).

Uses approved prototype kernel; adds no strategic turns or new rules.
Run: python -m strategy_game.rpg.playtest
"""
from __future__ import annotations

import json
from pathlib import Path
from tempfile import TemporaryDirectory

from .investigation import Investigation, InvestigationError

# GM-chosen difficulties are illustration inputs, not newly approved mechanics.
TRIALS = (
    ("witness_confidentiality", ("interview", "protect", "report"), "agent_1", "COG", 1, 516),
    ("device_provenance", ("inspect", "preserve", "withhold"), "agent_2", "INT", 1, 482),
    ("psi_test", ("interview", "disclose", "report"), "agent_3", "WIL", 2, 461),
)


def run_trials() -> dict:
    results = []
    for name, choices, actor, skill, difficulty, seed in TRIALS:
        case = Investigation()
        case.party(["leader", "agent_1", "agent_2", "agent_3", "agent_4"])
        case.choose(choices[0])
        roll = case.attempt(actor, skill, difficulty, seed)
        for choice in choices[1:]:
            case.choose(choice)
        if not case.finished:
            raise InvestigationError(f"incomplete playtest: {name}")
        with TemporaryDirectory() as dirname:
            path = Path(dirname) / "case.json"
            case.save(path)
            if Investigation.load(path).to_dict() != case.to_dict():
                raise InvestigationError(f"non-reproducible save: {name}")
        results.append({
            "name": name,
            "choices": list(case.choices),
            "participants": list(case.participants),
            "check": roll,
            "evidence": list(case.evidence),
            "events": list(case.events),
            "saved_and_reloaded": True,
        })
    return {"status": "passed", "noncanonical": True, "trials": results}


def main() -> int:
    print(json.dumps(run_trials(), indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
