"""Load the seeded UNSA social world into an Evennia character (#1042).

The seed file is data, not canon: actors, roles and quoted positions come from the campaign content
that already exists. The world itself lives on the character, so a player's observations accumulate
and survive a restart, and nothing here needs an LLM.
"""
from __future__ import annotations

import json
from pathlib import Path

from nopunk_mud.discourse import Actor, Event, SocialWorld

SEED_PATH = Path(__file__).resolve().parents[2] / "data" / "world" / "social_seed_1042.json"


def seed_world(path: Path | None = None) -> SocialWorld:
    """Build a world from the seed file, ingesting its events in order."""
    payload = json.loads((path or SEED_PATH).read_text(encoding="utf-8"))
    world = SocialWorld()
    for raw in payload.get("actors", []):
        world.add_actor(Actor(**raw))
    for actor_id, profile in (payload.get("profiles") or {}).items():
        from nopunk_mud.discourse import DiscourseProfile

        world.profiles[actor_id] = DiscourseProfile(**profile)
    for raw in payload.get("events", []):
        world.ingest(Event(**raw))
    return world


def world_for(store) -> SocialWorld:
    """Load this character's world, seeding it once. ``store`` is anything with a ``.db``."""
    raw = getattr(store.db, "social_world", None)
    if raw:
        return SocialWorld.from_dict(dict(raw))
    world = seed_world()
    store.db.social_world = world.to_dict()
    return world


def remember(store, world: SocialWorld) -> None:
    store.db.social_world = world.to_dict()
