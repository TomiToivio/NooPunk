"""Versioned persistence for the Streamlit Day 1 vertical slice."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

from src.hacking import LayeredHackingSession
from src.rpg import RPGSession, load_character, load_scenario, session_from_dict, session_to_dict
from src.sim.social import SocialSimulation

FORMAT = "noopunk-day-1-integrated"
VERSION = 1


@dataclass(frozen=True)
class Day1WebState:
    rpg: RPGSession
    social: SocialSimulation
    social_effects: int
    hacking: LayeredHackingSession | None
    hacking_applied: bool


def to_dict(
    rpg: RPGSession,
    social: SocialSimulation,
    social_effects: int,
    hacking: LayeredHackingSession | None,
    hacking_applied: bool,
) -> dict[str, Any]:
    if not 0 <= social_effects <= len(rpg.state.graph_effects):
        raise ValueError("Applied social effect count is invalid")
    return {
        "format": FORMAT,
        "version": VERSION,
        "rpg": session_to_dict(rpg),
        "social": social.to_dict(),
        "social_effects": social_effects,
        "hacking": hacking.to_save_dict() if hacking is not None else None,
        "hacking_applied": bool(hacking_applied),
    }


def from_dict(
    data: dict[str, Any],
    character_path: str | Path,
    scenario_path: str | Path,
    people_records: list[dict[str, object]],
    relationship_records: list[dict[str, object]],
) -> Day1WebState:
    """Restore an integrated save; legacy RPG-only saves remain loadable."""
    character = load_character(character_path)
    scenario = load_scenario(scenario_path)
    if not isinstance(data, dict):
        raise TypeError("Save must be a JSON object")

    if data.get("format") != FORMAT:
        rpg = session_from_dict(data, character, scenario)
        social = SocialSimulation.from_lab_data(people_records, relationship_records)
        return Day1WebState(rpg, social, 0, None, False)

    if data.get("version") != VERSION:
        raise ValueError(f"Unsupported integrated save version: {data.get('version')}")
    rpg = session_from_dict(data["rpg"], character, scenario)
    social = SocialSimulation.from_dict(data["social"])
    social_effects = int(data.get("social_effects", 0))
    if not 0 <= social_effects <= len(rpg.state.graph_effects):
        raise ValueError("Applied social effect count is invalid")
    raw_hacking = data.get("hacking")
    hacking = None if raw_hacking is None else LayeredHackingSession.from_save_dict(
        rpg.character, raw_hacking
    )
    hacking_applied = data.get("hacking_applied", False)
    if not isinstance(hacking_applied, bool):
        raise TypeError("Hacking transfer marker must be a boolean")
    if hacking_applied and hacking is None:
        raise ValueError("A missing hacking session cannot have an applied transfer")
    return Day1WebState(rpg, social, social_effects, hacking, hacking_applied)
