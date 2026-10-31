"""Text commands for the separate NoöPunk MUD."""
from evennia import Command
from evennia.commands.default.cmdset_character import CharacterCmdSet
from systems.cwn import skill_check

class CmdSheet(Command):
    key = "sheet"
    def func(self):
        attrs = self.caller.db
        self.caller.msg(f"CWN survivor | STR {attrs.strength} DEX {attrs.dexterity} CON {attrs.constitution} INT {attrs.intelligence} WIS {attrs.wisdom} CHA {attrs.charisma} | HP {attrs.hp}")

class CmdCheck(Command):
    key = "check"
    def func(self):
        try:
            skill, difficulty = (x.strip() for x in self.args.split("=", 1))
            if not skill or skill not in (self.caller.db.skills or {}):
                raise ValueError()
            difficulty = int(difficulty)
            if difficulty not in (6, 8, 10, 12, 14):
                raise ValueError()
        except (ValueError, TypeError):
            self.caller.msg("Usage: check <trained skill>=<difficulty 6/8/10/12/14>")
            return
        rank = self.caller.db.skills[skill]
        result = skill_check(rank=rank, attribute_modifier=0, difficulty=difficulty)
        self.caller.msg(f"{skill}: {result.total} vs {difficulty}, {'success' if result.success else 'failure'} ({result.dice[0]}+{result.dice[1]}+{rank}). Attribute modifiers TBD.")

class CmdSupplies(Command):
    key = "supplies"
    def func(self):
        self.caller.msg(f"Food: {self.caller.db.food or 0} | Water: {self.caller.db.water or 0}")

class CmdScavenge(Command):
    key = "scavenge"
    def func(self):
        if not self.caller.location or not self.caller.location.db.scavengeable:
            self.caller.msg("There are no safe supplies to recover here.")
            return
        pool = int(self.caller.location.db.food_cache or 0)
        if pool < 1:
            self.caller.msg("The shelves have already been stripped.")
            return
        self.caller.location.db.food_cache = pool - 1
        self.caller.db.food = int(self.caller.db.food or 0) + 1
        self.caller.msg("You secure one ration. Nearby survivors may notice.")

class CmdUnsa(Command):
    key = "unsa"
    def func(self):
        if not self.caller.location or not self.caller.location.db.unsa_recruitment:
            self.caller.msg("Visit the UNSA safehouse to request membership.")
            return
        if self.caller.db.faction == "UNSA":
            self.caller.msg("You are already registered with UNSA.")
            return
        self.caller.db.faction = "UNSA"
        self.caller.db.reputation = 0
        self.caller.msg("You are registered as an UNSA volunteer. Your standing is provisional.")

class CmdFaction(Command):
    key = "faction"
    def func(self):
        self.caller.msg(f"Faction: {self.caller.db.faction or 'independent'} | Reputation: {self.caller.db.reputation or 0}")

class CmdTalk(Command):
    key = "talk"
    def func(self):
        target = self.caller.search(self.args, location=self.caller.location)
        if not target:
            return
        if not target.db.npc_dialogue:
            self.caller.msg("They have nothing to say.")
            return
        self.caller.msg(f"{target.key} says: \"{target.db.npc_dialogue}\"")

class NoopunkCharacterCmdSet(CharacterCmdSet):
    key = "NoopunkCharacterCmdSet"
    def at_cmdset_creation(self):
        super().at_cmdset_creation()
        self.add(CmdSheet())
        self.add(CmdCheck())
        self.add(CmdSupplies())
        self.add(CmdScavenge())
        self.add(CmdUnsa())
        self.add(CmdFaction())
        self.add(CmdTalk())
