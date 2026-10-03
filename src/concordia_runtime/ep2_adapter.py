"""Concordia adapter for the isolated Eclipse Phase 2E homebrew rules kernel.

Concordia/LLMs choose intent; deterministic Python resolves the structured test.
"""

from __future__ import annotations

from dataclasses import asdict
from typing import Any, Mapping

from eclipse_phase_homebrew import EP2Character, EP2PoolState, PoolKind, PoolSpend, resolve_test


def resolve_ep2_action(*, character: EP2Character, action: Mapping[str, Any],
                       pools: EP2PoolState | None = None,
                       roll: int | None = None) -> dict[str, Any]:
    """Resolve a structured EP2 test request without letting the LLM roll dice."""
    skill = str(action.get("skill") or "").strip()
    aptitude = str(action.get("aptitude") or "").strip()
    modifier = int(action.get("modifier", 0))

    if skill:
        if skill in character.skills:
            target = int(character.skills[skill])
            defaulted = False
        elif aptitude and aptitude in character.aptitudes:
            target = int(character.aptitudes[aptitude])
            defaulted = True
        else:
            raise ValueError(f"Character lacks skill {skill!r}; provide its linked aptitude to default.")
    elif aptitude:
        if aptitude not in character.aptitudes:
            raise ValueError(f"Unknown aptitude {aptitude!r}.")
        target = int(character.aptitudes[aptitude])
        defaulted = False
    else:
        raise ValueError("Structured EP2 action requires skill or aptitude.")

    raw_kind = action.get("pool_kind")
    pool_kind = PoolKind(raw_kind) if raw_kind else None
    pool_spend = PoolSpend(action.get("pool_spend", PoolSpend.NONE))
    result = resolve_test(
        target=target, modifier=modifier, defaulted=defaulted, roll=roll,
        pools=pools, pool_kind=pool_kind, pool_spend=pool_spend,
    )
    payload = asdict(result)
    payload["degree"] = result.degree
    payload["character"] = character.name
    payload["skill"] = skill
    payload["aptitude"] = aptitude
    return payload
