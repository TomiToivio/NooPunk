# #950 — the Evennia MUD is the main NoöPunk game

**Status: author decision, effective 2026-10-31.** This record does not propose; it routes.
It supersedes the *equal-priority two-game* direction of #946 and the *Godot-first implementation*
direction of #897. It keeps, unchanged, the canonical CWN rules lock, the NoöPunk setting, the
scenario and lore work, and every NoöPunk module.

| | Before | After |
| --- | --- | --- |
| Default coding target | Godot RPG (`project.godot`, `godot/`) | **`mud/` (Python / Evennia)** |
| First deliverable | a graphical vertical slice | **a complete single-player UNSA story with zero LLM, Mesa or multiplayer dependencies** |
| Godot | primary game | **maintenance only**; existing work preserved, nothing deleted, no new generic RPG features |
| Multiplayer / Concordia / Lacuna-style agents / Mesa | part of the design | **phase 2**, explicitly out of the critical path |
| Rules | CWN lock (#897) | **unchanged** — CWN is still the only resolution engine |

## 1. What exists today, measured rather than promised

This is the state the pivot lands on. Every claim below was produced by running something, and the
commands are given so a reader can re-run them rather than trust this page.

| Artifact | Where | Evidence |
| --- | --- | --- |
| MUD server | `mud/` — Evennia 6.1.0 game dir, its own `requirements-mud.txt` | `evennia start` brings up portal + server; telnet on `:4000` |
| Playable neighbourhood | `mud/world/helsinki.py` — six rooms, seven exits, one safehouse, authored as data | `len(helsinki.ROOMS)` and a graph-walk test that every room is reachable |
| CWN sheet on a character | `mud/world/cwn.py`, `mud/typeclasses/characters.py` | `sheet` command renders six attributes, modifiers, skills, carried supplies |
| The rules themselves | `<repo>/src/rules` — **shared, not copied** | `mud/tests/test_mud_cwn.py` asserts `world.cwn.skill_check is rules.wn_core.skill_check` (identity, not equality) |
| First faction | `mud/world/factions.py` — UNSA: membership, roles, reputation, four stocks | `faction` command; a give-takes-from-the-carrier test |
| Survival loop | `scavenge` — one CWN Survival check, one consequence | an invariant test: exactly one of "supplies +1" or "room scarcity +1" per attempt, never both and never neither |
| Persistence across restart | `at_pre_puppet` restores `db.prelogout_location` | logged out in the stairwell, `evennia reload`, logged back in in the stairwell |
| Two concurrent humans | Evennia's own two-account fixture **and** a real telnet probe | `mud/tools/probe_two_sessions.py` → two accounts, one room, one sees the other speak |
| Test suite | `mud/tests/` — 22 tests | `evennia test --settings settings.py tests` → **22 tests, OK** |

**What is deliberately absent from this baseline:** LLM GM, LLM NPCs, Concordia, Mesa, other
factions, and any browser client. They are phase 2 and the issue says so.

## 2. The CWN migration, and what it actually found

The compliance matrix is `docs/mud/CWN_COMPLIANCE_MATRIX.md`, generated from
`data/mud/cwn_compliance.json` by `tools/cwn_compliance_audit.py`. It is generated rather than
written so the table cannot drift from what the audit can verify.

**Current audit, 46 rows:** 30 implemented · 7 partial · 6 godot-only · 1 missing · 2 omitted by the
SRD itself.

The finding that matters: **the Python CWN core is already substantial** — twenty `src/rules/cwn_*.py`
modules with twenty-four matching test files, all imported and exercised by the audit's import pass
and by `tests` under CI. The MUD is not starting from zero; it is starting from a rules kernel that
was written for the tabletop and the Godot rules adapter, and which the MUD now calls directly.

The migration work is therefore **the gaps, not a rewrite**:

| Gap | Size | Why it is first |
| --- | --- | --- |
| `focus gear budget` | small | character creation cannot be finished without it |
| `mission time` (scenes/rounds/mission clocks) | small | every MUD scene needs the clock; also the basis of quest timing |
| `wages and bribes` | small | a survival economy needs prices before the first shopping scene |
| `pharmaceuticals` | medium (catalogue + effects) | medical scenes, and the CWN drug tables are already written on the Godot side |
| `cyberware mods and systems` | medium (catalogue) | character concepts depend on it |
| `cyberware alienation` | medium | the clearest whole-subsystem gap: implemented and tested in GDScript, absent in Python |
| `chases and pursuit` | medium | GDScript has the round structure; Python has the vehicles only |
| `skillplugs` | small | **missing everywhere** — no implementation in either game |
| `demon and watchdog catalogues` | small | the hacking opposition model exists; the data does not |

Each is a follow-up issue with tests, in the order the single-player campaign needs them, not the
order the matrix rows appear.

**Coverage of the full book is not claimed.** The linked SRD states that it omits optional rules and
the antagonists/NPC sections; those rows are marked `omitted-by-srd`. Any future claim about an
optional rule must cite the Deluxe PDF as its source *and* respect its licence — the SRD is the open
source, the book is not.

## 3. Two-stage roadmap

**Phase 1 — the solo game (the only phase that is MVP).** A human creates a UNSA character and
completes a coherent investigation campaign and side quests in a text interface with **no other
players, no GM, no LLM, no external API**. Deterministic scripted NPCs and dialogue, quest state
machines, evidence tracking, travel, inventory, combat, hacking, progression, saves, consequences.
Every mechanic resolves through the shared CWN kernel. A headless path must exist for CI.

**Phase 2 — the world, later.** Multiplayer, LLM NPCs/GM, Mesa population simulation, other
factions. Each arrives behind an interface designed in phase 1 but not built: the deterministic
fallback is the product, the model is an enhancement.

## 4. Rulebook parity is compulsory

The tabletop rulebook stays a supported companion product. Every MUD pull request that changes a
mechanic must either update the matching rulebook section and matrix row, or say **"no tabletop
mechanics change"** and why. The matrix is the place where "the engine does X and the book says Y"
becomes visible instead of silent.

## 5. Deferrals, and what is *not* deferred

Deferred: Godot UI/graphics work, mandatory online LLMs, emergent multi-agent simulation, faction
strategy, mandatory multiplayer, and replacing CWN.

Not deferred: the CWN lock, the GUMSHOE investigative overlay, the Noösphere/ontological-shock
overlay (#943), the ideology/reputation layer, the canonical scenario and world data, and the
tabletop rulebook.

## 6. Open decisions this record does not answer

* **D65 — repository shape.** `mud/` in this repository (as landed) or a dedicated repository. The
  issue asks for the decision to be documented before implementation; `mud/` is the reversible
  default and can be extracted with `git subtree split` if the author prefers a split later.
* **D66 — what "maintenance only" means for Godot.** Frozen (no changes at all), bugfix-only, or
  kept buildable but feature-frozen. `godot/tests` and the Godot CI jobs still run today.
* **D67 — how rulebook parity is enforced.** A manual checklist in the PR template, or a
  documentation audit tool that compares matrix rows to `rulebook/` sections.

Queued in `docs/design/AUTHOR_DECISION_QUEUE.md`.
