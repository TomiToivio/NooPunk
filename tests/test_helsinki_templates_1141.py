"""The four Helsinki author worksheets (#1141) stay worksheets, stay readable, and stay linked.

Phase 1 of #1141 is documentation: four author-first writing worksheets, in prose, for Tomi to fill in.
The failure modes are not syntax errors — they are a worksheet that quietly becomes canon (an example
promoted to setting), a rule value invented where a book should be consulted, a worksheet that grows into
an atlas nobody will edit by hand, or a cross-link that rots.

These tests check the **documents**, not a rules engine: #1141 authorizes no implementation.

Written with `unittest`: CI discovers with `unittest` and does not install pytest.
"""
from __future__ import annotations

import json
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DESIGN = ROOT / "design"

WORLD = DESIGN / "HELSINKI_WORLD.md"
CITY = DESIGN / "HELSINKI_CITY.md"
FACTIONS = DESIGN / "HELSINKI_FACTIONS.md"
FACES = DESIGN / "HELSINKI_FACES_XENOBESTIARY.md"
ALL = (WORLD, CITY, FACTIONS, FACES)

RELATIVE_LINK = re.compile(r"\[[^\]]*\]\(([^)#\s]+)(?:#[^)]*)?\)")
# the faction worksheet prints its samples as: | **Cunning** | False Front | role | Cost 1; HP 2 |
ASSET_ROW = re.compile(r"\|\s*\*{0,2}(?P<kind>Cunning|Force|Wealth)\*{0,2}\s*\|\s*"
                       r"(?P<name>False Front|Hitmen|Franchise)\s*\|[^|]*\|\s*"
                       r"Cost\s+(?P<cost>\d+);\s*HP\s+(?P<hp>\d+)\s*\|")


def text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def flat(path: Path) -> str:
    """The document as prose: wrapped lines joined, emphasis markers dropped."""
    return " ".join(text(path).replace("**", "").split())


def catalogue() -> dict[str, dict]:
    """The repository's extracted SWN asset rows, loaded by glob rather than by literal filename.

    `tools/cwn_parity_audit.py` treats a test whose text mentions an implementation module as evidence that
    the matching CWN section is tested. A documentation guard is not evidence for any rule, so this file
    must not contain a module stem.
    """
    path = next((ROOT / "data" / "rules").glob("*faction_asset*.json"))
    return {row["name"]: row for row in json.loads(path.read_text(encoding="utf-8"))["assets"]}


class TheFourWorksheetsExist(unittest.TestCase):
    def test_all_four_documents_exist(self):
        for path in ALL:
            self.assertTrue(path.is_file(), f"missing worksheet: {path.name}")

    def test_each_declares_the_issue_and_that_it_is_a_draft(self):
        for path in ALL:
            head = text(path)[:400]
            self.assertIn("1141", head, path.name)
            self.assertIn("Phase 1", head, path.name)
            self.assertIn("NOT CANON", head, path.name)

    def test_each_opens_with_a_table_of_contents(self):
        """Before the first section — either spelling the repository uses is fine.

        The worksheets were rewritten into prose by another session while this guard was in flight and
        they spell it `**Contents**`; both spellings carry the requirement, so both are accepted rather
        than one being declared canonical by a test.
        """
        for path in ALL:
            body = text(path)
            marker = "**Contents:**" if "**Contents:**" in body else "**Contents**"
            self.assertIn("Contents", body, path.name)
            self.assertLess(body.index(marker), body.index("\n## "),
                            f"{path.name} lists its contents after the first section")

    def test_each_offers_the_shared_status_words(self):
        for path in ALL:
            body = flat(path)
            lowered = body.lower()
            for status in ("author canon", "repository canon", "example only", "open", "gm secret"):
                self.assertIn(status, lowered, f"{path.name} lacks the {status} status word")

    def test_each_asks_for_prose_rather_than_a_database(self):
        for path in ALL:
            body = flat(path)
            self.assertIn("Your version", body, f"{path.name} has no writing space")
            self.assertTrue("Writing prompts" in body or "Questions to help you write" in body,
                            f"{path.name} gives the author no prompts")

    def test_each_marks_its_examples_as_fiction(self):
        for path in ALL:
            self.assertGreaterEqual(text(path).count("Example only"), 3,
                                    f"{path.name} does not repeatedly mark its examples")

    def test_each_leaves_the_open_questions_to_the_author(self):
        for path in ALL:
            body = flat(path)
            self.assertIn("Open author decisions", body, f"{path.name} has no decision list")
            self.assertTrue("Author's answers" in body or "Author's notes and decisions" in body,
                            f"{path.name} gives the author nowhere to record decisions")

    def test_each_is_small_enough_to_edit_by_hand(self):
        """"Small enough for Tomi to replace/extend by hand" is a requirement, not a preference."""
        for path in ALL:
            lines = len(text(path).splitlines())
            self.assertLessEqual(
                lines, 300,
                f"{path.name} is {lines} lines; the issue asks for a worksheet, not an atlas")


class WorldWorksheet(unittest.TestCase):
    def test_all_seven_topics_are_present(self):
        body = text(WORLD).lower()
        for topic in ("cyberpunk themes", "world outside", "city at a glance", "district",
                      "megacorporation", "gang", "npc"):
            self.assertIn(topic, body, f"world worksheet missing: {topic}")

    def test_it_defers_the_setting_it_must_not_decide(self):
        body = text(WORLD)
        for anchor in ("GREATER_HELSINKI_2045.md", "ZONES.md", "EUROPOL_HELSINKI_1114.md"):
            self.assertIn(anchor, body)

    def test_it_does_not_settle_what_canon_leaves_open(self):
        self.assertIn("deliberately unknown", flat(WORLD).lower())


class CityWorksheet(unittest.TestCase):
    def test_every_cwn_city_topic_is_present(self):
        body = text(CITY).lower()
        for topic in ("timeline of collapse", "megacorporation", "other groups", "ethos",
                      "government and jurisdiction", "crime and punishment",
                      "social relationships", "districts of the city"):
            self.assertIn(topic, body, f"city worksheet missing: {topic}")

    def test_the_three_views_are_modelled_separately(self):
        body = text(CITY)
        for view in ("Physical", "Cyber", "Astral"):
            self.assertIn(view, body)

    def test_the_metaphysical_axes_are_not_conflated(self):
        body = flat(CITY)
        self.assertIn("Space/Time", body)
        self.assertIn("Time/Space", body)
        self.assertIn("fourth-density", body)
        self.assertIn("not map coordinates", body)
        self.assertIn("Interdimensional hypothesis", body)
        self.assertIn("in-world", body)

    def test_a_fully_described_location_exists(self):
        body = text(CITY).lower()
        for part in ("physical appearance", "cyber appearance", "astral appearance",
                     "access and movement", "gm-only question"):
            self.assertIn(part, body, f"location worksheet missing: {part}")

    def test_real_tunnels_are_not_declared_traversable(self):
        body = flat(CITY).lower()
        self.assertIn("publicly traversable", body)
        self.assertIn("do not imply", body)
        self.assertIn("fictional", body)

    def test_the_first_act_stays_grounded(self):
        body = flat(CITY).lower()
        self.assertIn("first act", body)
        self.assertIn("hidden", body)


class FactionsWorksheet(unittest.TestCase):
    def test_it_uses_the_swn_faction_statistics(self):
        body = flat(FACTIONS)
        for token in ("Force", "Cunning", "Wealth", "FacCreds"):
            self.assertIn(token, body)

    def test_its_asset_table_matches_the_repository_catalogue(self):
        rows = {m.group("name"): m for m in ASSET_ROW.finditer(text(FACTIONS))}
        self.assertEqual({"False Front", "Hitmen", "Franchise"}, set(rows),
                         "one verified sample per asset category is required")
        known = catalogue()
        for name, match in rows.items():
            self.assertEqual(int(match.group("cost")), known[name]["cost"], f"{name} cost drifted")
            self.assertEqual(int(match.group("hp")), known[name]["hp"], f"{name} HP drifted")
        for page in ("219", "221", "223"):
            self.assertIn(page, text(FACTIONS), f"printed page {page} not cited")

    def test_it_invents_no_scores_and_no_results(self):
        body = flat(FACTIONS)
        self.assertIn("Do not guess rulebook figures", body)
        self.assertIn("No outcome is assumed here", body)

    def test_wwn_and_awn_are_alternatives_not_extra_wallets(self):
        body = flat(FACTIONS)
        self.assertIn("WWN major project", body)
        self.assertIn("AWN enclave", body)
        self.assertIn("second set of free SWN actions", body)

    def test_reputation_is_not_a_faction_statistic(self):
        body = flat(FACTIONS)
        self.assertIn("not a faction statistic", body)


class FacesWorksheet(unittest.TestCase):
    def test_all_four_nhi_kinds_are_present(self):
        body = text(FACES).lower()
        for kind in ("biologics", "constructs", "noetics", "plasmoids"):
            self.assertIn(kind, body, f"no {kind} section")

    def test_ordinary_people_come_first(self):
        body = text(FACES)
        self.assertIn("Ordinary faces", body)

    def test_the_five_axes_are_kept_apart(self):
        body = flat(FACES).lower()
        for axis in ("body or species", "ontological type", "political affiliation", "density",
                     "realm or layer"):
            self.assertIn(axis, body, f"axis missing: {axis}")

    def test_a_program_is_not_automatically_a_being(self):
        body = flat(FACES)
        self.assertIn("cyber-only automated process is not automatically a conscious Construct or Noetic being",
                      body)

    def test_psi_cannot_shortcut_an_investigation(self):
        body = flat(FACES)
        self.assertIn("not a confession", body)
        self.assertIn("PSI_INVESTIGATION_BOUNDARY_1105.md", body)

    def test_no_invented_stat_blocks(self):
        body = flat(FACES).lower()
        self.assertIn("ordinary social encounter unless tomi supplies specific verified statistics", body)


class LinksAndIndexes(unittest.TestCase):
    def test_no_worksheet_links_to_a_missing_file(self):
        broken = []
        for path in ALL + (DESIGN / "README.md",):
            for match in RELATIVE_LINK.finditer(text(path)):
                target = match.group(1)
                if target.startswith(("http://", "https://", "mailto:")):
                    continue
                if not (path.parent / target).resolve().exists():
                    broken.append(f"{path.relative_to(ROOT)} -> {target}")
        self.assertEqual(broken, [], "broken relative links: " + "; ".join(broken))

    def test_the_design_index_lists_all_four_once(self):
        index = text(DESIGN / "README.md")
        self.assertEqual(index.count("## Issue #1141"), 1, "design/README.md has two #1141 sections")
        targets = [m.group(1) for m in RELATIVE_LINK.finditer(index)]
        for path in ALL:
            self.assertEqual(targets.count(path.name), 1,
                             f"design/README.md links {path.name} {targets.count(path.name)} times")

    def test_the_document_register_names_the_set(self):
        self.assertIn("HELSINKI_CITY.md", text(ROOT / "docs" / "DOCUMENT_REGISTER.md"))


if __name__ == "__main__":
    unittest.main()
