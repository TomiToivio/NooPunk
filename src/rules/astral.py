"""Astral graph and PSI permission layer for NoöPunk (#1164).

**Deferred by #1178:** Astral Projection is scripted and the Astral graph is not part of the
current four-graph slice. This module is a prototype, not runtime authority; do not wire it
into play until the Astral work is separately approved.

This is the **prototype add-on**, not a second rules engine: Effort accounting stays in
:mod:`src.rules.swn_psionics`, ordinary action resolution stays in CWN, and investigation remains
the resolver in :mod:`src.rules.investigation`. The module supplies only what the graph design
needs:

* a fail-closed **Verb x Target** permission matrix (the draft's ``DENIED`` default);
* the **embodied -> overlay -> projected -> returned** astral state machine with an anchor and a
  visible return path;
* a small, author-readable **Astral graph** with visibility and gate checks;
* one Effort commitment per projection, delegated to the existing psychic engine.

The matrix and the projection discipline are **proposals pending author approval**. Nothing here
grants an investigation clue, bypasses CWN hacking, or lets an astral action affect the physical
world without an explicit permission record.

Source: ``docs/design/DRAFT_GRAPH_SCENES_1164.md`` sections 7.2-7.3 and
``docs/design/DRAFT_NOOPUNK_PSIONICS.md``. Original code; no published technique text is copied.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum

from .swn_psionics import Duration, PsiRulesError, Psychic


class AstralError(ValueError):
    """An astral state or graph invariant was about to be violated."""


class AstralMode(str, Enum):
    EMBODIED = "embodied"
    OVERLAY = "overlay"
    PROJECTED = "projected"
    MANIFESTING = "manifesting"


class PsiVerb(str, Enum):
    PERCEIVE = "perceive"
    CONTACT = "contact"
    SHIELD = "shield"
    PROJECT = "project"
    INFLUENCE = "influence"
    IMPRINT = "imprint"
    RITUALIZE = "ritualize"
    MANIFEST = "manifest"


class PsiTarget(str, Enum):
    SELF = "self"
    PERSON = "person"
    BIOLOGIC = "biologic"
    MATTER = "matter"
    CYBER = "cyber"
    ASTRAL = "astral"
    GROUP = "group"


class PermissionStatus(str, Enum):
    """``active`` is player-activatable after an unlock; ``scripted`` is GM/NPC only."""

    ACTIVE = "active"
    SCRIPTED = "scripted"
    DENIED = "denied"


@dataclass(frozen=True)
class PsiPermission:
    """One cell of the Verb x Target matrix.

    ``requires_projection`` means the actor must already be in ``projected`` or
    ``manifesting`` mode. ``requires_consent`` is used for person-to-person contact; a defended
    target can still refuse. ``grants_investigation_clue`` is deliberately a constant ``False``
    and is asserted by the tests.
    """

    verb: PsiVerb
    target: PsiTarget
    status: PermissionStatus
    requires_projection: bool = False
    requires_consent: bool = False
    source: str = "swn_psionics"
    note: str = ""

    @property
    def grants_investigation_clue(self) -> bool:
        return False


def _permissions() -> dict[tuple[PsiVerb, PsiTarget], PsiPermission]:
    """Build the draft matrix. Every unspecified cell is ``DENIED``, not inferred."""

    active: dict[PsiVerb, tuple[PsiTarget, ...]] = {
        PsiVerb.PERCEIVE: (
            PsiTarget.SELF,
            PsiTarget.PERSON,
            PsiTarget.BIOLOGIC,
            PsiTarget.MATTER,
            PsiTarget.CYBER,
            PsiTarget.ASTRAL,
        ),
        PsiVerb.CONTACT: (PsiTarget.SELF, PsiTarget.PERSON, PsiTarget.ASTRAL),
        PsiVerb.SHIELD: (
            PsiTarget.SELF,
            PsiTarget.PERSON,
            PsiTarget.CYBER,
            PsiTarget.ASTRAL,
        ),
        PsiVerb.PROJECT: (PsiTarget.SELF, PsiTarget.ASTRAL),
        PsiVerb.INFLUENCE: (PsiTarget.SELF,),
    }
    scripted: dict[PsiVerb, tuple[PsiTarget, ...]] = {
        PsiVerb.PERCEIVE: (PsiTarget.GROUP,),
        PsiVerb.CONTACT: (PsiTarget.BIOLOGIC, PsiTarget.GROUP),
        PsiVerb.SHIELD: (PsiTarget.BIOLOGIC, PsiTarget.GROUP),
        PsiVerb.PROJECT: (PsiTarget.GROUP,),
        PsiVerb.INFLUENCE: (
            PsiTarget.PERSON,
            PsiTarget.BIOLOGIC,
            PsiTarget.ASTRAL,
            PsiTarget.GROUP,
        ),
        PsiVerb.IMPRINT: (
            PsiTarget.PERSON,
            PsiTarget.BIOLOGIC,
            PsiTarget.MATTER,
            PsiTarget.CYBER,
            PsiTarget.ASTRAL,
        ),
        PsiVerb.RITUALIZE: tuple(PsiTarget),
        PsiVerb.MANIFEST: (
            PsiTarget.SELF,
            PsiTarget.MATTER,
            PsiTarget.CYBER,
            PsiTarget.ASTRAL,
        ),
    }

    matrix: dict[tuple[PsiVerb, PsiTarget], PsiPermission] = {}
    for verb in PsiVerb:
        for target in PsiTarget:
            if target in active.get(verb, ()):
                matrix[(verb, target)] = PsiPermission(
                    verb,
                    target,
                    PermissionStatus.ACTIVE,
                    requires_projection=target is PsiTarget.ASTRAL,
                    requires_consent=(
                        verb is PsiVerb.CONTACT and target is PsiTarget.PERSON
                    ),
                )
            elif target in scripted.get(verb, ()):
                matrix[(verb, target)] = PsiPermission(
                    verb,
                    target,
                    PermissionStatus.SCRIPTED,
                    requires_projection=target is PsiTarget.ASTRAL,
                )
            else:
                matrix[(verb, target)] = PsiPermission(
                    verb, target, PermissionStatus.DENIED
                )
    return matrix


#: The single source of the matrix; callers read it through :func:`permission`.
PSI_MATRIX: dict[tuple[PsiVerb, PsiTarget], PsiPermission] = _permissions()


def permission(verb: PsiVerb | str, target: PsiTarget | str) -> PsiPermission:
    """Look up a cell. Unknown values and unspecified combinations are DENIED, never inferred."""
    try:
        verb_enum = PsiVerb(verb)
        target_enum = PsiTarget(target)
    except ValueError:
        return PsiPermission(
            PsiVerb.PERCEIVE,
            PsiTarget.SELF,
            PermissionStatus.DENIED,
            note="unknown verb or target",
        )
    return PSI_MATRIX[(verb_enum, target_enum)]


@dataclass(frozen=True)
class PsiAction:
    """The result of asking whether one PSI action is legal *before* any dice are rolled."""

    verb: PsiVerb
    target: PsiTarget
    permitted: bool
    status: PermissionStatus
    reason: str = ""
    scripted_only: bool = False
    requires_projection: bool = False

    @property
    def grants_investigation_clue(self) -> bool:
        return False


def authorize(
    verb: PsiVerb | str,
    target: PsiTarget | str,
    *,
    state: AstralState | None = None,
    consent: bool = False,
    unlocked: bool = False,
) -> PsiAction:
    """Fail-closed authorization for a **single** PSI action.

    The caller still supplies the CWN check, range, duration and consequences. This function only
    answers the design's permission question: may this verb target this kind of thing at all?
    """
    cell = permission(verb, target)
    if cell.status is PermissionStatus.DENIED:
        return PsiAction(
            cell.verb,
            cell.target,
            False,
            cell.status,
            "cell is denied by the PSI matrix",
            requires_projection=cell.requires_projection,
        )
    if cell.status is PermissionStatus.SCRIPTED:
        return PsiAction(
            cell.verb,
            cell.target,
            False,
            cell.status,
            "scripted or NPC-only; not a player action",
            scripted_only=True,
            requires_projection=cell.requires_projection,
        )
    if not unlocked:
        return PsiAction(
            cell.verb,
            cell.target,
            False,
            cell.status,
            "the technique or awakening has not been unlocked",
            requires_projection=cell.requires_projection,
        )
    if cell.requires_projection and (
        state is None
        or state.mode not in (AstralMode.PROJECTED, AstralMode.MANIFESTING)
    ):
        return PsiAction(
            cell.verb,
            cell.target,
            False,
            cell.status,
            "a projected or manifesting astral state is required",
            requires_projection=True,
        )
    if cell.requires_consent and not consent:
        return PsiAction(
            cell.verb,
            cell.target,
            False,
            cell.status,
            "the target has not consented to contact",
            requires_projection=cell.requires_projection,
        )
    return PsiAction(
        cell.verb,
        cell.target,
        True,
        cell.status,
        requires_projection=cell.requires_projection,
    )


def activate(
    verb: PsiVerb | str,
    target: PsiTarget | str,
    *,
    psychic: Psychic,
    key: str,
    state: AstralState | None = None,
    consent: bool = False,
    unlocked: bool = False,
    discipline: str = "Metapsionics",
    minimum_rank: int = 0,
    effort: int = 1,
    duration: Duration = Duration.SCENE,
) -> PsiAction:
    """Authorize and commit **one** payer for a non-projection PSI action.

    Projection has its own entry point (:meth:`AstralState.project`) so that it cannot be charged
    twice. This helper is for Shield, Contact, Perceive and the other bounded actions.
    """
    action = authorize(verb, target, state=state, consent=consent, unlocked=unlocked)
    if not action.permitted or effort <= 0:
        return action
    try:
        psychic.commit(
            key, discipline, minimum_rank=minimum_rank, duration=duration, amount=effort
        )
    except PsiRulesError as exc:
        return PsiAction(
            action.verb,
            action.target,
            False,
            action.status,
            str(exc),
            requires_projection=action.requires_projection,
        )
    return action


@dataclass
class AstralState:
    """One actor's position in the layered reality.

    The physical body is **not** moved by projection: ``anchor`` stays a real Physical node and
    the body remains findable, movable and vulnerable. Three filled link boxes mean a scene of
    finding the way back, not death.
    """

    mode: AstralMode = AstralMode.EMBODIED
    anchor: str = ""
    realm: str = ""
    current_node: str = ""
    link_boxes: int = 0
    scenes_projected: int = 0
    max_link_boxes: int = 3

    def __post_init__(self) -> None:
        if not isinstance(self.mode, AstralMode):
            self.mode = AstralMode(self.mode)
        if self.max_link_boxes < 1:
            raise AstralError("max_link_boxes must be positive")
        if not 0 <= self.link_boxes <= self.max_link_boxes:
            raise AstralError("link_boxes must be within 0..max_link_boxes")
        if self.scenes_projected < 0:
            raise AstralError("scenes_projected cannot be negative")

    @property
    def projected(self) -> bool:
        return self.mode in (AstralMode.PROJECTED, AstralMode.MANIFESTING)

    @property
    def link_lost(self) -> bool:
        return self.link_boxes >= self.max_link_boxes

    def overlay(self, *, anchor: str) -> None:
        """Perceive the astral while embodied; no travel and no disembodied action."""
        if self.mode is not AstralMode.EMBODIED:
            raise AstralError("overlay can only start from the embodied state")
        if not anchor:
            raise AstralError("overlay needs a physical anchor")
        self.mode = AstralMode.OVERLAY
        self.anchor = anchor

    def project(
        self,
        *,
        anchor: str,
        realm: str,
        psychic: Psychic,
        key: str = "astral.projection",
        discipline: str = "Metapsionics",
        minimum_rank: int = 0,
        entry_node: str = "",
    ) -> None:
        """Enter projected mode and commit the single Effort cost.

        The caller supplies the discipline/rank until the author fixes the technique mapping.
        ``key`` must be unique among the psychic's active commitments.
        """
        if self.mode not in (AstralMode.EMBODIED, AstralMode.OVERLAY):
            raise AstralError("projection can only start from embodied or overlay")
        if not anchor:
            raise AstralError("projection needs a physical anchor")
        if not realm:
            raise AstralError("projection needs a named realm")
        try:
            psychic.commit(
                key,
                discipline,
                minimum_rank=minimum_rank,
                duration=Duration.SCENE,
                amount=1,
            )
        except PsiRulesError as exc:
            raise AstralError(str(exc)) from exc
        self.mode = AstralMode.PROJECTED
        self.anchor = anchor
        self.realm = realm
        self.current_node = entry_node
        self.link_boxes = 0
        self.scenes_projected = 0

    def return_to_body(self) -> None:
        """End projection. Effort was committed for the scene and is not refunded early."""
        if not self.projected:
            raise AstralError("the character is not projected")
        self.mode = AstralMode.EMBODIED
        self.realm = ""
        self.current_node = ""
        self.link_boxes = 0
        self.scenes_projected = 0

    def tick_scene(self) -> None:
        """Count a projected scene; every scene past the first fills one link box."""
        if not self.projected:
            return
        self.scenes_projected += 1
        if self.scenes_projected > 1:
            self.strain()

    def strain(self, boxes: int = 1) -> None:
        """The anchor is fraying. At the maximum the return is a scene, not a death."""
        if boxes < 1:
            raise AstralError("strain adds at least one link box")
        self.link_boxes = min(self.max_link_boxes, self.link_boxes + boxes)

    def travel(
        self,
        graph: AstralGraph,
        destination: str,
        *,
        act: int = 1,
        discovered: frozenset[str] | set[str] = frozenset(),
        unlocked_gates: frozenset[str] | set[str] = frozenset(),
    ) -> None:
        """Move to an adjacent, visible node. No implicit universal travel."""
        if not self.projected:
            raise AstralError("travel requires a projected state")
        if not self.current_node:
            raise AstralError("projection has no entry node")
        if not graph.traverse(
            self.current_node,
            destination,
            act=act,
            discovered=discovered,
            unlocked_gates=unlocked_gates,
        ):
            raise AstralError(
                f"no visible, open astral route: {self.current_node} -> {destination}"
            )
        self.current_node = destination

    def snapshot(self) -> dict:
        return {
            "mode": self.mode.value,
            "anchor": self.anchor,
            "realm": self.realm,
            "current_node": self.current_node,
            "link_boxes": self.link_boxes,
            "scenes_projected": self.scenes_projected,
            "max_link_boxes": self.max_link_boxes,
        }

    @classmethod
    def from_snapshot(cls, state: dict) -> AstralState:
        return cls(
            mode=AstralMode(str(state.get("mode", AstralMode.EMBODIED.value))),
            anchor=str(state.get("anchor", "")),
            realm=str(state.get("realm", "")),
            current_node=str(state.get("current_node", "")),
            link_boxes=int(state.get("link_boxes", 0)),
            scenes_projected=int(state.get("scenes_projected", 0)),
            max_link_boxes=int(state.get("max_link_boxes", 3)),
        )


@dataclass(frozen=True)
class AstralNode:
    """An author-facing astral node. ``gm_secret`` is never rendered to a player by default."""

    node_id: str
    label: str
    node_type: str = "symbolic_site"
    visibility: str = "public"
    unlock_act: int = 0
    density: int = 3
    description: str = ""

    def __post_init__(self) -> None:
        if not self.node_id:
            raise AstralError("astral node needs an id")
        if self.node_type == "agent":
            raise AstralError(
                "a conscious agent is an occupant of an astral node, never a node: modelling "
                "Noöspace as a network of agents does not make an agent a place (#1261 §4)"
            )
        if self.visibility not in ("public", "discovered", "gm_secret"):
            raise AstralError(f"invalid astral visibility: {self.visibility}")
        if self.unlock_act < 0:
            raise AstralError("unlock_act cannot be negative")
        if not 1 <= self.density <= 7:
            raise AstralError("density must be 1..7")


@dataclass(frozen=True)
class AstralEdge:
    """A directed or undirected astral route with an optional gate."""

    source: str
    target: str
    relation: str = "path"
    directed: bool = True
    gate: str = ""

    def touches(self, node_id: str) -> bool:
        return self.source == node_id or (not self.directed and self.target == node_id)


@dataclass
class AstralGraph:
    """A small validated graph; NetworkX is a later projection, not this file's source of truth."""

    nodes: dict[str, AstralNode] = field(default_factory=dict)
    edges: tuple[AstralEdge, ...] = ()

    def __post_init__(self) -> None:
        if not self.nodes:
            raise AstralError("astral graph needs at least one node")
        for node_id, node in self.nodes.items():
            if node_id != node.node_id:
                raise AstralError(
                    f"node key {node_id!r} does not match node id {node.node_id!r}"
                )
        seen: set[tuple[str, str, str]] = set()
        for edge in self.edges:
            if edge.source not in self.nodes or edge.target not in self.nodes:
                raise AstralError(
                    f"dangling astral edge: {edge.source} -> {edge.target}"
                )
            key = (edge.source, edge.target, edge.relation)
            if key in seen:
                raise AstralError(f"duplicate astral edge: {key}")
            seen.add(key)

    def visible(
        self,
        node_id: str,
        *,
        act: int = 1,
        discovered: frozenset[str] | set[str] = frozenset(),
    ) -> bool:
        node = self.nodes.get(node_id)
        if node is None:
            return False
        if node.visibility == "public":
            return True
        if node.visibility == "discovered":
            return node_id in discovered or act >= node.unlock_act
        # gm_secret: requires both the act gate and an explicit discovery record.
        return act >= node.unlock_act and node_id in discovered

    def neighbors(
        self,
        node_id: str,
        *,
        act: int = 1,
        discovered: frozenset[str] | set[str] = frozenset(),
        unlocked_gates: frozenset[str] | set[str] = frozenset(),
    ) -> tuple[str, ...]:
        if not self.visible(node_id, act=act, discovered=discovered):
            return ()
        found: list[str] = []
        for edge in self.edges:
            if not edge.touches(node_id):
                continue
            if edge.gate and edge.gate not in unlocked_gates:
                continue
            other = edge.target if edge.source == node_id else edge.source
            if self.visible(other, act=act, discovered=discovered):
                found.append(other)
        return tuple(dict.fromkeys(found))

    def relation(self, source: str, destination: str) -> str:
        """The relation label of the edge between two nodes, or ``""`` if they are not adjacent.

        Time/Space navigation needs this: a route there is a resonance, a symbol or a memory, never a
        corridor. The perception layer lives in :mod:`src.rules.astral_body`; this is the graph fact it
        will need when an authored scene navigates symbolically (#1261 §2).
        """
        for edge in self.edges:
            if edge.source == source and edge.target == destination:
                return edge.relation
            if not edge.directed and edge.source == destination and edge.target == source:
                return edge.relation
        return ""

    def traverse(
        self,
        source: str,
        destination: str,
        *,
        act: int = 1,
        discovered: frozenset[str] | set[str] = frozenset(),
        unlocked_gates: frozenset[str] | set[str] = frozenset(),
    ) -> bool:
        return destination in self.neighbors(
            source, act=act, discovered=discovered, unlocked_gates=unlocked_gates
        )


__all__ = [
    "PSI_MATRIX",
    "AstralEdge",
    "AstralError",
    "AstralGraph",
    "AstralMode",
    "AstralNode",
    "AstralState",
    "PermissionStatus",
    "PsiAction",
    "PsiPermission",
    "PsiTarget",
    "PsiVerb",
    "activate",
    "authorize",
    "permission",
]
