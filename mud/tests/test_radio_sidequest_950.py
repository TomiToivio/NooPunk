"""#950: optional radio privacy case is deterministic and persists."""
import pytest
from nopunk_mud.campaign import CampaignEngine


def start():
    game = CampaignEngine()
    assert "UNSA radio" in game.command("wait 10")
    assert "dispatch" in game.command("radio")
    return game


@pytest.mark.parametrize("choice", ["protect", "disclose"])
def test_radio_case_consequences_persist_and_are_idempotent(choice):
    game = start()
    game.command("go street")
    game.command("go university")
    assert "breach" in game.command("trace")
    snapshot = game.to_dict()
    game = CampaignEngine.from_dict(snapshot)
    game.command("go street")
    game.command("go safehouse")
    assert "Side case complete" in game.command("resolve " + choice)
    restored = CampaignEngine.from_dict(game.to_dict())
    assert restored.state.consequences.count("radio_" + choice) == 1
    assert "radio side case: complete" in restored.command("status")
    assert "already resolved" in restored.command("resolve " + choice)
    assert restored.state.consequences.count("radio_" + choice) == 1


def test_radio_side_case_does_not_gate_main_evidence():
    game = CampaignEngine()
    game.command("go street")
    game.command("go university")
    assert "Access logs" in game.command("examine terminal")
    game.command("go street")
    game.command("go kurvi")
    game.command("ask witness badge")
    assert "badge" in game.command("examine woman").lower()
    game.command("go street")
    game.command("go safehouse")
    assert "Case filed" in game.command("report")
    assert game.state.ending == "solved"


def test_radio_case_refusals_cannot_mutate_quest():
    game = CampaignEngine()
    assert "No open radio" in game.command("radio")
    assert "Accept" in game.command("trace")
    assert "Trace" in game.command("resolve protect")
    assert not any(f.startswith("radio_") for f in game.state.flags)
    game.command("wait 10")
    game.command("radio")
    assert "university" in game.command("trace")
    assert "Trace" in game.command("resolve disclose")
    assert not game.state.consequences
