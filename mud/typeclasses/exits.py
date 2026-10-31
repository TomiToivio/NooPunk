"""The MUD's exits (#946).

Nothing is added here yet. The class exists so the map data can name a typeclass that is
ours, and so a later change (a blocked exit, a hidden one) has a home that is not the
framework's.
"""
from __future__ import annotations

from evennia.objects.objects import DefaultExit


class NoopunkExit(DefaultExit):
    """A normal exit, in a name this project owns."""
