"""#1261: the Astral Projection ladder's permission gate, and the no-duplicate-mechanism checks.

Two modules for one ladder landed in parallel: `astral_progression.py` (data-driven, the canonical gate per
`docs/DOCUMENT_REGISTER.md`) and an `astral_ranks.py` capability table. The table was folded into the canonical module
and deleted; this file tests what it added — the rank-3 permission rule — and the invariants that keep the superskill
from growing a second body, sheet or combat system.

The rank/technique/plane/duration gates are already covered by `test_astral_progression_1261.py`; they are not repeated
here.
"""

from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from rules import astral_body  # noqa: E402
from rules import astral_progression as ladder  # noqa: E402


def pattern(owner: str, *, mutable: bool = True, name: str = "p") -> "ladder.InformationPattern":
    return ladder.InformationPattern(name, owner, mutable=mutable)


class EditingPermissionTests(unittest.TestCase):
    def test_rank_two_cannot_edit_anything(self):
        self.assertFalse(ladder.may_edit(2, "tony.german", pattern("tony.german")))

    def test_rank_three_edits_its_own_mutable_information(self):
        self.assertTrue(ladder.may_edit(3, "tony.german", pattern("tony.german")))

    def test_an_immutable_pattern_is_never_editable(self):
        fixed = pattern("tony.german", mutable=False, name="bank-record")
        for rank in range(5):
            self.assertFalse(ladder.may_edit(rank, "tony.german", fixed), rank)

    def test_another_agents_pattern_needs_a_mandate(self):
        other = pattern("npc.witness", name="someone-elses-memory")
        self.assertFalse(ladder.may_edit(3, "tony.german", other))
        self.assertTrue(ladder.may_edit(3, "tony.german", other, mandate=True))

    def test_rank_four_plane_access_is_not_a_licence(self):
        other = pattern("npc.witness", name="identity")
        self.assertFalse(ladder.may_edit(4, "tony.german", other))

    def test_a_refused_edit_names_the_reason(self):
        with self.assertRaises(ladder.AstralProgressionError) as caught:
            ladder.require_edit(3, "tony.german", pattern("npc.other"))
        self.assertIn("another agent", str(caught.exception))
        with self.assertRaises(ladder.AstralProgressionError) as caught:
            ladder.require_edit(1, "tony.german", pattern("tony.german"))
        self.assertIn("cannot edit", str(caught.exception))
        with self.assertRaises(ladder.AstralProgressionError) as caught:
            ladder.require_edit(4, "tony.german", pattern("tony.german", mutable=False))
        self.assertIn("not editable", str(caught.exception))

    def test_a_pattern_needs_an_owner_and_an_id(self):
        with self.assertRaises(ladder.AstralProgressionError):
            ladder.InformationPattern("", "tony.german")


class NoDuplicateMechanismTests(unittest.TestCase):
    def test_the_adapter_is_a_view_over_the_one_ladder(self):
        """`astral_progression` must not own a second table; it must be the canonical module's view."""
        from rules import astral_ranks

        view = ladder.ranks()
        self.assertEqual(sorted(view), sorted(astral_ranks.RANKS))
        for rank, spec in astral_ranks.RANKS.items():
            self.assertEqual(view[rank].name, spec.name)
            self.assertEqual(view[rank].duration_cap_minutes, spec.provisional_max_minutes)

    def test_astral_damage_stays_gated(self):
        self.assertFalse(astral_body.ASTRAL_DAMAGE_BRIDGE_APPROVED)

    def test_a_projected_high_rank_still_cannot_act_physically(self):
        projection = astral_body.begin_projection(
            "tony.german", "loc.sornainen_home", astral_body.EntryTrigger.SLEEP,
        )
        self.assertFalse(projection.may_take_physical_action())

    def test_the_ladder_is_astral_domain_only(self):
        ladder.assert_astral_domain_only()

    def test_rote_and_ident_are_not_swn_techniques(self):
        from rules.psionics import load_catalogue

        catalogue = load_catalogue()
        for key in ("rote", "transmit_information", "learn_ident", "use_ident"):
            self.assertNotIn(key, catalogue)


if __name__ == "__main__":
    unittest.main()
