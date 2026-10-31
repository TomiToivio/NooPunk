"""Exit typeclass for the NoöPunk MUD.

Evennia's default settings name `typeclasses.exits.Exit`; keeping it in its own module (rather than in
`objects.py`) is what the default configuration expects.
"""
from evennia import DefaultExit


class Exit(DefaultExit):
    """A traversal between rooms. Nothing in the fiction travels without one."""
