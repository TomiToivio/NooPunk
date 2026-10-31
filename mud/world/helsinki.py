"""The playable neighbourhood: a Helsinki that is still recognisably Helsinki (#946).

Five rooms, six exits and one safehouse, authored as *data* so the same map can be
built by a test, by the first server start, or by a later migration without anybody
hand-placing objects in an editor. Collapse here is uneven and undramatic: a stairwell
works, a lift does not, the hospital has power and the block does not.

The builder is idempotent — running it twice must not duplicate a room — because it is
called both from ``at_initial_setup`` and from the tests, and the difference between a
world that survives a restart and one that doubles itself on every restart is exactly
this property.
"""
from __future__ import annotations

from typing import Any

#: ``key`` is the object key, ``desc`` the room text, ``exits`` pairs a command word with
#: a target key. ``powered`` is a fact the narration reads; it changes no roll.
ROOMS: tuple[dict[str, Any], ...] = (
    {
        "key": "Kallio, Toinen linja",
        "desc": (
            "The pavement is wet and the streetlights are on a timer nobody has updated since\n"
            "the emergency. A grocery has a hand-written sign in the window: |wNO CARD|n. Two\n"
            "people wait anyway, because the queue is where the news is. Somewhere up the hill\n"
            "a church bell rings the wrong number of times and nobody looks up."
        ),
        "powered": False,
        "exits": {"north": "Kallio, stairwell", "south": "Kallio, market square"},
    },
    {
        "key": "Kallio, stairwell",
        "desc": (
            "Five flights up, no lift since Tuesday. The stairwell smells of wet concrete and\n"
            "somebody else's cooking. A laminated notice announces that the water is safe.\n"
            "Somebody has added, in marker, |wIT IS NOT|n, and then, smaller, |wask us how we know|n."
        ),
        "powered": False,
        "exits": {"south": "Kallio, Toinen linja", "up": "UNSA safehouse"},
    },
    {
        "key": "Kallio, market square",
        "desc": (
            "A square with a tram stop that still shows a timetable. Cardboard over two of the\n"
            "windows in the corner shop; the third is a cafe that has started accepting things\n"
            "instead of money. A drone hangs at the height of a second-floor window, doing\n"
            "whatever it is doing, and everyone has decided not to notice it."
        ),
        "powered": True,
        "exits": {"north": "Kallio, Toinen linja", "east": "Meilahti, hospital entrance"},
    },
    {
        "key": "Meilahti, hospital entrance",
        "desc": (
            "The hospital has power, which is why the queue outside it is longer than the one at\n"
            "the shop. A triage board lists three names and a fourth that has been scrubbed out\n"
            "and written again. Staff move with the particular calm of people who have stopped\n"
            "counting how long this has been going on."
        ),
        "powered": True,
        "exits": {"west": "Kallio, market square", "in": "Meilahti, records office"},
    },
    {
        "key": "Meilahti, records office",
        "desc": (
            "A room that used to be for paper and is now half for paper, half for a terminal that\n"
            "answers questions slowly. The archive is intact. Whether the archive is |wtrue|n\n"
            "is a different question, and it is the one nobody wants to ask in writing."
        ),
        "powered": True,
        "exits": {"out": "Meilahti, hospital entrance"},
    },
    {
        "key": "UNSA safehouse",
        "desc": (
            "A flat that has been a safehouse for eleven days. A whiteboard with three names on\n"
            "it and one of them crossed out twice. The radio is on, quietly, tuned to a station\n"
            "that stopped broadcasting a week ago. Somebody keeps it on out of habit, or as a\n"
            "statement, or because the static is the only thing that still sounds like weather."
        ),
        "powered": True,
        "exits": {"down": "Kallio, stairwell"},
    },
)

#: Where a new character wakes up. The safehouse is the faction's, so the street is fairer.
START = "Kallio, Toinen linja"


def _room(key: str) -> Any:
    from evennia.objects.models import ObjectDB

    return ObjectDB.objects.filter(db_key=key).first()


def build() -> dict[str, Any]:
    """Create the neighbourhood if it is missing; return it either way.

    Idempotent by construction: every lookup is by key, and an existing room is never
    re-created. Exits are created only when their source room has none with that name.
    """
    from evennia import create_object
    from evennia.utils import utils

    created: dict[str, Any] = {}
    for spec in ROOMS:
        room = _room(spec["key"])
        if room is None:
            room = create_object(
                "typeclasses.rooms.NoopunkRoom",
                key=spec["key"],
                nohome=True,
            )
            room.db.desc = spec["desc"]
            room.db.powered = spec["powered"]
        created[spec["key"]] = room

    for spec in ROOMS:
        source = created[spec["key"]]
        present = {str(exit_obj.key).lower() for exit_obj in source.exits}
        for word, target_key in spec["exits"].items():
            if word.lower() in present:
                continue
            target = created[target_key]
            create_object(
                "typeclasses.exits.NoopunkExit",
                key=word,
                location=source,
                destination=target,
                nohome=True,
            )
    utils.logger.log_info("noopunk-mud: neighbourhood present (%d rooms)" % len(created))
    return created


def start_room() -> Any:
    """The room a fresh character is placed in, creating the world if it is absent."""
    room = _room(START)
    return room if room is not None else build()[START]
