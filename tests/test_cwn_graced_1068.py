"""CWN 6.3 The Graced (#1068)."""
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

from src.rules.cwn_graced import Graced, GracedError, art_points, may_take_edge


def test_points_accumulate_and_are_never_reset():
    assert art_points(1) == 2
    assert art_points(2) == 3          # +1
    assert art_points(4) == 6          # +1, +2
    assert art_points(5) == 6          # +0
    assert art_points(10) == 11


def test_a_level_one_graced_can_take_one_two_point_art_or_two_one_point_arts():
    a = Graced(level=1); a.buy("hundred_faces"); assert a.available == 0
    b = Graced(level=1); b.buy("arcane_skill"); b.buy("brazen_thews"); assert b.available == 0


def test_overspending_is_refused():
    g = Graced(level=1)
    with pytest.raises(GracedError):
        g.buy("arcane_skill"); g.buy("brazen_thews"); g.buy("flying_steps")


def test_an_art_is_permanent_and_cannot_be_rebought():
    g = Graced(level=2)
    g.buy("arcane_skill")
    with pytest.raises(GracedError):
        g.buy("arcane_skill")


def test_only_alacrity_can_be_upgraded():
    g = Graced(level=4)                       # 6 points
    g.buy("basic_alacrity")
    with pytest.raises(GracedError):
        g.upgrade("arcane_skill", "hundred_faces")
    g2 = Graced(level=4)
    g2.buy("basic_alacrity")
    # upgrading replaces the art and charges only the difference
    before = g2.available
    g2.upgrade("basic_alacrity", "hundred_faces")   # both 2 points: difference 0
    assert "hundred_faces" in g2.arts and "basic_alacrity" not in g2.arts
    assert g2.available == before


def test_a_graced_may_never_take_spellcaster_or_summoner():
    assert may_take_edge("Spellcaster") is False
    assert may_take_edge("Summoner") is False
    assert may_take_edge("Graced") is True


def test_unknown_arts_are_refused():
    with pytest.raises(GracedError):
        Graced(level=10).buy("invisibility_plus")


# CI runs `unittest discover`, which needs a TestCase rather than module-level functions.
# The shim keeps the pytest-style bodies and makes them discoverable without pytest.
ModuleLevelTests = register_module_functions(globals())
