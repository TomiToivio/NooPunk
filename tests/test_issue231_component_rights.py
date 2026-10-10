"""Release packaging guard for issue #231.

The source-level ledger (`game_system_rights.json`) records who we take from. This guard covers
what we actually SHIP, and it exists because attribution under CC BY and CC BY-SA is a CONDITION
of the grant, not a courtesy: a missing notice is a licence violation, and a notice that is
hand-maintained is a notice that eventually goes missing.

It checks four things no other guard does:

1. every component in `component_rights.json` matches at least one real file -- so the ledger
   cannot rot into describing a layout that no longer exists;
2. every source whose decision REQUIRES attribution appears in the generated
   `docs/sources/ATTRIBUTION.md`;
3. no component lists a non-shippable source (NC, proprietary, unverified OGL) as an input --
   #231 criterion 3, until the isolation audit is complete;
4. the licence choice is still recorded as PENDING, so nothing ships as if licensed.

Run: python3 -m unittest discover -s tests -p 'test_*.py'
"""
from __future__ import annotations

import json
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
COMPONENTS = ROOT / "data" / "sources" / "component_rights.json"
SOURCES = ROOT / "data" / "sources" / "game_system_rights.json"
ATTRIBUTION = ROOT / "docs" / "sources" / "ATTRIBUTION.md"

sys.path.insert(0, str(ROOT / "tools"))
import issue231_attribution as attribution


def components() -> dict:
    return json.loads(COMPONENTS.read_text(encoding="utf-8"))


def sources() -> dict:
    return json.loads(SOURCES.read_text(encoding="utf-8"))


class ComponentsMatchRealityTests(unittest.TestCase):
    def test_every_component_resolves_to_at_least_one_file(self) -> None:
        failures = []
        for component in components()["components"]:
            for pattern in component["paths"]:
                if not list(ROOT.glob(pattern)):
                    failures.append(f"{component['id']}: {pattern} matches nothing")
        self.assertFalse(failures, failures)

    def test_component_ids_are_unique(self) -> None:
        ids = [c["id"] for c in components()["components"]]
        self.assertEqual(sorted(ids), sorted(set(ids)))

    def test_inherits_references_point_at_real_components(self) -> None:
        known = {c["id"] for c in components()["components"]}
        for component in components()["components"]:
            licence = component["license"]
            if licence.startswith("inherits:"):
                self.assertIn(licence.split(":", 1)[1], known, f"{component['id']} inherits nothing")


class AttributionIsOwedAndPaidTests(unittest.TestCase):
    """CC BY / CC BY-SA attribution is a condition of the grant, so this is a legal check."""

    def test_every_attribution_owing_source_appears_in_the_generated_notice(self) -> None:
        text = ATTRIBUTION.read_text(encoding="utf-8")
        owed = [s for s in sources()["sources"]
                if attribution.ATTRIBUTION_OBLIGATIONS.get(s["decision"]) is True]
        self.assertTrue(owed, "no attribution-owing sources found; the ledger shape changed")
        for source in owed:
            with self.subTest(source=source["id"]):
                self.assertIn(source["source"], text,
                              f"{source['id']} requires attribution under {source['license']} "
                              f"but is missing from docs/sources/ATTRIBUTION.md")

    def test_the_notice_is_current(self) -> None:
        result = subprocess.run([sys.executable, "tools/issue231_attribution.py", "--check"],
                                cwd=ROOT, capture_output=True, text=True, check=False)
        self.assertEqual(result.returncode, 0, result.stderr or result.stdout)

    def test_the_notice_says_it_is_generated(self) -> None:
        self.assertIn("Do not edit by hand", ATTRIBUTION.read_text(encoding="utf-8"))


class NonShippableSourcesTests(unittest.TestCase):
    """#231 criterion 3: incompatible expression must be isolated before it can be an input."""

    def test_no_component_declares_a_non_shippable_input(self) -> None:
        excluded = set(components()["not_shipped"]["excluded_sources"])
        failures = [f"{c['id']} lists {i}" for c in components()["components"]
                    for i in c["third_party_inputs"] if i in excluded]
        self.assertFalse(failures, failures)

    def test_every_declared_input_exists_in_the_source_ledger(self) -> None:
        known = {s["id"] for s in sources()["sources"]}
        failures = [f"{c['id']} lists unknown source {i}" for c in components()["components"]
                    for i in c["third_party_inputs"] if i not in known]
        self.assertFalse(failures, failures)

    def test_non_commercial_sources_are_excluded(self) -> None:
        excluded = set(components()["not_shipped"]["excluded_sources"])
        by_id = {s["id"]: s for s in sources()["sources"]}
        for source_id in ("eclipse-phase-2e", "transhumanitys-fate"):
            with self.subTest(source=source_id):
                self.assertIn(source_id, excluded)
                self.assertIn("NC", by_id[source_id]["license"].upper())

    def test_proprietary_sources_are_excluded(self) -> None:
        excluded = set(components()["not_shipped"]["excluded_sources"])
        for source_id in ("cyberpunk-red-2020", "cy-borg", "shadowrun"):
            with self.subTest(source=source_id):
                self.assertIn(source_id, excluded)


class LicenceChoiceStaysOpenTests(unittest.TestCase):
    """Criterion 1 is the author's. The guard stops an agent deciding it by accident."""

    def test_the_target_licence_is_still_pending(self) -> None:
        target = components()["target_license"]
        self.assertEqual(target["state"], "pending-author-decision")
        self.assertEqual(target["code_license"], "pending-author-decision")

    def test_no_component_claims_a_decided_licence(self) -> None:
        for component in components()["components"]:
            with self.subTest(component=component["id"]):
                self.assertTrue(
                    component["license"].startswith(("pending-author-decision", "inherits:")),
                    f"{component['id']} claims {component['license']!r}, but no licence has "
                    f"been chosen; see issue #231 acceptance criterion 1",
                )

    def test_the_recommendation_matches_the_source_ledger(self) -> None:
        """The BY-SA recommendation exists so The Veil's share-alike text stays adaptable."""
        recommended = components()["target_license"]["recommended"]
        self.assertIn("BY-SA", recommended)
        veil = next(s for s in sources()["sources"] if s["id"] == "the-veil")
        self.assertIn("BY-SA", veil["license"].upper())

    def test_open_items_are_recorded(self) -> None:
        self.assertGreaterEqual(len(components()["open_items"]), 3,
                                "the unresolved criteria must be recorded, not implied")


if __name__ == "__main__":
    unittest.main()
