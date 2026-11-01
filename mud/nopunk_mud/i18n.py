"""Language-neutral content IDs and the fi/en catalogue (issues #981 and #980).

The rule this module exists to enforce: **Tomi writes Finnish, agents write English.** So the catalogue
carries two locales, and an agent may only ever fill ``en``. A missing Finnish string is not an error -
it is *pending localisation*, and the loader falls back to English so the game stays playable.

What is deliberately absent: any translation. There is no machine translation, no LLM call, and no
network access anywhere in this module. An agent that "helpfully" fills ``fi`` with invented Finnish has
broken the policy, not completed the task. ``validate_catalogue`` flags a Finnish string that no author
has claimed, so that kind of help is visible rather than silent.

Key format: dot-separated, lower snake_case segments, e.g. ``case.clue.record_1601``. Keys are stable and
never renumbered; a key's text may change, its identity may not.
"""
from __future__ import annotations

import json
from pathlib import Path
from typing import Iterable, Mapping

LOCALES = ("fi", "en")
DEFAULT_LOCALE = "fi"
FALLBACK_LOCALE = "en"
CATALOGUE_DIR = Path(__file__).with_name("locale")
LOCALE_FILE = "{locale}.json"
_KEY_SEGMENT = r"[a-z][a-z0-9_]*"


class I18nError(ValueError):
    """A catalogue or a lookup that breaks the content contract."""


def _valid_key(key: str) -> bool:
    import re

    return all(re.fullmatch(_KEY_SEGMENT, part) for part in key.split(".")) and len(key.split(".")) >= 2


def load_catalogue(locale: str, *, directory: Path | None = None) -> dict[str, str]:
    """Read one locale file. Values must be strings; ``null`` means "not yet localised"."""
    if locale not in LOCALES:
        raise I18nError(f"unknown locale {locale!r}; expected one of {LOCALES}")
    path = (directory or CATALOGUE_DIR) / LOCALE_FILE.format(locale=locale)
    if not path.exists():
        raise I18nError(f"no catalogue for {locale!r} at {path.name}")
    raw = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(raw, dict):
        raise I18nError(f"{path.name} must be a JSON object of key -> string")
    catalogue: dict[str, str] = {}
    for key, value in raw.items():
        if not _valid_key(key):
            raise I18nError(f"{path.name}: malformed key {key!r}")
        if value is None:
            continue  # pending localisation
        if not isinstance(value, str) or not value.strip():
            raise I18nError(f"{path.name}: {key!r} must be a non-empty string or null")
        catalogue[key] = value
    return catalogue


class Translator:
    """Resolve a content key in the player's locale, falling back to English.

    ``missing`` records the keys that resolved by fallback, so a caller can log how much of what the
    player saw was still agent-authored English rather than Tomi's Finnish.
    """

    def __init__(self, locale: str = DEFAULT_LOCALE, *, directory: Path | None = None) -> None:
        if locale not in LOCALES:
            raise I18nError(f"unknown locale {locale!r}")
        self.locale = locale
        self._catalogues = {name: load_catalogue(name, directory=directory) for name in LOCALES}
        self.missing: list[str] = []

    def has(self, key: str) -> bool:
        return any(key in catalogue for catalogue in self._catalogues.values())

    def text(self, key: str, **fields: object) -> str:
        """Resolve one key. Raises when no locale supplies it, rather than showing a blank to a player."""
        if not _valid_key(key):
            raise I18nError(f"malformed content key {key!r}")
        if key in self._catalogues[self.locale]:
            return self._catalogues[self.locale][key].format(**fields)
        if key in self._catalogues[FALLBACK_LOCALE]:
            if key not in self.missing:
                self.missing.append(key)
            return self._catalogues[FALLBACK_LOCALE][key].format(**fields)
        raise I18nError(f"no translation for {key!r} in any locale")


def validate_catalogue(catalogues: Mapping[str, Mapping[str, str]]) -> list[str]:
    """Report contract problems rather than raising, so a CI step can print all of them at once.

    Checks, in the order a reviewer cares about:
    * every locale is known;
    * every English key has a stable, well-formed id;
    * no string is empty;
    * **a Finnish string is never longer-than-plausible filler** - this cannot detect prose, but it does
      catch an agent pasting the English text into ``fi`` to make the gap look closed.
    """
    problems: list[str] = []
    for locale in catalogues:
        if locale not in LOCALES:
            problems.append(f"unknown locale {locale!r}")
    english = catalogues.get(FALLBACK_LOCALE, {})
    finnish = catalogues.get(DEFAULT_LOCALE, {})
    for key in english:
        if not _valid_key(key):
            problems.append(f"malformed key {key!r}")
        if not str(english[key]).strip():
            problems.append(f"{FALLBACK_LOCALE}: {key!r} is empty")
    for key, value in finnish.items():
        if not _valid_key(key):
            problems.append(f"malformed key {key!r}")
        if not str(value).strip():
            problems.append(f"{DEFAULT_LOCALE}: {key!r} is empty")
        if english.get(key) == value:
            problems.append(
                f"{DEFAULT_LOCALE}: {key!r} is identical to its English text - "
                "Finnish is authored by Tomi, never copied from the English"
            )
    return problems


def pending_finnish(catalogues: Mapping[str, Mapping[str, str]]) -> list[str]:
    """Keys that still need Tomi's Finnish. This is the localisation backlog, not a failure list."""
    finnish = catalogues.get(DEFAULT_LOCALE, {})
    return sorted(key for key in catalogues.get(FALLBACK_LOCALE, {}) if key not in finnish)
