"""Rules examples grounded in Cities Without Number Deluxe, pp. 5-6 / 9-10."""
from systems.cwn import attribute_modifier, skill_check, save_target, SKILLS

class Dice:
    def __init__(self, *values):
        self.values = iter(values)
    def randint(self, lo, hi):
        return next(self.values)

def test_modifier_table():
    assert [attribute_modifier(x) for x in (3, 4, 7, 8, 13, 14, 17, 18)] == [-2, -1, -1, 0, 0, 1, 1, 2]

def test_untrained_skill_rank_minus_one():
    result = skill_check(-1, 1, 8, rng=Dice(3, 4))
    assert result.total == 7
    assert result.success is False

def test_difficulty_and_real_cwn_skill_vocabulary():
    assert len(SKILLS) == 19
    assert {"program", "notice", "shoot", "work", "heal"} <= set(SKILLS)
    assert skill_check(0, 0, 14, rng=Dice(6, 6)).success is False

def test_saves_cwn_level_and_better_attribute():
    assert save_target(1, "physical", {"strength": 14, "constitution": 8}) == 14
    assert save_target(3, "mental", {"wisdom": 3, "charisma": 18}) == 11
