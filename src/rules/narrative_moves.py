"""The closed move set of the narrative layer — issue #689, stage 1.

Eight procedures, each a *trigger* plus a banded outcome. A move adds no dice, no modifier
and no currency: it hands the core's total to :func:`narrative_layer.band_for` and returns
what the fiction does next. The set is closed on purpose — eight procedures can be
table-tested at one table, and a ninth has to argue for itself against this line.

`data/rules/narrative_moves.json` is the single source; no outcome text is restated here.
Skills and attributes are validated against `data/rules/without_number.json`, so a rename in
the baseline cannot leave a move pointing at a skill that no longer exists.

**Status: PROVISIONAL, not canonical.** `IS_CANONICAL = False`; the author owns calibration.
"""
from __future__ import annotations

import json
import re
from collections.abc import Mapping
from dataclasses import dataclass, field
from functools import lru_cache
from pathlib import Path
from typing import Any

from .narrative_layer import OUTCOME_BANDS, NarrativeError, band_for, gm_move

DATA = Path(__file__).resolve().parents[2] / "data" / "rules"
MOVES_PATH = DATA / "narrative_moves.json"
BASELINE_PATH = DATA / "without_number.json"

#: PROVISIONAL. A ninth move must change this line and the rulebook chapter together.
CLOSED_SET_SIZE = 8

#: PROVISIONAL. The only two ways a move can be rolled.
KINDS = frozenset({"check", "save"})

#: A check whose skill is whatever the action itself uses ("set up").
ACTION_SKILL_POLICY = "action"

_ID = re.compile(r"^[a-z][a-z0-9_]*$")


@dataclass(frozen=True, slots=True)
class Move:
    """One trigger, four banded outcomes, and optional banded grants."""

    id: str
    name: str
    kind: str
    trigger: str
    outcomes: Mapping[str, str]
    skill: str | None = None
    attribute: str | None = None
    save: str | None = None
    skill_policy: str | None = None
    grants: Mapping[str, Mapping[str, int]] = field(default_factory=dict)

    def grant(self, name: str, band: str) -> int:
        return self.grants.get(name, {}).get(band, 0)


@dataclass(frozen=True, slots=True)
class MoveOutcome:
    """What the table is told: the band, the move it maps to, and the fiction."""

    move_id: str
    band: str
    gm_move: str
    outcome: str
    grants: Mapping[str, int]


def _vocabulary() -> tuple[frozenset[str], frozenset[str], frozenset[str]]:
    """The baseline's own vocabulary, so a rename there cannot leave a move dangling."""
    raw = json.loads(BASELINE_PATH.read_text(encoding="utf-8"))
    skills = frozenset(raw["skills"]["names"])
    attributes = frozenset(raw["attributes"]["names"])
    saves = frozenset(name.lower() for name in raw["saves"]["attributes"])
    return skills, attributes, saves


def _build(raw: Mapping[str, Any]) -> dict[str, Move]:
    skills, attributes, saves = _vocabulary()
    entries = raw.get("moves")
    if not isinstance(entries, list):
        raise NarrativeError("narrative_moves.json: 'moves' must be a list")
    if len(entries) != CLOSED_SET_SIZE:
        raise NarrativeError(
            f"the move set is closed: expected {CLOSED_SET_SIZE} moves, found {len(entries)}"
        )

    built: dict[str, Move] = {}
    for entry in entries:
        move_id = entry.get("id", "")
        if not _ID.match(move_id):
            raise NarrativeError(f"move id must be snake_case: {move_id!r}")
        if move_id in built:
            raise NarrativeError(f"duplicate move id: {move_id!r}")

        kind = entry.get("kind")
        if kind not in KINDS:
            raise NarrativeError(f"{move_id}: kind must be one of {sorted(KINDS)}, got {kind!r}")

        outcomes = entry.get("outcomes") or {}
        if set(outcomes) != set(OUTCOME_BANDS):
            raise NarrativeError(
                f"{move_id}: outcomes must name exactly {list(OUTCOME_BANDS)}, "
                f"got {sorted(outcomes)}"
            )
        for band, text in outcomes.items():
            if not str(text).strip():
                raise NarrativeError(f"{move_id}: empty outcome for band {band!r}")

        skill = attribute = save = policy = None
        if kind == "check":
            policy = entry.get("skill_policy")
            attribute = entry.get("attribute")
            skill = entry.get("skill")
            if policy == ACTION_SKILL_POLICY:
                # The action itself supplies skill and attribute; the move names neither.
                if skill or attribute:
                    raise NarrativeError(f"{move_id}: an action-skill move names no skill/attribute")
            elif policy is not None:
                raise NarrativeError(f"{move_id}: unknown skill_policy {policy!r}")
            else:
                if skill not in skills:
                    raise NarrativeError(f"{move_id}: {skill!r} is not a baseline skill")
                if attribute not in attributes:
                    raise NarrativeError(f"{move_id}: {attribute!r} is not a baseline attribute")
        else:
            save = entry.get("save")
            if save not in saves:
                raise NarrativeError(f"{move_id}: {save!r} is not a baseline save")
            if skill or attribute:
                raise NarrativeError(f"{move_id}: a save carries no skill or attribute")

        grants = entry.get("grants") or {}
        for name, per_band in grants.items():
            if not per_band:
                raise NarrativeError(f"{move_id}: grant {name!r} names no band")
            for band, amount in per_band.items():
                if band not in OUTCOME_BANDS:
                    raise NarrativeError(f"{move_id}: grant {name!r} has unknown band {band!r}")
                if not isinstance(amount, int) or isinstance(amount, bool) or amount <= 0:
                    raise NarrativeError(
                        f"{move_id}: grant {name!r}/{band} must be a positive integer"
                    )

        built[move_id] = Move(
            id=move_id,
            name=entry.get("name") or move_id,
            kind=kind,
            trigger=entry.get("trigger") or "",
            outcomes=dict(outcomes),
            skill=skill,
            attribute=attribute,
            save=save,
            skill_policy=policy,
            grants=dict(grants),
        )
    return built


@lru_cache(maxsize=4)
def _cached(path: str) -> dict[str, Move]:
    return _build(json.loads(Path(path).read_text(encoding="utf-8")))


def moves(path: Path | None = None) -> dict[str, Move]:
    """The closed set, keyed by id. One load per path per process."""
    return dict(_cached(str(path or MOVES_PATH)))


def move(move_id: str, path: Path | None = None) -> Move:
    try:
        return moves(path)[move_id]
    except KeyError:
        raise NarrativeError(
            f"unknown move: {move_id!r} (the set is closed; see narrative_moves.json)"
        ) from None


def move_ids(path: Path | None = None) -> tuple[str, ...]:
    return tuple(moves(path))


def resolve_move(
    move_id: str, *, total: int, difficulty: int, path: Path | None = None
) -> MoveOutcome:
    """Read the core's total into a band and return the move's outcome for it.

    Deterministic and total: no randomness, no LLM, no state. The caller rolls; this reads.
    """
    chosen = move(move_id, path)
    band = band_for(total - difficulty)
    return MoveOutcome(
        move_id=chosen.id,
        band=band,
        gm_move=gm_move(band=band),
        outcome=chosen.outcomes[band],
        grants={name: per_band[band] for name, per_band in chosen.grants.items() if band in per_band},
    )
