"""Issue #225 — the cross-domain state machine and the shared action economy.

The issue asks for five things; this pins each. Two halves, because the contract has
two halves: the **chapter** states the rules a table reads, and the **module** executes
the invariants that prose cannot enforce.

House discipline: every content assertion is a POSITIVE, clause-scoped claim, never a
bare noun a negation could satisfy. "No realm reaches another without a declared
gateway" is asserted as the denial-plus-condition it is.

Cross-links: #200 (epic), #217 (resolution semantics), #222 (cyberspace procedure).
"""
from __future__ import annotations

import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

from src.rules import cross_domain_state as cds
