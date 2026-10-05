# -*- coding: utf-8 -*-
"""Structure guard for the six-stat base model locked on issue #131.

Issue #113 landed a twelve-STAT model (three per layer, four layers) and wrote it into
the then-current ledger. Issue #120 then split the document: chapters 1-8 are the **live
core**, and the whole previous ledger is preserved verbatim below
``# Extended canon and reference material``.

The author simplified the universal core on #131: *"Use only these six base stats ...
Lock the basic stat model here and build everything else on top of it."*

Two things this guard must not get wrong, both of which made an earlier draft of it
fail against correct text:

* **The preserved ledger still contains the old twelve-stat section.** That is correct
  and intentional: it is an archive of the pre-#120 ledger, and editing it would be
  rewriting history. Every assertion here is therefore scoped to the **live core**,
  i.e. the text *before* the ``# Extended canon`` marker.
* The retired codes are two and three letters, so a bare ``\\bWIL\\b`` sweep collides
  with ordinary prose. Only the form a live STAT list actually uses is pinned.

Run: python3 -m unittest discover -s tests -p 'test_*.py'
"""
from __future__ import annotations

import json
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

RULEBOOK = "RULEBOOK.md"
ATTRIBUTES = "rulebook/2_ATTRIBUTES.md"
CORE = "data/rules/core.json"

#: The locked six, in the author's stated order.
SIX = ("FIT", "REF", "INT", "SOC", "CYB", "PSY")
SIX_NAMES = ("Fitness", "Reflexes", "Intelligence", "Social", "Cybernetics", "Psyche")

#: The four ontological layers survive this change and remain pinned in both documents.
LAYERS = ("Physical", "Social", "Psychic", "Cybernetic")

#: Hardware/system statistics — equipment properties, never character attributes.
HARDWARE = ("COMPUTE", "INTERFACE", "NETWORK")

#: The #120 split marker: everything above it is the live rulebook core.
CORE_MARKER = "# Extended canon and reference material"


def read(relative: str) -> str:
    return (ROOT / relative).read_text(encoding="utf-8")


def live_core(relative: str) -> str:
    """The live document, excluding the preserved pre-#120 compatibility ledger."""
    text = read(relative)
    return text.split(CORE_MARKER, 1)[0] if CORE_MARKER in text else text


def live_body(relative: str) -> str:
    """Live core with markdown emphasis stripped, for prose assertions."""
    return re.sub(r"[*`]", "", live_core(relative))


class SixStatLockTests(unittest.TestCase):
    def test_the_canonical_data_file_locks_the_six(self) -> None:
        canon = json.loads(read(CORE))
        self.assertEqual(canon["stats"]["final_list"], list(SIX))
        self.assertEqual(canon["stats"]["names"], dict(zip(SIX, SIX_NAMES)))
        # the skill list is still open and must keep reading as deferred
        self.assertEqual(canon["skills"]["final_list"], "deferred")

    def test_the_live_rulebook_states_the_six_base_stats(self) -> None:
        core = read(RULEBOOK).split(CORE_MARKER, 1)[0]
        for code, name in zip(SIX, SIX_NAMES):
            with self.subTest(code=code):
                self.assertIn(code, core)
                self.assertIn(name, core)

    def test_the_live_stat_table_has_exactly_six_rows(self) -> None:
        """A seventh stat must not be able to slip in beside the six.

        The other tests are all "the six are present" checks, so an added row would
        pass every one of them. Count the model's own table instead: extract the STAT
        table and assert its row count, because attribute bloat was the failure mode
        this whole issue was opened to fix.
        """
        core = read(RULEBOOK).split(CORE_MARKER, 1)[0]
        match = re.search(
            r"(?ms)^\|\s*STAT\s*\|[^\n]*\n\|[-\s|]+\|\n((?:\|[^\n]*\n)+)",
            core,
        )
        self.assertIsNotNone(match, "the six-stat table is missing from the live rulebook")
        assert match is not None  # narrows the type for the row extraction below
        rows = [ln for ln in match.group(1).splitlines() if ln.strip().startswith("|")]
        self.assertEqual(len(rows), 6, f"the STAT table has {len(rows)} rows, not six: {rows}")
        for row, code in zip(rows, SIX):
            with self.subTest(code=code):
                self.assertIn(f"**{code}**", row)

    def test_the_attribute_stub_lists_exactly_six_stat_sections(self) -> None:
        text = read(ATTRIBUTES)
        section = text.split("## The six base STATS", 1)
        self.assertEqual(len(section), 2, "the stub's six-stat section is missing")
        body = section[1].split("## The four-layer ontology", 1)[0]
        headings = re.findall(r"(?m)^### (.+)$", body)
        self.assertEqual(len(headings), 6, f"the stub defines {len(headings)} STATS: {headings}")
        for heading, name in zip(headings, SIX_NAMES):
            with self.subTest(name=name):
                self.assertIn(name, heading)

    def test_the_attribute_stub_states_the_six_base_stats(self) -> None:
        text = read(ATTRIBUTES)
        self.assertIn("FIT / REF / INT / SOC / CYB / PSY", text)
        for name in SIX_NAMES:
            with self.subTest(name=name):
                self.assertIn(f"### {name}", text)

    def test_the_six_count_is_stated_so_it_cannot_drift_quietly(self) -> None:
        for doc in (RULEBOOK, ATTRIBUTES):
            with self.subTest(doc=doc):
                self.assertRegex(
                    live_body(doc), r"six\s+base\s+STATS|six\s+STATS",
                    "the six-stat count is no longer stated",
                )

    def test_the_live_core_does_not_carry_the_retired_twelve(self) -> None:
        """The old twelve live on only in the preserved ledger, never as live canon."""
        core = live_core(RULEBOOK)
        for retired in ("Noesis (NOE)", "Integration (CYI)", "Reason (REA)",
                        "Resilience (RES)", "Intuition (INU)"):
            with self.subTest(retired=retired):
                self.assertNotIn(retired, core)
        self.assertNotRegex(core, r"three STATS in\s+each layer")

    def test_no_retired_stat_is_still_shown_as_a_live_table_row(self) -> None:
        """A retired concept must not appear as a live STAT table row.

        A document-wide `\\bWIL\\b` sweep would collide with prose, so pin the one
        form only a live STAT list uses: a markdown row naming the concept and code.
        """
        for doc in (RULEBOOK, ATTRIBUTES):
            body = live_core(doc)
            for concept, code in (("Resilience", "RES"), ("Reason", "REA"),
                                  ("Empathy", "EMP"), ("Presence", "PRE"),
                                  ("Will", "WIL"), ("Intuition", "INU"),
                                  ("Noesis", "NOE"), ("Integration", "CYI"),
                                  ("Bandwidth", "BND"), ("Control", "CTL")):
                with self.subTest(doc=doc, concept=concept):
                    self.assertNotRegex(
                        body, rf"\|[^\n|]*{concept} \({code}\)",
                        f"{concept} ({code}) is a retired #113 STAT still shown as live",
                    )

    def test_the_four_layers_are_still_four_and_still_named(self) -> None:
        """#131 replaces the STAT list, not the layer ontology."""
        for doc in (RULEBOOK, ATTRIBUTES):
            text = live_core(doc)
            for layer in LAYERS:
                with self.subTest(doc=doc, layer=layer):
                    self.assertIn(layer, text)
        core = live_core(RULEBOOK)
        for wrong in ("five layers", "five-layer", "four layers plus"):
            with self.subTest(wrong=wrong):
                self.assertNotIn(wrong, core)

    def test_cybernetic_is_still_a_noopunk_extension(self) -> None:
        text = live_core(RULEBOOK) + " " + read(ATTRIBUTES)
        self.assertRegex(
            text,
            r"Luhmann|noöpunk\s+(extension|adds|adaptation)|fourth\s+(type|domain|system)",
        )

    def test_compute_interface_network_are_equipment_statistics(self) -> None:
        """The author moved them to hardware/system statistics on #131.

        The positive half asserts the equipment claim; the negative half fails if
        they are re-promoted into the character STAT table, which is the realistic
        regression (they were proposed as a cybernetic stat block before #131).
        """
        joined = live_core(RULEBOOK) + " " + read(ATTRIBUTES)
        for name in HARDWARE:
            with self.subTest(name=name):
                self.assertIn(name, joined, f"{name} should be documented as hardware")
        self.assertRegex(
            joined,
            r"hardware/system statistics|hardware\s+statistics|"
            r"equipment statistics|system statistics",
            "the document no longer states that COMPUTE/INTERFACE/NETWORK are "
            "equipment statistics rather than character attributes",
        )
        # none of the three may appear as a row in a STAT table
        for doc in (RULEBOOK, ATTRIBUTES):
            body = live_core(doc)
            for name in HARDWARE:
                with self.subTest(doc=doc, name=name):
                    self.assertNotRegex(
                        body, rf"\|[^\n|]*\*\*{name}\*\*|\|\s*{name}\s*\|",
                        f"{name} is an equipment statistic, not a character STAT",
                    )

    def test_the_six_do_not_reintroduce_a_mental_or_ego_layer(self) -> None:
        core = live_core(RULEBOOK)
        self.assertNotIn("Mental/Ego layer that", core)
        self.assertRegex(core, r"[Tt]here is no generic Mental/Ego layer")

    def test_the_1_to_10_scale_and_na_rule_survive(self) -> None:
        for doc in (RULEBOOK, ATTRIBUTES):
            body = live_core(doc)
            with self.subTest(doc=doc):
                self.assertIn("1–10", body)
                self.assertRegex(body, r"0 does not mean absence|0 is not used for absence")
                self.assertIn("N/A", body)

    def test_no_generation_procedure_was_invented(self) -> None:
        """#131 locks a STAT list, not a point-buy or rolling method."""
        joined = live_core(RULEBOOK) + " " + read(ATTRIBUTES)
        for forbidden in ("point-buy", "point buy", "roll 3d6", "3d6", "27 points"):
            with self.subTest(forbidden=forbidden):
                self.assertNotIn(forbidden.lower(), joined.lower())


if __name__ == "__main__":
    unittest.main()
