"""Engine-neutral console play of an investigation case (#1053, #1054).

This package is the **reference adapter**: the smallest presentation that can play a case through the
canonical rules in `src/rules/investigation.py`. It holds no rules of its own.

The division it keeps, because it is the one that erodes quietly:

* the rules module decides what a competent investigator *sees* (`discover`), and refuses to
  conclude anything;
* this session decides what the *player* has done -- which scenes were visited, which facts were
  attached to which theory, what the dice said;
* the player, never the program, holds the theory. `conclude` records the player's answer and the
  evidence behind it; it does not grade it.
"""

from __future__ import annotations

from .session import CaseSession, SessionError, load_session, save_session

__all__ = ["CaseSession", "SessionError", "load_session", "save_session"]
