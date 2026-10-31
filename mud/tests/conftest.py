"""Make the MUD tests runnable from either directory.

The MUD suite is normally run from `mud/` (`python -m pytest tests`), where `nopunk_mud` is importable. Some
tests — the repository-level parity checks and the phase-1 acceptance arc — import through the repository
package path (`mud.nopunk_mud…`) because that is where they were written. Both are legitimate; the test
runner should not have to care.

This inserts the MUD directory and the repository root, and does nothing else.
"""
from __future__ import annotations

import sys
from pathlib import Path

MUD = Path(__file__).resolve().parents[1]
ROOT = MUD.parent

for path in (str(MUD), str(ROOT)):
    if path not in sys.path:
        sys.path.insert(0, path)
