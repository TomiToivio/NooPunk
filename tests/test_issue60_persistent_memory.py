"""Structure guard for persistent agent memory (issue #60, work package C).

Package C lists "Add persistent memory" as its last unchecked item, and the issue's
first-playable milestone requires persistent *agent* memory (success criterion 8) in
addition to the persistent world state. The maintained milestone doc names "private
agent memory" as the next gap after the shared event log.

This guard asserts the properties that make the addition the right thing and that a
later session would otherwise drift:

1. an actor's notes survive a close/reopen of the store;
2. notes are **private** - one actor's memory is not readable by another;
3. the store is **append-only** and carries **no mechanics** (no dice, ratings,
   statistics or resolution), per ``AGENTS.md`` section 1;
4. the refusal paths stay closed (empty actor, empty note, bad turn);
5. ``forget`` is scoped to the owning actor, so one actor cannot erase another's.

The class names and payload shape are asserted directly because they are the
interface the issue asks for, not incidental prose.
"""
from __future__ import annotations

import inspect
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from concordia_runtime.memory import MemoryObserver, MemoryStore


class MemoryRoundTripTests(unittest.TestCase):
    def test_remember_then_recall_returns_the_note(self) -> None:
        store = MemoryStore(":memory:")
        store.remember("player", "the analyst recognised my face", turn=3)
        notes = store.recall("player")
        self.assertEqual(len(notes), 1)
        self.assertEqual(notes[0]["note"], "the analyst recognised my face")
        self.assertEqual(notes[0]["turn"], 3)
        store.close()

    def test_notes_are_returned_in_insertion_order(self) -> None:
        store = MemoryStore(":memory:")
        for i in range(3):
            store.remember("player", f"note {i}", turn=i)
        self.assertEqual([n["note"] for n in store.recall("player")],
                         ["note 0", "note 1", "note 2"])
        store.close()

    def test_subject_filter_returns_only_that_subject(self) -> None:
        store = MemoryStore(":memory:")
        store.remember("player", "a", subject="dossier")
        store.remember("player", "b", subject="rumour")
        store.remember("player", "c", subject="dossier")
        got = [n["note"] for n in store.recall("player", subject="dossier")]
        self.assertEqual(got, ["a", "c"])
        store.close()

    def test_actors_lists_only_actors_with_notes(self) -> None:
        store = MemoryStore(":memory:")
        store.remember("player", "x")
        store.remember("analyst", "y")
        self.assertEqual(store.actors(), ("analyst", "player"))
        store.close()


class MemoryPersistenceTests(unittest.TestCase):
    def test_notes_survive_reopen(self) -> None:
        """The whole point of the item: memory persists, not just the world state."""
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "agent.sqlite"
            first = MemoryStore(path)
            first.remember("player", "the analyst recognised my face", turn=3)
            first.remember("player", "I owe the fixer a favour", turn=5)
            first.close()

            resumed = MemoryStore(path)
            notes = resumed.recall("player")
            self.assertEqual([n["note"] for n in notes],
                             ["the analyst recognised my face",
                              "I owe the fixer a favour"])
            resumed.close()

    def test_two_actors_persist_independently(self) -> None:
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "agent.sqlite"
            store = MemoryStore(path)
            store.remember("player", "player-private")
            store.remember("analyst", "analyst-private")
            store.close()

            resumed = MemoryStore(path)
            self.assertEqual([n["note"] for n in resumed.recall("player")],
                             ["player-private"])
            self.assertEqual([n["note"] for n in resumed.recall("analyst")],
                             ["analyst-private"])
            resumed.close()


class MemoryPrivacyTests(unittest.TestCase):
    def test_one_actor_cannot_read_another_actors_notes(self) -> None:
        store = MemoryStore(":memory:")
        store.remember("player", "player-private")
        store.remember("analyst", "analyst-private")
        self.assertEqual([n["note"] for n in store.recall("player")],
                         ["player-private"])
        self.assertNotIn("analyst-private",
                         [n["note"] for n in store.recall("player")])
        store.close()

    def test_unknown_actor_has_no_memories(self) -> None:
        store = MemoryStore(":memory:")
        store.remember("player", "x")
        self.assertEqual(store.recall("stranger"), [])
        store.close()

    def test_forget_cannot_erase_another_actors_note(self) -> None:
        store = MemoryStore(":memory:")
        victim = store.remember("player", "keep me")
        # An intruder holding the correct id still cannot remove it.
        removed = store.forget("analyst", victim["id"])
        self.assertFalse(removed)
        self.assertEqual(len(store.recall("player")), 1)
        store.close()

    def test_forget_removes_the_owners_own_note(self) -> None:
        store = MemoryStore(":memory:")
        note = store.remember("player", "drop me")
        self.assertTrue(store.forget("player", note["id"]))
        self.assertEqual(store.recall("player"), [])
        store.close()


class MemoryAppendOnlyTests(unittest.TestCase):
    def test_the_store_exposes_no_edit_operation(self) -> None:
        """Append-only, like the event log: corrections are new notes, not edits."""
        for forbidden in ("update", "edit", "amend"):
            with self.subTest(operation=forbidden):
                self.assertFalse(
                    any(forbidden in name.lower()
                        for name in dir(MemoryStore) if not name.startswith("__")),
                    f"MemoryStore must not expose an {forbidden!r} operation",
                )


class MemoryAntiInventionTests(unittest.TestCase):
    """Memory records meaning; it must not smuggle in mechanics (AGENTS.md section 1)."""

    def test_a_recorded_note_carries_no_mechanical_fields(self) -> None:
        store = MemoryStore(":memory:")
        note = store.remember("player", "a plain recollection", turn=2)
        self.assertEqual(set(note),
                         {"id", "actor", "turn", "subject", "note"})
        for mechanical in ("roll", "rating", "modifier", "dice", "skill",
                           "aptitude", "damage", "pool"):
            with self.subTest(field=mechanical):
                self.assertNotIn(mechanical, note)
        store.close()

    def test_the_memory_module_does_not_touch_the_resolver(self) -> None:
        """The resolver seam stays the only path from agent output into mechanics."""
        from concordia_runtime import memory as memory_module
        source = inspect.getsource(memory_module)
        for forbidden in ("resolve_ep2_action", "resolve_proposal",
                          "resolve_structured_check", "import random"):
            with self.subTest(symbol=forbidden):
                self.assertNotIn(forbidden, source)

    def test_the_store_defines_no_statistical_api(self) -> None:
        public = {n for n in dir(MemoryStore) if not n.startswith("_")}
        for forbidden in ("roll", "resolve", "check", "random", "statistics", "score"):
            with self.subTest(method=forbidden):
                self.assertNotIn(forbidden, public)


class MemoryRefusalTests(unittest.TestCase):
    def test_empty_actor_is_refused(self) -> None:
        store = MemoryStore(":memory:")
        with self.assertRaises(ValueError):
            store.remember("", "note")
        with self.assertRaises(ValueError):
            store.recall("")
        store.close()

    def test_empty_note_is_refused(self) -> None:
        store = MemoryStore(":memory:")
        with self.assertRaises(ValueError):
            store.remember("player", "")
        store.close()

    def test_bad_turn_is_refused(self) -> None:
        store = MemoryStore(":memory:")
        for bad in (-1, 1.5, "3"):
            with self.subTest(turn=bad), self.assertRaises(ValueError):
                store.remember("player", "note", turn=bad)  # type: ignore[arg-type]
        store.close()

    def test_a_refused_write_leaves_the_store_unchanged(self) -> None:
        store = MemoryStore(":memory:")
        with self.assertRaises(ValueError):
            store.remember("player", "")
        self.assertEqual(store.recall("player"), [])
        self.assertEqual(store.actors(), ())
        store.close()


class MemoryObserverBridgeTests(unittest.TestCase):
    """The observer turns the session's SHARED event log into PER-AGENT memory."""

    def _session(self, path):
        from concordia_runtime.ep2_session import EP2Session
        from eclipse_phase_homebrew import EP2Character, EP2PoolState
        session = EP2Session(path, seed=23)
        session.add_character("player",
                              EP2Character("fixture", skills={"Infosec": 60}),
                              EP2PoolState())
        session.offer_action("player", "mesh_test", {"skill": "Infosec"})
        return session

    def test_observing_a_committed_event_lands_in_that_actors_memory(self) -> None:
        store = MemoryStore(":memory:")
        session = self._session(":memory:")
        observer = MemoryObserver("player", store)
        event = session.resolve("player", "mesh_test", observers=(observer,))
        notes = store.recall("player")
        self.assertEqual(len(notes), 1)
        self.assertIn(str(event["id"]), notes[0]["note"])
        store.close()
        session.close()

    def test_two_agents_build_separate_memories_from_one_session(self) -> None:
        """This is the property that makes it *agent* memory, not a second log."""
        session = self._session(":memory:")
        player_store = MemoryStore(":memory:")
        analyst_store = MemoryStore(":memory:")
        session.resolve("player", "mesh_test", observers=(
            MemoryObserver("player", player_store),
            MemoryObserver("analyst", analyst_store),
        ))
        self.assertEqual(len(player_store.recall("player")), 1)
        self.assertEqual(len(analyst_store.recall("analyst")), 1)
        # Privacy holds across the two: neither sees the other's copy.
        self.assertEqual(player_store.recall("analyst"), [])
        self.assertEqual(analyst_store.recall("player"), [])
        player_store.close()
        analyst_store.close()
        session.close()

    def test_an_empty_observation_is_refused(self) -> None:
        store = MemoryStore(":memory:")
        observer = MemoryObserver("player", store)
        with self.assertRaises(ValueError):
            observer.observe("")
        self.assertEqual(store.recall("player"), [])
        store.close()

    def test_the_observer_requires_a_nonempty_actor(self) -> None:
        store = MemoryStore(":memory:")
        with self.assertRaises(ValueError):
            MemoryObserver("", store)
        store.close()


class MilestoneDocTests(unittest.TestCase):
    """The maintained #60 milestone doc must not re-list memory as missing."""

    def test_the_milestone_doc_records_memory_as_implemented(self) -> None:
        doc = (ROOT / "docs" / "sources" / "EP2_SESSION_MILESTONE.md").read_text(
            encoding="utf-8")
        flat = " ".join(doc.split())
        self.assertIn("MemoryStore", flat)
        # It may only appear as a remaining item if it is no longer listed there.
        remaining = flat.split("Remaining:", 1)[1] if "Remaining:" in flat else ""
        self.assertNotIn("private agent memory", remaining.casefold())


if __name__ == "__main__":
    unittest.main()
