"""Executable contracts for the faction-creation vocabulary (issue #346).

Code-only, per `AGENTS.md` and issue #271. These exercise the **vocabulary and the validator**: the
named position set, the tag kinds and scopes, referential integrity of the shipped template, the
player/GM fog-of-war split, and — the one that matters politically — the fact that NHI contact policy
and per-polity diplomacy are independent, so a pro-contact faction can hold a hostile relation toward a
named polity without the model complaining.

They do not assert what any faction says, and no test here computes affinity, tension or balance.

Run from the repository root:

    python -m unittest discover -s strategy_game/tests -p "test_*.py"
"""
from __future__ import annotations

import copy
import json
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:  # pragma: no cover - import bootstrap, mirrors the sibling test modules
    sys.path.insert(0, str(ROOT))

from strategy_game.faction_creation import (  # noqa: E402
    CREATION_FORMAT,
    DIPLOMATIC_STATES,
    POSITIONS,
    TAG_KINDS,
    TAG_SCOPES,
    creation_from_dict,
    draft_from_dict,
    load_faction_creation,
)

_FIXTURE = {
    "format": CREATION_FORMAT,
    "position_vocabulary": {
        "positions": [
            {"id": "strong_low_pole", "rank": -2},
            {"id": "moderate_low_pole", "rank": -1},
            {"id": "neutral", "rank": 0},
            {"id": "moderate_high_pole", "rank": 1},
            {"id": "strong_high_pole", "rank": 2},
        ]
    },
    "axes": [
        {"id": "economic", "low_pole": "commons", "high_pole": "markets"},
        {"id": "social", "low_pole": "liberal", "high_pole": "conservative"},
        {"id": "agi", "low_pole": "restriction", "high_pole": "acceleration"},
        {"id": "nhi", "low_pole": "isolation", "high_pole": "integration"},
        {"id": "psi", "low_pole": "materialism", "high_pole": "panpsychism"},
    ],
    "tag_families": [
        {"id": "doctrine", "kind": "belief", "tags": [
            {"id": "MATERIALIST", "label": "materialist"},
            {"id": "QIP_PANPSYCHIST", "label": "panpsychist"},
        ]},
        {"id": "ability", "kind": "competence", "tags": [
            {"id": "REMOTE_VIEWER", "label": "remote viewer"},
            {"id": "TELEPATH", "label": "telepath"},
        ]},
        {"id": "assets", "kind": "asset", "tags": [
            {"id": "REMOTE_VIEWING_TEAM", "applies_to": ["faction", "organization"]},
        ]},
        {"id": "goals", "kind": "goal", "tags": [{"id": "BUILD_EFTZ"}]},
    ],
    "nhi_polities": [{"id": "uccc"}, {"id": "orion_sphere"}],
    "diplomatic_states": [{"id": s} for s in DIPLOMATIC_STATES],
    "template": {"id": "template_faction", "positions": {"nhi": "strong_high_pole"},
                 "tags": ["MATERIALIST", "BUILD_EFTZ"]},
    "comparative_examples": [{"id": "example", "tags": ["TELEPATH"]}],
    "cross_axis_examples": [{"id": "a"}, {"id": "b"}, {"id": "c"}],
}


def _fixture():
    return creation_from_dict(copy.deepcopy(_FIXTURE))


class VocabularyTests(unittest.TestCase):
    def test_the_five_axes_answer_both_poles(self):
        model = _fixture()
        self.assertEqual(set(model.axes), {"economic", "social", "agi", "nhi", "psi"})
        for axis in model.axes.values():
            with self.subTest(axis=axis.identifier):
                self.assertTrue(axis.low_pole and axis.high_pole)

    def test_positions_are_the_declared_named_set_and_strictly_ordered(self):
        model = _fixture()
        self.assertEqual(set(model.positions), set(POSITIONS))
        ranks = [model.positions[p].rank for p in model.position_order]
        self.assertEqual(ranks, sorted(ranks))
        self.assertEqual(len(set(ranks)), len(ranks))

    def test_every_tag_declares_a_kind_and_a_family(self):
        model = _fixture()
        for tag in model.tags.values():
            with self.subTest(tag=tag.identifier):
                self.assertIn(tag.kind, TAG_KINDS)
                self.assertIn(tag.family, model.families)

    def test_no_numeric_scale_is_approved(self):
        """The issue allows named positions first, an ordered scale only after playtesting."""
        model = load_faction_creation()
        self.assertIs(model.numeric_scale_approved, False)


class MalformedRootTests(unittest.TestCase):
    """A JSON array, null or scalar is refused as the wrong document, not as an AttributeError."""

    def test_a_non_object_root_is_refused_cleanly(self) -> None:
        import json
        import tempfile

        for raw in ([], None, "a roster", 42):
            with self.subTest(root=raw), tempfile.TemporaryDirectory() as tmp:
                path = Path(tmp) / "faction_creation.json"
                path.write_text(json.dumps(raw), encoding="utf-8")
                with self.assertRaisesRegex(ValueError, "must contain a JSON object"):
                    load_faction_creation(path)


class TagKindTests(unittest.TestCase):
    """Issue #346: distinguish belief, competence, equipment, relationship, asset and goal."""

    def test_a_doctrine_is_not_a_capability(self):
        model = _fixture()
        self.assertEqual(model.tag("MATERIALIST").kind, "belief")
        self.assertEqual(model.tag("REMOTE_VIEWER").kind, "competence")
        self.assertNotIn("REMOTE_VIEWER", [t.identifier for t in model.tags_for(kind="belief")])
        self.assertNotIn("MATERIALIST", [t.identifier for t in model.tags_for(kind="competence")])

    def test_one_definition_serves_different_scopes(self):
        """A remote-viewing team is a faction asset; a remote viewer is a character's capability."""
        model = _fixture()
        self.assertTrue(model.validate_tag_scope("REMOTE_VIEWING_TEAM", "faction"))
        self.assertFalse(model.validate_tag_scope("REMOTE_VIEWING_TEAM", "character"))
        self.assertTrue(model.validate_tag_scope("REMOTE_VIEWER", "character"))
        self.assertNotIn("REMOTE_VIEWING_TEAM", [t.identifier for t in model.tags_for(scope="character")])

    def test_a_scope_that_is_not_declared_anywhere_is_reported(self):
        model = creation_from_dict(
            {
                "format": CREATION_FORMAT,
                "tag_families": [{"id": "f", "kind": "belief",
                                  "tags": [{"id": "ODD", "applies_to": ["spaceship"]}]}],
            }
        )
        self.assertIn(("ODD", "applies_to", "spaceship"), model.off_vocabulary())
        self.assertEqual([s for s in TAG_SCOPES if s == "spaceship"], [])


class SeparationOfPolicyAndDiplomacyTests(unittest.TestCase):
    """Issue #346: 'avoid forcing pro-NHI to equal pro-Confederacy or pro-Orion'."""

    def test_a_pro_contact_faction_may_be_hostile_to_named_polities(self):
        model = _fixture()
        draft = draft_from_dict(
            {
                "id": "pro_contact_but_hostile",
                "positions": {"nhi": "strong_high_pole"},
                "nhi_relations": {"uccc": "hostility", "orion_sphere": "hostility"},
            }
        )
        self.assertEqual(model.validate_draft(draft), ())

    def test_an_isolationist_may_still_trade_with_one_polity(self):
        model = _fixture()
        draft = draft_from_dict(
            {
                "id": "isolationist_but_trading",
                "positions": {"nhi": "strong_low_pole"},
                "nhi_relations": {"orion_sphere": "trading"},
            }
        )
        self.assertEqual(model.validate_draft(draft), ())

    def test_replacing_the_policy_position_does_not_touch_the_relations(self):
        model = _fixture()
        first = draft_from_dict({"id": "d", "positions": {"nhi": "strong_low_pole"},
                                 "nhi_relations": {"uccc": "alliance"}})
        second = draft_from_dict({"id": "d", "positions": {"nhi": "strong_high_pole"},
                                  "nhi_relations": {"uccc": "alliance"}})
        self.assertEqual(first.relations, second.relations)

    def test_the_shipped_document_records_the_separation_rule(self):
        model = load_faction_creation()
        self.assertEqual(model.separation_rule.get("policy_field"), "nhi")
        self.assertEqual(model.separation_rule.get("relations_field"), "nhi_relations")


class ValidationTests(unittest.TestCase):
    def test_an_unknown_axis_position_tag_polity_or_state_is_reported_by_name(self):
        model = _fixture()
        draft = draft_from_dict(
            {
                "id": "bad",
                "positions": {"no_such_axis": "neutral", "nhi": "halfway"},
                "tags": ["NO_SUCH_TAG"],
                "nhi_relations": {"no_such_polity": "trading", "uccc": "no_such_state"},
            }
        )
        problems = " | ".join(model.validate_draft(draft))
        for fragment in ("no_such_axis", "halfway", "NO_SUCH_TAG", "no_such_polity", "no_such_state"):
            self.assertIn(fragment, problems)

    def test_a_numeric_position_is_refused_and_says_why(self):
        model = _fixture()
        draft = draft_from_dict({"id": "numeric", "positions": {"nhi": 0.5}})
        problems = " | ".join(model.validate_draft(draft))
        self.assertIn("0.5", problems)
        self.assertIn("scale is not approved", problems)

    def test_a_well_formed_draft_has_no_problems(self):
        model = _fixture()
        draft = draft_from_dict(
            {
                "id": "fine",
                "positions": {"economic": "strong_low_pole", "psi": "moderate_high_pole"},
                "tags": ["MATERIALIST", "BUILD_EFTZ"],
                "nhi_relations": {"uccc": "contact"},
            }
        )
        self.assertEqual(model.validate_draft(draft), ())

    def test_a_draft_without_an_id_is_refused(self):
        with self.assertRaises(ValueError):
            draft_from_dict({"label": "nameless"})

    def test_a_duplicate_tag_id_is_refused(self):
        with self.assertRaises(ValueError):
            creation_from_dict(
                {
                    "format": CREATION_FORMAT,
                    "tag_families": [
                        {"id": "a", "tags": [{"id": "SAME"}]},
                        {"id": "b", "tags": [{"id": "SAME"}]},
                    ],
                }
            )


class FogOfWarTests(unittest.TestCase):
    """Issue #346: tags and axes must not reveal classified canon on the starting UI."""

    def test_the_hidden_agenda_never_reaches_the_player_view(self):
        model = _fixture()
        draft = draft_from_dict(
            {
                "id": "secretive",
                "positions": {"nhi": "moderate_high_pole"},
                "hidden_agenda": "serve the Orion bloc while preaching sovereignty",
                "nhi_relations": {"uccc": "contact", "orion_sphere": "trading"},
                "revealed_polities": ["uccc"],
            }
        )
        gm = draft.to_dict()
        player = model.player_view(draft)
        self.assertIn("hidden_agenda", gm)
        self.assertNotIn("hidden_agenda", player)
        self.assertNotIn("serve the Orion bloc", json.dumps(player))

    def test_an_unrevealed_polity_is_absent_from_the_player_view(self):
        model = _fixture()
        draft = draft_from_dict(
            {
                "id": "foggy",
                "nhi_relations": {"uccc": "contact", "orion_sphere": "trading"},
                "revealed_polities": ["uccc"],
            }
        )
        player = model.player_view(draft)
        self.assertEqual(set(player["nhi_relations"]), {"uccc"})
        self.assertEqual(set(draft.to_dict()["nhi_relations"]), {"uccc", "orion_sphere"})

    def test_the_shipped_fog_rule_names_what_is_withheld(self):
        model = load_faction_creation()
        withheld = set(model.fog_of_war.get("withheld_from_player") or [])
        self.assertIn("hidden_agenda", withheld)


class ShippedDocumentTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.model = load_faction_creation()

    def test_the_document_declares_its_format(self):
        from strategy_game.faction_creation import DATA_PATH

        self.assertTrue(DATA_PATH.is_file(), f"missing packaged vocabulary: {DATA_PATH}")
        with open(DATA_PATH, encoding="utf-8") as handle:
            self.assertEqual(json.load(handle)["format"], CREATION_FORMAT)

    def test_every_record_uses_the_declared_vocabularies(self):
        self.assertEqual(self.model.off_vocabulary(), ())

    def test_every_tag_the_template_and_examples_reference_exists(self):
        """Referential integrity: a card naming a tag the vocabulary does not define is a defect."""
        self.assertEqual(self.model.dangling_tag_references(), ())
        self.assertTrue(self.model.referenced_tags())

    def test_the_template_is_editable_rather_than_a_frozen_stat_block(self):
        note = str(self.model.template.get("note") or "")
        self.assertIn("PROPOSED", note)

    def test_the_issue_asks_for_two_or_three_cross_axis_contradictions_and_they_are_present(self):
        self.assertGreaterEqual(len(self.model.cross_axis_examples), 2)

    def test_a_player_view_of_every_example_carries_no_hidden_field(self):
        for example in (*self.model.comparative_examples, self.model.template):
            with self.subTest(example=example.get("id")):
                self.assertNotIn("hidden_agenda", json.dumps(self.model.player_view(draft_from_dict(
                    {"id": str(example.get("id")), "hidden_agenda": "x", "positions": example.get("positions") or {}}
                ))))

    def test_validating_and_viewing_do_not_mutate_the_model(self):
        draft = draft_from_dict({"id": "d", "positions": {"nhi": "neutral"},
                                 "nhi_relations": {"uccc": "contact"}})
        before = json.dumps({k: v.to_dict() for k, v in self.model.tags.items()}, sort_keys=True)
        self.model.validate_draft(draft)
        self.model.player_view(draft)
        after = json.dumps({k: v.to_dict() for k, v in self.model.tags.items()}, sort_keys=True)
        self.assertEqual(before, after)


class ScopeDirectiveTests(unittest.TestCase):
    """The crossover is inspired by LaclauGPT and must never import it (issues #282/#299)."""

    def test_importing_the_module_couples_to_no_laclaugpt_package(self):
        code = (
            "import sys, strategy_game, strategy_game.faction_creation as f;"
            "m = f.load_faction_creation();"
            "m.validate_draft(f.draft_from_dict({'id':'x','positions':{'nhi':'neutral'}}));"
            "m.player_view(f.draft_from_dict({'id':'x'}));"
            "print(sorted(x for x in sys.modules if x == 'laclaugpt' or x.startswith('laclaugpt.')))"
        )
        result = subprocess.run(
            [sys.executable, "-c", code], cwd=ROOT, capture_output=True, text=True, check=False
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stdout.strip(), "[]", f"loading the module pulled in LaclauGPT: {result.stdout}")

    def test_the_module_source_imports_no_laclaugpt(self):
        text = (ROOT / "strategy_game" / "faction_creation.py").read_text(encoding="utf-8")
        self.assertNotIn("import laclaugpt", text)
        self.assertNotIn("from laclaugpt", text)


class FirstTurnContainerTests(unittest.TestCase):
    """Issue #346 criterion 7: the container that names the slots and holds no value."""

    @classmethod
    def setUpClass(cls):
        cls.model = load_faction_creation()

    def test_the_shipped_container_is_well_formed_and_declares_no_value(self):
        self.assertTrue(self.model.first_turn)
        self.assertEqual(self.model.first_turn_problems(), ())
        self.assertIs(self.model.first_turn["values_declared"], False)
        self.assertTrue(self.model.first_turn["reason"])

    def test_the_container_names_the_issues_own_candidate_fields(self):
        fields = self.model.first_turn_fields()
        self.assertTrue(fields)
        for field in fields:
            with self.subTest(field=field.get("id")):
                self.assertTrue(field.get("id"))
                self.assertTrue(field.get("label"))

    def test_the_container_still_leaves_the_tag_and_axis_vocabularies_intact(self):
        self.assertEqual(self.model.off_vocabulary(), ())
        self.assertEqual(self.model.dangling_tag_references(), ())
        self.assertIs(self.model.numeric_scale_approved, False)

    def test_a_field_that_carries_a_value_is_refused_by_name(self):
        model = load_faction_creation()
        model.first_turn["candidate_sheet_fields"][0]["value"] = 5
        problems = " | ".join(model.first_turn_problems())
        self.assertIn("holds no value", problems)

    def test_a_named_field_that_carries_a_number_is_refused(self):
        model = load_faction_creation()
        model.first_turn["candidate_sheet_fields"][0]["label"] = 3
        self.assertIn(
            "is the number",
            " | ".join(model.first_turn_problems()),
        )

    def test_a_field_with_no_identifier_or_a_repeated_one_is_refused(self):
        model = load_faction_creation()
        model.first_turn["candidate_sheet_fields"] = [{"id": ""}, {"id": "funding"}, {"id": "funding"}]
        problems = " | ".join(model.first_turn_problems())
        self.assertIn("has no identifier", problems)
        self.assertIn("appears more than once", problems)

    def test_a_container_that_does_not_say_whether_values_are_declared_is_refused(self):
        model = load_faction_creation()
        del model.first_turn["values_declared"]
        self.assertIn(
            "does not state values_declared",
            " | ".join(model.first_turn_problems()),
        )

    def test_an_empty_field_is_only_honest_with_the_reason_it_is_empty(self):
        model = load_faction_creation()
        model.first_turn["reason"] = ""
        self.assertIn("gives no reason", " | ".join(model.first_turn_problems()))

    def test_a_document_without_the_container_says_so_rather_than_inventing_one(self):
        self.assertIn(
            "no first-turn container is declared",
            " | ".join(_fixture().first_turn_problems()),
        )


class PendingDecisionTests(unittest.TestCase):
    """The two criteria #346 cannot close: the reason each stays open is recorded, not restated twice."""

    @classmethod
    def setUpClass(cls):
        cls.model = load_faction_creation()

    def test_every_pending_decision_carries_the_reason_it_is_open(self):
        self.assertTrue(self.model.pending_decisions())
        self.assertEqual(self.model.unreasoned_decisions(), ())
        for item in self.model.pending_decisions():
            with self.subTest(decision=item.get("id")):
                self.assertTrue(item.get("container_instead"))

    def test_the_first_resource_question_is_recorded_as_an_economy_the_author_owns(self):
        ids = {item["id"] for item in self.model.pending_decisions()}
        self.assertIn("first_turn_resource_constraints", ids)

    def test_the_resolution_question_is_pointed_at_rather_than_recorded_twice(self):
        """One seam, one record: the resolution ruling lives in data/council.json and is cited here."""
        from strategy_game.council import load_council

        council_ids = {item["id"] for item in load_council().pending_decisions()}
        self.assertIn("mission_resolution", council_ids)
        entry = next(
            item for item in self.model.pending_decisions()
            if item["id"] == "abstract_mission_resolution"
        )
        self.assertIn("council.json", entry["why_not_decided"])


if __name__ == "__main__":
    unittest.main()
