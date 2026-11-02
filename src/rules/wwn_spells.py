"""The WWN spell corpus as content data, plus the learning procedure the caster class left out (#1044).

Source: the **Worlds Without Number SRD** (CC0 — `data/sources/game_system_rights.json`), the spell
list and the "Learning a Spell" section. `data/rules/wwn_spells.json` carries the catalogue's
*identity* only: tradition, name, level, and an anchor to the SRD entry. Effect text is deliberately
absent, for the same reason `cwn_spells` omits it — the effect belongs in the book the player reads,
and a paraphrase in code would be a second rulebook nobody proof-reads.

What this module adds is the part that is *procedure* and was missing from `wwn_high_mage`:

* a spell can only be learned if the caster can already cast that level;
* adding a spell from a tutor, a scroll or another spellbook costs **one week per spell level, less
  one week per level of the learner's Magic skill, to a minimum of one day**;
* re-scribing a lost spellbook costs the same as learning the spell in the first place;
* a High Mage learns two spells free on each level, an Elementalist or Necromancer one.

The counts in the SRD mirror are 83 spells: 52 High Magic (13/12/11/9/7 by level), 15 Elementalist
and 16 Necromancer. An earlier note in this repository said "86 spells (21/20/18/13/11)" — that was
wrong on both the total and the per-level split, and `tests/test_wwn_spells.py` now pins the real
numbers so the claim cannot drift back.

CWN is untouched; nothing here is a CWN rule.
"""
from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path

CATALOGUE = Path(__file__).resolve().parents[2] / "data/rules/wwn_spells.json"

TRADITIONS = ("high_magic", "elementalist", "necromancer")

#: Spells a caster learns for free on gaining a level, by tradition family (SRD, Learning a Spell).
FREE_SPELLS_PER_LEVEL = {"high_mage": 2, "partial_high_mage": 2, "elementalist": 1, "necromancer": 1}

#: One day, in days, is the floor of the learning time.
MINIMUM_LEARNING_DAYS = 1


class SpellError(ValueError):
    """A rule was about to be broken: unknown spell, uncastable level, impossible time."""


@dataclass(frozen=True)
class Spell:
    id: str
    name: str
    level: int
    tradition: str

    def __post_init__(self) -> None:
        if self.tradition not in TRADITIONS:
            raise SpellError(f"unknown tradition {self.tradition!r}")
        if not 1 <= self.level <= 5:
            raise SpellError(f"{self.name}: spell levels run 1-5")


def load_catalogue(path: str | Path | None = None) -> list[Spell]:
    """Read the catalogue and refuse a duplicate id or an impossible entry."""
    data = json.loads(Path(path or CATALOGUE).read_text(encoding="utf-8"))
    spells: list[Spell] = []
    seen: set[tuple[str, str]] = set()
    for row in data["spells"]:
        spell = Spell(row["id"], row["name"], int(row["level"]), row["tradition"])
        key = (spell.tradition, spell.id)
        if key in seen:
            raise SpellError(f"duplicate spell {key}")
        seen.add(key)
        spells.append(spell)
    return spells


SPELLS: list[Spell] = load_catalogue()


def spells_of_level(level: int, tradition: str | None = None) -> list[Spell]:
    """Every spell of one level, optionally narrowed to a tradition."""
    if tradition is not None and tradition not in TRADITIONS:
        raise SpellError(f"unknown tradition {tradition!r}")
    return [s for s in SPELLS
            if s.level == level and (tradition is None or s.tradition == tradition)]


def find(name_or_id: str) -> Spell:
    """Look a spell up by id or by its printed name, case-insensitively."""
    wanted = name_or_id.strip().lower().replace(" ", "_")
    for spell in SPELLS:
        if spell.id == wanted or spell.name.lower() == name_or_id.strip().lower():
            return spell
    raise SpellError(f"unknown spell {name_or_id!r}")


def counts_by_level(tradition: str | None = None) -> dict[int, int]:
    """{level: count}; the numbers the coverage claim is checked against."""
    return {level: len(spells_of_level(level, tradition)) for level in range(1, 6)}


def can_learn(spell: Spell, max_spell_level: int) -> bool:
    """SRD: a mage must be able to cast a spell in order to learn it."""
    if max_spell_level < 1:
        raise SpellError("max_spell_level starts at 1")
    return spell.level <= max_spell_level


def learning_days(spell_level: int, magic_skill: int) -> int:
    """Days to add one spell from a tutor, scroll or another spellbook.

    One week per spell level, less one week per level of the learner's Magic skill, never below a
    single day. The floor matters: a Magic-3 caster learning a level-1 spell still spends a day, and
    a naive subtraction would make it free (or negative).
    """
    if not 1 <= spell_level <= 5:
        raise SpellError(f"spell levels run 1-5, not {spell_level}")
    if magic_skill < 0:
        raise SpellError("Magic skill cannot be negative")
    return max(MINIMUM_LEARNING_DAYS, (spell_level - magic_skill) * 7)


def rescribe_days(spell_level: int, magic_skill: int) -> int:
    """Re-creating a lost spellbook costs the same per spell as learning it, with no material cost."""
    return learning_days(spell_level, magic_skill)


def free_spells_per_level(caster: str) -> int:
    """Spells learned at no cost when a level is gained."""
    if caster not in FREE_SPELLS_PER_LEVEL:
        raise SpellError(f"unknown caster {caster!r}")
    return FREE_SPELLS_PER_LEVEL[caster]
