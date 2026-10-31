"""
At_initial_setup: build the Helsinki neighbourhood on the very first start (#946).

Evennia calls this once, on a fresh database. The builder is idempotent, so calling it
from here, from a test and from a later migration all produce the same five rooms rather
than five more every time somebody restarts.

**Nothing here writes to ``settings``.** An earlier draft assigned the starting room
object to ``settings.START_LOCATION``, which put a live database object into a settings
mapping that gets pickled to the portal — the server then died in ``copyreg`` on every
restart attempt. The starting room is resolved at puppet time instead
(``typeclasses.characters.CwnCharacter.at_pre_puppet``), which is both later and cheaper.
"""


def at_initial_setup():
    from world.helsinki import build

    build()
