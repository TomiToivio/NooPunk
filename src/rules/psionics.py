"""NoöPunk psychic techniques: authorization over the existing SWN Effort engine.

This is an incremental #652 migration. Technique effects are original scenario
content, not a transcription of SWN Revised's proprietary power catalogue.
"""
from __future__ import annotations

from dataclasses import dataclass

from .swn_psionics import DISCIPLINES, Duration, PsiRulesError, Psychic as _EffortPsychic

PSYCHIC_PACKAGES = frozenset({"swn_psychic", "swn_partial_psychic"})
TECHNIQUES = {
    "surface_read": ("Telepathy", 0),
    "empathic_trace": ("Telepathy", 1),
    "premonition": ("Precognition", 0),
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
        try:
            discipline, rank = TECHNIQUES[technique_id]
        except KeyError as exc:
            raise PsiRulesError(f"unknown NoöPunk technique: {technique_id}") from exc
        self.commit(key, discipline, minimum_rank=rank,
                    duration=duration or Duration.SCENE)

    @classmethod
    def from_snapshot(cls, state: dict) -> "Psychic":
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


__all__ = ["DISCIPLINES", "Duration", "PsiRulesError", "Psychic",
           "Technique", "TECHNIQUES", "PSYCHIC_PACKAGES", "authorized"]
