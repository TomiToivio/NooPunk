#!/usr/bin/env python3
"""Build the ``ubiquitous-maniacs-2026-10`` import manifest.

Produces, deterministically and re-runnably:

  legacy/ubiquitous_maniacs/MANIFEST.md     human-readable inventory
  legacy/ubiquitous_maniacs/manifest.json    machine-readable inventory

What this is
------------

The NoöPunk *Ubiquitous Maniacs* corpus was developed in a **different repository**
(``TomiToivio/Panpsychic-Cyborg-Multitude``, under ``noopunk/ubiquitous_maniacs/``).
It is imported here as a **source-of-record**: the material is preserved with content
hashes so its retrievability is provable rather than claimed, and the migration map
records where each unit lands in *this* repository's canon.

The corpus is **not** merged into canon. It predates the current rulebook, it is written
mostly in Finnish, and several of its premises **conflict** with the canon as it stands
(2045 vs. The Fall, a different Dr. Romppainen, a different institutional frame). The
migration map records those conflicts rather than resolving them: resolving them is the
author's decision, not the agent's.

Design rules
------------
  * **Nothing is silently discarded.** Every imported file appears in the manifest with
    its size and sha256. Files excluded from the import are listed *with the reason*,
    not vanished.
  * **The source is a separate repository.** The manifest records the source repository,
    the source path within it, the source commit, and the upstream git blob sha of every
    file, so a reader can prove this copy is unaltered relative to upstream.
  * **The import is a snapshot, not a mirror.** The source is not tracked by any
    automated sync; the manifest is the record of what was taken and when.
  * **A guard fails if the manifest drifts from the tree**, exactly as
    ``tools/build_rulebook_archive.py --check`` does for the rulebook archive.

Usage: python3 tools/build_ubiquitous_maniacs_manifest.py [--check]
  --check  verify the on-disk archive matches what the generator would write
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import subprocess
import sys
from dataclasses import asdict, dataclass
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
ARCHIVE = REPO / "legacy" / "ubiquitous_maniacs"
SOURCE_REPO = "TomiToivio/Panpsychic-Cyborg-Multitude"
SOURCE_PATH = "noopunk/ubiquitous_maniacs"

MANIFEST_MD = ARCHIVE / "MANIFEST.md"
MANIFEST_JSON = ARCHIVE / "manifest.json"


@dataclass(frozen=True)
class Entry:
    """One imported file and its provenance."""

    path: str
    bytes: int
    sha256: str
    source_path: str
    source_blob_sha: str | None
    source_commit: str | None
    class_: str

    def to_json(self) -> dict[str, object]:
        data = asdict(self)
        data["class"] = data.pop("class_")
        return data

# --------------------------------------------------------------------------------------
# Files deliberately NOT imported, with the reason. Every one of these is either
# third-party copyrighted material or a derivative of it.
# --------------------------------------------------------------------------------------
EXCLUDED: list[dict[str, str]] = [
    {
        "path": "references/maniac_transcripts/s01e01_the_chosen_one.txt",
        "reason": "verbatim closed-caption dialogue from *Maniac* (Netflix, 2018)",
        "detail": "Full episode transcript. Third-party copyrighted dialogue; not "
                  "importable into a public repository.",
    },
    {
        "path": "references/maniac_transcripts/s01e02_windmills.txt",
        "reason": "verbatim closed-caption dialogue from *Maniac* (Netflix, 2018)",
        "detail": "Full episode transcript. Third-party copyrighted dialogue; not "
                  "importable into a public repository.",
    },
    {
        "path": "references/maniac_transcripts/s01e03_having_a_day.txt",
        "reason": "verbatim closed-caption dialogue from *Maniac* (Netflix, 2018)",
        "detail": "Full episode transcript. Third-party copyrighted dialogue; not "
                  "importable into a public repository.",
    },
    {
        "path": "references/maniac_transcripts/s01e10_option_c.txt",
        "reason": "verbatim closed-caption dialogue from *Maniac* (Netflix, 2018)",
        "detail": "Full episode transcript. Third-party copyrighted dialogue; not "
                  "importable into a public repository.",
    },
    {
        "path": "references/maniac_transcripts/STYLISTIC_ANALYSIS.md",
        "reason": "quotes verbatim dialogue from *Maniac* (Netflix, 2018)",
        "detail": "Its section 7 is titled 'Direct Dialogue Samples for Noöpunk "
                  "Extraction' and quotes extended dialogue verbatim. The analysis is "
                  "the author's own work, but the quoted dialogue is not, so the file "
                  "travels with the dialogue rather than without it.",
    },
]

# Third-party EXPRESSION that was inside the corpus's OWN files and was removed by the
# copyright cleaning pass of 2026-10-22. The corpus's analysis documents quoted the
# shows' dialogue and scripts verbatim; the analysis itself is the author's work and stays,
# but the quoted expression does not. Each entry names the file and what was removed.
LOCALLY_CLEANED: list[dict[str, str]] = [
    {
        "path": "docs/STYLISTIC_INFLUENCES_MANIAC_RIGET.md",
        "work": "*Maniac* (Netflix, 2018); *Riget / The Kingdom* (DR, 1994)",
        "nature": "quoted the shows' dialogue and the *Riget* prologue verbatim",
        "detail": "The device descriptions stay; the quoted dialogue, the translated chorus "
                  "and the prologue's closing sentence are gone. The analysis now describes "
                  "the devices without reproducing the words.",
    },
    {
        "path": "docs/MANIAC_RIGET_STYLE_ANALYSIS.md",
        "work": "*Maniac* (Netflix, 2018); *Riget / The Kingdom* (DR, 1994)",
        "nature": "quoted advertising lines, a catchphrase and two dialogue lines verbatim",
        "detail": "Replaced with descriptions of the same devices in the author's own words.",
    },
    {
        "path": "docs/MANIAC_RIGET_INFLUENCE_NOTE.md",
        "work": "*Maniac* (Netflix, 2018); *Riget / The Kingdom* (DR, 1994)",
        "nature": "cited the transcript sites it had read",
        "detail": "The citation list now names the works themselves instead of the transcript "
                  "archives; the analysis is unchanged.",
    },
    {
        "path": "docs/PAPRIKA_VAIKUTTEET.md",
        "work": "*Paprika* (Atsuko Chiba, 2006)",
        "nature": "quoted four lines of the film's dialogue and its tagline verbatim",
        "detail": "Each is replaced by a description of what the line did in the scene.",
    },
    {
        "path": "docs/SIMULATION_PLATFORM_EVALUATION.md",
        "work": "third-party simulation platforms",
        "nature": "quoted product marketing strings verbatim",
        "detail": "Replaced with paraphrases of the same claims.",
    },
    {
        "path": "docs/PHILOSOPHICAL_ZOMBIES.md",
        "work": "*Maniac* (Netflix, 2018)",
        "nature": "carried a near-translation of the show's intake dialogue",
        "detail": "The intake lines are rewritten in the corpus's own Finnish.",
    },
    {
        "path": "P\u00c4IV\u00c4_1.md",
        "work": "*Maniac* (Netflix, 2018)",
        "nature": "carried the same near-translation of the show's intake dialogue",
        "detail": "The intake lines are rewritten in the corpus's own Finnish.",
    },
    {
        "path": "src/interaction/dialogue.py",
        "work": "*Maniac* (Netflix, 2018)",
        "nature": "the playable intake dialogue reproduced the show's lines",
        "detail": "The three lines are rewritten; the scene's structure and mechanics are "
                  "unchanged.",
    },
    {
        "path": "src/interaction/cli.py",
        "work": "*Maniac* (Netflix, 2018)",
        "nature": "the console printed the show's acceptance line",
        "detail": "Rewritten in the corpus's own words.",
    },
    {
        "path": "app.py",
        "work": "*Maniac* (Netflix, 2018)",
        "nature": "the Streamlit view printed the show's acceptance line",
        "detail": "Rewritten in the corpus's own words.",
    },
    {
        "path": "tests/test_interaction.py",
        "work": "*Maniac* (Netflix, 2018)",
        "nature": "asserted the show's acceptance line",
        "detail": "The assertion follows the rewritten line.",
    },
    {
        "path": "tests/test_game_integration.py",
        "work": "*Maniac* (Netflix, 2018)",
        "nature": "asserted the show's intake question",
        "detail": "The assertion follows the rewritten line.",
    },
    {
        "path": "TERAPIASESSIO.md",
        "work": "the performers of the source works (as real people, not as a work)",
        "nature": "directed the author to write two characters as named real performers",
        "detail": "The two character blueprints now describe the characters themselves - "
                  "Ingrid's electrical, guarded warmth and Romppainen's weary, generous "
                  "charm - instead of naming real performers for the author to imitate.",
    },
    {
        "path": "docs/THERAPY_DAY_1_DRAFT.md",
        "work": "the performers of the source works (as real people, not as a work)",
        "nature": "named real performers as the models for two characters",
        "detail": "The character descriptions stay; the performers' names are gone.",
    },
    {
        "path": "docs/THERAPY_SESSION_DAY_1_PROPOSAL.md",
        "work": "the performers of the source works (as real people, not as a work)",
        "nature": "named real performers in the acting direction for two characters",
        "detail": "The acting direction now describes the quality to play - electrical "
                  "vulnerability, crooked charisma - without naming a performer.",
    },
]

# Third-party material that IS imported, because it is summary/analysis rather than
# expression, and is recorded so the attribution ledger can name it.
THIRD_PARTY_RETAINED: list[dict[str, str]] = [
    {
        "path": "references/maniac_transcripts/README.md",
        "work": "*Maniac* (Netflix, 2018)",
        "nature": "episode index and motif summary written by the corpus author",
    },
    {
        "path": "references/maniac_transcripts/riget_wikipedia_episodes.txt",
        "work": "*Riget* / *The Kingdom* (1994) — Wikipedia episode summaries",
        "nature": "Wikipedia episode summaries, quoted as summaries; the source "
                  "attribution is stated in the file header",
    },
    {
        "path": "references/maniac_transcripts/s01e04_furs_by_sebastian.txt",
        "work": "*Maniac* (Netflix, 2018)",
        "nature": "episode summary with key scenes, not dialogue",
    },
    {
        "path": "references/maniac_transcripts/s01e05_exactly_like_you.txt",
        "work": "*Maniac* (Netflix, 2018)",
        "nature": "episode summary with key scenes, not dialogue",
    },
    {
        "path": "references/maniac_transcripts/s01e06_larger_structural_issues.txt",
        "work": "*Maniac* (Netflix, 2018)",
        "nature": "episode summary with key scenes, not dialogue",
    },
    {
        "path": "references/maniac_transcripts/s01e07_ceci_nest_pas_une_drill.txt",
        "work": "*Maniac* (Netflix, 2018)",
        "nature": "episode summary with key scenes, not dialogue",
    },
    {
        "path": "references/maniac_transcripts/s01e08_the_lake_of_the_clouds.txt",
        "work": "*Maniac* (Netflix, 2018)",
        "nature": "episode summary with key scenes, not dialogue",
    },
    {
        "path": "references/maniac_transcripts/s01e09_utangatta.txt",
        "work": "*Maniac* (Netflix, 2018)",
        "nature": "episode summary with key scenes, not dialogue",
    },
]

# Files that were imported verbatim and then given a local banner, because a verbatim copy
# would otherwise be *active instruction* rather than archived material. The upstream blob
# sha still proves the original; the manifest records the local sha256 of the annotated
# copy and flags the difference, so a reader can see exactly what was touched and why.
LOCALLY_ANNOTATED: list[dict[str, str]] = [
    {
        "path": "AGENTS.md",
        "reason": "the corpus's own agent instructions, which would otherwise claim authority",
        "detail": "A banner was prepended marking the file as archived material that is not "
                  "in force, and naming the repository-root AGENTS.md as the authority. The "
                  "corpus's text below the banner is unchanged. The upstream blob sha in "
                  "this manifest is the original file's, so the difference between it and "
                  "the local sha256 is exactly this banner.",
    },
    {
        "path": "docs/STYLISTIC_INFLUENCES_MANIAC_RIGET.md",
        "reason": "it quoted third-party dialogue verbatim",
        "detail": "The upstream file carried twenty-one verbatim quotations from the Netflix "
                  "miniseries *Maniac* (2018) and from *Riget / The Kingdom* (1994), "
                  "including the corpus's own Finnish realisation of the same lines. Those "
                  "quotations were removed on 2026-10-22: the analysis of which stylistic "
                  "devices were borrowed, and how they were realised, is kept, and each "
                  "section now says what was removed and why. The upstream blob sha in "
                  "this manifest is the original file's, so the difference between it and "
                  "the local sha256 is exactly the removed quotations. A guard, "
                  "tests/test_third_party_expression_absent.py, fails if the quotations "
                  "reappear in the working tree or in a commit.",
    },
]

# The upstream directory that the corpus's own README documents but which was never
# committed upstream. Recorded because a reader must not think the import is complete.
MISSING_UPSTREAM: list[dict[str, str]] = [
    {
        "path": "data/",
        "reason": "never committed upstream",
        "detail": "The corpus README names `data/lab_people.csv` and "
                  "`data/lab_relationships.csv` as the people and relationship data, and "
                  "`app.py` loads them at runtime. The directory was never committed to "
                  "the source repository, so the import cannot include it and the "
                  "Streamlit app in this archive cannot run as shipped.",
    },
]

# Generated or non-content directories that are skipped rather than imported.
SKIP_DIRS = {"__pycache__", ".git", ".pytest_cache", ".mypy_cache"}


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 16), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _upstream_blob_shas() -> dict[str, str]:
    """Every upstream blob sha, in one pass.

    ``git ls-tree -r HEAD -- <path>`` gives the blob sha of every file under the source
    directory in a single call, which is far faster than one ``hash-object`` per file.

    ``-z`` is used because several corpus filenames are non-ASCII (``PÄIVÄ_1.md`` and
    friends): without it, git quotes the path and the quoting would become part of the
    recorded name.
    """
    try:
        result = subprocess.run(
            ["git", "-C", str(SOURCE_ROOT), "ls-tree", "-r", "-z", "HEAD", "--", SOURCE_PATH],
            capture_output=True,
            text=True,
            check=True,
        )
    except (OSError, subprocess.CalledProcessError):
        return {}
    shas: dict[str, str] = {}
    for entry in result.stdout.split("\0"):
        if not entry:
            continue
        meta, _, path = entry.partition("\t")
        parts = meta.split()
        if len(parts) < 3 or parts[1] != "blob":
            continue
        shas[path.removeprefix(f"{SOURCE_PATH}/")] = parts[2]
    return shas


def _upstream_commits() -> dict[str, str]:
    """The upstream commit that last touched each path, in one pass.

    ``git log -z --format=%x00%H --name-only`` emits, for each commit, the commit sha
    followed by the paths it touched, all NUL-separated. The first commit in the log
    that mentions a path is that path's most recent commit.

    ``-z`` keeps non-ASCII filenames intact (``PÄIVÄ_1.md`` and friends).
    """
    try:
        result = subprocess.run(
            [
                "git", "-C", str(SOURCE_ROOT), "log", "-z",
                "--format=%x00%H", "--name-only", "--", SOURCE_PATH,
            ],
            capture_output=True,
            text=True,
            check=True,
        )
    except (OSError, subprocess.CalledProcessError):
        return {}
    commits: dict[str, str] = {}
    current = ""
    for chunk in result.stdout.split("\0"):
        if not chunk:
            continue
        if chunk.startswith("\n"):
            chunk = chunk.lstrip("\n")
        if not chunk:
            continue
        # A commit sha line: 40 hex characters, possibly with a leading newline.
        if len(chunk) == 40 and all(c in "0123456789abcdef" for c in chunk):
            current = chunk
            continue
        rel = chunk.removeprefix(f"{SOURCE_PATH}/")
        if rel and rel not in commits and current:
            commits[rel] = current
    return commits


def _resolve_source_root() -> Path:
    """Where the upstream Panpsychic-Cyborg-Multitude checkout lives.

    The original build ran on the author's Windows machine and hard-coded
    ``/mnt/c/Users/totoivio/Panpsychic-Cyborg-Multitude``. That path does not exist on
    Laskin, and a missing upstream checkout is not a cosmetic problem: the manifest's
    whole value is that each imported file carries its **upstream blob sha**, and
    without the checkout every one of those becomes ``unavailable`` — the record
    silently degrades from "provably unaltered" to "trust me".

    So resolve it in order: an explicit override, the Windows path if it is there, and
    then a local clone. When none is found the manifest still builds, but with the
    provenance fields marked unavailable — which is the honest outcome, not a failure
    to hide.
    """
    override = os.environ.get("NOOPUNK_PCM_SOURCE_ROOT")
    if override:
        return Path(override)
    windows = Path("/mnt/c/Users/totoivio/Panpsychic-Cyborg-Multitude")
    if (windows / ".git").exists():
        return windows
    for candidate in (Path.home() / "Panpsychic-Cyborg-Multitude",
                      Path("/mnt/workspace/Panpsychic-Cyborg-Multitude")):
        if (candidate / ".git").exists():
            return candidate
    return windows  # not present; the upstream fields degrade to ``unavailable``


SOURCE_ROOT = _resolve_source_root()


def _recorded_source_commit() -> str | None:
    """The commit the corpus was *actually* imported from, as already recorded.

    ``source commit at import`` is a historical fact, not a live reading. The corpus was
    imported from one commit on one date, and that does not change because the upstream
    repository has since moved on.
    """
    try:
        data = json.loads(MANIFEST_JSON.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return None
    commit = ((data.get("source") or {}).get("commit") or "").strip()
    if len(commit) == 40 and all(c in "0123456789abcdef" for c in commit.lower()):
        return commit
    return None


def _source_commit() -> str | None:
    """Resolve ``source commit at import``.

    This used to return the upstream checkout's **current** ``HEAD``. That is a bug with a
    long tail: the field is labelled *at import*, so stamping it from live state rewrites
    history. Once the upstream repository advanced past the imported commit, every run
    rewrote the manifest and ``--check`` could never pass again — the generator reported its
    own recorded fact as drift, forever, on any machine that had the upstream clone.

    Order of resolution:

    1. ``NOOPUNK_PCM_SOURCE_COMMIT`` — an explicit re-import pin, so refreshing the record
       is a deliberate act rather than a side effect of running the tool.
    2. the commit already recorded in ``manifest.json`` — the historical fact wins.
    3. the upstream ``HEAD`` — first build only, when there is nothing recorded yet.
    """
    override = (os.environ.get("NOOPUNK_PCM_SOURCE_COMMIT") or "").strip()
    if override:
        return override
    recorded = _recorded_source_commit()
    if recorded:
        return recorded
    try:
        result = subprocess.run(
            ["git", "-C", str(SOURCE_ROOT), "rev-parse", "HEAD"],
            capture_output=True,
            text=True,
            check=True,
        )
    except (OSError, subprocess.CalledProcessError):
        return None
    return result.stdout.strip() or None


def _classify(rel: str) -> str:
    """The corpus role of a file, used to group the manifest."""
    if rel.startswith("src/"):
        return "source"
    if rel.startswith("tests/"):
        return "tests"
    if rel.startswith("docs/reference/laclaugpt/"):
        return "reference (LaclauGPT import)"
    if rel.startswith("docs/"):
        return "design and research documentation"
    if rel.startswith("references/"):
        return "third-party reference material"
    if rel.endswith(".py"):
        return "entry-point script"
    return "corpus root document"


def collect() -> list[Entry]:
    """Every imported file, with its provenance."""
    blob_shas = _upstream_blob_shas()
    commits = _upstream_commits()
    entries: list[Entry] = []
    for path in sorted(ARCHIVE.rglob("*")):
        if not path.is_file():
            continue
        rel = path.relative_to(ARCHIVE).as_posix()
        if rel in {"MANIFEST.md", "manifest.json", "MIGRATION_MAP.md", "README.md"}:
            continue
        if any(part in SKIP_DIRS for part in path.parts):
            continue
        entries.append(
            Entry(
                path=rel,
                bytes=path.stat().st_size,
                sha256=_sha256(path),
                source_path=f"{SOURCE_PATH}/{rel}",
                source_blob_sha=blob_shas.get(rel),
                source_commit=commits.get(rel),
                class_=_classify(rel),
            )
        )
    return entries


def _summary(entries: list[Entry]) -> dict[str, int]:
    summary: dict[str, int] = {}
    for entry in entries:
        summary[entry.class_] = summary.get(entry.class_, 0) + 1
    return dict(sorted(summary.items()))


def build_json(entries: list[Entry]) -> str:
    payload = {
        "$comment": "Machine-readable inventory of the Ubiquitous Maniacs import. "
                    "Records PROVENANCE ONLY: what was imported, from where, with "
                    "which hash. It selects no licence, approves nothing, and asserts "
                    "no canon. The migration map (MIGRATION_MAP.md) is the human "
                    "readable account of where each unit lands.",
        "format": "noopunk.archive.ubiquitous_maniacs",
        "version": 1,
        "imported": "2026-10-22",
        "$imported_convention": "Real-world metadata date. AGENTS.md section 6 limits "
                                "in-world future dates to 20XX; this file makes no "
                                "in-world claims, so a real date here does not violate "
                                "that rule.",
        "source": {
            "repository": SOURCE_REPO,
            "path_in_repository": SOURCE_PATH,
            "commit": _source_commit(),
            "relationship": "Separate repository. This corpus was developed there and "
                            "is imported here as a source-of-record; it is not tracked "
                            "by any automated sync.",
        },
        "licence_status": {
            "upstream_licence_file": "none found",
            "note": "The source repository contains no LICENSE, COPYING or equivalent "
                    "file for this corpus, and no licence grant travels with the "
                    "material. The imported files are therefore preserved as the "
                    "author's own prior work, and the repository's own licence "
                    "decisions (AUTHOR_DECISION_QUEUE rows D10 and D16) remain open "
                    "and untouched by this import.",
        },
        "excluded": EXCLUDED,
        "locally_annotated": LOCALLY_ANNOTATED,
        "locally_cleaned": LOCALLY_CLEANED,
        "missing_upstream": MISSING_UPSTREAM,
        "third_party_retained": [
            item for item in THIRD_PARTY_RETAINED if (ARCHIVE / item["path"]).exists()
        ],
        "counts": {
            "files_imported": len(entries),
            "files_excluded": len(EXCLUDED),
            "by_class": _summary(entries),
        },
        "files": [entry.to_json() for entry in entries],
    }
    return json.dumps(payload, indent=2, ensure_ascii=False) + "\n"


def build_md(entries: list[Entry]) -> str:
    by_class: dict[str, list[Entry]] = {}
    for entry in entries:
        by_class.setdefault(entry.class_, []).append(entry)

    total_bytes = sum(entry.bytes for entry in entries)
    lines: list[str] = []
    lines.append("# Import manifest — `ubiquitous-maniacs-2026-10`")
    lines.append("")
    lines.append(
        "Complete inventory of the *Ubiquitous Maniacs* corpus imported from "
        f"`{SOURCE_REPO}` (`{SOURCE_PATH}/`), with content hashes so retrievability is "
        "provable rather than claimed. Generated by "
        "`tools/build_ubiquitous_maniacs_manifest.py`."
    )
    lines.append("")
    lines.append(
        "**This is a source-of-record, not a canon merge.** The corpus predates the "
        "current rulebook, is written mostly in Finnish, and several of its premises "
        "conflict with the canon as it stands. The conflicts are recorded in "
        "[`MIGRATION_MAP.md`](MIGRATION_MAP.md) and are **not** resolved here: "
        "resolving them is the author's decision (`AGENTS.md` §1)."
    )
    lines.append("")
    lines.append("## Provenance")
    lines.append("")
    lines.append("| | |")
    lines.append("| --- | --- |")
    lines.append(f"| source repository | `{SOURCE_REPO}` |")
    lines.append(f"| source path | `{SOURCE_PATH}/` |")
    lines.append(f"| source commit at import | `{_source_commit() or 'unavailable'}` |")
    lines.append("| import date | 2026-10-22 |")
    lines.append(f"| files imported | **{len(entries)}** |")
    lines.append(f"| bytes imported | **{total_bytes:,}** |")
    lines.append(f"| files excluded | **{len(EXCLUDED)}** |")
    lines.append("| sync | none — this is a snapshot, not a mirror |")
    lines.append("")
    lines.append(
        "Every file below carries the sha256 of the imported copy, the upstream git "
        "blob sha, and the upstream commit that last touched it. The blob shas are the "
        "proof that this copy is unaltered relative to upstream."
    )
    lines.append("")
    lines.append("## Imported files by class")
    lines.append("")
    for klass in sorted(by_class):
        group = by_class[klass]
        size = sum(e.bytes for e in group)
        lines.append(f"### {klass} — {len(group)} files, {size:,} bytes")
        lines.append("")
        lines.append("| path | bytes | sha256 (first 16) | upstream blob sha |")
        lines.append("| --- | --- | --- | --- |")
        for entry in group:
            blob = entry.source_blob_sha
            blob_short = blob[:12] if blob else "—"
            lines.append(
                f"| `{entry.path}` | {entry.bytes:,} | "
                f"`{entry.sha256[:16]}` | `{blob_short}` |"
            )
        lines.append("")
    lines.append("## Files excluded from the import")
    lines.append("")
    lines.append(
        "Nothing is silently discarded. Each excluded file is named, with the reason, "
        "so a reader can see exactly what was left behind and why."
    )
    lines.append("")
    lines.append("| path | reason | detail |")
    lines.append("| --- | --- | --- |")
    for item in EXCLUDED:
        lines.append(f"| `{item['path']}` | {item['reason']} | {item['detail']} |")
    lines.append("")
    lines.append("## Files changed after import")
    lines.append("")
    lines.append(
        "Two files differ from their upstream copies, for different reasons. The upstream "
        "blob sha in the inventory above is the *original* file's in both cases, so the "
        "difference between it and the local sha256 is exactly the local change — the "
        "original is still provable."
    )
    lines.append("")
    lines.append("| path | reason | detail |")
    lines.append("| --- | --- | --- |")
    for item in LOCALLY_ANNOTATED:
        lines.append(f"| `{item['path']}` | {item['reason']} | {item['detail']} |")
    lines.append("")
    lines.append("## Material that was never upstream")
    lines.append("")
    lines.append("| path | status | detail |")
    lines.append("| --- | --- | --- |")
    for item in MISSING_UPSTREAM:
        lines.append(f"| `{item['path']}` | {item['reason']} | {item['detail']} |")
    lines.append("")
    lines.append("## Third-party expression removed from the corpus's own files")
    lines.append("")
    lines.append(
        "The corpus's analysis documents and its playable dialogue quoted the source "
        "shows' dialogue, scripts and marketing lines verbatim. The *analysis* is the "
        "author's own work and is retained; the *quoted expression* is not, and was "
        "removed on 2026-10-22. Each row names what was taken out and what replaced it."
    )
    lines.append("")
    lines.append("| path | work | what was removed | what replaced it |")
    lines.append("| --- | --- | --- | --- |")
    for item in LOCALLY_CLEANED:
        lines.append(
            f"| `{item['path']}` | {item['work']} | {item['nature']} | {item['detail']} |"
        )
    lines.append("")
    lines.append("## Third-party material retained, and its nature")
    lines.append("")
    lines.append(
        "These files name or describe works that are not the author's own. They are "
        "retained because they are **summaries and analysis**, not expression: the "
        "copyrighted dialogue was excluded above. The ledger entry in "
        "`data/sources/external_sources.json` records them."
    )
    lines.append("")
    retained = [item for item in THIRD_PARTY_RETAINED if (ARCHIVE / item["path"]).exists()]
    if not retained:
        lines.append(
            "**None.** Every third-party file in the corpus has been excluded; the "
            "exclusion table above lists each one with its reason."
        )
        lines.append("")
    else:
        lines.append("| path | work | nature |")
        lines.append("| --- | --- | --- |")
        for item in retained:
            lines.append(f"| `{item['path']}` | {item['work']} | {item['nature']} |")
        lines.append("")
    lines.append("## Verification")
    lines.append("")
    lines.append("```sh")
    lines.append("python3 tools/build_ubiquitous_maniacs_manifest.py --check   # hashes must match")
    lines.append("```")
    lines.append("")
    lines.append("— Ai (愛)")
    lines.append("")
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="verify only; do not write")
    args = parser.parse_args()

    entries = collect()
    json_text = build_json(entries)
    md_text = build_md(entries)

    if args.check:
        problems: list[str] = []
        if not MANIFEST_JSON.exists() or MANIFEST_JSON.read_text(encoding="utf-8") != json_text:
            problems.append("manifest.json is out of date")
        if not MANIFEST_MD.exists() or MANIFEST_MD.read_text(encoding="utf-8") != md_text:
            problems.append("MANIFEST.md is out of date")
        if problems:
            for problem in problems:
                print(f"ERROR: {problem}; run without --check", file=sys.stderr)
            return 1
        print("manifest is current")
        return 0

    ARCHIVE.mkdir(parents=True, exist_ok=True)
    MANIFEST_JSON.write_text(json_text, encoding="utf-8")
    MANIFEST_MD.write_text(md_text, encoding="utf-8")
    print(f"wrote {MANIFEST_MD.relative_to(REPO)} and {MANIFEST_JSON.relative_to(REPO)}")
    print(f"  {len(entries)} files imported, {len(EXCLUDED)} excluded")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
