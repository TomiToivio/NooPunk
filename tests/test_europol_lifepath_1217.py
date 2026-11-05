"""#1217: the Europol lifepath builder accepts legal characters and names every illegal one.

The fixtures are invented (a Background with two Learning skills, three Edges, three published Foci). They test the
*builder*, not CWN's catalogue: this repository does not carry a verified Edge list, so no test here claims a real
Edge name beyond the four the author approved in #1178.
"""

from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from rules.cwn_backgrounds import Background  # noqa: E402
from rules.cwn_character import ARRAY, ATTRIBUTES  # noqa: E402
from rules.cwn_edges_foci import Edge  # noqa: E402
from rules.europol_lifepath import (  # noqa: E402
    FIXED,
    PATHS,
    Lifepath,
    LifepathError,
    build_lifepath,
    legal_paths,
)
from rules.scene_tags import PersonalityTag  # noqa: E402

LAW = Background(
    id="Law Enforcement",
    free_skill="Investigate",
    learning=("Connect", "Shoot", "Drive"),
    growth=("Any Stat", "+1 Physical"),
)

#: An invented catalogue. Names are fixtures, not CWN claims — except Mutant and Focused, which the author named.
CATALOGUE = {
    "Mutant": Edge("Mutant", is_power=True),
    "Focused": Edge("Focused", grants_bonus_focus=True),
    "Alert": Edge("Alert"),
    "Ghost": Edge("Ghost"),
}

ARRAY_MAP = dict(zip(ATTRIBUTES, ARRAY, strict=True))
WEAK_MAP = dict(zip(ATTRIBUTES, (7, 7, 7, 7, 7, 7), strict=True))


def build(**overrides):
    kwargs = dict(
        path="grunt",
        attributes=ARRAY_MAP,
        background=LAW,
        edges=(CATALOGUE["Alert"], CATALOGUE["Ghost"]),
        foci=("Alert",),
        learning_picks=("Connect", "Shoot"),
        edge_catalogue=CATALOGUE,
    )
    kwargs.update(overrides)
    return build_lifepath(**kwargs)


class FixedFactTests(unittest.TestCase):
    def test_the_author_facts_are_quoted_with_their_source(self):
        for key in ("name", "origin", "academy", "employer", "posting", "supervisor", "background"):
            value, source = FIXED[key]
            self.assertTrue(value and source, key)
            self.assertIn("#1217", source)

    def test_the_posting_and_supervisor_are_the_authored_ones(self):
        self.assertIn("Ratakatu 12", FIXED["posting"][0])
        self.assertEqual(FIXED["supervisor"][0], "Dr Harri Romppainen")
        self.assertEqual(FIXED["employer"][0], "Europol")

    def test_no_route_grants_anything(self):
        for name, spec in PATHS.items():
            self.assertEqual(tuple(spec["grants"]), (), f"{name} must not invent a bonus")

    def test_only_the_freak_route_requires_an_edge(self):
        self.assertEqual(tuple(PATHS["freak"]["requires_edges"]), ("Mutant",))
        self.assertEqual(tuple(PATHS["grunt"]["requires_edges"]), ())
        self.assertEqual(tuple(PATHS["geek"]["requires_edges"]), ())


class LegalPathTests(unittest.TestCase):
    def test_a_plain_officer_builds(self):
        path = build()
        self.assertIsInstance(path, Lifepath)
        self.assertEqual(path.path, "grunt")
        self.assertEqual(set(path.edges), {"Alert", "Ghost"})
        self.assertEqual(path.skills.get("Investigate"), 0)
        self.assertEqual(path.background, "Law Enforcement")

    def test_the_result_is_deterministic(self):
        self.assertEqual(build().to_dict(), build().to_dict())

    def test_provenance_names_a_source_for_every_part(self):
        provenance = " ".join(build().provenance)
        for expected in ("cwn_character", "cwn_edges_foci", "cwn_backgrounds", "cwn_foci", "#1217"):
            self.assertIn(expected, provenance)

    def test_a_hybrid_may_take_the_freak_route_with_the_mutant_edge(self):
        path = build(
            path="freak",
            attributes=None,
            attribute_dice=(1,) * 18,
            edges=(CATALOGUE["Mutant"], CATALOGUE["Alert"], CATALOGUE["Ghost"]),
            foci=(),
        )
        self.assertEqual(path.path, "freak")
        self.assertTrue(path.underdog, "a modifier total of -3 should claim the bonus Edge")

    def test_personality_tags_travel_with_the_character(self):
        tag = PersonalityTag(owner_id="tony.german", trait="cautious", evidence="#1217 fixture")
        path = build(personality=(tag,))
        self.assertEqual(path.to_dict()["personality"][0]["trait"], "cautious")

    def test_legal_paths_follows_the_edges_taken(self):
        self.assertEqual(legal_paths(edges=("Alert",)), ("grunt", "geek"))
        self.assertIn("freak", legal_paths(edges=("Alert", "Mutant")))


class IllegalPathTests(unittest.TestCase):
    def assertViolation(self, field: str, **overrides):
        with self.assertRaises(LifepathError) as caught:
            build(**overrides)
        fields = {violation.field for violation in caught.exception.violations}
        self.assertIn(field, fields, str(caught.exception))

    def test_a_third_edge_without_the_underdog_rule_is_refused(self):
        self.assertViolation(
            "edges",
            edges=(CATALOGUE["Alert"], CATALOGUE["Ghost"], Edge("Extra")),
        )

    def test_the_freak_route_without_the_mutant_edge_is_refused(self):
        self.assertViolation("path", path="freak")

    def test_an_unknown_route_is_refused(self):
        self.assertViolation("path", path="wizard")

    def test_a_background_other_than_law_enforcement_is_refused(self):
        self.assertViolation("background", background=Background(
            id="Bum", free_skill="Survive", learning=("Connect",), growth=("Any Stat",)))

    def test_a_wrong_attribute_set_is_refused(self):
        self.assertViolation("attributes", attributes=dict(list(ARRAY_MAP.items())[:5]))

    def test_an_attribute_assignment_that_is_not_the_array_is_refused(self):
        self.assertViolation("attributes", attributes=dict(zip(ATTRIBUTES, (18, 18, 18, 18, 18, 18), strict=True)))

    def test_the_wrong_number_of_learning_picks_is_refused(self):
        self.assertViolation("skills", learning_picks=("Connect",))

    def test_a_learning_pick_outside_the_table_is_refused(self):
        self.assertViolation("skills", learning_picks=("Connect", "Pilot"))

    def test_an_edge_outside_the_supplied_catalogue_is_refused(self):
        self.assertViolation("edges", edges=(CATALOGUE["Alert"], Edge("Invented")))

    def test_a_focus_that_does_not_exist_is_refused(self):
        self.assertViolation("foci", foci=("Ninjitsu",))

    def test_two_foci_without_the_focused_edge_is_refused(self):
        self.assertViolation("foci", foci=("Alert", "Diplomat"))

    def test_the_focused_edge_buys_the_second_focus_slot(self):
        path = build(edges=(CATALOGUE["Focused"], CATALOGUE["Alert"]), foci=("Alert", "Diplomat"))
        self.assertEqual(sorted(path.focus_levels), ["Alert", "Diplomat"])

    def test_every_violation_is_reported_at_once(self):
        with self.assertRaises(LifepathError) as caught:
            build(path="freak", foci=("Ninjitsu",), learning_picks=("Connect",))
        self.assertGreaterEqual(len(caught.exception.violations), 3)
        self.assertEqual(
            {v.field for v in caught.exception.violations} >= {"path", "foci", "skills"}, True
        )

    def test_an_underdog_character_may_not_buy_a_power_edge_with_the_bonus(self):
        with self.assertRaises(LifepathError) as caught:
            build(
                path="freak",
                attributes=None,
                attribute_dice=(1,) * 18,
                edges=(CATALOGUE["Alert"], CATALOGUE["Ghost"], CATALOGUE["Mutant"]),
                foci=(),
            )
        self.assertIn("Underdog", str(caught.exception))


if __name__ == "__main__":
    unittest.main()
