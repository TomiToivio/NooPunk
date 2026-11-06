"""The authoritative game clock (#1230 Phase 1).

One clock, one timeline. Everything that needs to know what time it is in NoöPunk reads it from here, so a task's
remaining minutes, an appointment's due time and a nightly dream cannot disagree about when "now" is.

Three properties are deliberate:

* **No wall clock.** The clock is constructed with an explicit start and only ever moves when :meth:`advance` is
  called. A game that reads the host clock is not replayable, and a replay is how a save is tested.
* **Monotonic.** Time never goes backwards; a negative advance is refused rather than clamped, because a silent clamp
  hides the bug that produced it.
* **Local, not naive.** The setting is Helsinki, so the clock carries a timezone. DST is handled by the tz database,
  and a local time that does not exist (the spring-forward hour) raises instead of quietly landing an appointment an
  hour away from where the player expected it.

What this module does *not* do: it defines no schedule. Workdays, briefings, sleep and deadlines belong to the daily
loop, which asks this clock what time it is. Nothing here knows that Tony German exists.
"""
from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

__all__ = ["ClockError", "GameClock", "HELSINKI", "MINUTES_PER_DAY"]

#: The campaign's timezone. Named once so a test can assert it rather than repeat the string.
HELSINKI = "Europe/Helsinki"

MINUTES_PER_DAY = 24 * 60


class ClockError(ValueError):
    """A clock operation that would break determinism or the timeline."""


@dataclass(frozen=True, slots=True)
class GameClock:
    """A deterministic, monotonic, timezone-aware clock."""

    #: The current in-world moment. Always timezone-aware.
    now: datetime
    #: The timezone the campaign runs in.
    zone: str = HELSINKI

    def __post_init__(self) -> None:
        if self.now.tzinfo is None:
            raise ClockError("the game clock needs a timezone-aware moment, never a naive one")
        try:
            ZoneInfo(self.zone)
        except (ZoneInfoNotFoundError, ValueError) as exc:  # pragma: no cover - environment failure
            raise ClockError(f"unknown timezone {self.zone!r}") from exc
        if self.now.utcoffset() is None:
            raise ClockError("the game clock's moment has no UTC offset")

    # -- construction -------------------------------------------------------------------------- #
    @classmethod
    def start(cls, *, year: int, month: int, day: int, hour: int = 8, minute: int = 0,
              zone: str = HELSINKI) -> "GameClock":
        """Start a campaign at a local moment. The caller states the opening date; nothing is assumed."""
        return cls(now=cls.local(year, month, day, hour, minute, zone=zone), zone=zone)

    @staticmethod
    def local(year: int, month: int, day: int, hour: int, minute: int = 0, *,
              zone: str = HELSINKI) -> datetime:
        """An aware local moment, or :class:`ClockError` if that local time does not exist."""
        tz = ZoneInfo(zone)
        naive = datetime(year, month, day, hour, minute)
        aware = naive.replace(tzinfo=tz)
        # A spring-forward local time is unreal: round-tripping through UTC moves it. Refusing is the only honest
        # answer, because silently choosing an offset would place an appointment somewhere the player cannot see.
        if aware.astimezone(ZoneInfo("UTC")).astimezone(tz).replace(tzinfo=None) != naive:
            raise ClockError(f"{naive.isoformat()} does not exist in {zone} (daylight-saving transition)")
        return aware

    # -- reading ------------------------------------------------------------------------------- #
    @property
    def date_key(self) -> str:
        """The local calendar day, as ``YYYY-MM-DD``. Used for daily bookkeeping and save keys."""
        return self.now.astimezone(ZoneInfo(self.zone)).date().isoformat()

    def minutes_until(self, moment: datetime) -> int:
        """Whole minutes from now until ``moment``; negative when the moment has passed."""
        return int((moment - self.now).total_seconds() // 60)

    # -- moving -------------------------------------------------------------------------------- #
    def advance(self, *, minutes: int = 0, days: int = 0) -> "GameClock":
        """Return the clock moved forward. Never mutates, never goes backwards."""
        if minutes < 0 or days < 0:
            raise ClockError("the game clock cannot run backwards")
        if not minutes and not days:
            raise ClockError("advance needs a non-zero duration")
        return GameClock(now=self.now + timedelta(days=days, minutes=minutes), zone=self.zone)

    def advance_to(self, moment: datetime) -> "GameClock":
        """Fast-forward to a known moment (an appointment, a task's end). Refuses to move backwards."""
        if moment <= self.now:
            raise ClockError(f"{moment.isoformat()} is not in the future of {self.now.isoformat()}")
        return GameClock(now=moment, zone=self.zone)

    # -- persistence --------------------------------------------------------------------------- #
    def to_dict(self) -> dict[str, str]:
        return {"zone": self.zone, "now": self.now.isoformat()}

    @classmethod
    def from_dict(cls, payload: dict[str, object]) -> "GameClock":
        raw = payload.get("now")
        zone = str(payload.get("zone") or HELSINKI)
        if not isinstance(raw, str) or not raw:
            raise ClockError("a saved clock needs its 'now' moment")
        try:
            moment = datetime.fromisoformat(raw)
        except ValueError as exc:
            raise ClockError(f"unreadable clock moment {raw!r}") from exc
        return cls(now=moment, zone=zone)
