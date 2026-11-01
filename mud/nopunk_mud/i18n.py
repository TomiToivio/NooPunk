"""Single canonical Finglish content resolver; legacy fi/en files are read-only compatibility data.

Stable keys and saved campaign state are unaffected. No runtime locale selection or translations.
"""
from __future__ import annotations
import json
from pathlib import Path
from typing import Mapping

LOCALES = ("fi", "en")  # legacy storage identifiers, NOT available languages
DEFAULT_LOCALE = "finglish"
FALLBACK_LOCALE = "en"
CATALOGUE_DIR = Path(__file__).with_name("locale")
LOCALE_FILE = "{locale}.json"
_KEY_SEGMENT = r"[a-z][a-z0-9_]*"

class I18nError(ValueError):
    """Invalid content catalogue or key."""

def _valid_key(key: str) -> bool:
    import re
    return isinstance(key, str) and len(key.split(".")) >= 2 and all(
        re.fullmatch(_KEY_SEGMENT, part) for part in key.split("."))

def load_catalogue(locale: str, *, directory: Path | None = None) -> dict[str, str]:
    """Read historical source catalogues without altering or translating their text."""
    if locale not in LOCALES:
        raise I18nError(f"unknown historical catalogue {locale!r}")
    path = (directory or CATALOGUE_DIR) / LOCALE_FILE.format(locale=locale)
    if not path.exists():
        raise I18nError(f"no catalogue at {path}")
    raw = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(raw, dict):
        raise I18nError("catalogue must be an object")
    output = {}
    for key, value in raw.items():
        if not _valid_key(key):
            raise I18nError(f"invalid key {key!r}")
        if value is None:
            continue
        if not isinstance(value, str) or not value.strip():
            raise I18nError(f"invalid content for {key!r}")
        output[key] = value
    return output

class Translator:
    """Backward-compatible resolver with ONE canonical player-facing Finglish output.

    The old locale argument is accepted for old callers and save compatibility, but
    cannot affect displayed language. Preserved Finnish authored text takes priority;
    otherwise the agent's original English-led Finglish is displayed.
    """
    def __init__(self, locale: str = DEFAULT_LOCALE, *, directory: Path | None = None):
        if locale not in (*LOCALES, DEFAULT_LOCALE):
            raise I18nError(f"unsupported historical locale {locale!r}")
        self.locale = DEFAULT_LOCALE
        self._catalogues = {name: load_catalogue(name, directory=directory) for name in LOCALES}
        self.missing: list[str] = []  # compatibility only; no translation backlog

    def has(self, key: str) -> bool:
        return any(key in catalog for catalog in self._catalogues.values())

    def text(self, key: str, **fields: object) -> str:
        if not _valid_key(key):
            raise I18nError(f"invalid content key {key!r}")
        for source in ("fi", "en"):
            if key in self._catalogues[source]:
                return self._catalogues[source][key].format(**fields)
        raise I18nError(f"no canonical Finglish text for {key!r}")

def validate_catalogue(catalogues: Mapping[str, Mapping[str, str]]) -> list[str]:
    """Validate historical source preservation without localization-completeness gates."""
    errors = []
    for language, values in catalogues.items():
        if language not in LOCALES:
            errors.append(f"unknown historical source {language!r}")
        for key, value in values.items():
            if not _valid_key(key) or not isinstance(value, str) or not value.strip():
                errors.append(f"invalid source entry {language}:{key}")
    return errors

def pending_finnish(catalogues: Mapping[str, Mapping[str, str]]) -> list[str]:
    """Historical compatibility API: no Finnish translation backlog exists."""
    return []
