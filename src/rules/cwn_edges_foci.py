"""Edges and Foci: the selection contract, not the catalogue.

Original implementation of the structural rules in the Cities Without Number SRD
character-creation sections on Edges and Foci. **No Edge or Focus catalogue entry
is reproduced here.** A catalogue is commercial content; what a runtime needs is
the shape: how many you get, when you get another, how Focus levels work, and
which of the rules interact.

The interactions are where the real rules live:

* a starting character has **two Edges**, and a **third at fifth level**;
* an Edge **cannot be taken twice** unless it says so;
* a Focus is taken twice to reach **level 2**, and some Focuses have only one level;
* a new character has **one Focus**, or **two with the Focused Edge**;
* the **Underdog Rule** grants a bonus Edge to a character whose attribute
  modifiers still sum to -1 or less - and in exchange forbids raising attributes
  with skill points later in advancement.

That last one is the kind of rule that is invisible until an advancement system
quietly violates it, which is why the lock is exposed as state rather than
documented in a comment.
"""
from __future__ import annotations

from collections.abc import Iterable, Mapping
from dataclasses import dataclass, field

from .wn_core import attribute_modifier

EDGES_AT_START = 2
EDGE_LEVEL_THRESHOLD = 5
FOCI_AT_START = 1
FOCUS_LEVEL_MAX = 2
UNDERDOG_THRESHOLD = -1


class TalentRulesError(ValueError):
    """Raised when a selection is outside the rules rather than merely unusual."""


@dataclass(frozen=True)
class Edge:
    """An Edge as data: identity and the few properties the rules care about."""

    id: str
    repeatable: bool = False
    grants_bonus_focus: bool = False
    is_power: bool = False


@dataclass(frozen=True)
class Focus:
    """A Focus as data: identity, how many levels it has, and what it requires."""

    id: str
    levels: int = FOCUS_LEVEL_MAX
    requires: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        if self.levels < 1 or self.levels > FOCUS_LEVEL_MAX:
            raise TalentRulesError(f"a Focus has 1 or {FOCUS_LEVEL_MAX} levels, got {self.levels}")


@dataclass
class TalentSheet:
    """The selections a character has made, and the budget they were made against."""

    level: int = 1
    edges: list[str] = field(default_factory=list)
    focus_levels: dict[str, int] = field(default_factory=dict)
    underdog_used: bool = False

    def edge_slots(self, *, underdog_eligible: bool = False) -> int:
        """Two at start, a third at fifth level, plus one for the Underdog Rule."""
        slots = EDGES_AT_START + (1 if self.level >= EDGE_LEVEL_THRESHOLD else 0)
        if underdog_eligible and not self.underdog_used:
            slots += 1
        return slots


def attribute_modifier_total(attributes: Mapping[str, int]) -> int:
    """The sum of the six attribute modifiers, which is what the Underdog Rule tests."""
    return sum(attribute_modifier(score) for score in attributes.values())


def underdog_eligible(attributes: Mapping[str, int]) -> bool:
    """A character with a modifier total of -1 or less may claim the bonus Edge.

    The condition is checked at the *end* of character creation, so a character
    who later gains a modifier from cyberware or a new Focus does not lose an
    Edge they already took.
    """
    return attribute_modifier_total(attributes) <= UNDERDOG_THRESHOLD


def can_raise_attributes_with_skill_points(underdog_used: bool) -> bool:
    """The Underdog Rule's price: no later attribute increases from skill points."""
    return not underdog_used


def pick_edge(sheet: TalentSheet, edge: Edge, *, underdog_eligible: bool = False) -> None:
    """Spend an Edge slot.

    Duplicates are refused unless the Edge is marked repeatable, and the
    Underdog bonus is refused for magical or power Edges - the SRD excludes them
    so the rule cannot be used to buy a supernatural gift.
    """
    if edge.id in sheet.edges and not edge.repeatable:
        raise TalentRulesError(f"{edge.id} cannot be selected twice")
    if len(sheet.edges) >= sheet.edge_slots(underdog_eligible=underdog_eligible):
        raise TalentRulesError("no Edge slots remain")
    if underdog_eligible and sheet.underdog_used is False and len(sheet.edges) >= EDGES_AT_START:
        if edge.is_power:
            raise TalentRulesError("the Underdog bonus Edge cannot be a power Edge")
        sheet.underdog_used = True
    sheet.edges.append(edge.id)


def focus_slots(sheet: TalentSheet, *, has_focused_edge: bool = False) -> int:
    """One Focus at start, two with the Focused Edge."""
    return FOCI_AT_START + (1 if has_focused_edge else 0)


def pick_focus(sheet: TalentSheet, focus: Focus, *, has_focused_edge: bool = False,
               known_edges: Iterable[str] | None = None) -> int:
    """Take a Focus, or raise an existing one by a level; returns the new level.

    A Focus taken twice reaches level 2. A single-level Focus stops at 1 and a
    third selection is always refused, so no caller can quietly exceed the band.
    """
    # A requirement that names an Edge should see the character's own Edges by
    # default; the parameter exists only to check against a wider list.
    owned = set(sheet.edges if known_edges is None else known_edges)
    unknown = [requirement for requirement in focus.requires if requirement not in owned]
    if unknown:
        raise TalentRulesError(f"{focus.id} requires {unknown}")

    current = sheet.focus_levels.get(focus.id)
    if current is None:
        if len(sheet.focus_levels) >= focus_slots(sheet, has_focused_edge=has_focused_edge):
            raise TalentRulesError("no Focus slots remain")
        sheet.focus_levels[focus.id] = 1
        return 1

    if current >= focus.levels:
        raise TalentRulesError(f"{focus.id} has only {focus.levels} level(s)")
    sheet.focus_levels[focus.id] = current + 1
    return current + 1
