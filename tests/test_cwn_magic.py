"""Magic in the city: mage Effort, preparation, casting and overcasting (#1068).

Source: CWN Deluxe printed pp. 231–236. The numbers are the ones the tables give — Effort from the better
of Int/Wis plus Cast, prepared slots from half the level plus Cast, the overcasting bands — and the
book's own worked example (three implants at strain 2, 0 and 0.5 costing four points of Effort) is a
test, because it is the one place where the wording could be read two ways.
"""
import unittest

from src.rules.cwn_magic import (
    GRIMOIRE_COST,
    TUTOR_COST,
    Commitment,
    Mage,
    MagicError,
    cyber_effort_penalty,
    mage_effort_max,
    overcast_result,
    prepared_slots,
    summoner_effort_max,
    summoner_spirit_binding,
)


def mage(level=1, cast=1, int_mod=1, wis_mod=0, known=("blast", "stun"), **kwargs) -> Mage:
    return Mage(level=level, cast_skill=cast, int_mod=int_mod, wis_mod=wis_mod,
                known=list(known), **kwargs)


class EffortTests(unittest.TestCase):
    def test_better_of_intelligence_or_wisdom_plus_cast(self):
        self.assertEqual(mage_effort_max(2, 1, 3), 5, "Int +2 beats Wis +1, then Cast-3")
        self.assertEqual(mage_effort_max(0, 2, 1), 3)

    def test_the_pool_never_drops_below_one(self):
        self.assertEqual(mage_effort_max(-2, -1, 0), 1)

    def test_cyberware_cuts_the_pool_and_trivial_mods_still_cost_a_point(self):
        # The book's own example: three implants at strain 2, 0 and 0.5 cost four points of Effort.
        self.assertEqual(cyber_effort_penalty([2, 0, 0.5]), 4)
        self.assertEqual(mage_effort_max(2, 1, 3, cyber_strain_costs=[2, 0, 0.5]), 1,
                         "5 base minus 4, floored at the minimum of one")
        self.assertEqual(mage_effort_max(2, 1, 6, cyber_strain_costs=[2, 0, 0.5]), 4)

    def test_a_mage_with_no_cyberware_loses_nothing(self):
        self.assertEqual(mage_effort_max(1, 1, 2), 3)

    def test_summoners_use_the_better_of_constitution_or_charisma(self):
        self.assertEqual(summoner_effort_max(0, 3, 2), 5)
        self.assertEqual(summoner_effort_max(-1, -1, 0), 1)
        with self.assertRaises(MagicError):
            summoner_effort_max(0, 0, -1)


class PreparationTests(unittest.TestCase):
    def test_slots_are_half_level_rounded_up_plus_cast(self):
        self.assertEqual(prepared_slots(1, 1), 2, "the book's first-level example")
        self.assertEqual(prepared_slots(10, 4), 9, "the book's tenth-level master example")

    def test_preparing_more_than_the_slots_is_refused(self):
        caster = mage(level=1, cast=1, known=("blast", "stun", "cloak"))
        with self.assertRaises(MagicError):
            caster.prepare(["blast", "stun", "cloak"])

    def test_only_learned_spells_can_be_prepared(self):
        caster = mage(level=4, cast=1)
        with self.assertRaises(MagicError):
            caster.prepare(["arson"])

    def test_learning_costs_a_week_and_the_book_prices_are_recorded(self):
        caster = mage()
        caster.learn("arson")
        self.assertIn("arson", caster.known)
        with self.assertRaises(MagicError):
            caster.learn("arson")
        self.assertEqual((TUTOR_COST, GRIMOIRE_COST), (5000, 10000))


class CastingTests(unittest.TestCase):
    def test_casting_commits_one_effort_for_the_stated_duration(self):
        caster = mage(level=2, cast=2)
        caster.prepare(["blast"])
        result = caster.cast("blast", Commitment.DAY)
        self.assertEqual((result["effort"], result["commitment"]), (1, "day"))
        self.assertEqual(caster.committed_total, 1)

    def test_scene_and_duration_commitments_recover_differently(self):
        caster = mage(level=2, cast=2)
        caster.prepare(["blast", "stun"])
        caster.cast("blast", Commitment.SCENE)
        caster.cast("stun", Commitment.DURATION)
        self.assertEqual(caster.effort_free, caster.effort_max - 2)
        self.assertEqual(caster.reclaim_duration(), 1, "duration Effort is reclaimable at will")
        self.assertEqual(caster.end_scene(), 1, "scene Effort returns when the scene ends")
        self.assertEqual(caster.committed_total, 0)

    def test_a_restrained_or_grappled_caster_cannot_cast(self):
        caster = mage()
        caster.prepare(["blast"])
        with self.assertRaises(MagicError):
            caster.cast("blast", Commitment.SCENE, check={"disturbed": True})
        with self.assertRaises(MagicError):
            caster.cast("blast", Commitment.SCENE, check={"hands_free": False})

    def test_unprepared_spells_cannot_be_cast(self):
        caster = mage()
        with self.assertRaises(MagicError):
            caster.cast("blast", Commitment.SCENE)

    def test_casting_beyond_the_pool_is_refused(self):
        caster = mage(level=2, cast=1, int_mod=0, wis_mod=0)  # maximum 1
        caster.prepare(["blast"])
        caster.cast("blast", Commitment.DAY)
        with self.assertRaises(MagicError):
            caster.cast("blast", Commitment.DAY)

    def test_a_struck_caster_loses_the_spell_and_the_effort(self):
        caster = mage()
        caster.prepare(["blast"])
        self.assertEqual(caster.struck_while_casting(), {"spell_lost": True, "effort_wasted": True})

    def test_only_a_full_night_refreshes_the_pool(self):
        caster = mage(level=2, cast=2)
        caster.prepare(["blast"])
        caster.cast("blast", Commitment.DAY)
        with self.assertRaises(MagicError):
            caster.refresh(rested=False)
        self.assertEqual(caster.refresh(rested=True), caster.effort_max)
        self.assertEqual(caster.committed_total, 0)


class OvercastingTests(unittest.TestCase):
    def test_the_table_bands_match_the_book(self):
        self.assertEqual(overcast_result(1)["consequence"], "death")
        self.assertEqual(overcast_result(2)["consequence"], "mortal_wound")
        self.assertEqual(overcast_result(4)["consequence"], "mortal_wound")
        self.assertEqual(overcast_result(5)["consequence"], "unconscious_minute_4_strain")
        self.assertEqual(overcast_result(8)["strain"], 4)
        self.assertEqual(overcast_result(9)["consequence"], "stunned_2_strain")
        self.assertEqual(overcast_result(15)["strain"], 2)
        self.assertEqual(overcast_result(16)["consequence"], "lost_main_action_1_strain")
        self.assertEqual(overcast_result(19)["strain"], 1)
        self.assertEqual(overcast_result(20)["consequence"], "1_strain")
        self.assertEqual(overcast_result(40)["consequence"], "1_strain", "20+ is open-ended")

    def test_cast_and_constitution_are_added_and_day_commitment_subtracts_two(self):
        caster = mage(cast=2, con_mod=1)
        scene = caster.overcast_roll(10)
        day = caster.overcast_roll(10, day_commitment=True)
        self.assertEqual((scene["total"], day["total"]), (13, 11))
        self.assertEqual(day["strain"], 2, "11 lands in the 9–15 band")

    def test_overcasting_costs_no_effort_but_expires_after_the_scene(self):
        caster = mage(level=2, cast=1, int_mod=0, wis_mod=0)
        caster.prepare(["blast"])
        result = caster.cast("blast", Commitment.DAY, overcast=True)
        self.assertEqual(result["effort"], 0)
        self.assertEqual(result["commitment"], Commitment.SCENE.value,
                         "a duration-committed spell overcast lasts one scene")

    def test_an_overcast_roll_outside_the_d20_is_refused(self):
        with self.assertRaises(MagicError):
            mage().overcast_roll(0)


class SummonerTests(unittest.TestCase):
    def test_bound_effort_recovers_only_after_the_spirit_is_dispelled(self):
        binding = summoner_spirit_binding(effort=2)
        self.assertEqual(binding["effort_bound"], 2)
        self.assertTrue(binding["dismissed_but_bound_still_drains"])
        with self.assertRaises(MagicError):
            summoner_spirit_binding(effort=0)


class CoreIndependenceTests(unittest.TestCase):
    def test_the_module_imports_nothing_from_the_immutable_core(self):
        """Magic is an optional overlay: if it imported the combat or equipment rules it would be a fork."""
        import inspect

        import src.rules.cwn_magic as module

        source = inspect.getsource(module)
        self.assertNotIn("from .cwn_combat", source)
        self.assertNotIn("from .cwn_equipment", source)
        self.assertNotIn("from .cwn_character", source)


if __name__ == "__main__":
    unittest.main()
