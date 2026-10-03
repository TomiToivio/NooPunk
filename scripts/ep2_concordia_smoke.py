#!/usr/bin/env python3
"""Smoke-test the issue #60 EP2 homebrew boundary without an LLM."""

from __future__ import annotations

from pathlib import Path
import json
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from concordia_runtime.ep2_adapter import resolve_ep2_action
from eclipse_phase_homebrew import EP2Character, EP2PoolState, PoolKind


def main() -> int:
    character = EP2Character(
        name="NoöPunk EP2 prototype",
        skills={"Infosec": 65, "Perceive": 55, "Persuade": 45},
        aptitudes={"COG": 20, "INT": 20, "SAV": 15},
        morph="prototype morph",
    )
    pools = EP2PoolState(maximum={
        PoolKind.INSIGHT: 2, PoolKind.MOXIE: 1,
        PoolKind.VIGOR: 1, PoolKind.FLEX: 1,
    })
    result = resolve_ep2_action(
        character=character,
        action={"skill": "Infosec", "aptitude": "COG", "modifier": 0},
        pools=pools,
        roll=42,
    )
    print(json.dumps(result, indent=2, default=str))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
