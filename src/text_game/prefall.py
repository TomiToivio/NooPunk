"""Canonical issue #60 pre-Fall NoöPunk vertical slice.

This module deliberately uses only author-specified setting facts from issue #60.
Generic analyst/contact roles exist only to make the scenario playable; they do not
add named factions, biographies, or hidden setting canon.

The topology is an abstract simulation map, not a claim about literal travel time
between Earth, Mars, and a stargate survey site.
"""

from __future__ import annotations

from eclipse_phase_homebrew import EP2HarmState, EP2PoolState, PoolKind
from eclipse_phase_homebrew.embodiment import EP2Embodiment

from .model import ActorState, AdventureState, Item, Room, World
from .sheet import CharacterSheet


SCENARIO_PREFIX = "noopunk:"
HUMAN_ID = SCENARIO_PREFIX + "human"
SETI_ANALYST_ID = SCENARIO_PREFIX + "seti-analyst"
STARGATE_ANALYST_ID = SCENARIO_PREFIX + "stargate-analyst"
MARS_ARCHIVE_ID = SCENARIO_PREFIX + "mars-archive-contact"


def _sheet(
    name: str,
    *,
    skills: dict[str, int],
    aptitudes: dict[str, int] | None = None,
) -> dict:
    """Create a small EP2-derived sheet for scenario play.

    Ratings are mechanical playtest values, not setting claims about any real or
    canonical person's competence.
    """
    return CharacterSheet(
        name=name,
        aptitudes=aptitudes or {"COG": 55, "SAV": 50, "WIL": 50, "REF": 45},
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


def prefall_world() -> World:
    """Build the first canonical NoöPunk scenario for issue #60.

    The player moves among abstract evidence nodes and can inspect, discuss, and
    mechanically test actions around the setting's first-contact evidence.
    Collecting the SETI signal record completes the tiny vertical slice.
    """

    earth = SCENARIO_PREFIX + "earth-seti"
    mars = SCENARIO_PREFIX + "mars-ruins"
    gate = SCENARIO_PREFIX + "stargate-survey"

    seti_record = SCENARIO_PREFIX + "seti-signal-record"
    mars_record = SCENARIO_PREFIX + "mars-ruins-record"
    gate_record = SCENARIO_PREFIX + "stargate-survey-record"
    classification = SCENARIO_PREFIX + "classification-dossier"

    world = World(
        rooms={
            earth: Room(
                earth,
                "Earth / SETI Contact Archive",
                (
                    "Earth still exists in 20XX. SETI has received interstellar radio "
                    "signals from a seventh detected extraterrestrial civilization: "
                    "five civilizations were contacted on Earth, the sixth is known "
                    "from ancient Martian ruins, and this radio source is the seventh."
                ),
                exits={"east": mars, "north": gate},
                items=[seti_record, classification],
            ),
            mars: Room(
                mars,
                "Mars / Ruins Archive",
                (
                    "Mars Eldrich's colonization of Mars uncovered ancient ruins, "
                    "life, and evidence of a prior non-human civilization. Mars "
                    "Eldrich is now scouring the Solar System for crash-retrieval "
                    "material as anomalous transport threatens the rocket business."
                ),
                exits={"west": earth, "north": gate},
                items=[mars_record],
            ),
            gate: Room(
                gate,
                "Solar-System Stargate Survey",
                (
                    "Several stargates built by the Zookeepers billions of years ago "
                    "have been found in the Solar System. They explain some UAP "
                    "traffic, but UAPs are also observed using warp drives."
                ),
                exits={"south": earth, "west": mars},
                items=[gate_record],
            ),
        },
        items={
            seti_record: Item(
                seti_record,
                "SETI signal record",
                (
                    "A record of the interstellar signal counted as the seventh "
                    "detected ET civilization."
                ),
            ),
            mars_record: Item(
                mars_record,
                "Mars ruins record",
                (
                    "A record of ancient Martian ruins, life, and evidence of the "
                    "sixth detected extraterrestrial civilization."
                ),
            ),
            gate_record: Item(
                gate_record,
                "stargate survey record",
                (
                    "A survey record of multiple Zookeeper-built stargates and the "
                    "remaining warp-drive UAP traffic they do not explain."
                ),
            ),
            classification: Item(
                classification,
                "classification dossier",
                (
                    "Scientific classification remains unsettled: there is no "
                    "consensus whether Noetics, Plasmoids, and Constructs count as "
                    "civilizations."
                ),
            ),
        },
        actors={
            HUMAN_ID: ActorState(
                HUMAN_ID,
                "Player",
                earth,
                controller="human",
                sheet=_sheet(
                    "Player",
                    skills={"Perceive": 55, "Interface": 50, "Persuade": 45},
                ),
            ),
            SETI_ANALYST_ID: ActorState(
                SETI_ANALYST_ID,
                "SETI analyst",
                earth,
                controller="scripted",
                dialogue={
                    "default": (
                        "The radio source is counted as civilization seven. "
                        "Noetics, Plasmoids, and Constructs remain disputed categories."
                    )
                },
                sheet=_sheet(
                    "SETI analyst",
                    skills={"Perceive": 50, "Interface": 60, "Persuade": 45},
                ),
            ),
            STARGATE_ANALYST_ID: ActorState(
                STARGATE_ANALYST_ID,
                "Stargate survey analyst",
                gate,
                controller="llm",
                sheet=_sheet(
                    "Stargate survey analyst",
                    skills={"Perceive": 55, "Interface": 55, "Persuade": 40},
                ),
            ),
            MARS_ARCHIVE_ID: ActorState(
                MARS_ARCHIVE_ID,
                "Mars archive contact",
                mars,
                controller="llm",
                sheet=_sheet(
                    "Mars archive contact",
                    skills={"Perceive": 50, "Interface": 50, "Persuade": 50},
                ),
            ),
        },
        adventure=AdventureState(
            SCENARIO_PREFIX + "first-contact-evidence",
            objective_item_id=seti_record,
        ),
    )
    world.validate()
    return world


__all__ = [
    "HUMAN_ID",
    "MARS_ARCHIVE_ID",
    "SCENARIO_PREFIX",
    "SETI_ANALYST_ID",
    "STARGATE_ANALYST_ID",
    "prefall_world",
]
