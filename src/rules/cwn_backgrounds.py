"""Backgrounds and Contacts: the contract, not the tables.

Original implementation of the structural rules in the Cities Without Number SRD
character-creation sections on Backgrounds and Contacts. **No background table,
skill list or name list is reproduced.** The d20 background list, its Growth and
Learning tables and the contact suggestion tables are content; what a runtime
needs is the shape of the choices and the arithmetic around them.

The rules that are easy to get wrong, and therefore live here:

* a Background immediately grants **its free skill at level-0**;
* after that the player picks a route: **three rolls split between Growth and
  Learning in any proportion**, or **two specific picks from the Learning table**;
* a specific route **may take the same skill twice** to reach level-1, but may
  **not** take the "Any Skill" option;
* "Any Combat" resolves to Shoot, Stab or Punch;
* an attribute bonus may be **split between two attributes of the same kind**,
  and **no attribute may exceed 18**;
* a new character has **two acquaintances or one friend**, never a mix.

Dice enter as values so a table roll and a replay agree.
"""
from __future__ import annotations

from collections.abc import Sequence
from dataclasses import dataclass, field

ATTRIBUTE_CEILING = 18
PHYSICAL = ("Strength", "Dexterity", "Constitution")
MENTAL = ("Intelligence", "Wisdom", "Charisma")
ANY_COMBAT = ("Shoot", "Stab", "Punch")
GROWTH_ROLLS = 3
LEARNING_PICKS = 2


class BackgroundRulesError(ValueError):
    """Raised when a call is outside the creation procedure."""


# --------------------------------------------------------------------------- #
# What a table entry can do
# --------------------------------------------------------------------------- #

@dataclass(frozen=True)
class SkillPick:
    """A named skill on a background table."""

    skill: str


@dataclass(frozen=True)
class AnyCombat:
    """The table's "Any Combat" entry: the player names Shoot, Stab or Punch."""


@dataclass(frozen=True)
class AnySkill:
    """The table's "Any Skill" entry - excluded from the specific-pick route."""


@dataclass(frozen=True)
class AttributeBonus:
    """``+2 Physical`` and friends: a size and which attributes may receive it."""

    amount: int
    kind: str  # "Physical", "Mental" or "Any"

    def allowed_attributes(self) -> tuple[str, ...]:
        if self.kind == "Physical":
            return PHYSICAL
        if self.kind == "Mental":
            return MENTAL
        if self.kind == "Any":
            return PHYSICAL + MENTAL
        raise BackgroundRulesError(f"unknown attribute bonus kind {self.kind!r}")


@dataclass(frozen=True)
class Background:
    """One background row: its free skill and its two tables."""

    id: str
    free_skill: str
    learning: tuple[object, ...] = ()
    growth: tuple[object, ...] = ()

    def __post_init__(self) -> None:
        if not self.free_skill:
            raise BackgroundRulesError("a background needs its free skill")
        if not self.growth or not self.learning:
            raise BackgroundRulesError("a background needs both tables")
        # A plain string on a table is a skill name. Normalising here keeps every
        # row the same type, so callers do not have to test for strings.
        object.__setattr__(self, "learning", tuple(_as_entry(e) for e in self.learning))
        object.__setattr__(self, "growth", tuple(_as_entry(e) for e in self.growth))


def _as_entry(entry: object) -> object:
    return SkillPick(entry) if isinstance(entry, str) else entry


# --------------------------------------------------------------------------- #
# Choosing
# --------------------------------------------------------------------------- #

def grant_free_skill(background: Background, pool) -> int:
    """The free skill arrives at level-0 before any other choice is made."""
    return pool.pick(background.free_skill)


def specific_picks(background: Background, picks: Sequence[str], pool) -> list[int]:
    """Two picks from the Learning table, the same skill twice allowed.

    "Any Skill" is not a legal specific pick: it is an instruction to roll, not
    a choice, and the SRD excludes it on this route.
    """
    if len(picks) != LEARNING_PICKS:
        raise BackgroundRulesError(f"expected {LEARNING_PICKS} picks, got {len(picks)}")
    allowed = {entry.skill for entry in background.learning if isinstance(entry, SkillPick)}
    for skill in picks:
        if skill not in allowed:
            raise BackgroundRulesError(f"{skill!r} is not on this background's Learning table")
    return [pool.pick(skill) for skill in picks]


def growth_rolls(background: Background, rolls: Sequence[tuple[str, int]]) -> list[object]:
    """Three rolls, each naming its table and its die result.

    The split is free - all three may come from one table - because the SRD lets
    the player divide them in any way they wish.
    """
    if len(rolls) != GROWTH_ROLLS:
        raise BackgroundRulesError(f"expected {GROWTH_ROLLS} rolls, got {len(rolls)}")
    results: list[object] = []
    for table_name, die in rolls:
        table = background.growth if table_name == "growth" else (
            background.learning if table_name == "learning" else None)
        if table is None:
            raise BackgroundRulesError(f"unknown table {table_name!r}")
        results.append(resolve_table_entry(table, die))
    return results


def resolve_table_entry(table: Sequence[object], die: int) -> object:
    """A d20 result indexes the table; out-of-range results are refused, not clamped.

    A background table has as many rows as its author gave it, and inventing a
    row for an impossible roll would silently change the odds.
    """
    if not 1 <= die <= len(table):
        raise BackgroundRulesError(f"a roll of {die} is outside a table of {len(table)} rows")
    return table[die - 1]


def apply_attribute_bonus(
    bonus: AttributeBonus,
    attributes: dict[str, int],
    allocation: Sequence[tuple[str, int]],
) -> dict[str, int]:
    """Apply ``+N Physical`` and friends, splitting between attributes of that kind.

    No attribute may be raised above 18, and a split that would do so is refused
    outright rather than quietly trimmed - the player should re-allocate.
    """
    if sum(amount for _, amount in allocation) != bonus.amount:
        raise BackgroundRulesError("the allocation must spend the whole bonus")
    allowed = bonus.allowed_attributes()
    result = dict(attributes)
    for attribute, amount in allocation:
        if attribute not in allowed:
            raise BackgroundRulesError(f"{attribute} is not a legal target for a {bonus.kind} bonus")
        if amount < 0:
            raise BackgroundRulesError("a bonus cannot be negative")
        raised = result[attribute] + amount
        if raised > ATTRIBUTE_CEILING:
            raise BackgroundRulesError(f"{attribute} would exceed {ATTRIBUTE_CEILING}")
        result[attribute] = raised
    return result


# --------------------------------------------------------------------------- #
# Contacts
# --------------------------------------------------------------------------- #

ACQUAINTANCE = "acquaintance"
FRIEND = "friend"


@dataclass(frozen=True)
class Contact:
    """A contact, at one of the two levels the SRD recognises."""

    name: str
    level: str = ACQUAINTANCE

    def __post_init__(self) -> None:
        if not self.name:
            raise BackgroundRulesError("a contact needs a name")
        if self.level not in (ACQUAINTANCE, FRIEND):
            raise BackgroundRulesError(f"unknown contact level {self.level!r}")


@dataclass
class ContactBook:
    """Starting contacts: two acquaintances *or* one friend, and never a mix."""

    contacts: list[Contact] = field(default_factory=list)

    def __post_init__(self) -> None:
        self._validate()

    def _validate(self) -> None:
        friends = [c for c in self.contacts if c.level == FRIEND]
        acquaintances = [c for c in self.contacts if c.level == ACQUAINTANCE]
        if friends and acquaintances:
            raise BackgroundRulesError("starting contacts are either two acquaintances or one friend")
        if len(friends) > 1:
            raise BackgroundRulesError("a starting character has at most one friend")
        if len(acquaintances) > 2:
            raise BackgroundRulesError("a starting character has at most two acquaintances")

    def add(self, contact: Contact) -> None:
        self.contacts.append(contact)
        try:
            self._validate()
        except BackgroundRulesError:
            self.contacts.pop()
            raise

    def promote(self, name: str) -> None:
        """An acquaintance can become a friend; the book must still be legal."""
        for index, contact in enumerate(self.contacts):
            if contact.name == name:
                self.contacts[index] = Contact(name=contact.name, level=FRIEND)
                try:
                    self._validate()
                except BackgroundRulesError:
                    self.contacts[index] = contact
                    raise
                return
        raise BackgroundRulesError(f"no contact named {name!r}")
