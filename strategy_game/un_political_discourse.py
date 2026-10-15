"""Read-only four-party UN discourse and Reality Tunnel data (#469, #470).

No opinion scores, persuasion probabilities, turn effects or hidden truth resolver.
"""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

DATA_PATH = Path(__file__).with_name("data") / "un_political_discourse.json"
FORMAT = "noopunk.strategy_game.un_political_discourse"


def load_un_political_discourse(path: str | Path | None = None) -> dict[str, Any]:
    """Return descriptive data with future-party-compatible validation."""
    with open(path or DATA_PATH, encoding="utf-8") as stream:
        payload = json.load(stream)
    if payload.get("format") != FORMAT:
        raise ValueError("Unsupported UN discourse format")
    entries = payload.get("parties")
    if not isinstance(entries, list):
        raise ValueError("Parties must be an array")
    identifiers = [p.get("id") for p in entries if isinstance(p, dict)]
    if len(identifiers) != len(entries) or any(not x for x in identifiers) or len(set(identifiers)) != len(entries):
        raise ValueError("Party identifiers must be present and unique")
    return payload


def interpret_event(event_id: str, *, path: str | Path | None = None) -> dict[str, Any]:
    """Describe each party's pre-authored stance; never assert an event is true.

    This is a view, NOT an agent decision, rule, score or event resolution.
    """
    data = load_un_political_discourse(path)
    event = next((e for e in data["example_events"] if e["id"] == event_id), None)
    if event is None:
        raise KeyError(event_id)
    return {
        "event": dict(event),
        "party_readings": [
            {
                "party_id": party["id"],
                "party_name": party["name"],
                "stance": party["stances"].get(event["topic"]),
                "reality_tunnel": party["reality_tunnel"]["interpretation"],
                "evidence_status": party["reality_tunnel"]["evidence_status"],
            }
            for party in data["parties"]
        ],
    }


def relation_between(party_a, party_b, *, path=None):
    """The declared relation between two parties, or None when none is recorded.

    A view over authored data: it decides nothing and joins no side.
    """
    wanted = {party_a, party_b}
    for relation in load_un_political_discourse(path).get("relations", []):
        if set(relation.get("between", [])) == wanted:
            return dict(relation)
    return None


def majority_reaction(event_id, *, path=None):
    """The unaligned majority's reading of one event. Never a faction, never an opinion score."""
    data = load_un_political_discourse(path)
    event = next((e for e in data["example_events"] if e["id"] == event_id), None)
    if event is None:
        raise KeyError(event_id)
    return str(event.get("majority_reaction") or "")
