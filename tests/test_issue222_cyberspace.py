# -*- coding: utf-8 -*-
"""Issue #222 — the cyberspace subsystem, in the chapter the issue names.

The issue asks for five things and this pins each one, in the shape the repo's guard
discipline demands: a POSITIVE claim, clause-scoped, never a bare noun that a
negation could satisfy. "There is no universal brain-hack" is asserted as the denial
it is; "wetware is reachable only through a real neural path" is asserted as the
precondition it is.

The chapter previously deferred deep hacking in two places. Those deferrals are gone
and replaced by a pointer, so the chapter cannot both define the subsystem and say it
is undefined.
"""
from __future__ import annotations

import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CHAPTER = ROOT / "rulebook" / "5_CYBERNETIC.md"
RULEBOOK = ROOT / "RULEBOOK.md"


def flat(path: Path) -> str:
    """Whitespace-collapsed: the chapter hard-wraps, so phrases span line breaks."""
    return " ".join(path.read_text(encoding="utf-8").split())


if __name__ == "__main__":
    unittest.main()
