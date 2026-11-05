"""Deferred psionics work carried from #1178 into #1196.

Six items were deferred. Four can be built **without transcribing a rulebook**, because they are
structural constraints rather than numbers:

* the **Mutant** Edge is a PC option with Europol approval; mutation, ancestry and PSI remain independent
* **Mentalist / Spellcaster / Summoner** may not smuggle in an unrestricted SWN discipline (#1196 §3)
* a **device grant** lives and dies with the device that grants it (#1196 §4)
* the **Psychic Training Focus** cannot exist in code until somebody has quoted the book (#1196 §5)

The other two are deliberately not here: an Astral graph waits for a scene that needs navigation
(#1196 §1), and the Focus's *effects* are printed rules, not structure.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

try:  # see src/world/scenes.py for why the repository supports both import roots
    from src.rules.psi_access import (
        PC_DISCIPLINES,
        Grant,
        PsiAccessError,
        discipline_decision,
        edge_decision,
    )
    from src.rules.swn_psionics import DISCIPLINES, Psychic
except ModuleNotFoundError:  # pragma: no cover
    from rules.psi_access import (  # type: ignore[no-redef]
        PC_DISCIPLINES,
        Grant,
        PsiAccessError,
        discipline_decision,
        edge_decision,
    )
    from rules.swn_psionics import DISCIPLINES, Psychic  # type: ignore[no-redef]


class PsiEdgeError(ValueError):
    """A psionic Edge, template or grant breaks a structural rule."""


# --------------------------------------------------------------------------- #
# Evidence: nothing enters the game without a citation (#1196 §2, §5)
# --------------------------------------------------------------------------- #

@dataclass(frozen=True, slots=True)
class Citation:
    """A quotation from an authorised book, with the page it came from.

    This exists because the repository refuses to transcribe rules from memory. A citation is not
    decoration: an entry cannot be constructed without a non-empty quote, so a table that was
    "remembered" cannot be passed off as a table that was read.
    """

    source: str
    page: str
    quote: str

    def __post_init__(self) -> None:
        for field_name in ("source", "page", "quote"):
            value = getattr(self, field_name)
            if not isinstance(value, str) or not value.strip():
                raise PsiEdgeError(f"a citation needs a non-empty {field_name}")


# --------------------------------------------------------------------------- #
# §5 Psychic Training Focus — structure only, gated on a citation
# --------------------------------------------------------------------------- #

#: False until the Focus's level benefits have been quoted in. Kept next to
#: ``psi_access.PSYCHIC_TRAINING_FOCUS_AVAILABLE`` so the two cannot drift silently.
PSYCHIC_TRAINING_FOCUS_AVAILABLE = False


@dataclass(frozen=True, slots=True)
class FocusLevel:
    """One level's benefit, exactly as printed, with its citation."""

    level: int
    benefit: str
    citation: Citation

    def __post_init__(self) -> None:
        if not isinstance(self.level, int) or self.level < 1:
            raise PsiEdgeError("a Focus level is a positive integer")
        if not self.benefit.strip():
            raise PsiEdgeError("a Focus level needs its printed benefit")


@dataclass(frozen=True, slots=True)
class PsychicTrainingFocus:
    """The Focus as a *structure*: ordered levels, each quoting the book.

    The class deliberately has no defaults and no formulas. Whoever implements the real Focus fills
    the levels from the authorised edition; until then this object cannot be built, because every
    level demands a quote that does not exist yet.
    """

    discipline: str
    levels: tuple[FocusLevel, ...]

    def __post_init__(self) -> None:
        if self.discipline not in PC_DISCIPLINES:
            raise PsiEdgeError(
                f"a player character's Focus stays inside {PC_DISCIPLINES}; "
                f"{self.discipline!r} is not a player discipline"
            )
        if not self.levels:
            raise PsiEdgeError("a Focus needs at least one level")
        numbers = [level.level for level in self.levels]
        if len(set(numbers)) != len(numbers):
            raise PsiEdgeError("duplicate Focus level")
        if numbers != sorted(numbers):
            raise PsiEdgeError("Focus levels must be given in order")
        if any(level.citation.source.strip() == "" for level in self.levels):
            raise PsiEdgeError("every Focus level must cite its source")

    def benefit_at(self, level: int) -> str:
        for entry in self.levels:
            if entry.level == level:
                return entry.benefit
        raise PsiEdgeError(f"no level {level} in this Focus")


# --------------------------------------------------------------------------- #
# §3 Mentalist / Spellcaster / Summoner
# --------------------------------------------------------------------------- #

#: Where each selectable Edge comes from. A name outside this map is refused rather than assumed.
EDGE_SOURCES: dict[str, str] = {
    "Mutant": "Ashes Without Number",
    "Mentalist": "Ashes Without Number",
    "Spellcaster": "Cities Without Number",
    "Summoner": "Cities Without Number",
}

#: Resource a character spends to use the Edge. ``psi`` means the SWN Effort pool.
EDGE_RESOURCES: tuple[str, ...] = ("psi", "cwn_effort", "none")


@dataclass(frozen=True, slots=True)
class EdgeGrants:
    """What taking an Edge actually gives a character, expressed in facts we can check."""

    edge: str
    disciplines: tuple[str, ...] = ()
    resource: str = "none"
    grants_technique_progress: bool = False

    def __post_init__(self) -> None:
        if self.edge not in EDGE_SOURCES:
            raise PsiEdgeError(
                f"{self.edge!r} is not a selectable Edge; known: {', '.join(EDGE_SOURCES)}"
            )
        if self.resource not in EDGE_RESOURCES:
            raise PsiEdgeError(f"unknown Edge resource {self.resource!r}")
        for discipline in self.disciplines:
            if discipline not in DISCIPLINES:
                raise PsiEdgeError(f"{discipline!r} is not an SWN discipline")


def validate_edge(
    grants: EdgeGrants, *, psychic: Psychic | None = None, existing: Iterable[EdgeGrants] = ()
) -> list[str]:
    """Return every structural problem with taking this Edge. Empty list means admissible.

    The rule the issue names is the last one: *no combination produces a second progress track for
    the same power.* Two Edges that both advance psionic technique progress is that bug.
    """
    problems: list[str] = []
    # The Edge must be one a player character may take at all.
    decision = edge_decision(grants.edge)
    if not decision.allowed:
        problems.append(decision.reason)

    if grants.edge == "Mentalist" and psychic is not None:
        problems.append("AWN Mentalist cannot combine with SWN Psychic, full or partial (AWN Deluxe p.265)")
    if grants.edge == "Mentalist" and any(e.edge in ("Spellcaster", "Summoner") for e in existing):
        problems.append("AWN Mentalist cannot combine with CWN Mage/Spellcaster or Summoner (AWN Deluxe p.265)")
    if grants.edge in ("Spellcaster", "Summoner") and any(e.edge == "Mentalist" for e in existing):
        problems.append("CWN Mage/Summoner cannot combine with AWN Mentalist (AWN Deluxe p.265)")
    for discipline in grants.disciplines:
        allowed = discipline_decision(discipline)
        if not allowed.allowed:
            problems.append(
                f"{grants.edge} may not grant {discipline}: {allowed.reason}"
            )
        if psychic is not None and psychic.restricted_discipline:
            if discipline != psychic.restricted_discipline:
                problems.append(
                    f"{grants.edge} would grant {discipline}, but this Partial Psychic is "
                    f"restricted to {psychic.restricted_discipline}"
                )

    if psychic is not None and grants.resource == "psi" and grants.grants_technique_progress:
        problems.append(
            f"{grants.edge} would add a second psionic progress track alongside the Psychic class"
        )

    for other in existing:
        if other.edge == grants.edge:
            problems.append(f"{grants.edge} is already taken")
        shared = set(other.disciplines) & set(grants.disciplines)
        if shared:
            problems.append(
                f"{grants.edge} and {other.edge} both advance {', '.join(sorted(shared))}"
            )
        if (other.grants_technique_progress and grants.grants_technique_progress
                and other.resource == grants.resource == "psi"):
            problems.append(
                f"{grants.edge} and {other.edge} would each own psionic technique progress"
            )
    return problems


# --------------------------------------------------------------------------- #
# §4 Device-granted psionic effects
# --------------------------------------------------------------------------- #

def active_grants(
    carried_devices: Iterable[str], grants: Iterable[Grant]
) -> tuple[Grant, ...]:
    """The grants currently in force, given what the character is carrying.

    A psychotronic implant works while it is worn. Taking it off is not a rule change, it is the end
    of the grant — and a grant can never be turned into a selectable option, which ``Grant`` already
    enforces at construction.
    """
    carried = {device for device in carried_devices if device and device.strip()}
    return tuple(grant for grant in grants if grant.source in carried)


def require_device(grants: Iterable[Grant], device: str) -> tuple[Grant, ...]:
    """The grants a named device provides, refusing the call if it provides none."""
    selected = tuple(g for g in grants if g.source == device)
    if not selected:
        raise PsiEdgeError(f"{device!r} grants nothing")
    return selected


# --------------------------------------------------------------------------- #
# §2 Mutant — PC or NPC, and three independent facts
# --------------------------------------------------------------------------- #

@dataclass(frozen=True, slots=True)
class MutationEntry:
    """One mutation, exactly as printed, with its citation."""

    id: str
    effect: str
    citation: Citation

    def __post_init__(self) -> None:
        if not self.id.strip() or not self.effect.strip():
            raise PsiEdgeError("a mutation needs an id and its printed effect")


class MutationCatalogue:
    """The mutations a Mutant template may draw on.

    Empty until somebody transcribes the published tables. An empty catalogue is the honest state:
    a Mutant NPC built against it fails loudly instead of acquiring a mutation nobody can point to
    in a book.
    """

    def __init__(self, entries: Iterable[MutationEntry] = ()) -> None:
        self._entries: dict[str, MutationEntry] = {}
        for entry in entries:
            self.add(entry)

    def add(self, entry: MutationEntry) -> MutationEntry:
        if entry.id in self._entries:
            raise PsiEdgeError(f"duplicate mutation {entry.id!r}")
        self._entries[entry.id] = entry
        return entry

    def __len__(self) -> int:
        return len(self._entries)

    def get(self, mutation_id: str) -> MutationEntry:
        try:
            return self._entries[mutation_id]
        except KeyError:
            raise PsiEdgeError(
                f"mutation {mutation_id!r} is not in the catalogue; the tables are not transcribed"
            ) from None

    def ids(self) -> tuple[str, ...]:
        return tuple(sorted(self._entries))


@dataclass(frozen=True, slots=True)
class MutantTemplate:
    """A character with mutations; not a statement about ancestry.

    Three facts stay apart, which is the whole point of §2: **mutation** (what the body does),
    **ancestry** (where it came from, if anyone knows) and **PSI** (whether the character is psychic).
    A Mutant is not automatically psychic; a Hybrid is a possible origin, not a diagnosis.
    """

    npc: str
    mutations: tuple[str, ...]
    catalogue: MutationCatalogue
    ancestry_known: bool = False
    psi_discipline: str = ""

    def __post_init__(self) -> None:
        if not self.npc.strip():
            raise PsiEdgeError("a Mutant template names an NPC")
        if not self.mutations:
            raise PsiEdgeError("a Mutant template needs at least one mutation")
        for mutation_id in self.mutations:
            self.catalogue.get(mutation_id)  # raises when the tables are not transcribed
        if self.psi_discipline:
            allowed = discipline_decision(self.psi_discipline)
            if not allowed.allowed:
                # NPCs may hold any discipline; only a *player* is restricted. Record the fact.
                pass
        if self.ancestry_known and not self.mutations:
            raise PsiEdgeError("ancestry without mutation is a different template")


def assert_mutant_is_npc(template: MutantTemplate, *, is_player: bool) -> None:
    """Legacy compatibility helper: Mutant is now legal for PCs too."""
    return None
