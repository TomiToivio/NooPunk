"""Tests for the deterritorialized cyber actions (attune, exorcise, shelter)."""

from __future__ import annotations

from src.rpg import ActionType, GraphEffect, load_character
from src.rpg.cyber import attune, exorcise, shelter, intrude
from src.rpg.models import Character


def _actor() -> Character:
    """Minimal character with Cybernetics + Infosec for tests."""
    return Character(
        id="test_actor",
        name="Test Actor",
        attributes={
            "Intelligence": 2, "Awareness": 2, "Reflexes": 2,
            "Body": 2, "Charisma": 2, "Willpower": 2, "Cybernetics": 3,
        },
        skills={"Infosec": 3},
        tags=set(),
        aspects=set(),
        conditions=set(),
        consequences=[],
        stunts=set(),
        resources={},
        reputation={},
        advancement=0,
        ego={}, morph={}, psyche={}, cyber={},
    )


class TestAttune:
    def test_attune_is_overcome_action(self):
        actor = _actor()
        result = attune(actor, "ufab_terminal", 4, roll=0)
        assert result.action == ActionType.OVERCOME
        assert result.target == "ufab_terminal"

    def test_attune_produces_cyber_graph_effect(self):
        actor = _actor()
        result = attune(actor, "ufab_terminal", 4, roll=0)
        assert len(result.graph_effects) == 1
        assert result.graph_effects[0].domain == "cyber"
        assert result.graph_effects[0].operation == "set_edge"
        assert result.graph_effects[0].key == "attunement"

    def test_attune_succeeds_on_high_roll(self):
        actor = _actor()
        result = attune(actor, "ufab_terminal", 2, roll=4)
        assert result.succeeded
        assert result.applicable_graph_effects != ()

    def test_attune_fails_on_low_roll(self):
        actor = _actor()
        result = attune(actor, "ufab_terminal", 20, roll=-4)
        assert not result.succeeded
        assert result.applicable_graph_effects == ()

    def test_legacy_intrude_alias_works(self):
        """intrude() is a legacy alias for attune() — backward compat."""
        actor = _actor()
        result = intrude(actor, "ufab_terminal", 4, roll=0)
        assert result.action == ActionType.OVERCOME
        assert result.graph_effects[0].domain == "cyber"


class TestExorcise:
    def test_exorcise_is_overcome_action(self):
        actor = _actor()
        result = exorcise(actor, "trapped_persona", 5, roll=0)
        assert result.action == ActionType.OVERCOME
        assert result.target == "trapped_persona"

    def test_exorcise_removes_binding(self):
        actor = _actor()
        result = exorcise(actor, "trapped_persona", 5, roll=4)
        assert result.succeeded
        assert len(result.graph_effects) == 1
        assert result.graph_effects[0].operation == "remove_edge"
        assert result.graph_effects[0].key == "binding"

    def test_exorcise_uses_willpower(self):
        """Exorcism is an act of will, not just technical skill."""
        actor = _actor()
        result = exorcise(actor, "trapped_persona", 5, roll=0)
        # CheckResult should use Willpower attribute
        assert result.check.attribute == 2  # Willpower=2 in _actor


class TestShelter:
    def test_shelter_is_create_advantage(self):
        actor = _actor()
        result = shelter(actor, "fleeing_agi", 4, roll=0)
        assert result.action == ActionType.CREATE_ADVANTAGE

    def test_shelter_creates_social_edge(self):
        """Shelter creates a sanctuary in the SOCIAL layer, not cyber."""
        actor = _actor()
        result = shelter(actor, "fleeing_agi", 4, roll=4)
        assert result.succeeded
        assert len(result.graph_effects) == 1
        assert result.graph_effects[0].domain == "social"
        assert result.graph_effects[0].key == "sanctuary"

    def test_shelter_creates_aspect(self):
        actor = _actor()
        result = shelter(actor, "fleeing_agi", 4, roll=4)
        assert result.applicable_created_aspect == "sanctuary_granted:fleeing_agi"

    def test_shelter_uses_charisma(self):
        """Shelter is an act of care and invitation, using Charisma."""
        actor = _actor()
        result = shelter(actor, "fleeing_agi", 4, roll=0)
        assert result.check.attribute == 2  # Charisma=2 in _actor