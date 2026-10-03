"""Eclipse Phase 2E homebrew prototype layer for NoöPunk.

This package is isolated from the native NoöPunk rules so Concordia can prototype
a playable RPG loop with EP2-derived mechanics. Eclipse Phase is created by
Posthuman Studios. See docs/licenses/ECLIPSE_PHASE_HOMEBREW.md.
"""

from .core import EP2Character, EP2PoolState, EP2TestResult, PoolKind, PoolSpend, resolve_test

__all__ = ["EP2Character", "EP2PoolState", "EP2TestResult", "PoolKind", "PoolSpend", "resolve_test"]
