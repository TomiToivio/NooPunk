"""Helsinki-only Romppainen–Fujita helmet apparatus (#985).

A device-specific overlay, never a change to the CWN/SWN rules. The caller
persists the returned JSON-compatible state in the character's save data.
The in-world day comes from campaign state, NEVER the computer's clock.
"""
from __future__ import annotations

from dataclasses import dataclass

DEVICE = "Romppainen–Fujita"
OFFICE = "Helsinki"
DAILY_LIMIT = 4
HELMET_DESCRIPTION = (
    "The administrator and subject wear absurdly bulky psychotronic helmets. "
    "Blinking amber and violet lights blink out of sequence; the console beeps."
)


class DeviceUnavailable(ValueError):
    """The attempt was refused without spending a test."""


@dataclass(frozen=True)
class Use:
    day: int
    count: int

    def to_dict(self) -> dict[str, int]:
        return {"day": self.day, "count": self.count}

    @classmethod
    def from_dict(cls, value: dict | None, *, day: int) -> "Use":
        if isinstance(day, bool) or not isinstance(day, int) or day < 0:
            raise DeviceUnavailable("Invalid in-world day.")
        if not value:
            return cls(day, 0)
        saved_day, count = value.get("day"), value.get("count")
        if any(isinstance(v, bool) or not isinstance(v, int) for v in (saved_day, count)):
            raise DeviceUnavailable("Corrupt apparatus usage record; no changes made.")
        if saved_day > day or saved_day < 0 or not 0 <= count <= DAILY_LIMIT:
            raise DeviceUnavailable("Invalid apparatus usage record or reversed in-world day.")
        return cls(day, count if saved_day == day else 0)


def perform(
    record: dict | None, *, day: int, office: str,
    administrator_helmet: bool, subject_helmet: bool,
) -> Use:
    """Validate first; caller saves the returned record only after a completed use."""
    current = Use.from_dict(record, day=day)
    if office.casefold() != OFFICE.casefold():
        raise DeviceUnavailable("The Romppainen–Fujita apparatus is exclusive to UNSA Helsinki.")
    if not administrator_helmet or not subject_helmet:
        raise DeviceUnavailable("Both administrator and subject must wear their psychotronic helmets.")
    if current.count >= DAILY_LIMIT:
        raise DeviceUnavailable("Four tests already completed today. No fifth test is permitted.")
    return Use(day, current.count + 1)


def available(record: dict | None, *, day: int) -> int:
    return DAILY_LIMIT - Use.from_dict(record, day=day).count
