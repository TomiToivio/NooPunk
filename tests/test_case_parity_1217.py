"""The MUD and the terminal must play one case, with one actor, one sheet (#1217).

The tracker asks for *"one canonical actor ID and sheet across CLI/Evennia/GUI"* and that the first
approved investigation works *"consistently via selected interfaces"*. Before `case_bridge` existed,
the MUD had no path to the Lakkahaltia case at all — only `scripts/noopunk_case.py` could play it.

These tests are about **equivalence**, not about the bridge's own convenience: the same seed and the
same commands must produce the same scene, the same clues and the same theory, and a save written by
one interface must resume in the other.
"""

from __future__ import annotations

# The bridge imports the console through `rules.*`, exactly as `scripts/noopunk_case.py` does.
import sys
import tempfile
import unittest
from pathlib import Path

from mud.nopunk_mud.case_bridge import DEFAULT_CASE, CaseBridge, CaseBridgeError
from src.world.actor_registry import ActorRegistry

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src"))

from console.play import run_command
from console.session import CaseSession, load_session
from mud.nopunk_mud.case_bridge import DEFAULT_RATINGS
from rules.investigation import Investigator, load_case_graph

SCRIPT = ["look", "go corridor", "look", "clues", "status"]


class EquivalenceTest(unittest.TestCase):
    def test_the_bridge_and_the_terminal_agree_on_the_same_script(self) -> None:
        bridge = CaseBridge.open(actor_id="act.rookie", sheet_id="sheet.rookie", seed=7)

        graph = load_case_graph(DEFAULT_CASE)
        investigator = Investigator(name="act.rookie", ratings=dict(DEFAULT_RATINGS))
        plain = CaseSession.start(graph, investigator, seed=7)

        bridge_out = [bridge.command(line)[1] for line in SCRIPT]
        plain_out = [run_command(plain, line)[1] for line in SCRIPT]

        self.assertEqual(bridge_out, plain_out, "the same commands must print the same text")
        self.assertEqual(bridge.view()["scene"], plain.scene().id)
        self.assertEqual(bridge.view()["clues"], list(plain.open_clues()))

    def test_the_bridge_uses_the_terminals_dispatcher_not_its_own(self) -> None:
        """A command the console does not know must produce the console's own refusal."""
        bridge = CaseBridge.open(actor_id="act.rookie", sheet_id="sheet.rookie", seed=7)
        _keep, bridge_out = bridge.command("teleport")
        _keep2, plain_out = run_command(
            CaseSession.start(load_case_graph(DEFAULT_CASE),
                              Investigator(name="act.rookie", ratings=dict(DEFAULT_RATINGS)), seed=7),
            "teleport",
        )
        self.assertEqual(bridge_out, plain_out)
        self.assertIn("teleport", bridge_out)


class CrossInterfaceSaveTest(unittest.TestCase):
    def test_a_save_written_by_the_terminal_resumes_in_the_bridge(self) -> None:
        graph = load_case_graph(DEFAULT_CASE)
        plain = CaseSession.start(
            graph, Investigator(name="act.rookie", ratings=dict(DEFAULT_RATINGS)), seed=7
        )
        for line in ("look", "go corridor", "look"):
            run_command(plain, line)

        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "case.json"
            plain.save(path)
            resumed = CaseBridge.resume(path, actor_id="act.rookie", sheet_id="sheet.rookie")

        self.assertEqual(resumed.view()["scene"], plain.scene().id)
        self.assertEqual(resumed.view()["clues"], list(plain.open_clues()))

    def test_a_save_written_by_the_bridge_resumes_in_a_plain_session(self) -> None:
        bridge = CaseBridge.open(actor_id="act.rookie", sheet_id="sheet.rookie", seed=7)
        for line in ("look", "go corridor"):
            bridge.command(line)

        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "case.json"
            bridge.save(path)
            restored = load_session(load_case_graph(DEFAULT_CASE), path)

        self.assertEqual(restored.scene().id, bridge.view()["scene"])
        self.assertEqual(list(restored.open_clues()), bridge.view()["clues"])

    def test_the_snapshot_carries_the_interface_identity(self) -> None:
        bridge = CaseBridge.open(actor_id="act.rookie", sheet_id="sheet.rookie", seed=7)
        snapshot = bridge.snapshot()
        self.assertEqual(snapshot["interface"], {"actor_id": "act.rookie", "sheet_id": "sheet.rookie"})


class OneActorOneSheetTest(unittest.TestCase):
    def test_the_same_actor_cannot_enter_with_a_second_sheet(self) -> None:
        registry = ActorRegistry()
        CaseBridge.open(actor_id="act.rookie", sheet_id="sheet.rookie", registry=registry, seed=7)
        with self.assertRaises(CaseBridgeError) as caught:
            CaseBridge.open(actor_id="act.rookie", sheet_id="sheet.other", registry=registry, seed=7)
        self.assertIn("second sheet", str(caught.exception))

    def test_re_entering_with_the_same_sheet_is_allowed(self) -> None:
        """A new session in another interface must not be mistaken for a new character."""
        registry = ActorRegistry()
        first = CaseBridge.open(actor_id="act.rookie", sheet_id="sheet.rookie", registry=registry, seed=7)
        second = CaseBridge.open(actor_id="act.rookie", sheet_id="sheet.rookie", registry=registry, seed=7)
        self.assertEqual(first.sheet_id, second.sheet_id)
        self.assertEqual(len(registry.actor("act.rookie").handles), 2)

    def test_a_sheet_cannot_be_handed_to_a_second_actor(self) -> None:
        registry = ActorRegistry()
        CaseBridge.open(actor_id="act.rookie", sheet_id="sheet.rookie", registry=registry, seed=7)
        with self.assertRaises(CaseBridgeError) as caught:
            CaseBridge.open(actor_id="act.other", sheet_id="sheet.rookie", registry=registry, seed=7)
        self.assertIn("already belongs", str(caught.exception))

    def test_the_registry_records_the_views_the_graphs_need(self) -> None:
        bridge = CaseBridge.open(actor_id="act.rookie", sheet_id="sheet.rookie", seed=7)
        views = {handle.view: handle.handle for handle in bridge.registry.actor("act.rookie").handles}
        self.assertEqual(views["sheet"], "sheet.rookie")
        self.assertEqual(views["physical"], "act.rookie")


class PlayTest(unittest.TestCase):
    def test_play_stops_at_quit(self) -> None:
        bridge = CaseBridge.open(actor_id="act.rookie", sheet_id="sheet.rookie", seed=7)
        out = bridge.play(["look", "quit", "look"])
        self.assertEqual(len(out), 2, "nothing after quit may be executed")


if __name__ == "__main__":
    unittest.main()
