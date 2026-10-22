from pathlib import Path

import networkx as nx
import pytest

from src.rpg import (
    ActionType,
    Conflict,
    Conflictant,
    Consequence,
    CrossLayerEffect,
    Faction,
    FactionProject,
    GraphEffect,
    PsiMode,
    PsiActionContext,
    PsychosurgerySession,
    Relationship,
    RPGSession,
    advance_skill,
    apply_graph_effect,
    create_npc,
    intrude,
    load_character,
    load_scenario,
    resolve_action,
    resolve_psi_action,
    use_psi,
)


ROOT = Path(__file__).resolve().parents[1]


def romppainen():
    return load_character(ROOT / "data/rpg/characters/romppainen_day_1.md")


def test_action_supports_deterministic_roll_and_stunt() -> None:
    actor = romppainen()
    actor.stunts.add("Institutional Paranoia")
    result = resolve_action(
        actor,
        attribute="Awareness",
        skill="Notice",
        difficulty=5,
        action=ActionType.OVERCOME,
        roll=0,
        stunt="Institutional Paranoia",
    )
    assert result.check.roll == 0
    assert result.check.situational_modifier == 2
    assert result.succeeded


def test_action_rejects_impossible_fixed_4df_total() -> None:
    with pytest.raises(ValueError, match=r"between -4 and \+4"):
        resolve_action(romppainen(), attribute="Body", skill=None, difficulty=0, roll=5)


def test_action_supports_a_real_random_4df_roll() -> None:
    result = resolve_action(romppainen(), attribute="Body", skill=None, difficulty=0)
    assert len(result.check.dice) == 4
    assert set(result.check.dice) <= {-1, 0, 1}
    assert -4 <= result.check.roll <= 4


def test_costly_success_advances_but_is_not_clean() -> None:
    actor = romppainen()
    effect = GraphEffect("social", "adjust_edge", actor.id, "ingrid", "trust", 1)
    result = resolve_action(
        actor,
        attribute="Body",
        skill=None,
        difficulty=actor.attribute("Body") + 1,
        roll=0,
        graph_effects=(effect,),
    )
    assert result.check.tier.value == "costly_success"
    assert result.succeeded
    assert not result.clean_success
    assert result.requires_cost
    assert result.applicable_graph_effects == (effect,)


def test_created_aspect_only_applies_when_create_advantage_advances() -> None:
    actor = romppainen()
    failed = resolve_action(
        actor,
        attribute="Body",
        skill=None,
        difficulty=actor.attribute("Body") + 5,
        action=ActionType.CREATE_ADVANTAGE,
        roll=0,
        created_aspect="Avoin reitti",
    )
    costly = resolve_action(
        actor,
        attribute="Body",
        skill=None,
        difficulty=actor.attribute("Body") + 1,
        action=ActionType.CREATE_ADVANTAGE,
        roll=0,
        created_aspect="Avoin reitti",
    )

    assert failed.applicable_created_aspect is None
    assert costly.applicable_created_aspect == "Avoin reitti"


def test_graph_effect_is_portable_to_networkx() -> None:
    graph = nx.Graph()
    effect = GraphEffect("social", "adjust_edge", "romppainen", "ingrid", "trust", 3)
    apply_graph_effect(graph, effect)
    apply_graph_effect(graph, effect)
    assert graph["romppainen"]["ingrid"]["trust"] == 6


def test_relationship_tracks_dimensions_history_and_clamps() -> None:
    relationship = Relationship("romppainen", "ingrid", {"trust": 99})
    effect = relationship.change("trust", 5, "Shared a bad institutional joke")
    assert relationship.values["trust"] == 100
    assert effect.value == 1
    assert relationship.history
    assert effect.domain == "social"


def test_cyber_and_psi_are_unified_actions_with_graph_effects() -> None:
    actor = romppainen()
    cyber = intrude(actor, "ufab_terminal", 4, roll=0)
    psi = use_psi(actor, "ingrid_falk", PsiMode.RESONANCE, 4, roll=0)
    assert cyber.action == ActionType.OVERCOME
    assert cyber.graph_effects[0].domain == "cyber"
    assert psi.action == ActionType.CREATE_ADVANTAGE
    assert psi.graph_effects[0].domain == "noetic"

    failed = intrude(actor, "ufab_terminal", 20, roll=-4)
    assert not failed.succeeded
    assert failed.applicable_graph_effects == ()


def test_psychosurgery_requires_consent_for_identity_change() -> None:
    session = PsychosurgerySession(romppainen(), "ufab_ragnarok", consent=False)
    session.reveal_aspect("Somebody Else's Memories")
    with pytest.raises(PermissionError, match="consent"):
        session.integrate_aspect("Somebody Else's Memories")
    effect = session.resonate("ingrid_falk")
    assert effect.key == "resonance"


def test_psi_follows_an_open_low_resistance_trajectory() -> None:
    actor = romppainen()
    open_context = PsiActionContext(
        corridor_strength=3,
        bifurcation_openness=3,
        affective_salience=2,
        semantic_distance=1,
    )
    forced_context = PsiActionContext(
        semantic_distance=3,
        instrumentality=4,
        local_noise=3,
    )
    open_result = resolve_psi_action(
        actor, "ingrid_falk", PsiMode.RESONANCE, 6, context=open_context, roll=0
    )
    forced_result = resolve_psi_action(
        actor, "stranger", PsiMode.RESONANCE, 6, context=forced_context, roll=0
    )
    assert open_result.action_result.check.total > forced_result.action_result.check.total
    assert open_result.context.trajectory_modifier > 0
    assert forced_result.context.trajectory_modifier < 0


def test_psi_mode_selects_the_relevant_graph_layer() -> None:
    result = resolve_psi_action(
        romppainen(), "unstable_reactor", PsiMode.PSYCHOKINESIS, 5, roll=0
    )
    assert result.action_result.graph_effects[0].domain == "physical"
    assert result.action_result.graph_effects[0].key == "psychokinesis"


def test_instrumentalized_psi_accumulates_pressure() -> None:
    result = resolve_psi_action(
        romppainen(),
        "lottery_terminal",
        PsiMode.PRECOGNITION,
        20,
        context=PsiActionContext(instrumentality=4, semantic_distance=4, local_noise=4),
        roll=-4,
    )
    assert not result.action_result.succeeded
    assert result.pressure.psyche_load > 0
    assert result.pressure.noetic_trace > 0
    assert result.pressure.instability > 0


def test_cross_layer_identity_change_requires_consent() -> None:
    pivot = CrossLayerEffect(
        source_layer="cyber",
        target_layer="noetic",
        interface="bci",
        trigger="memory_feedback",
        effect=GraphEffect("noetic", "set_node", "romppainen", key="identity", value="edited"),
        provenance=("bci_feedback", "shared_dream"),
        consent_required=True,
        consent=False,
    )
    result = resolve_psi_action(
        romppainen(),
        "romppainen",
        PsiMode.PSYCHOSURGERY,
        1,
        context=PsiActionContext(corridor_strength=4, bifurcation_openness=4),
        roll=4,
        cross_layer_effects=(pivot,),
    )
    assert result.action_result.succeeded
    assert result.applicable_cross_layer_effects == ()


def test_unified_conflict_uses_opposed_action_totals() -> None:
    actor = romppainen()
    attack = resolve_action(
        actor, attribute="Charisma", skill="Provoke", difficulty=0,
        action=ActionType.ATTACK, roll=1,
    )
    defense = resolve_action(
        actor, attribute="Willpower", skill="Will", difficulty=0,
        action=ActionType.DEFEND, roll=-1,
    )
    conflict = Conflict("social", {"a": Conflictant("a"), "b": Conflictant("b")})
    shifts = conflict.apply_exchange("a", "b", attack, defense)
    assert shifts == max(0, attack.check.total - defense.check.total)
    assert conflict.participants["b"].stress == shifts


def test_consequence_can_absorb_conflict_shifts() -> None:
    participant = Conflictant("romppainen")
    remaining = participant.absorb_with_consequence(Consequence("Identity fracture", 4, "noetic"), 5)
    assert remaining == 1


def test_consequence_absorbs_shifts_during_exchange() -> None:
    actor = romppainen()
    attack = resolve_action(
        actor, attribute="Charisma", skill="Provoke", difficulty=0,
        action=ActionType.ATTACK, roll=4,
    )
    defense = resolve_action(
        actor, attribute="Willpower", skill="Will", difficulty=0,
        action=ActionType.DEFEND, roll=-4,
    )
    consequence = Consequence("Julkinen kasvojen menetys", 2, "social")
    conflict = Conflict("social", {"a": Conflictant("a"), "b": Conflictant("b")})
    raw_shifts = max(0, attack.check.total - defense.check.total)

    remaining = conflict.apply_exchange("a", "b", attack, defense, consequence)

    assert remaining == max(0, raw_shifts - consequence.severity)
    assert conflict.participants["b"].stress == remaining
    assert conflict.participants["b"].consequences == [consequence]


def test_conflict_rejects_wrong_action_types() -> None:
    actor = romppainen()
    overcome = resolve_action(actor, attribute="Body", skill=None, difficulty=0, roll=0)
    defense = resolve_action(
        actor, attribute="Body", skill=None, difficulty=0,
        action=ActionType.DEFEND, roll=0,
    )
    conflict = Conflict("physical", {"a": Conflictant("a"), "b": Conflictant("b")})

    with pytest.raises(ValueError, match="Attack action"):
        conflict.apply_exchange("a", "b", overcome, defense)


@pytest.mark.parametrize(
    ("attribute", "skill", "message"),
    [("Awereness", "Notice", "Unknown attribute"), ("Awareness", "Notise", "Unknown skill")],
)
def test_action_rejects_unknown_rule_identifiers(
    attribute: str, skill: str, message: str
) -> None:
    with pytest.raises(ValueError, match=message):
        resolve_action(romppainen(), attribute=attribute, skill=skill, difficulty=0, roll=0)


def test_concession_is_not_the_same_as_being_taken_out() -> None:
    conflict = Conflict("social", {"a": Conflictant("a"), "b": Conflictant("b")})
    consequence = Consequence("Public loss of face", 2, "social")
    conflict.concede("b", consequence)
    participant = conflict.participants["b"]
    assert participant.conceded
    assert participant.out_of_conflict
    assert not participant.taken_out
    assert participant.stress == 0
    assert participant.consequences == [consequence]

    attack = resolve_action(
        romppainen(), attribute="Body", skill=None, difficulty=0,
        action=ActionType.ATTACK, roll=0,
    )
    with pytest.raises(ValueError, match="left the conflict"):
        conflict.apply_exchange("a", "b", attack, attack)


def test_faction_projects_advance_without_full_simulation() -> None:
    project = FactionProject("Classify the anomaly", goal=3)
    faction = Faction("ufab", "UFAB", ["Maintain therapeutic legitimacy"], projects=[project])
    faction.advance_project(project.name, 2)
    faction.advance_project(project.name, 2)
    assert project.complete
    assert project.progress == 3


def test_npc_and_advancement_use_the_same_character_model() -> None:
    dahl = create_npc(
        "elin_dahl",
        "Dr. Elin Dahl",
        focus_attribute="Awareness",
        focus_skill="Kinesics",
        competence=2,
        aspects={"Institutional compassion"},
    )
    dahl.advancement = 1
    assert advance_skill(dahl, "Rapport") == 1
    assert dahl.advancement == 0


def test_day_1_relationship_change_emits_graph_effect() -> None:
    game = RPGSession(
        romppainen(),
        load_scenario(ROOT / "data/rpg/scenarios/day_1_arrival_and_entanglement.json"),
        fate_die=lambda: 0,
    )
    for interaction in (
        "ask_free_pills",
        "help_ingrid",
        "ask_side_effects",
        "shared_appointment",
        "clear_route",
        "stay_with_ingrid",
    ):
        game.perform_interaction(interaction)
    assert game.state.relationships["ingrid_falk"] > 0
    assert any(effect.domain == "social" and effect.target == "ingrid_falk" for effect in game.state.graph_effects)
