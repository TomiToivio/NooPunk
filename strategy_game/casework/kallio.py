"""The packaged case: *The Second Shadow* — Kallio, Helsinki, 2045 (issue #502, Phase 1 content).

**Status: authored scenario content, not canon.** The case uses the canonical frame and nothing
more: the 2045 campaign present, the Helsinki Field Office, UNSA, the post-Crisis network (the
quarantined old Internet behind the Blackwall, fast local networks, the slow managed Safenet) and
the escalating Reptilian raids of `rulebook/20_FIRST_CONTACT_AND_PSI_AWAKENING.md` §5 beat 9. The
incident, every person in it and its outcome are **fiction written for this vertical slice**. No name,
place or event here becomes setting canon, and the four agents around the PC are the canonical party
of `rulebook/NEW_EDITION.md` with **placeholder sheets** — their ratings are playtest values, exactly
as that document says of its own first case.

The case takes the opening dilemma the rulebook already poses — *"a credible victim of a Reptilian
raid possesses a Grey cortical stack, while the first independent psi-sensitive witness remembers an
event that never appeared on any camera"* — and makes it playable: the raid is real, the second
figure is not a raider, and the party has to decide what can be proved before noon.

    python -m strategy_game.casework --route investigate
"""
from __future__ import annotations

from ..campaign.case import Case
from ..campaign.state import Campaign, CampaignFaction
from ..characters import Tag
from ..rpg.fate import Action, Character
from .spec import (
    ActionSpec,
    CaseFile,
    CheckSpec,
    ClueSpec,
    Cost,
    CyberGate,
    FindingSpec,
    PsiGate,
    ResolutionSpec,
    SceneSpec,
)

__all__ = [
    "AGENT_IDS",
    "CASE",
    "CASE_ID",
    "FACTION_ID",
    "LEADER_ID",
    "WITNESS_ID",
    "build_campaign",
    "build_session",
]

CASE_ID = "hki-kallio-2045"
FACTION_ID = "player-faction"
LEADER_ID = "pc_leader"
AGENT_IDS = ("laura_falk", "harri_romppainen", "sebastian_virtanen", "laura_univaara")
WITNESS_ID = "aino_rautio"
SUSPECT_ID = "vesa_lahtinen"

#: The three facts the chain is assembled from, in the order the reasoning meets them.
CHAIN = ("stack-manifest", "camera-gap", "impression-double")

#: Fate's own mild consequence. A named injury, never a number on a faction book.
MILD = 2


# -- the party ---------------------------------------------------------------------------------

def _leader() -> Character:
    return Character(
        id=LEADER_ID,
        name="You",
        aspects=[
            "Faction leader of the Helsinki Field Office",
            "I signed for every person on this floor",
            "The noonday briefing is mine to walk into",
        ],
        skills={"COG": 2, "INT": 2, "REF": 2, "SAV": 4, "SOM": 1, "WIL": 3},
        fate_points=3,
        tags=(Tag("goal", "close the Kallio raid case before the noonday briefing"),),
    )


def _agents() -> dict[str, Character]:
    return {
        "laura_falk": Character(
            id="laura_falk",
            name="Laura Falk (Minerva)",
            aspects=[
                "Academy newcomer, three months in the Field Office",
                "Determined to be useful before she is careful",
                "Reads people faster than paperwork",
            ],
            skills={"COG": 3, "INT": 2, "REF": 1, "SAV": 3, "SOM": 1, "WIL": 2},
        ),
        "harri_romppainen": Character(
            id="harri_romppainen",
            name="Dr. Harri Romppainen (Dirty Harry)",
            aspects=[
                "Veteran of Ö-Mappi, transferred with the Supo team",
                "Reads the report before the room",
                "Has seen a stack lie before",
            ],
            skills={"COG": 4, "INT": 2, "REF": 1, "SAV": 1, "SOM": 1, "WIL": 2},
            tags=(Tag("competence", "forensic medicine"),),
        ),
        "sebastian_virtanen": Character(
            id="sebastian_virtanen",
            name="Sebastian Virtanen (Ukuli)",
            aspects=[
                "Veteran of Ö-Mappi",
                "Trusts a local route over a warrant",
                "Never met a building he could not read",
            ],
            skills={"COG": 2, "INT": 3, "REF": 3, "SAV": 1, "SOM": 2, "WIL": 1},
            tags=(Tag("competence", "local-access intrusion"),),
        ),
        "laura_univaara": Character(
            id="laura_univaara",
            name="Laura Univaara (Hecate)",
            aspects=[
                "Veteran of Ö-Mappi",
                "Carries the office's harder conversations",
                "Will not call a person unreliable for being frightened",
            ],
            skills={"COG": 1, "INT": 2, "REF": 1, "SAV": 3, "SOM": 1, "WIL": 4},
        ),
    }


def _witness() -> Character:
    """The psi-sensitive caretaker. Her capability is hers, not an agent's: the party supervises."""
    return Character(
        id=WITNESS_ID,
        name="Aino Rautio",
        aspects=[
            "Night caretaker of the Kallio building",
            "Saw a figure that had no breath",
            "Testified once before and was not believed",
        ],
        skills={"COG": 2, "INT": 3, "REF": 1, "SAV": 2, "SOM": 1, "WIL": 3},
        natural_psi=True,
        psi_abilities=["telepathic impression"],
        tags=(Tag("competence", "TELEPATH"),),
    )


def _suspect() -> Character:
    """The stores clerk. Not a fighter: a man with a cutter and a reason to leave."""
    return Character(
        id=SUSPECT_ID,
        name="Vesa Lahtinen",
        aspects=[
            "Field Office logistics clerk, eleven years of signatures",
            "Owes money to a clinic with Orion clients",
            "Would rather run than be arrested",
        ],
        skills={"COG": 2, "INT": 2, "REF": 2, "SAV": 3, "SOM": 2, "WIL": 2},
    )


# -- the case ----------------------------------------------------------------------------------

_BRIEFING = SceneSpec(
    id="briefing",
    title="The Kallio stairwell",
    location="Helsinki Field Office, operations floor — 06:20",
    prose=(
        "The night report is four hours old and already too clean. At 05:40 a Reptilian raid hit a "
        "UNSA relocation building in Kallio: two dead, one injured, one raider dead on the rear "
        "stair. The duty officer has written 'raider infiltration' in the attribution field and left "
        "it for you to sign.\n\n"
        "Two things do not fit. A resident, Nila Ahola, is in the secure ward carrying a Grey "
        "cortical stack she says she never agreed to. And the building's night caretaker insists "
        "there was a second figure on the stair — one the camera never recorded.\n\n"
        "The UNSA liaison wants an attribution before the noonday briefing. You have five people "
        "and one morning."
    ),
    actions=(
        ActionSpec(
            id="read_the_duty_log",
            label="Read the duty log against the raid clock",
            text=(
                "The raid begins at 05:40:12. The stairwell camera loses forty-one seconds from "
                "05:40:58, and the log calls it 'signal loss'. Everything else in the building "
                "recorded without a gap."
            ),
            check=CheckSpec(Action.OVERCOME, "COG", "Fair"),
            gives=("raid-log",),
            intel=("duty-log-gap",),
            on_tie=Cost(complications=("duty-log-thin",)),
            on_fail=Cost(complications=("duty-log-incomplete",), stress=1, mental=True),
            suggested_actor="harri_romppainen",
        ),
        ActionSpec(
            id="take_the_liaison_aside",
            label="Take the liaison aside before she drafts the attribution",
            text=(
                "Iida Ketonen has the noon statement half-written. She will hold it for two hours "
                "if you give her a reason she can defend upstairs — and she will remember being "
                "asked."
            ),
            check=CheckSpec(Action.OVERCOME, "SAV", "Average"),
            gives=("liaison-deadline",),
            intel=("unsa-wants-attribution",),
            on_tie=Cost(complications=("liaison-impatient",)),
            on_fail=Cost(complications=("liaison-doubt",)),
            suggested_actor=LEADER_ID,
        ),
        ActionSpec(
            id="hold_the_attribution",
            label="Refuse to sign the attribution yet",
            text=(
                "You do not sign. Ketonen's jaw tightens, but the field stays blank and the morning "
                "stays yours — for as long as you can carry it."
            ),
            check=CheckSpec(Action.CREATE_ADVANTAGE, "WIL", "Average"),
            aspect="Room to work",
            on_tie=Cost(complications=("deadline-tightened",)),
            on_fail=Cost(complications=("deadline-tightened", "liaison-doubt")),
            suggested_actor=LEADER_ID,
        ),
    ),
)

_VICTIM = SceneSpec(
    id="victim",
    title="The woman with the stores unit",
    location="Meilahti university clinic, secure ward — 07:05",
    prose=(
        "Nila Ahola is thirty-four and works nights cleaning offices four streets from the building "
        "that was raided. She was on the stair because the lift was out. She has a dressing on her "
        "neck and a Grey cortical stack under it, and she has been told by two doctors that the "
        "implant is 'a standard continuity device'.\n\n"
        "She keeps saying the same thing: she never signed for it."
    ),
    actions=(
        ActionSpec(
            id="interview_nila",
            label="Sit with Nila and let her tell it twice",
            text=(
                "She has the implant registration card in her coat. Serial GS-4471-08. She was "
                "given it in the stairwell, by someone she thought was a medic, while the shooting "
                "was still going on."
            ),
            check=CheckSpec(Action.OVERCOME, "SAV", "Fair"),
            gives=("stack-card",),
            intel=("nila-account",),
            on_tie=Cost(complications=("nila-guarded",)),
            on_fail=Cost(complications=("nila-withdraws",), stress=1, mental=True),
            suggested_actor="laura_falk",
        ),
        ActionSpec(
            id="scan_the_stack",
            label="Scan the unit against the stores registry",
            text=(
                "The serial is not a personal continuity unit. GS-4471 belongs to a decommissioned "
                "UNSA medical stores batch: telemetry units, issued to clinics, never to people. "
                "Somebody put a recorder in her and called it a backup."
            ),
            check=CheckSpec(Action.OVERCOME, "COG", "Good"),
            requires=("stack-card",),
            gives=("stack-manifest",),
            intel=("stores-batch-serial",),
            on_tie=Cost(complications=("clinic-logged-the-scan",)),
            on_fail=Cost(complications=("clinic-logged-the-scan",), stress=2, mental=True),
            suggested_actor="harri_romppainen",
        ),
        ActionSpec(
            id="ask_the_clinic",
            label="Ask the clinic what they were told",
            text=(
                "The duty nurse is apologetic and precise: the unit was not ordered for the "
                "patient. It came up from the stores depot with a batch number and a signature, and "
                "the ward was told to call it a continuity device."
            ),
            check=CheckSpec(Action.OVERCOME, "SAV", "Fair"),
            requires=("stack-card",),
            gives=("stack-manifest",),
            intel=("clinic-told-her-it-was-standard",),
            on_tie=Cost(complications=("clinic-nurse-nervous",)),
            on_fail=Cost(complications=("clinic-nurse-nervous",), stress=1, mental=True),
            suggested_actor="laura_falk",
        ),
        ActionSpec(
            id="promise_protection",
            label="Promise her the Field Office's protection",
            text=(
                "You put the faction's name behind her. She believes you, which is the problem: "
                "the promise is now on the record whether or not you can keep it."
            ),
            check=CheckSpec(Action.CREATE_ADVANTAGE, "SAV", "Average"),
            aspect="Nila's trust",
            intel=("shelter-requested",),
            on_tie=Cost(complications=("protection-promised",)),
            on_fail=Cost(complications=("protection-promised", "nila-guarded")),
            suggested_actor="laura_univaara",
        ),
    ),
)

_STAIRWELL = SceneSpec(
    id="stairwell",
    title="Forty-one seconds",
    location="Kallio, the relocation building's rear stair — 08:10",
    prose=(
        "The building smells of burnt polymer and disinfectant. The dead raider has been zipped and "
        "taken; the claw strikes in the door frame have not. Two floors up, a maintenance hatch is "
        "sealed with a Field Office tag dated this morning.\n\n"
        "The camera looks straight down the stair and sees nothing between 05:40:58 and 05:41:39."
    ),
    actions=(
        ActionSpec(
            id="read_the_stairwell",
            label="Walk the stair and time it against the gap",
            text=(
                "The gap is not a cut. It is a maintenance-mesh window: the building's own mesh "
                "took the stairwell camera offline for a service check at 05:41. The building logged "
                "it, because the building logs everything."
            ),
            check=CheckSpec(Action.OVERCOME, "INT", "Fair"),
            gives=("camera-gap",),
            intel=("camera-gap-is-a-fault",),
            on_tie=Cost(complications=("supervisor-watching",)),
            on_fail=Cost(complications=("supervisor-watching",), stress=1, mental=True),
            suggested_actor="sebastian_virtanen",
        ),
        ActionSpec(
            id="pull_the_mesh_log",
            label="Pull the maintenance mesh's own log",
            text=(
                "The mesh is local-only: no public network reaches it, and the old Internet is "
                "behind the Blackwall. Ukuli goes in through the field port in the basement, and "
                "the building's service ticket does the rest."
            ),
            check=CheckSpec(Action.OVERCOME, "COG", "Fair"),
            requires=("raid-log",),
            gives=("camera-gap",),
            intel=("mesh-maintenance-window", "mesh-service-ticket"),
            cyber=CyberGate(
                target_class="local_only",
                era="after_crisis",
                path="field_netrunner",
                local_presence=True,
                note=(
                    "the mesh cannot be reached remotely in any era; the question is answered "
                    "before the roll, not by the roll"
                ),
            ),
            on_tie=Cost(complications=("mesh-flagged-the-port",)),
            on_fail=Cost(complications=("mesh-flagged-the-port",), stress=1, mental=True),
            suggested_actor="sebastian_virtanen",
        ),
        ActionSpec(
            id="search_the_landing",
            label="Search the landing below the camera",
            text=(
                "Three claw strikes in the door frame, one of them through a steel hinge. Whatever "
                "else happened here, the raid was real: something with a Reptilian's reach came up "
                "these stairs and was fought."
            ),
            check=CheckSpec(Action.OVERCOME, "INT", "Average"),
            gives=("claw-mark",),
            intel=("raid-was-real",),
            on_tie=Cost(complications=("scene-contaminated",)),
            on_fail=Cost(complications=("scene-contaminated",)),
            suggested_actor="harri_romppainen",
        ),
    ),
)

_WITNESS = SceneSpec(
    id="witness",
    title="A shape worn like a coat",
    location="Aino Rautio's flat, Kallio — 09:00",
    prose=(
        "Aino Rautio is sixty-one and has been the building's night caretaker for nine years. She "
        "is calm until she describes the second figure, and then she is not.\n\n"
        "'It came up the stair behind the first one. It had the shape right. It did not breathe. "
        "When it turned, the air did not move.'\n\n"
        "She has testified once before, about a death in a stairwell in 2041, and the report called "
        "her impression 'unreliable narrative'."
    ),
    actions=(
        ActionSpec(
            id="supervise_the_reading",
            label="Supervise her reading of the stairwell",
            text=(
                "Univaara keeps the room quiet and holds the frame while Aino walks the stair again "
                "in her memory. What comes back is not a raider: no breath, no heat, a silhouette "
                "held up by something else."
            ),
            check=CheckSpec(Action.OVERCOME, "WIL", "Good", mental=True),
            psi=PsiGate(witness_id=WITNESS_ID, capability="TELEPATH"),
            gives=("impression-double",),
            intel=("psi-impression",),
            on_tie=Cost(stress=1, mental=True),
            on_fail=Cost(
                stress=MILD, mental=True, consequence="A nail behind the eyes"
            ),
            suggested_actor="laura_univaara",
        ),
        ActionSpec(
            id="check_the_thermal_record",
            label="Check the thermal record against her account",
            text=(
                "The stairwell's thermal log shows two warm bodies at 05:41 — the raider and the "
                "woman. If a third figure walked up that stair, it was not warm and it was not "
                "breathing."
            ),
            check=CheckSpec(Action.OVERCOME, "COG", "Fair"),
            gives=("impression-double",),
            intel=("thermal-two-bodies",),
            on_tie=Cost(complications=("thermal-log-sealed",)),
            on_fail=Cost(complications=("thermal-log-sealed",), stress=1, mental=True),
            suggested_actor="harri_romppainen",
        ),
        ActionSpec(
            id="ask_her_why_she_stayed",
            label="Ask her why she stayed on the stair",
            text=(
                "She stayed because the woman was screaming and nobody else was coming. She wants "
                "one thing in exchange for the statement: that the record uses her name."
            ),
            check=CheckSpec(Action.OVERCOME, "SAV", "Average"),
            gives=("witness-fear",),
            intel=("witness-prior-testimony",),
            on_tie=Cost(complications=("witness-frightened",)),
            on_fail=Cost(complications=("witness-frightened",), stress=1, mental=True),
            suggested_actor="laura_falk",
        ),
    ),
)

_RESOLUTION = SceneSpec(
    id="resolution",
    title="Before noon",
    location="Field Office operations floor, and a loading bay two blocks east — 11:40",
    prose=(
        "The stores batch has a signature on it: V. Lahtinen, logistics, eleven years in this "
        "building. He is on shift at the loading bay until twelve.\n\n"
        "Ketonen is upstairs with the draft statement. Whatever you do now, the noon briefing will "
        "say something, and it will be your name under it."
    ),
    actions=(
        ActionSpec(
            id="assemble_the_chain",
            label="Put the three facts on one board",
            text=(
                "A stores telemetry unit in a woman's neck. A camera gap the building logged itself. "
                "A figure with no breath and no heat. The conclusion is not in any one of them."
            ),
            finding="finding-empty-sleeve",
            suggested_actor=LEADER_ID,
        ),
        ActionSpec(
            id="pull_the_batch_signout",
            label="Pull the batch sign-out",
            text=(
                "GS-4471-08 left the stores registry on a signed requisition. The signature is Vesa "
                "Lahtinen's, and the receiving clinic is Orion-aligned."
            ),
            check=CheckSpec(Action.OVERCOME, "COG", "Fair"),
            requires=("stack-manifest",),
            gives=("batch-signature",),
            intel=("lahtinen-requisition",),
            on_tie=Cost(complications=("stores-clerk-alerted",)),
            on_fail=Cost(complications=("stores-clerk-alerted",), stress=1, mental=True),
            suggested_actor="harri_romppainen",
        ),
        ActionSpec(
            id="read_his_file",
            label="Read Lahtinen's personnel file",
            text=(
                "Two reprimands for unauthorised registry access, both dropped. A brother in a "
                "clinic that lists Orion clients. A man with eleven years of signatures and a "
                "reason to need money this month."
            ),
            check=CheckSpec(Action.OVERCOME, "INT", "Average"),
            requires=("batch-signature",),
            intel=("lahtinen-file",),
            on_tie=Cost(complications=("personnel-flagged-the-read",)),
            on_fail=Cost(complications=("personnel-flagged-the-read",)),
            suggested_actor="sebastian_virtanen",
        ),
        ActionSpec(
            id="brief_the_liaison_early",
            label="Brief Ketonen before she drafts the statement",
            text=(
                "You give her the shape of it without the conclusion, and she starts writing the "
                "statement you can actually defend."
            ),
            check=CheckSpec(Action.CREATE_ADVANTAGE, "SAV", "Fair"),
            aspect="The liaison is listening",
            on_tie=Cost(complications=("liaison-impatient",)),
            on_fail=Cost(complications=("liaison-doubt",)),
            suggested_actor=LEADER_ID,
        ),
    ),
)

CASE = CaseFile(
    id=CASE_ID,
    title="The Second Shadow",
    core_question=(
        "Was the second figure on the Kallio stair a Reptilian raider — or a body somebody wanted "
        "UNSA to see?"
    ),
    hook=(
        "A Reptilian raid in Kallio leaves two dead and one woman carrying a Grey cortical stack she "
        "never consented to. The only independent witness remembers a second figure that no camera "
        "recorded."
    ),
    era="after_crisis",
    era_label="2045, the Quarantine in force: the old Internet behind the Blackwall",
    scenes=(_BRIEFING, _VICTIM, _STAIRWELL, _WITNESS, _RESOLUTION),
    clues=(
        ClueSpec(
            "raid-log",
            "Duty log and the raid clock",
            "The raid begins at 05:40:12; the stairwell camera loses forty-one seconds from "
            "05:40:58 and nothing else in the building does.",
        ),
        ClueSpec(
            "liaison-deadline",
            "The noon attribution",
            "UNSA wants 'raider infiltration' signed before the noonday briefing, and will hold the "
            "statement for two hours if the reason is defensible.",
        ),
        ClueSpec(
            "stack-card",
            "Implant registration card",
            "Nila Ahola's card: serial GS-4471-08, issued in the stairwell during the shooting by "
            "someone she took for a medic.",
        ),
        ClueSpec(
            "stack-manifest",
            "A stores unit, not a backup",
            "GS-4471 belongs to a decommissioned UNSA medical stores batch — telemetry units issued "
            "to clinics, never to people.",
        ),
        ClueSpec(
            "camera-gap",
            "The logged maintenance window",
            "The forty-one-second gap is the building's own maintenance mesh taking the stairwell "
            "camera offline for a service check at 05:41. It is logged, not hidden.",
        ),
        ClueSpec(
            "claw-mark",
            "Claw strikes in the door frame",
            "Three strikes, one through a steel hinge: the raid itself was real, whatever else was "
            "on that stair.",
        ),
        ClueSpec(
            "impression-double",
            "A figure with no breath",
            "The caretaker's impression and the thermal record agree: a third silhouette on the "
            "stair, with no breath and no body heat.",
        ),
        ClueSpec(
            "witness-fear",
            "Why she stayed",
            "She stayed because the woman was screaming. She wants the record to use her name.",
        ),
        ClueSpec(
            "batch-signature",
            "The requisition signature",
            "GS-4471-08 left the registry on Vesa Lahtinen's signature, consigned to an "
            "Orion-aligned clinic.",
        ),
    ),
    findings=(
        FindingSpec(
            id="finding-empty-sleeve",
            label="An empty sleeve, worn during a real raid",
            text=(
                "The unit in Nila Ahola is a decommissioned stores telemetry unit, not a backup. "
                "The camera's forty-one missing seconds are a maintenance-mesh window the building "
                "logged itself. And the third figure on the stair had no breath and no heat. "
                "So the second 'raider' was an empty Grey sleeve, driven up the building's own "
                "service mesh during a real attack, and its work was to put a recorder into a woman "
                "nobody would believe. The raid was real. The second shadow was staged."
            ),
            requires_all=("stack-manifest", "camera-gap", "impression-double"),
            partial_min=2,
            partial_complication="unproven-chain",
        ),
    ),
    resolutions=(
        ResolutionSpec(
            id="closed_by_evidence",
            label="Close it on the record",
            text=(
                "You walk into the noon briefing with the chain on one page and the requisition "
                "number on the next. Ketonen reads it twice and signs the statement without the "
                "word 'infiltration' in it. UNSA gets a case it can defend; the clinic gets a "
                "letter; Nila Ahola gets a name in the record."
            ),
            skill="SAV",
            band="Good",
            requires_finding="finding-empty-sleeve",
            objective="Kallio raid case closed on the record",
            reputation=("unsa-field-office-trust",),
            on_fail_reputation=("unsa-field-office-doubt",),
            intel=("kallio-statement-corrected",),
        ),
        ResolutionSpec(
            id="closed_by_confrontation",
            label="Take it to the loading bay",
            text=(
                "Lahtinen is halfway through a signature when you come in. He does not ask how you "
                "found him; he asks whether the woman is alive. The controller is in his coat "
                "pocket, still warm from the mesh. He comes quietly, which is its own kind of "
                "confession."
            ),
            skill="SAV",
            band="Great",
            requires_finding="finding-empty-sleeve",
            requires=("batch-signature",),
            requires_fragments=2,
            opposed_by=SUSPECT_ID,
            consequence="Cutter wound, left forearm",
            objective="Kallio raid case closed with a detention",
            reputation=("unsa-field-office-trust", "kallio-residents-wary"),
            intel=("lahtinen-in-custody",),
            resources=("grey-sleeve-controller",),
        ),
        ResolutionSpec(
            id="closed_by_withdrawal",
            label="Refer it and walk away",
            text=(
                "You write four pages for Internal Affairs, attach the card and the mesh ticket, "
                "and hand it to a duty officer who will sit on it for a month. The noon statement "
                "says 'under review'. Nila Ahola keeps the unit in her neck and the promise in the "
                "record, and you keep the fact that you could have walked into that loading bay."
            ),
            skill="WIL",
            band="Average",
            objective="Kallio raid case referred to Internal Affairs",
            reputation=("internal-affairs-referral",),
            on_fail_reputation=("internal-affairs-referral", "case-left-open"),
            intel=("case-referred",),
        ),
    ),
    chain=CHAIN,
    author_note=(
        "Non-canonical scenario content for the #502 vertical slice. The frame is canon (2045, "
        "Helsinki Field Office, UNSA, the post-Crisis network, the Reptilian raids); the incident and "
        "its people are fiction. Character ratings are placeholder playtest values, not canon sheets."
    ),
    detail={
        "status": "AUTHORED SCENARIO CONTENT - NOT CANON",
        "design_record": "strategy_game/docs/RPG_FIRST_CASE.md",
        "refs": ["#502", "#461", "#482", "#516"],
    },
)


# -- the campaign the case is played on ----------------------------------------------------------

def build_campaign() -> Campaign:
    """A fresh campaign holding the five-seat roster, the case record, and the two NPCs.

    The faction is the player's own, not one of the authored global factions: naming a canonical
    faction here would put words in the setting's mouth. The NPC sheets live on the campaign so that
    a witness's stress and a suspect's consequences survive ``save_campaign`` too.
    """
    sheets = {LEADER_ID: _leader(), **_agents(), WITNESS_ID: _witness(), SUSPECT_ID: _suspect()}
    return Campaign(
        faction_id=FACTION_ID,
        leader_id=LEADER_ID,
        sheets=sheets,
        factions={
            FACTION_ID: CampaignFaction(
                identifier=FACTION_ID,
                name="The player's faction",
                leader_id=LEADER_ID,
                member_ids=[LEADER_ID, *AGENT_IDS],
                objectives=["Close the Kallio raid case before the noonday briefing"],
            )
        },
        cases={
            CASE_ID: Case(
                case_id=CASE_ID,
                core_question=CASE.core_question,
                hook=CASE.hook,
                investigator=LEADER_ID,
                partner="laura_falk",
                controller="iida_ketonen",
                initial_scene="briefing",
                domain_leads={
                    "physical": ["the rear stair", "the sealed maintenance hatch"],
                    "cybernetic": ["the building's maintenance mesh", "the stores registry"],
                    "social": ["the liaison", "the caretaker", "the stores clerk"],
                    "psychic_noospace": ["the caretaker's reading of the stairwell"],
                },
                witnesses=["aino_rautio", "nila_ahola"],
                contradictions=[
                    "the camera recorded no second figure; the caretaker saw one",
                    "the implant is called a backup; its serial is a stores telemetry unit",
                ],
                faction_interests=["the noon attribution", "the Field Office's standing with UNSA"],
                possible_player_choices=[
                    "close on the record",
                    "confront the stores clerk",
                    "refer it to Internal Affairs",
                ],
                resolution_notes=["no mandatory fixed solution; the table decides what can be proved"],
            )
        },
    )


def build_session(*, seed: int = 502, rng=None):
    """A ready-to-play session on a fresh campaign (import kept local to avoid a cycle)."""
    from .session import CaseSession

    return CaseSession(CASE, build_campaign(), seed=seed, rng=rng)
