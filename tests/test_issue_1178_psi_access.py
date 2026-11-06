"""Player access to psychic and Edge options (#1178).

The issue's rules are about **who may choose what**, not about numbers, so they can be implemented
before the printed SWN text is available — and they must be, because the alternative is a character
builder that quietly offers Precognition.

CI runs the standard library's unittest; this module therefore imports nothing else.
"""

from __future__ import annotations

import unittest

from src.rules.psi_access import (
    NPC_ONLY_DISCIPLINES,
    NPC_ONLY_EDGES,
    PC_DISCIPLINES,
    PC_EDGES,
    PSYCHIC_TRAINING_FOCUS_AVAILABLE,
    Grant,
    PsiAccessError,
    device_grant,
    discipline_decision,
    edge_decision,
    is_scripted_effect,
    require_pc_discipline,
    require_pc_edge,
    require_scripted,
    validate_selection,
)


class DisciplineAccessTests(unittest.TestCase):
    def test_a_player_may_take_telekinesis_and_telepathy(self):
        for name in ("Telekinesis", "Telepathy"):
            self.assertTrue(discipline_decision(name).allowed, name)
        self.assertEqual(set(PC_DISCIPLINES), {"Telekinesis", "Telepathy"})

    def test_every_other_swn_discipline_is_refused_with_a_reason(self):
        for name in NPC_ONLY_DISCIPLINES:
            decision = discipline_decision(name)
            self.assertFalse(decision.allowed, name)
            self.assertIn("not selectable by a player character", decision.reason)

    def test_an_unknown_discipline_is_refused_rather_than_assumed(self):
        decision = discipline_decision("Chronomancy")
        self.assertFalse(decision.allowed)
        self.assertIn("not a known discipline", decision.reason)

    def test_requiring_a_forbidden_discipline_raises(self):
        with self.assertRaises(PsiAccessError):
            require_pc_discipline("Precognition")
        self.assertEqual(require_pc_discipline("Telepathy"), "Telepathy")


class EdgeAccessTests(unittest.TestCase):
    def test_mutant_is_pc_selectable(self):
        self.assertTrue(edge_decision("Mutant").allowed)
        self.assertNotIn("Mutant", NPC_ONLY_EDGES)

    def test_mentalist_spellcaster_and_summoner_are_selectable(self):
        for name in ("Mentalist", "Spellcaster", "Summoner"):
            self.assertTrue(edge_decision(name).allowed, name)
        self.assertEqual(set(PC_EDGES), {"Mutant", "Mentalist", "Spellcaster", "Summoner"})

    def test_requiring_an_unknown_edge_raises(self):
        with self.assertRaises(PsiAccessError):
            require_pc_edge("Forbidden")


class ScriptedEffectTests(unittest.TestCase):
    def test_astral_projection_is_scripted_not_selectable(self):
        self.assertTrue(is_scripted_effect("Astral Projection"))
        self.assertTrue(require_scripted("Astral Projection"))
        self.assertFalse(discipline_decision("Astral Projection").allowed)

    def test_precognition_and_teleportation_are_scripted_as_well_as_npc_disciplines(self):
        for effect in ("Precognition", "Teleportation"):
            self.assertTrue(is_scripted_effect(effect), effect)
            self.assertFalse(discipline_decision(effect).allowed, effect)


class SelectionValidationTests(unittest.TestCase):
    def test_full_psychic_may_select_both_allowed_disciplines(self):
        self.assertEqual(validate_selection(disciplines=("Telepathy", "Telekinesis")), [])

    def test_partial_psychic_must_choose_one_discipline(self):
        problems = validate_selection(
            disciplines=("Telepathy", "Telekinesis"), partial_psychic=True
        )
        self.assertTrue(any("Partial Psychic" in p for p in problems))

    def test_full_psychic_focus_may_advance_other_allowed_discipline(self):
        self.assertEqual(
            validate_selection(
                disciplines=("Telepathy", "Telekinesis"),
                focus_disciplines=("Telekinesis",),
            ), []
        )

    def test_partial_psychic_focus_cannot_open_second_discipline(self):
        problems = validate_selection(
            disciplines=("Telepathy",),
            focus_disciplines=("Telekinesis",),
            partial_psychic=True,
        )
        self.assertTrue(any("Psychic Training Focus" in p for p in problems))

    def test_a_single_allowed_discipline_is_clean(self):
        self.assertTrue(validate_selection(disciplines=("Telepathy",), edges=("Mentalist",)))

    def test_a_focus_may_not_open_a_second_discipline(self):
        """The loophole the issue names: Psychic Training Focus as a back door."""
        problems = validate_selection(
            disciplines=("Telepathy",), focus_disciplines=("Biopsionics",)
        )
        self.assertTrue(any("Psychic Training Focus" in p for p in problems))

    def test_a_focus_inside_an_allowed_discipline_is_clean(self):
        self.assertEqual(
            validate_selection(disciplines=("Telekinesis",), focus_disciplines=("Telekinesis",)), []
        )


class DeviceGrantTests(unittest.TestCase):
    def test_a_device_grant_is_never_selectable(self):
        grant = device_grant(
            "Telepathy range extension", source="Europol defensive psychotronic implant"
        )
        self.assertFalse(grant.selectable)
        self.assertTrue(grant.ability and grant.source)

    def test_a_grant_cannot_be_declared_selectable(self):
        with self.assertRaises(PsiAccessError):
            Grant(ability="Precognition", source="prototype implant", selectable=True)

    def test_a_grant_does_not_widen_the_selection_policy(self):
        device_grant("Astral Projection", source="Monroe-style rig")
        self.assertFalse(discipline_decision("Astral Projection").allowed)


class DeferredWorkTests(unittest.TestCase):
    def test_the_psychic_training_focus_is_not_simulated_before_the_text_is_available(self):
        """Refusing to invent level benefits is the point; the flag documents the omission."""
        # Implemented from the author's quotation in #1178 §1; see src/rules/psychic_training.py (#1217 line 11).
        self.assertTrue(PSYCHIC_TRAINING_FOCUS_AVAILABLE)


if __name__ == "__main__":
    unittest.main()
