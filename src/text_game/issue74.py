"""Issue #74: tiny NoöPunk / Concordia / EP2 proof-of-concept scenario.

This module deliberately reuses the existing text-game engine, EP2-derived
character-sheet kernel, and Concordia-compatible LLM controller seam. It adds a
small bounded scenario only. Generic NPC roles are interface roles, not new canon.
"""

from __future__ import annotations

from eclipse_phase_homebrew import EP2HarmState, EP2PoolState, PoolKind
from eclipse_phase_homebrew.embodiment import EP2Embodiment

from .model import ActorState, AdventureState, Item, Room, World
from .sheet import CharacterSheet

SCENARIO_PREFIX = "issue74:"
HUMAN_ID = SCENARIO_PREFIX + "human"
ANALYST_ID = SCENARIO_PREFIX + "analyst"
TECHNICIAN_ID = SCENARIO_PREFIX + "technician"
SIGNAL_ID = SCENARIO_PREFIX + "signal-record"
DOSSIER_ID = SCENARIO_PREFIX + "classification-dossier"


def _sheet(name: str, *, skills: dict[str, int]) -> dict:
    return CharacterSheet(
        name=name,
        aptitudes={"COG": 55, "SAV": 50, "WIL": 50, "REF": 45},
        skills=skills,
        pools=EP2PoolState(
            maximum={
                PoolKind.INSIGHT: 2,
                PoolKind.MOXIE: 2,
                PoolKind.VIGOR: 2,
                PoolKind.FLEX: 1,
            }
        ),
        harm=EP2HarmState(
            durability=30,
            wound_threshold=6,
            lucidity=25,
            trauma_threshold=5,
        ),
        embodiment=EP2Embodiment(
            name="baseline biological morph",
            kind="biological",
            durability=30,
            wound_threshold=6,
        ),
    ).to_dict()


def issue74_world() -> World:
    """Return the deliberately tiny issue #74 vertical slice.

    The whole prototype occurs inside one abstract SETI/contact-analysis room.
    The mission is to authenticate and take custody of the SETI signal record.
    Existing mechanics allow investigation, technical/mesh checks, social tests,
    and combat resolution without adding new rules. Psionics remain deferred
    because issue #74 explicitly asks the prototype to teach us what is useful,
    not to invent a psionics subsystem prematurely.
    """

    archive = SCENARIO_PREFIX + "contact-archive"

    world = World(
        rooms={
            archive: Room(
                archive,
                "Earth / Contact Analysis Room",
                (
                    "20XX, alternate pre-Fall Eclipse Phase continuity. Earth is "
                    "still inhabited and politically central. The room contains "
                    "records concerning the SETI signal counted as the seventh "
                    "detected ET civilization, together with the unresolved "
                    "classification dispute over Noetics, Plasmoids, and Constructs."
                ),
                items=[SIGNAL_ID, DOSSIER_ID],
            ),
        },
        items={
            SIGNAL_ID: Item(
                SIGNAL_ID,
                "SETI signal record",
                (
                    "The interstellar radio-signal record counted as the seventh "
                    "detected extraterrestrial civilization."
                ),
            ),
            DOSSIER_ID: Item(
                DOSSIER_ID,
                "classification dossier",
                (
                    "A dossier noting that Noetics, Plasmoids, and Constructs are "
                    "not settled parts of the official civilization count."
                ),
            ),
        },
        actors={
            HUMAN_ID: ActorState(
                HUMAN_ID,
                "Player",
                archive,
                controller="human",
                sheet=_sheet(
                    "Player",
                    skills={
                        "Perceive": 55,
                        "Interface": 55,
                        "Persuade": 50,
                    },
                ),
            ),
            ANALYST_ID: ActorState(
                ANALYST_ID,
                "contact analyst",
                archive,
                controller="llm",
                sheet=_sheet(
                    "contact analyst",
                    skills={
                        "Perceive": 55,
                        "Interface": 60,
                        "Persuade": 50,
                    },
                ),
            ),
            TECHNICIAN_ID: ActorState(
                TECHNICIAN_ID,
                "archive technician",
                archive,
                controller="scripted",
                dialogue={
                    "default": (
                        "The signal record is genuine archive material. The disputed "
                        "NHI categories remain scientifically unsettled."
                    )
                },
                sheet=_sheet(
                    "archive technician",
                    skills={
                        "Perceive": 50,
                        "Interface": 55,
                        "Persuade": 45,
                    },
                ),
            ),
        },
        adventure=AdventureState(
            SCENARIO_PREFIX + "authenticate-signal",
            objective_item_id=SIGNAL_ID,
        ),
    )
    world.validate()
    return world


__all__ = [
    "ANALYST_ID",
    "DOSSIER_ID",
    "HUMAN_ID",
    "SCENARIO_PREFIX",
    "SIGNAL_ID",
    "TECHNICIAN_ID",
    "issue74_world",
]
