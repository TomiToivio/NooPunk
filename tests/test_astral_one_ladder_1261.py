"""One ladder, two APIs: the data module and the body module must not drift (#1261).

Two agents landed the same rank ladder within an hour of each other: a data-driven one
(`astral_progression`) and a behavioural one (`astral_body.AstralSkill`). Both are useful — the first owns the
table and the gates, the second owns what a projected body may do — but a second copy of the numbers is how
a rulebook and its code start disagreeing. These tests pin the derivation.
"""
import unittest

from src.rules.astral_body import MVP_RANKS, PROVISIONAL_MINUTES, AstralRank, AstralSkill
from src.rules.astral_progression import duration_cap_minutes, mvp_max_rank, rank_of, ranks


class DerivedTableTests(unittest.TestCase):
    def test_mvp_ranks_come_from_the_table(self):
        self.assertEqual(tuple(int(rank) for rank in MVP_RANKS), tuple(range(0, mvp_max_rank() + 1)))

    def test_provisional_minutes_are_the_table_values(self):
        for rank in AstralRank:
            with self.subTest(rank=rank.name):
                self.assertEqual(PROVISIONAL_MINUTES[rank], duration_cap_minutes(int(rank)))

    def test_plane_access_agrees_with_the_table(self):
        for rank in AstralRank:
            with self.subTest(rank=rank.name):
                self.assertEqual(
                    set(AstralSkill(rank).planes()), set(rank_of(int(rank)).planes),
                    f"{rank.name}: the body module and the rank table disagree about planes",
                )

    def test_capabilities_agree_with_the_table(self):
        for rank in AstralRank:
            row = rank_of(int(rank))
            skill = AstralSkill(rank)
            with self.subTest(rank=rank.name):
                self.assertEqual(skill.can_fly, row.flight)
                self.assertEqual(skill.can_enter_lower_astral, row.lower_astral)
                self.assertEqual(skill.can_send_rote, row.rote)
                self.assertEqual(skill.can_learn_ident, row.ident_learn)
                self.assertEqual(skill.can_use_ident, row.ident_use)

    def test_the_enums_and_the_table_describe_the_same_five_ranks(self):
        expected = {
            0: "Disorientation",
            1: "Lucidity and dream navigation",
            2: "Conscious Agent Network",
            3: "Authorised informational agency",
            4: "Cosmological research",
        }
        for value, name in expected.items():
            with self.subTest(rank=value):
                self.assertEqual(rank_of(value).name, name)
                self.assertEqual(int(AstralRank(value)), value)


class OneWindowTests(unittest.TestCase):
    def test_character_creation_and_the_gate_agree(self):
        from src.rules.astral_body import AstralBodyError
        from src.rules.astral_progression import AstralProgressionError, require_starting_rank

        for rank in range(5):
            with self.subTest(rank=rank):
                if rank <= mvp_max_rank():
                    AstralSkill.starting(rank)
                    require_starting_rank(rank)
                else:
                    with self.assertRaises(AstralBodyError):
                        AstralSkill.starting(rank)
                    with self.assertRaises(AstralProgressionError):
                        require_starting_rank(rank)

    def test_every_rank_in_the_table_has_a_body_enum_member(self):
        self.assertEqual({int(rank) for rank in AstralRank}, set(ranks()))


if __name__ == "__main__":
    unittest.main()
