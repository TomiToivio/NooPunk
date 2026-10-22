"""Keep clear-text secrets out of rendered output.

A renderer is a *view*, and the character-card layer's own rule is that "a renderer must not be the
thing that leaks a secret". This module is the print-boundary half of that rule: it withholds
values whose **key** marks them as private, so a board view, a JSON payload and a roster face all
pass through the same gate.

The check is by key, not by content: an author who marks an attribute ``private`` gets it withheld
without changing any renderer. The layer that owns the data stays responsible for not rendering it
at all; this is the last line of defence, not the first.
"""
from __future__ import annotations

import re
from collections.abc import Mapping
from typing import Any

#: Keys whose values are never printed in clear text.
SENSITIVE_KEYS: tuple[str, ...] = (
    "private",
    "secret",
    "secrets",
    "gm_notes",
    "gm_secrets",
    "token",
    "password",
    "api_key",
    "access_token",
)

#: The marker that replaces a withheld value, so the redaction is visible in the output.
WITHHELD = "[withheld]"


def _pattern(key: str) -> re.Pattern[str]:
    """A regex matching ``key: value`` / ``"key": "value"`` for one sensitive key."""
    return re.compile(
        r"((?:[\"']" + re.escape(key) + r"[\"']|" + re.escape(key) + r")\s*:\s*[\"'])(.*?)([\"'])",
        re.DOTALL,
    )


def redact(text: str) -> str:
    """Return ``text`` with sensitive-keyed values replaced by :data:`WITHHELD`."""
    out = text
    for key in SENSITIVE_KEYS:
        out = _pattern(key).sub(lambda m: m.group(1) + WITHHELD + m.group(3), out)
    return out


def redact_mapping(attributes: Mapping[str, Any]) -> dict[str, Any]:
    """Return the entries of ``attributes`` that may be shown.

    A key that is not sensitive is passed through unchanged; a sensitive key is dropped, because
    unlike a rendered string there is no value to mark in place.
    """
    if not isinstance(attributes, Mapping):
        return {}
    sensitive = {key.lower() for key in SENSITIVE_KEYS}
    return {
        key: value
        for key, value in attributes.items()
        if str(key).strip().lower() not in sensitive
    }


def emit(text: str) -> None:
    """Print rendered text with secrets withheld."""
    print(redact(text))
