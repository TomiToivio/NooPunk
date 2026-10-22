"""JSON save/load support for deterministic RPG sessions."""

from __future__ import annotations

from dataclasses import asdict
import json
from pathlib import Path
from typing import Any

from .engine import RPGSession
from .models import GraphEffect, RPGEvent, RPGState


SAVE_VERSION = 1
MAX_RANDOM_DRAWS = 1_000_000


def session_to_dict(session: RPGSession) -> dict[str, Any]:
    """Return a portable save document without serializing scenario content."""
    return {
        "version": SAVE_VERSION,
        "scenario_id": session.scenario.id,
        "character_id": session.character.id,
        "seed": session.seed,
        "random_draws": session.random_draws,
        "tarot_draws": session.tarot_draws,
        "character": {
            "tags": sorted(session.character.tags),
            "aspects": sorted(session.character.aspects),
            "conditions": sorted(session.character.conditions),
            "consequences": list(session.character.consequences),
            "resources": dict(session.character.resources),
            "reputation": dict(session.character.reputation),
            "advancement": session.character.advancement,
        },
        "state": {
            **asdict(session.state),
            "conditions": sorted(session.state.conditions),
            "known_information": sorted(session.state.known_information),
            "completed_interactions": sorted(session.state.completed_interactions),
        },
        "events": [asdict(event) for event in session.events],
    }


def session_from_dict(data: dict[str, Any], character, scenario) -> RPGSession:
    """Restore a save against explicitly loaded, validated content."""
    if not isinstance(data, dict):
        raise ValueError("Save document must be a JSON object")
    if data.get("version") != SAVE_VERSION:
        raise ValueError(f"Unsupported save version: {data.get('version')}")
    if data.get("scenario_id") != scenario.id or data.get("character_id") != character.id:
        raise ValueError("Save content does not match the supplied character and scenario")

    seed = data.get("seed")
    if seed is not None and (not isinstance(seed, int) or isinstance(seed, bool)):
        raise ValueError("Save seed must be an integer or null")
    draws = data.get("random_draws", 0)
    if not isinstance(draws, int) or isinstance(draws, bool) or not 0 <= draws <= MAX_RANDOM_DRAWS:
        raise ValueError(f"Save random_draws must be between 0 and {MAX_RANDOM_DRAWS}")
    tarot_draws = data.get("tarot_draws", 0)
    if (
        not isinstance(tarot_draws, int)
        or isinstance(tarot_draws, bool)
        or not 0 <= tarot_draws <= MAX_RANDOM_DRAWS
    ):
        raise ValueError(f"Save tarot_draws must be between 0 and {MAX_RANDOM_DRAWS}")

    char = data.get("character", {})
    if not isinstance(char, dict):
        raise ValueError("Save character must be a JSON object")

    raw = data.get("state")
    if not isinstance(raw, dict):
        raise ValueError("Save state must be a JSON object")
    scene_id = raw.get("current_scene")
    if scene_id not in scenario.scenes:
        raise ValueError(f"Save references unknown scene: {scene_id}")
    dialogue_id = raw.get("current_dialogue")
    if dialogue_id is not None and dialogue_id not in scenario.scenes[scene_id].dialogue:
        raise ValueError(f"Save references unknown dialogue: {dialogue_id}")
    current_character = raw.get("current_character")
    if current_character != character.id:
        raise ValueError("Save state character does not match the supplied character")
    restored_state = RPGState(
        current_scene=scene_id,
        current_character=current_character,
        current_dialogue=dialogue_id,
        scene_flags=dict(raw.get("scene_flags", {})),
        campaign_flags=dict(raw.get("campaign_flags", {})),
        conditions=set(raw.get("conditions", [])),
        consequences=list(raw.get("consequences", [])),
        known_information=set(raw.get("known_information", [])),
        completed_interactions=set(raw.get("completed_interactions", [])),
        relationships={key: int(value) for key, value in raw.get("relationships", {}).items()},
        graph_effects=[GraphEffect(**effect) for effect in raw.get("graph_effects", [])],
    )
    restored_events = [RPGEvent(event["type"], dict(event.get("payload", {}))) for event in data.get("events", [])]

    # Commit character mutations only after the complete save structure
    # (state, events, graph effects) has been validated and built.
    # If any validation above raised, the supplied Character is untouched.
    character.tags = set(char.get("tags", []))
    character.aspects = set(char.get("aspects", []))
    character.conditions = set(char.get("conditions", []))
    character.consequences = list(char.get("consequences", []))
    character.resources = dict(char.get("resources", {}))
    character.reputation = dict(char.get("reputation", {}))
    character.advancement = int(char.get("advancement", 0))

    session = RPGSession(character, scenario, seed=seed)
    session.state = restored_state
    session.events = restored_events
    session.restore_random_draws(draws)
    session.restore_tarot_draws(tarot_draws)
    return session


def save_session(session: RPGSession, path: str | Path) -> None:
    Path(path).write_text(
        json.dumps(session_to_dict(session), ensure_ascii=False, indent=2),
        encoding="utf-8",
    )


def load_session(path: str | Path, character, scenario) -> RPGSession:
    return session_from_dict(json.loads(Path(path).read_text(encoding="utf-8")), character, scenario)
