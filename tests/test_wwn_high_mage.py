"""WWN High Mage as the NoöPunk hermetic PSI practitioner (#1044).

Every number here is checked against the Worlds Without Number SRD (CC0): the two Arts-and-Spells
tables, the Effort formula, preparation, the casting economy and the Arts' durations. The tests are
deliberately arithmetic — an off-by-one in "spells prepared" or a lost "minimum of one Effort" is the
kind of defect that only shows up three sessions into a campaign.
"""
import json
import unittest

from src.rules.wwn_high_mage import (
    ARTS,
    HIGH_MAGE_TABLE,
    PARTIAL_HIGH_MAGE_TABLE,
    POOL,
    Duration,
    HighMage,
    HighMageError,
    Spell,
    effort_max,
)


def mage(**kwargs) -> HighMage:
    defaults = {"level": 1, "magic_skill": 1, "intelligence_modifier": 1,
                "charisma_modifier": 0}
    defaults.update(kwargs)
    return HighMage(**defaults)


def spell(identifier: str, level: int = 1) -> Spell:
    return Spell(identifier, identifier.replace("_", " ").title(), level)


class TableTests(unittest.TestCase):
    def test_full_table_matches_the_srd_progression(self):
        self.assertEqual(HIGH_MAGE_TABLE[1], (1, 1, 3, 2))
        self.assertEqual(HIGH_MAGE_TABLE[5], (3, 3, 6, 0))
        self.assertEqual(HIGH_MAGE_TABLE[10], (5, 6, 12, 1))

    def test_partial_table_is_its_own_progression_not_a_halved_full_mage(self):
        self.assertEqual(PARTIAL_HIGH_MAGE_TABLE[1], (1, 1, 2, 1))
        self.assertEqual(PARTIAL_HIGH_MAGE_TABLE[10], (3, 4, 9, 0))
        partial, full = mage(level=5, partial=True), mage(level=5)
        self.assertEqual((partial.casts_per_day, partial.prepared_slots), (2, 5))
        self.assertEqual((full.casts_per_day, full.prepared_slots), (3, 6))

    def test_arts_accrue_with_level(self):
        self.assertEqual(mage(level=1).arts_allowed, 2)
        self.assertEqual(mage(level=2).arts_allowed, 3)
        self.assertEqual(mage(level=10).arts_allowed, 7)
        self.assertEqual(mage(level=1, partial=True).arts_allowed, 1)


class EffortTests(unittest.TestCase):
    def test_effort_formula(self):
        # 1 + Magic skill + best of Int/Cha
        self.assertEqual(effort_max(0, 0, 0), 1)
        self.assertEqual(effort_max(2, 1, 0), 4)
        self.assertEqual(effort_max(2, 0, 1), 4, "the better of Int or Cha counts, not both")
        self.assertEqual(effort_max(3, 2, 0), 6)

    def test_effort_never_falls_below_one(self):
        self.assertEqual(effort_max(0, -2, -2), 1)
        self.assertEqual(effort_max(0, -2, -2, partial=True), 1, "the partial penalty clamps too")

    def test_partial_high_mage_has_one_point_less(self):
        self.assertEqual(effort_max(2, 1, 0, partial=True), 3)

    def test_the_pool_is_the_high_mage_pool(self):
        self.assertEqual(POOL, "high_mage", "SWN psychic Effort is a separate pool and cannot pay for this")


class ArtsTests(unittest.TestCase):
    def test_committing_and_releasing_duration_effort(self):
        caster = mage(level=2, magic_skill=2)
        caster.add_art("sense_magic")
        self.assertIs(caster.commit("sense_magic"), Duration.DURATION)
        self.assertEqual(caster.effort_free, caster.effort - 1)
        self.assertTrue(caster.release("sense_magic"))
        self.assertEqual(caster.effort_free, caster.effort)

    def test_turn_and_day_effort_cannot_be_reclaimed_early(self):
        caster = mage(level=3, magic_skill=2)
        caster.add_art("arcane_lexicon")
        caster.commit("arcane_lexicon")
        with self.assertRaises(HighMageError):
            caster.release("arcane_lexicon")

        caster.end_turn()
        self.assertNotIn("arcane_lexicon", caster.committed, "Turn Effort returns at end of Turn")

    def test_day_effort_survives_the_turn_and_needs_a_rest(self):
        caster = mage(level=3, magic_skill=2)
        caster.add_art("empowered_sorcery")
        caster.commit("empowered_sorcery")
        caster.end_turn()
        self.assertIn("empowered_sorcery", caster.committed)
        caster.rest()
        self.assertEqual(caster.committed, {})

    def test_a_comfortless_rest_returns_nothing(self):
        caster = mage(level=3, magic_skill=2)
        caster.add_art("empowered_sorcery")
        caster.commit("empowered_sorcery")
        with self.assertRaises(HighMageError):
            caster.rest(comfortable=False)
        self.assertEqual(caster.effort_committed, 1)

    def test_no_effort_left_is_refused(self):
        caster = mage(level=1, magic_skill=0, intelligence_modifier=0)
        caster.add_art("sense_magic")
        caster.add_art("wizards_grandeur")
        caster.commit("sense_magic")
        with self.assertRaises(HighMageError):
            caster.commit("wizards_grandeur")

    def test_an_art_not_known_cannot_be_committed(self):
        caster = mage(level=4, magic_skill=2)
        caster.add_art("sense_magic")
        with self.assertRaises(HighMageError):
            caster.commit("counter_magic")

    def test_art_picks_are_capped_by_level(self):
        caster = mage(level=1)
        caster.add_art("sense_magic")
        caster.add_art("wizards_grandeur")
        with self.assertRaises(HighMageError):
            caster.add_art("arcane_lexicon")

    def test_once_per_day_art_is_enforced(self):
        caster = mage(level=4, magic_skill=3)
        caster.add_art("retain_sorcery")
        caster.learn(spell("spark"))
        caster.prepare(["spark"])
        self.assertTrue(caster.cast("spark", retain=True)["retained"])
        with self.assertRaises(HighMageError):
            caster.cast("spark", retain=True)

    def test_every_srd_art_is_present_and_typed(self):
        self.assertEqual(len(ARTS), 15)
        for art in ARTS.values():
            self.assertIsInstance(art.duration, Duration)
            self.assertTrue(art.note, f"{art.identifier} needs a paraphrase")


class CastingTests(unittest.TestCase):
    def setUp(self):
        self.caster = mage(level=3, magic_skill=1)
        self.caster.learn(spell("arcane_spark", 1))
        self.caster.learn(spell("ward_line", 2))

    def test_casting_spends_a_slot_and_respects_the_daily_limit(self):
        self.caster.prepare(["arcane_spark"])
        record = self.caster.cast("arcane_spark")
        self.assertEqual(record["castings_left"], self.caster.casts_per_day - 1)

        for _ in range(self.caster.casts_per_day - 1):
            self.caster.cast("arcane_spark")
        with self.assertRaises(HighMageError):
            self.caster.cast("arcane_spark")

    def test_an_unprepared_spell_cannot_be_cast(self):
        self.caster.prepare(["arcane_spark"])
        with self.assertRaises(HighMageError):
            self.caster.cast("ward_line")

    def test_a_spell_above_the_level_maximum_is_refused(self):
        low = mage(level=1, magic_skill=1)
        low.learn(spell("first_circle", 1))
        with self.assertRaises(HighMageError):
            low.learn(spell("fifth_circle", 5))

    def test_preparation_is_capped_by_slots(self):
        caster = mage(level=1, magic_skill=1)
        for index in range(4):
            caster.learn(spell(f"minor_{index}", 1))
        with self.assertRaises(HighMageError):
            caster.prepare([f"minor_{index}" for index in range(4)])
        self.assertEqual(len(caster.prepare([f"minor_{index}" for index in range(3)])), 3)

    def test_preparation_needs_a_nights_rest(self):
        self.caster.prepare(["arcane_spark"])
        with self.assertRaises(HighMageError):
            self.caster.prepare(["arcane_spark"])

    def test_armour_and_shields_block_casting(self):
        self.caster.prepare(["arcane_spark"])
        with self.assertRaises(HighMageError):
            self.caster.cast("arcane_spark", armored=True)
        with self.assertRaises(HighMageError):
            self.caster.cast("arcane_spark", shielded=True)

    def test_damage_in_the_round_spoils_the_cast(self):
        self.caster.prepare(["arcane_spark"])
        with self.assertRaises(HighMageError):
            self.caster.cast("arcane_spark", damaged_this_round=True)
        self.assertEqual(self.caster.casts_used, 0, "a spoiled cast does not burn the slot")

    def test_a_full_rest_restores_castings(self):
        self.caster.prepare(["arcane_spark"])
        self.caster.cast("arcane_spark")
        self.caster.rest()
        self.assertEqual(self.caster.casts_used, 0)


class PersistenceTests(unittest.TestCase):
    def test_snapshot_round_trips(self):
        caster = mage(level=4, magic_skill=2)
        caster.learn(spell("arcane_spark", 1))
        caster.prepare(["arcane_spark"])
        caster.add_art("sense_magic")
        caster.commit("sense_magic")
        caster.cast("arcane_spark")

        restored = HighMage.from_json(caster.to_json())
        self.assertEqual(restored.snapshot(), caster.snapshot())
        self.assertEqual(restored.effort_free, caster.effort_free)
        self.assertEqual(restored.casts_left, caster.casts_left)

    def test_unknown_schema_is_refused(self):
        with self.assertRaises(HighMageError):
            HighMage.from_json(json.dumps({"schema": 99}))


class ReskinTests(unittest.TestCase):
    def test_a_hermetic_practitioner_is_a_cwn_character_with_a_package(self):
        """The class is additive: the object carries no CWN skill, save or combat state."""
        state = mage().snapshot()
        self.assertEqual(
            set(state),
            {"schema", "level", "magic_skill", "intelligence_modifier", "charisma_modifier",
             "partial", "repertoire", "prepared", "arts", "casts_used", "committed", "rested",
             "once_used", "turn"},
        )


if __name__ == "__main__":
    unittest.main()
