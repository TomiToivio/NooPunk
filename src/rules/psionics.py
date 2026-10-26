"""NoöPunk psychic techniques: authorization over the existing SWN Effort engine.

This is an incremental #652 migration. Technique effects are original scenario
content, not a transcription of SWN Revised's proprietary power catalogue.
"""
from __future__ import annotations

import json
from collections.abc import Mapping
from dataclasses import dataclass
from pathlib import Path

from .swn_psionics import DISCIPLINES, Duration, PsiRulesError
from .swn_psionics import Psychic as _EffortPsychic

PSYCHIC_PACKAGES = frozenset({"swn_psychic", "swn_partial_psychic"})
TECHNIQUES = {
    "surface_read": ("Telepathy", 0),
    "empathic_trace": ("Telepathy", 1),
    "premonition": ("Precognition", 0),
}

#: The catalogue's ``effort`` vocabulary mapped onto the Effort engine's durations.
DURATION_BY_EFFORT = {
    "commit_scene": Duration.SCENE,
    "commit_day": Duration.DAY,
    "none": Duration.ACTIVE,
}


@dataclass(frozen=True)
class Technique:
    key: str
    discipline: str
    minimum_rank: int
    duration: Duration = Duration.SCENE


def authorized(permissions: set[str]) -> bool:
    return bool(PSYCHIC_PACKAGES.intersection(permissions))


class Psychic(_EffortPsychic):
    """Effort pool with a strict psychic-package gate before any reservation."""

    def commit(self, key: str, discipline: str, *, minimum_rank: int = 0,
               duration: Duration = Duration.SCENE, amount: int = 1) -> None:
        if not authorized(self.permissions):
            raise PsiRulesError("psychic character package required")
        super().commit(key, discipline, minimum_rank=minimum_rank,
                       duration=duration, amount=amount)

    def use_technique(self, key: str, technique_id: str,
                      *, duration: Duration | None = None) -> None:
        """Commit Effort for a technique, resolving it through the authored catalogue.

        ``may_use`` reads the catalogue, so this must too: an id the gate accepts
        but this method rejects is the silent contradiction that made the first
        case's psionic beat unrunnable. The legacy ``TECHNIQUES`` map stays as a
        fallback for ids authored before the catalogue existed.
        """
        try:
            discipline, rank = TECHNIQUES[technique_id]
        except KeyError:
            entry = load_catalogue().get(technique_id)
            if entry is None:
                raise PsiRulesError(f"unknown NoöPunk technique: {technique_id}") from None
            discipline = str(entry.get("discipline", ""))
            rank = int(entry.get("min_skill", 0))
            if duration is None:
                duration = DURATION_BY_EFFORT.get(str(entry.get("effort", "none")),
                                                  Duration.SCENE)
        self.commit(key, discipline, minimum_rank=rank,
                    duration=duration or Duration.SCENE)

    @classmethod
    def from_snapshot(cls, state: dict) -> Psychic:
        # Validate snapshot through the original strict resource parser, then
        # reconstruct the concrete gated type without spending Effort again.
        legacy = _EffortPsychic.from_snapshot(state)
        if legacy.reservations and not authorized(legacy.permissions):
            raise PsiRulesError("unauthorized persisted Effort commitments")
        psychic = cls(legacy.wisdom, legacy.constitution,
                      dict(legacy.disciplines), set(legacy.permissions))
        psychic.reservations = dict(legacy.reservations)
        psychic.scene = legacy.scene
        return psychic


__all__ = [
    "DISCIPLINES",
    "PSYCHIC_PACKAGES",
    "TECHNIQUES",
    "Duration",
    "PsiRulesError",
    "Psychic",
    "Technique",
    "authorized",
]


# --------------------------------------------------------------------------- #
# The authored technique catalogue (#652)
# --------------------------------------------------------------------------- #
#
# `TECHNIQUES` above is the authorization gate: a technique id, its discipline and the rank it needs.
# The catalogue in `data/rules/psionics_techniques.json` adds what a table needs to *play* one — its
# Effort cost, how long the commitment lasts, whether it calls for a check, and its effect text. The
# effect text is NoöPunk content; SWN has no verified SRD licence, so none of its power text or names
# is reproduced (docs/licenses/ISSUE_569_WITHOUT_NUMBER_RIGHTS.md).

CATALOGUE_PATH = Path(__file__).resolve().parents[2] / "data" / "rules" / "psionics_techniques.json"

_CATALOGUE: dict[str, dict] | None = None


def load_catalogue(path: Path | str | None = None) -> dict[str, dict]:
    """Load the authored catalogue, keyed by technique id.

    The catalogue is validated by the scenario data-contract test, not here: a malformed entry is a
    content bug, and this function's job is only to make the content reachable.
    """
    global _CATALOGUE
    if path is None and _CATALOGUE is not None:
        return _CATALOGUE
    raw = json.loads(Path(path or CATALOGUE_PATH).read_text(encoding="utf-8"))
    entries: dict[str, dict] = {}
    for discipline, core in (raw.get("discipline_cores") or {}).items():
        entry = dict(core)
        entry.setdefault("discipline", discipline)
        entry["core"] = True
        entries[str(entry["id"])] = entry
    for entry in raw.get("techniques", []):
        entries[str(entry["id"])] = dict(entry)
    if path is None:
        _CATALOGUE = entries
    return entries


def may_use(disciplines: Mapping[str, int], technique_id: str,
            *, catalogue: dict[str, dict] | None = None) -> bool:
    """The training gate: a permission check, never a difficulty penalty.

    An untaught character cannot attempt the technique at all; a taught one still has to pass its
    check and pay its Effort.
    """
    entry = (catalogue or load_catalogue()).get(technique_id)
    if entry is None:
        return False
    discipline = str(entry.get("discipline", ""))
    return int(disciplines.get(discipline, -1)) >= int(entry.get("min_skill", 0))


def effort_duration(technique_id: str, *, catalogue: dict[str, dict] | None = None) -> str:
    """``none``, ``scene`` or ``day``: what using this technique does to the Effort pool."""
    entry = (catalogue or load_catalogue()).get(technique_id, {})
    cost = str(entry.get("effort", "none"))
    return {"commit_scene": "scene", "commit_day": "day"}.get(cost, "none")


__all__ += ["CATALOGUE_PATH", "effort_duration", "load_catalogue", "may_use"]
