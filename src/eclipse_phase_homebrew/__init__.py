"""Eclipse Phase 2E homebrew prototype layer for NoöPunk.

This package is isolated from the native NoöPunk rules so Concordia can prototype
a playable RPG loop with EP2-derived mechanics. Eclipse Phase is created by
Posthuman Studios. See docs/licenses/ECLIPSE_PHASE_HOMEBREW.md.
"""

from .core import EP2Character, EP2PoolState, EP2TestResult, PoolKind, PoolSpend, resolve_test
from .interactions import (
    EP2HarmState,
    EP2InteractionResult,
    EP2OpposedResult,
    resolve_combat_attack,
    resolve_hack_action,
    resolve_opposed_test,
    resolve_social_action,
)

__all__ = [
    "EP2Character",
    "EP2PoolState",
    "EP2TestResult",
    "PoolKind",
    "PoolSpend",
    "resolve_test",
    "EP2HarmState",
    "EP2InteractionResult",
    "EP2OpposedResult",
    "resolve_combat_attack",
    "resolve_hack_action",
    "resolve_opposed_test",
    "resolve_social_action",
]
