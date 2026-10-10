"""Release packaging guard for issue #231 (parent epic #200).

The #200 licence work already audits sources (``data/sources/game_system_rights.json``),
itemizes licence/NOTICE/attribution choices (``docs/licenses/ISSUE_200_LICENSE_AND_NOTICE_PLAN.md``)
and states a reuse boundary (``docs/licenses/ISSUE_200_CC_RELEASE_GATE.md``). What the gate
document's own checklist still lacked was its last item:

    "Add checks that flag unreviewed third-party material in packaging and prevent
     reintroduction of explicitly excluded licenses."

This module is that check. It is a *packaging* gate, not a licence and not a legal clearance:

* It never selects a licence and never writes ``LICENSE``/``NOTICE``.
* Its excluded-licence vocabulary is READ FROM the rights ledger's ``decision_vocabulary``,
  so the ledger stays the single source of truth and a second hand-maintained exclusion list
  cannot drift from it.
* It fails closed: a missing or unparseable policy/ledger is an error, not a pass.

Two modes, and the strictness follows from whether you named the bundle:

* **Full-tree scan** (no ``--bundle``): every tracked file is checked. Findings about
  unreviewed paths and documented licence mentions are WARNINGS, because a mid-development
  tree legitimately contains both. Internal inconsistency is still an ERROR. Use this in CI.
* **Explicit bundle** (``--bundle manifest.txt``): the listed paths are the release set, so a
  quarantined or unreviewed path in it is an ERROR. This is the actual packaging gate.

``--mode public`` additionally fails while the author's licence decision is open, because a
real release may not be declared clean on an unmade choice.

Usage::

    python3 tools/release_packaging_guard.py --mode audit                  # CI, full tree
    python3 tools/release_packaging_guard.py --bundle bundle.txt --mode public
"""

from __future__ import annotations

import argparse
import fnmatch
import json
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Iterable, Sequence

REPO_ROOT = Path(__file__).resolve().parent.parent

POLICY_PATH = "data/licenses/release_packaging_policy.json"
LEDGER_PATH = "data/sources/game_system_rights.json"

# Never walked, never released: VCS metadata, caches, editor droppings.
SKIP_DIRS = {".git", "__pycache__", ".pytest_cache", ".mypy_cache", "node_modules",
             ".ruff_cache", "ruff_cache"}
SKIP_FILES = {".DS_Store"}

ERROR = "error"
WARNING = "warning"


@dataclass
class Finding:
    severity: str
    code: str
    message: str
    path: str | None = None

    def __str__(self) -> str:
        where = f" [{self.path}]" if self.path else ""
        return f"{self.severity.upper():7} {self.code}: {self.message}{where}"


@dataclass
class GuardResult:
    mode: str
    bundle: list[str] | None = None
    findings: list[Finding] = field(default_factory=list)

    @property
    def errors(self) -> list[Finding]:
        return [f for f in self.findings if f.severity == ERROR]

    @property
    def warnings(self) -> list[Finding]:
        return [f for f in self.findings if f.severity == WARNING]

    @property
    def ok(self) -> bool:
        return not self.errors

    def format(self) -> str:
        scope = f"bundle of {len(self.bundle)} path(s)" if self.bundle is not None else "full tree"
        lines = [f"release packaging guard — mode={self.mode}, {scope}"]
        lines += [str(f) for f in self.findings] or ["no findings"]
        verdict = "PASS" if self.ok else "FAIL"
        lines.append(f"{verdict}: {len(self.errors)} error(s), {len(self.warnings)} warning(s)")
        return "\n".join(lines)


def _load_json(root: Path, rel: str) -> dict:
    """Load a JSON file, raising a clear error rather than silently returning {}."""
    path = root / rel
    if not path.exists():
        raise FileNotFoundError(f"required file is missing: {rel}")
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:  # fail closed
        raise ValueError(f"{rel} is not valid JSON: {exc}") from exc


def load_policy(root: Path = REPO_ROOT) -> dict:
    return _load_json(root, POLICY_PATH)


def load_ledger(root: Path = REPO_ROOT) -> dict:
    return _load_json(root, LEDGER_PATH)


def _normalize(rel: str) -> str:
    """Repo-relative POSIX path.

    Only a single leading ``./`` is stripped. ``str.lstrip('./')`` would eat a leading dot
    from real entries such as ``.github/``, mis-matching them as ``github/``.
    """
    rel = str(rel).replace("\\", "/")
    while rel.startswith("./"):
        rel = rel[2:]
    return rel


def path_matches_glob(rel: str, pattern: str) -> bool:
    """Match a repo-relative path against a policy glob.

    ``fnmatch`` alone does not let ``**/`` span zero directories, so anchor the pattern
    explicitly: ``src/**`` must match both ``src/x.py`` and ``src/a/b.py``.
    """
    rel, pattern = _normalize(rel), _normalize(pattern)
    if pattern.endswith("/**"):
        prefix = pattern[:-3]
        return rel == prefix or rel.startswith(prefix + "/")
    return fnmatch.fnmatch(rel, pattern)


def classify_path(rel: str, policy: dict) -> str | None:
    """Return the artifact-class id covering ``rel``, or None if unreviewed."""
    for cls in policy["artifact_classes"]:
        if any(path_matches_glob(rel, g) for g in cls["globs"]):
            return cls["id"]
    return None


def quarantine_reason(rel: str, policy: dict) -> str | None:
    for entry in policy["quarantined_paths"]:
        if path_matches_glob(rel, entry["glob"]):
            return entry["reason"]
    return None


def iter_tree_paths(root: Path) -> Iterable[str]:
    """Every release-bound path in the working tree."""
    for path in sorted(root.rglob("*")):
        if not path.is_file():
            continue
        rel = _normalize(str(path.relative_to(root)))
        parts = set(rel.split("/"))
        if parts & SKIP_DIRS or rel in SKIP_FILES:
            continue
        yield rel


def documented_mentions(root: Path, rel: str, markers: Sequence[str]) -> list[str]:
    """Excluded-licence names literally present in a text file (inventory, not a verdict)."""
    try:
        text = (root / rel).read_text(encoding="utf-8")
    except (UnicodeDecodeError, OSError):
        return []
    return [m for m in markers if m in text]


def check_policy_consistency(policy: dict, ledger: dict) -> list[Finding]:
    """The policy's exclusion vocabulary must exist in the ledger it defers to."""
    vocab = set(ledger.get("decision_vocabulary", {}).keys())
    if not vocab:
        return [Finding(ERROR, "ledger-vocabulary-empty",
                        "the rights ledger exposes no decision_vocabulary to defer to")]
    return [
        Finding(ERROR, "excluded-decision-not-in-ledger",
                f"policy excludes decision {d!r}, which the rights ledger does not define "
                f"— the two have drifted apart")
        for d in policy.get("excluded_licence_decisions", [])
        if d not in vocab
    ]


def check_class_licences(policy: dict) -> list[Finding]:
    """An artifact class may not be declared under an excluded licence decision.

    This is the class-level half of "prevent reintroduction of explicitly excluded licenses":
    the quarantine list catches the known EP2 paths, and this catches the mistake of
    *declaring* a release class under a licence the ledger says cannot ship.
    """
    excluded = set(policy.get("excluded_licence_decisions", []))
    return [
        Finding(ERROR, "class-declared-under-excluded-licence",
                f"artifact class {cls['id']!r} is declared as {cls.get('licence')!r}, which the "
                f"policy excludes from a release")
        for cls in policy.get("artifact_classes", [])
        if cls.get("licence") in excluded
    ]


def check_paths(root: Path, paths: Sequence[str], policy: dict, strict: bool) -> list[Finding]:
    """Quarantine and coverage checks. ``strict`` turns warnings into errors."""
    findings: list[Finding] = []
    sev = ERROR if strict else WARNING
    markers = policy.get("documented_mention_markers", [])

    for rel in paths:
        rel = _normalize(rel)

        reason = quarantine_reason(rel, policy)
        if reason:
            # In a full-tree audit this is informational: the prototype legitimately lives in
            # the repo, and the release step is what must exclude it. In an explicit bundle it
            # means the release set actually contains it, which is an error.
            findings.append(Finding(
                sev, "quarantined-path-in-release-set",
                f"quarantined material would be released: {reason}", rel))
            continue

        if classify_path(rel, policy) is None:
            findings.append(Finding(
                sev, "unreviewed-material",
                "path is covered by no artifact class in the licence plan; unreviewed "
                "third-party material must not ship", rel))

        # Always a warning, never an error, in every mode. A provenance note that names an
        # excluded licence is indistinguishable by inspection from copied expression, so this
        # check is an INVENTORY for human review. The enforceable checks are the quarantine
        # list, the coverage check and the class-licence check.
        hits = documented_mentions(root, rel, markers)
        if hits:
            findings.append(Finding(
                WARNING, "documented-licence-mention",
                f"names excluded licences {hits} — expected in provenance prose; confirm it is "
                f"documentation and not adapted expression", rel))
    return findings


def check_author_decision(policy: dict, mode: str) -> list[Finding]:
    if mode != "public" or not policy.get("author_decision_open", False):
        return []
    pending = sorted({
        c["id"] for c in policy.get("artifact_classes", [])
        if str(c.get("licence", "")).startswith("author-decision")
    })
    return [Finding(
        ERROR, "licence-decision-open",
        "a public release cannot be declared clean while the author's licence decision is "
        f"open; unresolved artifact classes: {pending}")]


def run_guard(root: Path = REPO_ROOT, mode: str = "audit",
              bundle: Sequence[str] | None = None) -> GuardResult:
    """Run every packaging check. ``bundle=None`` scans the whole tree."""
    if mode not in ("audit", "public"):
        raise ValueError(f"unknown mode {mode!r}; expected 'audit' or 'public'")

    policy = load_policy(root)
    ledger = load_ledger(root)
    paths = [_normalize(p) for p in bundle] if bundle is not None else list(iter_tree_paths(root))

    findings: list[Finding] = []
    findings += check_policy_consistency(policy, ledger)
    findings += check_class_licences(policy)
    findings += check_paths(root, paths, policy, strict=bundle is not None)
    findings += check_author_decision(policy, mode)

    findings.sort(key=lambda f: (f.code, f.path or ""))
    return GuardResult(mode=mode, bundle=list(paths) if bundle is not None else None,
                       findings=findings)


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="issue #231 release packaging guard")
    parser.add_argument("--mode", choices=("audit", "public"), default="audit")
    parser.add_argument("--bundle", help="file listing the release set, one path per line")
    parser.add_argument("--root", default=str(REPO_ROOT))
    args = parser.parse_args(argv)

    bundle = None
    if args.bundle:
        bundle = [ln.strip() for ln in Path(args.bundle).read_text(encoding="utf-8").splitlines()
                  if ln.strip() and not ln.startswith("#")]

    result = run_guard(Path(args.root), args.mode, bundle)
    print(result.format())
    return 0 if result.ok else 1


if __name__ == "__main__":
    sys.exit(main())
