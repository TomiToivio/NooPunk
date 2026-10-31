"""Evennia commands that let a logged-in player play the solo arc (#966).

Thin by design: every command hands the typed line to `nopunk_mud.evennia_bridge`, which owns the state and asks
the CWN kernel for any number. Nothing here resolves a check, invents a difficulty, or decides an ending.
"""
from __future__ import annotations

from evennia import Command

from nopunk_mud.evennia_bridge import ArcBridge


class CmdAssignment(Command):
    """
    Work the assigned case.

    Usage:
      assignment          what happened so far, and what you can do now
      assignment accept   take the assignment
      assignment interview question the witness in Kurvi
      assignment leave    move on to the university
      assignment records  pull the university access logs
      assignment press    put the second badge to the man who carries it
      assignment submit   file the case
      sheet             your UNSA recruit's attributes and trained skills

    This first assignment cannot be lost to a bad roll: a failed check costs a clue, never the case.
    """

    key = "assignment"
    aliases = ["arc"]
    locks = "cmd:all()"
    help_category = "NoöPunk"

    def func(self) -> None:
        bridge = ArcBridge(self.caller)
        self.caller.msg(bridge.handle(self.args))


class CmdRecruitSheet(Command):
    """
    Show the character sheet the case is being resolved against.

    Usage:
      recruitsheet
    """

    key = "recruitsheet"
    locks = "cmd:all()"
    help_category = "NoöPunk"

    def func(self) -> None:
        self.caller.msg(ArcBridge(self.caller).handle("sheet"))
