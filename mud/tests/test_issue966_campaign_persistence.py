"""Regression checks for the one authoritative solo campaign engine (#966)."""
import json

from nopunk_mud.campaign.engine import CampaignEngine


def test_combat_enemy_hp_survives_restart_and_does_not_reset():
    engine = CampaignEngine(seed=3)
    engine.state.location = "harbour"
    engine.rng.randint = lambda a, b: b  # deterministic high rolls
    output = engine.command("attack watcher")
    hp = engine.state.enemy_hp.get("watcher", 5)
    assert hp < 5
    saved = json.loads(json.dumps(engine.to_dict()))
    resumed = CampaignEngine.from_dict(saved)
    assert resumed.state.enemy_hp["watcher"] == hp
    if hp == 0:
        assert "already over" in resumed.command("attack watcher").lower()


def test_miss_costs_hp_and_records_consequence():
    engine = CampaignEngine(seed=3)
    engine.state.location = "harbour"
    engine.rng.randint = lambda a, b: a  # natural low rolls
    original_hp = engine.state.hp
    engine.command("attack watcher")
    assert engine.state.hp < original_hp
    assert "missed_shot" in engine.state.consequences


def test_rng_state_and_consequences_round_trip():
    engine = CampaignEngine(seed=14)
    engine.command("go street")
    engine.command("go kurvi")
    engine.command("go harbour")
    engine.command("flee")
    original = json.loads(json.dumps(engine.to_dict()))
    restored = CampaignEngine.from_dict(original)
    assert restored.to_dict() == original
    assert "fled_encounter" in restored.state.consequences
    assert restored.rng.randint(1, 10000) == engine.rng.randint(1, 10000)


def test_optional_clue_uses_published_cwn_skill_check():
    engine = CampaignEngine(seed=7)
    engine.state.location = "university"
    engine.rng.randint = lambda a, b: b
    output = engine.command("examine lab door")
    assert "second badge" in output.lower()
    assert "lab_note" in engine.state.clues
