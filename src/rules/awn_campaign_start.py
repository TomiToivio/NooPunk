"""AWN Deluxe campaign-start overlays for NoöPunk (printed pp. 49, 51, 55-58, 86-87, 104-110).

These are small deterministic adjudication functions. CWN retains authority for actions,
attacks, saves and character sheets. Callers supply actual dice results: no hidden dice
and no duplicated combat or Stress engine. Printed drugs/mutations are externally catalogued.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Literal


class AwnRulesError(ValueError):
    pass


@dataclass(frozen=True)
class RadiationResult:
    constitution: int
    system_strain: int
    fatal: bool
    mutation_trigger: str | None = None


def radiation_exposure(*, constitution: int, system_strain: int, max_strain: int,
                       physical_save_success: bool, strain_roll: int = 0,
                       constitution_loss_roll: int = 0, natural_roll: int | None = None,
                       mutation_enabled: bool = False) -> RadiationResult:
    """Resolve one AWN radiation save (p.55). Roll ranges are supplied by CWN dice."""
    if not 3 <= constitution <= 18 or not 0 <= system_strain <= max_strain:
        raise AwnRulesError("invalid constitution or System Strain")
    if physical_save_success:
        if not 1 <= strain_roll <= 4:
            raise AwnRulesError("successful radiation save requires 1d4 strain result")
        if system_strain + strain_roll <= max_strain:
            return RadiationResult(constitution, system_strain + strain_roll, False)
        # A successful save which exceeds maximum Strain becomes a failed save.
    if not 1 <= constitution_loss_roll <= 6:
        raise AwnRulesError("failed radiation save requires 1d6 Constitution loss")
    con = constitution - constitution_loss_roll
    trigger = None
    if mutation_enabled and natural_roll in (1, 20):
        trigger = "negative" if natural_roll == 1 else "positive"
    return RadiationResult(con, system_strain, con < 3, trigger)


@dataclass
class Addiction:
    """AWN p.58: voluntary addiction and a weekly recovery opportunity."""
    substance: str
    active: bool = True
    weeks_abstinent: int = 0

    def abstain_week(self, *, save_success: bool, heal_bonus_applied: bool = False) -> bool:
        """The caller makes the Physical/Mental save, optionally with a caregiver's Heal."""
        if not self.active:
            return True
        self.weeks_abstinent += 1
        if save_success:
            self.active = False
        return not self.active

    def indulge(self) -> None:
        if self.active:
            self.weeks_abstinent = 0


@dataclass(frozen=True)
class ChaseResult:
    caught: bool
    fleeing_total: int
    pursuing_total: int


def foot_chase(*, fleeing_check: int, pursuing_check: int,
               helper_bonus: int = 0, pursuit_modifier: int = 0) -> ChaseResult:
    """AWN p.51: pursuers must beat (not tie) the fleeing group's pace."""
    if not -3 <= helper_bonus <= 3:
        raise AwnRulesError("foot-chase assistance cannot exceed 3")
    pace = fleeing_check + helper_bonus
    pursuit = pursuing_check + pursuit_modifier
    return ChaseResult(pursuit > pace, pace, pursuit)


def vehicle_chase(*, fleeing_drive_check: int, fleeing_speed: int,
                  pursuing_drive_check: int, pursuing_speed: int,
                  fleeing_maneuver_bonus: int = 0, pursuit_modifier: int = 0) -> ChaseResult:
    """AWN p.51: vehicle pursuers must equal or exceed the fleeing total."""
    if not 0 <= fleeing_maneuver_bonus <= 3:
        raise AwnRulesError("vehicle maneuver bonus must be 0..3")
    fleeing = fleeing_drive_check + fleeing_speed + fleeing_maneuver_bonus
    pursuing = pursuing_drive_check + pursuing_speed + pursuit_modifier
    return ChaseResult(pursuing >= fleeing, fleeing, pursuing)


@dataclass(frozen=True)
class VehicleTurn:
    drive_action_required: bool
    crash: bool
    stopped: bool


def vehicle_combat_control(*, driver_spent_main_action: bool, relief_driver: bool = False,
                           luck_save_success: bool | None = None) -> VehicleTurn:
    """AWN p.49: a driver normally spends Main Action controlling a vehicle."""
    if driver_spent_main_action or relief_driver:
        return VehicleTurn(True, False, False)
    if luck_save_success is None:
        raise AwnRulesError("an uncontrolled vehicle needs a Luck save")
    return VehicleTurn(True, not luck_save_success, luck_save_success)


def moving_vehicle_attack_penalty(*, unsecured_personal_weapon: bool, moving: bool) -> int:
    """AWN p.49; vehicle-mounted weapons use normal gunner Main Actions."""
    return -4 if unsecured_personal_weapon and moving else 0


@dataclass(frozen=True)
class Pharmaceutical:
    """Effect metadata, not an alternative healing or drug engine (AWN pp.86-87)."""
    name: str
    high_tech_stim: bool
    min_heal_skill: int = 0

    def application(self, *, heal_skill: int) -> Literal["main_action", "minute_or_two"]:
        if heal_skill < self.min_heal_skill:
            raise AwnRulesError("drug application requires a higher Heal skill")
        return "main_action" if self.high_tech_stim else "minute_or_two"


ACTION_DICE = {1: 6, 2: 8, 3: 10, 4: 12, 5: 20}


@dataclass
class Enclave:
    """AWN pp.105-110: an enclave is not a second PC or combat ruleset."""
    name: str
    power: int
    cohesion: int | None = None
    trouble: int = 0
    dominion: int = 0
    features: tuple[str, ...] = ()
    problems: dict[str, int] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if self.power not in ACTION_DICE:
            raise AwnRulesError("enclave Power must be between 1 and 5")
        if self.cohesion is None:
            self.cohesion = self.power
        if not self.name:
            raise AwnRulesError("enclave needs a name")
        if self.trouble < 0 or self.dominion < 0:
            raise AwnRulesError("enclave ratings must be nonnegative")

    @property
    def action_die(self) -> int:
        return ACTION_DICE[self.power]

    @property
    def external_actions_per_turn(self) -> int:
        return self.power

    def trouble_check(self, die_roll: int) -> bool:
        """True means a Problem prevents the action (AWN p.106)."""
        if not 1 <= die_roll <= self.action_die:
            raise AwnRulesError("roll must fit enclave Action Die")
        return die_roll <= self.trouble

    def spend_dominion(self, cost: int) -> None:
        if cost < 0 or cost > self.dominion:
            raise AwnRulesError("not enough Dominion")
        self.dominion -= cost

    def gain_dominion(self, amount: int) -> None:
        if amount < 0:
            raise AwnRulesError("negative Dominion gain")
        self.dominion += amount


def stress_engine():
    """Use the pre-existing AWN stress tracker, not a new competing track."""
    try:
        from src.rules import awn_stress_tracker
    except ModuleNotFoundError:
        from rules import awn_stress_tracker
    return awn_stress_tracker
