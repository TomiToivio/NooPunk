#!/usr/bin/env python3
"""Validate the multi-axis ideological model (issue #8).

The model's whole value is that ideological positions are SEPARABLE: a faction's
position on one paradigm shift must not be readable from its position on another.
If this data ever collapses into a single axis, or a faction loses a position, the
world silently becomes the two-camp version the issue exists to prevent.

This is a structural test, not a content test: it does not check which faction
holds which position (that is the author's, and it may change), only that the
cross-product is intact and internally consistent.
"""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MODEL_PATH = ROOT / "data" / "world" / "ideology.json"

#: The paradigm shifts the author named in issue #8 and TIMELINE.md. Losing one
#: would mean a whole axis of ideological conflict had been dropped.
REQUIRED_AXES = {"ai", "nhi", "psionics", "panpsychism", "cyborgization", "noosphere"}

#: The four position kinds. "hybrid" is required at the model level, not as a
#: distinct faction type: it is what keeps contradictions representable.
REQUIRED_KINDS = {"accelerationist", "critical", "doomer", "hybrid"}

#: The example formations issue #8 asked for, to prove non-obvious combinations.
REQUIRED_EXAMPLES = {
    "psionic-secessionists",   # pro-psionics / pro-NHI / anti-AI
    "accelerant-frontier",     # AI accelerationist / anti-NHI
    "green-refusal",           # ecological AI doomer / pro collective consciousness
    "corporate-transhumanists",  # corporate transhumanist / panpsychism skeptic
    "spiritual-contact",       # religious anti-cyborg / NHI as spiritual
    "public-robotics-left",    # left AI-critical / pro public robotics
    "cyborg-rights",           # cyborg rights / hostile to centralised AI
    "machine-standing",        # machine rights / sceptical of human BCI
}

#: Issue #95 names three camps in the AI paradigm shift and asks that the setting
#: contain "the full ideological spectrum rather than adopting one official answer".
#: The accelerationist pole was already represented; these two were not, so the guard
#: pins all three to the axis they belong to. Losing one silently would mean the
#: simulation could only reason about part of the spectrum the issue specifies.
REQUIRED_AI_CAMPS = {
    "accelerant-frontier": "accelerationist",
    "critical-ai-camp": "critical",
    "xrisk-camp": "doomer",
}


def load() -> dict:
    return json.loads(MODEL_PATH.read_text(encoding="utf-8"))


def test_model_parses_and_is_versioned() -> None:
    model = load()
    assert model["format"] == "noopunk.world.ideology"
    assert isinstance(model["version"], int) and model["version"] >= 1


def test_all_six_paradigm_axes_present() -> None:
    model = load()
    axes = {axis["id"] for axis in model["paradigm_axes"]}
    assert axes == REQUIRED_AXES, f"axis drift: {axes ^ REQUIRED_AXES}"


def test_time_convention_is_20xx() -> None:
    """AGENTS.md §6: canonical future dates are 20XX, never a concrete year."""
    model = load()
    assert model["time_convention"] == "20XX"


def test_every_faction_takes_a_position_on_every_axis() -> None:
    """The cross-product: no faction may leave an axis unaddressed.

    This is what makes positions separable. A faction silent on an axis could be
    read as taking whichever position the reader assumed, which is exactly the
    collapse the model prevents.
    """
    model = load()
    axes = REQUIRED_AXES
    for faction in model["factions"]:
        missing = axes - set(faction["positions"])
        assert not missing, f"{faction['id']} has no position on {sorted(missing)}"


def test_positions_use_only_declared_kinds() -> None:
    model = load()
    kinds = {kind["id"] for kind in model["position_kinds"]}
    assert kinds == REQUIRED_KINDS, f"kind drift: {kinds ^ REQUIRED_KINDS}"
    for faction in model["factions"]:
        for axis, position in faction["positions"].items():
            assert position["kind"] in kinds, (
                f"{faction['id']}.{axis} uses undeclared kind {position['kind']!r}"
            )


def test_positions_carry_a_summary_not_just_a_label() -> None:
    """A bare label is the morality-box failure the issue warns against."""
    model = load()
    for faction in model["factions"]:
        for axis, position in faction["positions"].items():
            summary = position.get("summary", "").strip()
            assert len(summary) > 20, (
                f"{faction['id']}.{axis} needs a substantive summary, not a label"
            )


def test_pcm_exists_as_a_major_noospheric_faction() -> None:
    """Issue #8 deliverable 1."""
    model = load()
    pcm = next((f for f in model["factions"] if f["id"] == "pcm"), None)
    assert pcm is not None, "PCM faction missing"
    assert pcm["role"] == "major_noospheric_actor"
    assert pcm.get("is_assemblage") is True
    # the common short forms the issue names
    assert "PCM" in pcm["common_names"]
    assert "the Multitude" in pcm["common_names"]


def test_pcm_has_internal_disagreement_and_tensions() -> None:
    """Issue #8: PCM must contain tendencies, not one unified ideology."""
    model = load()
    pcm = next(f for f in model["factions"] if f["id"] == "pcm")
    assert pcm["internal_tensions"], "PCM must carry unresolved internal questions"
    assert len(pcm["internal_tensions"]) >= 5
    # a faction that cannot become oppressive is a wish, not a faction
    assert any("oppressive" in t for t in pcm["internal_tensions"])
    # positions that are contested internally are marked as such
    contested = [a for a, p in pcm["positions"].items() if p.get("internal_disagreement")]
    assert len(contested) >= 3, "PCM should be internally split on several axes"


def test_pcm_positions_are_not_uniform() -> None:
    """If PCM held one kind on every axis it would be an ideology box, not a faction."""
    model = load()
    pcm = next(f for f in model["factions"] if f["id"] == "pcm")
    kinds = {p["kind"] for p in pcm["positions"].values()}
    assert len(kinds) >= 2, "PCM must not hold one uniform position kind"


def test_the_issue_95_ai_spectrum_is_represented() -> None:
    """Issue #95: the setting contains the full AI spectrum, not one official answer.

    The accelerationist pole was already present; the Critical AI and existential-risk
    camps were not, so the simulation could only reason about a third of the spectrum
    the issue specifies. Pin all three to the axis, and pin that they are genuinely
    different kinds rather than three labels for one position.
    """
    model = load()
    by_id = {f["id"]: f for f in model["factions"]}
    for faction_id, expected_kind in REQUIRED_AI_CAMPS.items():
        assert faction_id in by_id, f"missing AI-spectrum camp: {faction_id}"
        actual = by_id[faction_id]["positions"]["ai"]["kind"]
        assert actual == expected_kind, (
            f"{faction_id} should hold the {expected_kind!r} position on the ai axis, "
            f"found {actual!r}"
        )
    kinds = {by_id[f]["positions"]["ai"]["kind"] for f in REQUIRED_AI_CAMPS}
    assert len(kinds) == 3, f"the three camps collapsed into one position: {kinds}"


def test_required_example_combinations_exist() -> None:
    """Issue #8 §5: several factions with deliberately mixed positions."""
    model = load()
    ids = {f["id"] for f in model["factions"]}
    missing = REQUIRED_EXAMPLES - ids
    assert not missing, f"missing example formations: {sorted(missing)}"


def test_examples_demonstrate_a_cross_product_not_one_axis() -> None:
    """At least one faction must be enthusiastic on one axis and hostile on another.

    This is the single assertion that the world has not collapsed into
    pro-technology versus anti-technology.
    """
    model = load()
    found = False
    for faction in model["factions"]:
        kinds = {p["kind"] for p in faction["positions"].values()}
        if "accelerationist" in kinds and "doomer" in kinds:
            found = True
            break
    assert found, (
        "no faction combines accelerationist and doomer positions across axes; "
        "the ideological cross-product has collapsed"
    )


def test_no_consciousness_score_or_numeric_ideology() -> None:
    """Issue #8 defers numeric mechanics; AGENTS.md §4 reserves them."""
    model = load()
    for faction in model["factions"]:
        for axis, position in faction["positions"].items():
            for key in ("score", "value", "weight", "modifier"):
                assert key not in position, (
                    f"{faction['id']}.{axis} carries numeric {key!r}; "
                    "issue #8 defers numeric ideology mechanics"
                )


def test_shift_events_are_declared_and_axis_bound() -> None:
    """Issue #8 §8: events realign factions, on their own axis."""
    model = load()
    axes = REQUIRED_AXES
    events = model["paradigm_shift_events"]
    assert len(events) >= 8, "the event list should cover the paradigm shifts"
    for event in events:
        assert event["primary_axis"] in axes, (
            f"event {event['id']} binds to unknown axis {event['primary_axis']!r}"
        )


def test_runtime_guidance_names_all_three_runtimes() -> None:
    """One RPG, three runtimes (AGENTS.md §11)."""
    model = load()
    guidance = model["runtime_guidance"]
    for runtime in ("tabletop", "godot", "concordia"):
        assert runtime in guidance, f"runtime guidance missing for {runtime}"


def test_world_document_references_the_data_artefact() -> None:
    """The doc must point at the canonical data rather than restate it."""
    doc = (ROOT / "docs" / "archive" / "WORLD_IDEOLOGY.md").read_text(encoding="utf-8")
    assert "data/world/ideology.json" in doc, (
        "WORLD_IDEOLOGY.md must reference the canonical data artefact"
    )
    assert "20XX" in doc, "the world document must keep the 20XX convention"


def test_the_three_name_words_are_concepts_in_their_own_right() -> None:
    """Issue #8 deliverable 2: panpsychism, cyborg and multitude recur BEYOND PCM.

    A world where only PCM uses these three words has failed the integration, so
    the document must treat each as a general concept, not as the faction's name.
    """
    doc = (ROOT / "docs" / "archive" / "WORLD_IDEOLOGY.md").read_text(encoding="utf-8").lower()
    for word in ("panpsychism", "cyborg", "multitude"):
        assert word in doc, f"{word} is not treated anywhere in the world document"
    # the export list must name the three words as separate concepts
    model = load()
    pcm = next(f for f in model["factions"] if f["id"] == "pcm")
    exported = {c.lower() for c in pcm["concepts_exported_beyond_this_faction"]}
    assert {"panpsychism", "cyborg", "multitude"} <= exported, (
        "PCM must export panpsychism, cyborg and multitude as general concepts"
    )


def test_world_document_stays_gameable_not_a_paper() -> None:
    """Issue #8 §9: translate theory into play, not into exposition."""
    doc = (ROOT / "docs" / "archive" / "WORLD_IDEOLOGY.md").read_text(encoding="utf-8")
    for section in ("Playing it", "Simulation hooks", "Events change the map"):
        assert section in doc, f"world document lost its gameable section: {section}"


def test_pcm_has_external_relationships() -> None:
    """Issue #8 §6: PCM's relationship with the Noöspheric order, not just a stance.

    The first pass modelled PCM's positions but not its relationships, so the
    deliverable that lists governments, corporations, NHI contact groups,
    psionics organisations, anti-AI movements, ecological movements, security
    services, religious movements, anarchists and public institutions had no
    data behind it.
    """
    model = load()
    pcm = next(f for f in model["factions"] if f["id"] == "pcm")
    assert "external_relationships" in pcm, "PCM has no external relationships"
    relations = pcm["external_relationships"]
    required = {
        "noospheric_infrastructure",
        "human_communities",
        "ai_agents",
        "governments",
        "corporations",
        "nhi_contact_groups",
        "psionic_organisations",
        "transhumanists",
        "anti_ai_movements",
        "ecological_movements",
        "security_services",
        "religious_movements",
        "anarchists_autonomists",
        "public_institutions",
    }
    missing = required - set(relations)
    assert not missing, f"PCM relationships missing: {sorted(missing)}"
    for target, relation in relations.items():
        if target.startswith("$"):
            continue
        assert isinstance(relation, str) and len(relation) > 40, (
            f"PCM's relationship with {target} is a label, not a relationship"
        )


def test_every_event_says_how_it_realigns_factions() -> None:
    """Issue #8 §8: events must actually move factions, not just name an axis.

    `primary_axis` records which paradigm an event belongs to; on its own it does
    not say that anything REACTS to it, which is the deliverable ("After such
    events, factions should split, merge, radicalize, moderate, or change
    alliances").
    """
    model = load()
    kinds = {"split", "merge", "radicalise", "moderate", "realign"}
    for event in model["paradigm_shift_events"]:
        moves = event.get("realignments")
        assert moves, f"event {event['id']} realigns nothing"
        assert len(moves) >= 2, f"event {event['id']} moves fewer than two factions"
        for move in moves:
            assert move["kind"] in kinds, (
                f"event {event['id']} uses unknown realignment kind {move['kind']!r}"
            )
            assert move.get("who"), f"event {event['id']} names no faction it moves"
            assert move.get("what"), f"event {event['id']} does not say what changes"


def test_realignments_do_not_all_push_one_direction() -> None:
    """An event that moves everyone the same way is a reset button, not history.

    The model's whole point is that an event moves ITS OWN axis and leaves others
    alone, so the realignments across the set must include opposite directions.
    """
    model = load()
    kinds = [m["kind"] for e in model["paradigm_shift_events"]
             for m in e.get("realignments", [])]
    assert "split" in kinds and "radicalise" in kinds, (
        "realignments must include both splitting and radicalising"
    )
    assert len(set(kinds)) >= 3, "realignments are not using the range of outcomes"


if __name__ == "__main__":  # pragma: no cover - manual run convenience
    import sys

    failures = 0
    for name, fn in sorted(globals().items()):
        if name.startswith("test_") and callable(fn):
            try:
                fn()
                print(f"ok   {name}")
            except AssertionError as exc:
                failures += 1
                print(f"FAIL {name}: {exc}")
    print(f"\n{'FAILED' if failures else 'passed'}: {failures} failure(s)")
    sys.exit(1 if failures else 0)
