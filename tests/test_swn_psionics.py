"""SWN Effort resource tests; mechanics are tested without copying technique text."""
import unittest

from src.rules.swn_psionics import Psychic, Duration, PsiRulesError, DISCIPLINES


def test_six_disciplines_and_effort_formula():
    assert len(DISCIPLINES) == 6
    p = Psychic(wisdom=9, constitution=18, disciplines={"Telepathy": 1, "Precognition": 0})
    assert p.capacity == 4  # one + CON modifier two + rank one


def test_scene_day_and_active_commitments_do_not_refund_early():
    p = Psychic(wisdom=14, constitution=10, disciplines={"Telepathy": 1})
    p.commit("contact", "Telepathy", duration=Duration.ACTIVE)
    p.commit("insight", "Telepathy", duration=Duration.SCENE)
    p.commit("vision", "Telepathy", duration=Duration.DAY)
    assert p.free == 0
    with unittest.TestCase().assertRaises(PsiRulesError):
        p.release("vision")
    with unittest.TestCase().assertRaises(PsiRulesError):
        p.commit("extra", "Telepathy")
    assert p.release("contact")
    assert p.free == 1
    p.end_scene()
    assert p.free == 2
    p.rest()
    assert p.free == p.capacity


def test_skill_access_and_duplicate_technique_key():
    p = Psychic(12, 12, {"Telepathy": 0})
    with unittest.TestCase().assertRaises(PsiRulesError):
        p.commit("unlearned", "Precognition")
    with unittest.TestCase().assertRaises(PsiRulesError):
        p.commit("advanced", "Telepathy", minimum_rank=1)
    p.commit("contact", "Telepathy")
    with unittest.TestCase().assertRaises(PsiRulesError):
        p.commit("contact", "Telepathy")


def test_snapshot_recovery_preserves_committed_effort():
    p = Psychic(14, 10, {"Precognition": 1}, {"swn_partial_psychic"})
    p.commit("oracle", "Precognition", duration=Duration.DAY)
    restored = Psychic.from_snapshot(p.snapshot())
    assert restored.snapshot() == p.snapshot()
    assert restored.free == p.free
    restored.end_scene()
    assert restored.free == p.free
    restored.rest()
    assert restored.free == restored.capacity


def test_reject_malformed_restores_and_scores():
    with unittest.TestCase().assertRaises(ValueError):
        Psychic(2, 10, {})
    with unittest.TestCase().assertRaises(PsiRulesError):
        Psychic(12, 12, {"Unknown": 1})
    p = Psychic(12, 12, {"Telepathy": 0})
    state = p.snapshot()
    state["reservations"] = {"bad": {"amount": 99, "duration": "day"}}
    with unittest.TestCase().assertRaises(PsiRulesError):
        Psychic.from_snapshot(state)
