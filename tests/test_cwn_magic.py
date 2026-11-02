"""Magic in the city: Effort, preparation, casting and overcasting (#1068).

Source: CWN Deluxe printed pp. 231–236. The numbers are the ones the tables give; the book's own worked
examples are tests, because they are where a plausible-looking implementation goes wrong.
"""
import unittest

from src.rules.cwn_magic import (
    COMMITMENTS,
    GRIMOIRE_COST,
    TUTOR_COST,
    EffortPool,
    MagicError,
    Spellbook,
    can_cast,
    cyberware_penalty,
    mage_effort,
    overcast_result,
    prepared_slots,
    summoner_effort,
)


class EffortTests(unittest.TestCase):
    def test_better_mental_modifier_plus_cast(self):
        self.assertEqual(mage_effort(intelligence=14, wisdom=8, cast_skill=1), 2)
        self.assertEqual(mage_effort(intelligence=8, wisdom=17, cast_skill=2), 3)

    def test_the_pool_never_drops_below_one(self):
        self.assertEqual(mage_effort(intelligence=3, wisdom=3, cast_skill=0), 1)

    def test_each_implant_costs_its_strain_and_at_least_one_point(self):
        # The book's example: implants at 2, 0 and 0.5 cost four points of maximum Effort.
        self.assertEqual(cyberware_penalty([2, 0, 0.5]), 4)
        base = mage_effort(intelligence=18, wisdom=9, cast_skill=3)
        self.assertEqual(mage_effort(intelligence=18, wisdom=9, cast_skill=3, strain_costs=[2, 0, 0.5]),
                         max(1, base - 4), "base minus four points of chrome")
        self.assertEqual(mage_effort(intelligence=3, wisdom=3, cast_skill=0, strain_costs=[5]), 1)

    def test_negative_strain_is_refused(self):
        with self.assertRaises(MagicError):
            cyberware_penalty([-1])

    def test_summoners_use_constitution_or_charisma(self):
        self.assertEqual(summoner_effort(constitution=14, charisma=8, summon_skill=1), 2)
        self.assertEqual(summoner_effort(constitution=8, charisma=17, summon_skill=2), 3)
        self.assertEqual(summoner_effort(constitution=3, charisma=3, summon_skill=0), 1)


class PreparationTests(unittest.TestCase):
    def test_slots_are_half_level_rounded_up_plus_cast(self):
        self.assertEqual(prepared_slots(1, 1), 2, "the book's first-level example")
        self.assertEqual(prepared_slots(10, 4), 9, "the book's tenth-level master example")

    def test_only_learned_spells_can_be_prepared(self):
        book = Spellbook(level=4, cast_skill=1, known=["blast"])
        with self.assertRaises(MagicError):
            book.prepare(["arson"])

    def test_preparing_beyond_the_slots_is_refused(self):
        book = Spellbook(level=1, cast_skill=1, known=["blast", "stun", "cloak"])
        with self.assertRaises(MagicError):
            book.prepare(["blast", "stun", "cloak"])
        book.prepare(["blast", "stun"])
        self.assertEqual(book.prepared, ["blast", "stun"])

    def test_a_spell_is_learned_once_and_the_book_prices_are_recorded(self):
        book = Spellbook(level=2, cast_skill=1)
        book.learn("blast")
        with self.assertRaises(MagicError):
            book.learn("blast")
        self.assertEqual((TUTOR_COST, GRIMOIRE_COST), (5000, 10000))


class CastingTests(unittest.TestCase):
    def test_a_cast_commits_one_effort_for_its_duration(self):
        book = Spellbook(level=2, cast_skill=2, known=["blast"], prepared=["blast"])
        pool = EffortPool(maximum=3)
        result = book.cast("blast", pool, duration="day")
        self.assertEqual((result["effort"], result["commitment"]), (1, "day"))
        self.assertEqual(pool.available, 2)

    def test_the_three_commitments_recover_differently(self):
        pool = EffortPool(maximum=4)
        pool.commit(1, duration="day")
        pool.commit(1, duration="scene")
        pool.commit(1, duration="duration")
        self.assertEqual(pool.reclaim_duration(), 1, "duration Effort is reclaimable at will")
        self.assertEqual(pool.end_scene(), 1, "scene Effort returns when the scene ends")
        self.assertFalse(pool.refresh_morning(slept_eight_hours=False), "day Effort needs the night")
        self.assertTrue(pool.refresh_morning())
        self.assertEqual(pool.available, 4)
        self.assertEqual(set(pool.committed), set(COMMITMENTS))

    def test_casting_needs_a_free_hand_a_voice_and_a_steady_round(self):
        self.assertTrue(can_cast(free_hand=True, can_speak=True))
        self.assertFalse(can_cast(free_hand=False, can_speak=True))
        self.assertFalse(can_cast(free_hand=True, can_speak=False))
        self.assertFalse(can_cast(free_hand=True, can_speak=True, disturbed=True),
                         "damage or a grapple in the round spoils the cast")

    def test_unprepared_spells_cannot_be_cast(self):
        book = Spellbook(level=2, cast_skill=1, known=["blast"])
        with self.assertRaises(MagicError):
            book.cast("blast", EffortPool(maximum=2))

    def test_an_exhausted_pool_refuses_the_cast(self):
        book = Spellbook(level=2, cast_skill=1, known=["blast"], prepared=["blast"])
        pool = EffortPool(maximum=1)
        book.cast("blast", pool, duration="day")
        with self.assertRaises(MagicError):
            book.cast("blast", pool, duration="day")

    def test_a_pool_cannot_commit_more_than_it_holds(self):
        pool = EffortPool(maximum=2)
        with self.assertRaises(MagicError):
            pool.commit(3, duration="scene")


class OvercastingTests(unittest.TestCase):
    def test_the_bands_match_the_book(self):
        expected = {1: "death", 2: "mortal_wound", 4: "mortal_wound", 5: "unconscious_minute_4_strain",
                    8: "unconscious_minute_4_strain", 9: "stunned_2_strain", 15: "stunned_2_strain",
                    16: "lost_main_action_1_strain", 19: "lost_main_action_1_strain", 20: "1_strain",
                    35: "1_strain"}
        for total, consequence in expected.items():
            self.assertEqual(overcast_result(total)["consequence"], consequence, total)
        self.assertEqual(overcast_result(8)["strain"], 4)

    def test_cast_and_constitution_are_added_and_day_commitment_subtracts_two(self):
        pool = EffortPool(maximum=3)
        scene = pool.overcast_roll(10, cast_skill=2, constitution_mod=1)
        day = pool.overcast_roll(10, cast_skill=2, constitution_mod=1, day_commitment=True)
        self.assertEqual((scene["total"], day["total"]), (13, 11))
        self.assertEqual(day["strain"], 2)

    def test_an_overcast_spell_costs_no_effort_and_lasts_one_scene(self):
        book = Spellbook(level=2, cast_skill=1, known=["blast"], prepared=["blast"])
        pool = EffortPool(maximum=1)
        result = book.cast("blast", pool, duration="day", overcast=True)
        self.assertEqual(result["effort"], 0)
        self.assertEqual(result["commitment"], "scene")
        self.assertEqual(pool.available, 1, "overcasting does not touch the pool")

    def test_a_roll_outside_the_d20_is_refused(self):
        with self.assertRaises(MagicError):
            EffortPool(maximum=2).overcast_roll(0)


class CoreIndependenceTests(unittest.TestCase):
    def test_magic_is_an_overlay_not_a_fork_of_the_core(self):
        import inspect

        import src.rules.cwn_magic as module

        source = inspect.getsource(module)
        self.assertNotIn("from .cwn_combat", source)
        self.assertNotIn("from .cwn_equipment", source)


if __name__ == "__main__":
    unittest.main()
