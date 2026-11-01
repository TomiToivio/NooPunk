"""#950: deterministic mission clock and radio scene in solo CLI/Evennia engine."""
import pytest
from nopunk_mud.campaign import CampaignEngine


def test_wait_crosses_scene_once_and_persists():
    game = CampaignEngine()
    assert "minute: 0" in game.command("status")
    assert "scene 0" in game.command("wait 9")
    assert "radio_bulletin" not in game.state.flags
    text = game.command("wait 1")
    assert "UNSA radio" in text
    assert game.state.minute == 10
    assert game.state.flags.count("radio_bulletin") == 1
    restored = CampaignEngine.from_dict(game.to_dict())
    assert restored.state.minute == 10
    assert "UNSA radio" not in restored.command("wait 20")
    assert restored.state.flags.count("radio_bulletin") == 1
    assert "scene: 3" in restored.command("status")


@pytest.mark.parametrize("bad", ["", "0", "-3", "61", "1.5", "2 3", "foo"])
def test_invalid_wait_does_not_advance_clock(bad):
    game = CampaignEngine()
    game.command("wait " + bad)
    assert game.state.minute == 0
    assert "radio_bulletin" not in game.state.flags


def test_old_save_defaults_to_mission_minute_zero():
    game = CampaignEngine()
    snapshot = game.to_dict()
    snapshot.pop("minute")
    assert CampaignEngine.from_dict(snapshot).state.minute == 0


def test_corrupt_negative_clock_rejected():
    game = CampaignEngine()
    snapshot = game.to_dict()
    snapshot["minute"] = -1
    with pytest.raises(ValueError, match="negative"):
        CampaignEngine.from_dict(snapshot)


def test_long_wait_fires_bulletin_once_and_never_gates_core_clues():
    game = CampaignEngine()
    assert "UNSA radio" in game.command("wait 60")
    game.command("go street")
    game.command("go university")
    assert "access logs" in game.command("examine terminal").lower()
