from __future__ import annotations

from src.rpg import (
    Character,
    PsiActionContext,
    PsiMode,
    PsiPressure,
    ResultTier,
    belief_bonus,
    consensus_modifier,
    load_psi_tables,
    ontological_shock,
    psi_rating_for,
    reality_shift,
    resolve_psi_action,
)


def _character(psyche: dict | None = None, tags: set | None = None) -> Character:
    return Character(
        id="seer",
        name="Seer",
        attributes={
            "Intelligence": 3, "Awareness": 3, "Reflexes": 2, "Body": 2,
            "Charisma": 3, "Willpower": 3, "Cybernetics": 1,
        },
        skills={"Notice": 2, "Rapport": 2},
        tags=tags or set(),
        psyche=psyche or {},
    )


def test_psi_rating_bound_is_zero_to_six() -> None:
    PsiActionContext(psi_rating=0)
    PsiActionContext(psi_rating=6)
    for bad in (-1, 7, 99):
        try:
            PsiActionContext(psi_rating=bad)
        except ValueError:
            continue
        raise AssertionError(f"psi_rating {bad} should be rejected")


def test_existing_context_fields_still_bounded_zero_to_four() -> None:
    for bad in (-1, 5):
        try:
            PsiActionContext(corridor_strength=bad)
        except ValueError:
            continue
        raise AssertionError(f"field value {bad} should be rejected")


def test_psi_rating_contributes_to_trajectory_modifier() -> None:
    base = PsiActionContext(psi_rating=0).trajectory_modifier
    high = PsiActionContext(psi_rating=6).trajectory_modifier
    # rating 6 → 3 steps of +1, capped at 2 → +2 modifier
    assert high - base == 2


def test_consensus_modifier_sign_and_cap() -> None:
    cfg = load_psi_tables()["consensus"]
    cap = int(cfg["cap"])
    assert consensus_modifier(3, 0) == cap
    assert consensus_modifier(0, 3) == -cap
    assert consensus_modifier(1, 1) == 0
    # capped beyond cap
    assert consensus_modifier(10, 0) == cap


def test_consensus_feeds_context_modifier() -> None:
    believers = PsiActionContext(believers=3, doubters=0).trajectory_modifier
    doubters = PsiActionContext(believers=0, doubters=3).trajectory_modifier
    assert believers > doubters


def test_belief_bonus_for_matching_domain_tag() -> None:
    char = _character(tags={"belief:noetic"})
    assert belief_bonus(char, "noetic") == 1
    assert belief_bonus(char, "physical") == 0


def test_psi_rating_for_reads_and_clamps_psyche() -> None:
    char = _character(psyche={"psi_rating": 5})
    assert psi_rating_for(char) == 5
    over = _character(psyche={"psi_rating": 99})
    assert psi_rating_for(over) == 6
    unset = _character()
    assert psi_rating_for(unset) == 0


def test_ontological_shock_triggers_at_threshold_not_below() -> None:
    cfg = load_psi_tables()["ontological_shock"]
    threshold = int(cfg["threshold"])
    low = PsiPressure(psyche_load=0, noetic_trace=0, instability=threshold - 1)
    assert ontological_shock(low, rating=0) is None
    at = PsiPressure(psyche_load=0, noetic_trace=0, instability=threshold)
    effect = ontological_shock(at, rating=0)
    assert effect is not None
    assert effect.target_layer == "physical"
    assert effect.effect.value >= 1


def test_ontological_shock_rating_contributes_to_trigger() -> None:
    # instability 1 + rating 3 (>= threshold 3) → shock
    pressure = PsiPressure(psyche_load=0, noetic_trace=0, instability=1)
    assert ontological_shock(pressure, rating=3) is not None
    # instability 1 + rating 1 (= 2 < 3) → no shock
    assert ontological_shock(pressure, rating=1) is None


def test_reality_shift_only_on_critical_success_at_high_rating() -> None:
    assert reality_shift(ResultTier.CRITICAL_SUCCESS, rating=6) is not None
    assert reality_shift(ResultTier.CRITICAL_SUCCESS, rating=5) is not None
    # below min_rating
    assert reality_shift(ResultTier.CRITICAL_SUCCESS, rating=4) is None
    # wrong tier
    assert reality_shift(ResultTier.SUCCESS, rating=6) is None
    assert reality_shift(ResultTier.FAILURE, rating=6) is None


def test_reality_shift_effect_bridges_astral_to_physical() -> None:
    shift = reality_shift(ResultTier.CRITICAL_SUCCESS, rating=6)
    assert shift is not None
    assert shift.effect.source_layer == "astral"
    assert shift.effect.target_layer == "physical"
    assert shift.rating == 6


def test_resolve_psi_action_uses_rating_modifier() -> None:
    char = _character(psyche={"psi_rating": 6})
    low = resolve_psi_action(
        char, "target_a", PsiMode.INTUITION, difficulty=6,
        context=PsiActionContext(psi_rating=0), roll=0,
    )
    high = resolve_psi_action(
        char, "target_a", PsiMode.INTUITION, difficulty=6,
        context=PsiActionContext(psi_rating=6), roll=0,
    )
    # The higher-rating context produces a better-or-equal margin.
    assert high.action_result.check.margin >= low.action_result.check.margin