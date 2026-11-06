"""The Astral Projection superskill ranks, loaded from one data file (#1261).

The author's governing direction makes rank a statement about *understanding and permission*, not a clock:
rank 1 is lucid, rank 2 perceives the Conscious Agent Network, rank 3 may edit only what it is authorised to
edit, rank 4 studies the planes. This module turns that table into gates a caller can be refused by.

It deliberately does **not** implement ranks 2–4 as play: the author keeps them design-only, and the MVP
allows rank 0–1 at character creation. The gates exist so a later campaign cannot skip the ladder, and so a
test can prove that the ladder has not been skipped.

Source: issue #1261, author comments of 2026-11-06 (15:42 provisional durations, 15:47 ROTE, 15:57 Use
Ident, 16:35 the superskill update that moved Devachanic/Etheric/Buddhic access to rank 4).
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "data" / "rules" / "astral_progression_1261.json"


class AstralProgressionError(ValueError):
    """A rank, technique or plane access the author's table does not allow."""


@dataclass(frozen=True)
class Rank:
    rank: int
    name: str
    status: str
    understanding: str
    perception: tuple[str, ...]
    capability: tuple[str, ...]
    flight: bool
    lower_astral: bool
    time_space: bool
    rote: bool
    ident_learn: bool
    ident_use: bool
    planes: tuple[str, ...]
    akashic: bool
    duration_cap_minutes: int

    @property
    def playable(self) -> bool:
        return self.status == "playable"


def _load() -> dict:
    return json.loads(DATA.read_text(encoding="utf-8"))


def ranks() -> dict[int, Rank]:
    payload = _load()
    table: dict[int, Rank] = {}
    for entry in payload["ranks"]:
        table[int(entry["rank"])] = Rank(
            rank=int(entry["rank"]),
            name=entry["name"],
            status=entry["status"],
            understanding=entry["understanding"],
            perception=tuple(entry["perception"]),
            capability=tuple(entry["capability"]),
            flight=bool(entry["flight"]),
            lower_astral=bool(entry["lower_astral"]),
            time_space=bool(entry["time_space"]),
            rote=bool(entry["rote"]),
            ident_learn=bool(entry["ident_learn"]),
            ident_use=bool(entry["ident_use"]),
            planes=tuple(entry["planes"]),
            akashic=bool(entry["akashic"]),
            duration_cap_minutes=int(entry["duration_cap_minutes"]),
        )
    return table


def rank_of(value: int) -> Rank:
    """The rank record, refusing anything outside 0–4."""
    table = ranks()
    try:
        return table[int(value)]
    except (KeyError, TypeError, ValueError) as exc:
        raise AstralProgressionError(f"Astral Projection rank must be 0..4, got {value!r}") from exc


def mvp_max_rank() -> int:
    return int(_load()["mvp_max_rank"])


def require_playable(value: int) -> Rank:
    """Refuse a rank the author keeps design-only. Used by play entry points, not by the design data."""
    rank = rank_of(value)
    if rank.rank > mvp_max_rank():
        raise AstralProgressionError(
            f"rank {rank.rank} ({rank.name}) is design-only; the initial campaign allows 0..{mvp_max_rank()}"
        )
    return rank


def require_starting_rank(value: int) -> Rank:
    """Character creation may start at 0 or 1 and not above."""
    if int(value) > mvp_max_rank():
        raise AstralProgressionError(
            f"a character may not start above Astral Projection {mvp_max_rank()}"
        )
    return require_playable(value)


#: Techniques the author has named, with the rank that first permits each one.
_TECHNIQUE_RANK = {"rote": 2, "learn_ident": 2, "use_ident": 3}


def require_technique(value: int, technique: str) -> None:
    """Refuse a technique below its author-defined rank — ROTE at 1, or Use Ident at 2."""
    key = technique.strip().lower()
    if key not in _TECHNIQUE_RANK:
        raise AstralProgressionError(f"unknown Astral Projection technique {technique!r}")
    rank = rank_of(value)
    needed = _TECHNIQUE_RANK[key]
    if rank.rank < needed:
        raise AstralProgressionError(
            f"{technique} needs Astral Projection {needed}; the character has {rank.rank}"
        )


def require_plane(value: int, plane: str) -> None:
    """Devachanic, Etheric and Buddhic access is rank 4 in the governing direction, not rank 2."""
    key = plane.strip().lower()
    rank = rank_of(value)
    if key not in {name.lower() for name in rank.planes}:
        raise AstralProgressionError(
            f"{plane} is not available at Astral Projection {rank.rank}"
            + (" (it needs rank 4)" if key in {"devachanic", "etheric", "buddhic"} else "")
        )


def assert_astral_domain_only() -> None:
    """Every rank is confined to the Astral: no physical, Cyber or hacking permission exists here.

    The function exists so a caller or a test can state the boundary instead of trusting the docstring.
    """
    for rank in ranks().values():
        joined = " ".join(rank.capability).lower()
        for forbidden in ("program check", "hack", "root access", "teleport the body", "resurrect"):
            if forbidden in joined:
                raise AstralProgressionError(
                    f"rank {rank.rank} claims a non-astral power ({forbidden!r}); the superskill is "
                    "astral-domain only"
                )


def duration_cap_minutes(value: int) -> int:
    """The provisional ceiling, returned with no pretence that the author has finalised it."""
    return rank_of(value).duration_cap_minutes
