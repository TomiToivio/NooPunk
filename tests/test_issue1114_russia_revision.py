"""#1114: one playable timeline, and the Soviet-survival story demoted to evidence.

The failure this guards against already happened once: two mutually exclusive chronologies were both
written as fact, so the setting had a canonical USSR that survived *and* a canonical Russia that
collapsed. Canon pages are prose, so nothing here tests a schema — it tests the claims the pages are
allowed to make, and the ones they are not.
"""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CANON = ROOT / "docs" / "world" / "ALTERNATE_HISTORY_1114.md"
ANCHORS = ROOT / "docs" / "research" / "SOVIET_PSI_UFOLOGY_ANCHORS_1114.md"
TIMELINE = ROOT / "rulebook" / "7_TIMELINE.md"
POST_NHI = ROOT / "docs" / "world" / "POST_NHI_WORLD_1005.md"
EUROPOL = ROOT / "docs" / "world" / "EUROPOL_HELSINKI_1114.md"
DECISIONS = ROOT / "docs/design/AUTHOR_DECISION_QUEUE.md"
REGISTER = ROOT / "docs" / "DOCUMENT_REGISTER.md"


def text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def flat(path: Path) -> str:
    """Prose with markdown emphasis removed and wrapped lines joined, for phrase assertions."""
    raw = re.sub(r"(?m)^\s*>\s?", "", text(path))
    return re.sub(r"\s+", " ", re.sub(r"[*_`]", "", raw))


def test_the_canon_page_declares_one_playable_timeline() -> None:
    body = flat(CANON)
    assert "single authority" in body
    assert "one playable timeline" in body.lower()
    assert "not a second canon" in body
    assert "Status: canonical setting history" in body


def test_the_five_strata_are_named_and_explained() -> None:
    body = flat(CANON)
    for stratum in (
        "Playable-world baseline",
        "Accepted pre-collapse secret history",
        "Contested testimony",
        "Mandela-effect material",
        "Author-only unknowns",
    ):
        assert stratum in body, f"stratum missing: {stratum}"


def test_the_baseline_has_every_element_the_issue_requires() -> None:
    body = flat(CANON)
    required = {
        "USSR collapses": "The USSR collapses",
        "Ukraine independent": "Ukraine becomes independent",
        "Ukraine joins the EU": "Ukraine joins the European Union",
        "short EU-Russia war": "short EU–Russia war",
        "UAP nuclear interception": "UAPs intercept nuclear weapons",
        "failed state": "chaotic failed state",
        "fortified border": "border is closed and heavily fortified",
        "Europol employer": "Europol Helsinki Field Office",
        "UNSA limited": "not a world government",
    }
    for label, phrase in required.items():
        assert phrase in body, f"baseline missing {label}: {phrase!r}"


def test_the_soviet_survival_is_never_asserted_as_fact() -> None:
    """The old claim may appear only as a remembered or contradicted claim."""
    body = flat(CANON).split("## 8. What this supersedes")[0]
    forbidden = (
        "The Soviet Union never collapses",
        "the Soviet Union survives",
        "USSR survives the Cold War",
        "the Soviet Union does not dissolve",
    )
    for phrase in forbidden:
        assert phrase not in body, f"canon still asserts: {phrase!r}"
    # And the correction must be findable, not merely absent.
    assert "Mandela Effect" in body
    assert "not as verified rulers" in body


def test_programma_keeps_its_pre_collapse_baseline_and_its_unknowns() -> None:
    body = flat(CANON)
    for phrase in (
        "1950s",
        "closed city (ZATO)",
        "Komsomol",
        "Homo Sovieticus",
        "fourth-density Social Memory Complex",
        "hive mind",
        "ARVs",
        "1991",
        "rogue deep-state network",
    ):
        assert phrase in body, f"ПРОГРАММА baseline missing: {phrase!r}"
    # The programme must not be promoted into a solved organisation.
    assert "unresolved" in body.lower()


def test_mj12_and_programma_stay_unsolved_with_a_clue_ladder() -> None:
    body = flat(CANON)
    assert "MJ-12" in body
    assert "cannot be closed" in body
    for tier in ("Public documented research", "Cold War hearsay", "Intelligence allegation",
                 "Firsthand post-Crisis observation", "Ontological anomaly"):
        assert tier in body, f"clue tier missing: {tier}"


def test_the_law_of_one_is_a_source_claim_not_archaeology() -> None:
    body = flat(CANON)
    assert "source claim inside the fiction" in body
    assert "not verified history" in body


def test_the_anchor_sheet_separates_fact_claim_allegation_and_canon() -> None:
    body = flat(ANCHORS)
    for label in ("DOCUMENTED", "CLAIM", "ALLEGATION", "GAME CANON"):
        assert label in body, f"anchor label missing: {label}"
    for anchor in ("SETKA-MO / SETKA-AN", "Vasiliev", "Kazhinsky", "ZATO", "Voronezh", "8.6"):
        assert anchor in body, f"historical anchor missing: {anchor}"
    assert "Do not present SETKA as a secret NHI programme" in body


def test_the_rulebook_timeline_matches_the_revision() -> None:
    body = flat(TIMELINE)
    assert "The Soviet Union dissolves" in body
    assert "short EU–Russia war" in body
    assert "Mandela Effect" in body
    for stale in ("The Soviet Union survives, reforms", "ends without the USSR breaking"):
        assert stale not in body, f"rulebook still asserts: {stale!r}"


def test_the_superseded_world_page_carries_the_correction() -> None:
    body = flat(POST_NHI)
    assert "Soviet Union dissolved" in body
    assert "failed state" in body
    assert "Mandela Effect" in body


def test_helsinki_perception_is_named_as_an_in_universe_view() -> None:
    body = flat(EUROPOL)
    assert "in-universe EU public perception" in body
    assert "Russia does not dominate the opening campaign" in body


def test_the_register_names_one_authority_for_the_russia_question() -> None:
    body = text(REGISTER)
    rows = [line for line in body.splitlines() if "ALTERNATE_HISTORY_1114.md" in line]
    assert len(rows) == 1, "the register must list exactly one canonical setting-history page"
    assert "SOVIET_PSI_UFOLOGY_ANCHORS_1114.md" in body


def test_the_decision_queue_does_not_assert_soviet_survival() -> None:
    """D75 described the *old* canon long after the canon changed.

    A decision log that keeps a superseded premise is worse than no log: the next agent reads it as the
    current state of the question and writes a scene where the USSR still exists.
    """
    body = flat(DECISIONS)
    assert "The canon now fixes the USSR's survival" not in body
    assert "collapse of the USSR in 1991" in body or "collapsed in 1991" in body
    assert "Mandela-effect material" in body
