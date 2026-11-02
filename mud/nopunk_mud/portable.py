"""Engine-neutral NoöPunk single-player application API.

Issue #1053/#1054: a thin, standard-library-only boundary over existing
published CWN mechanics and the original UNSA solo-campaign transitions.
No framework imports; no replacement rules or hidden GM required.
"""
from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from .solo_campaign import Campaign, advance, SCENES
from .cwn_core import skill_check

STATE_VERSION = 1


@dataclass(frozen=True)
class Command:
    action: str
    location: str


@dataclass(frozen=True)
class Result:
    state: dict[str, Any]
    message: str
    finished: bool


class PortableSession:
    """Same public commands/state for terminal, Evennia and future adapters."""

    def __init__(self, campaign: Campaign | None = None):
        self._campaign = campaign or Campaign()

    @property
    def state(self) -> dict[str, Any]:
        return {"version": STATE_VERSION, "campaign": self._campaign.to_dict()}

    def execute(self, command: Command) -> Result:
        next_campaign, message = advance(
            self._campaign, command.action, command.location
        )
        self._campaign = next_campaign
        return Result(self.state, message, next_campaign.stage == "complete")

    def describe(self) -> str:
        return SCENES[self._campaign.stage]

    def save(self, filename: str | Path) -> None:
        Path(filename).write_text(
            json.dumps(self.state, ensure_ascii=False, indent=2), encoding="utf-8"
        )

    @classmethod
    def restore(cls, filename: str | Path) -> "PortableSession":
        data = json.loads(Path(filename).read_text(encoding="utf-8"))
        if data.get("version") != STATE_VERSION:
            raise ValueError("Unsupported portable save version")
        campaign = data.get("campaign")
        if not isinstance(campaign, dict):
            raise ValueError("Invalid campaign save")
        if campaign.get("stage", "briefing") not in SCENES:
            raise ValueError("Unknown campaign stage")
        return cls(Campaign.from_dict(campaign))


def resolve_cwn_check(rank: int, attribute_score: int,
                      difficulty: int, *, dice: tuple[int, int]):
    """Delegate skill checks to the existing CWN implementation unchanged."""
    return skill_check(rank, attribute_score, difficulty, dice=dice)
