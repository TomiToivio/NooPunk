"""Connectivity classes and authorisation rungs (#1200).

The point of this module is a **permission question**, not a dice roll: after the collapse of the old Internet, the
network class decides whether a remote attempt is even possible. A closed organisational network cannot be reached
from outside — no CWN Hacking check, however good, substitutes for a body, a badge or a medium in the room.

Nothing here resolves an intrusion. CWN Hacking stays the resolver; this module only answers *may this be attempted
at all, and who has to sign for it*.
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Mapping

__all__ = [
    "NetworkError", "Network", "AuthorisationRung", "Topology",
    "load_topology", "DEFAULT_TOPOLOGY",
]

DEFAULT_TOPOLOGY = Path(__file__).resolve().parents[2] / "data" / "world" / "networks.json"


class NetworkError(ValueError):
    """Raised when a reachability question breaks the topology contract."""


@dataclass(frozen=True, slots=True)
class Network:
    id: str
    name: str
    kind: str
    owner: str
    remotely_reachable: bool
    requires_physical_access: bool
    requires_credential: bool
    risk: str
    description: str = ""

    def __post_init__(self) -> None:
        if self.requires_physical_access and self.remotely_reachable:
            raise NetworkError(
                f"{self.id!r}: a network cannot require physical access and be remotely reachable at the same time"
            )


@dataclass(frozen=True, slots=True)
class AuthorisationRung:
    rung: int
    action: str
    authority: str
    signer: str

    def __post_init__(self) -> None:
        if self.rung < 0:
            raise NetworkError("an authorisation rung cannot be negative")


@dataclass(frozen=True, slots=True)
class Topology:
    perimeter_name: str
    informal_perimeter_name: str
    subsystem_codename: str | None
    operated_by: str
    networks: tuple[Network, ...]
    rungs: tuple[AuthorisationRung, ...]

    def network(self, network_id: str) -> Network:
        for network in self.networks:
            if network.id == network_id:
                return network
        raise NetworkError(f"unknown network {network_id!r}")

    # -- the one permission question ----------------------------------------------------------
    def can_attempt(
        self,
        network_id: str,
        *,
        remote: bool,
        on_site: bool = False,
        has_credential: bool = False,
    ) -> tuple[bool, str]:
        """May an intrusion be attempted at all? Returns (allowed, reason)."""
        network = self.network(network_id)
        if remote and not network.remotely_reachable:
            return False, (
                f"{network.name}: no remote path exists; a terminal, a badge or a medium has to be in the room"
            )
        if network.requires_physical_access and not on_site:
            return False, f"{network.name}: physical access is required"
        if network.requires_credential and not has_credential:
            return False, f"{network.name}: an account or credential is required"
        if network.id == "old_internet":
            return True, f"{network.name}: attempted, but the network is hostile — the risk is the scene"
        return True, f"{network.name}: prerequisites met; CWN Hacking resolves the attempt"

    # -- who signs ----------------------------------------------------------------------------
    def rung_for(self, action: str) -> AuthorisationRung:
        for rung in self.rungs:
            if rung.action == action:
                return rung
        raise NetworkError(f"unknown action {action!r}")

    def requires_warrant(self, action: str) -> bool:
        return "warrant" in self.rung_for(action).authority


def _network(raw: Mapping[str, Any]) -> Network:
    return Network(
        id=str(raw["id"]),
        name=str(raw["name"]),
        kind=str(raw["kind"]),
        owner=str(raw["owner"]),
        remotely_reachable=bool(raw["remotely_reachable"]),
        requires_physical_access=bool(raw["requires_physical_access"]),
        requires_credential=bool(raw["requires_credential"]),
        risk=str(raw["risk"]),
        description=str(raw.get("description", "")),
    )


def load_topology(path: str | Path | None = None) -> Topology:
    raw = json.loads(Path(path or DEFAULT_TOPOLOGY).read_text(encoding="utf-8"))
    perimeter = raw.get("perimeter", {})
    return Topology(
        perimeter_name=str(perimeter.get("name", "")),
        informal_perimeter_name=str(perimeter.get("informal_name", "")),
        subsystem_codename=perimeter.get("subsystem_codename"),
        operated_by=str(perimeter.get("operated_by", "")),
        networks=tuple(_network(entry) for entry in raw.get("networks", ())),
        rungs=tuple(
            AuthorisationRung(
                rung=int(entry["rung"]),
                action=str(entry["action"]),
                authority=str(entry["authority"]),
                signer=str(entry["signer"]),
            )
            for entry in raw.get("authorisation_rungs", ())
        ),
    )
