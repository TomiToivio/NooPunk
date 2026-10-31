"""The MUD's own commands (#946).

Three, deliberately. Every one of them either reads state or asks the CWN sheet; none of
them invents a number, and none of them is a hook for a language model to write into the
world. `scavenge` is the milestone-3 vertical slice: one CWN check, one consequence, one
piece of state that survives a restart.
"""
from __future__ import annotations

from evennia import Command
from evennia.utils import utils

from world.factions import STOCK_NAMES


class CmdSheet(Command):
    """
    Read your CWN sheet.

    Usage:
      sheet

    Attributes, their modifiers and your trained skills. The numbers are the shared
    Cities Without Number rules, not a MUD variant of them.
    """

    key = "sheet"
    locks = "cmd:all()"
    help_category = "NoöPunk"

    def func(self):
        caller = self.caller
        if not hasattr(caller, "sheet"):
            self.msg("This character carries no sheet.")
            return
        self.msg(f"|w{caller.key}|n\n{caller.sheet.to_text()}")
        self.msg(f"Carried supplies: {getattr(caller.db, 'supplies', 0) or 0}")


class CmdScavenge(Command):
    """
    Look for something to eat, drink or burn.

    Usage:
      scavenge [simple|significant|expert]

    A CWN Survival check. Success puts one supply in your hands. Failure does not: the
    street gets a little worse instead, and the room remembers it.
    """

    key = "scavenge"
    aliases = ("forage", "search")
    locks = "cmd:all()"
    help_category = "NoöPunk"

    def func(self):
        caller = self.caller
        difficulty = (self.args or "significant").strip().lower()
        try:
            check = caller.sheet.check("Survive", difficulty=difficulty)
        except ValueError as err:
            self.msg(f"|r{err}|n")
            return

        roll = f"{check.dice[0]}+{check.dice[1]} ({check.total} vs {check.difficulty})"
        if check.success:
            caller.db.supplies = (caller.db.supplies or 0) + 1
            self.msg(f"You find something worth carrying. |g{roll}|n")
            caller.location.msg_contents(
                f"$You() $conj(find) something in the rubble and $conj(keep) it.",
                from_obj=caller,
                exclude=[caller],
            )
            return

        # Failure is a consequence, not a penalty to a hidden number: the room gets worse.
        room = caller.location
        room.db.scarcity = (room.db.scarcity or 0) + 1
        self.msg(
            f"Nothing. You spend the hour on it and the hour wins. |r{roll}|n\n"
            f"|yThis place has been picked over {room.db.scarcity} time(s) since anybody counted.|n"
        )
        caller.location.msg_contents(
            "$You() $conj(search) for a while and $conj(come) back empty-handed.",
            from_obj=caller,
            exclude=[caller],
        )


class CmdFaction(Command):
    """
    Inspect the faction you belong to, or hand over what you are carrying.

    Usage:
      faction
      faction join <name>
      faction give <stock> [amount]

    UNSA is the first playable faction. Membership, reputation and stocks are visible;
    nothing here decides an ideological outcome or simulates a strategy game.
    """

    key = "faction"
    locks = "cmd:all()"
    help_category = "NoöPunk"

    def func(self):
        caller = self.caller
        faction = caller.faction
        parts = self.args.split()
        verb = parts[0].lower() if parts else ""

        if not verb:
            self.msg(faction.to_text())
            return

        if verb == "join":
            name = " ".join(parts[1:]).strip() or caller.key
            if not faction.join(name):
                self.msg(f"|y{name} is already on the roster, or the name is empty.|n")
                return
            caller.save_faction(faction)
            self.msg(f"|g{name} joins {faction.name}. Somebody writes it on the board.|n")
            return

        if verb == "give":
            if len(parts) < 2 or parts[1].lower() not in STOCK_NAMES:
                self.msg(f"Stocks: {', '.join(STOCK_NAMES)}")
                return
            amount = 1
            if len(parts) > 2:
                try:
                    amount = int(parts[2])
                except ValueError:
                    self.msg("|rThe amount must be a whole number.|n")
                    return
            carried = getattr(caller.db, "supplies", 0) or 0
            if amount <= 0 or carried < amount:
                self.msg("|rYou are not carrying that much.|n")
                return
            caller.db.supplies = carried - amount
            left = faction.adjust(parts[1].lower(), amount)
            if parts[1].lower() in ("food", "water", "medicine") and amount >= 2:
                faction.reputation_with(1)
            caller.save_faction(faction)
            utils.logger.log_info(
                "noopunk-mud: %s gave %s %s to %s" % (caller.key, amount, parts[1], faction.name)
            )
            self.msg(f"You hand over {amount} {parts[1]}. {faction.name} has {left}.")
            return

        self.msg("Usage: faction / faction join <name> / faction give <stock> [amount]")
