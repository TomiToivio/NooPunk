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
PROTOCOL = "romppainen_fujita"
PROTOCOL_NAME = "Romppainen–Fujita psychotronic empathy assessment"
DEVICE_NAME = "Romppainen–Fujita psychotronic empathy device"
MAX_DAILY_TESTS = 4
DEVICE_LOCATION = "UNSA Helsinki Field Office"


class DeviceError(ValueError):
    """The device cannot be used as requested; it refuses rather than improvising."""


@dataclass
class DeviceSession:
    """Daily-use rules for the Romppainen–Fujita device (#985).

    The device is only installed in the Helsinki field office, both people wear the helmet, and a
    field agent may run at most four tests a day before the goofiness makes further readings junk.
    """

    tests_today: int = 0
    location: str = DEVICE_LOCATION
    administrator_helmet: bool = True
    subject_helmet: bool = True

    def administer(self) -> int:
        if self.location != DEVICE_LOCATION:
            raise DeviceError("the device is only used by the Helsinki UNSA Field Office")
        if not (self.administrator_helmet and self.subject_helmet):
            raise DeviceError("both administrator and subject must wear the psychotronic helmet")
        if self.tests_today >= MAX_DAILY_TESTS:
            raise DeviceError("daily limit reached: more than four tests makes the readings goofy")
        self.tests_today += 1
        return self.tests_today

    @property
    def goofy(self) -> bool:
        return self.tests_today >= MAX_DAILY_TESTS


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


# --------------------------------------------------------------------------------------------------
# The device itself (#985)
# --------------------------------------------------------------------------------------------------
# A device-specific NooPunk overlay: it constrains who may be tested and how often. It is not a CWN rule
# and it must not be modelled as fatigue damage or as a modifier to the assessment score.

#: The device is not standard UNSA equipment; only the Helsinki field office runs one. Its name lives in
#: DEVICE_NAME above - do not redefine it here, or this block shadows the canonical constant.

FIELD_OFFICE = "helsinki"
#: More than this in one in-world day leaves a field agent feeling "goofy". The rule is a safety limit,
#: not a convenience: the counter is per agent and per in-world day.
DAILY_TEST_LIMIT = 4


@dataclass(frozen=True)
class DeviceState:
    """How many tests one agent has taken on one in-world day.

    Plain data so it survives a save: ``day`` is the in-world day ordinal, ``used`` the tests taken that day.
    A different ``day`` means the counter has rolled over.
    """

    day: int = 0
    used: int = 0

    def to_dict(self) -> dict[str, int]:
        return {"day": self.day, "used": self.used}

    @classmethod
    def from_dict(cls, data: dict) -> DeviceState:
        return cls(day=int(data.get("day", 0)), used=int(data.get("used", 0)))


def _that_day(state: DeviceState, day: int) -> DeviceState:
    """Roll the counter over when the in-world day has changed."""
    return DeviceState(day=day, used=0) if state.day != day else state


def check_fit(*, administrator_helmet: bool, subject_helmet: bool) -> None:
    """Both the administrator and the subject must wear the helmet. One helmet is not a test."""
    if not administrator_helmet:
        raise DeviceError("the administrator must wear the psychotronic helmet too")
    if not subject_helmet:
        raise DeviceError("the subject must wear the psychotronic helmet")


def remaining(state: DeviceState, *, day: int) -> int:
    """How many tests this agent may still take today."""
    return DAILY_TEST_LIMIT - _that_day(state, day).used


def begin_test(state: DeviceState, *, day: int,
               administrator_helmet: bool, subject_helmet: bool) -> DeviceState:
    """Validate a session and return the state with the test recorded.

    Refuses, without recording anything, when the helmets are not worn or the daily cap is reached. The
    case still yields its core clue by another path - the cap must never make a case unsolvable.
    """
    check_fit(administrator_helmet=administrator_helmet, subject_helmet=subject_helmet)
    current = _that_day(state, day)
    if current.used >= DAILY_TEST_LIMIT:
        raise DeviceError(
            f"this agent has already taken {DAILY_TEST_LIMIT} tests today; "
            f"more than that leaves them goofy. Try again on the next in-world day.")
    return DeviceState(day=current.day, used=current.used + 1)
