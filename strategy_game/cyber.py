"""Cyberspace reachability: the three eras, access paths, and what is actually illegal (issue #344).

Issue #344's author clarification of 2026-10-13 fixes a **temporal progression** that overrides any
earlier implication that the Blackwall world already exists at the opening of the campaign: the player
starts *before* the NHI Crisis, the internet is still useful, and what changes across the eras is
**network reachability**, not the netrunner's capability. This module carries that model as data and
answers the one question the acceptance criteria demand before any skill roll:

    is an intrusion *physically and logically possible*, and along which access path?

Three of the issue's own rules are what make this a module rather than prose:

* *"An inaccessible air-gapped machine cannot be hacked remotely by narrative fiat."* — a genuinely
  isolated target is refused a remote path in every era.
* *"A social/institutional network edge ... does not mean an Internet route or a hackable TCP/IP
  connection."* — a Castellsian tie is refused **by name** as an access path, so the mistake is loud
  instead of silent.
* *"Keep an accidentally exposed private network distinct from the illegal old-Internet containment
  breach."* — the two illegalities stay two: an INFOSEC failure is not a crime against the
  containment boundary.

What this module is **not**: approved rules. `strategy_game/RULEBOOK.md` still says *NO RULES
APPROVED*. It computes **no** probability, difficulty, detection chance or numeric modifier — it
reports possibility, the path used, and which of the two illegalities applies. Detection risk,
defensive response and the mission's own resolution belong to the author's abstract agent-led mission
system, and the astral half of that engine is `docs/design/ISSUE_224_NOOSPACE_SCOPE.md`, consumed here
rather than restated. Standard library only; no LaclauGPT import.
"""
from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from .provenance import Provenance

__all__ = [
    "ACCESS_MODES",
    "CONNECTIVITY_FORMAT",
    "DATA_PATH",
    "ERA_IDS",
    "ILLEGALITY_CLASSES",
    "REMOTE_INTRUSION_STANCES",
    "AccessAssessment",
    "AccessPath",
    "ConnectivityClass",
    "ConnectivityModel",
    "Era",
    "connectivity_from_dict",
    "load_connectivity",
]

#: The declared file format, so a caller cannot silently load a different document.
CONNECTIVITY_FORMAT = "noopunk.strategy_game.connectivity"

#: The packaged model.
DATA_PATH = Path(__file__).with_name("data") / "connectivity.json"

#: The three campaign periods the author fixed: before the NHI Crisis, during it, and after it.
ERA_IDS: tuple[str, ...] = ("acceleration", "nhi_crisis", "after_crisis")

#: What a connectivity class says about intrusion from off-site. ``impossible`` is a hard block.
REMOTE_INTRUSION_STANCES: tuple[str, ...] = (
    "possible",
    "requires_authorised_path",
    "requires_local_presence",
    "impossible",
)

#: How an access path reaches a target. ``forbidden`` is performable and always a grave crime.
ACCESS_MODES: tuple[str, ...] = ("local", "proxied", "authorized", "remote", "forbidden")

#: The two things that must never be merged into one "cyber crime" tag.
ILLEGALITY_CLASSES: tuple[str, ...] = ("infosec_failure", "containment_breach")

#: Paths that are *not* network routes, whatever a strategy map draws. Refused by name on purpose.
_REFUSED_PATH_IDS: tuple[str, ...] = (
    "social_tie",
    "faction_relationship",
    "network_edge",
    "influence_edge",
    "personal_contact",
)

#: Connectivity classes a remote path can never reach, in any era.
_UNREACHABLE_REMOTELY: tuple[str, ...] = ("local_only", "isolated")


def _strings(value: Any) -> tuple[str, ...]:
    if value is None:
        return ()
    if isinstance(value, str):
        return (value,)
    if isinstance(value, (list, tuple)):
        return tuple(str(item) for item in value)
    return (str(value),)


def _records(value: Any) -> tuple[dict[str, Any], ...]:
    if value is None:
        return ()
    if isinstance(value, dict):
        return (dict(value),)
    if isinstance(value, (list, tuple)):
        return tuple(dict(item) if isinstance(item, dict) else {"value": item} for item in value)
    return ({"value": value},)


@dataclass
class Era:
    """One campaign period. A period, not a difficulty: it changes what is reachable."""

    identifier: str
    label: str
    position: str = ""
    public_network: str = ""
    remote_reach: bool = False
    cross_border_reach: bool = False
    local_links: bool = True
    couriers: str = ""
    typical_hacking: tuple[str, ...] = ()
    note: str = ""
    detail: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        payload = {
            "id": self.identifier,
            "label": self.label,
            "position": self.position,
            "public_network": self.public_network,
            "remote_reach": self.remote_reach,
            "cross_border_reach": self.cross_border_reach,
            "local_links": self.local_links,
            "couriers": self.couriers,
            "typical_hacking": list(self.typical_hacking),
            "note": self.note,
        }
        payload.update(self.detail)
        return payload


@dataclass
class ConnectivityClass:
    """What a target's network situation affords an intruder standing outside it."""

    identifier: str
    label: str
    remote_intrusion: str
    description: str = ""
    note: str = ""
    detail: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        payload = {
            "id": self.identifier,
            "label": self.label,
            "remote_intrusion": self.remote_intrusion,
            "description": self.description,
            "note": self.note,
        }
        payload.update(self.detail)
        return payload


@dataclass
class AccessPath:
    """One way in. The issue's list is exhaustive: an unlisted route is not a route."""

    identifier: str
    label: str
    mode: str
    requires_local_presence: bool = False
    needs_remote_reach: bool = False
    requires_authorisation: bool = False
    illegality: str = ""
    note: str = ""
    detail: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        payload = {
            "id": self.identifier,
            "label": self.label,
            "mode": self.mode,
            "requires_local_presence": self.requires_local_presence,
            "needs_remote_reach": self.needs_remote_reach,
            "requires_authorisation": self.requires_authorisation,
            "illegality": self.illegality,
            "note": self.note,
        }
        payload.update(self.detail)
        return payload


@dataclass
class AccessAssessment:
    """Whether an intrusion is possible, and what it costs legally. No numbers, no odds."""

    target_class: str
    era: str
    access_path: str
    possible: bool
    reason: str
    mode: str = ""
    illegality: str = ""
    is_containment_breach: bool = False
    requires_local_presence: bool = False

    def to_dict(self) -> dict[str, Any]:
        return {
            "target_class": self.target_class,
            "era": self.era,
            "access_path": self.access_path,
            "possible": self.possible,
            "reason": self.reason,
            "mode": self.mode,
            "illegality": self.illegality,
            "is_containment_breach": self.is_containment_breach,
            "requires_local_presence": self.requires_local_presence,
        }


@dataclass
class ConnectivityModel:
    """The loaded model, and the one check: :meth:`resolve_access`."""

    eras: dict[str, Era] = field(default_factory=dict)
    connectivity_classes: dict[str, ConnectivityClass] = field(default_factory=dict)
    access_paths: dict[str, AccessPath] = field(default_factory=dict)
    illegality_classes: dict[str, dict[str, Any]] = field(default_factory=dict)
    refused_path_ids: frozenset[str] = frozenset()
    research_priorities: tuple[dict[str, Any], ...] = ()
    example_mission: dict[str, Any] = field(default_factory=dict)
    containment_event: dict[str, Any] = field(default_factory=dict)
    sources: tuple[str, ...] = ()
    provenance: Provenance = field(default_factory=Provenance)
    detail: dict[str, Any] = field(default_factory=dict)

    # -- lookups ---------------------------------------------------------------------------

    def era(self, era_id: str) -> Era:
        return self.eras[era_id]

    def target_class(self, class_id: str) -> ConnectivityClass:
        return self.connectivity_classes[class_id]

    def access_path(self, path_id: str) -> AccessPath:
        """The named path — refusing, by name, the social relations that are not routes."""
        if path_id in self.refused_path_ids:
            raise ValueError(
                f"{path_id!r} is a social or institutional relation, not an access path: a "
                "Castellsian network edge is not a TCP connection (issue #344)"
            )
        return self.access_paths[path_id]

    def starting_era(self) -> Era:
        for era in self.eras.values():
            if era.position == "starting_era":
                return era
        raise ValueError("no era is marked as the starting era")

    # -- the check -------------------------------------------------------------------------

    def resolve_access(
        self,
        target_class: str,
        era: str,
        access_path: str,
        *,
        local_presence: bool = False,
        authorised: bool = False,
    ) -> AccessAssessment:
        """Can an intrusion reach this target, in this era, by this path?

        ``local_presence`` means a named agent (or a device that operator has already delivered) is at
        the site. ``authorised`` means the faction actually holds the authority the path needs. The
        question this answers is the issue's own: *whether access is physically and logically possible
        before any skill roll* — never how likely it is to succeed.
        """
        target = self.target_class(target_class)
        period = self.era(era)
        path = self.access_path(access_path)

        def verdict(possible: bool, reason: str) -> AccessAssessment:
            return AccessAssessment(
                target_class=target_class,
                era=era,
                access_path=access_path,
                possible=possible,
                reason=reason,
                mode=path.mode,
                illegality=path.illegality,
                is_containment_breach=(
                    self.illegality_classes.get(path.illegality, {}).get("is_containment_breach", False)
                    if path.illegality
                    else False
                ),
                requires_local_presence=path.requires_local_presence,
            )

        # The forbidden route is about the operator's own connection to the quarantined old
        # internet, not about a target class, so it is settled first: it needs to be at the
        # boundary, and it is a grave international crime in every era.
        if path.mode == "forbidden":
            if not local_presence:
                return verdict(False, "bridging the quarantine needs a real physical or authorised route to it")
            return verdict(True, "possible, and a grave international crime in every era")

        if path.requires_authorisation and not authorised:
            return verdict(False, "the path needs authority the faction does not hold")

        if path.needs_remote_reach and not period.remote_reach:
            return verdict(
                False,
                f"in the {period.identifier} period there is no public network to reach it over: "
                "this is now a field operation, not a remote one",
            )

        if target.remote_intrusion == "impossible" or target_class in _UNREACHABLE_REMOTELY:
            if path.mode in {"local", "proxied"}:
                if path.requires_local_presence and not local_presence:
                    return verdict(False, "nothing about this target is reachable from off-site")
                return verdict(True, "a locally delivered connection, which is the only kind that reaches it")
            return verdict(False, "an isolated or local-only system cannot be entered remotely, by any path")

        if target.remote_intrusion == "requires_local_presence":
            if path.mode in {"local", "proxied"}:
                if path.requires_local_presence and not local_presence:
                    return verdict(False, "nothing about this target is reachable from off-site")
                return verdict(True, "a locally delivered connection")
            if path.mode == "authorized":
                return verdict(True, "an authorised connection into the site")
            return verdict(False, "this target has no outside route")

        if path.mode == "remote":
            return verdict(True, "a reachable path exists while the public network is up")

        return verdict(True, "a valid access path to this target")

    # -- reporting -------------------------------------------------------------------------

    def is_containment_breach(self, illegality_id: str) -> bool:
        """The distinction the issue insists on, as a function rather than a comment."""
        return bool(self.illegality_classes.get(illegality_id, {}).get("is_containment_breach", False))

    def off_vocabulary(self) -> tuple[tuple[str, str, str], ...]:
        """``(record_id, field, value)`` for values outside the declared vocabularies, without raising."""
        out: list[tuple[str, str, str]] = []
        for era in self.eras.values():
            if era.identifier not in ERA_IDS:
                out.append((era.identifier, "era", era.identifier))
        for target in self.connectivity_classes.values():
            if target.remote_intrusion not in REMOTE_INTRUSION_STANCES:
                out.append((target.identifier, "remote_intrusion", target.remote_intrusion))
        for path in self.access_paths.values():
            if path.mode not in ACCESS_MODES:
                out.append((path.identifier, "mode", path.mode))
        return tuple(out)


def connectivity_from_dict(data: dict[str, Any]) -> ConnectivityModel:
    """Build the model from the packaged document shape."""
    eras: dict[str, Era] = {}
    for record in _records(data.get("eras")):
        known = {
            "id", "label", "position", "public_network", "remote_reach", "cross_border_reach",
            "local_links", "couriers", "typical_hacking", "note",
        }
        eras[str(record["id"])] = Era(
            identifier=str(record["id"]),
            label=str(record.get("label") or record["id"]),
            position=str(record.get("position") or ""),
            public_network=str(record.get("public_network") or ""),
            remote_reach=bool(record.get("remote_reach")),
            cross_border_reach=bool(record.get("cross_border_reach")),
            local_links=bool(record.get("local_links", True)),
            couriers=str(record.get("couriers") or ""),
            typical_hacking=_strings(record.get("typical_hacking")),
            note=str(record.get("note") or ""),
            detail={key: value for key, value in record.items() if key not in known},
        )

    classes: dict[str, ConnectivityClass] = {}
    for record in _records(data.get("connectivity_classes")):
        known = {"id", "label", "remote_intrusion", "description", "note"}
        classes[str(record["id"])] = ConnectivityClass(
            identifier=str(record["id"]),
            label=str(record.get("label") or record["id"]),
            remote_intrusion=str(record.get("remote_intrusion") or "impossible"),
            description=str(record.get("description") or ""),
            note=str(record.get("note") or ""),
            detail={key: value for key, value in record.items() if key not in known},
        )

    paths: dict[str, AccessPath] = {}
    for record in _records(data.get("access_paths")):
        known = {
            "id", "label", "mode", "requires_local_presence", "needs_remote_reach",
            "requires_authorisation", "illegality", "note",
        }
        paths[str(record["id"])] = AccessPath(
            identifier=str(record["id"]),
            label=str(record.get("label") or record["id"]),
            mode=str(record.get("mode") or "local"),
            requires_local_presence=bool(record.get("requires_local_presence")),
            needs_remote_reach=bool(record.get("needs_remote_reach")),
            requires_authorisation=bool(record.get("requires_authorisation")),
            illegality=str(record.get("illegality") or ""),
            note=str(record.get("note") or ""),
            detail={key: value for key, value in record.items() if key not in known},
        )

    illegality: dict[str, dict[str, Any]] = {}
    for record in _records(data.get("illegality_classes")):
        illegality[str(record.get("id"))] = dict(record)

    refused = _REFUSED_PATH_IDS
    declared_refusals = data.get("refused_as_access_paths")
    if isinstance(declared_refusals, dict):
        refused = tuple(dict.fromkeys((*_REFUSED_PATH_IDS, *_strings(declared_refusals.get("ids")))))

    return ConnectivityModel(
        eras=eras,
        connectivity_classes=classes,
        access_paths=paths,
        illegality_classes=illegality,
        refused_path_ids=frozenset(refused),
        research_priorities=_records(data.get("research_priorities")),
        example_mission=dict(data.get("example_mission") or {}),
        containment_event=dict(data.get("containment_event") or {}),
        sources=_strings(data.get("sources")),
        provenance=Provenance.from_dict(data.get("provenance")),
        detail={
            key: value
            for key, value in data.items()
            if key not in {
                "format", "eras", "connectivity_classes", "access_paths", "illegality_classes",
                "refused_as_access_paths", "research_priorities", "example_mission",
                "containment_event", "sources", "provenance",
            }
        },
    )


def load_connectivity(path: Path | str | None = None) -> ConnectivityModel:
    """Load the packaged model, refusing a document that is not one."""
    target = Path(path) if path is not None else DATA_PATH
    with open(target, encoding="utf-8") as handle:
        data = json.load(handle)
    declared = data.get("format")
    if declared is not None and declared != CONNECTIVITY_FORMAT:
        raise ValueError(f"not a NoöPunk connectivity document: format={declared!r}")
    return connectivity_from_dict(data)
