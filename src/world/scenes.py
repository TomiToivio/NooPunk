"""Scene types for the NoöPunk graph model (#1178, #1184, scene-type proposal).

A scene is an *episode of play that references* the persistent graphs; it is not a location. This
module gives each kind a contract — which graphs it may use, which narrative tags it needs, which
CWN material resolves it, and what it refuses to become — so that "Social scene" means one thing in
the tabletop, the CLI and the future graphical client.

Implemented now: **Social, Investigation, Exploration, Action, Cyber.**
Deferred by author decision: **Astral** (until scripted Astral Projection lands, #1178 §2).
Proposed, for review: **Interrogation, Data Collection, Data Analysis** — see
`docs/design/SCENE_TYPES_PROPOSAL.md`. They are *not* accepted kinds and a `Scene` refuses them.

Three constraints come from decisions already made elsewhere in the repository:

* **CWN is immutable.** Each contract names CWN skills; none invents a new one, a new resource, or a
  new resolution procedure.
* **No investigation-point economy** (#1184, #1164). Investigation scenes do not spend points.
* **Core clues are never gated behind a roll.** Borrowed from GUMSHOE's structure (see the proposal);
  CWN's roll decides *consequences* and *timing*, not whether a necessary fact exists.
"""
from __future__ import annotations

from collections.abc import Iterable
from dataclasses import dataclass

try:  # imported as src.world.scenes
    from .graphs import WorldGraphs
    from .narrative_tags import NarrativeTag, NarrativeTags
except ImportError:  # a caller that put `src/world` on sys.path
    from graphs import WorldGraphs  # type: ignore[no-redef]
    from narrative_tags import (  # type: ignore[no-redef]
        NarrativeTag,
        NarrativeTags,
    )

__all__ = [
    "DEFERRED_SCENE_KINDS",
    "IMPLEMENTED_SCENE_KINDS",
    "PROPOSED_SCENE_KINDS",
    "SCENE_CONTRACTS",
    "Scene",
    "SceneContract",
    "SceneError",
]


class SceneError(ValueError):
    """A scene would run without what its contract requires."""


IMPLEMENTED_SCENE_KINDS = ("Social", "Investigation", "Exploration", "Action", "Cyber")
DEFERRED_SCENE_KINDS = ("Astral",)
PROPOSED_SCENE_KINDS = ("Interrogation", "Data Collection", "Data Analysis")


@dataclass(frozen=True)
class SceneContract:
    kind: str
    uses_graphs: tuple[str, ...]
    requires_tags: tuple[str, ...]
    resolution: tuple[str, ...]
    core_rule: str
    refuses: str
    requires_any_tags: tuple[str, ...] = ()


SCENE_CONTRACTS: dict[str, SceneContract] = {
    "Social": SceneContract(
        kind="Social",
        uses_graphs=("social", "physical"),
        requires_tags=(),
        requires_any_tags=("social", "personality"),
        resolution=("Talk", "Connect", "Lead", "Know (culture)", "notice"),
        core_rule=(
            "A social tag opens a door — it makes the meeting possible. Whether the meeting "
            "succeeds is a CWN check with its consequences; no tag and no scene compels an NPC."
        ),
        refuses="no persuasion meter, no loyalty score, no dialogue puzzle with a correct answer",
    ),
    "Investigation": SceneContract(
        kind="Investigation",
        uses_graphs=("physical", "social", "story"),
        requires_tags=("clue",),
        resolution=("Notice", "Search", "Know", "Connect", "Program (records)", "Fix", "Administer"),
        core_rule=(
            "Core clues are never gated behind a roll: the roll decides time, noise, a complication "
            "or an extra fact — never whether the case can proceed."
        ),
        refuses="no investigation-point economy, no 'you failed to notice the plot' state",
    ),
    "Exploration": SceneContract(
        kind="Exploration",
        uses_graphs=("physical",),
        requires_tags=(),
        resolution=("Move (CWN overland/travel)", "Notice", "Survival", "Sneak", "Exert"),
        core_rule=(
            "Movement follows the Physical graph's routes and nothing else; a scene may reveal a "
            "route, but may not teleport a character."
        ),
        refuses="no hex crawl, no procedural map generation, no travel minigame",
    ),
    "Action": SceneContract(
        kind="Action",
        uses_graphs=("physical", "cyber"),
        requires_tags=(),
        resolution=("CWN combat when unavoidable", "Pursue (Drive/Exert)", "Notice", "Talk (surrender)"),
        core_rule=(
            "An Action scene is an arrest, a pursuit, a containment, a forced entry, a restraint or a "
            "standoff. CWN combat is what it calls when force cannot be avoided, and a sustained "
            "firefight is a failure state with paperwork."
        ),
        refuses="no tactical grid, no military hardware fantasy, no armed-civilian set piece",
    ),
    "Cyber": SceneContract(
        kind="Cyber",
        uses_graphs=("cyber", "physical"),
        requires_tags=(),
        resolution=("Program", "Fix", "Connect", "Know (security)", "Notice"),
        core_rule=(
            "An avatar moves through the Cyber graph under CWN hacking; moving it never moves its "
            "operator's body, and device actions resolve with CWN's verbs."
        ),
        refuses="no second hacking engine, no minigame, no 'netrunning' subsystem",
    ),
}


@dataclass(frozen=True)
class Scene:
    """One episode of play, referencing graphs and tags rather than owning them."""

    id: str
    kind: str
    title: str
    participants: tuple[str, ...] = ()
    tag_refs: tuple[str, ...] = ()
    location_refs: tuple[str, ...] = ()
    story_node_ref: str = ""
    notes: str = ""

    def __post_init__(self) -> None:
        if not self.id.strip():
            raise SceneError("scene id must be non-empty")
        if self.kind in DEFERRED_SCENE_KINDS:
            raise SceneError(
                f"{self.kind} scenes are deferred until scripted Astral Projection lands (#1178 §2); "
                "use a Story scene with tags for now"
            )
        if self.kind in PROPOSED_SCENE_KINDS:
            raise SceneError(
                f"{self.kind!r} is proposed, not accepted: see docs/design/SCENE_TYPES_PROPOSAL.md"
            )
        if self.kind not in SCENE_CONTRACTS:
            raise SceneError(f"unknown scene kind {self.kind!r}; implemented kinds are {IMPLEMENTED_SCENE_KINDS}")
        if any(not participant.strip() for participant in self.participants):
            raise SceneError("participants must be non-empty character ids")
        if len(set(self.tag_refs)) != len(self.tag_refs):
            raise SceneError("a scene may not cite the same tag twice")

    @property
    def contract(self) -> SceneContract:
        return SCENE_CONTRACTS[self.kind]


def validate_scene(
    scene: Scene,
    *,
    tags: NarrativeTags,
    graphs: WorldGraphs | None = None,
) -> None:
    """Check a scene against its contract: tags exist, refs resolve, prerequisites are present."""
    contract = scene.contract
    cited: list[NarrativeTag] = [tags.get(tag_id) for tag_id in scene.tag_refs]

    cited_kinds = {tag.kind for tag in cited}
    missing = sorted(set(contract.requires_tags) - cited_kinds)
    if missing:
        raise SceneError(
            f"{scene.kind} scene {scene.id!r} needs at least one {'/'.join(missing)} tag"
        )
    if contract.requires_any_tags and not (cited_kinds & set(contract.requires_any_tags)):
        raise SceneError(
            f"{scene.kind} scene {scene.id!r} needs one of "
            f"{'/'.join(contract.requires_any_tags)} tags"
        )

    if graphs is not None:
        unknown_places = [ref for ref in scene.location_refs if ref not in graphs.physical.nodes]
        if unknown_places:
            raise SceneError(f"{scene.id!r} references unknown places {unknown_places}")
        if "cyber" in contract.uses_graphs:
            bad_devices = [
                ref for ref in scene.location_refs
                if ref.startswith("cyber.") and ref not in graphs.cyber.nodes
            ]
            if bad_devices:
                raise SceneError(f"{scene.id!r} references unknown devices {bad_devices}")

    if scene.kind == "Action" and not scene.location_refs:
        raise SceneError("an Action scene must name at least one physical location")
    if scene.kind == "Investigation" and not tags.core_clues():
        raise SceneError(
            "an Investigation scene needs at least one CORE clue in the case; "
            "otherwise the scene can dead-end, which the contract forbids"
        )


def scenes_for_story(scenes: Iterable[Scene], story_node: str) -> tuple[Scene, ...]:
    return tuple(scene for scene in scenes if scene.story_node_ref == story_node)
