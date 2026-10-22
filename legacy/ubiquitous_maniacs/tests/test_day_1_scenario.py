from __future__ import annotations

from pathlib import Path

from src.rpg import RPGSession, ResultTier, load_character, load_scenario


ROOT = Path(__file__).resolve().parents[1]
CHARACTER = ROOT / "data/rpg/characters/romppainen_day_1.md"
SCENARIO = ROOT / "data/rpg/scenarios/day_1_arrival_and_entanglement.json"


def day_1_session(die=lambda: 0) -> RPGSession:
    return RPGSession(load_character(CHARACTER), load_scenario(SCENARIO), fate_die=die)


def test_day_1_character_encodes_cover_and_suppressed_identity() -> None:
    romppainen = load_character(CHARACTER)

    assert romppainen.psyche["active_persona"] == "Sven-Olof"
    assert romppainen.psyche["latent_persona"] == "Romppainen"
    assert "dissociated_cover_personality" in romppainen.conditions
    assert "suppressed_detective_reflexes" in romppainen.tags


def test_day_1_contains_the_complete_initial_day_structure() -> None:
    scenario = load_scenario(SCENARIO)

    assert scenario.entry_scene == "d1_screening"
    assert list(scenario.scenes) == [
        "d1_screening",
        "d1_meet_ingrid",
        "d1_orientation",
        "d1_therapy_ingress",
        "d1_stockholm",
        "d1_collision",
        "d1_ufab_heist",
        "d1_night_signal",
        "d1_complete",
    ]
    assert sum(len(scene.interactions) for scene in scenario.scenes.values()) == 24


def test_every_day_1_outcome_points_to_a_known_scene() -> None:
    scenario = load_scenario(SCENARIO)

    for scene in scenario.scenes.values():
        for interaction in scene.interactions.values():
            outcomes = list(interaction.outcomes.values())
            if interaction.automatic_outcome is not None:
                outcomes.append(interaction.automatic_outcome)
            for outcome in outcomes:
                assert outcome.next_scene is None or outcome.next_scene in scenario.scenes


def test_every_checked_choice_has_narrative_for_every_result_tier() -> None:
    scenario = load_scenario(SCENARIO)

    for scene in scenario.scenes.values():
        for interaction in scene.interactions.values():
            if interaction.check is None:
                continue
            for tier in ResultTier:
                outcome = RPGSession._outcome_for_tier(interaction, tier)
                assert outcome.text


def test_one_full_day_1_route_reaches_day_2_hook() -> None:
    game = day_1_session()
    route = [
        ("ask_android", "d1_meet_ingrid"),
        ("help_ingrid", "d1_orientation"),
        ("ask_side_effects", "d1_therapy_ingress"),
        ("shared_appointment", "d1_stockholm"),
        ("clear_route", "d1_collision"),
        ("stay_with_ingrid", "d1_ufab_heist"),
        ("inspect_batch", "d1_night_signal"),
        ("answer_signal", "d1_complete"),
    ]

    for interaction_id, expected_scene in route:
        assert interaction_id in {item.id for item in game.available_interactions()}
        game.perform_interaction(interaction_id)
        assert game.state.current_scene == expected_scene

    assert game.state.campaign_flags["day_1_complete"] is True
    assert game.state.campaign_flags["day_2_persona"] == "kiimainen_poliisi"
    assert "entangled_assemblage" in game.state.campaign_flags
    assert any(event.type == "day_completed" for event in game.events)
    assert game.available_interactions() == []


def test_social_continuity_remains_local_to_the_rpg_state() -> None:
    game = day_1_session()
    game.perform_interaction("ask_android")
    game.perform_interaction("help_ingrid")

    assert game.state.campaign_flags["first_contact"] == "shared_lie"
    assert not any(event.type == "relationship_change_requested" for event in game.events)


def test_day_1_keeps_nordic_language_and_mythology_in_the_foreground() -> None:
    scenario = load_scenario(SCENARIO)
    orientation = scenario.scenes["d1_orientation"]
    ingress = scenario.scenes["d1_therapy_ingress"]

    assert "Ruotsinkielinen" in orientation.description
    assert "Behandlingen leds av Ragnarök" in orientation.dialogue["orientation_pitch"].text
    assert "suomalaista, karjalaista ja ruotsalaista mytologiaa" in ingress.description
    assert "VÄINÄMÖINEN / ODEN" in ingress.dialogue["which_symptom"].text


def test_day_1_preserves_sister_and_projection_canon() -> None:
    stockholm = load_scenario(SCENARIO).scenes["d1_stockholm"]

    assert "Elsa Falk — Ingridin nuorempi sisar" in stockholm.participants
    assert "kadonneen poikaystävän paikalle" in stockholm.description
    assert "muisto, projektio, Ragnarökin valinta vai jotakin muuta" in stockholm.description


def test_stockholm_session_foreshadows_mythic_roles_without_fixing_them() -> None:
    stockholm = load_scenario(SCENARIO).scenes["d1_stockholm"]

    assert "rappeutunut Väinämöinen" in stockholm.description
    assert "UFAB 80MG -pakkaus Sampona" in stockholm.description
    assert "Vesi yrittää sovittaa Ingridiä Aino-kuvastoon" in stockholm.description
    assert "tarjoamatta yhtä oikeaa tulkintaa" in stockholm.description


def test_kallio_intrudes_but_cannot_locate_romppainen_on_day_1() -> None:
    stockholm = load_scenario(SCENARIO).scenes["d1_stockholm"]

    assert "Blondi Europol-poliisi / tunnistamaton yhteys" in stockholm.participants
    assert "En mä myy mitään" in stockholm.description
    assert "Nainen näyttää tunnistavan hänet" in stockholm.description
    assert "oikea yhteys, Ragnarökin roolitus vai vieras muisto" in stockholm.description
    assert "vuosikymmenten partneri" not in stockholm.description
    assert "psykotroninen ingressi" not in stockholm.description


def test_maniac_riget_influences_are_embedded_as_noopunk_content() -> None:
    scenario = load_scenario(SCENARIO)
    screening = scenario.scenes["d1_screening"].description
    orientation = scenario.scenes["d1_orientation"].description
    ingress = scenario.scenes["d1_therapy_ingress"].description
    aftermath = scenario.scenes["d1_ufab_heist"].description
    night = scenario.scenes["d1_night_signal"].description

    assert "mainosrahoitteisen anestesian" in screening
    assert "mahdoton kolmas käyrä" in orientation
    assert all("VARAHENKILÖ" in text for text in (screening, ingress, night))
    assert "Ingridin märkä jonotusnumero" in aftermath
    assert "olemattomaan kerrokseen −1" in aftermath
    assert "hississä omalla nimellä" in aftermath


def test_style_influence_does_not_copy_source_specific_brands() -> None:
    raw = SCENARIO.read_text(encoding="utf-8")
    assert "AdBuddy" not in raw
    assert "Milgrim" not in raw
    assert "Friend Proxy" not in raw
