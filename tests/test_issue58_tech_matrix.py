#!/usr/bin/env python3
"""Structure guard for the regional technology matrix (issue #58).

This is a STRUCTURE test, in the style of ``test_world_ideology.py``. It does not
check which region holds which value — that is the author's and may change — only
that the properties the issue relies on cannot be lost by a later session.

What is protected:

* the matrix exists, parses, and is versioned with the 20XX time convention;
* all thirteen dimensions are present and each is an ORDERED scale;
* every region carries a profile keyed on every dimension (a value or an explicit
  null), a posture, and at least one gain and one vulnerability;
* the ANTI-RANKING rule: no region is rankable as simply advanced, there is no
  scalar technology score anywhere, and every region has vulnerabilities;
* profile values are on their own dimension's scale (a typo cannot invent a value);
* the two rogue-AGI catastrophes exist and are ordered;
* the deliberately unresolved questions stay unresolved — the jinn question and
  Ganesh are recorded as in-world unknown with candidate readings, not settled;
* the issue's own "author decision" items are NOT answered;
* no rules leaked in: no modifier, cost, or numeric point value.
"""
from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MATRIX_PATH = ROOT / "data" / "world" / "tech_matrix.json"
DOC_PATH = ROOT / "docs" / "TECH_MATRIX.md"
TIMELINE_PATH = ROOT / "TIMELINE.md"

#: The thirteen dimensions the issue names. Losing one would drop a whole axis of
#: regional variation.
REQUIRED_DIMENSIONS = {
    "ai_autonomy", "robotics", "cybernetics", "bci", "biotech", "virtuality",
    "space", "energy", "manufacturing", "psionics", "noosphere", "governance",
    "ecology",
}

#: The seven regional sketches the issue specifies.
REQUIRED_REGIONS = {
    "united-states", "european-federation", "china", "russia",
    "middle-east", "india", "sub-saharan-africa",
}

#: The ideological postures the issue names.
REQUIRED_POSTURES = {"accelerationist", "ai_critical", "doomer_anti_ai", "hybrid"}

#: Words that would betray a scalar ranking of "advancedness". The design forbids one.
FORBIDDEN_SCALAR_KEYS = (
    "tech_score", "technology_score", "global_tech_level", "tech_level",
    "advancedness", "development_index", "tier",
)


def load() -> dict:
    return json.loads(MATRIX_PATH.read_text(encoding="utf-8"))


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def normalised(path: Path) -> str:
    """Lowercased, whitespace-collapsed, markdown emphasis stripped.

    Structural markers are stripped so a line-wrapped or emphasised phrase still
    matches, but the comparison characters are NOT touched.
    """
    return " ".join(re.sub(r"[>*_`]", " ", read(path)).split()).lower()


def test_the_matrix_exists_and_is_versioned() -> None:
    model = load()
    assert model["format"] == "noopunk.world.tech_matrix"
    assert isinstance(model["version"], int) and model["version"] >= 1


def test_time_convention_is_20xx() -> None:
    """AGENTS.md §6: canonical future dates are 20XX, never a concrete year."""
    model = load()
    assert model["time_convention"] == "20XX"
    assert not re.search(r"\b(20[2-9]\d)\b", read(MATRIX_PATH)), "a concrete year leaked in"


def test_all_thirteen_dimensions_are_present() -> None:
    model = load()
    ids = {d["id"] for d in model["dimensions"]}
    assert ids == REQUIRED_DIMENSIONS, f"dimension drift: {ids ^ REQUIRED_DIMENSIONS}"


def test_every_dimension_has_an_ordered_scale_of_at_least_two_values() -> None:
    """A dimension with one value would be a constant, not a dimension."""
    for dim in load()["dimensions"]:
        with_subtest = dim["id"]
        assert isinstance(dim.get("scale"), list), f"{with_subtest} has no scale"
        assert len(dim["scale"]) >= 2, f"{with_subtest} scale is degenerate: {dim['scale']}"
        assert len(set(dim["scale"])) == len(dim["scale"]), f"{with_subtest} scale has duplicates"


def test_all_seven_regions_are_present() -> None:
    model = load()
    ids = {r["id"] for r in model["regions"]}
    assert ids == REQUIRED_REGIONS, f"region drift: {ids ^ REQUIRED_REGIONS}"


def test_all_four_postures_are_defined() -> None:
    model = load()
    ids = {p["id"] for p in model["ideological_postures"]}
    assert ids == REQUIRED_POSTURES, f"posture drift: {ids ^ REQUIRED_POSTURES}"


def test_every_region_has_a_known_posture() -> None:
    model = load()
    known = {p["id"] for p in model["ideological_postures"]}
    for region in model["regions"]:
        assert region.get("posture") in known, f"{region['id']} has posture {region.get('posture')!r}"


def test_every_region_keys_every_dimension() -> None:
    """A missing key would be indistinguishable from 'not yet considered'."""
    model = load()
    dims = {d["id"] for d in model["dimensions"]}
    for region in model["regions"]:
        missing = dims - set(region["profile"])
        assert not missing, f"{region['id']} omits dimensions: {sorted(missing)}"


def test_every_profile_value_is_on_its_dimensions_scale() -> None:
    """A typo must not be able to invent a value."""
    model = load()
    scales = {d["id"]: d["scale"] for d in model["dimensions"]}
    for region in model["regions"]:
        for dim, value in region["profile"].items():
            if value is None:
                continue
            assert value in scales[dim], (
                f"{region['id']}.{dim} = {value!r} is not on the scale {scales[dim]}"
            )


def test_unassigned_dimensions_stay_null_rather_than_being_filled() -> None:
    """AGENTS.md §1: a blank stays blank and is reported, not 'helpfully' completed."""
    model = load()
    # China's sketch deliberately leaves several dimensions unspecified.
    china = next(r for r in model["regions"] if r["id"] == "china")
    unassigned = [d for d, v in china["profile"].items() if v is None]
    assert unassigned, "China's unassigned dimensions were filled in"
    assert len(unassigned) >= 3, f"only {len(unassigned)} unassigned; the sketch is vaguer than that"


# --- the anti-ranking rule: the heart of the issue -------------------------

def test_no_region_is_rankable_as_simply_advanced() -> None:
    """Every region must carry vulnerabilities, or the matrix became a ranking."""
    model = load()
    for region in model["regions"]:
        assert region.get("vulnerabilities"), f"{region['id']} lists no vulnerabilities"
        assert len(region["vulnerabilities"]) >= 1


def test_every_region_also_lists_gains() -> None:
    """The pair is the point: no region is purely deficient either."""
    for region in load()["regions"]:
        assert region.get("gains"), f"{region['id']} lists no gains"


def test_no_scalar_technology_score_exists() -> None:
    raw = read(MATRIX_PATH)
    for forbidden in FORBIDDEN_SCALAR_KEYS:
        assert forbidden not in raw, f"a scalar ranking key leaked in: {forbidden!r}"


def test_the_design_rule_states_the_anti_ranking_principle() -> None:
    model = load()
    rule = model["design_rule"].lower()
    assert "not" in rule and ("equipment progression" in rule or "ranking" in rule)


def test_the_doc_does_not_rank_regions() -> None:
    """A prose ranking would defeat the data-level guarantee."""
    text = normalised(DOC_PATH)
    for phrase in ("most advanced region", "least advanced region",
                   "most advanced country", "behind the others"):
        assert phrase not in text, f"the doc ranks regions: {phrase!r}"


# --- the two catastrophes --------------------------------------------------

def test_both_rogue_agi_catastrophes_are_recorded() -> None:
    model = load()
    events = model.get("rogue_agi_catastrophes", [])
    assert len(events) == 2, f"expected two catastrophes, found {len(events)}"
    assert {e["ordinal"] for e in events} == {1, 2}


def test_the_catastrophes_are_ordered_by_severity() -> None:
    """The first was contained and read as a success; the second devastated the US."""
    events = {e["ordinal"]: e for e in load()["rogue_agi_catastrophes"]}
    assert events[1]["severity"] == "contained"
    assert events[2]["severity"] != "contained"
    assert "emp" in events[2]["resolution"].lower()


def test_the_timeline_records_the_two_event_supersession() -> None:
    """The change must be visible in the timeline, not only in a new data file."""
    text = normalised(TIMELINE_PATH)
    assert "superseded" in text
    assert "#58" in read(TIMELINE_PATH)
    assert "first rogue agi" in text
    assert "second rogue agi" in text


def test_company_attributions_are_marked_as_setting_fiction() -> None:
    """The issue warns these are not claims about the real world.

    The disclaimer appears in MORE THAN ONE place (the top-level epistemic note and
    each catastrophe). A plain substring check therefore passes even after one
    occurrence is stripped, so this asserts EVERY occurrence is negated: the guard
    must cover all of them, not the first.
    """
    model = load()
    for event in model["rogue_agi_catastrophes"]:
        assert "$attribution_note" in event, f"{event['id']} has no attribution note"
        assert event["epistemic_status"] == "noopunk_extrapolation"

    raw = read(MATRIX_PATH)
    claims = re.findall(r"(\w+\s+){0,3}claims about the real", raw)
    assert claims, "the 'not claims about the real world' disclaimer disappeared entirely"
    unnegated = [c for c in claims if "not " not in c]
    assert not unnegated, f"a disclaimer lost its negation: {unnegated}"
    assert len(claims) >= 3, f"only {len(claims)} disclaimers remain; some were stripped"


# --- unresolved stays unresolved -------------------------------------------

def test_the_jinn_question_stays_unresolved() -> None:
    model = load()
    middle_east = next(r for r in model["regions"] if r["id"] == "middle-east")
    jinn = middle_east["jinn"]
    assert jinn["resolution"] == "in_world_unknown"
    assert len(jinn["candidate_readings"]) >= 4, "the competing readings were pruned"


def test_ganesh_stays_unresolved() -> None:
    model = load()
    india = next(r for r in model["regions"] if r["id"] == "india")
    assert india["ganesh"]["resolution"] == "in_world_unknown"
    note = india["ganesh"]["$resolution_note"].lower()
    assert "deliberately" in note


def test_ganesh_statement_is_kept_verbatim_in_the_doc() -> None:
    text = normalised(DOC_PATH)
    assert "ganesh has returned" in text


# --- author decisions are left alone ---------------------------------------

def test_the_matrix_does_not_assign_an_exact_era() -> None:
    text = normalised(DOC_PATH)
    assert "20xx" in text
    assert not re.search(r"\b20(4[6-9]|5\d)\b", text), "an exact future year was assigned"


def test_the_matrix_defines_no_rules() -> None:
    """AGENTS.md §4: equipment statistics, economy and simulation mechanics are unresolved."""
    model = load()
    guidance = model["gameplay_guidance"]
    # the guidance is narrative: it must carry no numbers at all
    serialised = json.dumps(guidance, ensure_ascii=False)
    assert not re.search(r"\bmodifier\b|\bpoint cost\b|\bdice\b|\+\d\b", serialised, re.I), (
        "the gameplay guidance invented a rule"
    )
    assert "not rules" in guidance["$comment"].lower()


def test_the_runtime_guidance_is_per_runtime_and_defers_the_rest() -> None:
    model = load()
    guidance = model["runtime_guidance"]
    for key in ("shared", "tabletop", "godot", "concordia", "not_yet"):
        assert key in guidance, f"runtime guidance missing {key!r}"
    assert "author" in guidance["not_yet"].lower()


def test_the_doc_links_the_canonical_data_and_related_documents() -> None:
    text = read(DOC_PATH)
    assert "data/world/tech_matrix.json" in text
    assert "TIMELINE.md" in text
    assert "ideology.json" in text


if __name__ == "__main__":
    import sys

    failures = 0
    for name, fn in sorted(globals().items()):
        if name.startswith("test_") and callable(fn):
            try:
                fn()
                print(f"PASS {name}")
            except AssertionError as exc:
                failures += 1
                print(f"FAIL {name}: {exc}")
    print(f"\n{'OK' if not failures else 'FAILED'} ({failures} failures)")
    sys.exit(1 if failures else 0)
