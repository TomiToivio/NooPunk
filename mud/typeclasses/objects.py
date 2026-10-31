"""Object typeclasses for the NoöPunk MUD: props, doors, and the exits between rooms.

Evennia's default settings name `typeclasses.objects.Object` and expect a matching Exit; the scaffold shipped
characters and rooms only, so a fresh checkout could not load its own database.
"""
from evennia import DefaultObject


class Object(DefaultObject):
    """A default object: a prop, a terminal, a body."""
