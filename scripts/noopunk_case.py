#!/usr/bin/env python3
"""Play a NoöPunk investigation case in a plain terminal (#1053, #1054).

    python scripts/noopunk_case.py                       # interactive
    python scripts/noopunk_case.py --script walkthrough.txt --seed 7
    python scripts/noopunk_case.py --load case-save.json

The case data is the UNSA/Lakkahaltia graph already in `data/scenarios/`; this script only presents
it. Rules live in `src/rules/investigation.py` and are imported, never re-implemented.
"""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
for candidate in (ROOT, ROOT / "src"):
    if str(candidate) not in sys.path:
        sys.path.insert(0, str(candidate))

from console.play import main  # noqa: E402

if __name__ == "__main__":
    raise SystemExit(main())
