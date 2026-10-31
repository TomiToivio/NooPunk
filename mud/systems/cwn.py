"""CWN 2d6 skill-check slice. Not a replacement for the published rules."""
from dataclasses import dataclass
import random

@dataclass(frozen=True)
class CheckResult:
    dice: tuple[int, int]
    total: int
    difficulty: int
    success: bool

def skill_check(rank: int, attribute_modifier: int, difficulty: int = 8, rng=None) -> CheckResult:
    if not -1 <= rank <= 4 or not -3 <= attribute_modifier <= 3:
        raise ValueError("Unsupported skill rank or attribute modifier")
    if difficulty not in (6, 8, 10, 12, 14):
        raise ValueError("Unsupported CWN difficulty")
    rng = rng or random
    dice = (rng.randint(1, 6), rng.randint(1, 6))
    total = sum(dice) + rank + attribute_modifier
    return CheckResult(dice, total, difficulty, total >= difficulty)
