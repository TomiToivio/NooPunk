"""The human-only boundary around `NooPunk-Story/Story/`, enforced on the diff (#1295).

Tomi's prose is the source of truth, and no agent may write it — not while refactoring, not while
converting it to a Story Graph, not as a side effect of anything. `AGENTS.md`, `CODEOWNERS` and
`tests/test_issue_1295_structure.py` state and protect the rule; none of them can *see* a committed edit
to the manuscript, because agents commit under the repository owner's identity.

This tool can. It reads the paths a branch changed and refuses any of them inside
`NooPunk-Story/Story/`. The single allowlisted path is the boundary note the skeleton installed there
(`Story/README.md` is policy, not prose) — and even that changes only with the `story-authored-by-tomi`
label, which a human applies on the pull request itself.

Usage:

    python3 tools/story_boundary.py                      # diff against origin/main
    python3 tools/story_boundary.py --base origin/main
    python3 tools/story_boundary.py --paths A B C        # check an explicit list (tests, hooks)

Exit codes: 0 clean, 1 violation found, 2 the diff could not be read.
"""
from __future__ import annotations

import argparse
import subprocess
import sys
from collections.abc import Iterable, Sequence

__all__ = ["ALLOWED", "STORY_DIR", "changed_paths", "main", "violations"]

#: The human-only directory, without a trailing slash so a prefix test cannot match a sibling name.
STORY_DIR = "NooPunk-Story/Story"

#: The boundary note: policy about the directory, not content in it. Never the manuscript.
ALLOWED = frozenset({f"{STORY_DIR}/README.md"})


def normalize(path: str) -> str:
    """Repo-relative POSIX path, so a Windows checkout's separators cannot slip past the check."""
    path = str(path).strip().replace("\\", "/")
    while path.startswith("./"):
        path = path[2:]
    return path


def violations(paths: Iterable[str]) -> list[str]:
    """Every changed path inside the human-only directory that is not the boundary note."""
    inside = []
    for raw in paths:
        path = normalize(raw)
        if not path:
            continue
        inside_dir = path == STORY_DIR or path.startswith(STORY_DIR + "/")
        if inside_dir and path not in ALLOWED:
            inside.append(path)
    return sorted(set(inside))


def changed_paths(base: str, root: str = ".") -> list[str]:
    """Paths changed on this branch relative to ``base``, using the merge base git already knows."""
    completed = subprocess.run(
        ["git", "-C", root, "diff", "--name-only", f"{base}...HEAD"],
        capture_output=True, text=True, check=False,
    )
    if completed.returncode != 0:
        raise RuntimeError(completed.stderr.strip() or f"git diff against {base!r} failed")
    return [line for line in completed.stdout.splitlines() if line.strip()]


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Refuse any change to NooPunk-Story/Story/ except its boundary note (#1295).",
    )
    parser.add_argument("--base", default="origin/main", help="ref to diff against (default origin/main)")
    parser.add_argument("--paths", nargs="+", help="explicit paths to check instead of reading a diff")
    parser.add_argument("--root", default=".", help="repository root for the git call")
    arguments = parser.parse_args(argv)

    if arguments.paths:
        paths = list(arguments.paths)
    else:
        try:
            paths = changed_paths(arguments.base, arguments.root)
        except (RuntimeError, FileNotFoundError) as error:
            print(f"story-boundary: cannot read the diff: {error}", file=sys.stderr)
            return 2

    offenders = violations(paths)
    if offenders:
        print(
            "story-boundary: NooPunk-Story/Story/ is Tomi's to write. This branch changes:\n"
            + "\n".join(f"  {path}" for path in offenders)
            + "\n\nPropose the change to Tomi instead (a review note or an issue comment). If he made"
              "\nthis edit himself, the pull request carries the `story-authored-by-tomi` label.",
            file=sys.stderr,
        )
        return 1

    print(f"story-boundary: {len(paths)} changed path(s), none inside {STORY_DIR}/")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
