"""Layer II political field: an abstract Laclau/Castells vocabulary, containers only (issue #282).

This module gives the political-simulation layer a **small abstract vocabulary** rather than a port
of LaclauGPT: Laclau and Mouffe's demands, signifiers and their roles, articulations and antagonistic
frontiers, plus Castells' modes of communicative power. It implements **no rules** — no transitions,
no scores, no thresholds, no turn cadence, no win conditions — matching the issue's "code only empty
interfaces, data containers, serialization" and the Gate B requirement in
``docs/RULE_SYSTEM_RESEARCH.md``.

Two boundaries are deliberate, and both are asserted by tests rather than left as prose:

* **LaclauGPT is not imported.** The theory is used as vocabulary, never as a dependency: nothing
  here loads the LaclauGPT package, its classifier or its pipeline, and no analytic label is turned
  into a causal formula (``docs/INTEGRATION_BOUNDARIES.md``).
* **Hegemony is a relation, not a score.** A formation's standing is read from which demands are
  articulated to which signifier and who sits inside or outside a frontier. No numeric quantity is
  stored anywhere in this layer, because "political hegemony is not automatically a scalar score"
  (``docs/RULE_SYSTEM_RESEARCH.md``).

The proposed but **unapproved** play loop is described in ``docs/POLITICAL_SIMULATION_DESIGN.md``.
The field is not wired into :class:`~strategy_game.core.WorldState`: integrating the two layers is a
Gate D decision, so for now the field refers to leaders and factions by id.
"""
from __future__ import annotations

import json
from dataclasses import dataclass, field
from enum import Enum
from typing import Any

from .provenance import Provenance

__all__ = [
    "POWER_MODES",
    "SIGNIFIER_ROLES",
    "Articulation",
    "CommunicativeTie",
    "Demand",
    "Frontier",
    "PoliticalField",
    "PoliticalFormation",
    "PowerMode",
    "Signifier",
    "SignifierRole",
]


class SignifierRole(Enum):
    """Laclau's roles for a signifier. Descriptive categories, not a strength scale."""

    #: Demands are articulated around it; the centre of a chain.
    NODAL = "nodal"
    #: Formations compete to give it their own content.
    FLOATING = "floating"
    #: Holds a chain together while its content stays under-determined.
    EMPTY = "empty"


#: The declared value set, so callers can validate without constructing an enum member.
SIGNIFIER_ROLES: tuple[str, ...] = tuple(role.value for role in SignifierRole)


class PowerMode(Enum):
    """Castells' modes of communicative power. Descriptive categories."""

    #: Setting the meaning a network carries.
    PROGRAMMING = "programming"
    #: Connecting or disconnecting networks.
    SWITCHING = "switching"


#: The declared value set, so callers can validate without constructing an enum member.
POWER_MODES: tuple[str, ...] = tuple(mode.value for mode in PowerMode)


def _provenance(value: Any) -> Provenance:
    """Coerce a provenance payload: a ``Provenance``, a dict, a legacy string or ``None``."""
    return value if isinstance(value, Provenance) else Provenance.from_dict(value)


def _role(value: Any) -> SignifierRole | None:
    """Read a recorded role, or ``None`` when it is absent or unrecognised.

    An unrecorded role stays ``None`` instead of defaulting to a role. That is the same rule that
    keeps provenance ``UNKNOWN``: an absence is left visible rather than being silently upgraded
    into an assertion about the signifier.
    """
    if value is None or isinstance(value, SignifierRole):
        return value
    try:
        return SignifierRole(str(value))
    except ValueError:
        return None


def _mode(value: Any) -> PowerMode | None:
    """Read a recorded power mode, or ``None`` when it is absent or unrecognised."""
    if value is None or isinstance(value, PowerMode):
        return value
    try:
        return PowerMode(str(value))
    except ValueError:
        return None


@dataclass
class Demand:
    """A claim voiced by a constituency: the unit Laclau's populist reason works on."""

    identifier: str
    text: str = ""
    provenance: Provenance = field(default_factory=Provenance)

    def __post_init__(self) -> None:
        self.provenance = _provenance(self.provenance)

    def to_dict(self) -> dict[str, Any]:
        return {
            "identifier": self.identifier,
            "text": self.text,
            "provenance": self.provenance.to_dict(),
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "Demand":
        return cls(
            identifier=data["identifier"],
            text=data.get("text", ""),
            provenance=_provenance(data.get("provenance")),
        )


@dataclass
class Signifier:
    """A name that demands are articulated to. Its role is descriptive and may be unrecorded."""

    identifier: str
    label: str = ""
    role: SignifierRole | None = None
    provenance: Provenance = field(default_factory=Provenance)

    def __post_init__(self) -> None:
        self.role = _role(self.role)
        self.provenance = _provenance(self.provenance)

    def to_dict(self) -> dict[str, Any]:
        return {
            "identifier": self.identifier,
            "label": self.label,
            "role": None if self.role is None else self.role.value,
            "provenance": self.provenance.to_dict(),
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "Signifier":
        return cls(
            identifier=data["identifier"],
            label=data.get("label", ""),
            role=_role(data.get("role")),
            provenance=_provenance(data.get("provenance")),
        )


@dataclass
class Articulation:
    """An equivalential link: a demand attached to a signifier (Laclau & Mouffe)."""

    signifier_id: str
    demand_id: str
    provenance: Provenance = field(default_factory=Provenance)

    def __post_init__(self) -> None:
        self.provenance = _provenance(self.provenance)

    def to_dict(self) -> dict[str, Any]:
        return {
            "signifier_id": self.signifier_id,
            "demand_id": self.demand_id,
            "provenance": self.provenance.to_dict(),
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "Articulation":
        return cls(
            signifier_id=data["signifier_id"],
            demand_id=data["demand_id"],
            provenance=_provenance(data.get("provenance")),
        )


@dataclass
class Frontier:
    """An antagonistic divide around a signifier: who is inside the chain, who is excluded."""

    identifier: str
    signifier_id: str = ""
    included_demand_ids: list[str] = field(default_factory=list)
    excluded_demand_ids: list[str] = field(default_factory=list)
    provenance: Provenance = field(default_factory=Provenance)

    def __post_init__(self) -> None:
        self.provenance = _provenance(self.provenance)

    def to_dict(self) -> dict[str, Any]:
        return {
            "identifier": self.identifier,
            "signifier_id": self.signifier_id,
            "included_demand_ids": list(self.included_demand_ids),
            "excluded_demand_ids": list(self.excluded_demand_ids),
            "provenance": self.provenance.to_dict(),
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "Frontier":
        return cls(
            identifier=data["identifier"],
            signifier_id=data.get("signifier_id", ""),
            included_demand_ids=list(data.get("included_demand_ids", [])),
            excluded_demand_ids=list(data.get("excluded_demand_ids", [])),
            provenance=_provenance(data.get("provenance")),
        )


@dataclass
class CommunicativeTie:
    """A Castellsian communicative relation between two actors, in a declared mode.

    ``source_id`` and ``target_id`` are ids of records elsewhere (a leader, a faction, or a
    signifier). The scaffold stores the relation and never derives reach or influence from it.
    """

    source_id: str
    target_id: str
    mode: PowerMode | None = None
    provenance: Provenance = field(default_factory=Provenance)

    def __post_init__(self) -> None:
        self.mode = _mode(self.mode)
        self.provenance = _provenance(self.provenance)

    def to_dict(self) -> dict[str, Any]:
        return {
            "source_id": self.source_id,
            "target_id": self.target_id,
            "mode": None if self.mode is None else self.mode.value,
            "provenance": self.provenance.to_dict(),
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "CommunicativeTie":
        return cls(
            source_id=data["source_id"],
            target_id=data["target_id"],
            mode=_mode(data.get("mode")),
            provenance=_provenance(data.get("provenance")),
        )


@dataclass
class PoliticalFormation:
    """An *inferred* bloc: the signifiers an observer reads as one articulated position.

    "Inferred" is deliberate. A formation is not a party, a population or a measured quantity, and
    the scaffold neither derives it nor scores it — the author records it.
    """

    identifier: str
    label: str = ""
    signifier_ids: list[str] = field(default_factory=list)
    provenance: Provenance = field(default_factory=Provenance)

    def __post_init__(self) -> None:
        self.provenance = _provenance(self.provenance)

    def to_dict(self) -> dict[str, Any]:
        return {
            "identifier": self.identifier,
            "label": self.label,
            "signifier_ids": list(self.signifier_ids),
            "provenance": self.provenance.to_dict(),
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "PoliticalFormation":
        return cls(
            identifier=data["identifier"],
            label=data.get("label", ""),
            signifier_ids=list(data.get("signifier_ids", [])),
            provenance=_provenance(data.get("provenance")),
        )


@dataclass
class PoliticalField:
    """The Layer II container. Data only: no transition, no score, no cadence."""

    schema_version: str = "political-1"
    demands: list[Demand] = field(default_factory=list)
    signifiers: list[Signifier] = field(default_factory=list)
    articulations: list[Articulation] = field(default_factory=list)
    frontiers: list[Frontier] = field(default_factory=list)
    ties: list[CommunicativeTie] = field(default_factory=list)
    formations: list[PoliticalFormation] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        """Plain-JSON representation. Nested records are serialized explicitly."""
        return {
            "schema_version": self.schema_version,
            "demands": [item.to_dict() for item in self.demands],
            "signifiers": [item.to_dict() for item in self.signifiers],
            "articulations": [item.to_dict() for item in self.articulations],
            "frontiers": [item.to_dict() for item in self.frontiers],
            "ties": [item.to_dict() for item in self.ties],
            "formations": [item.to_dict() for item in self.formations],
        }

    def to_json(self) -> str:
        return json.dumps(self.to_dict(), ensure_ascii=False, sort_keys=True)

    @classmethod
    def from_json(cls, text: str) -> "PoliticalField":
        return cls.from_dict(json.loads(text))

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "PoliticalField":
        # ``.get`` so a snapshot written before a collection existed still loads.
        return cls(
            schema_version=data.get("schema_version", "political-1"),
            demands=[Demand.from_dict(item) for item in data.get("demands", [])],
            signifiers=[Signifier.from_dict(item) for item in data.get("signifiers", [])],
            articulations=[Articulation.from_dict(item) for item in data.get("articulations", [])],
            frontiers=[Frontier.from_dict(item) for item in data.get("frontiers", [])],
            ties=[CommunicativeTie.from_dict(item) for item in data.get("ties", [])],
            formations=[PoliticalFormation.from_dict(item) for item in data.get("formations", [])],
        )

    # -- read-only structural queries: no transition, no scoring ---------------------
    def demands_of(self, signifier_id: str) -> tuple[str, ...]:
        """Demand ids articulated to ``signifier_id``, in the order they were recorded."""
        return tuple(a.demand_id for a in self.articulations if a.signifier_id == signifier_id)

    def signifiers_of(self, demand_id: str) -> tuple[str, ...]:
        """Signifier ids that ``demand_id`` is articulated to, in the order they were recorded."""
        return tuple(a.signifier_id for a in self.articulations if a.demand_id == demand_id)
