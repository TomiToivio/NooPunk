"""Executable contracts for cyberspace reachability (issue #344).

Code-only, per `AGENTS.md` and issue #271. These tests exercise the **validator**: which targets a
remote path can reach in which era, that a genuinely isolated system refuses a remote path in every
era, that a social relation is refused *by name* as an access path, and that the two illegalities stay
two. They do not assert the setting's prose.

Where a test sweeps the shipped document it does so through the loader, so the assertions state the
model's behaviour rather than the author's wording.

Run from the repository root:

    python -m unittest discover -s strategy_game/tests -p "test_*.py"
"""
from __future__ import annotations

import copy
import json
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:  # pragma: no cover - import bootstrap, mirrors the sibling test modules
    sys.path.insert(0, str(ROOT))

from strategy_game.cyber import (  # noqa: E402
    ACCESS_MODES,
    CONNECTIVITY_FORMAT,
    ERA_IDS,
    ILLEGALITY_CLASSES,
    REMOTE_INTRUSION_STANCES,
    connectivity_from_dict,
    load_connectivity,
)

_FIXTURE = {
    "format": CONNECTIVITY_FORMAT,
    "eras": [
        {"id": "acceleration", "position": "starting_era", "remote_reach": True, "local_links": True},
        {"id": "nhi_crisis", "remote_reach": False, "local_links": True},
        {"id": "after_crisis", "remote_reach": True, "local_links": True},
    ],
    "connectivity_classes": [
        {"id": "public_gateway", "remote_intrusion": "possible"},
        {"id": "safenet_exposed", "remote_intrusion": "possible"},
        {"id": "private_linked", "remote_intrusion": "requires_authorised_path"},
        {"id": "local_only", "remote_intrusion": "requires_local_presence"},
        {"id": "isolated", "remote_intrusion": "impossible"},
    ],
    "access_paths": [
        {"id": "field_netrunner", "mode": "local", "requires_local_presence": True},
        {"id": "drone_proxy", "mode": "proxied"},
        {"id": "authorized_link", "mode": "authorized", "requires_authorisation": True},
        {"id": "remote_public_service", "mode": "remote", "needs_remote_reach": True},
        {"id": "bridge_old_internet", "mode": "forbidden", "requires_local_presence": True,
         "illegality": "containment_breach"},
    ],
    "illegality_classes": [
        {"id": "infosec_failure", "is_containment_breach": False},
        {"id": "containment_breach", "is_containment_breach": True},
    ],
    "refused_as_access_paths": {"ids": ["social_tie", "faction_relationship", "network_edge"]},
}


def _fixture():
    return connectivity_from_dict(copy.deepcopy(_FIXTURE))


class ShippedDocumentTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.model = load_connectivity()

    def test_the_document_declares_its_format(self):
        from strategy_game.cyber import DATA_PATH

        self.assertTrue(DATA_PATH.is_file(), f"missing packaged model: {DATA_PATH}")
        with open(DATA_PATH, encoding="utf-8") as handle:
            self.assertEqual(json.load(handle)["format"], CONNECTIVITY_FORMAT)

    def test_the_three_periods_are_present_and_the_start_is_pre_crisis(self):
        self.assertEqual(set(self.model.eras), set(ERA_IDS))
        self.assertEqual(self.model.starting_era().identifier, "acceleration")

    def test_every_record_uses_the_declared_vocabularies(self):
        self.assertEqual(self.model.off_vocabulary(), ())

    def test_each_connectivity_class_states_a_declared_stance(self):
        for target in self.model.connectivity_classes.values():
            with self.subTest(target=target.identifier):
                self.assertIn(target.remote_intrusion, REMOTE_INTRUSION_STANCES)

    def test_each_access_path_states_a_declared_mode(self):
        for path in self.model.access_paths.values():
            with self.subTest(path=path.identifier):
                self.assertIn(path.mode, ACCESS_MODES)

    def test_the_two_illegalities_are_both_present_and_distinguishable(self):
        self.assertEqual(set(self.model.illegality_classes), set(ILLEGALITY_CLASSES))
        breaches = {i for i in ILLEGALITY_CLASSES if self.model.is_containment_breach(i)}
        self.assertEqual(breaches, {"containment_breach"})


class RemoteIntrusionTests(unittest.TestCase):
    """Issue #344: block remote hacking of truly disconnected targets without an established path."""

    def test_no_remote_path_reaches_an_isolated_target_in_any_era(self):
        model = _fixture()
        for era in ERA_IDS:
            for path_id in ("remote_public_service",):
                with self.subTest(era=era, path=path_id):
                    result = model.resolve_access("isolated", era, path_id)
                    self.assertFalse(result.possible, result.reason)

    def test_a_local_path_reaches_an_isolated_target_only_with_someone_on_site(self):
        model = _fixture()
        without = model.resolve_access("isolated", "after_crisis", "field_netrunner")
        self.assertFalse(without.possible)
        with_agent = model.resolve_access("isolated", "after_crisis", "field_netrunner", local_presence=True)
        self.assertTrue(with_agent.possible, with_agent.reason)

    def test_a_public_target_is_reachable_remotely_only_while_the_network_is_up(self):
        model = _fixture()
        before = model.resolve_access("public_gateway", "acceleration", "remote_public_service")
        during = model.resolve_access("public_gateway", "nhi_crisis", "remote_public_service")
        after = model.resolve_access("public_gateway", "after_crisis", "remote_public_service")
        self.assertTrue(before.possible, before.reason)
        self.assertFalse(during.possible, during.reason)
        self.assertTrue(after.possible, after.reason)

    def test_the_crisis_removes_reachability_rather_than_capability(self):
        """The same netrunner and the same path stop working; nothing about the operator changed."""
        model = _fixture()
        before = model.resolve_access("private_linked", "acceleration", "remote_public_service")
        during = model.resolve_access("private_linked", "nhi_crisis", "remote_public_service")
        self.assertNotEqual(before.possible, during.possible)

    def test_an_influence_edge_is_not_a_route(self):
        """Issue #344: a Castellsian tie does not create a usable network path."""
        model = _fixture()
        for refused in sorted(model.refused_path_ids):
            with self.subTest(path=refused):
                with self.assertRaises(ValueError) as caught:
                    model.resolve_access("public_gateway", "acceleration", refused)
                self.assertIn("not an access path", str(caught.exception))
        for target in ("isolated", "local_only", "public_gateway"):
            with self.subTest(target=target):
                with self.assertRaises(ValueError):
                    model.resolve_access(target, "acceleration", "social_tie")

    def test_a_local_only_target_has_no_outside_route(self):
        model = _fixture()
        off_site = model.resolve_access("local_only", "after_crisis", "remote_public_service")
        self.assertFalse(off_site.possible, off_site.reason)
        on_site = model.resolve_access("local_only", "after_crisis", "field_netrunner", local_presence=True)
        self.assertTrue(on_site.possible, on_site.reason)


class LegalityTests(unittest.TestCase):
    """Issue #344: keep a mismanaged exposure distinct from a containment breach."""

    def test_bridging_the_quarantine_is_a_containment_breach(self):
        model = _fixture()
        result = model.resolve_access("public_gateway", "after_crisis", "bridge_old_internet", local_presence=True)
        self.assertTrue(result.possible)
        self.assertEqual(result.illegality, "containment_breach")
        self.assertTrue(result.is_containment_breach)

    def test_attacking_a_mismanaged_exposure_is_not_a_containment_breach(self):
        """The INFOSEC failure is serious and recurring, but it is not the boundary crime."""
        model = _fixture()
        result = model.resolve_access("safenet_exposed", "after_crisis", "remote_public_service")
        self.assertTrue(result.possible)
        self.assertFalse(result.is_containment_breach)
        self.assertEqual(result.illegality, "")

    def test_the_breach_needs_the_operator_at_the_boundary(self):
        model = _fixture()
        result = model.resolve_access("public_gateway", "after_crisis", "bridge_old_internet")
        self.assertFalse(result.possible)

    def test_an_authorised_path_needs_the_authority(self):
        model = _fixture()
        without = model.resolve_access("private_linked", "after_crisis", "authorized_link")
        self.assertFalse(without.possible, without.reason)
        with_it = model.resolve_access("private_linked", "after_crisis", "authorized_link", authorised=True)
        self.assertTrue(with_it.possible, with_it.reason)


class ShapeTests(unittest.TestCase):
    def test_an_unknown_target_era_or_path_is_a_clear_error(self):
        model = _fixture()
        for args in (("no_such_class", "acceleration", "field_netrunner"),
                     ("public_gateway", "no_such_era", "field_netrunner"),
                     ("public_gateway", "acceleration", "no_such_path")):
            with self.subTest(args=args):
                with self.assertRaises(KeyError):
                    model.resolve_access(*args)

    def test_resolving_does_not_mutate_the_model(self):
        model = _fixture()
        before = {key: value.to_dict() for key, value in model.access_paths.items()}
        for target in model.connectivity_classes:
            for era in model.eras:
                for path in model.access_paths:
                    model.resolve_access(target, era, path, local_presence=True, authorised=True)
        self.assertEqual({key: value.to_dict() for key, value in model.access_paths.items()}, before)

    def test_every_assessment_carries_its_reason(self):
        model = _fixture()
        for target in model.connectivity_classes:
            for path in model.access_paths:
                with self.subTest(target=target, path=path):
                    self.assertTrue(model.resolve_access(target, "acceleration", path, local_presence=True).reason)

    def test_a_document_of_another_format_is_refused(self):
        import tempfile

        with tempfile.TemporaryDirectory() as tmp:
            wrong = Path(tmp) / "other.json"
            wrong.write_text(json.dumps({"format": "something.else"}), encoding="utf-8")
            with self.assertRaises(ValueError):
                load_connectivity(wrong)

    def test_the_shipped_model_records_the_example_mission_across_all_three_periods(self):
        model = load_connectivity()
        periods = {item["era"] for item in model.example_mission.get("periods", [])}
        self.assertEqual(periods, set(ERA_IDS))


class ScopeDirectiveTests(unittest.TestCase):
    """The crossover is inspired by LaclauGPT and must never import it (issues #282/#299)."""

    def test_importing_the_cyber_module_couples_to_no_laclaugpt_package(self):
        code = (
            "import sys, strategy_game, strategy_game.cyber;"
            "m = strategy_game.cyber.load_connectivity();"
            "m.resolve_access('isolated', 'after_crisis', 'field_netrunner', local_presence=True);"
            "print(sorted(x for x in sys.modules if x == 'laclaugpt' or x.startswith('laclaugpt.')))"
        )
        result = subprocess.run(
            [sys.executable, "-c", code], cwd=ROOT, capture_output=True, text=True, check=False
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stdout.strip(), "[]", f"loading the model pulled in LaclauGPT: {result.stdout}")

    def test_the_module_source_imports_no_laclaugpt(self):
        text = (ROOT / "strategy_game" / "cyber.py").read_text(encoding="utf-8")
        self.assertNotIn("import laclaugpt", text)
        self.assertNotIn("from laclaugpt", text)


if __name__ == "__main__":
    unittest.main()
