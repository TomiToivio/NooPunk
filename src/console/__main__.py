"""``python -m console`` — the reference adapter (§4 of docs/DESIGN_PRINCIPLES.md)."""
from __future__ import annotations

from .play import main

if __name__ == "__main__":
    raise SystemExit(main())
