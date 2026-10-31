"""Host the solo arc inside Evennia, without letting Evennia into the arc (#966).

The arc (`solo_arc`) is engine-free and takes a resolver. The command layer is Evennia-only and knows nothing
about rules. This module is the seam: it turns a persistent object's attributes into an `Arc`, routes one typed
line to `solo_arc.advance`, resolves checks through the CWN kernel, and writes the result back.

It imports **no Evennia**, so it can be tested without a server — and it imports no rules of its own, so the
command layer cannot grow a second set of numbers.
"""
from __future__ import annotations

from typing import Any

from nopunk_mud import kernel_resolver, solo_arc

#: What the player can type, by stage. Kept here rather than in the arc because it is presentation: the arc
#: rejects anything it does not recognise regardless of what we advertise.
ACTIONS_BY_STAGE: dict[str, dict[str, str]] = {
    "briefing": {"accept": "accept the assignment"},
    "kurvi": {"interview": "interview the witness", "leave": "leave for the university"},
    "records": {"records": "pull the access logs"},
    "confrontation": {"press": "press the man with the second badge"},
    "report": {"submit": "file the case"},
    "complete": {},
}


class ArcBridge:
    """Persist and drive one character's arc. `store` is anything with a `.db` attribute (an Evennia object)."""

    def __init__(self, store: Any, resolver: kernel_resolver.Resolver | None = None) -> None:
        self.store = store
        self.resolver = resolver or kernel_resolver.Resolver.for_recruit()

    # ---- persistence -------------------------------------------------------------------------

    @property
    def arc(self) -> solo_arc.Arc:
        raw = getattr(self.store.db, "solo_arc", None)
        if raw is None:
            return solo_arc.Arc()
        try:
            # Evennia stores db dicts as `_SaverDict`, which is a Mapping but NOT a dict subclass. Testing
            # `isinstance(raw, dict)` silently resets the arc on every command.
            return solo_arc.Arc.from_dict(dict(raw))
        except (TypeError, ValueError):
            return solo_arc.Arc()

    @arc.setter
    def arc(self, value: solo_arc.Arc) -> None:
        self.store.db.solo_arc = value.to_dict()

    # ---- the command surface ----------------------------------------------------------------

    def prompt(self) -> str:
        """What the player can do now. A finished case offers nothing."""
        arc = self.arc
        options = ACTIONS_BY_STAGE.get(arc.stage, {})
        head = f"[{arc.stage}] " + solo_arc._status(arc)
        if not options:
            return head
        listed = "; ".join(f"{verb} - {text}" for verb, text in options.items())
        return f"{head}\nAvailable: {listed}"

    def handle(self, line: str) -> str:
        """One typed line in, one line out. Never raises on player input."""
        text = (line or "").strip()
        if not text:
            return self.prompt()

        verb, _, rest = text.partition(" ")
        verb = verb.lower()
        rest = rest.strip()

        if verb in ("arc", "case", "status"):
            return self.prompt()

        if verb == "sheet":
            return self._sheet()

        arc, reply = solo_arc.advance(self.arc, verb, self.resolver)
        if reply.startswith("That action is unavailable"):
            return f"{reply}\n{self.prompt()}"
        self.arc = arc
        return f"{reply}\n{self.prompt()}"

    # ---- character sheet --------------------------------------------------------------------

    def _sheet(self) -> str:
        r = self.resolver
        attrs = " ".join(f"{k} {v}" for k, v in r.attributes.items())
        skills = ", ".join(f"{k} {v:+d}" for k, v in r.skills.items()) or "none"
        return f"UNSA field recruit | {attrs} | trained: {skills}"
