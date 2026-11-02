"""CWN SRD special combat maneuvers, pure tabletop-compatible adjudication.

Source: https://cwn.quadrifons.com/rules-of-the-game/combat/special-combat-maneuvers/
Caller resolves ordinary attack/skill/save rolls through the shared CWN engine.
This module adjudicates their results; it does not change those underlying rules.
"""
from dataclasses import dataclass
from enum import Enum


class ManeuverError(ValueError):
    """A CWN maneuver prerequisite is not met."""


class TargetSize(str, Enum):
    HUMAN = "human"
    LARGE_HUMANOID = "large_humanoid"
    AWKWARD = "awkward"


SIZE_PENALTY = {
    TargetSize.HUMAN: 0,
    TargetSize.LARGE_HUMANOID: -2,
    TargetSize.AWKWARD: -4,
}


def size_check_modifier(size: TargetSize) -> int:
    """Apply to every grappling/shoving skill check against unusual targets."""
    return SIZE_PENALTY[TargetSize(size)]


@dataclass(frozen=True)
class ShoveOutcome:
    succeeded: bool
    metres: int = 0
    prone: bool = False


def shove(*, melee_hit: bool, attacker_check: int, defender_check: int,
          knock_prone: bool = False, size: TargetSize = TargetSize.HUMAN) -> ShoveOutcome:
    """A damaging melee attack is replaced by an opposed Str/Exert or Str/Punch check.

    The caller rolls the ordinary melee attack first; no damage is dealt on a hit.
    """
    won = melee_hit and attacker_check + size_check_modifier(size) > defender_check
    return ShoveOutcome(won, 0 if not won or knock_prone else 3, won and knock_prone)


@dataclass(frozen=True)
class GrappleState:
    """One victim, with any number of reasonable attackers represented by their check rolls."""

    assailants: int

    def __post_init__(self) -> None:
        if self.assailants < 1:
            raise ManeuverError("a grapple requires at least one assailant")

    @property
    def movement_locked(self) -> bool:
        return True

    @property
    def unarmed_only(self) -> bool:
        return True

    @property
    def automatic_unarmed_damage_each_round(self) -> bool:
        return True


def start_grapple(*, unarmed_hit: bool, hands_free: bool, attacker_check: int,
                  defender_check: int, size: TargetSize = TargetSize.HUMAN) -> GrappleState | None:
    """Both hands must be free; the initial unarmed attack deals no damage."""
    if not hands_free:
        raise ManeuverError("grappling needs both hands free")
    if unarmed_hit and attacker_check + size_check_modifier(size) > defender_check:
        return GrappleState(1)
    return None


def escape_grapple(*, defender_check: int, assailant_checks: tuple[int, ...]) -> bool:
    """Victim spends a Main Action; must beat *every* assailant's Str/Punch check."""
    if not assailant_checks:
        raise ManeuverError("no assailants to escape")
    return all(defender_check > roll for roll in assailant_checks)


@dataclass(frozen=True)
class GrappleMove:
    escaped: bool
    movement_metres: int = 0
    thrown_metres: int = 0
    prone: bool = False


def move_grappled_target(*, attacker_check: int, defender_check: int,
                         throw: bool = False, size: TargetSize = TargetSize.HUMAN) -> GrappleMove:
    """Costs the grappler a Main Action; failure OR tie frees the target."""
    if attacker_check + size_check_modifier(size) <= defender_check:
        return GrappleMove(escaped=True)
    return GrappleMove(False, thrown_metres=2, prone=True) if throw else GrappleMove(False, movement_metres=3)


def dual_wield(*, first_skill: int, second_skill: int,
               target_in_both_ranges: bool) -> dict[str, int]:
    """Choose one weapon to attack with: -1 hit, +2 damage (not Shock) if both in range."""
    if first_skill < 1 or second_skill < 1:
        raise ManeuverError("dual-wielding requires level 1 in each relevant weapon skill")
    return {"hit_modifier": -1, "damage_bonus": 2 if target_in_both_ranges else 0,
            "shock_bonus": 0}


def execution_ranged_difficulty(*, unsuspecting: bool, uninterrupted_minute: bool,
                                range_band: str) -> int:
    """Dex/Shoot difficulty: point blank 6, normal range 8, long range 10."""
    if not unsuspecting or not uninterrupted_minute:
        raise ManeuverError("execution requires an unsuspecting target and an undisturbed minute")
    difficulties = {"within_two_metres": 6, "normal": 8, "long": 10}
    if range_band not in difficulties:
        raise ManeuverError("unknown execution range")
    return difficulties[range_band]


def execution_melee_auto_hit(*, unsuspecting: bool, uninterrupted_minute: bool,
                             within_reach: bool) -> bool:
    """A full minute of undisturbed proximity grants an automatic melee hit."""
    return unsuspecting and uninterrupted_minute and within_reach


@dataclass(frozen=True)
class ExecutionOutcome:
    save_penalty: int
    mortally_wounded: bool
    unconscious: bool
    traumatic_hit: bool = True
    normal_damage: bool = True


def execution_hit(*, combat_skill: int, physical_save_succeeded: bool,
                  nonlethal: bool = False) -> ExecutionOutcome:
    """Call ONLY after a successful execution hit; apply normal/traumatic damage even on a save.

    The ordinary Physical save engine must include -combat_skill in its roll.
    """
    if combat_skill < 0:
        raise ManeuverError("combat skill must be nonnegative")
    failed = not physical_save_succeeded
    return ExecutionOutcome(-combat_skill, failed and not nonlethal, failed and nonlethal)
