"""The Europol rookie's legal build path (#1217, #1174, #1178).

Two validators already exist and do not know about each other:

* `cwn_edges_foci.pick_edge` enforces the **CWN budget** — two Edges at start, a third at level 5,
  the Underdog bonus, no duplicate unless repeatable.
* `psi_access.validate_selection` enforces the **NoöPunk access policy** — which Edges a PC may take,
  which disciplines, and the AWN Mentalist combination bar.

Nothing joined them, and the joining is not cosmetic. On `main` this sequence is accepted today:

    sheet = TalentSheet()
    pick_edge(sheet, Edge("Mentalist", "Mentalist"))
    pick_edge(sheet, Edge("Spellcaster", "Spellcaster"))

…which `psi_access` forbids outright — *"AWN Mentalist cannot combine with CWN Mage/Spellcaster or
Summoner (AWN Deluxe p.265)"*. Neither module is wrong; the character-creation path simply never asks
the second one. That is the "no unlawful ability combinations" requirement in #1217 failing in
practice, not in theory.

The obvious fix — make `pick_edge` consult `psi_access` — is **not** available: `cwn_edges_foci.py` is
a `cwn-core` tier module, and `tools/rules_constitution_audit.py` fails if a core module imports a
`noopunk-mod` one. That boundary is deliberate, and this module respects it by sitting *above* both:
it is the NoöPunk-level composition, so CWN stays ignorant of NoöPunk policy and NoöPunk never forks
CWN's arithmetic.

What this is not: a second character generator. Attributes, the skill pool, Edge/Focus slots and their
level behaviour all stay in the CWN modules; this class **delegates every one of them** and adds only
the access questions CWN cannot answer.

**Not enforced here:** the Academy Graduate Edge. It is a NoöPunk homebrew still marked *draft pending
author review* (`docs/design/DRAFT_EUROPOL_ROOKIE_BUILD_1174.md` §8), so requiring it would implement an
unapproved rule. When the author decides whether it is an Edge, a Focus or a career package, the answer
belongs in `psi_access.PC_EDGES` and then here — not invented now.
"""

from __future__ import annotations

from collections.abc import Iterable
from dataclasses import dataclass, field

from .cwn_edges_foci import (
    Edge,
    Focus,
    TalentRulesError,
    TalentSheet,
    pick_edge,
    pick_focus,
)
from .psi_access import (
    discipline_decision,
    edge_decision,
    validate_selection,
)

__all__ = ["BuildError", "RookieBuild", "check_build"]


class BuildError(ValueError):
    """A build the CWN chassis or the NoöPunk access policy does not allow."""


@dataclass
class RookieBuild:
    """One player character's choices, validated against both budgets.

    ``actor_id`` is the canonical identity — the same string the actor registry, the graphs and the
    character sheet must agree on (``docs/tabletop/WORLD_GRAPHS_1178.md`` check 7). Two builds may not
    claim one actor: that is how a second sheet gets created by accident.
    """

    actor_id: str
    background: str = "Law Enforcement"
    sheet: TalentSheet = field(default_factory=TalentSheet)
    disciplines: list[str] = field(default_factory=list)
    focus_disciplines: list[str] = field(default_factory=list)
    partial_psychic: bool = False
    europol_approved: bool = True

    def __post_init__(self) -> None:
        if not self.actor_id or not self.actor_id.strip():
            raise BuildError("a build needs a canonical actor id")
        if not self.background:
            raise BuildError("a build needs a Background")

    # -- choices -------------------------------------------------------------------------------
    def add_edge(self, edge: Edge, *, underdog_eligible: bool = False) -> None:
        """Take an Edge only if the **resulting set** is legal, and roll back if it is not.

        Two different policies have to hold: the single Edge must be one a PC may take
        (``edge_decision``), and the *combination* must be legal (``validate_selection``) — AWN
        Mentalist may not sit beside Spellcaster or Summoner, and Mutant needs Europol approval.
        Checking only the first is what let the old path through, so the set is re-validated and the
        pick is undone when a new problem appears.
        """
        decision = edge_decision(edge.id)
        if not decision.allowed:
            raise BuildError(decision.reason)

        before = tuple(self.problems())
        underdog_was_used = self.sheet.underdog_used
        try:
            pick_edge(self.sheet, edge, underdog_eligible=underdog_eligible)
        except TalentRulesError as error:
            raise BuildError(str(error)) from None

        introduced = [problem for problem in self.problems() if problem not in before]
        if introduced:
            self.sheet.edges.pop()
            self.sheet.underdog_used = underdog_was_used
            raise BuildError("; ".join(introduced))

    def add_focus(self, focus: Focus, *, has_focused_edge: bool | None = None) -> int:
        """Take or raise a Focus; the level cap stays CWN's."""
        if has_focused_edge is None:
            has_focused_edge = any(
                edge.grants_bonus_focus for edge in _known_edges(self.sheet.edges)
            )
        try:
            return pick_focus(self.sheet, focus, has_focused_edge=has_focused_edge)
        except TalentRulesError as error:
            raise BuildError(str(error)) from None

    def add_discipline(self, name: str) -> None:
        decision = discipline_decision(name)
        if not decision.allowed:
            raise BuildError(decision.reason)
        if name not in self.disciplines:
            self.disciplines.append(name)

    # -- validation ----------------------------------------------------------------------------
    def problems(self) -> list[str]:
        """Every violation at once, so a builder screen can show them together."""
        found = list(
            validate_selection(
                disciplines=self.disciplines,
                edges=self.sheet.edges,
                focus_disciplines=self.focus_disciplines,
                partial_psychic=self.partial_psychic,
                character_level=self.sheet.level,
                europol_approved=self.europol_approved,
            )
        )
        # The Edge budget is CWN's, but a build that skipped pick_edge (loaded from a save, say)
        # must still be caught here rather than trusted.
        slots = self.sheet.edge_slots()
        if len(self.sheet.edges) > slots:
            found.append(
                f"{len(self.sheet.edges)} Edges selected but only {slots} slot(s) exist at level "
                f"{self.sheet.level}"
            )
        if len(set(self.sheet.edges)) != len(self.sheet.edges):
            found.append("a non-repeatable Edge was selected more than once")
        return found

    def validate(self) -> RookieBuild:
        problems = self.problems()
        if problems:
            raise BuildError("; ".join(problems))
        return self


def check_build(build: RookieBuild, *, other: Iterable[RookieBuild] = ()) -> list[str]:
    """Validate one build in the context of the others (duplicate actor identity)."""
    problems = build.problems()
    for existing in other:
        if existing is build:
            continue
        if existing.actor_id == build.actor_id:
            problems.append(
                f"two builds claim actor {build.actor_id!r}; one actor has one sheet "
                "(docs/tabletop/WORLD_GRAPHS_1178.md check 7)"
            )
    return problems


def _known_edges(edge_ids: Iterable[str]) -> list[Edge]:
    """Minimal Edge records for ids already on a sheet, enough to read ``grants_bonus_focus``."""
    return [
        Edge(id=edge_id, grants_bonus_focus=(edge_id == "Focused")) for edge_id in edge_ids
    ]
