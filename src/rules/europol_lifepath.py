"""#1217: Tony German's lifepath — a deterministic builder with legality checks.

The tracker asks for an author-approved **choose-your-lifepath** flow and a deterministic builder for the fixed
opening character, with *"test legality and tabletop equivalence"*. This module is that builder's core, and it is
deliberately narrower than a character generator:

* **The fixed facts are not ours to invent.** The name, the Helsinki origin, the mandatory Europol Academy
  appointment, the Ratakatu 12 posting and Dr Harri Romppainen are Tomi's, recorded once in :data:`FIXED` with the
  source of each line. Nothing here writes a memory, a dream or a line of dialogue.
* **No Edge, Focus or Background is conjured.** Callers pass the catalogue they have verified; an id that is not in
  it is a violation, never a default. (CWN Foci are the documented exception — the repository already carries the
  twenty-six published ones in :data:`rules.cwn_foci.FOCI`, so they are the default here.)
* **The budget comes from the rules modules, not from a copy.** Edge slots, the Underdog Rule, Focus slots and the
  creation skill ceiling are all delegated to :mod:`rules.cwn_edges_foci` and :mod:`rules.cwn_character`. A change
  there changes this builder; a second copy of the arithmetic cannot drift because there is no second copy.
* **Every violation is reported at once.** A player-facing flow has to be able to say "no: here are the three things
  wrong", not fail on the first and hide the rest.

What this module does **not** do: pick the character's tags for them, choose their Edges, or decide which recruitment
path the authored opening uses. Those are the choices the flow exists to offer.
"""
from __future__ import annotations

from collections.abc import Iterable, Mapping, Sequence
from dataclasses import dataclass, field

from .cwn_backgrounds import (
    LEARNING_PICKS,
    Background,
    grant_free_skill,
    specific_picks,
)
from .cwn_character import ARRAY, ATTRIBUTES, SkillPool, assign_array, roll_attributes
from .cwn_edges_foci import (
    EDGES_AT_START,
    Edge,
    Focus as TalentFocus,
    TalentSheet,
    attribute_modifier_total,
    focus_slots,
    pick_edge,
    pick_focus,
    underdog_eligible,
)
from .cwn_foci import FOCI as FOCUS_CATALOGUE
from .psi_access import PC_EDGES
from .rookie_build import BuildError as RookieBuildError
from .rookie_build import RookieBuild
from .scene_tags import PersonalityTag

#: The canonical actor id the console slice, the actor registry and the graphs already agree on.
ACTOR_ID = "tony.german"

__all__ = [
    "FIXED",
    "PATHS",
    "Lifepath",
    "LifepathError",
    "LifepathViolation",
    "build_lifepath",
    "legal_paths",
]


class LifepathError(ValueError):
    """One or more selections are outside the rules; see :attr:`LifepathError.violations`."""

    def __init__(self, violations: Sequence["LifepathViolation"]) -> None:
        self.violations = tuple(violations)
        super().__init__("; ".join(f"{v.field}: {v.reason}" for v in self.violations))


@dataclass(frozen=True, slots=True)
class LifepathViolation:
    """A single reason a submitted lifepath is not legal."""

    field: str
    reason: str


# --------------------------------------------------------------------------- #
# Author facts — not agent invention
# --------------------------------------------------------------------------- #
#: The opening character's fixed facts, each with where it came from. An agent may reformat these; it may not add to
#: them. A new fixed fact needs a line in the issue, not a plausible guess here.
FIXED: Mapping[str, tuple[str, str]] = {
    "name": ("Tony German", "#1217 line 7 (fixed name)"),
    "origin": ("Helsinki", "#1217 line 7 (Helsinki origin)"),
    "academy": ("Europol Academy", "#1217 line 7 (mandatory Academy/Law Enforcement)"),
    "background": ("Law Enforcement", "#1217 line 7 and the published CWN background of that name"),
    "employer": ("Europol", "#1217 note (supersedes the older UNSA employer)"),
    "posting": ("Europol Field Office, Ratakatu 12", "#1217 line 8"),
    "supervisor": ("Dr Harri Romppainen", "#1217 line 8"),
}

#: The three recruitment routes named by the tracker. They are **labels for the authored flow**, not mechanics: none
#: grants a bonus, and none may invent one. ``freak`` additionally requires the author-approved Mutant Edge, because
#: #1178 makes that Edge the human-alien Hybrid and the route is named for it.
PATHS: Mapping[str, Mapping[str, object]] = {
    "grunt": {
        "summary": "Uniformed response route: the officer who is sent first and asked later.",
        "requires_edges": (),
        "grants": (),
    },
    "geek": {
        "summary": "Technical route: forensics, systems, the part of the job done sitting down.",
        "requires_edges": (),
        "grants": (),
    },
    "freak": {
        "summary": "Hybrid route: the Mutant Edge, a registered or unregistered ancestry, and the clearance problem.",
        "requires_edges": ("Mutant",),
        "grants": (),
    },
}


def legal_paths(*, edges: Iterable[str]) -> tuple[str, ...]:
    """Which recruitment routes a character with these Edge ids may take."""
    owned = set(edges)
    return tuple(
        name for name, spec in PATHS.items()
        if all(requirement in owned for requirement in tuple(spec["requires_edges"]))  # type: ignore[arg-type]
    )


@dataclass(frozen=True)
class Lifepath:
    """A validated character-creation result, with the provenance of each part."""

    path: str
    attributes: Mapping[str, int]
    background: str
    edges: tuple[str, ...]
    focus_levels: Mapping[str, int]
    skills: Mapping[str, int]
    underdog: bool
    personality: tuple[PersonalityTag, ...] = ()
    provenance: tuple[str, ...] = field(default=())

    def to_dict(self) -> dict[str, object]:
        """A save-friendly form; key order is stable so two equal lifepaths serialise identically."""
        return {
            "path": self.path,
            "attributes": dict(sorted(self.attributes.items())),
            "background": self.background,
            "edges": list(self.edges),
            "focus_levels": dict(sorted(self.focus_levels.items())),
            "skills": dict(sorted(self.skills.items())),
            "underdog": self.underdog,
            "personality": [
                {"owner_id": t.owner_id, "trait": t.trait, "evidence": t.evidence}
                for t in self.personality
            ],
            "provenance": list(self.provenance),
        }


def build_lifepath(
    *,
    path: str,
    attributes: Mapping[str, int] | None = None,
    background: Background,
    attribute_dice: Sequence[int] | None = None,
    edges: Sequence[Edge],
    foci: Sequence[str] = (),
    learning_picks: Sequence[str] = (),
    personality: Sequence[PersonalityTag] = (),
    edge_catalogue: Mapping[str, Edge] | None = None,
    focus_catalogue: Mapping[str, object] | None = None,
    level: int = 1,
) -> Lifepath:
    """Validate a complete set of choices and return the character, or raise with every violation.

    Parameters mirror the flow's questions: which route, which attribute assignment, which Background, which Edges,
    which Focus picks and which Learning picks. ``edge_catalogue`` exists because the repository does not carry a
    verified CWN Edge list — only the four author-approved PC Edges in :mod:`rules.psi_access`. Passing ``None``
    means "trust these Edge objects", which is what the tests do with fixtures; a caller with a real catalogue should
    pass it so that a typo becomes a violation instead of a character.
    """
    violations: list[LifepathViolation] = []
    catalogue = dict(edge_catalogue) if edge_catalogue is not None else None
    foci_catalogue = dict(focus_catalogue) if focus_catalogue is not None else dict(FOCUS_CATALOGUE)

    # -- route -----------------------------------------------------------------
    if path not in PATHS:
        violations.append(LifepathViolation("path", f"unknown recruitment route {path!r}"))
    required = tuple(PATHS.get(path, {}).get("requires_edges", ()))  # type: ignore[arg-type]
    owned = {edge.id for edge in edges}
    for name in required:
        if name not in owned:
            violations.append(
                LifepathViolation("path", f"the {path} route requires the {name} Edge")
            )

    # -- attributes ------------------------------------------------------------
    scores: Mapping[str, int] = {}
    if (attributes is None) == (attribute_dice is None):
        violations.append(
            LifepathViolation(
                "attributes",
                "give either a rolled assignment (attributes) or the 3d6 results (attribute_dice), not both/neither",
            )
        )
    elif attribute_dice is not None:
        try:
            # The rules module owns the roll arithmetic; this builder only records the result.
            scores = roll_attributes(attribute_dice)
        except Exception as exc:
            violations.append(LifepathViolation("attributes", str(exc)))
    elif set(attributes) != set(ATTRIBUTES):  # type: ignore[arg-type]
        violations.append(
            LifepathViolation("attributes", f"expected the six CWN attributes, got {sorted(attributes)}")
        )
    else:
        try:
            scores = assign_array(attributes)  # type: ignore[arg-type]
        except Exception as exc:  # the rules module owns the exact message
            violations.append(LifepathViolation("attributes", str(exc)))

    # -- background and its two Learning picks ---------------------------------
    if background.id not in FIXED["background"][0] and background.id != "Law Enforcement":
        violations.append(
            LifepathViolation(
                "background",
                f"{background.id!r} is not the authored background ({FIXED['background'][0]!r}); "
                "a different Background is an author decision, not a builder option",
            )
        )
    pool = SkillPool()
    try:
        grant_free_skill(background, pool)
        if len(learning_picks) != LEARNING_PICKS:
            raise ValueError(f"expected {LEARNING_PICKS} Learning picks, got {len(learning_picks)}")
        specific_picks(background, learning_picks, pool)
    except Exception as exc:
        violations.append(LifepathViolation("skills", str(exc)))

    # -- Edges, through the composition that knows both budgets -----------------
    # `rookie_build` is the NoöPunk-level join of CWN's slot arithmetic and the access policy; using it here means
    # this builder cannot accept a combination that either of them refuses (#1231).
    build = RookieBuild(actor_id=ACTOR_ID, background=background.id, sheet=TalentSheet(level=level))
    sheet = build.sheet
    underdog = False
    if scores:
        underdog = underdog_eligible(scores)
    for edge in edges:
        if catalogue is not None and edge.id not in catalogue:
            violations.append(LifepathViolation("edges", f"{edge.id!r} is not in the supplied catalogue"))
            continue
        try:
            if edge.id in PC_EDGES:
                # The four psi Edges are the only ones the access policy knows, so they are the only ones it can
                # validate: Mutant needs Europol approval, Mentalist may not sit beside a Spellcaster or Summoner.
                build.add_edge(edge, underdog_eligible=underdog)
            else:
                # A generic CWN Edge has no policy entry; `psi_access.edge_decision` would refuse it as unknown, which
                # would make this builder reject every ordinary CWN character. Slots are still CWN's arithmetic.
                pick_edge(sheet, edge, underdog_eligible=underdog)
                build.sheet = sheet
        except (RookieBuildError, Exception) as exc:
            violations.append(LifepathViolation("edges", str(exc)))
    if scores and len(edges) > EDGES_AT_START and not underdog and level < 5:
        violations.append(
            LifepathViolation(
                "edges",
                f"{len(edges)} Edges at level {level} with an attribute modifier total of "
                f"{attribute_modifier_total(scores)}; only the Underdog Rule or fifth level grants a third",
            )
        )

    # -- Foci, against the same sheet ------------------------------------------
    picks = list(foci)
    focused = "Focused" in sheet.edges
    slot_count = focus_slots(sheet, has_focused_edge=focused)
    if len(picks) > slot_count:
        violations.append(
            LifepathViolation("foci", f"{len(picks)} Focus picks exceed the {slot_count} slot(s) available")
        )
    for name in picks:
        if name not in foci_catalogue:
            violations.append(LifepathViolation("foci", f"{name!r} is not a CWN Focus"))
            continue
        focus = foci_catalogue[name]
        try:
            # `cwn_foci` carries the published names and level counts; the slot/requirement arithmetic lives in
            # `cwn_edges_foci.Focus`, so the published record is projected onto it rather than duplicated.
            talent = TalentFocus(
                id=getattr(focus, "name", name),
                levels=getattr(focus, "levels", 2),
                requires=tuple(getattr(focus, "requires", ())),
            )
            pick_focus(sheet, talent, has_focused_edge=focused)
        except Exception as exc:
            violations.append(LifepathViolation("foci", str(exc)))

    # -- personality tags: descriptive only, but they must be real tags ---------
    for tag in personality:
        if not isinstance(tag, PersonalityTag):
            violations.append(LifepathViolation("personality", "personality tags must be PersonalityTag records"))

    if violations:
        raise LifepathError(violations)

    provenance = [
        f"name/origin/academy/posting: {FIXED['name'][1]}",
        "attribute array: CWN character generation (rules.cwn_character.ARRAY)",
        "Edge slots, Underdog Rule and Focus slots: rules.cwn_edges_foci",
        "Background free skill and Learning picks: rules.cwn_backgrounds",
        "Focus levels: rules.cwn_foci (published CWN Foci)",
        f"recruitment route: #1217 line 7 ({path})",
    ]
    if path == "freak":
        provenance.append("Mutant Edge as the Hybrid: #1178 §species and ancestry")

    return Lifepath(
        path=path,
        attributes=dict(sorted(scores.items())),
        background=background.id,
        edges=tuple(sheet.edges),
        focus_levels=dict(sorted(sheet.focus_levels.items())),
        skills=dict(sorted(pool.levels.items())),
        underdog=sheet.underdog_used,
        personality=tuple(personality),
        provenance=tuple(provenance),
    )
