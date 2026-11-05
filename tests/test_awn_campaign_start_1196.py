"""Regression checks for AWN Deluxe at campaign start (#1196)."""
import unittest

from src.rules.awn_mutant import MutantBuild, Mutation, MutationError
from src.rules.awn_mentalist import Art, MentalistError, create_first_level_mentalist
from src.rules.awn_campaign_start import (
    Addiction, AwnRulesError, Enclave, Pharmaceutical, foot_chase,
    moving_vehicle_attack_penalty, radiation_exposure, stress_engine,
    vehicle_chase, vehicle_combat_control,
)
from src.rules.psi_access import validate_selection
from src.rules.psi_edges import EdgeGrants, validate_edge


class MutantCreationTests(unittest.TestCase):
    def test_approved_europol_mutant_is_not_hybrid_or_psychic(self):
        build = MutantBuild("pc.rookie", True, "unusual eyes")
        self.assertFalse(build.alien_hybrid)
        self.assertFalse(build.psychic)
        self.assertEqual(build.mutation_points, 2)
        self.assertEqual(validate_selection(edges=("Mutant",)), [])

    def test_concealed_stigma_costs_one_point(self):
        self.assertEqual(MutantBuild("pc", True, "small mark", True).mutation_points, 1)

    def test_negative_roll_and_random_positive(self):
        build = MutantBuild("pc", True, "bright skin")
        build.add_negative(Mutation("published drawback", "negative", "negative", 18))
        build.add_positive(Mutation("published benefit", "positive", "sense", 21), method="random")
        self.assertEqual(build.mutation_points, 3)
        with self.assertRaises(MutationError):
            build.add_negative(Mutation("published drawback", "negative", "negative", 18))

    def test_unapproved_or_hybrid_rogue_not_rookie(self):
        with self.assertRaises(MutationError):
            MutantBuild("pc", False, "marked")
        with self.assertRaises(MutationError):
            MutantBuild("pc", True, "marked", alien_hybrid=True)

    def test_mentalist_is_selectable_but_not_with_psychic_or_summoner(self):
        self.assertEqual(validate_selection(edges=("Mentalist",)), [])
        self.assertTrue(validate_selection(edges=("Mentalist",), disciplines=("Telepathy",)))
        self.assertTrue(validate_selection(edges=("Mentalist", "Summoner")))
        self.assertTrue(validate_selection(edges=("Mentalist",), character_level=2))
        self.assertTrue(validate_edge(EdgeGrants("Mentalist"), existing=(EdgeGrants("Summoner"),)))


class CampaignRulesTests(unittest.TestCase):
    def test_radiation_and_overflow(self):
        ok = radiation_exposure(constitution=12, system_strain=1, max_strain=5,
                                physical_save_success=True, strain_roll=3)
        self.assertEqual(ok.system_strain, 4)
        overflow = radiation_exposure(constitution=12, system_strain=4, max_strain=5,
                                      physical_save_success=True, strain_roll=2,
                                      constitution_loss_roll=5)
        self.assertEqual(overflow.constitution, 7)

    def test_radiation_fatal(self):
        result = radiation_exposure(constitution=4, system_strain=0, max_strain=10,
                                    physical_save_success=False, constitution_loss_roll=3)
        self.assertTrue(result.fatal)

    def test_chase_tie_distinction(self):
        self.assertFalse(foot_chase(fleeing_check=10, pursuing_check=10).caught)
        self.assertTrue(vehicle_chase(fleeing_drive_check=6, fleeing_speed=3,
                                      pursuing_drive_check=7, pursuing_speed=2).caught)

    def test_vehicle_crash_and_attack_penalty(self):
        self.assertTrue(vehicle_combat_control(driver_spent_main_action=False,
                                               luck_save_success=False).crash)
        self.assertEqual(moving_vehicle_attack_penalty(
            unsecured_personal_weapon=True, moving=True), -4)

    def test_recovery_and_pharmaceuticals(self):
        addict = Addiction("fictional compound")
        self.assertFalse(addict.abstain_week(save_success=False))
        self.assertTrue(addict.abstain_week(save_success=True))
        self.assertEqual(Pharmaceutical("stim", True).application(heal_skill=0), "main_action")
        self.assertEqual(Pharmaceutical("antibiotic", False).application(heal_skill=0), "minute_or_two")

    def test_enclave_power_and_trouble(self):
        base = Enclave(name="Helsinki crisis shelter", power=2, trouble=2)
        self.assertEqual(base.action_die, 8)
        self.assertEqual(base.external_actions_per_turn, 2)
        self.assertTrue(base.trouble_check(2))
        self.assertFalse(base.trouble_check(3))
        base.gain_dominion(3)
        base.spend_dominion(2)
        self.assertEqual(base.dominion, 1)

    def test_mentalist_first_level_and_effort(self):
        m = create_first_level_mentalist("pc.rookie", (
            Art("lesser-a", "Mindreading"), Art("lesser-b", "Mindreading")))
        self.assertEqual(m.mentalism_skill, 0)
        self.assertEqual(len(m.arts), 2)
        self.assertEqual(m.effort_max, 1)
        m.commit(duration="scene")
        with self.assertRaises(MentalistError):
            m.commit(duration="day")
        m.end_scene()
        m.commit(duration="day")
        m.sleep(comfortable=False)
        self.assertEqual(m.effort_day, 1)
        m.sleep(comfortable=True)
        self.assertEqual(m.effort_day, 0)
        with self.assertRaises(MentalistError):
            m.check_cyberware(nerve_type=True)

    def test_existing_stress_implementation_is_reused(self):
        self.assertIsNotNone(stress_engine())


if __name__ == "__main__":
    unittest.main()
