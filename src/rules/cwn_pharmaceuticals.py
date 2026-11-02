"""CWN SRD pharmaceutical administration rules (engine-independent).

Reference: https://cwn.quadrifons.com/gear-vehicles-cyberware/pharmaceuticals-street-drugs/
Does not replace the published medicine effects or existing item catalogue.
"""
from __future__ import annotations

from dataclasses import dataclass

# None means no Heal training is needed; 0 and 1 require the indicated rank.
MIN_HEAL = {
    "Avalanche": 0, "Boneshaker": None, "Chokeout": None,
    "Control-Delete": None, "Hellbender": None, "Lurch": 0,
    "Madeleine": None, "Medical prescription": None, "Olympus": 0,
    "Panacea": 1, "Pillow": 0, "Psycho": None, "Reset": None,
    "Sand": None, "Trauma Patch": None, "Window": 1,
}
MAIN_ACTIONS_TO_ADMINISTER = 1


class PharmaceuticalError(ValueError):
    """Invalid character state or unknown CWN pharmaceutical."""


@dataclass(frozen=True)
class Administration:
    eligible: bool
    main_actions: int
    min_heal: int | None
    benefit_allowed: bool


def administer(
    name: str, *, heal_rank: int | None,
    system_strain: int, strain_maximum: int, strain_cost: int = 0,
    lurch_doses_today: int = 0,
) -> Administration:
    """Check permission and Strain ceiling; negative effects still occur if blocked.

    Lurch requires Heal-0 for the first dose, Heal-1 for the second and so on.
    Strain costs are supplied by the specific drug effect, not invented here.
    """
    if name not in MIN_HEAL:
        raise PharmaceuticalError(f"unknown pharmaceutical: {name}")
    if system_strain < 0 or strain_maximum < 0 or system_strain > strain_maximum:
        raise PharmaceuticalError("invalid System Strain")
    if strain_cost < 0 or lurch_doses_today < 0:
        raise PharmaceuticalError("costs and prior doses cannot be negative")
    required = MIN_HEAL[name]
    if name == "Lurch":
        required = lurch_doses_today
    eligible = required is None or (heal_rank is not None and heal_rank >= required)
    return Administration(eligible, MAIN_ACTIONS_TO_ADMINISTER, required,
                          eligible and system_strain + strain_cost <= strain_maximum)


def strongest_bonus(*bonuses: int) -> int:
    """Multiple simultaneously active drugs do not stack the same benefit."""
    if not bonuses:
        return 0
    return max(bonuses)


def panacea_first_aid(healed_hp: int) -> int:
    """Panacea doubles First Aid HP recovered, minimum six."""
    if healed_hp < 0:
        raise PharmaceuticalError("healed HP must be nonnegative")
    return max(6, 2 * healed_hp)


def trauma_patch_difficulty(rounds_elapsed: int) -> int | None:
    """Int/Heal or Dex/Heal difficulty 6 plus elapsed full rounds; useless after six."""
    if rounds_elapsed < 0:
        raise PharmaceuticalError("rounds cannot be negative")
    return None if rounds_elapsed >= 6 else 6 + rounds_elapsed


def trauma_patch_works(*, rounds_elapsed: int, check_total: int,
                       poison_or_disease: bool = False,
                       dismembered: bool = False) -> bool:
    difficulty = trauma_patch_difficulty(rounds_elapsed)
    return (difficulty is not None and not poison_or_disease
            and not dismembered and check_total >= difficulty)
