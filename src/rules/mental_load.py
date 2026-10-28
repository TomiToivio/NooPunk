"""Mental load as conditions on the CWN chassis (#698, D46-D48).

The mind is modelled the way the decisions say: **conditions with mechanical teeth**, not a
depleting pool. Three rules are structural here, not advisory:

* **D46 - no second harm economy.** Nothing in this module subtracts from a number. A
  condition *constrains a choice*; CWN's Trauma / Frail / Strain remain the only resources
  that deplete.
* **D47 - four layers.** An exposure moves from `observable event` to `acute response` to
  `persistent condition` to `worldview state`. The layers are separate fields because
  conflating them is how a setting ends up with "sanity points".
* **D48 - the player decides what the character believes.** There is no function here that
  takes a roll, and ``apply_choice`` refuses to run without an explicit choice. A world
  view may not be changed by a die.

No severity scale, recovery rate or condition catalogue is defined here: those are author
decisions and inventing them would pre-empt the choice the design gate protected.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum


class MentalLoadError(ValueError):
    """Raised when the model is asked to do something the decisions forbid."""


class WorldviewState(str, Enum):
    """What a character currently holds about a claim, not what is true."""

    RECEIVED = "received"      # taken as given; never questioned
    CRACKED = "cracked"        # contradicted, not yet resolved
    REFRAMED = "reframed"      # the belief was revised to include the evidence
    INTEGRATED = "integrated"  # revised and lived with; no longer destabilising
    FRACTURED = "fractured"    # held anyway, at a cost that persists


class Layer(str, Enum):
    EVENT = "observable_event"
    ACUTE = "acute_response"
    PERSISTENT = "persistent_condition"
    WORLDVIEW = "worldview"


@dataclass(frozen=True)
class Condition:
    """A persistent condition. ``constrains`` is fiction, not a modifier.

    ``clears_when`` is prose on purpose: the recovery rule is the author's to set, and a
    number invented here would silently become canon.
    """

    id: str
    layer: Layer
    constrains: str
    clears_when: str = ""

    def __post_init__(self) -> None:
        if not self.id:
            raise MentalLoadError("a condition needs an id")
        if self.layer is Layer.EVENT:
            raise MentalLoadError("an observable event is not a condition")


@dataclass(frozen=True)
class ParadigmShock:
    """A dated, sourced event that contradicts a held belief.

    The shock is a property of the setting's exposure, not of a character's roll.
    """

    id: str
    claim: str
    contradicts: str
    source: str = ""


@dataclass(frozen=True)
class ShockChoice:
    """The two ways a shock can be met. Neither is correct; they cost differently."""

    shock_id: str
    claim: str
    accept: Condition
    hold: Condition


@dataclass
class CharacterMind:
    """A character's worldview states and the conditions they carry."""

    worldviews: dict[str, WorldviewState] = field(default_factory=dict)
    conditions: list[Condition] = field(default_factory=list)

    def state_of(self, claim: str) -> WorldviewState:
        return self.worldviews.get(claim, WorldviewState.RECEIVED)

    def present(self, shock: ParadigmShock) -> ShockChoice:
        """Offer the two costs. This function decides nothing on the character's behalf."""
        if not shock.id or not shock.contradicts:
            raise MentalLoadError("a shock needs an id and a contradicted claim")
        current = self.state_of(shock.contradicts)
        if current in (WorldviewState.INTEGRATED,):
            raise MentalLoadError(
                f"{shock.contradicts} is already integrated; this shock is not destabilising"
            )
        accept = Condition(
            id=f"{shock.id}:reframe",
            layer=Layer.PERSISTENT,
            constrains="the character must act on the revised belief, not the old one",
            clears_when="the revision has been lived with through a scene of consequence",
        )
        hold = Condition(
            id=f"{shock.id}:denial",
            layer=Layer.PERSISTENT,
            constrains="the character must explain away or avoid the evidence",
            clears_when="the character states the old belief aloud under pressure",
        )
        return ShockChoice(shock_id=shock.id, claim=shock.contradicts, accept=accept, hold=hold)

    def apply_choice(self, choice: ShockChoice, *, accept: bool) -> WorldviewState:
        """Record a decision the player made. There is no random input, by design.

        ``accept=True`` revises the belief (reformed, then integrated on a second scene of
        consequence); ``accept=False`` holds it and marks the worldview fractured.
        """
        if not isinstance(accept, bool):
            raise MentalLoadError("accept must be an explicit player decision, not a roll")
        condition = choice.accept if accept else choice.hold
        self.conditions.append(condition)
        state = WorldviewState.REFRAMED if accept else WorldviewState.FRACTURED
        self.worldviews[choice.claim] = state
        return state

    def integrate(self, claim: str) -> WorldviewState:
        """Second step of the acceptance path: lived with, no longer destabilising."""
        if self.state_of(claim) is not WorldviewState.REFRAMED:
            raise MentalLoadError("only a reframed worldview can be integrated")
        self.worldviews[claim] = WorldviewState.INTEGRATED
        return WorldviewState.INTEGRATED



def no_roll_parameter(func) -> bool:  # pragma: no cover - documentation helper
    """Guards the D48 invariant when reviewing additions to this module."""
    import inspect

    return not any(
        name in inspect.signature(func).parameters
        for name in ("roll", "die", "dice", "rng", "random")
    )
