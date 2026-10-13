"""Executable contracts for the paradigm and genre vocabulary (issue #359).

Code-only, per `AGENTS.md` and issue #271. These exercise the **reader and the three rules of the
record**: the three technology domains stay distinct and interacting, no genre spawns a game system,
and a real research tradition is never recorded as an achieved capability. They do not assert the
setting's prose.

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

from strategy_game.genre_paradigms import (  # noqa: E402
    CAPABILITY_STATUSES,
    CANDIDATE_KINDS,
    DOMAIN_IDS,
    GENRE_FORMAT,
    GENRE_IDS,
    INSPIRATION_KINDS,
    LENS_STATUSES,
    PRIOR_USE_CLAIMS,
    PROMOTION_STATUSES,
    RESEARCH_KINDS,
    genre_paradigms_from_dict,
    load_genre_paradigms,
)

_FIXTURE = {
    "format": GENRE_FORMAT,
    "technologies": [
        {"id": d, "domain": d, "interacts_with": [o for o in DOMAIN_IDS if o != d], "paradigm_shift": True}
        for d in DOMAIN_IDS
    ],
    "system_distinction": {"domains_interact": True, "domains_mutually_exclusive": False},
    "framing": {"rule": "genres overlap without spawning separate game systems"},
    "genres": [
        {"id": "biopunk", "established_genre_canon": True, "spawns_system": False, "centres_on": ["bionics"]},
        {"id": "solarpunk", "established_genre_canon": True, "spawns_system": False},
        {"id": "nanopunk", "established_genre_canon": True, "spawns_system": False},
        {"id": "psipunk", "established_genre_canon": True, "spawns_system": False, "centres_on": ["psychotronics"]},
        {"id": "ufopunk", "established_genre_canon": False, "spawns_system": False},
        {"id": "xenopunk", "established_genre_canon": False, "spawns_system": False},
    ],
    "inspirations": [
        {"id": "a_book", "kind": "fiction", "capability_status": "not_applicable", "genres": ["biopunk"], "contributes": "a story"},
        {"id": "a_researcher", "kind": "real_research", "capability_status": "early_research", "genres": ["biopunk"], "contributes": "lab work"},
        {"id": "a_tradition", "kind": "research_tradition", "capability_status": "research_tradition", "genres": ["psipunk"], "contributes": "contested experiments"},
    ],
    "genre_lenses": [
        {"id": "hopepunk", "status": "established_literary_movement", "adds": "solidarity"},
        {"id": "robopunk", "status": "internal_descriptor", "adds": "robot labour politics"},
    ],
    "candidate_paradigms": [
        {"id": "quantum", "kind": "technology", "promotion": "pending_author_decision",
         "promotion_test": "the issue's design test", "attaches_to": ["cybernetics"],
         "event_cards": ["a_card"]},
    ],
    "faction_pressure_axes": [
        {"id": "biotech_alignment", "poles": ["pro-biotech", "anti-biotech"],
         "recorded_as": "pending_author_decision"},
    ],
    "strategic_projects": [
        {"id": "living_seawalls", "genres": ["biopunk"], "status": "author_supplied_title", "effects": []},
    ],
    "event_card_ideas": [
        {"id": "a_card", "genres": ["psipunk"], "status": "author_supplied_title", "effects": []},
    ],
    "prior_uses": {
        "reading": "no widely established genre canon for the name was found",
        "entries": [{"id": "a_tag", "genre": "ufopunk", "claim": "scattered_use"}],
    },
    "related_issues": [{"issue": 345, "relation": "owns the PSI track"}],
}


def _fixture():
    return genre_paradigms_from_dict(copy.deepcopy(_FIXTURE))


class ShippedDocumentTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.model = load_genre_paradigms()

    def test_the_document_declares_its_format(self):
        from strategy_game.genre_paradigms import DATA_PATH

        self.assertTrue(DATA_PATH.is_file(), f"missing packaged vocabulary: {DATA_PATH}")
        with open(DATA_PATH, encoding="utf-8") as handle:
            self.assertEqual(json.load(handle)["format"], GENRE_FORMAT)

    def test_every_record_uses_the_declared_vocabularies(self):
        self.assertEqual(self.model.off_vocabulary(), ())

    def test_the_three_technology_domains_are_present(self):
        self.assertEqual(set(self.model.technologies), set(DOMAIN_IDS))

    def test_every_domain_declares_what_it_interacts_with(self):
        for technology in self.model.technologies.values():
            with self.subTest(domain=technology.identifier):
                self.assertTrue(technology.interacts_with)
                self.assertNotIn(technology.identifier, technology.interacts_with)

    def test_every_genre_centres_on_real_domains_only(self):
        for genre in self.model.genres.values():
            for domain_id in genre.centres_on:
                with self.subTest(genre=genre.identifier, domain=domain_id):
                    self.assertIn(domain_id, DOMAIN_IDS)


class DomainSeparationTests(unittest.TestCase):
    """Issue #359: interacting, not mutually exclusive; the correspondence is an abstraction."""

    def test_the_domains_are_not_recorded_as_exclusive(self):
        self.assertFalse(load_genre_paradigms().domains_are_exclusive())

    def test_a_record_claiming_exclusivity_is_reported(self):
        data = copy.deepcopy(_FIXTURE)
        data["system_distinction"]["domains_mutually_exclusive"] = True
        self.assertTrue(genre_paradigms_from_dict(data).domains_are_exclusive())

    def test_a_domain_that_interacts_with_nothing_is_reported(self):
        data = copy.deepcopy(_FIXTURE)
        data["technologies"][0]["interacts_with"] = []
        self.assertTrue(genre_paradigms_from_dict(data).domains_are_exclusive())

    def test_the_fixture_keeps_the_three_domains_symmetric(self):
        model = _fixture()
        for domain_id in DOMAIN_IDS:
            with self.subTest(domain=domain_id):
                others = set(DOMAIN_IDS) - {domain_id}
                self.assertEqual(set(model.technology(domain_id).interacts_with), others)


class GenreRuleTests(unittest.TestCase):
    """Issue #359: genres overlap without spawning separate game systems."""

    def test_no_shipped_genre_spawns_a_system(self):
        model = load_genre_paradigms()
        self.assertEqual(model.systems_spawned_by_genres(), ())
        self.assertEqual(set(model.genres), set(GENRE_IDS))

    def test_a_genre_that_spawns_a_system_is_reported(self):
        data = copy.deepcopy(_FIXTURE)
        data["genres"][0]["spawns_system"] = True
        self.assertEqual(genre_paradigms_from_dict(data).systems_spawned_by_genres(), ("biopunk",))

    def test_no_genre_is_a_paradigm_shift(self):
        """PSIpunk is an explicit genre and NOT a new paradigm shift: PSI already is a paradigm."""
        model = load_genre_paradigms()
        self.assertEqual(model.genre_paradigm_shifts(), ())
        self.assertFalse(model.genre("psipunk").is_paradigm_shift)
        self.assertIn("psychotronics", model.technologies)

    def test_bionics_is_a_paradigm_shift_among_three_domains(self):
        model = load_genre_paradigms()
        self.assertIn("bionics", model.paradigm_shifts())
        self.assertEqual(len(model.paradigm_shifts()), len(DOMAIN_IDS))

    def test_the_two_internal_definitions_do_not_claim_established_canon(self):
        model = load_genre_paradigms()
        for genre_id in ("ufopunk", "xenopunk"):
            with self.subTest(genre=genre_id):
                self.assertFalse(model.genre(genre_id).established_genre_canon)
                self.assertIn("canon", model.genre(genre_id).note.lower())

    def test_the_four_established_genres_do_claim_it(self):
        model = load_genre_paradigms()
        for genre_id in ("biopunk", "solarpunk", "nanopunk", "psipunk"):
            with self.subTest(genre=genre_id):
                self.assertTrue(model.genre(genre_id).established_genre_canon)


class EpistemicRuleTests(unittest.TestCase):
    """Issue #359: a research tradition is never recorded as an achieved capability."""

    def test_no_shipped_research_entry_lacks_a_capability_status(self):
        self.assertEqual(load_genre_paradigms().unearned_capability_claims(), ())

    def test_a_research_entry_without_a_status_is_reported(self):
        data = copy.deepcopy(_FIXTURE)
        data["inspirations"][1]["capability_status"] = ""
        self.assertEqual(genre_paradigms_from_dict(data).unearned_capability_claims(), ("a_researcher",))

    def test_no_research_entry_is_marked_not_applicable(self):
        """``not_applicable`` belongs to fiction; on a research record it would read as a capability."""
        model = load_genre_paradigms()
        for item in model.order():
            if item.is_research:
                with self.subTest(inspiration=item.identifier):
                    self.assertNotEqual(item.capability_status, "not_applicable")
                    self.assertIn(item.capability_status, CAPABILITY_STATUSES)

    def test_fiction_is_exempt_from_the_rule(self):
        model = _fixture()
        fiction = model.inspiration("a_book")
        self.assertFalse(fiction.is_research)
        self.assertNotIn(fiction.identifier, model.unearned_capability_claims())

    def test_the_research_traditions_are_present_and_typed(self):
        model = load_genre_paradigms()
        traditions = {item.identifier for item in model.inspirations_for_kind("research_tradition")}
        self.assertIn("j_b_rhine", traditions)
        self.assertIn("rupert_sheldrake", traditions)
        self.assertIn("ganzfeld_protocols", traditions)
        self.assertNotIn("the_demolished_man", traditions)

    def test_every_kind_used_is_declared(self):
        model = load_genre_paradigms()
        for item in model.order():
            self.assertIn(item.kind, INSPIRATION_KINDS)
        self.assertTrue(RESEARCH_KINDS)

    def test_the_shipped_record_states_the_rule(self):
        model = load_genre_paradigms()
        self.assertIn("achieved", json.dumps(model.epistemic_rule).lower())


class ShapeTests(unittest.TestCase):
    def test_every_inspiration_has_a_genre_a_kind_and_a_contribution(self):
        model = _fixture()
        for item in model.order():
            with self.subTest(inspiration=item.identifier):
                self.assertTrue(item.genres)
                self.assertTrue(item.contributes)

    def test_inspirations_for_an_unknown_genre_is_a_clear_error(self):
        with self.assertRaises(KeyError):
            _fixture().inspirations_for_genre("steampunk")

    def test_an_unknown_domain_or_genre_or_inspiration_is_a_clear_error(self):
        model = _fixture()
        for call in (
            lambda: model.technology("no_such_domain"),
            lambda: model.genre("no_such_genre"),
            lambda: model.inspiration("no_such_inspiration"),
        ):
            with self.assertRaises(KeyError):
                call()

    def test_a_duplicate_inspiration_id_is_refused(self):
        data = copy.deepcopy(_FIXTURE)
        data["inspirations"].append(dict(data["inspirations"][0]))
        with self.assertRaises(ValueError):
            genre_paradigms_from_dict(data)

    def test_a_document_of_another_format_is_refused(self):
        import tempfile

        with tempfile.TemporaryDirectory() as tmp:
            wrong = Path(tmp) / "other.json"
            wrong.write_text(json.dumps({"format": "something.else"}), encoding="utf-8")
            with self.assertRaises(ValueError):
                load_genre_paradigms(wrong)

    def test_lookups_do_not_mutate_the_model(self):
        model = _fixture()
        before = json.dumps({k: v.to_dict() for k, v in model.genres.items()}, sort_keys=True)
        model.inspirations_for_genre("biopunk")
        model.systems_spawned_by_genres()
        model.unearned_capability_claims()
        model.off_vocabulary()
        after = json.dumps({k: v.to_dict() for k, v in model.genres.items()}, sort_keys=True)
        self.assertEqual(before, after)


class ScopeDirectiveTests(unittest.TestCase):
    """The crossover is inspired by LaclauGPT and must never import it (issues #282/#299)."""

    def test_importing_the_module_couples_to_no_laclaugpt_package(self):
        code = (
            "import sys, strategy_game, strategy_game.genre_paradigms as g;"
            "m = g.load_genre_paradigms();"
            "m.systems_spawned_by_genres(); m.unearned_capability_claims();"
            "m.inspirations_for_genre('psipunk');"
            "print(sorted(x for x in sys.modules if x == 'laclaugpt' or x.startswith('laclaugpt.')))"
        )
        result = subprocess.run(
            [sys.executable, "-c", code], cwd=ROOT, capture_output=True, text=True, check=False
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stdout.strip(), "[]", f"loading the module pulled in LaclauGPT: {result.stdout}")

    def test_the_module_source_imports_no_laclaugpt(self):
        text = (ROOT / "strategy_game" / "genre_paradigms.py").read_text(encoding="utf-8")
        self.assertNotIn("import laclaugpt", text)
        self.assertNotIn("from laclaugpt", text)


class LensTests(unittest.TestCase):
    """Issue #359: further lenses are overlapping readings, not compulsory genre declarations."""

    def test_no_shipped_lens_spawns_a_system(self):
        model = load_genre_paradigms()
        self.assertEqual(model.lenses_that_spawn_a_system(), ())
        self.assertTrue(model.genre_lenses, "the lens index would be empty")

    def test_every_shipped_lens_declares_a_status_from_the_vocabulary(self):
        model = load_genre_paradigms()
        for lens in model.genre_lenses.values():
            with self.subTest(lens=lens.identifier):
                self.assertIn(lens.status, LENS_STATUSES)

    def test_a_lens_that_spawns_a_system_is_reported(self):
        data = copy.deepcopy(_FIXTURE)
        data["genre_lenses"][0]["spawns_system"] = True
        self.assertEqual(genre_paradigms_from_dict(data).lenses_that_spawn_a_system(), ("hopepunk",))

    def test_a_lens_with_an_undeclared_status_is_reported(self):
        data = copy.deepcopy(_FIXTURE)
        data["genre_lenses"][0]["status"] = "seventh_genre"
        reported = genre_paradigms_from_dict(data).off_vocabulary()
        self.assertIn(("hopepunk", "lens_status", "seventh_genre"), reported)

    def test_the_lenses_are_not_silently_promoted_into_the_six_genres(self):
        """A lens is a way of reading the six genres; adding one must not add a seventh genre."""
        model = load_genre_paradigms()
        self.assertEqual(set(model.genres), set(GENRE_IDS))
        self.assertFalse(set(model.genre_lenses) & set(model.genres))


class CandidateParadigmTests(unittest.TestCase):
    """Issue #359: a candidate is not promoted except by the author's own design test."""

    def test_no_shipped_candidate_is_promoted(self):
        model = load_genre_paradigms()
        self.assertEqual(model.promoted_paradigms(), ())
        self.assertEqual(model.candidates_without_a_promotion_status(), ())
        self.assertTrue(model.candidates(), "the candidate list would be empty")

    def test_every_shipped_candidate_states_where_it_stands_and_its_test(self):
        model = load_genre_paradigms()
        for candidate in model.candidates():
            with self.subTest(candidate=candidate.identifier):
                self.assertIn(candidate.promotion, PROMOTION_STATUSES)
                self.assertIn(candidate.kind, CANDIDATE_KINDS)
                self.assertTrue(candidate.promotion_test.strip())

    def test_a_promoted_candidate_is_reported(self):
        data = copy.deepcopy(_FIXTURE)
        data["candidate_paradigms"][0]["promotion"] = "promoted_foundational"
        self.assertEqual(genre_paradigms_from_dict(data).promoted_paradigms(), ("quantum",))

    def test_a_candidate_without_a_status_is_reported(self):
        data = copy.deepcopy(_FIXTURE)
        data["candidate_paradigms"][0].pop("promotion")
        self.assertEqual(genre_paradigms_from_dict(data).candidates_without_a_promotion_status(), ("quantum",))

    def test_a_candidate_attaches_only_to_declared_domains(self):
        model = load_genre_paradigms()
        for candidate in model.candidates():
            for domain_id in candidate.attaches_to:
                with self.subTest(candidate=candidate.identifier, domain=domain_id):
                    self.assertIn(domain_id, DOMAIN_IDS)

    def test_a_candidate_attached_to_an_invented_domain_is_reported(self):
        data = copy.deepcopy(_FIXTURE)
        data["candidate_paradigms"][0]["attaches_to"] = ["chronomancy"]
        reported = genre_paradigms_from_dict(data).off_vocabulary()
        self.assertIn(("quantum", "attaches_to", "chronomancy"), reported)

    def test_a_candidate_naming_an_undeclared_event_card_is_reported(self):
        data = copy.deepcopy(_FIXTURE)
        data["candidate_paradigms"][0]["event_cards"] = ["a_card_that_does_not_exist"]
        reported = genre_paradigms_from_dict(data).off_vocabulary()
        self.assertIn(("quantum", "event_cards", "a_card_that_does_not_exist"), reported)


class ProposalTests(unittest.TestCase):
    """Issue #359: a named event card or strategic project is a title, never an effect."""

    def test_no_shipped_project_or_event_idea_carries_an_effect(self):
        model = load_genre_paradigms()
        self.assertEqual(model.proposals_with_effects(), ())
        self.assertTrue(model.strategic_projects and model.event_card_ideas)

    def test_a_proposal_with_an_effect_is_reported(self):
        data = copy.deepcopy(_FIXTURE)
        data["strategic_projects"][0]["effects"] = [{"kind": "unspecified"}]
        self.assertEqual(genre_paradigms_from_dict(data).proposals_with_effects(), ("living_seawalls",))

    def test_a_proposal_naming_an_undeclared_genre_is_reported(self):
        data = copy.deepcopy(_FIXTURE)
        data["event_card_ideas"][0]["genres"] = ["steampunk"]
        reported = genre_paradigms_from_dict(data).off_vocabulary()
        self.assertIn(("a_card", "genres", "steampunk"), reported)

    def test_every_shipped_proposal_names_a_genre_the_setting_declares(self):
        model = load_genre_paradigms()
        for proposal in model.proposals():
            for genre_id in proposal.genres:
                with self.subTest(proposal=proposal.identifier, genre=genre_id):
                    self.assertIn(genre_id, GENRE_IDS)


class PressureAxisTests(unittest.TestCase):
    """Issue #359's faction responses, recorded as pairs of named positions rather than a scale."""

    def test_every_shipped_axis_is_a_pair_of_named_positions(self):
        model = load_genre_paradigms()
        self.assertEqual(model.axes_that_are_not_pairs(), ())
        self.assertTrue(model.faction_pressure_axes)
        for axis in model.faction_pressure_axes.values():
            with self.subTest(axis=axis.identifier):
                self.assertEqual(len(axis.poles), 2)
                self.assertTrue(all(pole.strip() for pole in axis.poles))

    def test_an_axis_that_is_not_a_pair_is_reported(self):
        data = copy.deepcopy(_FIXTURE)
        data["faction_pressure_axes"][0]["poles"] = ["pro-biotech"]
        self.assertEqual(genre_paradigms_from_dict(data).axes_that_are_not_pairs(), ("biotech_alignment",))

    def test_no_axis_is_recorded_as_an_approved_scale(self):
        """Whether an axis becomes a tag set is pending; the reader must not read one as settled."""
        model = load_genre_paradigms()
        for axis in model.faction_pressure_axes.values():
            with self.subTest(axis=axis.identifier):
                self.assertEqual(axis.recorded_as, "pending_author_decision")


class PriorUseTests(unittest.TestCase):
    """Issue #359: record the earlier uses of a name without claiming the name established a school."""

    def test_no_shipped_prior_use_claims_established_canon(self):
        model = load_genre_paradigms()
        self.assertEqual(model.prior_uses_claiming_established_canon(), ())
        self.assertTrue(model.prior_use_order_records())

    def test_every_shipped_prior_use_names_a_declared_genre_and_claim(self):
        model = load_genre_paradigms()
        for use in model.prior_use_order_records():
            with self.subTest(use=use.identifier):
                self.assertIn(use.genre, GENRE_IDS)
                self.assertIn(use.claim, PRIOR_USE_CLAIMS)

    def test_a_prior_use_with_an_undeclared_claim_is_reported(self):
        data = copy.deepcopy(_FIXTURE)
        data["prior_uses"]["entries"][0]["claim"] = "established_canon"
        reported = genre_paradigms_from_dict(data).prior_uses_claiming_established_canon()
        self.assertEqual(reported, ("a_tag",))

    def test_the_prior_uses_are_read_as_prior_uses_of_the_two_internal_names(self):
        model = load_genre_paradigms()
        genres = {use.genre for use in model.prior_use_order_records()}
        self.assertEqual(genres, {"ufopunk", "xenopunk"})
        for genre_id in genres:
            with self.subTest(genre=genre_id):
                self.assertFalse(model.genre(genre_id).established_genre_canon)


class CatalogueCoverageTests(unittest.TestCase):
    """Issue #359 asks for a fiction **and** a non-fiction catalogue per genre."""

    def test_every_shipped_genre_has_a_fiction_and_a_non_fiction_entry(self):
        model = load_genre_paradigms()
        self.assertEqual(model.genres_without_a_fiction_and_a_research_inspiration(), ())

    def test_a_genre_with_only_fiction_is_reported(self):
        data = copy.deepcopy(_FIXTURE)
        data["inspirations"][1]["kind"] = "fiction"
        data["inspirations"][1]["capability_status"] = "not_applicable"
        reported = genre_paradigms_from_dict(data).genres_without_a_fiction_and_a_research_inspiration()
        self.assertIn("biopunk", reported)

    def test_the_ufopunk_and_xenopunk_non_fiction_entries_are_typed_as_research(self):
        """Neither name has established canon, so its non-fiction side is a tradition of claims."""
        model = load_genre_paradigms()
        for genre_id in ("ufopunk", "xenopunk"):
            research = [item for item in model.inspirations_for_genre(genre_id) if item.is_research]
            with self.subTest(genre=genre_id):
                self.assertTrue(research)
                for item in research:
                    self.assertIn(item.capability_status, CAPABILITY_STATUSES)
                    self.assertNotEqual(item.capability_status, "not_applicable")


class CrossReferenceTests(unittest.TestCase):
    """Issue #359 requires the links to the paradigm, PSI, faction and timeline issues to survive."""

    def test_the_related_issues_are_kept_with_their_relation(self):
        model = load_genre_paradigms()
        numbers = {int(record["issue"]) for record in model.related_issues}
        self.assertTrue({98, 42, 328, 329, 345, 346, 348, 304} <= numbers, sorted(numbers))
        for record in model.related_issues:
            with self.subTest(issue=record["issue"]):
                self.assertTrue(str(record.get("relation") or "").strip())


if __name__ == "__main__":
    unittest.main()
