"""Layer II: the political-simulation vocabulary, as data only (issue #282, epic #200).

**No rules live here.** This module defines the *containers* for the Laclau/Mouffe/Palonen and
Castells concepts the issue names, and nothing else: no statistics, thresholds, costs, turn
cadence, scoring, transitions, agent decisions or win conditions. Every value stays the author's
to interpret, and the rule-authoring gate for this layer (Gate B in
``docs/RULE_SYSTEM_RESEARCH.md``) is still open.

The design, in one sentence: **the political field is one labelled multiplex graph** — the
theory's concepts are node kinds, and its relations are edge layers on the *existing*
:class:`strategy_game.core.NetworkEdge` rather than a second edge type.

Why that shape:

* it is **abstract** — one structure carries articulation chains, equivalential links,
  antagonistic frontiers and communication ties, so there is no per-concept subsystem to build;
* it is **simple** — no corpus, no model, no extraction pipeline, no numbers;
* it is **gamified** — a player can see which demands are linked to which signifier and where
  the frontier runs, because that is literally the graph.

What is deliberately **NOT** imported from LaclauGPT: its empirical extraction and
interpretation pipeline, its corpora and any real political data, its classifier output, any
confidence score or threshold, and any assumption that its analytical categories are a validated
generative law. The Phase 1 taxonomy *describes* discourse; turning a description into a causal
transition needs its own stated assumptions and author approval.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any

from .provenance import Provenance


class SignifierKind(Enum):
    """A signifier's role in an articulation, as the theory names it.

    Defaults to :attr:`UNSPECIFIED`, on the same principle as
    :attr:`strategy_game.provenance.ProvenanceKind.UNKNOWN`: whether a signifier is nodal,
    floating or empty is an *interpretation* the author makes, so an unlabelled signifier stays
    visibly unlabelled instead of silently reading as ``NODAL``.
    """

    #: Not classified. Deliberately the default.
    UNSPECIFIED = "unspecified"
    #: Partially fixes meaning for a chain of demands (Laclau/Mouffe).
    NODAL = "nodal"
    #: Its meaning is contested between competing chains.
    FLOATING = "floating"
    #: Stands for the chain as a whole while emptying its particular content.
    EMPTY = "empty"


#: The declared signifier labels, so callers can validate without constructing a member.
SIGNIFIER_KINDS: tuple[str, ...] = tuple(kind.value for kind in SignifierKind)


class PoliticalNodeKind(Enum):
    """Which political concept a graph node represents. Used by the view model as ``type``."""

    DEMAND = "demand"
    SIGNIFIER = "signifier"
    FORMATION = "formation"
    FRONTIER = "frontier"


#: Node kinds in the order the view emits them. Factions are emitted before these.
POLITICAL_NODE_KINDS: tuple[str, ...] = tuple(kind.value for kind in PoliticalNodeKind)


class RelationLayer(Enum):
    """The label on a political relation edge.

    A relation is a :class:`strategy_game.core.NetworkEdge` carrying one of these as its
    ``layer``. These are **descriptive labels**, not mechanics: the scaffold does not say what a
    link does, costs, or permits, and no layer implies a strength or a direction of causation.
    """

    #: Linking a demand to a signifier (Laclau/Mouffe articulation).
    ARTICULATION = "articulation"
    #: Demands linked to one another by a shared opposition rather than by content.
    EQUIVALENCE = "equivalence"
    #: An antagonistic relation across a frontier.
    ANTAGONISM = "antagonism"
    #: A communicative tie (Castells). Network-making, programming and switching are *not*
    #: modelled here — only the presence of a tie is recorded.
    COMMUNICATION = "communication"


#: The declared relation labels, so a call site cannot invent a fourth one by accident.
RELATION_LAYERS: tuple[str, ...] = tuple(layer.value for layer in RelationLayer)


@dataclass
class Demand:
    """A claim made by an actor. Data only; nothing here interprets or weighs it."""

    identifier: str
    label: str
    #: The actor making the claim, if declared. Free reference, not resolved by the scaffold.
    claimant_id: str | None = None
    provenance: Provenance = field(default_factory=Provenance)

    def __post_init__(self) -> None:
        self.provenance = Provenance.from_dict(self.provenance)

    def to_dict(self) -> dict[str, Any]:
        return {
            "identifier": self.identifier,
            "label": self.label,
            "claimant_id": self.claimant_id,
            "provenance": self.provenance.to_dict(),
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "Demand":
        return cls(
            identifier=data["identifier"],
            label=data["label"],
            claimant_id=data.get("claimant_id"),
            provenance=Provenance.from_dict(data.get("provenance")),
        )


@dataclass
class Signifier:
    """A signifier that demands can be articulated to."""

    identifier: str
    label: str
    #: A ``SignifierKind``; a bare string is accepted and normalised, so a legacy or
    #: hand-written snapshot loads rather than being rejected.
    kind: SignifierKind | str = SignifierKind.UNSPECIFIED
    provenance: Provenance = field(default_factory=Provenance)

    def __post_init__(self) -> None:
        self.provenance = Provenance.from_dict(self.provenance)
        if isinstance(self.kind, str):
            self.kind = (SignifierKind(self.kind) if self.kind in SIGNIFIER_KINDS
                         else SignifierKind.UNSPECIFIED)

    def to_dict(self) -> dict[str, Any]:
        return {
            "identifier": self.identifier,
            "label": self.label,
            "kind": self.kind.value,
            "provenance": self.provenance.to_dict(),
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "Signifier":
        return cls(
            identifier=data["identifier"],
            label=data["label"],
            kind=data.get("kind", SignifierKind.UNSPECIFIED.value),
            provenance=Provenance.from_dict(data.get("provenance")),
        )


@dataclass
class Formation:
    """A hegemonic formation: a stabilized articulation the player may be part of or against.

    The scaffold does not record strength, coherence, stability or allegiance. Those would be
    mechanics, and this layer has no approved rules.
    """

    identifier: str
    label: str
    provenance: Provenance = field(default_factory=Provenance)

    def __post_init__(self) -> None:
        self.provenance = Provenance.from_dict(self.provenance)

    def to_dict(self) -> dict[str, Any]:
        return {
            "identifier": self.identifier,
            "label": self.label,
            "provenance": self.provenance.to_dict(),
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "Formation":
        return cls(
            identifier=data["identifier"],
            label=data["label"],
            provenance=Provenance.from_dict(data.get("provenance")),
        )


@dataclass
class Frontier:
    """An antagonistic boundary: the us/them division a formation draws.

    A frontier is a *node* rather than an edge, so a player has a single thing to look at when
    the boundary itself is the subject of play. Which formations sit on which side is expressed
    by ordinary relation edges, not by fields here.
    """

    identifier: str
    label: str
    provenance: Provenance = field(default_factory=Provenance)

    def __post_init__(self) -> None:
        self.provenance = Provenance.from_dict(self.provenance)

    def to_dict(self) -> dict[str, Any]:
        return {
            "identifier": self.identifier,
            "label": self.label,
            "provenance": self.provenance.to_dict(),
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "Frontier":
        return cls(
            identifier=data["identifier"],
            label=data["label"],
            provenance=Provenance.from_dict(data.get("provenance")),
        )


def political_node_kind_of(identifier: str, state: Any) -> str | None:
    """Which :class:`PoliticalNodeKind` an identifier belongs to in ``state``, or ``None``.

    A lookup helper for the view model. It interprets nothing about the node's meaning; it only
    answers "which of the four collections holds this id".
    """
    for kind, collection in (
        (PoliticalNodeKind.DEMAND, getattr(state, "demands", ())),
        (PoliticalNodeKind.SIGNIFIER, getattr(state, "signifiers", ())),
        (PoliticalNodeKind.FORMATION, getattr(state, "formations", ())),
        (PoliticalNodeKind.FRONTIER, getattr(state, "frontiers", ())),
    ):
        if any(item.identifier == identifier for item in collection):
            return kind.value
    return None
