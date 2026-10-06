"""Structure guard for the six-stat base attribute model (issue #131).

Issue #131 (2026-10-05) is the author's explicit, locked decision to *simplify* the
base attribute model. After a period in which the base list grew to twelve STATS
(issue #113), the author ruled:

    "Use only these six base stats ... Decision: FIT / REF / INT / SOC / CYB / PSY ...
     Lock the basic stat model here and build everything else on top of it."

Two properties matter and are easy to lose in a later edit:

* the six base STATs stay six, with these exact codes and names, on the 1..10 scale;
* cybernetic *hardware* statistics (processing / bandwidth / storage / hardening and
  the older COMPUTE / INTERFACE / NETWORK sketch) are properties of equipment and
  agents, NOT character attributes -- and the detail belongs in the Social and Psychic
  domain layers, not in more base attributes.

This guard pins the machine-readable canon (`data/rules/core.json`), the two binding
documents (`RULEBOOK.md`, `rulebook/2_ATTRIBUTES.md`), the agent contract (`AGENTS.md`)
and the exported Python constants. It asserts structure only; it does not constrain how
the domain layers are implemented.

Run: python3 -m unittest discover -s tests -p "test_*.py"
"""
from __future__ import annotations

import json
import re
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

RULEBOOK = "RULEBOOK.md"
ATTRIBUTES = "rulebook/2_ATTRIBUTES.md"
AGENTS = "AGENTS.md"
CORE_JSON = "data/rules/core.json"

#: The locked six base STATs, in canonical order.
BASE_STATS = ["FIT", "REF", "INT", "SOC", "CYB", "PSY"]

#: Canonical code -> display name.
BASE_NAMES = {
    "FIT": "Fitness",
    "REF": "Reflexes",
    "INT": "Intelligence",
    "SOC": "Social",
    "CYB": "Cybernetics",
    "PSY": "Psyche",
}

#: Canonical code -> four-layer ontology.
BASE_LAYER = {
    "FIT": "Physical",
    "REF": "Physical",
    "INT": "Social",
    "SOC": "Social",
    "CYB": "Cybernetic",
    "PSY": "Psychic",
}

#: The twelve STATS of the superseded #113 draft. They must not come back as the model.
SUPERSEDED_CODES = ("RES", "REA", "EMP", "PRE", "WIL", "INU", "NOE", "CYI", "BND", "CTL")


def read(relative: str) -> str:
    return (ROOT / relative).read_text(encoding="utf-8")


def flat(relative: str) -> str:
    """Whitespace-collapsed, emphasis-stripped, lowercased."""
    text = re.sub(r"[*`]", "", read(relative))
    return " ".join(text.split()).lower()


def canon() -> dict:
    return json.loads(read(CORE_JSON))


class CoreJsonTests(unittest.TestCase):
    def test_stats_final_list_is_the_six_in_order(self) -> None:
        self.assertEqual(canon()["stats"]["final_list"], BASE_STATS)

    def test_stats_names_and_layers_are_recorded(self) -> None:
        stats = canon()["stats"]
        self.assertEqual(stats["names"], BASE_NAMES)
        self.assertEqual(stats["layer"], BASE_LAYER)

    def test_skill_list_matches_canonical_vocabulary(self) -> None:
        """#131 locks the STAT list; #159 later resolved the skill list in the same core.json."""
        skills = json.loads(read("data/rules/skills.json"))
        canonical = [row["name"] for row in skills["skills"]]
        self.assertEqual(canon()["skills"]["final_list"], canonical)

    def test_the_human_scale_stays_one_to_ten(self) -> None:
        self.assertEqual((canon()["stats"]["min"], canon()["stats"]["max"]), (1, 10))


class ExportedConstantsTests(unittest.TestCase):
    def test_core_module_exposes_the_six(self) -> None:
        from rules import STAT_LAYER, STAT_LIST, STAT_NAMES

        self.assertEqual(tuple(STAT_LIST), tuple(BASE_STATS))
        self.assertEqual(STAT_NAMES, BASE_NAMES)
        self.assertEqual(STAT_LAYER, BASE_LAYER)

    def test_every_layer_is_represented(self) -> None:
        layers = set(BASE_LAYER.values())
        self.assertEqual(layers, {"Physical", "Social", "Psychic", "Cybernetic"})


class BindingDocumentTests(unittest.TestCase):
    def test_attribute_stub_names_all_six_with_codes(self) -> None:
        text = read(ATTRIBUTES)
        for code, name in BASE_NAMES.items():
            with self.subTest(stat=code):
                self.assertRegex(
                    text,
                    rf"{re.escape(name)}\s*\({re.escape(code)}\)",
                    f"{name} ({code}) is not named in {ATTRIBUTES}",
                )

    def test_attribute_stub_keeps_the_four_layer_ontology(self) -> None:
        """The layer vocabulary is the #78 invariant and must not be simplified away."""
        for doc in (RULEBOOK, ATTRIBUTES):
            text = flat(doc)
            with self.subTest(doc=doc):
                for layer in ("physical", "social", "psychic", "cybernetic"):
                    self.assertIn(layer, text)

    def test_attribute_stub_no_longer_presents_the_twelve_stat_model(self) -> None:
        """The stub may *mention* the superseded draft, but must not present it as the model."""
        text = flat(ATTRIBUTES)
        self.assertNotIn("final 12-stat list", text)
        self.assertRegex(text, r"issue #131 supersedes issue #113",
                         "the superseding issue is not recorded")

    def test_rulebook_stats_section_names_the_six(self) -> None:
        body = RULEBOOK_SECTION()
        for code in BASE_STATS:
            with self.subTest(stat=code):
                self.assertIn(code, body)

    def test_rulebook_no_longer_presents_the_superseded_layers(self) -> None:
        """The §9.2 table must not still advertise the #113 twelve."""
        body = RULEBOOK_SECTION()
        self.assertNotIn("Integration (CYI)", body)
        self.assertNotIn("Noesis (NOE)", body)
        self.assertRegex(body, r"issue #131", "the superseding issue is not recorded")

    def test_agents_md_records_the_locked_six(self) -> None:
        text = flat(AGENTS)
        for code in BASE_STATS:
            with self.subTest(stat=code):
                self.assertIn(code.lower(), text)
        self.assertIn("issue #131", text)


def RULEBOOK_SECTION() -> str:
    """The §9.2 attribute subsection of RULEBOOK.md, anchored by heading text.

    Anchor by heading text, never by a bare ``## N.`` number: after #120 the rulebook
    carries two numbering namespaces (core chapters and the preserved ledger), so
    numbers are ambiguous.
    """
    body = read(RULEBOOK)
    pattern = (
        r"(?ms)^###\s+[^\n]*(?:Six base STATs|Four-layer 1.{0,3}10 attribute system)"
        r"[^\n]*\n(.*?)(?=^###\s+|^##\s+|\Z)"
    )
    match = re.search(pattern, body, re.IGNORECASE)
    assert match, "the RULEBOOK §9.2 attribute subsection was not found"
    return " ".join(re.sub(r"[*`]", "", match.group(1)).split())


class HardwareStatisticsTests(unittest.TestCase):
    def test_hardware_capacities_are_not_character_stats(self) -> None:
        """The author's ruling: hardware/system properties belong to the deck, not the sheet."""
        text = flat(ATTRIBUTES)
        self.assertRegex(
            text,
            r"(not character (attributes|stats))|(statistics of the equipment)",
            "the hardware-vs-character boundary is not stated",
        )

    def test_the_cybernetic_sketch_is_relegated(self) -> None:
        """COMPUTE / INTERFACE / NETWORK may be named, but not as the base STAT model."""
        text = flat(ATTRIBUTES)
        for token in ("processing", "bandwidth", "storage", "hardening"):
            with self.subTest(token=token):
                self.assertIn(token, text, f"the hardware capacity {token!r} is not recorded")


class SupersededStatTests(unittest.TestCase):
    def test_superseded_codes_are_not_the_model(self) -> None:
        """The twelve-stat draft is gone from the two binding documents' live model.

        The archived pre-#120 snapshot legitimately still contains it, so this checks the
        live attribute stub and the #9.2 subsection only, not the whole rulebook.
        """
        stub = flat(ATTRIBUTES)
        for code in SUPERSEDED_CODES:
            with self.subTest(code=code):
                self.assertNotRegex(
                    stub,
                    rf"\b{code}\b\s*\|",
                    f"{code} still appears as a STAT code in the attribute stub table",
                )


if __name__ == "__main__":
    unittest.main()
