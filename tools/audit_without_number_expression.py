"""Issue #569 — measure actual textual overlap between this tree and the Without Number books.

The rights matrix (`docs/licenses/ISSUE_569_WITHOUT_NUMBER_RIGHTS.md`) leaves one item open in its
own words: *"a complete repository-wide similarity audit remains outstanding"*. It also states the
reason a keyword search cannot close it — a name ban "would falsely reject legitimate attribution and
miss paraphrased copying". This tool is the honest version: an **n-gram containment audit**.

It answers one question: *does any file in this tree contain a run of N consecutive words that also
appears in a licence-blocked source document?* Ten words is long enough that a match is copying rather
than coincidence, and short enough to catch a lifted sentence fragment.

Design decisions that matter:

* **Two corpora, because a match alone is not a verdict.** The *blocked* corpus is the licence-blocked
  books — Stars Without Number Revised and Ashes Without Number. The *attributable* corpus is the CC0
  SRD text — Cities Without Number and Worlds Without Number. A hit that also appears in the CC0 SRD
  is **usable with attribution**; a hit that appears *only* in a blocked edition is the thing this
  audit exists to catch. Reporting one number instead of two would either excuse copying or cry wolf.
* **No third-party text is ever printed, stored or committed.** The report names *our* file, the line,
  and how many matched words there were. Printing the matched run would reproduce exactly the
  expression the audit exists to keep out.
* **The corpus is not shippable**, so this is an operator tool and not a CI gate: the books live on the
  operator's disk and must not enter the repository. `tools/release_packaging_guard.py` remains the
  CI-side gate (manifest, licence resolution, quarantine policy).
* **Quarantined paths are separated, not ignored.** `legacy/` and `archive/` are preserved corpora that
  the release policy already excludes; they are reported in their own section so a real violation in
  first-party paths is never hidden by them.

Usage::

    python3 tools/audit_without_number_expression.py \
        --source /path/StarsWithoutNumberRevised-FreeEdition-122917.pdf \
        --source /path/AshesWithoutNumber_FreeVersion_071025.pdf \
        --cc0-source /path/CWN-SRD-V5 \
        --cc0-source /path/WWNSRDV1

    python3 tools/audit_without_number_expression.py --json --source ...   # machine-readable
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from collections import Counter
from dataclasses import dataclass, field
from pathlib import Path
from typing import Iterable, Iterator, Mapping, Sequence

REPO_ROOT = Path(__file__).resolve().parent.parent

#: Consecutive-word run length. Ten is the threshold: long enough that a shared run is copying.
SHINGLE_WORDS = 10

#: Files whose text is compared. Deliberately no binaries, no PDFs, no generated archives.
SCANNED_SUFFIXES = (".md", ".py", ".json", ".yaml", ".yml", ".gd", ".txt", ".html")

#: Never walked. `.git` is metadata; `__pycache__` is bytecode.
SKIP_DIRS = {".git", "__pycache__", ".pytest_cache", ".mypy_cache", "node_modules", ".ruff_cache"}

#: Preserved corpora the release policy already excludes. Reported separately.
QUARANTINE_PREFIXES = ("legacy/", "archive/", "docs/archive/", "rulebook/source_snapshots/")

_WORD = re.compile(r"[a-z0-9']+")


def words(text: str) -> list[str]:
    """Normalise to lowercase word tokens with punctuation and case removed."""
    return _WORD.findall(text.lower())


def _hash(phrase: str) -> int:
    return int.from_bytes(hashlib.blake2b(phrase.encode("utf-8"), digest_size=8).digest(), "big")


def shingles(token_stream: Sequence[str], size: int = SHINGLE_WORDS) -> set[int]:
    """Hashes of every `size`-word run. A set, because repetition in the source is irrelevant."""
    if len(token_stream) < size:
        return set()
    return {_hash(" ".join(token_stream[i:i + size])) for i in range(len(token_stream) - size + 1)}


@dataclass
class Corpus:
    """The licence-blocked books, reduced to shingle hashes (no text retained)."""

    documents: dict[str, int] = field(default_factory=dict)  # doc id -> number of shingles
    hashes: set[int] = field(default_factory=set)            # union

    def add(self, doc_id: str, text: str) -> None:
        found = shingles(words(text))
        self.documents[doc_id] = len(found)
        self.hashes |= found


@dataclass(frozen=True)
class Finding:
    path: str
    line: int
    matched_words: int
    quarantined: bool
    also_in_cc0: bool = False


def corpus_from_paths(specs: Iterable[str]) -> Corpus:
    """Build a corpus from PDFs or directories of `.md`/`.txt` (the SRD repos are markdown)."""
    corpus = Corpus()
    for spec in specs:
        path = Path(spec)
        if path.is_dir():
            text = "\n".join(
                p.read_text(encoding="utf-8")
                for p in sorted(path.rglob("*"))
                if p.is_file() and p.suffix.lower() in (".md", ".txt")
            )
            corpus.add(path.name, text)
        elif path.suffix.lower() == ".pdf":
            corpus.add(path.name, pdf_text(path))
        else:
            corpus.add(path.name, path.read_text(encoding="utf-8"))
    return corpus


def pdf_text(path: Path) -> str:
    """Extract text from a PDF. Imported lazily so the tool runs without PyMuPDF on PATH.

    `pymupdf` is tried before `fitz` because the legacy `fitz` shim prints a deprecation warning to
    stdout, which would corrupt `--json` output.
    """
    try:
        import pymupdf as fitz  # type: ignore[import-not-found]
    except ImportError:
        try:
            import fitz  # type: ignore[import-not-found,no-redef]
        except ImportError:  # pragma: no cover - operator environment detail
            raise SystemExit(
                "PyMuPDF is required for PDF sources (pip install pymupdf), or pass "
                "--source-text with pre-extracted .txt files instead."
            ) from None
    with fitz.open(str(path)) as doc:
        return "\n".join(page.get_text() for page in doc)


def iter_text_files(root: Path = REPO_ROOT) -> Iterator[Path]:
    for path in sorted(root.rglob("*")):
        if not path.is_file() or path.suffix.lower() not in SCANNED_SUFFIXES:
            continue
        if any(part in SKIP_DIRS for part in path.parts):
            continue
        yield path


def is_quarantined(rel: str) -> bool:
    return any(rel.startswith(prefix) for prefix in QUARANTINE_PREFIXES)


def scan_file(path: Path, corpus: Corpus, root: Path = REPO_ROOT,
              size: int = SHINGLE_WORDS, attributable: Corpus | None = None) -> list[Finding]:
    """Find every run of `size` words in `path` that also occurs in the corpus.

    Line numbers are recovered by tracking token positions, so a finding points at the first line of
    the matched run without ever printing the matched text.
    """
    try:
        text = path.read_text(encoding="utf-8")
    except (UnicodeDecodeError, OSError):
        return []
    tokens = words(text)
    if len(tokens) < size or not corpus.hashes:
        return []

    # Token index -> line number, so a hit can be located without quoting it.
    line_of: list[int] = []
    line = 1
    for raw_line in text.splitlines(keepends=True):
        line_of.extend([line] * len(words(raw_line)))
        line += raw_line.count("\n")
    while len(line_of) < len(tokens):
        line_of.append(line)

    rel = path.relative_to(root).as_posix()
    quarantined = is_quarantined(rel)
    findings: list[Finding] = []
    for i in range(len(tokens) - size + 1):
        digest = _hash(" ".join(tokens[i:i + size]))
        if digest in corpus.hashes:
            findings.append(Finding(
                rel, line_of[i], size, quarantined,
                also_in_cc0=bool(attributable and digest in attributable.hashes),
            ))
    return findings


def audit(corpus: Corpus, attributable: Corpus | None = None, root: Path = REPO_ROOT,
          size: int = SHINGLE_WORDS) -> dict:
    """Scan `root` against a *blocked* corpus, classifying hits that also occur in a CC0 corpus."""
    attributable = attributable or Corpus()
    findings: list[Finding] = []
    scanned = 0
    for path in iter_text_files(root):
        scanned += 1
        findings.extend(scan_file(path, corpus, root, size, attributable))

    def summarise(rows: Iterable[Finding]) -> dict:
        rows = list(rows)
        blocked_only = [f for f in rows if not f.also_in_cc0]
        return {
            "hits": len(rows),
            "blocked_only": len(blocked_only),
            "attributable": len(rows) - len(blocked_only),
            "files": [{"path": p, "hits": n,
                       "blocked_only": sum(1 for f in blocked_only if f.path == p)}
                      for p, n in sorted(Counter(f.path for f in rows).items())],
        }

    first_party = summarise(f for f in findings if not f.quarantined)
    quarantined = summarise(f for f in findings if f.quarantined)
    return {
        "format": "noopunk.issue569.similarity_audit",
        "version": 1,
        "issue": 569,
        "shingle_words": size,
        "corpus": {"documents": corpus.documents, "unique_shingles": len(corpus.hashes)},
        "attributable_corpus": {"documents": attributable.documents,
                                "unique_shingles": len(attributable.hashes)},
        "scanned_files": scanned,
        "first_party": first_party,
        "quarantined": quarantined,
        "clean": first_party["blocked_only"] == 0,
    }


def format_report(report: Mapping, *, limit: int = 25) -> str:
    corpus = report["corpus"]
    attributable = report["attributable_corpus"]
    lines = [
        "Without Number expression audit — issue #569 (n-gram containment; no source text retained)",
        f"corpus: {', '.join(f'{k} ({v} shingles)' for k, v in corpus['documents'].items())}"
        f" — {corpus['unique_shingles']} unique {report['shingle_words']}-word runs",
        f"attributable (CC0 SRD): {', '.join(f'{k} ({v})' for k, v in attributable['documents'].items())}"
        f" — {attributable['unique_shingles']} unique runs",
        f"scanned: {report['scanned_files']} text files",
        "",
        f"First-party hits: {report['first_party']['hits']} "
        f"({report['first_party']['blocked_only']} blocked-only, "
        f"{report['first_party']['attributable']} attributable)",
    ]
    for row in report["first_party"]["files"][:limit]:
        lines.append(f"   {row['path']}: {row['hits']} ({row['blocked_only']} blocked-only)")
    if not report["first_party"]["files"]:
        lines.append("   none — no first-party file shares a 10-word run with the corpus")
    lines.append("")
    lines.append(f"Quarantined hits: {report['quarantined']['hits']} "
                 f"({report['quarantined']['blocked_only']} blocked-only) "
                 f"in {len(report['quarantined']['files'])} preserved-corpus files")
    for row in report["quarantined"]["files"][:limit]:
        lines.append(f"   {row['path']}: {row['hits']} ({row['blocked_only']} blocked-only)")
    return "\n".join(lines)


def main(argv: Iterable[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--source", action="append", default=[], metavar="PDF",
                        help="licence-blocked book (can be repeated)")
    parser.add_argument("--source-text", action="append", default=[], metavar="TXT",
                        help="pre-extracted text of a book (can be repeated)")
    parser.add_argument("--cc0-source", action="append", default=[], metavar="PATH",
                        help="CC0 SRD (PDF, .md/.txt file, or a directory of markdown); "
                             "a hit that also appears here is attributable rather than a violation")
    parser.add_argument("--root", default=str(REPO_ROOT), help="tree to scan")
    parser.add_argument("--words", type=int, default=SHINGLE_WORDS, help="run length")
    parser.add_argument("--json", action="store_true", help="emit JSON")
    args = parser.parse_args(list(argv) if argv is not None else None)

    if not args.source and not args.source_text:
        parser.error("at least one --source or --source-text is required")
    blocked = corpus_from_paths([*args.source, *args.source_text])
    cc0 = corpus_from_paths(args.cc0_source)
    report = audit(blocked, cc0, Path(args.root), args.words)
    print(json.dumps(report, indent=2) if args.json else format_report(report))
    return 0 if report["clean"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
