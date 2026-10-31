"""Text commands for the separate NoöPunk MUD."""
from evennia import Command
from evennia.commands.default.cmdset_character import CharacterCmdSet
from systems.cwn import skill_check, attribute_modifier, ATTRIBUTES, SKILLS
from nopunk_mud.solo_campaign import Campaign, advance

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
            if not skill or skill.lower() not in SKILLS:
                raise ValueError()
            difficulty = int(difficulty)
            if difficulty not in (6, 8, 10, 12, 14):
                raise ValueError()
        except (ValueError, TypeError):
            self.caller.msg("Usage: check <trained skill>=<difficulty 6/8/10/12/14>")
            return
        skill = skill.lower()
        ranks = self.caller.db.skills or {}
        rank = ranks.get(skill, -1)
        # Attribute is selected by situation rather than fixed to each skill.
        # Explicit caller-selected attribute makes the choice visible.
        attr_name = (self.caller.db.check_attribute or "intelligence").lower()
        if attr_name not in ATTRIBUTES:
            attr_name = "intelligence"
        mod = attribute_modifier(int(getattr(self.caller.db, attr_name) or 10))
        result = skill_check(rank=rank, attribute_modifier=mod, difficulty=difficulty)
        self.caller.msg(f"{skill} ({attr_name}): {result.total} vs {difficulty}, {'success' if result.success else 'failure'} ({result.dice[0]}+{result.dice[1]}{rank:+d}{mod:+d}). Set attribute with 'checkattr <attribute>'.")

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


class CmdCheckAttr(Command):
    key = "checkattr"
    def func(self):
        attr = self.args.strip().lower()
        if attr not in ATTRIBUTES:
            self.caller.msg("Usage: checkattr strength|dexterity|constitution|intelligence|wisdom|charisma")
            return
        self.caller.db.check_attribute = attr
        self.caller.msg(f"Skill checks now use {attr.upper()} where narratively appropriate.")

class CmdCase(Command):
    """A deterministic UNSA case, fully playable with no external GM."""
    key = "case"
    def func(self):
        campaign = Campaign.from_dict(self.caller.db.unsa_campaign or {})
        state, feedback = advance(campaign, self.args.strip() or "status",
                                  self.caller.location.key if self.caller.location else "")
        self.caller.db.unsa_campaign = state.to_dict()
        self.caller.msg(feedback)

class NoopunkCharacterCmdSet(CharacterCmdSet):
    key = "NoopunkCharacterCmdSet"
    def at_cmdset_creation(self):
        super().at_cmdset_creation()
        self.add(CmdSheet())
        self.add(CmdCheckAttr())
        self.add(CmdCase())
        self.add(CmdCheck())
        self.add(CmdSupplies())
        self.add(CmdScavenge())
        self.add(CmdUnsa())
        self.add(CmdFaction())
        self.add(CmdTalk())
