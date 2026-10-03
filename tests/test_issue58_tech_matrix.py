"""Structure guard for the regional technology matrix (issue #58).

This is a STRUCTURE guard in the style of the other issue guards here. It asserts
that the matrix exists, is internally coherent, and preserves the properties issue #58
depends on. It deliberately does NOT check which region holds which value — that is
authorial worldbuilding, and a test asserting it would freeze setting material.

What is protected:

* the matrix exists and is valid JSON with the repository's world-data conventions;
* all seven regions and all thirteen dimensions the issue names are present;
* every region profile is complete across every dimension (an explicit `unassigned`
  is a value; a missing key is a bug);
* **every dimension value is a member of its own ladder** — a typo like "ubiquituous"
  would otherwise pass silently and read as a capability claim;
* **there is no numeric technology score and no derived modifier anywhere** — the
  issue's central claim is that technological regimes are incomparable, so a scalar
  would collapse it;
* **every region carries a gains/vulnerabilities pair, with at least one
  vulnerability** — that is the issue's anti-ranking rule;
* the rogue-AGI catastrophes exist, in order, and the second carries an explicit
  supersession of the single-event `TIMELINE.md` wording rather than a silent rewrite;
  issue #89 extends the structure from two to four, recorded as a further explicit
  supersession;
* the open metaphysical readings the issue says to keep ambiguous are recorded as
  unresolved and are not decided;
* dates stay at 20XX (AGENTS.md §6);
* the author's own open questions are carried as unassigned, not answered.

Run: python3 -m unittest discover -s tests -p "test_*.py"
"""
from __future__ import annotations

import json
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MATRIX = "data/world/tech_matrix.json"
DOC = "docs/archive/TECH_MATRIX.md"
TIMELINE = "rulebook/7_TIMELINE.md"

#: The issue's own regional section headings.
REGIONS = (
    "united-states",
    "european-federation",
    "china",
    "russia",
    "middle-east",
    "india",
    "sub-saharan-africa",
)

#: The issue's own dimension list, in its order.
DIMENSIONS = (
    "ai_autonomy", "robotics", "cybernetics", "bci", "biotech", "virtuality",
    "space", "energy", "manufacturing", "psionics", "noosphere", "governance",
    "ecology",
)

UNASSIGNED = "unassigned"

#: Words that would indicate a scalar technology level crept in.
SCALAR_HINTS = (
    "tech_level", "techlevel", "technology_level", "tech_score", "tech_rating",
    "advancement_level", "development_index", "capability_score",
)


def load() -> dict:
    return json.loads((ROOT / MATRIX).read_text(encoding="utf-8"))


def read(relative: str) -> str:
    return (ROOT / relative).read_text(encoding="utf-8")


class MatrixExistsTests(unittest.TestCase):
    def test_matrix_exists_and_parses(self) -> None:
        self.assertTrue((ROOT / MATRIX).exists(), f"{MATRIX} is missing")
        self.assertIsInstance(load(), dict)

    def test_follows_the_world_data_conventions(self) -> None:
        data = load()
        self.assertEqual(data["format"], "noopunk.world.tech_matrix")
        self.assertIsInstance(data["version"], int)
        self.assertEqual(data["time_convention"], "20XX")
        self.assertIn("$comment", data)
        self.assertIn("$sources", data)

    def test_doc_exists_and_points_at_the_json(self) -> None:
        self.assertTrue((ROOT / DOC).exists(), f"{DOC} is missing")
        self.assertIn("tech_matrix.json", read(DOC))


class CoverageTests(unittest.TestCase):
    def test_all_seven_regions_present(self) -> None:
        ids = [r["id"] for r in load()["regions"]]
        self.assertEqual(sorted(ids), sorted(REGIONS))
        self.assertEqual(len(ids), len(set(ids)), "duplicate region id")

    def test_all_thirteen_dimensions_present_in_the_issue_order(self) -> None:
        self.assertEqual(tuple(d["id"] for d in load()["dimensions"]), DIMENSIONS)

    def test_every_dimension_declares_an_open_ladder(self) -> None:
        for dim in load()["dimensions"]:
            with self.subTest(dimension=dim["id"]):
                self.assertIsInstance(dim.get("ladder"), list)
                self.assertGreaterEqual(len(dim["ladder"]), 3)

    def test_every_region_profile_covers_every_dimension(self) -> None:
        """A missing key is a bug; an explicit `unassigned` is a value."""
        data = load()
        for region in data["regions"]:
            with self.subTest(region=region["id"]):
                self.assertEqual(set(region["profile"]), set(DIMENSIONS))


class LadderMembershipTests(unittest.TestCase):
    def test_every_assigned_value_is_a_member_of_its_own_ladder(self) -> None:
        """Catches typos, which would otherwise read as capability claims."""
        data = load()
        ladders = {d["id"]: set(d["ladder"]) for d in data["dimensions"]}
        for region in data["regions"]:
            for dimension, value in region["profile"].items():
                if value == UNASSIGNED:
                    continue
                with self.subTest(region=region["id"], dimension=dimension):
                    self.assertIn(
                        value, ladders[dimension],
                        f"{region['id']}.{dimension}={value!r} is not in the ladder "
                        f"{sorted(ladders[dimension])}",
                    )


class NoRankingTests(unittest.TestCase):
    """The issue's central claim: regimes are incomparable, not ranked."""

    def test_no_numeric_technology_score_anywhere(self) -> None:
        text = read(MATRIX)
        for hint in SCALAR_HINTS:
            with self.subTest(hint=hint):
                self.assertNotIn(hint, text.lower())
        # No numeric value may be attached to a dimension value.
        for dim in load()["dimensions"]:
            for value in dim["ladder"]:
                with self.subTest(value=value):
                    self.assertNotRegex(value, r"\d")

    def test_every_region_has_a_gains_and_vulnerabilities_pair(self) -> None:
        for region in load()["regions"]:
            with self.subTest(region=region["id"]):
                self.assertTrue(region.get("gains"), "a region with no gains is a strawman")
                self.assertTrue(
                    region.get("vulnerabilities"),
                    "the issue forbids a region that is simply more advanced: every "
                    "profile must carry at least one vulnerability",
                )

    def test_the_us_and_europe_are_given_different_kinds_of_strength(self) -> None:
        """Spot-check the incomparability claim on the issue's clearest contrast."""
        by_id = {r["id"]: r for r in load()["regions"]}
        us, eu = by_id["united-states"], by_id["european-federation"]
        self.assertNotEqual(us["profile"], eu["profile"])
        self.assertNotEqual(us["gains"], eu["gains"])

    def test_the_anti_trope_region_is_not_given_material_ruin(self) -> None:
        """Sub-Saharan Africa must not be a ruined extraction zone."""
        region = {r["id"]: r for r in load()["regions"]}["sub-saharan-africa"]
        joined = " ".join(region["vulnerabilities"]).lower()
        for trope in ("ruin", "extraction zone", "poverty", "collapse"):
            with self.subTest(trope=trope):
                self.assertNotIn(trope, joined)


class CatastropheTests(unittest.TestCase):
    def test_catastrophes_in_order(self) -> None:
        """The structure is four: #58 specified two, and issue #89 extended it."""
        cats = load()["catastrophes"]
        self.assertEqual(len(cats), 4)
        self.assertEqual([c["ordinal"] for c in cats],
                         ["first", "second", "third", "fourth"])

    def test_the_original_two_retain_their_severity_and_resolution(self) -> None:
        first, second = load()["catastrophes"][:2]
        self.assertNotEqual(first["severity"], second["severity"])
        self.assertNotEqual(first["resolution"], second["resolution"])

    def test_the_second_supersedes_the_timeline_explicitly(self) -> None:
        """A timeline change must be recorded, not applied silently."""
        second = load()["catastrophes"][1]
        self.assertIsInstance(second.get("supersedes"), dict)
        self.assertEqual(second["supersedes"]["target_file"], "TIMELINE.md")

    def test_the_fourth_records_the_issue_89_extension(self) -> None:
        """#89 extended the two-event structure to four; the extension must be recorded."""
        fourth = load()["catastrophes"][3]
        self.assertIsInstance(fourth.get("supersedes"), dict)
        self.assertIn("#89", fourth["supersedes"]["reason"])

    def test_the_third_and_fourth_do_not_invent_severity(self) -> None:
        """#89 states no severity or resolution for the third and fourth."""
        third, fourth = load()["catastrophes"][2:4]
        for cat in (third, fourth):
            with self.subTest(cat=cat["id"]):
                self.assertEqual(cat["severity"], "unassigned")
                self.assertEqual(cat["resolution"], "unassigned")

    def test_the_timeline_records_the_two_event_structure(self) -> None:
        text = read(TIMELINE)
        self.assertIn("Rogue AGI / ASI Disasters in the United States", text)
        self.assertIn("First Rogue AGI Holocaust", text)
        self.assertIn("Second Rogue AGI Holocaust", text)
        self.assertIn("#58", text, "the supersession must name the issue that caused it")

    def test_real_company_names_are_marked_setting_fiction(self) -> None:
        """The issue warns these are speculative; the artefact must say so."""
        data = load()
        self.assertIn("$company_attribution_note", data)
        note = data["$company_attribution_note"].lower()
        self.assertIn("setting fiction", note)
        self.assertIn("not", note)
        self.assertIn("real", note)


class OpenQuestionTests(unittest.TestCase):
    def test_jinn_remains_in_world_unknown(self) -> None:
        region = {r["id"]: r for r in load()["regions"]}["middle-east"]
        note = region.get("$jinn_note", "").lower()
        self.assertIn("in-world unknown", note)
        self.assertIn("must not", note, "the refusal must be stated so it cannot be resolved")

    def test_ganesh_remains_open(self) -> None:
        region = {r["id"]: r for r in load()["regions"]}["india"]
        self.assertIn("open", region.get("$open_reading", "").lower())

    def test_the_author_open_questions_are_carried_not_answered(self) -> None:
        questions = load()["open_questions_unassigned"]
        self.assertGreaterEqual(len(questions), 8)
        joined = " ".join(questions).lower()
        for topic in ("era", "globally mature", "region-specific", "eclipse phase"):
            with self.subTest(topic=topic):
                self.assertIn(topic, joined)

    def test_china_is_left_deliberately_sparse(self) -> None:
        """The issue asks to preserve mystery; filling it in would break that."""
        region = {r["id"]: r for r in load()["regions"]}["china"]
        unassigned = sum(1 for v in region["profile"].values() if v == UNASSIGNED)
        self.assertGreaterEqual(
            unassigned, len(DIMENSIONS) // 2,
            "the majority of China's cells must stay unassigned to preserve opacity",
        )

    def test_unassigned_summary_count_matches_the_data(self) -> None:
        """A stated count that disagrees with the data is a fabricated claim."""
        data = load()
        actual = sum(
            1 for r in data["regions"] for k in DIMENSIONS if r["profile"][k] == UNASSIGNED
        )
        summary = data["$unassigned_summary"]
        match = re.search(r"\b(\d+)\b", summary)
        self.assertIsNotNone(match, "the summary must state a count")
        assert match is not None
        claimed = int(match.group(1))
        self.assertEqual(claimed, actual, "the summary count must match the matrix")

    def test_no_dates_beyond_20XX_are_assigned(self) -> None:
        """AGENTS.md §6: agents must not assign exact future dates."""
        text = read(MATRIX)
        # A concrete *date* is a year attached to an event. Note the trap: the
        # reference-game title "Cyberpunk 2020/RED" contains four digits and is not a
        # date, so a naive four-digit scan fails on correct text. Exclude it by
        # stripping the known reference-game titles before scanning.
        for title in ("Cyberpunk 2020/RED", "Cyberpunk 2020", "Cyberpunk 2013/RED"):
            text = text.replace(title, "<reference-game-title>")
        concrete = re.findall(r"\b(?:19|20)\d{2}\b", text)
        self.assertEqual(concrete, [], f"the matrix assigns concrete years: {concrete}")
        self.assertIn("20XX", read(DOC))

        # The timeline is where dates actually live, and this issue rewrote part of
        # it, so scan it too -- an earlier version of this guard only checked the
        # matrix and let a concrete year into TIMELINE.md unnoticed.
        timeline = read(TIMELINE)
        # Scope to headings that are *dated at all*: TIMELINE.md legitimately carries
        # undated section headings too, so asserting every heading starts with 20XX
        # would fail on correct text.
        dated = [
            h for h in re.findall(r"(?m)^##\s*(.+)$", timeline)
            if re.search(r"\b(?:19|20)\d{2}\b|\b20XX\b", h)
        ]
        self.assertTrue(dated, "expected dated timeline headings to check")
        for heading in dated:
            with self.subTest(heading=heading[:40]):
                self.assertTrue(
                    heading.startswith("20XX"),
                    f"a timeline heading assigns a concrete date: {heading!r}",
                )


class AntiMechanicsTests(unittest.TestCase):
    def test_the_doc_defines_no_rpg_mechanics(self) -> None:
        """AGENTS.md §4 keeps equipment, economy and simulation mechanics unresolved."""
        text = read(DOC).lower()
        # The doc names these in order to *refuse* them, so a bare absence check
        # would fail on correct text. What must not exist is an assignment: a
        # mechanic given a value.
        for mechanic in ("point cost is", "costs \\d", "rolls? \\d+d\\d", "damage rating is"):
            with self.subTest(mechanic=mechanic):
                self.assertNotRegex(text, mechanic)

    def test_the_doc_says_the_gameplay_section_is_guidance_only(self) -> None:
        text = read(DOC).lower()
        self.assertIn("produce no rules here", text)
        self.assertIn("narrative guidance", text)

    def test_runtimes_must_not_derive_a_scalar(self) -> None:
        guidance = load()["runtime_guidance"]
        self.assertIn("no", guidance["shared"].lower())
        self.assertIn("numeric technology score", guidance["shared"].lower())

    def test_refusal_not_penalty_is_recorded_for_concordia(self) -> None:
        """Mirrors the absent-system shape in the rules layer."""
        guidance = load()["runtime_guidance"]["concordia"].lower()
        self.assertIn("refused", guidance)


if __name__ == "__main__":
    unittest.main()
