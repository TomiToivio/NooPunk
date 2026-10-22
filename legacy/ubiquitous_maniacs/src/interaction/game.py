"""Reception game: yhdistää tilan, dialogin ja käyttöliittymän."""

from __future__ import annotations

from .state import EnrollmentStatus, ReceptionGame as _ReceptionGame
from .cli import run_reception_scene as _run_reception_scene

ReceptionGame = _ReceptionGame
run_reception_scene = _run_reception_scene

__all__ = ["ReceptionGame", "run_reception_scene", "EnrollmentStatus"]