#!/usr/bin/env python3
"""Audit the imported corpus for third-party expression.

**This is a documentation audit, not a test.** It is deliberately *not* wired into CI and it
deliberately does not live under ``tests/``.

``AGENTS.md``'s "Automated tests policy: executable code only" prohibits automated tests and
CI assertions for *rules, lore, scenario prose, worldbuilding, canon, rulebook structure,
design principles, or wording*. This tool checks the **wording of archived prose** — whether a
copyrighted line, a borrowed brand or a real performer's name survives in the archive. That is
precisely the category the policy excludes from the automated test suite, and precisely the
category that the policy says the author reviews *editorially*.

So the material is preserved, the check is preserved, and the check stays out of the test run:

    python3 tools/audit_corpus_expression.py          # report
    python3 tools/audit_corpus_expression.py --check  # non-zero exit if anything is found

Two consequences are worth stating plainly:

* The **licensing** assertions are not here and are not in the tool. They live in
  ``strategy_game/tests/test_rpg_boundary.py``, which asserts on the contents of
  ``strategy_game/rpg/ATTRIBUTION.md`` — an attribution and licensing record, not creative
  prose. The repository keeps that test, and this audit does not touch it.
* The **code** assertions are not here either. The corpus's mechanics are exercised by
  ``strategy_game/tests/test_rpg_corpus_ports.py`` and the unification by
  ``strategy_game/tests/test_casework_intake_unification.py``; both act on executable objects,
  which is what the policy asks for.

What this tool actually checks
------------------------------

1. **No reproduced dialogue.** The distinctive lines of the two third-party works the corpus
   drew on, in either the original language or the corpus's own translation of them.
2. **No borrowed brands.** The product names, protocol names and in-joke terms the source
   works are known for.
3. **No real performer used as a character blueprint.** A performer's name may appear in the
   archive's *records* — the manifest and the migration map have to be able to say who was
   removed — but not as a model for a character.
4. **No episode titles and no proprietary data.** The episode-by-episode names and the
   corpus's copy of the source's data tables.

The corpus's own guard tests are exempt from the brand check: they name the borrowed brands in
order to assert their **absence**, which is the correct use of a name.
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
#: The imported corpus. It lives under ``legacy/`` because it is quarantined legacy
#: material, not a release asset; the earlier ``archive/`` location is gone.
ARCHIVE = REPO / "legacy" / "ubiquitous_maniacs"
CASE_MODULE = REPO / "strategy_game" / "casework" / "intake.py"

#: Files whose whole purpose is to assert the *absence* of the borrowed brands.
BRAND_GUARD_FILES = frozenset(
    {
        "test_maniac_riget_style.py",
        "test_day_1_scenario.py",
    }
)

#: The corpus's **influence-analysis documents**. These name the source's devices in order
#: to analyse their technique. That is the whole point of the document.
INFLUENCE_DOCUMENTS = frozenset(
    {
        "MANIAC_RIGET_STYLE_ANALYSIS.md",
        "STYLISTIC_INFLUENCES_MANIAC_RIGET.md",
        "MANIAC_RIGET_INFLUENCE_NOTE.md",
    }
)

#: The corpus's own **provenance records**. These must be able to name the files that were
#: removed and the sources that were excluded — that is the record of the cleanup, and a
#: removal that cannot be audited is not a removal. A title appearing inside one of these is
#: a record of the removal, not a reproduction, so the title check skips them.
PROVENANCE_RECORDS = frozenset(
    {
        "MANIFEST.md",
        "manifest.json",
        "MIGRATION_MAP.md",
    }
)

#: Reproduced dialogue, in the source language and in the corpus's own translation of it.
DIALOGUE: tuple[str, ...] = (
    r"Annie,\s*I'?m a hawk",
    r"the pattern is the pattern",
    r"Option A,\s*so?",
    r"True bliss",
    r"Ceci n'?est pas une? (?:drill|une drill)",
    r"None of this is real",
    r"882 minds",
    r"Do we actually have free will",
    r"Genesis of the ?Real ?Techno ?Alchemy",
    r"the cake is a lie",
    r"Manifest Destiny",
    r"Odense",
    r"Poul Herning",
    r"Villarroel",
)

#: The source's **own devices** — its brands, its protocol names, its in-joke terms.
#:
#: These are not dialogue and naming one is not reproducing one: an influence analysis that
#: refused to say which work it was analysing would be useless, and the corpus's influence
#: document is allowed to name them. What must not happen is one of them being used as a
#: *branded term in the corpus's own content* — a character who runs the "AdBuddy" is
#: borrowing the source's world, which is a different act from writing about it.
#:
#: So these are checked against the corpus **content**, and skipped in the influence-analysis
#: documents and the provenance records.
SOURCE_DEVICES: tuple[str, ...] = (
    r"AdBuddy",
    r"Milgram",
    r"DOX STOP",
    r"Neberdine",
    r"GRTA",
    r"Mantleray",
)

#: The source's episode-by-episode titles and its own copy of the source's data tables.
#:
#: These are checked against the corpus **content**. They are deliberately NOT checked against
#: the influence-analysis documents, which are allowed to name the source's devices: naming
#: an influence is not reproducing it, and an influence analysis that refused to say which
#: work it was analysing would be useless. What must not survive is the source's *words*,
#: and that is what :data:`DIALOGUE` covers.
PROPRIETARY: tuple[str, ...] = (
    r"Utangatta",
    r"Furs by Sebastian",
    r"Exactly Like You",
    r"Larger Structural Issues",
    r"The Lake of the Clouds",
    r"The Chosen One",
    r"Having a Day",
    r"Option C",
    r"Windmills",
    r"Church of the Externally Generated",
    r"Techno-occult",
)

#: Real performers and real characters the corpus used as character blueprints.
ACTORS: tuple[str, ...] = (
    r"Emma Stone",
    r"Jonah Hill",
    r"Jack Nicholson",
    r"Annie Landsberg",
    r"Owen Milgrim",
    r"Cary Joji",
    r"Steven Prince",
)

#: A performer's name is forbidden *as a blueprint*: on a line that also reads as a character
#: instruction. A record that merely says who was removed is allowed, and must be.
BLUEPRINT_WORDS = re.compile(
    r"esikuva|näyttelijäohje|acting as|played by|portrayed by|blueprint", re.IGNORECASE
)


#: Every place the corpus may live. The tree was imported under ``archive/`` and later moved
#: to ``legacy/`` when it was quarantined as unreviewed legacy material; scanning both means
#: a leftover copy in either place is caught.
CORPUS_ROOTS = (
    REPO / "legacy" / "ubiquitous_maniacs",
    REPO / "archive" / "ubiquitous-maniacs-2026-10",
)


def _archive_files() -> list[Path]:
    files: list[Path] = []
    for root in CORPUS_ROOTS:
        if not root.is_dir():
            continue
        files.extend(
            path
            for path in root.rglob("*")
            if path.is_file() and path.suffix in {".md", ".py", ".txt", ".json", ".csv"}
        )
    return sorted(files)


def _findings() -> list[str]:
    findings: list[str] = []
    for path in _archive_files():
        text = path.read_text(encoding="utf-8", errors="replace")
        for pattern in DIALOGUE:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                if path.name in BRAND_GUARD_FILES:
                    continue
                findings.append(
                    f"{path.relative_to(REPO)}: reproduced dialogue ({pattern})"
                )
        for pattern in PROPRIETARY:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                if path.name in BRAND_GUARD_FILES or path.name in PROVENANCE_RECORDS:
                    continue
                findings.append(
                    f"{path.relative_to(REPO)}: proprietary title or data ({pattern})"
                )
        for pattern in SOURCE_DEVICES:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                if path.name in BRAND_GUARD_FILES or path.name in INFLUENCE_DOCUMENTS:
                    continue
                findings.append(
                    f"{path.relative_to(REPO)}: the source's own device used as the "
                    f"corpus's own ({pattern})"
                )
        for pattern in ACTORS:
            for match in re.finditer(pattern, text, re.IGNORECASE):
                start = text.rfind("\n", 0, match.start()) + 1
                end = text.find("\n", match.end())
                line = text[start : end if end != -1 else len(text)]
                if BLUEPRINT_WORDS.search(line):
                    findings.append(
                        f"{path.relative_to(REPO)}: real performer as a character "
                        f"blueprint ({pattern})"
                    )
    if CASE_MODULE.is_file():
        text = CASE_MODULE.read_text(encoding="utf-8")
        for pattern in DIALOGUE + PROPRIETARY + SOURCE_DEVICES + ACTORS:
            if re.search(pattern, text, re.IGNORECASE):
                findings.append(
                    f"{CASE_MODULE.relative_to(REPO)}: the case carries third-party "
                    f"expression ({pattern})"
                )
    return findings


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--check",
        action="store_true",
        help="exit non-zero when anything is found",
    )
    args = parser.parse_args()

    if not ARCHIVE.is_dir():
        print(f"archive not found: {ARCHIVE}", file=sys.stderr)
        return 2

    findings = _findings()
    scanned = len(_archive_files())
    if findings:
        print(f"FOUND {len(findings)} finding(s) in {scanned} archived file(s):")
        for finding in findings:
            print(f"  {finding}")
        if args.check:
            return 1
        return 1
    print(f"clean: no third-party expression in {scanned} archived file(s)")
    if args.check:
        return 0
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
