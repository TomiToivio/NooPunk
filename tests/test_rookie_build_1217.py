"""The legal-build path must refuse what the two separate validators each refuse (#1217).

The point of the module is the case that `main` accepted before it existed:

    pick_edge(sheet, Edge("Mentalist", "Mentalist"))
    pick_edge(sheet, Edge("Spellcaster", "Spellcaster"))   # accepted, though psi_access forbids it

So the tests are mostly negative, and the first one reproduces that exact build.
"""

from __future__ import annotations

import unittest

from src.rules.cwn_edges_foci import Edge, Focus, TalentSheet, pick_edge
from src.rules.rookie_build import BuildError, RookieBuild, check_build


class TheRegressionTest(unittest.TestCase):
    def test_mentalist_plus_spellcaster_is_refused(self) -> None:
        """The build the CWN path accepts and the policy forbids."""
        build = RookieBuild("act.rookie")
        build.add_edge(Edge("Mentalist"))
        with self.assertRaises(BuildError):
            build.add_edge(Edge("Spellcaster"))
        self.assertEqual(len(build.sheet.edges), 1, "a refused Edge must not consume a slot")

    def test_the_old_path_still_accepts_it(self) -> None:
        """Documents why the bridge exists: CWN alone has no policy to consult."""
        sheet = TalentSheet()
        pick_edge(sheet, Edge("Mentalist"))
        pick_edge(sheet, Edge("Spellcaster"))
        self.assertEqual(sheet.edges, ["Mentalist", "Spellcaster"])


class BudgetTest(unittest.TestCase):
    def test_two_edges_at_start_and_the_third_is_refused(self) -> None:
        build = RookieBuild("act.rookie")
        build.add_edge(Edge("Mutant"))
        build.add_edge(Edge("Summoner"))
        with self.assertRaises(BuildError):
            build.add_edge(Edge("Spellcaster"))

    def test_a_third_edge_is_allowed_at_fifth_level(self) -> None:
        build = RookieBuild("act.rookie")
        build.sheet.level = 5
        build.add_edge(Edge("Mutant"))
        build.add_edge(Edge("Summoner"))
        build.add_edge(Edge("Spellcaster"))  # slots, not policy, is what is being tested
        self.assertEqual(len(build.sheet.edges), 3)

    def test_a_duplicate_non_repeatable_edge_is_refused(self) -> None:
        build = RookieBuild("act.rookie")
        build.add_edge(Edge("Mutant"))
        with self.assertRaises(BuildError):
            build.add_edge(Edge("Mutant"))

    def test_problems_reports_an_over_budget_sheet_loaded_from_a_save(self) -> None:
        """A build loaded from disk never went through add_edge, so validate() must still catch it."""
        build = RookieBuild("act.rookie")
        build.sheet.edges = ["Mutant", "Summoner", "Spellcaster"]
        problems = build.problems()
        self.assertTrue(any("only 2 slot" in problem for problem in problems), problems)


class PolicyTest(unittest.TestCase):
    def test_an_unknown_edge_is_refused(self) -> None:
        build = RookieBuild("act.rookie")
        with self.assertRaises(BuildError) as caught:
            build.add_edge(Edge("Warlord"))
        self.assertIn("not a known Edge", str(caught.exception))

    def test_mutant_without_europol_approval_is_refused(self) -> None:
        build = RookieBuild("act.rookie", europol_approved=False)
        with self.assertRaises(BuildError) as caught:
            build.add_edge(Edge("Mutant"))
        self.assertIn("Europol approval", str(caught.exception))

    def test_mutant_does_not_imply_hybrid_ancestry(self) -> None:
        """The AWN module owns this rule; the builder must not loosen it."""
        from src.rules.awn_mutant import MutantBuild, MutationError

        with self.assertRaises(MutationError):
            MutantBuild("act.rookie", True, "marked", alien_hybrid=True)

    def test_precognition_is_not_a_pc_discipline(self) -> None:
        build = RookieBuild("act.rookie")
        with self.assertRaises(BuildError) as caught:
            build.add_discipline("Precognition")
        self.assertIn("Precognition", str(caught.exception))

    def test_the_two_allowed_disciplines_are_accepted(self) -> None:
        build = RookieBuild("act.rookie")
        build.add_discipline("Telepathy")
        build.add_discipline("Telekinesis")
        self.assertEqual(build.disciplines, ["Telepathy", "Telekinesis"])

    def test_a_partial_psychic_may_not_hold_two_disciplines(self) -> None:
        build = RookieBuild("act.rookie", partial_psychic=True)
        build.disciplines = ["Telepathy", "Telekinesis"]
        self.assertTrue(any("Partial Psychic" in p for p in build.problems()))

    def test_mentalist_cannot_combine_with_a_psychic_discipline(self) -> None:
        build = RookieBuild("act.rookie")
        build.add_edge(Edge("Mentalist"))
        build.disciplines = ["Telepathy"]
        self.assertTrue(any("cannot combine" in p for p in build.problems()), build.problems())


class IdentityTest(unittest.TestCase):
    def test_two_builds_may_not_claim_one_actor(self) -> None:
        first = RookieBuild("act.rookie")
        second = RookieBuild("act.rookie")
        problems = check_build(second, other=[first])
        self.assertTrue(any("one actor has one sheet" in p for p in problems), problems)

    def test_a_build_needs_an_actor_id(self) -> None:
        with self.assertRaises(BuildError):
            RookieBuild("")

    def test_validate_returns_the_build_when_clean(self) -> None:
        build = RookieBuild("act.rookie")
        build.add_edge(Edge("Mutant"))
        self.assertIs(build.validate(), build)


class FocusTest(unittest.TestCase):
    def test_one_focus_at_start_and_the_cap_is_cwns(self) -> None:
        build = RookieBuild("act.rookie")
        self.assertEqual(build.add_focus(Focus("Alert", levels=1)), 1)
        # Raising the same Focus is allowed to its own cap; a third level is refused by pick_focus.
        self.assertEqual(build.add_focus(Focus("Alert", levels=2)), 2)
        with self.assertRaises(BuildError):
            build.add_focus(Focus("Alert", levels=2))


if __name__ == "__main__":
    unittest.main()
