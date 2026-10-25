"""Executable contracts for NoöPunk's own subsystems (#572): the ubiquitous network and natural PSI.

Code-only, per `AGENTS.md` and issue #271. These test the **implementations**, not prose.

Both modules exist because the Without Number family has no equivalent: CWN/SWN/AWN/WWN assume a
matrix-and-deck network economy and a virus-or-class psionics, while NoöPunk assumes **ubiquity with
islands** and **a natural capacity that training makes reliable**. So what is pinned here is exactly
the part that must not drift:

* the route ↔ target table is the chapter's own (§22.5.2), including `isolated` → class 1 only;
* exposure is the only budget, it never falls except by a Cover action, and its bands escalate;
* a psychic discipline is refused when it is untrained — learnability is the mechanic, not a bonus;
* Effort is committed capacity (the WWN *pattern*, independently implemented), never a second
  hit-point track, and both subsystems resolve on the one `STAT + Skill + 1d10` kernel.

Run:
    python -m unittest discover -s tests -p "test_issue572_native_subsystems.py"
"""

from __future__ import annotations

import json
import unittest
from pathlib import Path
from random import Random

from src.rules import natural_psi as psi
from src.rules import ubiquitous_network as net

ROOT = Path(__file__).resolve().parents[1]


class ReachTableTests(unittest.TestCase):
    """§22.5.2's pairing table is canon; this module consumes it and may not soften it."""

    def test_isolated_is_reachable_only_by_class_one_in_every_era(self) -> None:
        for era in net.Era:
            for access in net.AccessClass:
                if access is net.AccessClass.QUARANTINE:
                    continue  # class 5 is its own legality question, tested below
                possible, _ = net.reach(net.ConnectivityClass.ISOLATED, access, era)
                self.assertEqual(possible, access is net.AccessClass.LOCAL,
                                 f"{access.value} vs isolated in {era.value}")

    def test_the_table_matches_the_chapter_for_every_public_pair(self) -> None:
        era = net.Era.AFTER_CRISIS
        expectations = {
            net.ConnectivityClass.PUBLIC_GATEWAY: {net.AccessClass.SAFENET, net.AccessClass.LAN},
            net.ConnectivityClass.SAFENET_EXPOSED: {net.AccessClass.SAFENET, net.AccessClass.LAN},
            net.ConnectivityClass.PRIVATE_LINKED: {net.AccessClass.LAN, net.AccessClass.LOCAL},
            net.ConnectivityClass.LOCAL_ONLY: {net.AccessClass.LOCAL, net.AccessClass.NEARBY},
            net.ConnectivityClass.ISOLATED: {net.AccessClass.LOCAL},
        }
        self.assertEqual(set(net.REACH_TABLE), set(expectations))
        for target, allowed in expectations.items():
            for access in net.AccessClass:
                if access is net.AccessClass.QUARANTINE:
                    continue
                self.assertEqual(net.reach(target, access, era)[0], access in allowed)

    def test_the_public_network_can_be_down_and_only_that_changes(self) -> None:
        """The era dial: class 4 fails during the crisis; class 3 still works."""
        target = net.ConnectivityClass.PUBLIC_GATEWAY
        self.assertFalse(net.reach(target, net.AccessClass.SAFENET, net.Era.NHI_CRISIS)[0])
        self.assertTrue(net.reach(target, net.AccessClass.LAN, net.Era.NHI_CRISIS)[0])
        self.assertTrue(net.reach(target, net.AccessClass.SAFENET, net.Era.AFTER_CRISIS)[0])

    def test_class_five_is_always_possible_and_always_a_breach(self) -> None:
        for target in net.ConnectivityClass:
            possible, reason = net.reach(target, net.AccessClass.QUARANTINE, net.Era.ACCELERATION)
            self.assertTrue(possible)
            self.assertIn("crime", reason)

    def test_an_impossible_pairing_cannot_start_a_session(self) -> None:
        with self.assertRaises(net.NetworkError):
            net.IntrusionSession(target=net.ConnectivityClass.ISOLATED,
                                 access=net.AccessClass.SAFENET, era=net.Era.ACCELERATION)


class ExposureEconomyTests(unittest.TestCase):
    """Ubiquity means everything logs. There is no concealment stat, only exposure."""

    def _session(self, *, seed: int = 7) -> net.IntrusionSession:
        return net.IntrusionSession(
            target=net.ConnectivityClass.LOCAL_ONLY,
            access=net.AccessClass.NEARBY,
            era=net.Era.ACCELERATION,
            rng=Random(seed),
        )

    def test_exposure_only_falls_by_covering_and_never_below_zero(self) -> None:
        session = self._session()
        start = session.exposure
        session.intrude(stat=5, skill_rating=5, dv=15)
        self.assertGreater(session.exposure, start)
        session.new_exchange()
        session.cover()
        self.assertGreaterEqual(session.exposure, 0)
        session.new_exchange()
        session.cover()
        self.assertEqual(session.exposure, 0, "cover may not push exposure negative")

    def test_a_failed_attempt_costs_more_than_a_quiet_success(self) -> None:
        session = self._session(seed=1)
        failed = session.intrude(stat=5, skill_rating=5, dv=25)     # hopeless
        session.new_exchange()
        quiet = session.intrude(stat=10, skill_rating=10, dv=5, quiet=True)  # certain
        self.assertGreater(failed.exposure_added, quiet.exposure_added)

    def test_alert_bands_escalate_and_are_ordered(self) -> None:
        states = [net.alert_state(n) for n in range(0, 15)]
        seen = [s for i, s in enumerate(states) if i == 0 or s is not states[i - 1]]
        self.assertEqual(seen, [net.AlertState.QUIET, net.AlertState.WATCHED,
                                net.AlertState.FLAGGED, net.AlertState.HUNTED])

    def test_ap_is_the_shared_clock_and_does_not_carry(self) -> None:
        session = self._session()
        for _ in range(net.TUNING_AP_PER_EXCHANGE):
            session.intrude(stat=5, skill_rating=5, dv=15)
            session.new_exchange()
        session.intrude(stat=5, skill_rating=5, dv=15)
        session.intrude(stat=5, skill_rating=5, dv=15)
        session.intrude(stat=5, skill_rating=5, dv=15)
        with self.assertRaises(net.NetworkError):
            session.intrude(stat=5, skill_rating=5, dv=15)

    def test_intrusion_resolves_on_the_one_kernel(self) -> None:
        session = self._session(seed=7)
        step = session.intrude(stat=5, skill_rating=4, dv=15, die=3)
        self.assertEqual(step.outcome, "failure")
        self.assertEqual(step.margin, 5 + 4 + 3 - 15,
                         "the margin is the kernel's total minus the DV, never a second roll")
        session.new_exchange()
        loud = session.intrude(stat=5, skill_rating=4, dv=10, die=8)
        self.assertEqual(loud.outcome, "success")
        self.assertEqual(loud.margin, 5 + 4 + 8 - 10)

    def test_the_same_seed_replays_and_a_different_seed_does_not(self) -> None:
        def margins(seed: int) -> list[int]:
            session = self._session(seed=seed)
            out = []
            for _ in range(10):
                out.append(session.intrude(stat=5, skill_rating=5, dv=15).margin)
                session.new_exchange()
            return out

        self.assertEqual(margins(5), margins(5))
        self.assertNotEqual(margins(5), margins(6), "different seeds must change the sequence")


class NaturalPsiTests(unittest.TestCase):
    """PSI is a natural capacity that training makes usable — not a virus, class or level."""

    def test_the_disciplines_are_exactly_the_six_canonical_psy_skills(self) -> None:
        canon = json.loads((ROOT / "data" / "rules" / "core.json").read_text(encoding="utf-8"))
        psy_skills = {s for s in canon["skills"]["final_list"]
                      if s in {"ESP", "Telepathy", "Psychokinesis", "Precognition",
                               "Psychic Defence", "Noöspace"}}
        self.assertEqual({d.value for d in psi.Discipline}, psy_skills)

    def test_training_decides_usability_and_unsupervised_hours_count_half(self) -> None:
        self.assertIs(psi.training_for(0), psi.Training.UNTRAINED)
        self.assertIs(psi.training_for(psi.TUNING_MIN_PRACTICE), psi.Training.PRACTISED)
        self.assertIs(psi.training_for(psi.TUNING_MASTERY_PRACTICE), psi.Training.MASTERED)
        block = psi.practice(psi.Discipline.ESP, hours=40, supervised=False)
        self.assertEqual(block["hours"], 20)
        self.assertEqual(block["training_after"], psi.Training.PRACTISED.value)

    def test_effort_capacity_grows_slowly_and_stops(self) -> None:
        curve = [psi.effort_capacity(psy) for psy in range(1, 11)]
        self.assertEqual(curve, sorted(curve))
        self.assertEqual(max(curve), psi.TUNING_MAX_EFFORT)
        self.assertEqual(curve[-1], psi.TUNING_MAX_EFFORT, "PSY 10 reaches the cap")
        self.assertEqual(curve[0], psi.TUNING_BASE_EFFORT)
        with self.assertRaises(psi.PsiError):
            psi.effort_capacity(0)

    def test_an_untrained_discipline_is_refused_before_any_die(self) -> None:
        actor = psi.Practitioner(psy=6, skills={"ESP": 5})
        with self.assertRaises(psi.PsiError) as caught:
            actor.attempt(psi.Discipline.ESP, dv=15)
        self.assertIn("untrained", str(caught.exception))

    def test_a_trained_attempt_resolves_on_the_one_kernel(self) -> None:
        actor = psi.Practitioner(psy=6, practice={psi.Discipline.TELEPATHY: 40},
                                 skills={"Telepathy": 5})
        attempt = actor.attempt(psi.Discipline.TELEPATHY, dv=15, die=5)
        self.assertEqual(attempt.total, 6 + 5 + 5)
        self.assertEqual(attempt.outcome, psi.Outcome.SUCCESS)

    def test_mastery_softens_the_cost_of_failure_once(self) -> None:
        practised = psi.Practitioner(psy=6, practice={psi.Discipline.ESP: 40}, skills={"ESP": 1})
        mastered = psi.Practitioner(psy=6, practice={psi.Discipline.ESP: 200}, skills={"ESP": 1})
        hard = 25
        self.assertEqual(practised.attempt(psi.Discipline.ESP, dv=hard, die=1).pressure.psyche_load,
                         psi.TUNING_PRESSURE_PER_FAILURE)
        self.assertEqual(mastered.attempt(psi.Discipline.ESP, dv=hard, die=1).pressure.psyche_load,
                         max(0, psi.TUNING_PRESSURE_PER_FAILURE - 1))

    def test_a_discipline_without_a_rating_is_refused_not_rolled(self) -> None:
        """The kernel takes a 1..10 Skill; a practised but unrated discipline says so."""
        actor = psi.Practitioner(psy=6, practice={psi.Discipline.ESP: 40}, skills={})
        with self.assertRaises(psi.PsiError) as caught:
            actor.attempt(psi.Discipline.ESP, dv=15)
        self.assertIn("no rating", str(caught.exception))

    def test_consensus_is_capped_and_symmetric(self) -> None:
        cap = psi.TUNING_CONSENSUS_CAP
        self.assertEqual(psi.consensus_modifier(9, 0), cap)
        self.assertEqual(psi.consensus_modifier(0, 9), -cap)
        self.assertEqual(psi.consensus_modifier(0, 0), 0)

    def test_effort_is_committed_capacity_and_release_is_explicit(self) -> None:
        actor = psi.Practitioner(psy=6, practice={psi.Discipline.ESP: 40})
        actor.commit("a watching thread", cost=2)
        self.assertEqual(actor.effort_free, actor.capacity - 2)
        with self.assertRaises(psi.PsiError):
            actor.commit("too much", cost=actor.capacity)
        self.assertEqual(actor.release("a watching thread"), 2)
        self.assertEqual(actor.effort_free, actor.capacity)
        self.assertEqual(actor.release("never committed"), 0)

    def test_psyche_load_recovers_but_commitments_do_not_expire(self) -> None:
        actor = psi.Practitioner(psy=6, practice={psi.Discipline.ESP: 40}, skills={"ESP": 1})
        actor.attempt(psi.Discipline.ESP, dv=25, die=1)
        self.assertGreater(actor.psyche_load, 0)
        actor.commit("a lasting effect", cost=1)
        actor.recover(scenes=3)
        self.assertEqual(actor.psyche_load, 0)
        self.assertEqual(actor.effort_free, actor.capacity - 1,
                         "a commitment is released, not timed out")

    def test_the_same_seed_replays(self) -> None:
        def run(seed: int) -> psi.Attempt:
            actor = psi.Practitioner(psy=6, practice={psi.Discipline.ESP: 40},
                                     skills={"ESP": 4}, rng=Random(seed))
            return actor.attempt(psi.Discipline.ESP, dv=15)
        self.assertEqual(run(3), run(3))


if __name__ == "__main__":
    unittest.main()
