"""Ubiquitous Maniacs: playable non-canonical NoöPunk case.

Uses the live casework/Fate campaign runtime, not the archived game engine.
The treatment-lab premise is adapted from the author's older Ubiquitous Maniacs
material; scenes, dialogue and incident text here are original. No third-party
screenplay, transcript or fictional universe is imported.
"""
from __future__ import annotations

from ..campaign.case import Case
from ..rpg.fate import Action
from . import kallio
from .session import CaseSession
from .spec import ActionSpec, CaseFile, CheckSpec, ClueSpec, Cost, FindingSpec, ResolutionSpec, SceneSpec

CASE_ID = "hki-ubiquitous-maniacs-2045"
CASE = CaseFile(
    id=CASE_ID,
    title="Ubiquitous Maniacs: The Listening Ward",
    core_question="Did the research ward invent its anomalous patient, or did its records erase one?",
    hook="A closed neurological research ward sends UNSA a distress call through a disconnected terminal.",
    era="post_crisis",
    era_label="Helsinki, 2045 (optional side case)",
    scenes=(
        SceneSpec(
            id="arrival",
            title="A ward that should be empty",
            location="Helsinki, sealed research annex",
            prose=(
                "The annex was decommissioned three years ago. Its reception desk still "
                "prints tomorrow's appointments. An orderly insists that the patients were "
                "discharged; the attendance book contains sixteen entries in one handwriting. "
                "A maintenance console has no route to the Safenet. Someone inside keeps calling."
            ),
            actions=(
                ActionSpec(
                    id="inspect_register",
                    label="Examine the attendance book",
                    text="The ink ages differently from the paper. One patient identifier appears twice.",
                    check=CheckSpec(action=Action.OVERCOME, skill="COG", band="Fair"),
                    gives=("register",),
                    on_fail=Cost(complications=("records-tampered",)),
                ),
                ActionSpec(
                    id="question_orderly",
                    label="Interview the orderly",
                    text="The orderly remembers the evacuation but not who authorized it.",
                    check=CheckSpec(action=Action.OVERCOME, skill="SAV", band="Fair"),
                    gives=("register",),
                    on_fail=Cost(complications=("orderly-alarmed",)),
                ),
            ),
            aspects=("Decommissioned but occupied",),
        ),
        SceneSpec(
            id="records",
            title="The unconnected machine",
            location="Annex records room, isolated local terminal",
            prose=(
                "The console has no external link. Its spool records simultaneous neurological "
                "readings from two locations. A patient who appears in one record does not "
                "appear on the security roster. A voice on the intercom requests that nobody "
                "erase the final tape."
            ),
            actions=(
                ActionSpec(
                    id="compare_traces",
                    label="Compare the neurological traces",
                    text="Two instruments disagree about which person was in the chair.",
                    check=CheckSpec(action=Action.OVERCOME, skill="COG", band="Good"),
                    gives=("trace",),
                    on_fail=Cost(complications=("trace-corrupted",)),
                ),
                ActionSpec(
                    id="interview_patient",
                    label="Speak to the patient without prompting",
                    text="The patient describes a room that has been locked since the shutdown.",
                    check=CheckSpec(action=Action.OVERCOME, skill="WIL", band="Fair"),
                    gives=("testimony",),
                    on_fail=Cost(complications=("witness-distressed",)),
                ),
                ActionSpec(
                    id="reconcile_accounts",
                    label="Assemble an evidence record",
                    text="Compare the recorded names, measurements and first-person account.",
                    finding="finding-ward",
                ),
            ),
            aspects=("Isolated records terminal",),
        ),
    ),
    clues=(
        ClueSpec("register", "Contradictory register", "One identity is logged twice under different names."),
        ClueSpec("trace", "Parallel trace", "The equipment shows incompatible occupancy records."),
        ClueSpec("testimony", "Patient account", "The patient's experience cannot be confirmed by the cameras."),
    ),
    findings=(
        FindingSpec(
            id="finding-ward",
            label="Unresolved identity contradiction",
            text="The ward's official account is inconsistent; neither fraud nor PSI is proved.",
            requires_all=("register", "trace", "testimony"),
            partial_min=2,
        ),
    ),
    resolutions=(
        ResolutionSpec(
            id="closed_by_evidence",
            label="Preserve the ward's evidence",
            text="UNSA seals the originals and protects the patient's right to give evidence. "
                 "No metaphysical explanation is declared proven.",
            skill="COG",
            band="Fair",
            requires_finding="finding-ward",
            objective="Ward records preserved for independent review",
            reputation=("patient-consent-protected",),
            intel=("ward-identity-contradiction",),
        ),
        ResolutionSpec(
            id="closed_by_withdrawal",
            label="Refer the unexplained case",
            text="The team files a cautious report. The ward remains sealed, pending an "
                 "independent inquiry; no patient is declared a threat on this evidence.",
            skill="WIL",
            band="Average",
            objective="Ward anomaly referred for review",
            reputation=("ward-referral",),
            intel=("ward-incident-filed",),
        ),
    ),
    chain=("register", "trace", "testimony"),
    author_note="Optional non-canonical 2045 side scenario. Historical 16 Psyche / UFAB ideas are "
                "reinterpreted as fictional legacy research, not a new world-canon institution "
                "or an imported ruleset. All checks use existing NoöPunk casework mechanics.",
    detail={"status": "OPTIONAL SCENARIO, NOT CANON", "legacy_source": "archive/ubiquitous-maniacs-2026-10"},
)


def build_campaign():
    """Reuse the current five-seat UNSA roster and replace only its case assignment."""
    campaign = kallio.build_campaign()
    campaign.cases.clear()
    campaign.cases[CASE_ID] = Case(
        case_id=CASE_ID,
        core_question=CASE.core_question,
        hook=CASE.hook,
        investigator=campaign.leader_id,
        partner="laura_falk",
        controller="iida_ketonen",
        initial_scene="arrival",
        domain_leads={
            "physical": ["the abandoned annex", "the attendance register"],
            "cybernetic": ["the isolated local terminal"],
            "social": ["the orderly", "the patient"],
            "psychic_noospace": ["the incompatible first-person account"],
        },
        witnesses=["the orderly", "the patient"],
        contradictions=["the register lists one identity twice", "the instrument readings conflict"],
        faction_interests=["patient consent", "preservation of anomalous evidence"],
        possible_player_choices=["preserve evidence", "refer the case"],
        resolution_notes=["cause remains an open question; this is not a canon disclosure"],
    )
    campaign.factions[campaign.faction_id].objectives = [
        "Investigate the Listening Ward without prejudging the anomaly"
    ]
    return campaign


def build_session(*, seed: int = 502) -> CaseSession:
    """Return a live, seeded, saveable casework session."""
    return CaseSession(CASE, build_campaign(), seed=seed)
