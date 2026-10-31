"""The solo UNSA campaign: content (#950).

Original NoöPunk material. One case, four places, two named colleagues, one fight, three ways it can end.
Everything here is data — the engine in `engine.py` reads it and decides nothing by itself.

Design rules the content obeys:

* **A core clue is never behind a roll.** Every scene that carries the case forward yields its clue to any
  investigator who looks, because a mystery that stops is not a mystery.
* **Optional clues cost a check.** They add colour, a name, an advantage — never the solution.
* **No dead ends.** Every refusal names what is missing.
* Nothing here is copied from a published adventure.
"""
from __future__ import annotations

from typing import Any

#: Attribute scores for the rookie. Deliberately unremarkable: the case is solved by looking, not by luck.
RECRUIT_ATTRIBUTES = {
    "Strength": 10, "Dexterity": 12, "Constitution": 11,
    "Intelligence": 13, "Wisdom": 10, "Charisma": 9,
}
RECRUIT_SKILLS = {"Administer": 1, "Notice": 1, "Talk": 0, "Shoot": 0}

LOCATIONS: dict[str, dict[str, Any]] = {
    "safehouse": {
        "name": "UNSA safehouse, Ratakatu",
        "description": "A basement room with a table, a radio and two chairs. Romppainen has left a paper "
                       "folder open at your place.",
        "exits": {"street": "street"},
        "npcs": ["romppainen"],
    },
    "street": {
        "name": "Helsinginkatu",
        "description": "Tram rails, a shuttered kiosk, rain that will not commit. Kurvi is east; the "
                       "university is south.",
        "exits": {"safehouse": "safehouse", "kurvi": "kurvi", "university": "university"},
        "npcs": [],
    },
    "kurvi": {
        "name": "Kurvi",
        "description": "The junction where Kallio argues with itself. A woman in a raincoat watches the "
                       "tram stop and does not get on.",
        "exits": {"street": "street", "harbour": "harbour"},
        "npcs": ["witness"],
    },
    "university": {
        "name": "University of Helsinki, department corridor",
        "description": "An unattended terminal hums beside a door marked LAITOSKIRJASTO. The corridor "
                       "smells of floor wax and old paper.",
        "exits": {"street": "street"},
        "npcs": [],
    },
    "harbour": {
        "name": "West Harbour",
        "description": "Containers, a crane that stopped moving, and a man who has been standing by the "
                       "same van for twenty minutes.",
        "exits": {"kurvi": "kurvi"},
        "npcs": ["watcher"],
    },
}

NPCS: dict[str, dict[str, Any]] = {
    "romppainen": {
        "name": "Dr. Harri Romppainen",
        "greeting": "«Sit down. The folder is yours — a researcher stopped answering her phone. "
                    "Everyone agrees that means nothing. Ask me what you need.»",
        "topics": {
            "case": "«Virtanen. Biotech, third floor. Missed two lectures and a supervision. "
                    "Her badge still opens the lab, which is the part I dislike.»",
            "uniform": "«You are wearing the new uniform. Everyone knows. Nobody will say it to your "
                       "face today, and tomorrow you will dress like a person.»",
            "advice": "«Look at where she worked before you look at who she knew. Paper first.»",
        },
        "wants": "case",
    },
    "witness": {
        "name": "Woman in a raincoat",
        "greeting": "She looks at your badge, then at your face, and decides you are not important "
                    "enough to lie to.",
        "topics": {
            "badge": "«University badge. She came off the tram at eleven and went towards the water. "
                     "I remember because she was the only person who looked at the sky.»",
            "van": "«Grey. No markings. It was already there when she came back past me at midnight, "
                   "and it was still there when I went home.»",
        },
        "wants": "badge",
    },
    "watcher": {
        "name": "Man by the van",
        "greeting": "He does not introduce himself. He does not step away from the van either.",
        "topics": {
            "van": "«You are not with the agency that hired me. So we can talk, briefly.»",
        },
        "wants": "van",
        "hostile": True,
    },
}

#: Things that can be examined. `core` clues are free to anyone who looks; `optional` ones cost a check.
CLUES: dict[str, dict[str, Any]] = {
    "access_log": {
        "location": "university",
        "label": "the terminal",
        "core": True,
        "requires": None,
        "text": "Access logs put Virtanen's badge in the laboratory at 23:40 — after the building closed, "
                "and after the last tram.",
        "grants": ["knows_lab_time"],
    },
    "witness_badge": {
        "location": "kurvi",
        "label": "the woman in the raincoat",
        "core": True,
        "requires": "badge",
        "text": "A university badge, a tram at eleven, a walk towards the water. She was last seen going "
                "south, not home.",
        "grants": ["knows_route"],
    },
    "van_plate": {
        "location": "harbour",
        "label": "the van",
        "core": False,
        "requires": "van",
        "check": {"skill": "Notice", "difficulty": 8},
        "text": "A partial plate, three characters. Enough to ask a question later, not enough to prove "
                "anything now.",
        "grants": ["has_plate"],
    },
    "lab_note": {
        "location": "university",
        "label": "the lab door",
        "core": False,
        "requires": None,
        "check": {"skill": "Notice", "difficulty": 10},
        "text": "A note taped inside the doorframe: 'second badge — file it'. Someone else had access.",
        "grants": ["knows_second_badge"],
    },
}

#: The one fight. It is avoidable if the player has the plate and chooses to leave.
ENCOUNTERS: dict[str, dict[str, Any]] = {
    "harbour_van": {
        "location": "harbour",
        "npc": "watcher",
        "trigger": "provoke",
        "enemy_name": "the man by the van",
        "enemy_hp": 5,
        "enemy_ac": 12,
        "enemy_damage_die": 6,
        "player_weapon_die": 6,
        "flee_to": "kurvi",
    },
}

ENDINGS: dict[str, dict[str, str]] = {
    "solved": {
        "title": "Case filed: the researcher, the van, the second badge",
        "text": "Romppainen reads your report twice, then puts it down. «The plate will be gone by "
                "Monday. The badge is the part that will still matter.» He signs it. You are, officially, "
                "useful.",
    },
    "incomplete": {
        "title": "Case filed: insufficient evidence",
        "text": "Romppainen reads it once. «You have a timeline and no names. It happens.» He signs it "
                "anyway, because the alternative is a case nobody closed.",
    },
    "killed": {
        "title": "Case closed: agent down",
        "text": "The file ends with your name and a date. Somebody else picks up the folder in the "
                "morning, because somebody always does.",
    },
}


def location(name: str) -> dict[str, Any] | None:
    return LOCATIONS.get(name)


def clue(name: str) -> dict[str, Any] | None:
    return CLUES.get(name)
