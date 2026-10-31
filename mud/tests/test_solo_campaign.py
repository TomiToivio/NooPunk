"""No-LLM single-player prologue and persistence-contract tests (#950)."""
from nopunk_mud.solo_campaign import Campaign, advance

def test_complete_solo_case_without_other_players_or_llm():
    state = Campaign()
    state, text = advance(state, "accept", "UNSA safehouse")
    assert state.stage == "investigation"
    state, text = advance(state, "report", "UNSA safehouse")
    assert "no evidence" in text
    state, _ = advance(state, "interview", "Kurvi")
    state, _ = advance(state, "records", "University of Helsinki")
    restored = Campaign.from_dict(state.to_dict())
    restored, _ = advance(restored, "report", "UNSA safehouse")
    restored, _ = advance(restored, "submit", "UNSA safehouse")
    assert restored.stage == "complete"
    assert "Missing Researcher" in restored.completed
    assert state.stage == "investigation"

def test_invalid_actions_do_not_mutate_state():
    state = Campaign()
    new, _ = advance(state, "submit", "Kurvi")
    assert state == new
