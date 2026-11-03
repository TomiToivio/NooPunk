# CWN immutable core and dual-implementation audit (#1068)

**Decision:** Cities Without Number is the **immutable** NoöPunk OSR foundation. NoöPunk development **never modifies or rebalances CWN**. Every new mechanic belongs to an explicitly named, opt-in, separately tested Mod that is either **compatible with CWN** or **simpler than CWN**. A tag system inspired by Otherscape or Neon City Overdrive can add descriptions/fictional positioning, but must not replace baseline CWN resolution or silently alter its probabilities, saves, combat or advancement. SWN/WWN/AWN are named supplements, not permission to change CWN.

## Source baseline

- Hosted SRD: https://cwn.quadrifons.com/
- Free rulebook: https://tesera.ru/images/items/2301450/CWN_Free_Version_081123.pdf

The free rulebook and hosted SRD are **not interchangeable evidence**: page coverage, missing SRD chapters, edition discrepancies and optional/deluxe content must be identified rather than assumed. Respect copyright and existing license guidance in `docs/licenses/`.

## Existing evidence and limitations

- `data/rules/cwn_fe_toc.json` inventories headings and Free Edition PDF page numbers; headings are **not** proof of implemented mechanics.
- `docs/rules/CWN_PARITY_MATRIX.md` and `tools/cwn_parity_audit.py` track 66 SRD navigation sections with heuristic file/test evidence; **implemented** in that matrix does **not** mean source-verified. See the generator's status definitions.
- The current coverage report is `docs/rules/CWN_COVERAGE_1068.md`, generated from `data/rules/cwn_traceability.json` and `data/rules/cwn_compliance_matrix.json` by `tools/cwn_parity_audit.py`. `docs/rules/CWN_COMPLIANCE_MATRIX_950.md` was a second rendering of the same JSON and has been retired; `docs/CWN_COVERAGE_MATRIX.md` and `docs/mud/CWN_COMPLIANCE_MATRIX.md` are historical inventories with different scopes and dates. Do **not** aggregate their percentages or treat the earlier MUD gap list as an up-to-date exhaustive diagnosis, and do not create another coverage report.
- `docs/RULES_PARITY_1053.md` records save-target adapter contract disagreements among Python and MUD entry points. This remains a **source-fidelity and shared-library integration blocker**, not an authorized reason to rewrite core CWN.
- `RULEBOOK.md` and `docs/rulebook_segments/` are tabletop documentation. `src/rules/cwn_*.py` is one Python rules surface; `mud/` is an interface/integration surface. Prior Godot copies are not a normative source for future changes.

**Audit status:** repository inventory exists; complete **rule-by-rule source verification, tabletop playability proof, and code-to-document parity are NOT established**. A green structural CI check must never be described as 100% CWN conformance.

## Mandatory traceability record for each source procedure

| Field | Required evidence |
| --- | --- |
| Source | SRD section URL **and/or** Free Edition PDF page and edition |
| Mechanic | Short original-language description, inputs, results, edge cases |
| Python | Canonical `src/rules/` symbol and deterministic conformance tests |
| Tabletop | Exact `RULEBOOK.md`/segment heading and executable pen-and-paper procedure |
| Integration | Evennia/CLI/browser adapter calling the canonical Python rule, or documented gap |
| Status | Verified / partial / missing / source not available, independently **for Python and tabletop** |
| Provenance | Date, reviewer, test command or output; differences vs SRD/PDF explicitly recorded |

Do not mark a row **verified** solely because a filename, keyword, or test exists. If one side is missing, both-sides parity is **not verified**. Any discrepancy must be resolved in an addition or adapter, not by modifying CWN.

## Required completion work

1. Check **every** Free Edition TOC procedure and **every** relevant SRD subprocedure, not only the 66 navigation headings. Resolve duplicates and missing/optional sections with evidence.
2. Verify character generation, background/contact/edges/foci, skills/saves, combat and trauma/shock, injuries/healing/strain, advancement, gear/crafting, cyberware, hacking/programs, drones/vehicles/chases, mission and NPC/GM procedures.
3. Write canonical Python example tests for each procedure and boundary conditions, independently verified from the cited source.
4. Check that the tabletop rulebook gives a self-contained, dice-and-pencil playable procedure for each rule, with attribution rather than copyrighted verbatim copied source text.
5. Convert duplicate interface implementations to delegates to the same Python rule. Preserve input normalization and compare outputs across adapters.
6. Keep core/module changes and their precise rulebook changes in the **same PR**. Add Mod compatibility assertions and clearly separate core and Mod test suites.
7. Produce a reviewed coverage matrix counting **verified Python**, **verified tabletop**, **both verified**, **partial**, **missing**, and **not in referenced free/SRD scope**. Close #1068 **only once all in-scope procedures have evidence and no outstanding unresolved differences**.

## Enforceable development constraints

- The default answer to any proposal to change a CWN core dice rule, threshold, progression cost or other mechanic is **no**.
- An explicit optional Mod is additive and may not shadow or mutate a CWN outcome. Document its compatibility/simplicity and tabletop operation.
- Interface code must not become a second source of mechanical truth.
- `python tools/check_cwn_lock_1068.py` validates essential evidence files. It is deliberately **structural only**. Human source checking and semantic test coverage remain required; do not confuse structural CI with game-rule verification.
