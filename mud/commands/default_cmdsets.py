"""Text commands for the separate NoöPunk MUD."""
from evennia import Command
from evennia.commands.default.cmdset_character import CharacterCmdSet
from systems.cwn import skill_check
from nopunk_mud.case_consciousness import run_case, attribute_modifier, ATTRIBUTES, SKILLS
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
    aliases = ["factions", "rank"]
    def func(self):
        from nopunk_mud.faction_tags import normalize, rank, RANKS, REWARDS
        state = normalize(self.caller.db.faction_tags)
        level = rank(state)
        self.caller.msg(
            f"UNSA | {RANKS[level]} (rank {level}) | "
            f"training: {REWARDS[level]['training']} | equipment: {REWARDS[level]['equipment']}"
            if level is not None else "No active UNSA membership."
        )


class CmdReputation(Command):
    key = "reputation"
    aliases = ["rep"]
    def func(self):
        from nopunk_mud.faction_tags import normalize, NETWORKS, visible_reputations
        state = normalize(self.caller.db.faction_tags)
        entries = visible_reputations(state, viewer="owner")
        lines = [f"{name}: {entries.get('network:'+name, {}).get('value', 0):+d}"
                 for name in NETWORKS]
        lines += [f"{k}: {v['value']:+d}" for k, v in sorted(entries.items())
                  if k not in {'network:'+n for n in NETWORKS}]
        self.caller.msg("Reputation | " + " | ".join(lines))


class CmdGoals(Command):
    key = "goals"
    def func(self):
        from nopunk_mud.faction_tags import normalize, visible_goals
        state = normalize(self.caller.db.faction_tags)
        goals = visible_goals(state)
        self.caller.msg("Goals: " + (
            "; ".join(f"{key}: {value['description']} [{value['status']}]"
                      for key, value in sorted(goals.items())) if goals else "none yet"
        ))


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

class CmdSolo(Command):
    """Run the headless UNSA investigation inside Evennia, persistently.

    Usage: solo look | solo status | solo go street | solo examine terminal
    The solo case maintains its own map, inventory and HP; it never changes the
    shared Evennia room, combat state, or possessions.
    """
    key = "solo"
    aliases = ["unsa-solo"]

    def func(self):
        # The typed session is the adapter boundary (#1053/#1054): it owns the engine and
        # derives events from the state transition. This command holds no rule and no story.
        from nopunk_mud.session import Action, CampaignSession

        stored = self.caller.db.unsa_solo_state
        try:
            session = CampaignSession.from_dict(dict(stored)) if stored else CampaignSession()
        except (TypeError, ValueError, KeyError) as exc:
            self.caller.msg(
                f"Saved solo case could not be loaded ({exc}). "
                "No state was overwritten; ask an administrator to inspect the save."
            )
            return

        action = self.args.strip() or "look"
        # CampaignEngine's CLI 'save' writes arbitrary local paths; Evennia already persists state, so reject
        # that command at the multiplayer command boundary.
        if action.split()[0].lower() == "save":
            self.caller.msg("Your solo case is saved automatically after each command.")
            return
        result = session.execute(Action(action))
        self.caller.db.unsa_solo_state = dict(result.state)
        self.caller.msg(result.text)


class CmdAssess(Command):
    """Run the helmet-based Helsinki device, max four uses per in-world day.

    Usage: assess status | assess equip | assess run
    A successful run saves the character's use counter in Evennia Attributes.
    The campaign may advance caller.db.unsa_day; real-world midnight never does.
    """
    key = "assess"

    def func(self):
        from nopunk_mud.romppainen_fujita import (
            DeviceUnavailable, HELMET_DESCRIPTION, Use, available, perform,
        )

        action = self.args.strip().lower() or "status"
        # A game-world day is an explicit persisted campaign attribute, not wall time.
        day = self.caller.db.unsa_day
        if day is None:
            day = 1
        record = self.caller.db.romppainen_fujita_uses
        if action == "status":
            try:
                remaining = available(record, day=day)
            except DeviceUnavailable as exc:
                self.caller.msg(str(exc))
                return
            self.caller.msg(f"Romppainen–Fujita: {remaining} of 4 tests remain on in-world day {day}. "
                            "Use 'assess equip' then 'assess run'.")
            return
        if action == "equip":
            self.caller.db.romppainen_fujita_helmets = True
            self.caller.msg(HELMET_DESCRIPTION)
            return
        if action != "run":
            self.caller.msg("Usage: assess status | assess equip | assess run")
            return
        try:
            updated = perform(
                record, day=day, office=self.caller.db.unsa_office or "Helsinki",
                administrator_helmet=bool(self.caller.db.romppainen_fujita_helmets),
                subject_helmet=bool(self.caller.db.romppainen_fujita_helmets),
            )
        except DeviceUnavailable as exc:
            self.caller.msg(str(exc) + " The investigation can proceed using interviews and records.")
            return
        # No mutations until validation succeeds; the interview never gates core clues.
        result = run_case()
        self.caller.db.romppainen_fujita_uses = updated.to_dict()
        self.caller.db.romppainen_fujita_helmets = False
        self.caller.msg("The console beeps and its tiny lights blink. Both helmets hum.")
        self.caller.msg(f"Assessment pattern: {result.assessment.classification} "
                        f"(score {result.assessment.score}, confidence {result.assessment.confidence}). "
                        "Pattern, not proof of consciousness.")
        for clue in result.clues:
            self.caller.msg("Clue: " + clue)
        self.caller.msg("Lead: " + result.assessment.core_clue)
        self.caller.msg(f"{4 - updated.count} test(s) remain today.")


class CmdDictionary(Command):
    """Explain public Finglish vocabulary without revealing story secrets."""
    key = "dictionary"
    aliases = ["lexicon"]

    def func(self):
        from nopunk_mud.lexicon import lookup
        self.caller.msg(lookup(self.args))


class CmdDossier(Command):
    """
    Read the discourse: what people said, where that puts them, and who they actually know.

    Usage:
      dossier                     who is on record, and which signifiers are contested
      dossier <actor>             that actor's statements, positions and relationships
      dossier <a> vs <b>          how much two actors agree, beside how much they trust

    Three layers stay apart: what was said (DA), where an actor stands (DNA), who they know (SNA).
    Agreement and trust are printed next to each other and never merged; a rumour is shown as a
    rumour, and the evidence-only position is printed separately from the position on all claims.
    """

    key = "dossier"
    locks = "cmd:all()"
    help_category = "NoöPunk"

    def func(self) -> None:
        from nopunk_mud.ideology_seed import (
            discourse_for,
            render_actor,
            render_overview,
            render_pair,
            viewer_scope,
        )

        discourse = discourse_for(self.caller)
        scope = viewer_scope()
        text = (self.args or "").strip()

        if not text:
            self.caller.msg(render_overview(discourse, scope=scope))
        elif " vs " in text:
            left, _, right = text.partition(" vs ")
            self.caller.msg(render_pair(discourse, left, right))
        else:
            self.caller.msg(render_actor(discourse, text, scope=scope))


class CmdFirstDay(Command):
    """Tony German's first day, using the canonical WorldSession (#1217).

    Usage:
      firstday                  what can I do now
      firstday look             where am I, and which scene is active
      firstday kit              issued kit state
      firstday wake
      firstday uniform
      firstday inspect <item>
      firstday connect <item>
      firstday repair <item>
      firstday dispatch|ride|arrive|report

    This is a *renderer* over `src.console.first_day`; it never rolls and never
    keeps a second map or sheet. The canonical snapshot is stored on the caller.
    """

    key = "firstday"
    aliases = ["first-day"]
    locks = "cmd:all()"
    help_category = "NoöPunk"

    def func(self) -> None:
        from nopunk_mud.first_day_adapter import FirstDayAdapter, FirstDayAdapterError

        stored = self.caller.db.first_day_state
        try:
            adapter = FirstDayAdapter.from_snapshot(dict(stored)) if stored else FirstDayAdapter()
            text = self.args.strip() or "status"
            if text.lower() == "reset":
                adapter = FirstDayAdapter()
                self.caller.msg("First day reset; no other character state was touched.")
                self.caller.db.first_day_state = adapter.snapshot()
                return
            self.caller.msg(adapter.act(text))
            self.caller.db.first_day_state = adapter.snapshot()
        except (FirstDayAdapterError, ValueError, KeyError, TypeError) as exc:
            self.caller.msg(
                f"First day: {exc}. The saved morning was not overwritten; use 'firstday status'."
            )


class NoopunkCharacterCmdSet(CharacterCmdSet):
    key = "NoopunkCharacterCmdSet"
    def at_cmdset_creation(self):
        super().at_cmdset_creation()
        self.add(CmdDictionary())
        self.add(CmdSheet())
        self.add(CmdCheckAttr())
        self.add(CmdCase())
        self.add(CmdSolo())
        # #985: the Romppainen assessment was implemented and tested but never registered, so a player
        # could not run it. `test_every_command_is_registered` now fails if a command is defined and not added.
        self.add(CmdAssess())
        self.add(CmdCheck())
        self.add(CmdSupplies())
        self.add(CmdScavenge())
        self.add(CmdUnsa())
        self.add(CmdFaction())
        self.add(CmdReputation())
        self.add(CmdGoals())
        self.add(CmdDossier())
        self.add(CmdTalk())
        self.add(CmdFirstDay())
