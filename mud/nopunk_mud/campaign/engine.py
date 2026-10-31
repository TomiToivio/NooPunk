"""The solo UNSA campaign: engine (#950).

A deterministic, single-player text engine with **no LLM, no Mesa, no Godot and no second player**. It owns the
state, validates every command, and returns text. Evennia will wrap this; the CLI already drives it.

Two rules from the rest of the project carry straight in:

* **A core clue is never gated by a roll.** `examine()` on a core clue succeeds for anyone who looks.
* **A refused action says why.** Every failure returns a reason the player can act on.
"""
from __future__ import annotations

import json
import random
from dataclasses import dataclass, field
from pathlib import Path

from nopunk_mud import cwn
from nopunk_mud.campaign import content

SCHEMA_VERSION = 1


@dataclass
class State:
    location: str = "safehouse"
    hp: int = 6
    max_hp: int = 6
    inventory: dict[str, int] = field(default_factory=lambda: {"pistol": 1})
    clues: list[str] = field(default_factory=list)
    flags: list[str] = field(default_factory=list)
    talked: list[str] = field(default_factory=list)
    ending: str = ""
    turns: int = 0
    seed: int = 7
    enemy_hp: dict[str, int] = field(default_factory=dict)
    consequences: list[str] = field(default_factory=list)


class CampaignEngine:
    """All state changes go through `command()`. Nothing else mutates the world."""

    def __init__(self, seed: int = 7) -> None:
        self.state = State(seed=seed)
        self.rng = random.Random(seed)
        self.log: list[str] = []
        self.attributes = dict(content.RECRUIT_ATTRIBUTES)
        self.skills = dict(content.RECRUIT_SKILLS)
        self.state.max_hp = cwn.hit_points(1, cwn.attribute_modifier(self.attributes["Constitution"]),
                                           dice=(6,))
        self.state.hp = self.state.max_hp

    # ---- helpers --------------------------------------------------------------------------------

    def has(self, flag: str) -> bool:
        return flag in self.state.flags

    def knows(self, clue: str) -> bool:
        return clue in self.state.clues

    def _grant(self, flags: list[str]) -> None:
        for flag in flags:
            if flag not in self.state.flags:
                self.state.flags.append(flag)

    def _say(self, text: str) -> str:
        self.log.append(text)
        return text

    # ---- the command surface --------------------------------------------------------------------

    def command(self, line: str) -> str:
        """Parse and run one command. Returns the text the player sees."""
        raw = str(line).strip()
        if not raw:
            return "Say something. Try `look`."
        parts = raw.split()
        verb = parts[0].lower()
        args = parts[1:]
        handler = getattr(self, f"_cmd_{verb}", None)
        if handler is None:
            return self._say(f"`{verb}` is not something you can do here. Try `look`, `status` or `help`.")
        self.state.turns += 1
        result = handler(args)
        if self.state.hp <= 0 and not self.state.ending:
            self.state.ending = "killed"
            result += "\n\n" + self._ending_text()
        return result

    def _cmd_help(self, args: list[str]) -> str:
        return self._say("look · status · go <place> · talk <person> · ask <person> <topic> · "
                         "examine <thing> · take <item> · attack <person> · flee · report · save")

    def _cmd_look(self, args: list[str]) -> str:
        place = content.location(self.state.location)
        if place is None:
            return self._say("You are nowhere the engine knows about. That is a bug.")
        lines = [place["name"], place["description"], ""]
        if place["npcs"]:
            names = [content.NPCS[npc]["name"] for npc in place["npcs"]]
            lines.append("Here: " + ", ".join(names) + ".")
        lines.append("Exits: " + ", ".join(sorted(place["exits"])) + ".")
        return self._say("\n".join(lines))

    def _cmd_status(self, args: list[str]) -> str:
        place = content.location(self.state.location)
        known = ", ".join(self.state.clues) if self.state.clues else "nothing yet"
        return self._say(
            f"HP {self.state.hp}/{self.state.max_hp} · at {place['name'] if place else '?'} · "
            f"clues: {known}"
            + (f" · case: {self.state.ending}" if self.state.ending else ""))

    def _cmd_go(self, args: list[str]) -> str:
        if not args:
            return self._say("Go where? `go kurvi`.")
        want = args[0].lower()
        place = content.location(self.state.location)
        if place is None or want not in place["exits"]:
            available = ", ".join(sorted(place["exits"])) if place else "nowhere"
            return self._say(f"You cannot go to {want} from here. Available: {available}.")
        self.state.location = place["exits"][want]
        return self._cmd_look([])

    def _cmd_talk(self, args: list[str]) -> str:
        if not args:
            return self._say("Talk to whom?")
        npc_id = args[0].lower()
        place = content.location(self.state.location)
        if place is None or npc_id not in place["npcs"]:
            return self._say(f"{npc_id} is not here.")
        npc = content.NPCS[npc_id]
        if npc_id not in self.state.talked:
            self.state.talked.append(npc_id)
        topics = ", ".join(sorted(npc["topics"]))
        return self._say(f"{npc['name']}\n{npc['greeting']}\n\nTopics: {topics}")

    def _cmd_ask(self, args: list[str]) -> str:
        if len(args) < 2:
            return self._say("Ask whom about what? `ask romppainen case`.")
        npc_id, topic = args[0].lower(), args[1].lower()
        place = content.location(self.state.location)
        if place is None or npc_id not in place["npcs"]:
            return self._say(f"{npc_id} is not here to answer.")
        npc = content.NPCS[npc_id]
        if topic not in npc["topics"]:
            return self._say(f"{npc['name']} has nothing to say about {topic}. "
                             f"Topics: {', '.join(sorted(npc['topics']))}.")
        self._grant([f"asked_{npc_id}_{topic}"])
        if topic == npc.get("wants"):
            self._grant([f"topic_{topic}"])
        return self._say(npc["topics"][topic])

    def _cmd_examine(self, args: list[str]) -> str:
        if not args:
            return self._say("Examine what?")
        target = " ".join(args).lower()
        for clue_id, clue in content.CLUES.items():
            if clue["location"] != self.state.location:
                continue
            if target not in clue["label"].lower() and target not in clue_id:
                continue
            return self._resolve_clue(clue_id, clue)
        return self._say(f"There is nothing called {target} here worth examining.")

    def _resolve_clue(self, clue_id: str, clue: dict) -> str:
        if self.knows(clue_id):
            return self._say("You already have that.")
        required = clue.get("requires")
        if required and not self.has(f"topic_{required}"):
            return self._say("Nothing here reads yet. Someone would have to tell you what to look for.")
        check = clue.get("check")
        if check:
            result = cwn.skill_check(
                rank=self.skills.get(check["skill"], -1),
                attribute=self.attributes["Intelligence"],
                difficulty=check["difficulty"],
                dice=(self.rng.randint(1, 6), self.rng.randint(1, 6)))
            if not result.success:
                return self._say("You look, and see nothing you can use. The detail is there; your eyes "
                                 "are not having a good day. You could look again.")
        # Core clues and successful checks both land here. A core clue never reaches a failure branch.
        self.state.clues.append(clue_id)
        self._grant(list(clue.get("grants", [])))
        return self._say(clue["text"])

    def _cmd_take(self, args: list[str]) -> str:
        if not args:
            return self._say("Take what?")
        item = args[0].lower()
        if self.state.location != "university" or item != "folder":
            return self._say(f"There is no {item} here to take.")
        if self.state.inventory.get("folder"):
            return self._say("You already have the folder.")
        self.state.inventory["folder"] = 1
        self._grant(["has_folder"])
        return self._say("You take the case folder. It is thinner than it should be.")

    def _cmd_attack(self, args: list[str]) -> str:
        if not args:
            return self._say("Attack whom?")
        target = args[0].lower()
        place = content.location(self.state.location)
        if place is None or target not in place["npcs"]:
            return self._say(f"{target} is not here.")
        template = next((e for e in content.ENCOUNTERS.values()
                          if e["location"] == self.state.location and e["npc"] == target), None)
        if template is None:
            return self._say(f"Attacking {target} is not part of this case, and the engine will not "
                             f"improvise a fight.")
        # A copy, not the template: the enemy's hit points belong to this game. Mutating the content
        # dictionary would carry damage from one playthrough into the next.
        encounter = dict(template)
        return self._fight(encounter)

    def _fight(self, encounter: dict) -> str:
        key = encounter["npc"]
        current_hp = self.state.enemy_hp.get(key, encounter["enemy_hp"])
        if current_hp <= 0:
            return self._say("The encounter is already over.")
        hit = cwn.attack_roll(attack_bonus=0, attribute=self.attributes["Dexterity"],
                              combat_rank=self.skills.get("Shoot", -1),
                              armor_class=encounter["enemy_ac"], die=self.rng.randint(1, 20))
        if not hit.hit:
            self.state.consequences.append("missed_shot")
            incoming = cwn.damage_roll(weapon_die=encounter["enemy_damage_die"],
                                      roll=self.rng.randint(1, encounter["enemy_damage_die"]),
                                      attribute=10)
            self.state.hp = max(0, self.state.hp - incoming)
            return self._say(f"You miss. {encounter['enemy_name']} hits back for {incoming}. "
                             f"HP {self.state.hp}/{self.state.max_hp}.")
        dealt = cwn.damage_roll(weapon_die=encounter["player_weapon_die"],
                                roll=self.rng.randint(1, encounter["player_weapon_die"]),
                                attribute=self.attributes["Dexterity"])
        self.state.enemy_hp[key] = max(0, current_hp - dealt)
        if self.state.enemy_hp[key] <= 0:
            self._grant(["van_cleared"])
            return self._say(f"You hit for {dealt}. {encounter['enemy_name']} goes down and stays down. "
                             f"The van door is unlocked.")
        incoming = cwn.damage_roll(weapon_die=encounter["enemy_damage_die"],
                                   roll=self.rng.randint(1, encounter["enemy_damage_die"]),
                                   attribute=10)
        self.state.hp = max(0, self.state.hp - incoming)
        return self._say(f"You hit for {dealt}. He hits back for {incoming}. "
                         f"HP {self.state.hp}/{self.state.max_hp}.")

    def _cmd_flee(self, args: list[str]) -> str:
        encounter = next((e for e in content.ENCOUNTERS.values()
                          if e["location"] == self.state.location), None)
        if encounter is None:
            return self._say("There is nothing to run from.")
        self.state.consequences.append("fled_encounter")
        self.state.location = encounter["flee_to"]
        return self._say("You run. The case will have to survive without that answer.") + "\n" \
            + self._cmd_look([])

    def _cmd_report(self, args: list[str]) -> str:
        if self.state.location != "safehouse":
            return self._say("You report in person, at the safehouse.")
        if self.state.ending:
            return self._say("The case is already filed.")
        if not self.state.clues:
            return self._say("You have no evidence. Romppainen would sign it and think less of you.")
        solved = self.knows("access_log") and self.knows("witness_badge")
        self.state.ending = "solved" if solved else "incomplete"
        if not solved:
            self.state.consequences.append("insufficient_evidence")
        return self._say(self._ending_text())

    def _ending_text(self) -> str:
        ending = content.ENDINGS.get(self.state.ending or "killed", content.ENDINGS["killed"])
        return f"{ending['title']}\n\n{ending['text']}"

    def _cmd_save(self, args: list[str]) -> str:
        if not args:
            return self._say("Save where? `save /tmp/case.json`.")
        path = Path(args[0])
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(self.to_dict(), indent=2, ensure_ascii=False), encoding="utf-8")
        return self._say(f"Saved to {path}.")

    # ---- persistence ----------------------------------------------------------------------------

    def to_dict(self) -> dict:
        return {
            "schema_version": SCHEMA_VERSION,
            "location": self.state.location,
            "hp": self.state.hp,
            "max_hp": self.state.max_hp,
            "inventory": self.state.inventory,
            "clues": self.state.clues,
            "flags": self.state.flags,
            "talked": self.state.talked,
            "ending": self.state.ending,
            "turns": self.state.turns,
            "seed": self.state.seed,
            "rng_state": self._rng_state_json(),
            "enemy_hp": dict(self.state.enemy_hp),
            "consequences": list(self.state.consequences),
        }

    def _rng_state_json(self) -> list:
        # random.Random state is a tuple tree; JSON requires lists.
        version, values, gaussian = self.rng.getstate()
        return [version, list(values), gaussian]

    @classmethod
    def from_dict(cls, data: dict) -> "CampaignEngine":
        if int(data.get("schema_version", 0)) != SCHEMA_VERSION:
            raise ValueError(f"unsupported campaign schema: {data.get('schema_version')}")
        engine = cls(seed=int(data.get("seed", 7)))
        if "rng_state" in data:
            version, values, gaussian = data["rng_state"]
            engine.rng.setstate((int(version), tuple(int(v) for v in values), gaussian))
        else:
            # Backward compatibility for older saves that only stored turns.
            # Replays are not inferred; this save continues from its original seed.
            pass
        engine.state.location = str(data.get("location", "safehouse"))
        engine.state.max_hp = int(data.get("max_hp", engine.state.max_hp))
        engine.state.hp = int(data.get("hp", engine.state.hp))
        engine.state.inventory = dict(data.get("inventory", {}))
        engine.state.clues = list(data.get("clues", []))
        engine.state.flags = list(data.get("flags", []))
        engine.state.talked = list(data.get("talked", []))
        engine.state.ending = str(data.get("ending", ""))
        engine.state.turns = int(data.get("turns", 0))
        engine.state.enemy_hp = {str(k): int(v) for k, v in dict(data.get("enemy_hp", {})).items()}
        engine.state.consequences = list(data.get("consequences", []))
        return engine


def play(script: list[str], seed: int = 7) -> tuple[CampaignEngine, list[str]]:
    """Run a scripted playthrough. Returns the engine and the text of every turn."""
    engine = CampaignEngine(seed=seed)
    transcript = [engine.command(line) for line in script]
    return engine, transcript
