"""Persistent EP2 action/observation seam; no LLM may supply dice or ratings."""
from __future__ import annotations

from dataclasses import asdict
import json
from pathlib import Path
import random
import sqlite3
from typing import Any, Mapping, Protocol

from eclipse_phase_homebrew import (
    EP2Character,
    EP2Embodiment,
    EP2GearItem,
    EP2Inventory,
    EP2PoolState,
)
from .ep2_adapter import resolve_ep2_action


class Observer(Protocol):
    def observe(self, observation: str) -> None: ...


class EP2Session:
    """SQLite-backed characters, legal GM-authored tests and shared event memory.

    Each accepted test commits the pool update, RNG state and event together.
    Observers receive committed facts; failed delivery does not undo an event.
    """

    def __init__(self, path: str | Path, *, seed: int = 0):
        self.db = sqlite3.connect(path)
        self.db.execute("CREATE TABLE IF NOT EXISTS state (id INTEGER PRIMARY KEY, payload TEXT NOT NULL)")
        self.db.execute("CREATE TABLE IF NOT EXISTS events (id INTEGER PRIMARY KEY, payload TEXT NOT NULL)")
        self.rng = random.Random(seed)
        row = self.db.execute("SELECT payload FROM state WHERE id=1").fetchone()
        if row:
            self.state = json.loads(row[0])
            self.rng.setstate(self._tuples(self.state["rng"]))
        else:
            self.state = {"version": 1, "characters": {}, "actions": {}, "world": {}}
            self._save()

    @staticmethod
    def _tuples(value):
        return tuple(EP2Session._tuples(v) for v in value) if isinstance(value, list) else value

    def _save(self):
        self.state["rng"] = self.rng.getstate()
        self.db.execute("INSERT OR REPLACE INTO state VALUES (1, ?)", (json.dumps(self.state),))
        self.db.commit()

    def _record_event(self, event: dict[str, Any]) -> dict[str, Any]:
        """Atomically persist current state and one already-resolved event."""
        self.state["rng"] = self.rng.getstate()
        with self.db:
            cursor = self.db.execute(
                "INSERT INTO events(payload) VALUES (?)",
                (json.dumps(event),),
            )
            self.db.execute(
                "UPDATE state SET payload=? WHERE id=1",
                (json.dumps(self.state),),
            )
        return {**event, "id": cursor.lastrowid}

    def close(self):
        self.db.close()

    def add_character(
        self,
        actor: str,
        character: EP2Character,
        pools: EP2PoolState,
        *,
        embodiment: EP2Embodiment | None = None,
        inventory: EP2Inventory | None = None,
    ):
        if not actor or actor in self.state["characters"]:
            raise ValueError("Actor ID must be nonempty and unique.")
        active_embodiment = embodiment
        if active_embodiment is None and character.morph:
            active_embodiment = EP2Embodiment(
                name=character.morph,
                durability=character.durability or 30,
                wound_threshold=character.wound_threshold or 6,
            )
        self.state["characters"][actor] = {
            "sheet": asdict(character),
            "maximum": dict(pools.maximum),
            "current": dict(pools.current),
            "embodiment": asdict(active_embodiment) if active_embodiment else None,
            "inventory": {
                item_id: asdict(item)
                for item_id, item in (inventory or EP2Inventory()).items.items()
            },
        }
        self._save()

    def character_state(self, actor: str) -> dict[str, Any]:
        if actor not in self.state["characters"]:
            raise ValueError("Unknown actor.")
        return self.state["characters"][actor]

    def inventory(self, actor: str) -> EP2Inventory:
        stored = self.character_state(actor)
        return EP2Inventory(
            items={
                item_id: EP2GearItem(**payload)
                for item_id, payload in stored.get("inventory", {}).items()
            }
        )

    def set_embodiment(self, actor: str, embodiment: EP2Embodiment) -> dict[str, Any]:
        """Persist a resleeve/body-platform change as an explicit world event."""
        stored = self.character_state(actor)
        previous = stored.get("embodiment")
        stored["embodiment"] = asdict(embodiment)
        event = {
            "actor": actor,
            "action": "set_embodiment",
            "result": {
                "previous": previous,
                "current": asdict(embodiment),
            },
        }
        return self._record_event(event)

    def add_gear(self, actor: str, item: EP2GearItem) -> dict[str, Any]:
        stored = self.character_state(actor)
        inventory = self.inventory(actor)
        inventory.add(item)
        stored["inventory"] = {
            item_id: asdict(gear) for item_id, gear in inventory.items.items()
        }
        event = {
            "actor": actor,
            "action": "add_gear",
            "result": asdict(item),
        }
        return self._record_event(event)

    def remove_gear(self, actor: str, item_id: str, quantity: int = 1) -> dict[str, Any]:
        stored = self.character_state(actor)
        inventory = self.inventory(actor)
        removed = inventory.remove(item_id, quantity)
        stored["inventory"] = {
            gear_id: asdict(gear) for gear_id, gear in inventory.items.items()
        }
        event = {
            "actor": actor,
            "action": "remove_gear",
            "result": asdict(removed),
        }
        return self._record_event(event)

    def offer_action(self, actor: str, action_id: str, test: Mapping[str, Any]):
        """The GM supplies trusted mechanics, never the agent's free text."""
        if actor not in self.state["characters"] or not action_id:
            raise ValueError("Action requires an existing actor and nonempty ID.")
        allowed = {"skill", "aptitude", "modifier", "pool_kind", "pool_spend"}
        if set(test) - allowed:
            raise ValueError("Unknown test fields.")
        self.state["actions"].setdefault(actor, {})[action_id] = dict(test)
        self._save()

    def legal_actions(self, actor: str) -> tuple[str, ...]:
        return tuple(self.state["actions"].get(actor, {}))

    def resolve(self, actor: str, action_id: str, *, observers: tuple[Observer, ...] = ()):
        if action_id not in self.legal_actions(actor):
            raise ValueError("Agent must choose an offered action.")
        stored = self.state["characters"][actor]
        # Resolve on a copy: validation failures cannot spend persisted resources.
        pools = EP2PoolState(maximum=stored["maximum"], current=dict(stored["current"]))
        rng_before = self.rng.getstate()
        try:
            result = resolve_ep2_action(
                character=EP2Character(**stored["sheet"]),
                action=self.state["actions"][actor][action_id], pools=pools,
                roll=self.rng.randint(0, 99),
            )
        except Exception:
            self.rng.setstate(rng_before)
            raise
        event = {"actor": actor, "action": action_id, "result": result}
        old_current = stored["current"]
        stored["current"] = dict(pools.current)
        try:
            committed = self._record_event(event)
        except Exception:
            stored["current"] = old_current
            self.rng.setstate(rng_before)
            raise
        for observer in observers:
            observer.observe(json.dumps(committed, ensure_ascii=False))
        return committed

    def memories(self) -> list[dict]:
        return [{**json.loads(payload), "id": event_id}
                for event_id, payload in self.db.execute("SELECT id,payload FROM events ORDER BY id")]
