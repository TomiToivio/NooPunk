"""Romppainen consciousness assessment (#985).

A deterministic, CWN-compatible interview procedure. It scores four observed channels, returns a
pattern band with confidence and caveats, and always yields a core investigative clue — a failed
interview roll costs detail, never the case. It is not a consciousness detector and says so.
"""
from __future__ import annotations

from dataclasses import dataclass, field

CHANNELS = ("affect", "coherence", "bci", "empathy")
WEIGHTS = {"affect": 0.30, "coherence": 0.25, "bci": 0.25, "empathy": 0.20}
SIGNAL_MIN, SIGNAL_MAX = -2, 2
PROTOCOL = "helsinki"


class AssessmentError(ValueError):
    """Invalid observations; the protocol refuses rather than guessing."""


@dataclass(frozen=True)
class Signals:
    affect: int
    coherence: int
    bci: int
    empathy: int
    psi: int | None = None

    def values(self) -> dict[str, int]:
        return {"affect": self.affect, "coherence": self.coherence,
                "bci": self.bci, "empathy": self.empathy}


@dataclass(frozen=True)
class Assessment:
    score: int
    classification: str
    confidence: float
    strongest_channel: str
    core_clue: str
    caveats: tuple[str, ...] = field(default_factory=tuple)
    protocol: str = PROTOCOL


CORE_CLUES = {
    "affect": "The subject's affect does not match the account they are giving.",
    "coherence": "The account changes under gentle repetition; the contradiction is usable evidence.",
    "bci": "The telemetry disagrees with the spoken answer at a specific, testable moment.",
    "empathy": "The subject's concern is selective rather than absent; the boundary is evidence.",
}


def _check(signals: Signals) -> None:
    for channel, value in signals.values().items():
        if not SIGNAL_MIN <= value <= SIGNAL_MAX:
            raise AssessmentError(f"{channel} signal outside {SIGNAL_MIN}..{SIGNAL_MAX}")
    if signals.psi is not None and not SIGNAL_MIN <= signals.psi <= SIGNAL_MAX:
        raise AssessmentError(f"psi signal outside {SIGNAL_MIN}..{SIGNAL_MAX}")


def _normalised(value: int) -> float:
    return (value - SIGNAL_MIN) / (SIGNAL_MAX - SIGNAL_MIN) * 100.0


def assess(signals: Signals) -> Assessment:
    _check(signals)
    score = round(sum(_normalised(value) * WEIGHTS[channel]
                      for channel, value in signals.values().items()))

    # A coherent interior account that fails human empathy is not the same finding as a simulated
    # affect with no interior account. Keep them separate rather than collapsing both into a score.
    if signals.coherence >= 1 and signals.empathy <= -1:
        classification = "nhi_nonanthropocentric"
    elif signals.affect >= 1 and signals.coherence < 0 and signals.empathy <= 0:
        classification = "nonconscious_pattern"
    elif score >= 75:
        classification = "baseline_human"
    elif score >= 60:
        classification = "uncertain"
    else:
        classification = "atypical"

    values = list(signals.values().values())
    spread = max(values) - min(values)
    confidence = round(min(0.95, 0.55 + (100 - spread * 20) / 200 + (0.05 if signals.psi is not None else 0.0)), 2)
    if classification == "uncertain":
        confidence = min(confidence, 0.6)

    strongest = max(signals.values(), key=lambda channel: abs(signals.values()[channel]))
    caveats = [
        "Pattern, not proof: consciousness is not intelligence and not empathy.",
        "Anthropocentric empathy criteria can fail a genuine non-human consciousness.",
        "Interviewer skill, language and BCI quality move the result.",
    ]
    if signals.psi is None:
        caveats.append("No psychotronic/PSI channel was taken; later cases may add one.")
    return Assessment(score=score, classification=classification, confidence=confidence,
                       strongest_channel=strongest, core_clue=CORE_CLUES[strongest],
                       caveats=tuple(caveats))
