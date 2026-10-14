"""Ideology and Reality Tunnels for NoöPunk factions (issue #469).

Laclau's apparatus — articulation, nodal points, floating signifiers, equivalential chains and
antagonistic frontiers — plus Robert Anton Wilson's Reality Tunnels, as *structure*. This module loads
the four UN parties of the 2045 default scenario (#470) and the Reality Tunnel portraits that read the
same evidence differently.

It defines no mechanic, no number and no rule: a tunnel is a reading, and the readings are marked
PROPOSAL until the author adopts them. `strategy_game/RULEBOOK.md` still reads NO RULES APPROVED.
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Mapping

DATA_DIR = Path(__file__).with_name("data")
PARTIES_PATH = DATA_DIR / "un_parties_2045.json"
TUNNELS_PATH = DATA_DIR / "reality_tunnels.json"

#: Tokens a structure-only framework must never contain.
FORBIDDEN_TOKENS = ("modifier", "bonus", "damage", "threshold", "difficulty")

#: The four stance axes each party must answer for (#470's own acceptance criterion).
STANCE_AXES: tuple[str, ...] = ("soft_psi", "confederacy", "orion", "asi")

#: The evidence every tunnel must read. A Reality Tunnel is a reading *of the same* facts.
EVIDENCE_IDS: tuple[str, ...] = (
    "rogue_agi_incident",
    "soft_psi_revival",
    "confederacy_contact",
    "orion_abductions",
)


@dataclass(frozen=True)
class Party:
    identifier: str
    label: str
    subtitle: str
    stances: Mapping[str, str]
    internal_currents: tuple[str, ...]
    material_base: str
    raw: Mapping[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class Tunnel:
    identifier: str
    label: str
    held_by: str
    nodal_points: tuple[str, ...]
    floating_signifiers: tuple[str, ...]
    equivalential_chain: tuple[str, ...]
    frontier: str
    readings: Mapping[str, str]

    def reading(self, evidence_id: str) -> str:
        return self.readings[evidence_id]


def _load(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def load_parties(path: Path | str | None = None) -> tuple[Party, ...]:
    document = _load(Path(path) if path else PARTIES_PATH)
    parties = []
    for record in document["parties"]:
        parties.append(
            Party(
                identifier=record["id"],
                label=record["label"],
                subtitle=record.get("subtitle", ""),
                stances=dict(record.get("stances") or {}),
                internal_currents=tuple(
                    current["id"] for current in record.get("internal_currents") or []
                ),
                material_base=str(record.get("material_base") or ""),
                raw=record,
            )
        )
    return tuple(parties)


def load_tunnels(path: Path | str | None = None) -> tuple[Tunnel, ...]:
    document = _load(Path(path) if path else TUNNELS_PATH)
    tunnels = []
    for record in document["tunnels"]:
        tunnels.append(
            Tunnel(
                identifier=record["id"],
                label=record["label"],
                held_by=record.get("held_by", ""),
                nodal_points=tuple(record.get("nodal_points") or []),
                floating_signifiers=tuple(record.get("floating_signifiers") or []),
                equivalential_chain=tuple(record.get("equivalential_chain") or []),
                frontier=str(record.get("frontier") or ""),
                readings=dict(record.get("readings") or {}),
            )
        )
    return tuple(tunnels)


def validate(*, parties_path: Path | str | None = None, tunnels_path: Path | str | None = None) -> tuple[str, ...]:
    """Structural problems, refused by name. Empty means the model is well formed."""
    problems: list[str] = []
    try:
        parties = load_parties(parties_path)
        tunnels = load_tunnels(tunnels_path)
    except (OSError, KeyError, ValueError) as error:
        return (f"unreadable: {error}",)

    if len(parties) != 4:
        problems.append(f"{len(parties)} parties declared; the author's decision names four")
    for party in parties:
        head = f"party {party.identifier}"
        missing = [axis for axis in STANCE_AXES if not party.stances.get(axis)]
        if missing:
            problems.append(f"{head}: no stance on {missing}")
        if len(party.internal_currents) < 2:
            problems.append(f"{head}: fewer than two internal currents; the roster is internally plural")
        if not party.material_base.strip():
            problems.append(f"{head}: no material base recorded")

    for tunnel in tunnels:
        head = f"tunnel {tunnel.identifier}"
        missing = [e for e in EVIDENCE_IDS if not tunnel.readings.get(e)]
        if missing:
            problems.append(f"{head}: does not read {missing}; a tunnel reads the same evidence as the others")
        if not tunnel.nodal_points:
            problems.append(f"{head}: no nodal point")
        if not tunnel.frontier.strip():
            problems.append(f"{head}: no antagonistic frontier")

    source = Path(__file__).read_text(encoding="utf-8")
    code = source.split('"""', 2)[-1]
    # the constant above names these on purpose, so its own definition is excluded from the scan
    lines = code.splitlines(keepends=True)
    scanning, scannable = True, []
    for line in lines:
        if "FORBIDDEN_TOKENS" in line:
            scanning = False
        if scanning:
            scannable.append(line)
        if not scanning and line.strip() == ")":
            scanning = True
    for banned in FORBIDDEN_TOKENS:
        if banned in "".join(scannable):
            problems.append(f"the framework contains the mechanic token {banned!r}")
    return tuple(problems)
