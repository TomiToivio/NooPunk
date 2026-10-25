"""The ubiquitous network — NoöPunk's own hacking subsystem (issue #572).

**Status: PROVISIONAL, not canonical.** Every number is a `TUNING_` constant and belongs to the
author; nothing in the shipped `src/rules/core.py` path imports this module.

Why this exists at all: `AGENTS.md` §4 reserves *hacking / cyberspace mechanics* until the author
defines an original subsystem. Issue #517 landed the canon geography (`rulebook/22_CYBERSPACE_AFTER_THE_CRISIS.md`:
five **access classes**, the Blackwall, Safenet, the three swarms) and issue #344 landed the target
taxonomy (`connectivity.json`: five **connectivity classes**) — but neither is arithmetic. The
CWN/SWN/AWN/WWN family offers a deck-and-program economy that assumes a *matrix*; NoöPunk assumes
**ubiquity with islands**, so the family has no equivalent to import. This module is the missing
arithmetic, and it obeys three canon statements rather than inventing around them:

1. *"Networks have geography again"* — reach is a property of **route × target × era**, never of a
   skill rating (22.5).
2. *"An air-gapped machine cannot be hacked remotely by narrative fiat"* — `isolated` is reachable
   by **class 1 only**, in every era, for every skill (22.5.2, enforced in `strategy_game/cyber.py`
   and re-used here).
3. Ubiquity is the **default**, and the crisis is the exception: in 2045 almost every device is on
   some mesh, so the interesting constraint is not *whether* a network exists but **who is watching
   it**. That is what `Exposure` models.

The design consequence, and the reason this is a NoöPunk subsystem rather than a CWN port: **there is
no concealment economy to buy, only an exposure economy to spend.** Nothing in the setting lets a
character become invisible on a ubiquitous network; the only lever is *how much of yourself you
leave* — which is the same lever the Noösphere and the three swarms apply in 22.6.4.

Usage::

    session = IntrusionSession(target=ConnectivityClass.LOCAL_ONLY,
                               access=AccessClass.NEARBY, era=Era.NHI_CRISIS, rng=Random(7))
    step = session.intrude(skill_rating=4, dv=15)   # costs AP, accrues exposure, rolls the core die
    session.cover()                                 # spends AP to stop leaving traces
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
import random
from typing import Any

from . import core
from .cross_domain_state import AP_PER_EXCHANGE

#: PROVISIONAL. The author owns every number below; they exist so the procedure is executable.
IS_CANONICAL = False

# --------------------------------------------------------------------------- #
# Canon vocabulary — consumed, never re-declared
# --------------------------------------------------------------------------- #

class ConnectivityClass(str, Enum):
    """What the *target* is. Issue #344's taxonomy, by name."""

    PUBLIC_GATEWAY = "public_gateway"
    SAFENET_EXPOSED = "safenet_exposed"
    PRIVATE_LINKED = "private_linked"
    LOCAL_ONLY = "local_only"
    ISOLATED = "isolated"


class AccessClass(str, Enum):
    """How the *operator* reaches it. `rulebook/22…` §22.5.1, classes 1–5."""

    LOCAL = "local"          # 1 — a body, a hand, a cable, a delivered device
    NEARBY = "nearby"        # 2 — the local RF envelope
    LAN = "lan"              # 3 — a foothold inside a segmented private network
    SAFENET = "safenet"      # 4 — the public network of the era
    QUARANTINE = "quarantine"  # 5 — a deliberate bridge into the quarantined old Internet


class Era(str, Enum):
    ACCELERATION = "acceleration"
    NHI_CRISIS = "nhi_crisis"
    AFTER_CRISIS = "after_crisis"


#: 22.5.2's pairing table, executable. A route reaches a target class only if it is listed here.
#: `isolated` → `LOCAL` only is the invariant the chapter repeats twice and #344 enforces in code.
REACH_TABLE: dict[ConnectivityClass, frozenset[AccessClass]] = {
    ConnectivityClass.PUBLIC_GATEWAY: frozenset({AccessClass.SAFENET, AccessClass.LAN}),
    ConnectivityClass.SAFENET_EXPOSED: frozenset({AccessClass.SAFENET, AccessClass.LAN}),
    ConnectivityClass.PRIVATE_LINKED: frozenset({AccessClass.LAN, AccessClass.LOCAL}),
    ConnectivityClass.LOCAL_ONLY: frozenset({AccessClass.LOCAL, AccessClass.NEARBY}),
    ConnectivityClass.ISOLATED: frozenset({AccessClass.LOCAL}),
}

#: 22.3.2 — entering the quarantined old Internet is a distinct offence, never a normal intrusion.
CONTAINMENT_BREACH_CLASSES = frozenset({AccessClass.QUARANTINE})

# --------------------------------------------------------------------------- #
# TUNING — the author's numbers, marked as such
# --------------------------------------------------------------------------- #

TUNING_AP_PER_ACTION = 1
TUNING_EXPOSURE_PER_ACTION = 1
TUNING_EXPOSURE_PER_MARGIN = 1        # a loud success leaves more than a quiet one
TUNING_COVER_REDUCTION = 2            # one Cover action buys back two units of exposure
TUNING_EXPOSURE_QUIET_MAX = 2
TUNING_EXPOSURE_WATCHED_MAX = 5
TUNING_EXPOSURE_FLAGGED_MAX = 9        # beyond this the network is hunting you
#: The shared clock's budget, consumed rather than re-declared (`rulebook/18`, #225).
TUNING_AP_PER_EXCHANGE = AP_PER_EXCHANGE


class NetworkError(ValueError):
    """A canon invariant was about to be violated."""


class AlertState(str, Enum):
    QUIET = "quiet"        # nobody is reading the logs
    WATCHED = "watched"    # a human might read them later
    FLAGGED = "flagged"    # something has been referred
    HUNTED = "hunted"      # the network is looking for you specifically


def reach(target: ConnectivityClass, access: AccessClass, era: Era) -> tuple[bool, str]:
    """Can this route reach this target in this era? Never a difficulty, always a gate.

    The era matters in exactly one place: the public network can be *down*. When it is, class 4
    reaches nothing and the operator must find a class 3 foothold instead — ubiquity is a property
    of the setting, not a guarantee at every hour of the crisis.
    """
    if access in CONTAINMENT_BREACH_CLASSES:
        return True, "a deliberate bridge: possible, and a grave international crime in every era"
    if access is AccessClass.SAFENET and era is Era.NHI_CRISIS and not safenet_up(era):
        return False, "the public network is degraded in this era: find a foothold (class 3)"
    if access in REACH_TABLE[target]:
        return True, f"class {access.value} reaches a target of class {target.value}"
    return False, f"a {access.value} route cannot reach a target of class {target.value}"


def safenet_up(era: Era) -> bool:
    """Whether the era's public network is usable at all.

    Acceleration: yes, and it is the open Internet. NHI Crisis: it is Safenet, degraded — the
    chapter's point is that the *mode* survives and the *reach* does not. After the Crisis: Safenet
    is up again and policed. TUNING: the crisis outage is a scenario dial, not a law.
    """
    return era is not Era.NHI_CRISIS


def alert_state(exposure: int) -> AlertState:
    """Where an exposure total sits. The bands are the author's; the ordering is the contract."""
    if exposure <= TUNING_EXPOSURE_QUIET_MAX:
        return AlertState.QUIET
    if exposure <= TUNING_EXPOSURE_WATCHED_MAX:
        return AlertState.WATCHED
    if exposure <= TUNING_EXPOSURE_FLAGGED_MAX:
        return AlertState.FLAGGED
    return AlertState.HUNTED


# --------------------------------------------------------------------------- #
# The session — a scene's worth of intrusion
# --------------------------------------------------------------------------- #

@dataclass(frozen=True)
class Step:
    """One intrusion action, and what it left behind."""

    action: str
    ap_spent: int
    exposure_added: int
    exposure_total: int
    alert: AlertState
    outcome: str = ""
    margin: int = 0
    breach: bool = False

    def as_text(self) -> str:
        bits = [f"{self.action}: {self.outcome or 'no check'}", f"{self.exposure_added:+d} exposure"]
        if self.margin:
            bits.append(f"margin {self.margin:+d}")
        if self.breach:
            bits.append("CONTAINMENT BREACH")
        bits.append(f"{self.exposure_total} total → {self.alert.value}")
        return "; ".join(bits)


@dataclass
class IntrusionSession:
    """One operator, one target, one scene.

    Action points are the shared clock's (3 per exchange, `rulebook/18`); this session spends them
    but does not own a second economy. Exposure is the setting's answer to ubiquity: it only ever
    goes up, except for what a Cover action buys back.
    """

    target: ConnectivityClass
    access: AccessClass
    era: Era
    rng: Any = field(default_factory=random.Random)
    exposure: int = 0
    ap: int = TUNING_AP_PER_EXCHANGE
    log: list[Step] = field(default_factory=list)

    def __post_init__(self) -> None:
        possible, reason = reach(self.target, self.access, self.era)
        if not possible:
            raise NetworkError(reason)

    # -- state ---------------------------------------------------------------------------

    @property
    def alert(self) -> AlertState:
        return alert_state(self.exposure)

    @property
    def breach(self) -> bool:
        return self.access in CONTAINMENT_BREACH_CLASSES

    def new_exchange(self) -> None:
        self.ap = TUNING_AP_PER_EXCHANGE

    def _spend(self, actions: int = 1) -> None:
        if self.ap < actions:
            raise NetworkError(
                f"not enough AP: {self.ap} left, {actions} needed; AP do not carry between exchanges"
            )
        self.ap -= actions

    # -- actions -------------------------------------------------------------------------

    def intrude(self, *, stat: int, skill_rating: int, dv: int, quiet: bool = False,
                die: int | None = None) -> Step:
        """Attempt one intrusion step on the shared kernel.

        `stat` is whichever STAT the canon skill binds to — `INT` for `Program`/`Insight`,
        `CYB` for `Interface`/`Infosec` — supplied by the caller from `data/rules/skills.json`
        rather than guessed here.

        `quiet=True` is the deliberate, slower attempt: it costs the same AP but halves the
        exposure a success adds (TUNING), which is the only way to trade time for silence.
        """
        self._spend()
        result = core.resolve_check(stat=stat, skill=skill_rating, target=dv,
                                    rng=self.rng, die=die)
        outcome = "success" if result.success else "failure"
        margin = result.total - dv
        added = TUNING_EXPOSURE_PER_ACTION + (max(0, margin) // 2 if not quiet else 0)
        if not result.success:
            added += TUNING_EXPOSURE_PER_ACTION  # a failed attempt is logged too
        self.exposure += added
        step = Step("intrude", TUNING_AP_PER_ACTION, added, self.exposure, self.alert,
                    outcome=outcome, margin=margin, breach=self.breach)
        self.log.append(step)
        return step

    def cover(self) -> Step:
        """Erase traces. The only action that lowers exposure, and it cannot go below zero."""
        self._spend()
        removed = min(TUNING_COVER_REDUCTION, self.exposure)
        self.exposure -= removed
        step = Step("cover", TUNING_AP_PER_ACTION, -removed, self.exposure, self.alert,
                    outcome="traces reduced", breach=self.breach)
        self.log.append(step)
        return step

    def exit(self) -> Step:
        """Leave. Always available, always costs something — the canon rule for projected states."""
        self._spend()
        step = Step("exit", TUNING_AP_PER_ACTION, 0, self.exposure, self.alert,
                    outcome="disconnected", breach=self.breach)
        self.log.append(step)
        return step


# --------------------------------------------------------------------------- #
# Ubiquity, stated as a measurement rather than a mood
# --------------------------------------------------------------------------- #

def ubiquity_table() -> dict[str, float]:
    """How much of the world is on a network, per era. A setting dial, not a rule.

    Acceleration is the high-water mark: almost everything is reachable, and `isolated` exists
    because someone *paid* to make it so. The crisis inverts the ratio. After it, the network is
    back but the islands stayed, which is exactly why class 1 never stops mattering.
    """
    return {
        Era.ACCELERATION.value: 0.95,
        Era.NHI_CRISIS.value: 0.55,
        Era.AFTER_CRISIS.value: 0.85,
    }


def coverage(era: Era) -> float:
    """The fraction of the world a class-2-or-better route reaches in `era` (TUNING)."""
    return ubiquity_table()[era.value]
