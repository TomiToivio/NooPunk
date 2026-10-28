"""The anomaly gate (#704): a case cannot conclude 'anomalous' while a core test is unrun.

Stdlib unittest only — NoöPunk's CI has no pytest.
"""

from __future__ import annotations

import unittest

from src.rules.anomaly_gate import Dossier, GateError, Readings
from src.rules.investigation import Case, Clue, ClueKind, Scene


def scene(sid: str, cid: str) -> Scene:
    return Scene(
        id=sid,
        title=sid.title(),
        clues=(
            Clue(id=cid, scene_id=sid, kind=ClueKind.CORE, competency="Forensics", fact=f"fact {cid}"),
        ),
    )


def ward_case() -> Case:
    case = Case(id="lakkahaltia", scenes=(scene("intake", "C1"), scene("morgue", "C3")))
    case.validate()
    return case


def dossier() -> Dossier:
    d = Dossier(case=ward_case())
    d.declare("C1", mundane="a template artefact", anomalous="precognitive files",
              discriminator="compare template deployment date to file timestamps")
    d.declare("C3", mundane="the body was moved after death", anomalous="placed by someone",
              discriminator="lividity and ambient temperature log")
    return d


class TestDeclarations(unittest.TestCase):
    def test_a_clue_needs_both_readings_and_a_test(self):
        for field in ("mundane", "anomalous", "discriminator"):
            kwargs = {"mundane": "a", "anomalous": "b", "discriminator": "c"}
            kwargs[field] = "  "
            with self.assertRaises(GateError):
                Readings("C1", **kwargs)

    def test_identical_readings_are_refused(self):
        # One reading dressed twice does not preserve uncertainty.
        with self.assertRaises(GateError):
            Readings("C1", mundane="a bug", anomalous="a bug", discriminator="check the log")

    def test_declaring_an_unknown_clue_is_refused(self):
        with self.assertRaises(GateError):
            dossier().declare("NOPE", mundane="a", anomalous="b", discriminator="c")

    def test_every_core_clue_must_be_declared_before_play(self):
        d = Dossier(case=ward_case())
        d.declare("C1", mundane="a", anomalous="b", discriminator="c")
        self.assertEqual(d.undeclared_core(), ("C3",))
        with self.assertRaises(GateError):
            d.validate()

    def test_a_fully_declared_dossier_validates(self):
        dossier().validate()


class TestTheGate(unittest.TestCase):
    def setUp(self):
        self.d = dossier()

    def test_the_gate_starts_closed(self):
        self.assertFalse(self.d.gate_open())
        self.assertEqual(self.d.untested_core(), ("C1", "C3"))

    def test_one_attempt_does_not_open_it(self):
        self.d.attempt("C1")
        self.assertFalse(self.d.gate_open())
        self.assertFalse(self.d.may_conclude_anomalous())

    def test_attempting_every_core_clue_opens_it(self):
        self.d.attempt("C1")
        self.d.attempt("C3")
        self.assertTrue(self.d.gate_open())
        self.assertTrue(self.d.may_conclude_anomalous())

    def test_require_open_names_what_is_missing(self):
        self.d.attempt("C1")
        with self.assertRaises(GateError) as ctx:
            self.d.require_open()
        self.assertIn("C3", str(ctx.exception))
        self.assertNotIn("C1", str(ctx.exception))

    def test_attempt_returns_the_declared_test(self):
        self.assertEqual(self.d.attempt("C3"), "lividity and ambient temperature log")

    def test_attempting_an_undeclared_clue_is_refused(self):
        with self.assertRaises(GateError):
            self.d.attempt("C3x")


class TestResolution(unittest.TestCase):
    def setUp(self):
        self.d = dossier()

    def test_a_test_cannot_resolve_before_it_is_attempted(self):
        with self.assertRaises(GateError):
            self.d.resolve("C1", anomalous=True)

    def test_resolution_is_recorded_after_the_attempt(self):
        self.d.attempt("C1")
        self.d.resolve("C1", anomalous=False)
        self.assertEqual(self.d.resolved, {"C1": "mundane"})

    def test_the_tally_counts_and_does_not_judge(self):
        self.d.attempt("C1")
        self.d.resolve("C1", anomalous=False)
        tally = self.d.tally()
        self.assertEqual(tally["attempted"], 1)
        self.assertEqual(tally["resolved_mundane"], 1)
        self.assertEqual(tally["resolved_anomalous"], 0)
        self.assertEqual(tally["outstanding"], 1)
        self.assertNotIn("verdict", tally)


if __name__ == "__main__":
    unittest.main()
