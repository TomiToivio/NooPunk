"""The CWN contract: shared facts, and a resolver the host owns (#946).

The MUD must not contain a second CWN implementation. This module carries only what Godot, the tabletop and
the MUD have to agree on — the numbers published in the canonical rules file — and a Protocol that the host
implements with its own engine.

Conformance is testable: `canon()` reads `data/rules/without_number.json` from the repository, and
`tests/test_rules_contract.py` fails if this module's constants drift away from it.
"""
from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Protocol, runtime_checkable

#: Repository root, two levels up from this file (`mud/nopunk_mud/`).
REPO_ROOT = Path(__file__).resolve().parents[2]
CANON_PATH = REPO_ROOT / "data" / "rules" / "without_number.json"

#: The 2d6 difficulty bands. Published values; the host resolves against them, it does not invent new ones.
DIFFICULTIES: dict[str, int] = {"easy": 6, "routine": 8, "hard": 10, "very_hard": 12, "heroic": 14}

#: Untrained skills take this modifier, per the Without Number core.
UNTRAINED_MODIFIER = -1

ATTRIBUTE_MIN = 3
ATTRIBUTE_MAX = 18
SKILL_RANK_MIN = -1  # -1 is untrained
SKILL_RANK_MAX = 4


class CanonError(RuntimeError):
    """The canonical rules file cannot be read or does not say what this module claims it says."""


def canon(path: Path = CANON_PATH) -> dict[str, Any]:
    """Load the canonical rules facts. Read-only: the MUD never writes here."""
    if not path.is_file():
        raise CanonError(f"canonical rules file missing: {path}")
    return json.loads(path.read_text(encoding="utf-8"))


@dataclass(frozen=True)
class Check:
    """A CWN skill check request. The MUD builds these; the host resolves them."""

    skill: str
    rank: int
    attribute_modifier: int
    difficulty: int
    circumstances: int = 0
    aid: int = 0

    def modifier(self) -> int:
        # Rank 0 is TRAINED in Without Number; only -1 is untrained. Treating 0 as untrained would
        # quietly penalise every starting character.
        rank_modifier = UNTRAINED_MODIFIER if self.rank < 0 else self.rank
        return rank_modifier + self.attribute_modifier + self.circumstances + self.aid

    def target(self) -> int:
        return self.difficulty

    def legal(self) -> list[str]:
        """Problems with this request. Empty means the host may resolve it."""
        problems: list[str] = []
        if not SKILL_RANK_MIN <= self.rank <= SKILL_RANK_MAX:
            problems.append(f"rank {self.rank} outside {SKILL_RANK_MIN}..{SKILL_RANK_MAX}")
        if self.difficulty not in DIFFICULTIES.values():
            problems.append(f"difficulty {self.difficulty} is not a published band")
        if not -2 <= self.circumstances <= 2:
            problems.append("circumstances cap at +/-2")
        if not 0 <= self.aid <= 1:
            problems.append("assistance is capped at +1")
        return problems


@dataclass(frozen=True)
class CheckResult:
    success: bool
    total: int
    target: int
    dice: tuple[int, int]
    engine: str = "cwn"


@runtime_checkable
class RulesEngine(Protocol):
    """What the host must provide. Evennia will implement this over the same kernel Godot uses."""

    def roll(self, check: Check) -> CheckResult:  # pragma: no cover - protocol
        ...


class DeterministicEngine:
    """A resolver with no randomness: for tests and for the no-LLM fallback path.

    It is **not** a second rules engine — it takes a pre-rolled pair and applies the published arithmetic.
    """

    def __init__(self, dice: tuple[int, int] | None = None) -> None:
        self._dice = dice

    def roll(self, check: Check) -> CheckResult:
        problems = check.legal()
        if problems:
            raise ValueError("; ".join(problems))
        dice = self._dice or (3, 3)  # a middling, deterministic result
        total = dice[0] + dice[1] + check.modifier()
        return CheckResult(success=total >= check.target(), total=total, target=check.target(), dice=dice)
