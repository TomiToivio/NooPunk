"""The MUD's rooms (#946).

A room knows one fact the narration uses and no rule reads: whether it has power. That
is the whole extension — the temptation here is a "scarcity level" per room, and a number
nobody spends is a number that will grow a subsystem.
"""
from __future__ import annotations

from evennia.objects.objects import DefaultRoom
from evennia.typeclasses.attributes import AttributeProperty


class NoopunkRoom(DefaultRoom):
    """A place in the neighbourhood. ``powered`` is narration, never a modifier."""

    powered = AttributeProperty(False)

    def return_appearance(self, looker, **kwargs):
        text = super().return_appearance(looker, **kwargs)
        state = "The lights are on." if self.powered else "The lights are out."
        return f"{text}\n|y{state}|n"
