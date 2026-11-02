"""CWN 6.1.3.5 spells and 6.2.8 spirit powers — the two catalogues (#1068)."""
from __future__ import annotations

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

from src.rules.cwn_spells import (
    SPELLS,
    SpellError,
    overcast,
    overcast_outcome,
    overcast_roll,
    spell,
    spells_committed,
)
from src.rules.cwn_spirit_powers import POWERS, SpiritPowerError, power, total_cost


def test_the_spell_catalogue_is_complete_and_well_formed():
    assert len(SPELLS) >= 25
    assert all(s["commitment"] in ("Day", "Scene", "Scene/Day", "None") for s in SPELLS.values())


def test_scene_and_day_spells_are_distinguishable():
    assert "Arson" in spells_committed("Day")
    assert "Bless" in spells_committed("Scene")


def test_an_unknown_spell_is_an_error_not_a_default():
    with pytest.raises(SpellError):
        spell("Wish")


def test_overcasting_adds_cast_and_constitution_and_penalises_day_commitment():
    # CON 14 -> +1. d20 10 + Cast 2 + 1 = 13; a day-commit spell pays 2 more, so 11.
    assert overcast_roll(die=10, cast_skill=2, constitution=14, commits_for_day=False) == 13
    assert overcast_roll(die=10, cast_skill=2, constitution=14, commits_for_day=True) == 11


def test_the_overcasting_table_bands_match_the_book():
    assert overcast_outcome(1)["effect"] == "instant and unavoidable death"
    assert overcast_outcome(3)["effect"] == "mortally wounded and at zero HP"
    assert overcast_outcome(6)["strain"] == 4
    assert overcast_outcome(12)["strain"] == 2
    assert overcast_outcome(18)["strain"] == 1
    assert overcast_outcome(22)["strain"] == 1


def test_overcasting_past_the_strain_maximum_means_unconscious_for_an_hour():
    out = overcast(die=6, cast_skill=0, constitution=10, commits_for_day=False,
                   current_strain=9, max_strain=10)
    assert out["strain"] == 4
    assert out["unconscious_one_hour"] is True
    assert out["note"] == "wakes with 1 hit point"


def test_overcasting_within_the_maximum_does_not_knock_the_mage_out():
    out = overcast(die=6, cast_skill=0, constitution=10, commits_for_day=False,
                   current_strain=0, max_strain=10)
    assert out["unconscious_one_hour"] is False


def test_the_spirit_power_catalogue_is_complete_and_costed():
    assert len(POWERS) >= 25
    assert all(p["cost"] >= 1 for p in POWERS.values())
    assert power("Violent Will")["cost"] == 1


def test_spirit_power_totals_drive_the_summoning_cost():
    # Real catalogue entries only: inventing a power name to make a test pass is how a fake rule gets in.
    assert total_cost(["Violent Will"]) == 1
    assert total_cost(["Violent Will", "Curse"]) == 2
    with pytest.raises(SpiritPowerError):
        total_cost(["Violent Will", "Flicker"])


def test_an_unknown_power_is_an_error():
    with pytest.raises(SpiritPowerError):
        power("Summon Pizza")


# CI runs `unittest discover`, which needs a TestCase rather than module-level functions.
# The shim keeps the pytest-style bodies and makes them discoverable without pytest.
ModuleLevelTests = register_module_functions(globals())
