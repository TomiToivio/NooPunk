"""WWN High Mage, reskinned as NoöPunk's hermetic / ritual PSI practitioner (#1044).

Source: the **Worlds Without Number SRD** (CC0 — see ``data/sources/game_system_rights.json``), tables
for the High Mage and Partial High Mage traditions plus the spell-preparation and casting rules. The
numbers here are the SRD's own; the prose is not reproduced. Where a rule needs a sentence of
explanation, it is paraphrased and the table/page it comes from is named in the docstring.

Why this class and not a bespoke caster: the setting premise is *"magick is psionics; psionics is
magick"*, which is an interpretation, not a licence to invent mechanics. So the chassis is WWN's
High Mage exactly — Magic skill, spell levels, prepared slots, casts per day, Arts and their Effort —
and only the *naming* is NoöPunk: a spell is a ritual working, an Art is a trained noetic reflex, and
Effort is commitment of attention. Factions and characters may disagree in-world about whether this
is magic or psi; the rules do not care, and nothing here is duplicated from ``swn_psionics``
(SWN psychic Effort is a **separate pool** — see :data:`POOL`).

Deliberate absences: no spell effect text (the SRD spell list is a catalogue of effects that belong in
content data, not in the rule module), no combat integration, no CWN skill changes.
"""
from __future__ import annotations

import json
from dataclasses import dataclass, field
from enum import Enum

#: The Effort pool this class draws from. Kept explicit so nothing can spend an SWN psychic's Effort
#: (``rules.swn_psionics.Psychic``) on a High Magic spell or the other way round: the SRD states each
#: Effort-using class has its own pool and that points cannot be transferred between them.
POOL = "high_mage"

#: Full High Mage (SRD, High Mage Arts and Spells): level -> (max spell level, spells cast/day,
#: spells prepared, arts gained at that level).
HIGH_MAGE_TABLE: dict[int, tuple[int, int, int, int]] = {
    1: (1, 1, 3, 2),
    2: (1, 1, 3, 1),
    3: (2, 2, 4, 0),
    4: (2, 2, 5, 1),
    5: (3, 3, 6, 0),
    6: (3, 3, 7, 1),
    7: (4, 4, 8, 0),
    8: (4, 4, 9, 1),
    9: (5, 5, 10, 0),
    10: (5, 6, 12, 1),
}

#: Partial High Mage (SRD, same section — its own table, not a halved full mage).
PARTIAL_HIGH_MAGE_TABLE: dict[int, tuple[int, int, int, int]] = {
    1: (1, 1, 2, 1),
    2: (1, 1, 3, 1),
    3: (1, 1, 3, 1),
    4: (1, 2, 4, 0),
    5: (2, 2, 5, 0),
    6: (2, 3, 6, 1),
    7: (2, 3, 7, 0),
    8: (2, 3, 7, 0),
    9: (3, 4, 8, 1),
    10: (3, 4, 9, 0),
}

#: SRD: learning a spell requires being able to cast it, so the repertoire is gated by level.
SPELLS_LEARNED_PER_LEVEL = {"full": 2, "partial": 2}


class HighMageError(ValueError):
    pass


class Duration(str, Enum):
    """How long committed Effort stays tied up (SRD, Committing Effort)."""

    DURATION = "duration"   # until the caster reclaims it
    TURN = "turn"           # until the end of the Turn, not reclaimable earlier
    DAY = "day"             # until a comfortable night's rest


@dataclass(frozen=True)
class Art:
    """A High Mage Art. ``note`` paraphrases what the Art does; effects are not rulebook text."""

    identifier: str
    name: str
    duration: Duration
    note: str
    instant: bool = False
    once_per: str = ""


#: The fourteen SRD High Mage Arts. Costs are the SRD's durations; ``once_per`` records the ones the
#: book caps (once per round / Turn / day), because a cap nobody enforces is not a rule.
ARTS: dict[str, Art] = {
    "arcane_lexicon": Art("arcane_lexicon", "Arcane Lexicon", Duration.TURN,
                          "read any script not deliberately encoded"),
    "counter_magic": Art("counter_magic", "Counter Magic", Duration.DAY,
                         "opposed Int/Magic or Cha/Magic check to fizzle a visible mage's spell",
                         instant=True, once_per="round"),
    "empowered_sorcery": Art("empowered_sorcery", "Empowered Sorcery", Duration.DAY,
                             "re-roll one variable die of a spell's effect, keep the better",
                             instant=True),
    "hang_sorcery": Art("hang_sorcery", "Hang Sorcery", Duration.TURN,
                        "hold a cast spell ready to release later; no other casting meanwhile",
                        instant=True),
    "inexorable_effect": Art("inexorable_effect", "Inexorable Effect", Duration.DAY,
                             "force an enemy to re-roll a successful save, worse result",
                             instant=True, once_per="turn"),
    "iron_resolution": Art("iron_resolution", "Iron Resolution", Duration.DAY,
                           "Physical save to ignore injury for concentration", instant=True),
    "preparatory_countermagic": Art("preparatory_countermagic", "Preparatory Countermagic",
                                    Duration.TURN, "shrug off a spell you have prepared",
                                    instant=True),
    "psychic_conversion": Art("psychic_conversion", "Psychic Conversion", Duration.DAY,
                              "spend a casting slot to clear 1 System Strain and heal 2/level",
                              instant=False, once_per="day"),
    "restrained_casting": Art("restrained_casting", "Restrained Casting", Duration.DAY,
                              "cast silently and without gestures", instant=True),
    "retain_sorcery": Art("retain_sorcery", "Retain Sorcery", Duration.DAY,
                          "a cast spell does not count against the daily limit",
                          instant=False, once_per="day"),
    "sense_magic": Art("sense_magic", "Sense Magic", Duration.DURATION,
                       "see magical energy and read one sentence about any standing effect",
                       instant=True),
    "suppress_magic": Art("suppress_magic", "Suppress Magic", Duration.DAY,
                          "suppress one known effect for 1d6 rounds + level", instant=False),
    "swift_casting": Art("swift_casting", "Swift Casting", Duration.DAY,
                         "turn a Main Action spell into a Free action", instant=False,
                         once_per="turn"),
    "ward_allies": Art("ward_allies", "Ward Allies", Duration.DAY,
                       "omit up to six allies from your area spell", instant=True),
    "wizards_grandeur": Art("wizards_grandeur", "Wizard's Grandeur", Duration.DURATION,
                            "stay clean, comfortable and presentable regardless of conditions"),
}


@dataclass(frozen=True)
class Spell:
    """A ritual working known to the practitioner. Only identity and level live here."""

    identifier: str
    name: str
    level: int

    def __post_init__(self) -> None:
        if not self.identifier or not self.name:
            raise HighMageError("a spell needs an id and a name")
        if type(self.level) is not int or not 1 <= self.level <= 5:
            raise HighMageError("spell levels run 1..5")


def effort_max(magic_skill: int, intelligence_modifier: int, charisma_modifier: int,
               *, partial: bool = False) -> int:
    """SRD: 1 + Magic skill + the better of Int or Cha, minimum 1; a Partial High Mage has one less."""
    if min(magic_skill, intelligence_modifier, charisma_modifier) < -3 or magic_skill > 6:
        raise HighMageError("attribute and skill values are out of range")
    total = 1 + magic_skill + max(intelligence_modifier, charisma_modifier)
    if partial:
        total -= 1
    return max(1, total)


@dataclass
class HighMage:
    """One practitioner's daily state: repertoire, preparations, castings, committed Effort.

    Nothing here is CWN state: CWN skills, saves and advancement are untouched, and the class is an
    additive package a CWN character carries (``partial=True`` for the Partial High Mage package).
    """

    level: int = 1
    magic_skill: int = 0
    intelligence_modifier: int = 0
    charisma_modifier: int = 0
    partial: bool = False
    repertoire: dict[str, Spell] = field(default_factory=dict)
    prepared: list[str] = field(default_factory=list)
    arts: list[str] = field(default_factory=list)
    casts_used: int = 0
    committed: dict[str, Duration] = field(default_factory=dict)
    rested: bool = True
    once_used: dict[str, int] = field(default_factory=dict)
    turn: int = 1

    def __post_init__(self) -> None:
        if type(self.level) is not int or not 1 <= self.level <= 10:
            raise HighMageError("level runs 1..10")
        for art in self.arts:
            if art not in ARTS:
                raise HighMageError(f"unknown art {art!r}")
        for key in self.prepared:
            if key not in self.repertoire:
                raise HighMageError(f"prepared spell {key!r} is not in the repertoire")

    # -- table lookups ---------------------------------------------------------------
    @property
    def _row(self) -> tuple[int, int, int, int]:
        return (PARTIAL_HIGH_MAGE_TABLE if self.partial else HIGH_MAGE_TABLE)[self.level]

    @property
    def max_spell_level(self) -> int:
        return self._row[0]

    @property
    def casts_per_day(self) -> int:
        return self._row[1]

    @property
    def prepared_slots(self) -> int:
        return self._row[2]

    @property
    def arts_allowed(self) -> int:
        table = PARTIAL_HIGH_MAGE_TABLE if self.partial else HIGH_MAGE_TABLE
        return sum(table[level][3] for level in range(1, self.level + 1))

    @property
    def casts_left(self) -> int:
        return max(0, self.casts_per_day - self.casts_used)

    # -- Effort ----------------------------------------------------------------------
    @property
    def effort(self) -> int:
        return effort_max(self.magic_skill, self.intelligence_modifier, self.charisma_modifier,
                          partial=self.partial)

    @property
    def effort_committed(self) -> int:
        return len(self.committed)

    @property
    def effort_free(self) -> int:
        return max(0, self.effort - self.effort_committed)

    def commit(self, art: str) -> Duration:
        """Commit one point of Effort to an Art (the SRD: one point unless the power says otherwise)."""
        if art not in ARTS:
            raise HighMageError(f"unknown art {art!r}")
        if art not in self.arts:
            raise HighMageError(f"{ARTS[art].name} is not among this practitioner's arts")
        if art in self.committed:
            raise HighMageError(f"{ARTS[art].name} is already active")
        if self.effort_free < 1:
            raise HighMageError("no Effort left to commit")
        cap = ARTS[art].once_per
        if cap and self.once_used.get(f"{art}:{cap}", 0) >= 1:
            raise HighMageError(f"{ARTS[art].name} is once per {cap}")
        self.committed[art] = ARTS[art].duration
        if cap:
            self.once_used[f"{art}:{cap}"] = self.once_used.get(f"{art}:{cap}", 0) + 1
        return ARTS[art].duration

    def release(self, art: str) -> bool:
        """Reclaim Effort committed *for the duration*; Turn and day Effort cannot be taken back."""
        duration = self.committed.get(art)
        if duration is None:
            return False
        if duration is not Duration.DURATION:
            raise HighMageError(f"{ARTS[art].name} was committed for the {duration.value} "
                                "and cannot be reclaimed early")
        del self.committed[art]
        return True

    def end_turn(self) -> None:
        """Turn-bound Effort returns; round- and turn-capped Arts become available again."""
        for art, duration in list(self.committed.items()):
            if duration is Duration.TURN:
                del self.committed[art]
        for key in [k for k in self.once_used if k.endswith((":round", ":turn"))]:
            del self.once_used[key]
        self.turn += 1

    def rest(self, *, comfortable: bool = True) -> None:
        """A comfortable night returns day-bound Effort, all castings and the ability to prepare."""
        if not comfortable:
            raise HighMageError("day Effort needs a comfortable night's rest")
        for art, duration in list(self.committed.items()):
            if duration is Duration.DAY:
                del self.committed[art]
        self.casts_used = 0
        self.rested = True
        self.once_used = {k: v for k, v in self.once_used.items() if not k.endswith(":day")}

    # -- repertoire and preparation ---------------------------------------------------
    def learn(self, spell: Spell) -> None:
        """SRD: a mage must be able to cast a spell to learn it."""
        if spell.level > self.max_spell_level:
            raise HighMageError(f"level {self.level} cannot learn level {spell.level} spells")
        if spell.identifier in self.repertoire:
            raise HighMageError(f"{spell.name} is already in the repertoire")
        self.repertoire[spell.identifier] = spell

    def prepare(self, spell_ids: list[str]) -> list[str]:
        """Prepare the day's spells: one hour, after a night's rest, and never more than the slots."""
        if not self.rested:
            raise HighMageError("preparation needs a good night's rest first")
        if len(spell_ids) > self.prepared_slots:
            raise HighMageError(f"{self.prepared_slots} prepared slots at level {self.level}")
        chosen: list[str] = []
        for key in spell_ids:
            spell = self.repertoire.get(key)
            if spell is None:
                raise HighMageError(f"{key!r} is not in the repertoire")
            if spell.level > self.max_spell_level:
                raise HighMageError(f"{spell.name} is above this level's maximum")
            chosen.append(key)
        self.prepared = chosen
        self.rested = False
        return list(self.prepared)

    def add_art(self, art: str) -> None:
        if art not in ARTS:
            raise HighMageError(f"unknown art {art!r}")
        if art in self.arts:
            raise HighMageError(f"{ARTS[art].name} is already known")
        if len(self.arts) >= self.arts_allowed:
            raise HighMageError(f"level {self.level} allows {self.arts_allowed} arts")
        self.arts.append(art)

    # -- casting ---------------------------------------------------------------------
    def can_cast(self, *, armored: bool = False, shielded: bool = False,
                 damaged_this_round: bool = False) -> bool:
        """SRD casting preconditions: no armour or shield, and no damage in the round."""
        return not (armored or shielded or damaged_this_round) and self.casts_left > 0

    def cast(self, spell_id: str, *, armored: bool = False, shielded: bool = False,
             damaged_this_round: bool = False, retain: bool = False) -> dict:
        """Cast a prepared spell. Returns the audited record; raises rather than silently no-op'ing."""
        if armored or shielded:
            raise HighMageError("spells and arts cannot be cast in armour, restrictive clothing "
                                "or with a shield")
        if damaged_this_round:
            raise HighMageError("damage in the round spoiled the concentration")
        spell = self.repertoire.get(spell_id)
        if spell is None or spell_id not in self.prepared:
            raise HighMageError(f"{spell_id!r} is not prepared")
        if spell.level > self.max_spell_level:
            raise HighMageError(f"{spell.name} is above this level's maximum")
        if self.casts_left < 1 and not retain:
            raise HighMageError("no castings left today")
        if retain:
            if self.once_used.get("retain_sorcery:day"):
                raise HighMageError("Retain Sorcery is once per day")
            self.once_used["retain_sorcery:day"] = 1
        else:
            self.casts_used += 1
        return {"turn": self.turn, "spell": spell.identifier, "level": spell.level,
                "castings_left": self.casts_left, "retained": retain}

    # -- persistence -------------------------------------------------------------------
    def snapshot(self) -> dict:
        return {"schema": 1, "level": self.level, "magic_skill": self.magic_skill,
                "intelligence_modifier": self.intelligence_modifier,
                "charisma_modifier": self.charisma_modifier, "partial": self.partial,
                "repertoire": {k: vars(v) for k, v in self.repertoire.items()},
                "prepared": list(self.prepared), "arts": list(self.arts),
                "casts_used": self.casts_used,
                "committed": {k: v.value for k, v in self.committed.items()},
                "rested": self.rested, "once_used": dict(self.once_used), "turn": self.turn}

    def to_json(self) -> str:
        return json.dumps(self.snapshot(), indent=2)

    @classmethod
    def from_json(cls, text: str) -> HighMage:
        state = json.loads(text)
        if state.get("schema") != 1:
            raise HighMageError(f"unsupported schema {state.get('schema')!r}")
        mage = cls(level=state["level"], magic_skill=state["magic_skill"],
                   intelligence_modifier=state["intelligence_modifier"],
                   charisma_modifier=state["charisma_modifier"], partial=state["partial"],
                   repertoire={k: Spell(**v) for k, v in state["repertoire"].items()},
                   prepared=list(state["prepared"]), arts=list(state["arts"]),
                   casts_used=state["casts_used"],
                   committed={k: Duration(v) for k, v in state["committed"].items()},
                   rested=state["rested"], once_used=dict(state["once_used"]),
                   turn=state["turn"])
        return mage
