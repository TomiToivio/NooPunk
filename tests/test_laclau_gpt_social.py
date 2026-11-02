"""The LaclauGPT character mod keeps ideology, stances and relations apart (#1042).

The issue's acceptance criterion is blunt: a character may ideologically agree with an untrusted
stranger and disagree with a trusted colleague, and the engine must not confuse the two. Most of these
tests exist to hold that line — that no stance writes a tie, that no tie writes trust, and that a
missing statement is reported as *no evidence* instead of as neutrality.
"""
import json
import unittest

from src.rules.laclau_gpt_social import (
    SCHEMA_VERSION,
    Compatibility,
    Concept,
    DiscourseProfile,
    GameRelation,
    GoalKind,
    Polarity,
    Provenance,
    SocialModelError,
    SocialWorld,
    Stance,
    Tie,
    TieKind,
)


def world_with(*actors: str) -> SocialWorld:
    world = SocialWorld()
    for actor in actors:
        world.add_actor(actor, name=actor.title(), provenance=Provenance.FICTION)
    for concept in ("noosphere", "disclosure", "curfew"):
        world.add_concept(Concept(concept, concept.title(), chain="psi"))
    return world


def stance(actor: str, concept: str, polarity: Polarity, on: str = "2026-03-01",
           provenance: Provenance = Provenance.EVIDENCE) -> Stance:
    return Stance(actor=actor, concept=concept, polarity=polarity, on=on, provenance=provenance)


class SeparationTests(unittest.TestCase):
    """DNA and SNA must not leak into each other."""

    def test_agreement_creates_no_tie(self):
        world = world_with("maja", "hanna")
        world.record_stance(stance("maja", "disclosure", Polarity.SUPPORT))
        world.record_stance(stance("hanna", "disclosure", Polarity.SUPPORT))

        self.assertEqual(world.compatibility("maja", "hanna").score, 1.0)
        self.assertEqual(world.ties_of("maja"), ())
        self.assertIsNone(world.relation("maja", "hanna"))

    def test_a_tie_grants_no_trust(self):
        world = world_with("maja", "hanna")
        world.record_tie(Tie("maja", "hanna", TieKind.COMMUNICATION, "2026-02-01", Provenance.EVIDENCE))

        self.assertEqual(len(world.ties_of("maja")), 1)
        self.assertIsNone(world.relation("maja", "hanna"), "a call log is not trust")

    def test_disagreement_with_a_trusted_colleague_stays_disagreement(self):
        world = world_with("maja", "hanna")
        world.record_stance(stance("maja", "curfew", Polarity.OPPOSE))
        world.record_stance(stance("hanna", "curfew", Polarity.SUPPORT))
        world.record_tie(Tie("maja", "hanna", TieKind.AFFILIATION, "2026-01-10", Provenance.EVIDENCE))
        world.adjust_relation("maja", "hanna", trust=3)

        compatibility = world.compatibility("maja", "hanna")
        self.assertEqual((compatibility.agree, compatibility.disagree), (0, 1))
        self.assertEqual(compatibility.score, -1.0)
        relation = world.relation("maja", "hanna")
        assert relation is not None
        self.assertEqual(relation.trust, 3)

    def test_agreement_with_a_stranger_stays_agreement(self):
        world = world_with("maja", "stranger")
        world.record_stance(stance("maja", "noosphere", Polarity.SUPPORT))
        world.record_stance(stance("stranger", "noosphere", Polarity.SUPPORT))

        self.assertEqual(world.compatibility("maja", "stranger").score, 1.0)
        self.assertEqual(world.decision_context("maja")["ties"], [])
        self.assertEqual(world.decision_context("maja")["relations"], {})


class UncertaintyTests(unittest.TestCase):
    def test_no_shared_statement_is_not_neutrality(self):
        world = world_with("maja", "hanna")
        world.record_stance(stance("maja", "curfew", Polarity.SUPPORT))

        compatibility = world.compatibility("maja", "hanna")
        self.assertIsInstance(compatibility, Compatibility)
        self.assertFalse(compatibility.has_evidence)
        self.assertIsNone(compatibility.score)
        self.assertEqual(compatibility.shared, 0)

    def test_uncertain_is_counted_apart_from_agree_and_disagree(self):
        world = world_with("maja", "hanna")
        world.record_stance(stance("maja", "disclosure", Polarity.SUPPORT))
        world.record_stance(stance("hanna", "disclosure", Polarity.UNCERTAIN))

        compatibility = world.compatibility("maja", "hanna")
        self.assertEqual((compatibility.agree, compatibility.disagree, compatibility.uncertain), (0, 0, 1))
        self.assertIsNone(compatibility.score, "an unsure actor is not a vote either way")

    def test_uncertain_does_not_dilute_a_decided_score(self):
        world = world_with("maja", "hanna")
        world.record_stance(stance("maja", "disclosure", Polarity.SUPPORT))
        world.record_stance(stance("hanna", "disclosure", Polarity.SUPPORT))
        world.record_stance(stance("maja", "curfew", Polarity.SUPPORT))
        world.record_stance(stance("hanna", "curfew", Polarity.UNCERTAIN))

        self.assertEqual(world.compatibility("maja", "hanna").score, 1.0)


class VersioningTests(unittest.TestCase):
    def test_a_later_stance_supersedes_but_does_not_erase(self):
        world = world_with("maja")
        world.record_stance(stance("maja", "disclosure", Polarity.SUPPORT, on="2026-01-01"))
        world.record_stance(stance("maja", "disclosure", Polarity.OPPOSE, on="2026-04-01"))

        self.assertEqual(world.stance("maja", "disclosure").polarity, Polarity.OPPOSE)
        self.assertEqual(world.stance("maja", "disclosure", on_or_before="2026-02-01").polarity,
                         Polarity.SUPPORT)
        self.assertEqual(len(world.stances), 2, "history is append-only")

    def test_profile_revision_must_be_the_next_version(self):
        world = world_with("maja")
        first = DiscourseProfile(actor="maja", values=["transparency"], on="2026-01-01")
        world.set_profile(first)

        with self.assertRaises(SocialModelError):
            world.set_profile(DiscourseProfile(actor="maja", version=3, on="2026-02-01"))

        second = first.revise("2026-02-01", demands=["publish the Vallée files"])
        world.set_profile(second)
        self.assertEqual(world.profiles["maja"].version, 2)
        self.assertEqual(world.profiles["maja"].values, ["transparency"])


class ProvenanceTests(unittest.TestCase):
    def test_every_write_is_logged_with_its_kind_and_provenance(self):
        world = world_with("maja", "hanna")
        world.record_stance(stance("maja", "disclosure", Polarity.SUPPORT))
        world.record_tie(Tie("maja", "hanna", TieKind.PERSONAL, "2026-02-02", Provenance.FICTION))
        world.adjust_relation("maja", "hanna", trust=1)

        kinds = [(event["kind"], event["provenance"]) for event in world.events]
        self.assertIn(("stance.recorded", "evidence"), kinds)
        self.assertIn(("tie.recorded", "fiction"), kinds)
        self.assertIn(("relation.adjusted", "outcome"), kinds)

    def test_a_fictional_stance_is_recorded_as_fiction(self):
        world = world_with("maja")
        world.record_stance(stance("maja", "noosphere", Polarity.SUPPORT, provenance=Provenance.FICTION))
        self.assertEqual(world.stances[0].provenance, Provenance.FICTION)


class DecisionContextTests(unittest.TestCase):
    def test_context_keeps_the_layers_labelled(self):
        world = world_with("maja", "hanna")
        profile = DiscourseProfile(actor="maja", identities=["UNSA analyst"],
                                   goals={GoalKind.INSTITUTIONAL: ["keep the office open"]},
                                   on="2026-01-01")
        world.set_profile(profile)
        world.record_stance(stance("maja", "disclosure", Polarity.SUPPORT))
        world.record_tie(Tie("maja", "hanna", TieKind.COMMUNICATION, "2026-02-01", Provenance.EVIDENCE))
        world.adjust_relation("maja", "hanna", trust=2, access=1)

        context = world.decision_context("maja", concept="disclosure")
        self.assertEqual(context["ideology"]["identities"], ["UNSA analyst"])
        self.assertEqual(context["stance"]["polarity"], "support")
        self.assertEqual(context["ties"], ["hanna"])
        self.assertEqual(context["relations"]["hanna"]["trust"], 2)
        self.assertEqual(context["relations"]["hanna"]["access"], 1)

    def test_absent_stance_is_reported_as_absent(self):
        world = world_with("maja")
        self.assertIsNone(world.decision_context("maja", concept="curfew")["stance"])


class PersistenceTests(unittest.TestCase):
    def test_snapshot_round_trips_through_json(self):
        world = world_with("maja", "hanna")
        world.set_profile(DiscourseProfile(actor="maja", values=["transparency"],
                                          goals={GoalKind.PERSONAL: ["find the witness"]},
                                          on="2026-01-01"))
        world.record_stance(stance("maja", "curfew", Polarity.OPPOSE))
        world.record_tie(Tie("maja", "hanna", TieKind.AFFILIATION, "2026-02-01", Provenance.EVIDENCE))
        world.adjust_relation("maja", "hanna", trust=2)

        restored = SocialWorld.from_json(world.to_json())

        self.assertEqual(restored.snapshot(), world.snapshot())
        self.assertEqual(restored.compatibility("maja", "hanna").score, None)
        relation = restored.relation("maja", "hanna")
        assert relation is not None
        self.assertEqual((relation.trust, relation.access), (2, 0))

    def test_unknown_schema_is_refused(self):
        with self.assertRaises(SocialModelError):
            SocialWorld.from_snapshot({"schema": SCHEMA_VERSION + 1, "actors": {}, "concepts": {},
                                       "profiles": [], "stances": [], "ties": [], "relations": [],
                                       "events": []})

    def test_a_relation_axis_typo_cannot_silently_do_nothing(self):
        relation = GameRelation()
        with self.assertRaises(SocialModelError):
            relation.adjust(trustt=1)


class RegistrationTests(unittest.TestCase):
    def test_stances_and_ties_require_registered_actors(self):
        world = world_with("maja")
        with self.assertRaises(SocialModelError):
            world.record_stance(stance("ghost", "curfew", Polarity.SUPPORT))
        with self.assertRaises(SocialModelError):
            world.record_tie(Tie("maja", "ghost", TieKind.COMMUNICATION, "2026-01-01",
                                 Provenance.EVIDENCE))

    def test_an_unknown_concept_is_refused(self):
        world = world_with("maja")
        with self.assertRaises(SocialModelError):
            world.record_stance(stance("maja", "ufology", Polarity.SUPPORT))

    def test_ids_and_dates_are_validated(self):
        with self.assertRaises(SocialModelError):
            Stance(actor="", concept="curfew", polarity=Polarity.SUPPORT, on="2026-01-01",
                   provenance=Provenance.EVIDENCE)
        with self.assertRaises(SocialModelError):
            Stance(actor="maja", concept="curfew", polarity=Polarity.SUPPORT, on="1.1.2026",
                   provenance=Provenance.EVIDENCE)

    def test_a_self_tie_is_refused(self):
        with self.assertRaises(SocialModelError):
            Tie("maja", "maja", TieKind.PERSONAL, "2026-01-01", Provenance.EVIDENCE)


class SerialisationShapeTests(unittest.TestCase):
    def test_goals_serialise_by_name_not_by_enum_repr(self):
        world = world_with("maja")
        world.set_profile(DiscourseProfile(actor="maja",
                                           goals={GoalKind.IDEOLOGICAL: ["end the secrecy"]},
                                           on="2026-01-01"))
        payload = json.loads(world.to_json())
        self.assertEqual(payload["profiles"][0]["goals"], {"ideological": ["end the secrecy"]})


if __name__ == "__main__":
    unittest.main()
