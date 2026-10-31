"""Small source-backed CWN mechanics layer; not full rulebook coverage (#950).

CWN Deluxe, pp. 5-6 (attributes/skills), 30-31 (saves/checks).
"""
from dataclasses import dataclass
import random

SKILLS = frozenset(("administer connect drive exert fix heal know lead notice perform "
                    "program punch shoot sneak stab survive talk trade work").split())
ATTRIBUTES = ("strength", "dexterity", "constitution", "intelligence", "wisdom", "charisma")

def attribute_modifier(score: int) -> int:
    if not 3 <= score <= 18:
        raise ValueError("CWN attribute score must be 3..18")
    if score == 3:
        return -2
    if score <= 7:
        return -1
    if score <= 13:
        return 0
    if score <= 17:
        return 1
    return 2

_SAVE_PAIRS = {
    "physical": ("strength", "constitution"),
    "evasion": ("dexterity", "intelligence"),
    "mental": ("wisdom", "charisma"),
}
def save_target(level: int, kind: str, attributes: dict[str, int]) -> int:
    """CWN save target (book p. 30), excluding special modifiers and natural 1/20."""
    if not 1 <= level <= 10 or kind not in _SAVE_PAIRS:
        raise ValueError("Unsupported CWN level/save kind")
    return 16 - level - max(attribute_modifier(attributes[a]) for a in _SAVE_PAIRS[kind])

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
        raise ValueError("Unsupported CWN difficulty band")
    rng = rng or random
    dice = (rng.randint(1, 6), rng.randint(1, 6))
    total = sum(dice) + rank + attribute_modifier
    return CheckResult(dice, total, difficulty, total >= difficulty)
