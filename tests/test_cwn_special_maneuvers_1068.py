"""SRD examples and edge cases for CWN special combat maneuvers (#1068)."""
try:  # `unittest discover -s tests` puts tests/ on sys.path
    from _pytest_compat import pytest, register_module_functions
except ModuleNotFoundError:  # pytest.ini uses --import-mode=importlib, which does not
    import importlib.util as _ilu
    import pathlib as _pl

    _spec = _ilu.spec_from_file_location(
        "_pytest_compat", _pl.Path(__file__).with_name("_pytest_compat.py"))
    assert _spec and _spec.loader
    _compat = _ilu.module_from_spec(_spec)
    _spec.loader.exec_module(_compat)
    pytest, register_module_functions = _compat.pytest, _compat.register_module_functions

from src.rules.cwn_special_maneuvers import (
    ManeuverError,
    TargetSize,
    dual_wield,
    escape_grapple,
    execution_hit,
    execution_melee_auto_hit,
    execution_ranged_difficulty,
    move_grappled_target,
    shove,
    size_check_modifier,
    start_grapple,
)


def test_shove_requires_melee_hit_and_strict_opposed_win():
    assert not shove(melee_hit=False, attacker_check=12, defender_check=4).succeeded
    assert not shove(melee_hit=True, attacker_check=8, defender_check=8).succeeded
    assert shove(melee_hit=True, attacker_check=9, defender_check=8).metres == 3
    prone = shove(melee_hit=True, attacker_check=9, defender_check=8, knock_prone=True)
    assert prone.prone and prone.metres == 0


def test_grappling_both_hands_size_modifiers_and_ties():
    with pytest.raises(ManeuverError):
        start_grapple(unarmed_hit=True, hands_free=False, attacker_check=15, defender_check=1)
    assert start_grapple(unarmed_hit=True, hands_free=True, attacker_check=8, defender_check=8) is None
    state = start_grapple(unarmed_hit=True, hands_free=True, attacker_check=11,
                          defender_check=8, size=TargetSize.LARGE_HUMANOID)
    assert state and state.movement_locked and state.unarmed_only
    assert state.automatic_unarmed_damage_each_round
    assert size_check_modifier(TargetSize.AWKWARD) == -4


def test_multiple_assailants_all_must_be_beaten():
    assert escape_grapple(defender_check=10, assailant_checks=(9, 8))
    assert not escape_grapple(defender_check=10, assailant_checks=(9, 10))
    with pytest.raises(ManeuverError):
        escape_grapple(defender_check=10, assailant_checks=())


def test_moving_grappled_target_tie_frees_and_throw_is_two_metres():
    assert move_grappled_target(attacker_check=10, defender_check=10).escaped
    assert move_grappled_target(attacker_check=11, defender_check=10).movement_metres == 3
    thrown = move_grappled_target(attacker_check=11, defender_check=10, throw=True)
    assert thrown.thrown_metres == 2 and thrown.prone and not thrown.escaped


def test_dual_wield_requires_skill_one_and_never_adds_shock():
    with pytest.raises(ManeuverError):
        dual_wield(first_skill=0, second_skill=1, target_in_both_ranges=True)
    assert dual_wield(first_skill=1, second_skill=1, target_in_both_ranges=True) == {
        "hit_modifier": -1, "damage_bonus": 2, "shock_bonus": 0}
    assert dual_wield(first_skill=2, second_skill=1, target_in_both_ranges=False)["damage_bonus"] == 0


@pytest.mark.parametrize("band,difficulty", [("within_two_metres", 6), ("normal", 8), ("long", 10)])
def test_execution_ranged_difficulties(band, difficulty):
    assert execution_ranged_difficulty(unsuspecting=True, uninterrupted_minute=True,
                                        range_band=band) == difficulty


def test_execution_requires_unaware_target_and_full_minute():
    with pytest.raises(ManeuverError):
        execution_ranged_difficulty(unsuspecting=False, uninterrupted_minute=True, range_band="normal")
    assert not execution_melee_auto_hit(unsuspecting=True, uninterrupted_minute=False, within_reach=True)
    assert execution_melee_auto_hit(unsuspecting=True, uninterrupted_minute=True, within_reach=True)


def test_execution_save_and_trauma_even_on_save():
    fail = execution_hit(combat_skill=2, physical_save_succeeded=False)
    assert fail.save_penalty == -2 and fail.mortally_wounded and fail.traumatic_hit
    saved = execution_hit(combat_skill=2, physical_save_succeeded=True)
    assert not saved.mortally_wounded and saved.normal_damage and saved.traumatic_hit
    assert execution_hit(combat_skill=2, physical_save_succeeded=False, nonlethal=True).unconscious


# CI runs `unittest discover`, which needs a TestCase rather than module-level functions.
# The shim keeps the pytest-style bodies and makes them discoverable without pytest.
ModuleLevelTests = register_module_functions(globals())
