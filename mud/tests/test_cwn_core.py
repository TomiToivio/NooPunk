"""CWN core port (#950): boundaries and deterministic resolution."""
from __future__ import annotations

import random

import pytest

from nopunk_mud import cwn_core as cwn


class TestAttributes:
    @pytest.mark.parametrize("score,want", [(3, -2), (4, -1), (7, -1), (8, 0),
                                            (13, 0), (14, 1), (17, 1), (18, 2)])
    def test_modifier_boundaries(self, score, want):
        assert cwn.attribute_modifier(score) == want

    def test_out_of_range_is_refused(self):
        for score in (2, 19):
            with pytest.raises(ValueError):
                cwn.attribute_modifier(score)

    def test_3d6_down_the_line_is_seeded(self):
        first = cwn.roll_attributes(random.Random(950))
        second = cwn.roll_attributes(random.Random(950))
        assert first == second
        assert set(first) == set(cwn.ATTRIBUTES)
        assert all(3 <= value <= 18 for value in first.values())

    def test_array_assignment(self):
        scores = cwn.assign_array()
        assert scores["STR"] == 14 and scores["CHA"] == 7
        assert cwn.assign_array([3, 4, 5, 6, 7, 8])["CON"] == 5

    def test_array_rejects_wrong_shape(self):
        with pytest.raises(ValueError):
            cwn.assign_array([10, 10, 10])


class TestDerived:
    def test_hit_points_max_first_die_and_con_modifier(self):
        assert cwn.hit_points(1, 14) == 7       # 6 + 1
        assert cwn.hit_points(2, 10, [6, 3]) == 9
        assert cwn.hit_points(2, 3, [1, 1]) == 1  # never below 1

    def test_save_target_uses_best_of_pair(self):
        scores = {"STR": 14, "DEX": 10, "CON": 10, "INT": 10, "WIS": 10, "CHA": 10}
        assert cwn.save_target(1, scores, "Physical") == 14
        assert cwn.save_target(3, scores, "Physical") == 12

    def test_unknown_save_category(self):
        with pytest.raises(ValueError):
            cwn.save_target(1, {name: 10 for name in cwn.ATTRIBUTES}, "Sanity")


class TestChecks:
    def test_skill_check_arithmetic(self):
        result = cwn.skill_check(1, 14, 8, dice=(4, 5))
        assert result.total == 4 + 5 + 1 + 1
        assert result.success

    def test_untrained_penalty(self):
        assert not cwn.skill_check(-1, 10, 8, dice=(3, 3)).success  # 6 - 1 = 5

    def test_illegal_inputs(self):
        for kwargs in ({"rank": 5}, {"rank": 0, "difficulty": 7}, {"rank": 0, "circumstances": 3}):
            with pytest.raises(ValueError):
                cwn.skill_check(**{"rank": 0, "attribute_score": 10, "difficulty": 8,
                                   "dice": (3, 3), **kwargs})

    def test_attack_hits_on_ac(self):
        attack = cwn.attack_roll(1, 14, 1, 13, die=10)
        assert attack.total == 10 + 1 + 1 + 1
        assert attack.hit

    def test_attack_misses_below_ac(self):
        assert not cwn.attack_roll(0, 10, 0, 15, die=5).hit


class TestDamageAndStrain:
    def test_damage_adds_attribute_modifier(self):
        result = cwn.damage(8, [5], 14)
        assert result["damage"] == 6

    def test_trauma_triggers_on_target(self):
        result = cwn.damage(8, [4], 10, trauma_die=10, trauma_roll=7, trauma_rating=2)
        assert result["trauma"] is True
        assert result["trauma_bonus_damage"] == 10  # 2 * (10 // 2)

    def test_trauma_miss_has_no_bonus(self):
        result = cwn.damage(8, [4], 10, trauma_die=10, trauma_roll=3)
        assert result["trauma"] is False and result["trauma_bonus_damage"] == 0

    def test_strain_absorbs_up_to_con(self):
        assert cwn.strain_absorb(2, 3, 12)["current"] == 5
        overflow = cwn.strain_absorb(11, 3, 12)
        assert overflow["ok"] is False and overflow["overflow"] == 2


class TestCatalogueAndActions:
    def test_weapon_and_armour_lookup(self):
        assert cwn.weapon("knife")["shock"] == {"damage": 1, "ac": 15}
        assert cwn.armour("ordinary_clothing")["ranged_ac"] == 10
        with pytest.raises(ValueError):
            cwn.weapon("plasma_banana")

    def test_shock_only_when_ac_is_low_enough(self):
        assert cwn.shock_on_miss("knife", 15) == 1
        assert cwn.shock_on_miss("knife", 16) == 0
        assert cwn.shock_on_miss("rifle", 10) == 0

    def test_action_modifiers(self):
        assert cwn.combat_action("snap")["to_hit"] == -4
        assert cwn.combat_action("charge")["to_hit"] == 2
        assert cwn.combat_action("total_defense")["immune_to_shock"] is True
        with pytest.raises(ValueError):
            cwn.combat_action("snap", main_unspent=False)

    def test_encumbrance_tiers(self):
        base = cwn.encumbrance(10, stowed=10, readied=5)
        assert base["fits"] and base["overload_steps"] == 0 and base["speed_metres"] == 10.0
        heavy = cwn.encumbrance(10, stowed=12, readied=5)
        assert heavy["overload_steps"] == 1 and heavy["speed_metres"] == 7.0
        over = cwn.encumbrance(10, stowed=15, readied=5)
        assert over["overload_steps"] == 2 and over["speed_metres"] == 5.0
        assert not cwn.encumbrance(10, stowed=19, readied=5)["fits"]

    def test_encumbrance_rejects_bad_input(self):
        with pytest.raises(ValueError):
            cwn.encumbrance(10, stowed=-1)
