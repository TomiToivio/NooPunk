"""Issue #689 — the 2d6 bands and the closed move set.

Behaviour only: the band classifier, its exact distribution, and the move catalogue's
contracts. No assertions about the rulebook's prose (AGENTS.md: executable code only).

The calibration is pinned here rather than inherited: #691's measurement says one step is
worth +16.7 percentage points of success at DV 8, and that is exactly `6/36`.
"""
from __future__ import annotations

import json
import tempfile
import unittest
from fractions import Fraction
from pathlib import Path

from src.rules import narrative_layer as nl
from src.rules import narrative_moves as nm


class BandTests(unittest.TestCase):
    """The band is a reading of the margin, not a second roll."""

    def test_band_boundaries(self) -> None:
        cases = {-5: "miss", -1: "miss", 0: "cost", 1: "cost", 2: "clean", 4: "clean", 5: "style", 60: "style"}
        for margin, band in cases.items():
            with self.subTest(margin=margin):
                self.assertEqual(nl.band_for(margin), band)

    def test_outcome_band_reads_the_core_total(self) -> None:
        self.assertEqual(nl.outcome_band(7, 8), "miss")
        self.assertEqual(nl.outcome_band(8, 8), "cost")
        self.assertEqual(nl.outcome_band(10, 8), "clean")
        self.assertEqual(nl.outcome_band(13, 8), "style")

    def test_non_integer_margins_are_refused(self) -> None:
        for bad in ("3", 2.5, True, None):
            with self.subTest(bad=bad), self.assertRaises(nl.NarrativeError):
                nl.band_for(bad)  # type: ignore[arg-type]

    def test_every_band_has_a_gm_move_and_the_move_is_described(self) -> None:
        for band in nl.OUTCOME_BANDS:
            with self.subTest(band=band):
                self.assertIn(nl.gm_move(band=band), nl.GM_MOVES)
        with self.assertRaises(nl.NarrativeError):
            nl.gm_move(band="brutal")  # the retired d10 vocabulary must not resolve

    def test_distribution_is_exact_and_total(self) -> None:
        dist = nl.band_distribution()
        self.assertEqual(sum(dist.values()), 1)
        self.assertEqual(dist["miss"], Fraction(21, 36))
        self.assertEqual(dist["cost"], Fraction(9, 36))
        self.assertEqual(dist["clean"], Fraction(6, 36))
        self.assertEqual(dist["style"], 0)

    def test_one_step_is_six_out_of_thirty_six_at_the_standard_difficulty(self) -> None:
        """#691's headline, re-derived from the bands rather than quoted."""
        base = sum(nl.band_distribution().values()) - nl.band_distribution()["miss"]
        stepped = 1 - nl.band_distribution(modifier=1)["miss"]
        self.assertEqual(base, Fraction(15, 36))
        self.assertEqual(stepped, Fraction(21, 36))
        self.assertAlmostEqual(float(stepped - base) * 100, 16.67, places=2)

    def test_a_second_step_is_worth_a_difficulty_step(self) -> None:
        """+2 at DV 8 lands where +0 lands at DV 6: the reason the cap is one invoke."""
        self.assertEqual(
            sum(v for b, v in nl.band_distribution(modifier=2).items() if b != "miss"),
            sum(v for b, v in nl.band_distribution(difficulty=6).items() if b != "miss"),
        )


class MoveSetTests(unittest.TestCase):
    """The set is closed, its vocabulary is the baseline's, and resolution is total."""

    def test_the_set_is_closed_at_eight(self) -> None:
        self.assertEqual(len(nm.moves()), nm.CLOSED_SET_SIZE)
        self.assertEqual(
            nm.move_ids(),
            (
                "read_a_sitch",
                "read_a_person",
                "apply_pressure",
                "hold_steady",
                "cross_a_threshold",
                "set_up",
                "ground_yourself",
                "contact_the_noosphere",
            ),
        )

    def test_every_move_carries_every_band(self) -> None:
        for move_id, move in nm.moves().items():
            with self.subTest(move=move_id):
                self.assertEqual(set(move.outcomes), set(nl.OUTCOME_BANDS))
                self.assertTrue(move.trigger.strip())

    def test_every_move_is_rollable_as_a_check_or_a_save(self) -> None:
        for move_id, move in nm.moves().items():
            with self.subTest(move=move_id):
                self.assertIn(move.kind, nm.KINDS)
                if move.kind == "save":
                    self.assertIn(move.save, {"physical", "evasion", "mental"})
                    self.assertIsNone(move.skill)
                    self.assertIsNone(move.attribute)
                elif move.skill_policy == nm.ACTION_SKILL_POLICY:
                    self.assertIsNone(move.skill)
                    self.assertIsNone(move.attribute)
                else:
                    self.assertTrue(move.skill and move.attribute)

    def test_no_move_grants_a_modifier(self) -> None:
        """Grants may name questions, aspects or cancellations -- never a bonus."""
        allowed = {"questions", "aspects", "conditions_cancelled"}
        for move_id, move in nm.moves().items():
            with self.subTest(move=move_id):
                self.assertLessEqual(set(move.grants), allowed)

    def test_resolution_reads_the_margin(self) -> None:
        self.assertEqual(nm.resolve_move("read_a_sitch", total=7, difficulty=8).band, "miss")
        self.assertEqual(nm.resolve_move("read_a_sitch", total=8, difficulty=8).band, "cost")
        self.assertEqual(nm.resolve_move("read_a_sitch", total=11, difficulty=8).band, "clean")
        self.assertEqual(nm.resolve_move("read_a_sitch", total=13, difficulty=8).band, "style")

    def test_grants_are_banded_and_absent_otherwise(self) -> None:
        self.assertEqual(nm.resolve_move("read_a_sitch", total=8, difficulty=8).grants, {"questions": 1})
        self.assertEqual(nm.resolve_move("read_a_sitch", total=10, difficulty=8).grants, {"questions": 3})
        self.assertEqual(nm.resolve_move("read_a_sitch", total=6, difficulty=8).grants, {})
        self.assertEqual(nm.resolve_move("hold_steady", total=6, difficulty=8).grants, {})

    def test_resolution_is_deterministic(self) -> None:
        first = nm.resolve_move("apply_pressure", total=11, difficulty=9)
        second = nm.resolve_move("apply_pressure", total=11, difficulty=9)
        self.assertEqual(first, second)

    def test_an_unknown_move_is_refused(self) -> None:
        with self.assertRaises(nl.NarrativeError):
            nm.resolve_move("invent_a_move", total=10, difficulty=8)


class MoveCatalogueContractTests(unittest.TestCase):
    """A malformed catalogue must fail loudly, not resolve as `miss` forever."""

    def load(self, payload: dict) -> dict:
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "moves.json"
            path.write_text(json.dumps(payload), encoding="utf-8")
            return nm.moves(path)

    def catalogue(self) -> dict:
        return json.loads(nm.MOVES_PATH.read_text(encoding="utf-8"))

    def test_the_shipped_catalogue_loads(self) -> None:
        self.assertEqual(len(self.load(self.catalogue())), nm.CLOSED_SET_SIZE)

    def test_a_ninth_move_is_refused_until_the_constant_changes(self) -> None:
        payload = self.catalogue()
        payload["moves"].append(dict(payload["moves"][0], id="a_ninth_move"))
        with self.assertRaises(nl.NarrativeError):
            self.load(payload)

    def test_a_duplicate_id_is_refused(self) -> None:
        payload = self.catalogue()
        payload["moves"][1]["id"] = payload["moves"][0]["id"]
        with self.assertRaises(nl.NarrativeError):
            self.load(payload)

    def test_an_unknown_skill_is_refused(self) -> None:
        payload = self.catalogue()
        payload["moves"][0]["skill"] = "Guns"  # retired label, not a baseline skill
        with self.assertRaises(nl.NarrativeError):
            self.load(payload)

    def test_an_unknown_save_is_refused(self) -> None:
        payload = self.catalogue()
        payload["moves"][3]["save"] = "sanity"
        with self.assertRaises(nl.NarrativeError):
            self.load(payload)

    def test_a_missing_band_is_refused(self) -> None:
        payload = self.catalogue()
        del payload["moves"][0]["outcomes"]["style"]
        with self.assertRaises(nl.NarrativeError):
            self.load(payload)

    def test_a_grant_on_an_unknown_band_is_refused(self) -> None:
        payload = self.catalogue()
        payload["moves"][0]["grants"]["questions"]["critical"] = 4
        with self.assertRaises(nl.NarrativeError):
            self.load(payload)

    def test_a_non_positive_grant_is_refused(self) -> None:
        payload = self.catalogue()
        payload["moves"][0]["grants"]["questions"]["clean"] = 0
        with self.assertRaises(nl.NarrativeError):
            self.load(payload)


if __name__ == "__main__":
    unittest.main()
