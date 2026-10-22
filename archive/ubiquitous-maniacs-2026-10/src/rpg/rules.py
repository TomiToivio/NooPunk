"""Small Fate-inspired check resolver with explicit narrative tiers."""

from __future__ import annotations

from collections.abc import Callable

from .dice import roll_4df
from .models import CANONICAL_ATTRIBUTES, Character, CheckResult, ResultTier, SkillCheck


TRANSHUMANITY_FATE_SKILLS = (
    "Athletics", "Civ Rep", "Cover", "Cred", "Deceive", "Eye Rep", "Fight",
    "Hardware", "Infiltrate", "Infosec", "Investigate", "Kinesics", "Medicine",
    "Notice", "Pilot", "Program", "Provoke", "Rapport", "Shoot", "Somatics",
    "Survival", "Will", "Xeno-Contact", "X-Risks",
)


def validate_skill_check(check: SkillCheck) -> None:
    """Reject misspelled rule identifiers instead of resolving them as +0."""
    if check.attribute not in CANONICAL_ATTRIBUTES:
        raise ValueError(f"Unknown attribute: {check.attribute}")
    if check.skill is not None and check.skill not in TRANSHUMANITY_FATE_SKILLS:
        raise ValueError(f"Unknown skill: {check.skill}")


def validate_transhumanity_fate_skill_profile(
    character: Character,
    *,
    expected_points: int | None = None,
) -> None:
    """Validate the TF skill list, +4 cap, point budget, and Fate columns."""
    unknown = set(character.skills) - set(TRANSHUMANITY_FATE_SKILLS)
    if unknown:
        raise ValueError(f"Unknown Transhumanity's Fate skills: {sorted(unknown)}")
    invalid = {name: rank for name, rank in character.skills.items() if rank < 0 or rank > 4}
    if invalid:
        raise ValueError(f"Skill ranks must be between +0 and +4: {invalid}")
    points = sum(character.skills.values())
    if expected_points is not None and points != expected_points:
        raise ValueError(f"Expected {expected_points} skill points, got {points}")
    counts = {rank: sum(value == rank for value in character.skills.values()) for rank in range(1, 5)}
    if not counts[4] <= counts[3] <= counts[2] <= counts[1]:
        raise ValueError(f"Skill profile violates Fate columns: {counts}")


def tier_for_margin(margin: int) -> ResultTier:
    if margin >= 3:
        return ResultTier.CRITICAL_SUCCESS
    if margin >= 0:
        return ResultTier.SUCCESS
    if margin >= -2:
        return ResultTier.COSTLY_SUCCESS
    if margin >= -4:
        return ResultTier.FAILURE
    return ResultTier.CATASTROPHIC_FAILURE


def resolve_check(
    character: Character,
    check: SkillCheck,
    fate_die: Callable[[], int] | None = None,
) -> CheckResult:
    """Resolve 4dF + attribute + skill + explicit tag/aspect bonuses."""
    validate_skill_check(check)
    dice = roll_4df(fate_die)

    tag_bonus = sum(tag in character.tags for tag in check.bonus_tags)
    tag_bonus += sum(tag in character.tags for tag in check.specialization_tags)
    aspect_bonus = sum(aspect in character.aspects for aspect in check.bonus_aspects)
    attribute_value = character.attribute(check.attribute)
    skill_value = character.skill(check.skill)
    roll = sum(dice)
    total = (
        roll
        + attribute_value
        + skill_value
        + tag_bonus
        + aspect_bonus
        + check.situational_modifier
    )
    margin = total - check.difficulty
    return CheckResult(
        tier=tier_for_margin(margin),
        dice=dice,
        roll=roll,
        attribute=attribute_value,
        skill=skill_value,
        tag_bonus=tag_bonus,
        aspect_bonus=aspect_bonus,
        situational_modifier=check.situational_modifier,
        total=total,
        difficulty=check.difficulty,
        margin=margin,
    )

