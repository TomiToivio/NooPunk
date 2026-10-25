"""The interpreter the game needs, checked before anything expensive is imported.

**Why this module exists.** The RPG layer uses ``enum.StrEnum`` (Python 3.11+) and
``datetime.UTC`` (3.11+). On an older interpreter the failure surfaces as a bare
``ImportError: cannot import name 'StrEnum' from 'enum'`` raised from the middle of a deep
transitive import — ``strategy_game.casework`` → ``campaign`` → ``rpg`` → ``projection`` — with
no indication that the *interpreter* is the problem or what to do about it.

The repository documents Python 3.12 as the tested version (``README.md``), and CI runs 3.12.
Nothing enforced it. A player following the documented command on a machine with 3.10 therefore
got a stack trace that points at a file they were not editing and a symbol they had never heard
of.

This module gives the two documented CLI entrypoints something to say before that happens. It is
deliberately **not** a hard gate on importing the library: a library that calls ``sys.exit`` on
import is hostile to anything embedding it, including a test runner. The entrypoints call
:func:`require`, catch :class:`UnsupportedInterpreter`, print :func:`message`, and exit 2.
"""
from __future__ import annotations

import sys

#: The oldest interpreter the game runs on. ``enum.StrEnum`` and ``datetime.UTC`` both landed in
#: 3.11, and the tested version is 3.12 (``README.md``, CI).
MINIMUM: tuple[int, int] = (3, 11)

#: The version CI tests, named in the remedy so the advice is concrete.
TESTED: str = "3.12"

#: How to get a supported interpreter, keyed by the platform the player is most likely on.
_REMEDY_UNIX = (
    "Install a supported interpreter and run the game with it, for example:\n"
    "    python3.12 -m venv .venv && . .venv/bin/activate\n"
    "    python -m pip install -r requirements.txt\n"
    "    python -m strategy_game.rpg --scenario ubiquitous-maniacs --save ward.json --new\n"
    "\n"
    "If you already have one, call it directly: `python3.12 -m strategy_game.rpg ...`."
)

_REMEDY_WINDOWS = (
    "Install Python 3.12 from https://www.python.org/downloads/ (or the Microsoft Store), then:\n"
    "    py -3.12 -m venv .venv\n"
    "    .venv\\Scripts\\activate\n"
    "    python -m pip install -r requirements.txt\n"
    "    python -m strategy_game.rpg --scenario ubiquitous-maniacs --save ward.json --new"
)


class UnsupportedInterpreter(RuntimeError):
    """The running interpreter is older than the game supports."""

    def __init__(self, found: tuple[int, int], minimum: tuple[int, int] = MINIMUM) -> None:
        self.found = found
        self.minimum = minimum
        super().__init__(
            f"Python {found[0]}.{found[1]} is too old: the game needs "
            f"{minimum[0]}.{minimum[1]} or newer (tested on {TESTED})."
        )


def found_version() -> tuple[int, int]:
    """The running interpreter's ``(major, minor)``."""
    return sys.version_info.major, sys.version_info.minor


def require(minimum: tuple[int, int] = MINIMUM) -> None:
    """Raise :class:`UnsupportedInterpreter` if the interpreter is too old.

    Callers that are a CLI should catch this and exit 2 with :func:`message`; callers that are a
    library should let it propagate or catch it themselves.
    """
    if found_version() < minimum:
        raise UnsupportedInterpreter(found_version(), minimum)


def message(error: UnsupportedInterpreter | None = None) -> str:
    """A complete, actionable explanation for a player who hit the version gate."""
    if error is None:
        try:
            require()
        except UnsupportedInterpreter as exc:  # pragma: no cover - only on old interpreters
            error = exc
    found = error.found if error else found_version()
    remedy = _REMEDY_WINDOWS if sys.platform.startswith("win") else _REMEDY_UNIX
    return (
        f"Ubiquitous Maniacs / NoöPunk RPG needs Python {MINIMUM[0]}.{MINIMUM[1]} or newer.\n"
        f"This interpreter is Python {found[0]}.{found[1]}, which lacks `enum.StrEnum` and\n"
        f"`datetime.UTC` — both used by the rules layer — so the game cannot start on it.\n"
        f"The tested version is {TESTED}.\n"
        "\n"
        f"{remedy}"
    )
