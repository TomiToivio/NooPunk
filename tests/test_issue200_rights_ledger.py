"""Guard for the game-system rights ledger (issue #200).

Issue #200 replaces NooPunk's closed-system design framing with a fully Creative Commons
direction, and demands that this happen through a rights audit rather than by assertion:
"audit before deleting", "verify the specific CWN/SWN/AW license at publisher or actual SRD,
not mirror assertion", and "no blanket assumption that a full game is CC because it has a free
SRD".

The findings themselves are dated observations and legitimately change -- a licence can be
relicensed, a blocked page can come back. What must NOT drift is the machinery:

* the ledger and its document exist and point at each other;
* every system #200 names is accounted for -- a source quietly dropped from the audit is the
  failure mode, because the audit is what a later importer would trust;
* the decision vocabulary is closed, so "blocked" and "no grant" cannot be laundered into
  "fine to use";
* **nothing is marked reusable without a verification method and a date** -- the rule that
  turns the ledger from documentation into a gate;
* **the proprietary systems are never marked reusable**, and the NonCommercial ones are
  explicitly excluded from a commercially reusable release;
* a blocked fetch is recorded as blocked rather than as a licence finding;
* nothing is recorded as imported;
* the author-owned authority conflict is recorded, and is not silently resolved by an agent;
* the audit inventory's live claim sites still exist, so the audit cannot go stale by
  attrition.

Run: python3 -m unittest discover -s tests -p "test_*.py"
"""
from __future__ import annotations

import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LEDGER = ROOT / "data" / "sources" / "game_system_rights.json"
AUDIT_DOC = ROOT / "docs" / "sources" / "GAME_SYSTEM_RIGHTS.md"
AGENTS = ROOT / "AGENTS.md"

#: An entry MUST use one of these. The point is that the permissive-sounding verdicts are
#: reserved for sources whose licence was actually read.
DECISIONS = {
    "verified-permissive",
    "verified-public-domain",
    "verified-nc-sharealike",
    "no-cc-grant-established",
    "blocked-unverified",
    "proprietary-out-of-scope",
}

#: Verdicts that assert a reusable licence -- these carry the evidence burden.
REUSABLE = {"verified-permissive", "verified-public-domain"}

#: (label, needle) for every system #200 names, in its own words.
REQUIRED_SOURCES = (
    ("Fate", "fate"),
    ("Fudge", "fudge"),
    ("Psi-Punk", "psi-punk"),
    ("Eclipse Phase", "eclipse"),
    ("Transhumanity's Fate", "transhumanity"),
    ("Cities Without Number", "cities-without-number"),
    ("Stars Without Number", "stars-without-number"),
    ("Apocalypse World", "apocalypse-world"),
    ("The Veil", "veil"),
    ("Cyberpunk RED", "cyberpunk"),
    ("CY_BORG", "cy-borg"),
    ("Shadowrun", "shadowrun"),
    ("Neon City Overdrive / Otherscape / GURPS / Sprawl / Expanse", "other-proprietary"),
    ("computer-game references", "computer-game"),
)


def ledger() -> dict:
    return json.loads(LEDGER.read_text(encoding="utf-8"))


class LedgerShapeTests(unittest.TestCase):
    def test_the_ledger_and_its_document_exist(self) -> None:
        self.assertTrue(LEDGER.is_file(), "the machine-readable ledger is missing")
        self.assertTrue(AUDIT_DOC.is_file(), "the audit document is missing")

    def test_they_point_at_each_other(self) -> None:
        """A ledger nobody links is a ledger nobody trusts."""
        doc = AUDIT_DOC.read_text(encoding="utf-8")
        self.assertIn("game_system_rights.json", doc)
        self.assertTrue(ledger()["issue"].endswith("/200"))

    def test_it_is_a_versioned_format_like_the_issue_60_ledger(self) -> None:
        d = ledger()
        self.assertEqual(d["format"], "noopunk.sources.game_system_rights")
        self.assertIsInstance(d["version"], int)
        self.assertEqual(d["retrieved"], "2026-10-10")

    def test_the_licence_decision_is_recorded_as_open(self) -> None:
        """#200 asks for an explicit choice; an agent must not make it silently."""
        t = ledger()["target_license"]
        self.assertIn("CC BY-SA 4.0", t["rulebook_and_original_setting"]["recommended"])
        self.assertIn("CC BY 4.0", t["rulebook_and_original_setting"]["alternative"])
        self.assertIn("NOT RATIFIED", t["status"])
        # code is not a CC surface
        self.assertRegex(t["code"]["license"], r"MIT|Apache|GPL")


class CoverageTests(unittest.TestCase):
    def test_every_system_the_issue_names_is_accounted_for(self) -> None:
        blob = json.dumps(ledger()).lower()
        for label, needle in REQUIRED_SOURCES:
            with self.subTest(source=label):
                self.assertIn(needle, blob, f"{label} is missing from the rights ledger")

    def test_the_decision_vocabulary_is_closed(self) -> None:
        for entry in ledger()["sources"]:
            with self.subTest(source=entry["id"]):
                self.assertIn(entry["decision"], DECISIONS,
                              f"{entry['id']} invents a decision outside the vocabulary")


class GateTests(unittest.TestCase):
    """The clauses that make the ledger a gate rather than a description."""

    def test_nothing_is_marked_reusable_without_a_verification(self) -> None:
        for entry in ledger()["sources"]:
            if entry["decision"] not in REUSABLE:
                continue
            with self.subTest(source=entry["id"]):
                self.assertTrue(entry.get("how_verified"),
                                f"{entry['id']} claims a reusable licence with no method")
                self.assertRegex(entry.get("license_checked", ""), r"\d{4}-\d{2}-\d{2}",
                                 f"{entry['id']} has no dated check")

    def test_no_proprietary_system_is_marked_reusable(self) -> None:
        for entry in ledger()["sources"]:
            if entry["decision"] != "proprietary-out-of-scope":
                continue
            with self.subTest(source=entry["id"]):
                self.assertNotIn(entry["decision"], REUSABLE)
                self.assertNotRegex(entry.get("license", ""), r"\bCC BY\b")

    def test_noncommercial_sources_are_excluded_from_commercial_reuse(self) -> None:
        nc = [e for e in ledger()["sources"] if e["decision"] == "verified-nc-sharealike"]
        self.assertTrue(nc, "the NC-bound sources vanished from the ledger")
        for entry in nc:
            with self.subTest(source=entry["id"]):
                self.assertRegex(entry["license"], r"NC")
        self.assertIn("NOT usable in a commercially reusable", ledger()["reuse_rules"]["cc_by_nc_sa"])

    def test_a_blocked_fetch_is_not_recorded_as_a_licence_finding(self) -> None:
        blocked = [e for e in ledger()["sources"] if e["decision"] == "blocked-unverified"]
        self.assertTrue(blocked, "the blocked verifications vanished")
        for entry in blocked:
            with self.subTest(source=entry["id"]):
                self.assertNotIn(entry["decision"], REUSABLE,
                                 "a blocked source claims a reusable licence")
                # A blocked entry may still RECORD a party's own claim (The Veil's attached
                # edition says BY-SA 3.0, and a sibling agent read Psi-Punk's page), but it
                # must say plainly that it was not verified here.
                self.assertRegex(entry.get("how_verified", ""),
                                 r"(?i)could not verify|not verified|not verify"
                                 r"|not independently reproduced|recorded as reported",
                                 f"{entry['id']} is blocked but does not say so")

    def test_public_availability_is_explicitly_not_a_licence(self) -> None:
        rules = ledger()["reuse_rules"]
        self.assertIn("public_availability_is_not_a_license", rules)
        self.assertIn("ideas_vs_expression", rules)

    def test_the_srd_scope_caution_survives(self) -> None:
        """The CWN finding is CC0 for the SRD; the full book is not."""
        cwn = next(e for e in ledger()["sources"] if e["id"] == "cities-without-number-srd")
        self.assertEqual(cwn["decision"], "verified-public-domain")
        self.assertRegex(cwn["notes"], r"SCOPE MATTERS|not a finding that the full")

    def test_nothing_is_recorded_as_imported(self) -> None:
        imports = ledger()["current_imports"]
        self.assertTrue(imports["summary"].startswith("None."),
                        "the ledger claims something was imported")


class AuthorityTests(unittest.TestCase):
    """HERMES.md: a lock is preserved and the conflict is reported, not edited around."""

    def test_the_author_owned_conflict_is_recorded(self) -> None:
        conflict = ledger()["closed_system_claim_inventory"]["authority_conflict"]
        self.assertIn("AGENTS.md", conflict["why_it_blocks"])
        self.assertIn("author-approved process", conflict["why_it_blocks"])
        self.assertIn("PRESERVED UNCHANGED", conflict["agent_action"])

    def test_the_build_coupling_is_recorded(self) -> None:
        """AGENTS.md §13 + DESIGN_PRINCIPLES.md + the test move as a set, or not at all."""
        coupling = ledger()["closed_system_claim_inventory"]["authority_conflict"]["build_coupling"]
        for needle in ("AGENTS.md", "DESIGN_PRINCIPLES.md", "test_design_principles.py"):
            with self.subTest(file=needle):
                self.assertIn(needle, coupling)

    def test_the_conflict_matches_the_repository_state(self) -> None:
        """If an author update lands, the inventory must move with it -- not drift apart."""
        agents = AGENTS.read_text(encoding="utf-8")
        pole_claim = next(c for c in ledger()["closed_system_claim_inventory"]["live"]
                          if c["file"] == "AGENTS.md" and c["line"] == 263)
        self.assertIn("AUTHOR-OWNED", pole_claim["action"])
        if "CY_BORG" in agents and "Cyberpunk 2020" in agents:
            pass  # the locked poles are still in place: the inventory is accurate
        else:
            self.fail("AGENTS.md poles changed but the rights ledger still calls them "
                      "author-owned and untouched -- update the inventory with the change")

    def test_the_migration_order_exists_and_starts_with_the_audit(self) -> None:
        order = ledger()["migration_order"]
        self.assertIn("1_audit", order)
        self.assertIn("2_license_choice", order)
        self.assertIn("3_authority_update", order)


class InventoryTests(unittest.TestCase):
    def test_the_live_claim_sites_still_exist(self) -> None:
        """An audit that names deleted files is stale; reword, do not silently delete."""
        for claim in ledger()["closed_system_claim_inventory"]["live"]:
            with self.subTest(file=claim["file"]):
                self.assertTrue((ROOT / claim["file"]).is_file(),
                                f"{claim['file']} is listed in the audit but no longer exists")
                self.assertTrue(claim.get("action"))

    def test_the_audit_document_reports_the_same_inventory(self) -> None:
        doc = AUDIT_DOC.read_text(encoding="utf-8")
        self.assertIn("audit before deleting", doc.lower())
        self.assertIn("Nothing has been deleted", doc)
        # the load-bearing closed-system claim has to be named in both places
        self.assertIn("RPG_CONVERSION_REFERENCE.md", doc)
        self.assertIn("RPG_CONVERSION_REFERENCE.md",
                      json.dumps(ledger()["closed_system_claim_inventory"]["live"]))

    def test_the_doc_keeps_the_blocked_and_unverified_distinction(self) -> None:
        doc = AUDIT_DOC.read_text(encoding="utf-8")
        self.assertRegex(doc, r"blocked is (?:still )?not a finding")
        self.assertIn("no CC grant established", doc)


class CombinationTests(unittest.TestCase):
    """#200 was worked by three agents at once; the set must reconcile, not fork."""

    def setUp(self) -> None:
        self.d = ledger()
        self.doc = AUDIT_DOC.read_text(encoding="utf-8")

    def test_the_sibling_artifacts_are_recorded(self) -> None:
        sib = self.d["sibling_artifacts"]
        blob = json.dumps(sib)
        for pr in ("#203", "#205", "#204"):
            with self.subTest(pr=pr):
                self.assertIn(pr, blob)

    def test_it_records_what_was_adopted_and_what_was_offered(self) -> None:
        sib = self.d["sibling_artifacts"]
        self.assertTrue(sib["adopted_from_the_siblings"])
        self.assertTrue(sib["offered_to_the_siblings"])
        # the two corrections that came from the sibling pass, not from this one
        adopted = " ".join(sib["adopted_from_the_siblings"])
        self.assertIn("Veil", adopted)
        self.assertIn("Fudge", adopted)

    def test_the_overlap_is_recorded_as_a_trail_rather_than_erased(self) -> None:
        """Parallel ledgers must not be silently deleted by whichever agent lands last.

        The consolidation did happen later (#208), which is fine -- what matters is that the
        ledger records both that it was flagged and who resolved it, so the history is not
        rewritten to look like it was never a duplication.
        """
        sib = self.d["sibling_artifacts"]
        flagged = sib["overlap_flagged_before_consolidation"]
        self.assertIn("rules_engine_rights.json", flagged)
        self.assertIn("duplication", flagged)
        self.assertIn("#208", sib["overlap_resolved_by"])
        self.assertNotIn("both are left in place", json.dumps(sib),
                         "the stale 'both are left in place' claim survived the consolidation")

    def test_the_veil_verification_survives_with_its_caveat(self) -> None:
        veil = next(e for e in self.d["sources"] if e["id"] == "the-veil")
        self.assertEqual(veil["decision"], "verified-permissive")
        self.assertIn("BY-SA 3.0", veil["license"])
        # the AW-derived portions inside The Veil are NOT covered by The Veil's licence
        self.assertIn("does not transfer", veil["notes"])

    def test_the_author_owned_inconsistency_is_reported_not_fixed(self) -> None:
        inc = self.d["open_inconsistency"]
        blob = json.dumps(inc)
        for needle in ("DESIGN_PRINCIPLES.md", "AGENTS.md", "test_design_principles.py"):
            with self.subTest(needle=needle):
                self.assertIn(needle, blob)
        # it must read as REPORTED: either "reported, not fixed" or "instead of resolving"
        self.assertRegex(blob, r"REPORTED, not silently fixed|instead of resolving")
        # the heading says "author-owned", not "locked": this repo has no TOMI-LOCKED markers,
        # and its own plan notes warn against citing a lock that is not there.
        self.assertIn("An inconsistency in the author-owned set", self.doc)

    def test_the_remaining_inconsistency_matches_the_repository_state(self) -> None:
        """If the author reconciles AGENTS.md, this record must move with it -- not go stale."""
        inc = self.d["open_inconsistency"]
        agents = (ROOT / "AGENTS.md").read_text(encoding="utf-8")
        principles = (ROOT / "docs" / "archive" / "DESIGN_PRINCIPLES.md").read_text(encoding="utf-8")
        agents_old = "CY_BORG" in agents and "Cyberpunk 2020" in agents
        principles_new = "Apocalypse World" in principles
        if agents_old and principles_new:
            self.assertIn("what_remains", inc)
            self.assertIn("AGENTS.md", inc["what_remains"])
        else:
            self.fail("AGENTS.md and DESIGN_PRINCIPLES.md now agree, but the rights ledger "
                      "still records a standing contradiction -- update open_inconsistency")

    def test_the_ep_prototype_quarantine_is_in_the_migration_order(self) -> None:
        order = self.d["migration_order"]
        self.assertIn("4b_ep_prototype_quarantine", order)
        self.assertIn("eclipse_phase_homebrew", order["4b_ep_prototype_quarantine"])
        self.assertIn("ISSUE_200_CC_RELEASE_GATE.md", self.doc)


if __name__ == "__main__":
    unittest.main()
