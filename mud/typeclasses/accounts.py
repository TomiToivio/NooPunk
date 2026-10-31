"""Account typeclass for the NoöPunk MUD.

Evennia's default settings name these paths; the scaffold shipped characters and rooms but not the four
required typeclasses, so a fresh checkout could not load its own database.
"""
from evennia import DefaultAccount


class Account(DefaultAccount):
    """A player account. Characters hold the fiction; the account holds the login."""
