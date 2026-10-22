from __future__ import annotations

from pathlib import Path

from src.rpg import (
    ActionType,
    Character,
    ResultTier,
    Scenario,
    SkillCheck,
    load_deck,
    resolve_action_tarot,
    resolve_check_tarot,
    scenario_from_dict,
    session_from_dict,
    session_to_dict,
    value_to_roll,
)
from src.rpg.tarot import Card, DrawnCard, draw, redraw

ROOT = Path(__file__).resolve().parents[1]
DECK = ROOT / "data/rpg/tarot_deck.json"


def _character() -> Character:
    return Character(
        id="tester",
        name="Tester",
        attributes={
            "Intelligence": 3, "Awareness": 2, "Reflexes": 2, "Body": 2,
            "Charisma": 2, "Willpower": 2, "Cybernetics": 1,
        },
        skills={"Investigate": 2},
    )


def test_deck_loads_with_22_major_and_56_minor() -> None:
    deck = load_deck(DECK)
    assert len(deck.major) == 22
    assert len(deck.minor) == 56
    assert set(deck.suits) == {"Circuits", "Resonators", "Datblades", "Tokens"}
    assert all(card.is_major for card in deck.major)
    assert all(not card.is_major for card in deck.minor)


def test_major_arcana_cover_all_five_tiers() -> None:
    deck = load_deck(DECK)
    tiers = {card.override_tier for card in deck.major}
    assert tiers == set(ResultTier)


def test_value_to_roll_maps_extremes_and_negates_when_reversed() -> None:
    assert value_to_roll(1) == -4
    assert value_to_roll(14) == 4
    assert value_to_roll(1, reversed=True) == 4
    assert value_to_roll(14, reversed=True) == -4
    assert value_to_roll(0) == 0  # Major Arcana never feeds the roll
    # monotonic
    rolls = [value_to_roll(v) for v in range(1, 15)]
    assert rolls == sorted(rolls)


def test_draw_is_deterministic_for_a_fixed_seed() -> None:
    deck = load_deck(DECK)
    first = draw(42, deck)
    second = draw(42, deck)
    assert first == second
    # A different seed should usually differ (not a strict guarantee, but robust here).
    other = draw(43, deck)
    assert other.card.id != first.card.id or other.reversed != first.reversed


def test_draw_respects_suit() -> None:
    deck = load_deck(DECK)
    for suit in deck.suits:
        card = draw(7, deck, suit=suit)
        assert card.card.suit == suit


def test_draw_rejects_unknown_suit() -> None:
    deck = load_deck(DECK)
    try:
        draw(7, deck, suit="Pentacles")
    except ValueError:
        return
    raise AssertionError("expected ValueError for unknown suit")


def test_resolve_check_tarot_minor_returns_checkresult() -> None:
    deck = load_deck(DECK)
    char = _character()
    # Force a Minor card (Ace of Circuits, value 1 → roll -4) to determinism.
    ace = next(c for c in deck.minor if c.id == "ci01")
    drawn = DrawnCard(card=ace, reversed=False)
    check = SkillCheck(attribute="Intelligence", difficulty=2, skill="Investigate")
    result, used = resolve_check_tarot(
        char, seed=1, check=check, deck=deck, force_card=drawn,
    )
    assert used is drawn
    # roll -4 + Int 3 + Investigate 2 = total 1; margin = 1 - 2 = -1 → COSTLY_SUCCESS
    assert result.roll == -4
    assert result.margin == -1
    assert result.tier == ResultTier.COSTLY_SUCCESS


def test_resolve_check_tarot_major_arcana_forces_override_tier() -> None:
    deck = load_deck(DECK)
    char = _character()
    source = next(c for c in deck.major if c.override_tier == ResultTier.CRITICAL_SUCCESS)
    drawn = DrawnCard(card=source, reversed=False)
    check = SkillCheck(attribute="Willpower", difficulty=2, skill=None)
    result, used = resolve_check_tarot(
        char, seed=1, check=check, deck=deck, force_card=drawn,
    )
    assert used.card.is_major
    assert result.tier == ResultTier.CRITICAL_SUCCESS
    assert result.shifts if hasattr(result, "shifts") else True


def test_resolve_action_tarot_returns_action_result_and_drawn_card() -> None:
    deck = load_deck(DECK)
    char = _character()
    king = next(c for c in deck.minor if c.id == "ci14")  # King of Circuits, value 14 → +4
    drawn = DrawnCard(card=king, reversed=False)
    result, used = resolve_action_tarot(
        char, seed=1, attribute="Intelligence", skill="Investigate", difficulty=4,
        action=ActionType.OVERCOME, deck=deck, force_card=drawn,
    )
    assert used.card.id == "ci14"
    # roll +4 + Int 3 + Investigate 2 = 9; margin 9 - 4 = 5 → CRITICAL_SUCCESS
    assert result.check.tier == ResultTier.CRITICAL_SUCCESS
    assert result.succeeded


def test_scenario_rejects_unknown_resolver() -> None:
    scenario_dict = {
        "id": "bad_resolver",
        "title": "Bad Resolver",
        "entry_scene": "s1",
        "scenes": [
            {
                "id": "s1", "title": "S1", "description": "", "location": "x",
                "interactions": [
                    {
                        "id": "i1", "label": "I1", "resolver": "coins",
                        "check": {"attribute": "Intelligence", "difficulty": 2},
                        "outcomes": {"success": {"text": "ok"}},
                    }
                ],
            }
        ],
    }
    try:
        scenario_from_dict(scenario_dict)
    except ValueError:
        return
    raise AssertionError("expected ValueError for unknown resolver")


def test_scenario_accepts_tarot_resolver() -> None:
    scenario_dict = {
        "id": "tarot_scene",
        "title": "Tarot Scene",
        "entry_scene": "s1",
        "scenes": [
            {
                "id": "s1", "title": "S1", "description": "", "location": "x",
                "interactions": [
                    {
                        "id": "i1", "label": "I1", "resolver": "tarot",
                        "check": {"attribute": "Willpower", "difficulty": 2},
                        "outcomes": {"success": {"text": "ok"}, "failure": {"text": "no"}},
                    }
                ],
            }
        ],
    }
    scenario: Scenario = scenario_from_dict(scenario_dict)
    assert scenario.scenes["s1"].interactions["i1"].resolver == "tarot"


def test_engine_resolves_tarot_interaction() -> None:
    from src.rpg import RPGSession, load_character

    scenario_dict = {
        "id": "tarot_engine",
        "title": "Tarot Engine",
        "entry_scene": "s1",
        "scenes": [
            {
                "id": "s1", "title": "S1", "description": "", "location": "x",
                "interactions": [
                    {
                        "id": "draw_card", "label": "Draw a card", "resolver": "tarot",
                        "check": {"attribute": "Willpower", "difficulty": 2},
                        "outcomes": {
                            "critical_success": {"text": "transcendent"},
                            "success": {"text": "ok"},
                            "costly_success": {"text": "price"},
                            "failure": {"text": "no"},
                            "catastrophic_failure": {"text": "doom"},
                        },
                    }
                ],
            }
        ],
        "terminal_scenes": ["s1"],
    }
    scenario = scenario_from_dict(scenario_dict)
    char = load_character(ROOT / "data/rpg/characters/demo_operator.md")
    session = RPGSession(char, scenario, seed=123)
    result = session.perform_interaction("draw_card")
    assert result.check is not None
    assert result.check.tier in set(ResultTier)
    assert session.tarot_draws == 1


def test_tarot_draw_sequence_survives_save_round_trip() -> None:
    from src.rpg import RPGSession

    scenario = scenario_from_dict({
        "id": "tarot_save",
        "title": "Tarot Save",
        "entry_scene": "s1",
        "scenes": [{
            "id": "s1",
            "title": "S1",
            "description": "",
            "location": "x",
            "interactions": [{
                "id": "draw_card",
                "label": "Draw a card",
                "resolver": "tarot",
                "repeatable": True,
                "check": {"attribute": "Willpower", "difficulty": 2},
                "outcomes": {
                    "critical_success": {"text": "transcendent"},
                    "success": {"text": "ok"},
                    "costly_success": {"text": "price"},
                    "failure": {"text": "no"},
                    "catastrophic_failure": {"text": "doom"},
                },
            }],
        }],
    })
    uninterrupted = RPGSession(_character(), scenario, seed=123)
    uninterrupted.perform_interaction("draw_card")
    saved = session_to_dict(uninterrupted)

    restored = session_from_dict(saved, _character(), scenario)

    assert saved["tarot_draws"] == 1
    assert restored.tarot_draws == 1
    expected = uninterrupted.perform_interaction("draw_card")
    actual = restored.perform_interaction("draw_card")
    assert actual.check == expected.check
    assert restored.tarot_draws == uninterrupted.tarot_draws == 2


def test_legacy_save_without_tarot_counter_still_loads() -> None:
    from src.rpg import RPGSession

    scenario = Scenario(id="legacy", title="Legacy", entry_scene="s1", scenes={
        "s1": scenario_from_dict({
            "id": "nested",
            "title": "Nested",
            "entry_scene": "s1",
            "scenes": [{"id": "s1", "title": "S1", "description": "", "location": "x", "interactions": []}],
        }).scenes["s1"],
    })
    data = session_to_dict(RPGSession(_character(), scenario, seed=5))
    data.pop("tarot_draws")

    restored = session_from_dict(data, _character(), scenario)

    assert restored.tarot_draws == 0


# ── Regression tests for review fixes ─────────────────────────────────────


def test_redraw_never_returns_the_identical_card() -> None:
    """C1: a LUCK redraw must never hand back the same card (full deck)."""
    deck = load_deck(DECK)
    for seed in range(20):
        first = draw(seed, deck)
        again = redraw(seed, deck, first)
        assert again.card.id != first.card.id, (
            f"redraw returned the same card {first.card.id!r} for seed {seed}"
        )


def test_redraw_never_returns_identical_card_within_a_suit() -> None:
    """C1: redraw within a suit (14-card pool) must also differ."""
    deck = load_deck(DECK)
    for suit in deck.suits:
        first = draw(11, deck, suit=suit)
        again = redraw(11, deck, first, suit=suit)
        assert again.card.id != first.card.id
        assert again.card.suit == suit


def test_major_arcana_without_override_tier_raises() -> None:
    """C2: a Major Arcana with no override_tier must fail fast, not feed the roll."""
    deck = load_deck(DECK)
    char = _character()
    malformed = Card(id="major_blank", name="Blank Major", suit=None,
                     value=0, arcana="major", override_tier=None)
    drawn = DrawnCard(card=malformed, reversed=False)
    check = SkillCheck(attribute="Willpower", difficulty=2, skill=None)
    try:
        resolve_check_tarot(char, seed=1, check=check, deck=deck, force_card=drawn)
    except ValueError:
        return
    raise AssertionError("expected ValueError for Major Arcana without override_tier")
