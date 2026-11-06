"""Core records for the standalone LaclauGPT social-science simulator (#1286).

This package is not the NoöPunk RPG, not a game engine and not a second rules
resolver. It models synthetic communicating agents and organizations over the
discourse contracts produced by LaclauGPT AI26. Every record carries provenance
and a material class so observed evidence, interpretation, synthesis and
simulation cannot be silently mixed.
"""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass, field
from enum import Enum
from typing import Any

__all__ = [
    "Actor",
    "Articulation",
    "Claim",
    "CommunicationEdge",
    "Material",
    "Provenance",
    "SimulationConfig",
    "SocialEdge",
]


class Material(str, Enum):
    """What kind of material a record represents.

    ``OBSERVED`` is source material, ``INFERRED`` is an interpretive analysis of
    source material, ``SYNTHESIZED`` is a fixture or researcher-authored input and
    ``SIMULATED`` is produced by this package. The distinction survives export.
    """

    OBSERVED = "observed"
    INFERRED = "inferred"
    SYNTHESIZED = "synthesized"
    SIMULATED = "simulated"


def _text(value: Any, field_name: str) -> str:
    text = str(value or "").strip()
    if not text:
        raise ValueError(f"{field_name} must be a non-empty string")
    return text


def _unit_interval(value: float, field_name: str) -> float:
    number = float(value)
    if not 0.0 <= number <= 1.0:
        raise ValueError(f"{field_name} must be between 0 and 1")
    return number


@dataclass(frozen=True, slots=True)
class Provenance:
    """Where a fact came from and how much it should be trusted."""

    material: Material
    source_id: str
    method: str = ""
    uncertainty: float = 0.0
    review_status: str = "PROVISIONAL"
    note: str = ""

    def __post_init__(self) -> None:
        if not isinstance(self.material, Material):
            try:
                object.__setattr__(self, "material", Material(self.material))
            except ValueError as exc:
                raise ValueError(f"unknown material class {self.material!r}") from exc
        _text(self.source_id, "provenance source_id")
        _unit_interval(self.uncertainty, "provenance uncertainty")
        if not str(self.review_status).strip():
            raise ValueError("provenance review_status must be explicit")

    def to_dict(self) -> dict[str, Any]:
        return {
            "material": self.material.value,
            "source_id": self.source_id,
            "method": self.method,
            "uncertainty": self.uncertainty,
            "review_status": self.review_status,
            "note": self.note,
        }

    @classmethod
    def from_dict(cls, raw: Mapping[str, Any]) -> Provenance:
        return cls(
            material=Material(raw["material"]),
            source_id=str(raw["source_id"]),
            method=str(raw.get("method", "")),
            uncertainty=float(raw.get("uncertainty", 0.0)),
            review_status=str(raw.get("review_status", "PROVISIONAL")),
            note=str(raw.get("note", "")),
        )


@dataclass(slots=True)
class Actor:
    """A synthetic individual or organization.

    Attributes are simulation variables, never NoöPunk RPG tags. ``disposition`` is
    a bounded stance toward a claim or signifier; it is not a personality score.
    """

    id: str
    label: str
    kind: str = "individual"
    affiliation: str = ""
    roles: tuple[str, ...] = ()
    resources: float = 1.0
    attention: float = 0.5
    disposition: dict[str, float] = field(default_factory=dict)
    active: bool = True
    provenance: Provenance = field(
        default_factory=lambda: Provenance(Material.SYNTHESIZED, "fixture:actor")
    )

    def __post_init__(self) -> None:
        _text(self.id, "actor id")
        _text(self.label, "actor label")
        if self.kind not in {"individual", "organization"}:
            raise ValueError("actor kind must be 'individual' or 'organization'")
        if not 0.0 <= float(self.resources) <= 1.0:
            raise ValueError("actor resources must be between 0 and 1")
        _unit_interval(float(self.attention), "actor attention")
        for key, value in self.disposition.items():
            _text(key, "disposition key")
            if not -1.0 <= float(value) <= 1.0:
                raise ValueError("disposition values must be between -1 and 1")

    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "label": self.label,
            "kind": self.kind,
            "affiliation": self.affiliation,
            "roles": list(self.roles),
            "resources": self.resources,
            "attention": self.attention,
            "disposition": dict(sorted(self.disposition.items())),
            "active": self.active,
            "provenance": self.provenance.to_dict(),
        }

    @classmethod
    def from_dict(cls, raw: Mapping[str, Any]) -> Actor:
        return cls(
            id=str(raw["id"]),
            label=str(raw["label"]),
            kind=str(raw.get("kind", "individual")),
            affiliation=str(raw.get("affiliation", "")),
            roles=tuple(str(role) for role in raw.get("roles", ())),
            resources=float(raw.get("resources", 1.0)),
            attention=float(raw.get("attention", 0.5)),
            disposition={
                str(k): float(v) for k, v in raw.get("disposition", {}).items()
            },
            active=bool(raw.get("active", True)),
            provenance=Provenance.from_dict(raw["provenance"]),
        )


@dataclass(frozen=True, slots=True)
class SocialEdge:
    """A typed, time-indexed social relation between two actors."""

    source: str
    target: str
    relation: str
    time: int
    provenance: Provenance
    uncertainty: float = 0.0

    def __post_init__(self) -> None:
        _text(self.source, "social edge source")
        _text(self.target, "social edge target")
        _text(self.relation, "social edge relation")
        if self.source == self.target:
            raise ValueError("a social edge must connect two different actors")
        if self.time < 0:
            raise ValueError("social edge time must be non-negative")
        _unit_interval(self.uncertainty, "social edge uncertainty")

    def to_dict(self) -> dict[str, Any]:
        return {
            "source": self.source,
            "target": self.target,
            "relation": self.relation,
            "time": self.time,
            "provenance": self.provenance.to_dict(),
            "uncertainty": self.uncertainty,
        }


@dataclass(frozen=True, slots=True)
class CommunicationEdge:
    """A public or private communication event as a typed edge."""

    source: str
    target: str
    time: int
    channel: str = "public"
    provenance: Provenance = field(
        default_factory=lambda: Provenance(Material.SIMULATED, "fixture:communication")
    )
    uncertainty: float = 0.0

    def __post_init__(self) -> None:
        _text(self.source, "communication source")
        _text(self.target, "communication target")
        if self.source == self.target:
            raise ValueError("a communication edge must connect two different actors")
        if self.time < 0:
            raise ValueError("communication time must be non-negative")
        if self.channel not in {"public", "private"}:
            raise ValueError("communication channel must be 'public' or 'private'")
        _unit_interval(self.uncertainty, "communication uncertainty")

    def to_dict(self) -> dict[str, Any]:
        return {
            "source": self.source,
            "target": self.target,
            "time": self.time,
            "channel": self.channel,
            "provenance": self.provenance.to_dict(),
            "uncertainty": self.uncertainty,
        }


@dataclass(frozen=True, slots=True)
class Claim:
    """A demand, signifier or project represented in the simulation."""

    id: str
    label: str
    owner: str = ""
    kind: str = "demand"
    provenance: Provenance = field(
        default_factory=lambda: Provenance(Material.SYNTHESIZED, "fixture:claim")
    )
    uncertainty: float = 0.0

    def __post_init__(self) -> None:
        _text(self.id, "claim id")
        _text(self.label, "claim label")
        _text(self.kind, "claim kind")
        _unit_interval(self.uncertainty, "claim uncertainty")

    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "label": self.label,
            "owner": self.owner,
            "kind": self.kind,
            "provenance": self.provenance.to_dict(),
            "uncertainty": self.uncertainty,
        }

    @classmethod
    def from_dict(cls, raw: Mapping[str, Any]) -> Claim:
        return cls(
            id=str(raw["id"]),
            label=str(raw["label"]),
            owner=str(raw.get("owner", "")),
            kind=str(raw.get("kind", "demand")),
            provenance=Provenance.from_dict(raw["provenance"]),
            uncertainty=float(raw.get("uncertainty", 0.0)),
        )


@dataclass(frozen=True, slots=True)
class Articulation:
    """An explicit discourse-theoretical relation, never raw co-occurrence."""

    id: str
    left: str
    right: str
    relation: str
    provenance: Provenance
    uncertainty: float = 0.0

    def __post_init__(self) -> None:
        _text(self.id, "articulation id")
        _text(self.left, "articulation left")
        _text(self.right, "articulation right")
        if self.left == self.right:
            raise ValueError("an articulation must connect two different claims")
        if self.relation not in {"equivalence", "difference"}:
            raise ValueError(
                "articulation relation must be 'equivalence' or 'difference'"
            )
        _unit_interval(self.uncertainty, "articulation uncertainty")

    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "left": self.left,
            "right": self.right,
            "relation": self.relation,
            "provenance": self.provenance.to_dict(),
            "uncertainty": self.uncertainty,
        }

    @classmethod
    def from_dict(cls, raw: Mapping[str, Any]) -> Articulation:
        return cls(
            id=str(raw["id"]),
            left=str(raw["left"]),
            right=str(raw["right"]),
            relation=str(raw["relation"]),
            provenance=Provenance.from_dict(raw["provenance"]),
            uncertainty=float(raw.get("uncertainty", 0.0)),
        )


@dataclass(frozen=True, slots=True)
class SimulationConfig:
    """Explicit behavioral assumptions for a run.

    These are research assumptions, not laws derived from LaclauGPT. Changing one
    is a modelling decision and must be reported with the run.
    """

    seed: int = 0
    turns: int = 12
    communication_probability: float = 0.65
    influence_rate: float = 0.20
    coalition_threshold: float = 0.25
    institutional_threshold: float = 0.60
    attention_decay: float = 0.05
    abstention_probability: float = 0.15

    def __post_init__(self) -> None:
        if self.turns < 1:
            raise ValueError("turns must be at least 1")
        for name in (
            "communication_probability",
            "influence_rate",
            "coalition_threshold",
            "institutional_threshold",
            "attention_decay",
            "abstention_probability",
        ):
            _unit_interval(float(getattr(self, name)), name)

    def to_dict(self) -> dict[str, Any]:
        return {
            "seed": self.seed,
            "turns": self.turns,
            "communication_probability": self.communication_probability,
            "influence_rate": self.influence_rate,
            "coalition_threshold": self.coalition_threshold,
            "institutional_threshold": self.institutional_threshold,
            "attention_decay": self.attention_decay,
            "abstention_probability": self.abstention_probability,
        }
