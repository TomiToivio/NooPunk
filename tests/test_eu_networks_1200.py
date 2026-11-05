"""Connectivity classes and authorisation rungs from #1200.

Code tests: they exercise `src/world/networks.py` reading `data/world/networks.json`, not document prose.
"""

from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from src.world.networks import NetworkError, load_topology

DATA = Path(__file__).resolve().parents[1] / "data" / "world" / "networks.json"


class TopologyTests(unittest.TestCase):
    def setUp(self) -> None:
        self.topology = load_topology()

    def test_the_four_connectivity_classes_exist(self) -> None:
        ids = {network.id for network in self.topology.networks}
        self.assertEqual(ids, {"old_internet", "closed_organisation", "euronet", "courier"})

    def test_a_closed_network_cannot_be_reached_remotely(self) -> None:
        allowed, reason = self.topology.can_attempt("closed_organisation", remote=True)
        self.assertFalse(allowed)
        self.assertIn("no remote path", reason)

    def test_a_closed_network_needs_physical_access_and_a_credential(self) -> None:
        allowed, reason = self.topology.can_attempt("closed_organisation", remote=False, on_site=True)
        self.assertFalse(allowed)
        self.assertIn("credential", reason)

        allowed, _ = self.topology.can_attempt(
            "closed_organisation", remote=False, on_site=True, has_credential=True
        )
        self.assertTrue(allowed)

    def test_euronet_is_public_but_needs_an_account(self) -> None:
        allowed, reason = self.topology.can_attempt("euronet", remote=True)
        self.assertFalse(allowed)
        self.assertIn("credential", reason)
        allowed, _ = self.topology.can_attempt("euronet", remote=True, has_credential=True)
        self.assertTrue(allowed)

    def test_the_old_internet_is_reachable_and_hostile(self) -> None:
        allowed, reason = self.topology.can_attempt("old_internet", remote=True)
        self.assertTrue(allowed)
        self.assertIn("hostile", reason)

    def test_a_courier_is_physical_by_definition(self) -> None:
        allowed, _ = self.topology.can_attempt("courier", remote=True)
        self.assertFalse(allowed)
        self.assertFalse(self.topology.network("courier").remotely_reachable)

    def test_the_perimeter_is_plato_eiss_and_has_no_in_world_nickname(self) -> None:
        self.assertEqual(self.topology.perimeter_name, "the Plato/EISS perimeter")
        # "Great Firewall" and bare "Firewall" are retired in-world terms (22_CYBERSPACE §22.3, RULEBOOK §34).
        self.assertIsNone(self.topology.informal_perimeter_name)
        self.assertIsNone(self.topology.subsystem_codename)   # AEGIS is not canon
        self.assertIn("Europol", self.topology.operated_by)

    def test_the_authorisation_ladder_is_ordered_and_warrants_are_marked(self) -> None:
        rungs = [rung.rung for rung in self.topology.rungs]
        self.assertEqual(rungs, sorted(rungs))
        self.assertEqual(rungs[0], 0)
        self.assertFalse(self.topology.requires_warrant("routine OSINT"))
        self.assertTrue(self.topology.requires_warrant("intrusive surveillance"))
        self.assertTrue(self.topology.requires_warrant("offensive hacking"))
        self.assertFalse(self.topology.requires_warrant("emergency containment"))

    def test_a_network_cannot_be_both_air_gapped_and_remote(self) -> None:
        raw = json.loads(DATA.read_text(encoding="utf-8"))
        broken = dict(raw)
        broken["networks"] = [dict(raw["networks"][1], remotely_reachable=True)]
        with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False, encoding="utf-8") as handle:
            handle.write(json.dumps(broken))
            path = Path(handle.name)
        try:
            with self.assertRaises(NetworkError):
                load_topology(path)
        finally:
            path.unlink(missing_ok=True)


if __name__ == "__main__":
    unittest.main()
