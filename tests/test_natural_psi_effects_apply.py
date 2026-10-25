"""Regression tests: an effect that is computed must actually apply.

Found by review on 2026-10-25. Both tests below failed against `main` because
`Practitioner.attempt` computed two things and then threw them away:

1. `modifier` (consensus: believers make an act easier, doubters harder) was computed,
   stored on the returned `Attempt`, and **never passed to the kernel** — because
   `core.resolve_check` takes `STAT + Skill + 1d10 >= DV` and no modifier argument.
   So the room had no effect on any roll.
2. `effort` was committed and then released at the end of the same call, so spending
   Effort was a pure no-op that also cost nothing: it only asserted you had the
   capacity, then handed it straight back. `commitments do not expire on their own`
   was true everywhere except in the one method that spends them.

Neither bug was caught because the only consensus test asserted the *value* of
`consensus_modifier` and nothing ever passed `effort=`.
"""
import unittest

from src.rules import natural_psi as psi


def _practitioner() -> psi.Practitioner:
    return psi.Practitioner(
        psy=6,
        practice={psi.Discipline.TELEPATHY: psi.TUNING_MIN_PRACTICE},
        skills={psi.Discipline.TELEPATHY.value: 1},
    )


class ConsensusActuallyAppliesTests(unittest.TestCase):
    """The room matters — so it has to change the result, not just a field."""

    def test_believers_make_a_tie_into_a_success(self) -> None:
        p = _practitioner()
        # PSY 6 + Skill 1 + die 5 = 12 against DV 12 is a tie with nobody watching.
        bare = p.attempt(psi.Discipline.TELEPATHY, dv=12, die=5)
        self.assertIs(bare.outcome, psi.Outcome.TIE)
        self.assertFalse(bare.succeeded)

        heard = p.attempt(psi.Discipline.TELEPATHY, dv=12, die=5, believers=2)
        self.assertGreater(heard.modifier, 0)
        self.assertGreater(heard.total, bare.total,
                           "two convinced witnesses must move the total, not just the field")
        self.assertTrue(heard.succeeded)

    def test_doubters_turn_a_tie_into_a_failure(self) -> None:
        p = _practitioner()
        bare = p.attempt(psi.Discipline.TELEPATHY, dv=12, die=5)
        doubted = p.attempt(psi.Discipline.TELEPATHY, dv=12, die=5, doubters=2)
        self.assertLess(doubted.modifier, 0)
        self.assertLess(doubted.total, bare.total)
        self.assertIs(doubted.outcome, psi.Outcome.FAILURE)

    def test_the_modifier_is_capped_on_both_sides(self) -> None:
        p = _practitioner()
        many = p.attempt(psi.Discipline.TELEPATHY, dv=12, die=5, believers=9)
        self.assertEqual(many.modifier, psi.TUNING_CONSENSUS_CAP)


class EffortActuallyCostsTests(unittest.TestCase):
    """Committing Effort locks capacity until it is released — including in attempt()."""

    def test_effort_spent_on_an_attempt_stays_committed(self) -> None:
        p = _practitioner()
        before = p.effort_free
        p.attempt(psi.Discipline.TELEPATHY, dv=10, die=5, effort=2)
        self.assertEqual(p.effort_free, before - 2,
                         "Effort spent on an attempt must remain committed, not be returned")
        self.assertTrue(p.committed, "the commitment must be visible so it can be released")

    def test_the_commitment_can_be_released_by_its_label(self) -> None:
        p = _practitioner()
        before = p.effort_free
        attempt = p.attempt(psi.Discipline.TELEPATHY, dv=10, die=5, effort=1)
        self.assertEqual(attempt.effort_spent, 1)
        released = p.release(f"attempt:{psi.Discipline.TELEPATHY.value}")
        self.assertEqual(released, 1)
        self.assertEqual(p.effort_free, before)

    def test_an_attempt_cannot_overcommit(self) -> None:
        p = _practitioner()
        with self.assertRaises(psi.PsiError):
            p.attempt(psi.Discipline.TELEPATHY, dv=10, die=5, effort=p.capacity + 1)

    def test_a_failed_attempt_does_not_refund_the_effort(self) -> None:
        p = _practitioner()
        before = p.effort_free
        bad = p.attempt(psi.Discipline.TELEPATHY, dv=99, die=5, effort=1)
        self.assertIs(bad.outcome, psi.Outcome.FAILURE)
        self.assertEqual(p.effort_free, before - 1,
                         "failure must not hand the capacity back")


class NetworkEffectsActuallyApplyTests(unittest.TestCase):
    """Same bug class in the sibling module: a documented effect that never happened."""

    def _session(self, **kw):
        from src.rules import ubiquitous_network as net
        return net.IntrusionSession(target=net.ConnectivityClass.PUBLIC_GATEWAY,
                                    access=net.AccessClass.SAFENET,
                                    era=net.Era.ACCELERATION, **kw)

    def test_quiet_drops_the_margin_term(self) -> None:
        loud = self._session()
        quiet = self._session()
        a = loud.intrude(stat=10, skill_rating=1, dv=1, die=10)
        b = quiet.intrude(stat=10, skill_rating=1, dv=1, die=10, quiet=True)
        self.assertEqual(b.exposure_added, 1, "a quiet success costs only the base action")
        self.assertGreater(a.exposure_added, b.exposure_added)

    def test_a_failed_attempt_still_costs_more_than_a_quiet_success(self) -> None:
        session = self._session()
        quiet = session.intrude(stat=10, skill_rating=1, dv=1, die=10, quiet=True)
        failed = session.intrude(stat=1, skill_rating=1, dv=99, die=1)
        self.assertGreater(failed.exposure_added, quiet.exposure_added)

    def test_exit_is_always_available_even_with_no_ap_left(self) -> None:
        session = self._session()
        while session.ap > 0:
            session._spend()
        self.assertEqual(session.ap, 0)
        step = session.exit()  # must not raise: disengaging cannot be gated on AP
        self.assertEqual(step.action, "exit")
        self.assertEqual(session.ap, 0)


if __name__ == "__main__":
    unittest.main()
