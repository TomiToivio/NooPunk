"""Physical conflict — the executable half of issue #219.

`rulebook/3_PHYSICAL.md` is the human-readable procedure; this module is the arithmetic,
so the properties the chapter claims can be **proved rather than asserted**. It adds no
mechanics: every constant is one the chapter states.

**Status: PROVISIONAL, not canonical.** `IS_CANONICAL = False`; nothing in the shipped
`src/rules/core.py` path imports it. The author owns the calibration.

The three properties worth executing, because prose cannot stop a later edit from
breaking them:

* **Mode parity.** Simple and advanced tactical modes differ only in *where the target
  number comes from*. The effect arithmetic is literally the same function, so a
  character is never numerically weaker for playing the simpler mode.
* **The ladder is a state, not a counter.** Two solid hits do not add up to a worse
  rung; each attack selects a rung independently. This is what `RULEBOOK.md` §51
  requires and what a naive accumulating damage track would quietly violate.
* **Armor mitigates in ladder steps and never past the top.** No subtraction, no
  negative margins, and no state better than Scratched.
"""
from __future__ import annotations

#: PROVISIONAL. The author owns calibration.
IS_CANONICAL = False

# --------------------------------------------------------------------------- #
# The wound ladder (RULEBOOK.md §51 — quoted exactly, never redefined)
# --------------------------------------------------------------------------- #

#: The four states `RULEBOOK.md` §51 records. Order is severity, least to most.
LADDER: tuple[str, ...] = ("Scratched", "Wounded", "Critical", "Down")

#: Machines do not bleed: the same bands drive a function ladder instead.
MACHINE_LADDER: tuple[str, ...] = ("Operational", "Impaired", "Disabled", "Destroyed")

#: Margin of success -> effect band, most severe first. PROVISIONAL thresholds.
BANDS: tuple[tuple[int, str], ...] = (
    (9, "brutal"),
    (5, "severe"),
    (1, "solid"),
    (0, "glancing"),
)

#: Effect band -> rung on the ladder, by index into LADDER.
BAND_TO_LADDER_INDEX: dict[str, int] = {
    "glancing": 0,  # Scratched
    "solid": 1,     # Wounded
    "severe": 2,    # Critical
    "brutal": 3,    # Down
}

#: The core difficulty ladder (`RULEBOOK.md` §4.2), used by simple mode.
DIFFICULTY_LADDER: tuple[int, ...] = (9, 13, 15, 17, 21, 24, 29)

#: The band a simple-mode target sits at before cover, aim and range adjust it.
BAND_DIFFICULTY: dict[str, int] = {
    "engaged": 13,
    "near": 13,
    "far": 15,
    "distant": 17,
}

#: Damage types the chapter lists. Armor is rated by which of these it resists.
DAMAGE_TYPES: tuple[str, ...] = (
    "ballistic",
    "kinetic",
    "energy",
    "electrical",
    "chemical",
    "radiation",
    "psychotronic",
)


class PhysicalConflictError(ValueError):
    """A physical-conflict invariant was violated."""


# --------------------------------------------------------------------------- #
# The effect arithmetic — ONE function, used by both tactical modes
# --------------------------------------------------------------------------- #

def margin(total: int, target: int) -> int:
    """Margin of success: how far the check beat its target number."""
    return total - target


def band_for_margin(value: int) -> str:
    """The effect band for a margin. Defined for every integer, including negatives."""
    for threshold, band in BANDS:
        if value >= threshold:
            return band
    return "glancing"


def ladder_index_for_band(band: str) -> int:
    try:
        return BAND_TO_LADDER_INDEX[band]
    except KeyError:
        raise PhysicalConflictError(f"unknown effect band: {band!r}") from None


def shift_ladder(index: int, steps_up: int) -> int:
    """Mitigation moves a rung *up* (less severe), never past the top."""
    if steps_up < 0:
        raise PhysicalConflictError("mitigation cannot move a wound down the ladder")
    return max(0, index - steps_up)


def armor_steps(damage_type: str, resists: frozenset[str] | set[str] | tuple[str, ...]) -> int:
    """Armor's effect is a ladder step, not a subtraction.

    One step when the armor resists the damage type, none when it does not, and armor
    never stacks with itself -- which is why this returns 0 or 1 and not a sum.
    """
    if damage_type not in DAMAGE_TYPES:
        raise PhysicalConflictError(f"unknown damage type: {damage_type!r}")
    return 1 if damage_type in set(resists) else 0


def wound_state(total: int, target: int, *, armor_steps_applied: int = 0) -> str:
    """The single rung an attack lands on.

    Both tactical modes call this. The ladder is a *state*, not a counter: this
    function takes no previous wound state, so two solid hits cannot accumulate into a
    worse rung.
    """
    band = band_for_margin(margin(total, target))
    index = shift_ladder(ladder_index_for_band(band), armor_steps_applied)
    return LADDER[index]


def machine_state(total: int, target: int, *, armor_steps_applied: int = 0) -> str:
    """The same bands and the same mitigation, on the function ladder."""
    band = band_for_margin(margin(total, target))
    index = shift_ladder(ladder_index_for_band(band), armor_steps_applied)
    return MACHINE_LADDER[index]


# --------------------------------------------------------------------------- #
# Target numbers: the ONLY thing the two modes disagree about
# --------------------------------------------------------------------------- #

def simple_target_number(
    position: str,
    *,
    cover_steps: int = 0,
    aim_steps: int = 0,
) -> int:
    """Simple mode's target number: the core ladder, moved a step per cover/aim.

    Cover and aim are difficulty *steps* on `RULEBOOK.md` §4.2's ladder, so the result is
    always one of the authored values rather than an invented number.
    """
    try:
        base = BAND_DIFFICULTY[position]
    except KeyError:
        raise PhysicalConflictError(
            f"unknown band: {position!r} (expected one of {tuple(BAND_DIFFICULTY)})"
        ) from None
    if cover_steps < 0 or aim_steps < 0:
        raise PhysicalConflictError("cover and aim cannot make an attack easier")
    index = DIFFICULTY_LADDER.index(base) + cover_steps - aim_steps
    return DIFFICULTY_LADDER[max(0, min(index, len(DIFFICULTY_LADDER) - 1))]


def opposed_target_number(defender_ref: int, defender_fray: int, defender_roll: int) -> int:
    """Advanced mode's target number: the defender's own roll."""
    for label, value in (("REF", defender_ref), ("Fray", defender_fray)):
        if value < 0:
            raise PhysicalConflictError(f"{label} cannot be negative")
    return defender_ref + defender_fray + defender_roll


# --------------------------------------------------------------------------- #
# Suppression: a status, never a wound
# --------------------------------------------------------------------------- #

#: The PSY + Fray check the target must pass to avoid being Pinned.
SUPPRESSION_SKILL = "Fray"
SUPPRESSION_AP_LOST = 1


def resist_suppression(psy: int, fray: int, roll: int, target: int) -> bool:
    """True when the target shakes off suppression. Never wounds, by construction."""
    return psy + fray + roll >= target
