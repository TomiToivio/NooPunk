"""The proposed strategic agent skill roster, and its mapping from the Fate-side skills (#482).

This module reads ``data/strategic_skills.json``. That file is a **proposal**: issue #482 authorises
the individual (RPG) skill layer and the six skills in it, and explicitly does **not** approve a
strategic roster, a mission list, a probability or a numeric effect. So this module validates and
publishes the proposal, and the RPG layer treats the roster as an injected, optional parameter
(``rpg.skills.validate_skill``) rather than as a constant.

Why a separate module from ``rpg/skills.py``
--------------------------------------------

The six individual skills are an author decision and belong to the sheet, so they are code constants
in the RPG layer. The strategic roster is strategy-layer vocabulary awaiting approval, so it stays
data, outside ``rpg/`` -- the RPG package imports no strategy module and reads no roster file
(``tests/test_rpg_boundary.py`` pins that boundary). A caller that wants a faction-agent check passes
the loaded roster in:

    from strategy_game.rpg.skills import ActionContext, check
    from strategy_game.strategic_skills import load_strategic_roster

    roster = load_strategic_roster()
    check(agent, ActionContext.FACTION_AGENT, Action.OVERCOME, "statecraft", 2, rng=rng,
          strategic_roster=roster)

Nothing here resolves anything, and the roster grants no bonus.
"""
from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Mapping

__all__ = [
    "FORMAT",
    "VERSION",
    "MappingRow",
    "StrategicRosterError",
    "StrategicSkill",
    "load_strategic_roster",
    "mapping_rows",
    "roster_from_dict",
]

FORMAT = "noopunk.strategy_game.strategic_skills"
VERSION = 1
DATA_PATH = Path(__file__).with_name("data") / "strategic_skills.json"

#: The fields a roster entry must carry. A missing one is a broken proposal, not a default.
REQUIRED_SKILL_FIELDS = ("id", "label", "definition", "mission_kinds")


class StrategicRosterError(ValueError):
    """The roster file is not a well-formed *proposal*."""


@dataclass(frozen=True)
class StrategicSkill:
    """One proposed strategic agent skill.

    ``mission_kinds`` names the kinds of faction mission that would check it. Those names are part of
    the same proposal: they describe mission *shapes* (organisational, political, covert, ...), and
    they carry no difficulty, cost, odds or effect.
    """

    id: str
    label: str
    definition: str
    mission_kinds: tuple[str, ...]
    overlaps: str = ""
    #: What the skill is consolidated from on the Fate side, recorded so the mapping is traceable.
    consolidated_from: tuple[str, ...] = ()

    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "label": self.label,
            "definition": self.definition,
            "mission_kinds": list(self.mission_kinds),
            "overlaps": self.overlaps,
            "consolidated_from": list(self.consolidated_from),
        }


@dataclass(frozen=True)
class MappingRow:
    """One row of the Transhumanity's Fate / Fate Core -> proposed strategic skill mapping."""

    source_skill: str
    source: str
    proposed: str
    note: str = ""

    def to_dict(self) -> dict[str, Any]:
        return {
            "source_skill": self.source_skill,
            "source": self.source,
            "proposed": self.proposed,
            "note": self.note,
        }


def _strings(value: Any, field: str, where: str) -> tuple[str, ...]:
    if value is None:
        return ()
    if not isinstance(value, (list, tuple)) or not all(isinstance(v, str) for v in value):
        raise StrategicRosterError(f"{where}: {field} must be a list of strings")
    return tuple(value)


def roster_from_dict(data: Mapping[str, Any]) -> tuple[tuple[StrategicSkill, ...], tuple[MappingRow, ...]]:
    """Validate the proposal and return its roster and mapping, or explain what is wrong with it."""
    if data.get("format") != FORMAT:
        raise StrategicRosterError(f"format must be {FORMAT!r}, got {data.get('format')!r}")
    if data.get("version") != VERSION:
        raise StrategicRosterError(f"version must be {VERSION}, got {data.get('version')!r}")
    status = str(data.get("status") or "")
    if "PROPOSAL" not in status.upper():
        raise StrategicRosterError(
            "the roster must still declare itself a proposal while no strategic roster is approved; "
            f"status was {status!r}"
        )
    records = data.get("strategic_skills")
    if not isinstance(records, list) or not records:
        raise StrategicRosterError("strategic_skills must be a non-empty list")

    roster: list[StrategicSkill] = []
    for index, record in enumerate(records):
        if not isinstance(record, dict):
            raise StrategicRosterError(f"strategic_skills[{index}] must be an object")
        missing = [field for field in REQUIRED_SKILL_FIELDS if not str(record.get(field) or "").strip()]
        if missing:
            raise StrategicRosterError(
                f"strategic_skills[{index}] is missing {', '.join(missing)}"
            )
        roster.append(
            StrategicSkill(
                id=str(record["id"]).strip(),
                label=str(record["label"]).strip(),
                definition=str(record["definition"]).strip(),
                mission_kinds=_strings(record.get("mission_kinds"), "mission_kinds",
                                       f"strategic_skills[{index}]"),
                overlaps=str(record.get("overlaps") or "").strip(),
                consolidated_from=_strings(record.get("consolidated_from"), "consolidated_from",
                                           f"strategic_skills[{index}]"),
            )
        )

    ids = [skill.id for skill in roster]
    if len(set(ids)) != len(ids):
        raise StrategicRosterError(f"duplicate strategic skill ids: {sorted(ids)}")

    rows: list[MappingRow] = []
    for index, record in enumerate(data.get("mapping") or []):
        if not isinstance(record, dict):
            raise StrategicRosterError(f"mapping[{index}] must be an object")
        missing = [f for f in ("source_skill", "source", "proposed") if not str(record.get(f) or "").strip()]
        if missing:
            raise StrategicRosterError(f"mapping[{index}] is missing {', '.join(missing)}")
        proposed = str(record["proposed"]).strip()
        if proposed not in ids:
            raise StrategicRosterError(
                f"mapping[{index}] proposes {proposed!r}, which is not in the roster; a mapping row "
                "must land on a proposed skill"
            )
        rows.append(
            MappingRow(
                source_skill=str(record["source_skill"]).strip(),
                source=str(record["source"]).strip(),
                proposed=proposed,
                note=str(record.get("note") or "").strip(),
            )
        )
    return tuple(roster), tuple(rows)


def load_strategic_roster(path: Path | str | None = None) -> dict[str, StrategicSkill]:
    """The proposed roster, keyed by skill id, ready to hand to ``rpg.skills.check``."""
    roster, _rows = _load(path)
    return {skill.id: skill for skill in roster}


def mapping_rows(path: Path | str | None = None) -> tuple[MappingRow, ...]:
    """The Fate-side -> proposed strategic skill mapping, for the design record and the rulebook."""
    _roster, rows = _load(path)
    return rows


def _load(path: Path | str | None = None) -> tuple[tuple[StrategicSkill, ...], tuple[MappingRow, ...]]:
    source = Path(path) if path is not None else DATA_PATH
    with open(source, encoding="utf-8") as handle:
        return roster_from_dict(json.load(handle))
