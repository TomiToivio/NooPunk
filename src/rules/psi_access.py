"""Who may take which psychic option (#1178).

This module is a **policy layer, not a rules engine**. It answers one question — may a player
character select this option? — and refuses everything else. It deliberately contains no Effort
costs, no technique lists and no discipline ranks: those belong to the published rules, and this
repository refuses to transcribe them from memory.

The author's decisions (#1178 §1–§4) that this encodes:

* A player character may select **Telekinesis** and **Telepathy**, and no other SWN discipline.
* The other disciplines exist for NPCs and as **scripted events**, never as player options.
* **Astral Projection is scripted** — an OOBE, an NDE, or a psychotronic event — not a selectable
  power, and not a running Astral subsystem.
* **Mutant** is an NPC-only Edge. A player character may not take it.
* **Mentalist**, **Spellcaster** and **Summoner** are selectable Edges, each using its own published
  mechanics. Knowing Telepathy grants no free spellcasting: *Magick is PSI* is a statement about the
  fiction, not a conversion rule.
* A **psychotronic device may grant an ability**; a grant never makes a prohibited discipline
  selectable, and it never turns into a permanent character option.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

#: Disciplines a player character may choose. Everything else in the SWN list is closed to PCs.
PC_DISCIPLINES: tuple[str, ...] = ("Telekinesis", "Telepathy")

#: The rest of the SWN discipline list, kept explicit so a typo cannot quietly become an option.
NPC_ONLY_DISCIPLINES: tuple[str, ...] = (
    "Biopsionics",
    "Metapsionics",
    "Precognition",
    "Teleportation",
)

#: Effects that exist only inside authored scenes.
SCRIPTED_ONLY: tuple[str, ...] = (
    "Astral Projection",
    "Precognition",
    "Teleportation",
)

#: Edges a player character may select, each with its own published mechanics.
PC_EDGES: tuple[str, ...] = ("Mentalist", "Spellcaster", "Summoner")

#: Edges reserved for NPCs.
NPC_ONLY_EDGES: tuple[str, ...] = ("Mutant",)

#: The Psychic Training Focus is only implemented once the printed text is available. Until then the
#: policy refuses to *simulate* it rather than inventing level benefits.
PSYCHIC_TRAINING_FOCUS_AVAILABLE = False
PSYCHIC_TRAINING_FOCUS_BLOCKED_REASON = (
    "Psychic Training Focus needs its published level benefits and Effort increases verbatim; "
    "this repository does not transcribe rules from memory (#1043, #1178 §1)."
)


class PsiAccessError(ValueError):
    """A character option was about to break the access policy."""


@dataclass(frozen=True)
class Decision:
    """A refusal that says why, because a silent exclusion is indistinguishable from a bug."""

    allowed: bool
    reason: str = ""

    def __bool__(self) -> bool:  # a Decision is usable as a condition
        return self.allowed


def discipline_decision(name: str) -> Decision:
    """May a *player character* select this discipline?"""
    if name in PC_DISCIPLINES:
        return Decision(True)
    if name in NPC_ONLY_DISCIPLINES:
        return Decision(False, f"{name} is not selectable by a player character (#1178 §1)")
    return Decision(False, f"{name!r} is not a known discipline; refusing rather than guessing")


def edge_decision(name: str) -> Decision:
    """May a player character select this Edge?"""
    if name in PC_EDGES:
        return Decision(True)
    if name in NPC_ONLY_EDGES:
        return Decision(False, f"{name} is NPC-only (#1178 §3)")
    return Decision(False, f"{name!r} is not a known Edge; refusing rather than guessing")


def require_pc_discipline(name: str) -> str:
    decision = discipline_decision(name)
    if not decision.allowed:
        raise PsiAccessError(decision.reason)
    return name


def require_pc_edge(name: str) -> str:
    decision = edge_decision(name)
    if not decision.allowed:
        raise PsiAccessError(decision.reason)
    return name


def is_scripted_effect(effect: str) -> bool:
    """True when an effect may only happen because an authored scene says so."""
    return effect in SCRIPTED_ONLY


def require_scripted(effect: str) -> bool:
    """Assert that an effect is treated as scripted rather than selectable."""
    if not is_scripted_effect(effect):
        raise PsiAccessError(f"{effect!r} is not a scripted-only effect")
    return True


def validate_selection(
    *,
    disciplines: Iterable[str] = (),
    edges: Iterable[str] = (),
    focus_disciplines: Iterable[str] = (),
) -> list[str]:
    """Return every violation in one pass, so a character builder can show all of them at once.

    ``focus_disciplines`` are the disciplines a Psychic Training Focus would advance. They must also
    be player-allowed — that is the loophole the issue names: a Focus must not become a back door to
    a second, prohibited discipline.
    """
    problems: list[str] = []
    chosen = list(disciplines)
    for name in chosen:
        decision = discipline_decision(name)
        if not decision.allowed:
            problems.append(decision.reason)
    if len(set(chosen)) > 1:
        problems.append(
            "a player character may hold only Telepathy or Telekinesis, not several disciplines "
            "(#1178 §1)"
        )
    for name in edges:
        decision = edge_decision(name)
        if not decision.allowed:
            problems.append(decision.reason)
    for name in focus_disciplines:
        decision = discipline_decision(name)
        if not decision.allowed:
            problems.append("Psychic Training Focus: " + decision.reason)
        elif chosen and name not in chosen:
            problems.append(
                f"Psychic Training Focus may not open a second discipline ({name!r}); "
                "for the PC the Focus stays inside Telepathy or Telekinesis (#1178 §1)"
            )
    return problems


@dataclass(frozen=True)
class Grant:
    """An ability a *device* gives the character while it is in use.

    ``selectable`` is always False, and that is the whole point: a psychotronic implant can do
    something remarkable without widening what the character may choose at advancement.
    """

    ability: str
    source: str
    selectable: bool = False

    def __post_init__(self) -> None:
        if self.selectable:
            raise PsiAccessError(
                "a device grant is never a selectable option (#1178 §2)"
            )


def device_grant(ability: str, *, source: str) -> Grant:
    """Record that a device grants an ability for as long as it is used."""
    if not ability.strip():
        raise PsiAccessError("a grant needs an ability")
    if not source.strip():
        raise PsiAccessError("a grant needs a source device")
    return Grant(ability=ability, source=source)
