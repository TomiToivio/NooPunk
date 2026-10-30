# CWN SRD parity audit (#858)

**Measured:** 2026-10-30 against `origin/main` (`67539a2` era). **This is an audit, not a certificate.**
`docs/CWN_COVERAGE_MATRIX.md` was the starting point; this file answers the harder question the issue
asks: for each published section, is there **code**, a **tested procedure**, a **playable interface**, and
**verified agreement with the SRD text**?

Four columns, four different claims. A file existing proves only the first.

## How this was measured

```bash
ls godot/core/*.gd | wc -l          # 31
ls godot/tests/test_*.gd | wc -l    # 28
ls src/rules/cwn_*.py | wc -l       # 21
godot --headless --path . --script res://godot/tests/run_tests.gd   # 791 checks, 0 failed
```

Section list taken from the SRD itself (1.1.0 → 4.5.0 present in the source text; 5.x antagonists and
6.x magic are **not on the linked site** and are out of scope below).

## Reconciliation after PR #865

PR #865 (`890d4168bf581e1a92f3086db7b0794c4aa285b7`) merged new Godot kernels for chases, cyberware operations, mission time, attack modifiers, and gear modifications. The original audit measurements and historical 791-check count below remain a snapshot, **not current verification**. This reconciliation updates only the affected evidence rows. No local test suite or windowed playtest was run for this documentation change. The source-parity and playable columns remain conservative.

## Contacts integration (#869, PR #872)

The Contacts rules kernel now models acquaintance/friend favors, starting contact choices, limits on risky or expensive favors, one call per session, no mission participation, and trust changes. Its behavior has regression checks in `godot/tests/test_cwn_vanilla.gd`. It is not yet exposed as an end-to-end playable interface; full §1.4 source parity remains unverified.

## Status of each published section

| § | Section | Code | Tested | Playable | SRD parity |
|---|---|---|---|---|---|
| 1.1 | Attributes | yes — `cwn_character.gd`, `catalogue` | yes — `test_cwn_engine.gd` | yes — `campaign.tscn` sheet | **unverified** |
| 1.2 | Skills | yes — `cwn_catalogue.gd`, `data/rules/cwn/skills.json` | yes — `test_cwn_catalogue.gd` | partial | **unverified** |
| 1.3 | Backgrounds | yes — `cwn_character.gd` | yes | partial | **unverified** |
| 1.4 | Contacts | yes — `cwn_contacts.gd` rules kernel | yes — `test_cwn_vanilla.gd` | no complete player interface | **unverified** |
| 1.5 | Edges | yes — 13 files reference Edges | partial | partial | **unverified** |
| 1.6 | Foci | partial — 4 files | partial | no | **absent** |
| 1.7 | Final creation steps | yes — `field_agent.gd`, `cwn_character.gd` | yes | yes | **unverified** |
| 2.1 | Scenes, rounds, mission time | yes — `cwn_mission_time.gd`, `combat.gd`, `session.gd` | yes — mission-time kernel tests reported in PR #865 | partial — dedicated mission-clock UI not independently demonstrated | **unverified** |
| 2.2 | Saving throws | yes — `dice.gd`, `cwn_combat_rules.gd` | yes | yes | **unverified** |
| 2.3 | Skill checks | yes — `dice.gd`, `rules_adapter.gd` | yes | yes | **unverified** |
| 2.4 | Combat | yes — `combat.gd`, `cwn_combat_actions.gd`, `cwn_combat_rules.gd` | yes — `test_combat.gd` | yes | **unverified** |
| 2.5 | Injury, healing, strain | yes — `cwn_injury.gd`, `cwn_healing.gd`, `cwn_strain.gd` | yes — `test_cwn_injury.gd` | partial | **unverified** |
| 2.6 | Chases and pursuit | yes — `cwn_chases.gd` (foot and vehicle) | yes — deterministic checks reported in PR #865 | no dedicated chase interface demonstrated | **unverified** |
| 2.7 | Advancement | yes — `cwn_progression.gd`, `swn_progression.gd` | yes | partial | **unverified** |
| 2.8 | Crafting and modifying gear | yes — `cwn_gear_mods.gd`, `data/rules/cwn_gear_mods.json` | yes — deterministic checks reported in PR #865 | no dedicated crafting interface demonstrated | **unverified** |
| 2.9 | Encumbrance | yes — `cwn_encumbrance.gd` | yes | partial | **unverified** |
| 3.1 | Mission gear | data only — `srd_tables.json` | no | no | **unverified** |
| 3.2 | Lifestyles, wages, bribes | data only | no | no | **absent** |
| 3.3 | Armor | yes — catalogue + soak | yes — `test_cwn_catalogue.gd` | partial | **unverified** |
| 3.4 | Weapons | yes — catalogue | yes | yes | **unverified** |
| 3.5 | Pharmaceuticals and street drugs | thin — 2 files | no | no | **absent** |
| 3.6 | Cyberware | yes — `cwn_cyberware_ops.gd` (installation, removal, Alienation) plus catalogue | partial — operational tests reported in PR #865; d12 complication table still missing | partial | **unverified** |
| 3.7 | Cyberdecks | yes — `hacking.gd`, `cwn_hacking.gd` | yes — `test_hacking.gd` | partial | **unverified** |
| 3.8 | Drones | partial — 10 files reference drones | partial | no | **absent** |
| 3.9 | Vehicles | yes — `cwn_vehicles.gd`, `cwn_srd_vehicles.gd` | yes — `test_cwn_srd_vehicles.gd` | no | **unverified** |
| 4.1 | Cyberspace basics | yes — `hacking.gd` | yes | partial | **unverified** |
| 4.2 | Hacking mechanics | yes — `hacking.gd` (Access, security, alert clock) | yes | partial | **unverified** |
| 4.3 | Programs | yes — `cwn_programs.gd`, `cwn_program_rules.gd`, **`cwn_hacking_catalogue.gd`** | yes — `test_cwn_hacking_catalogue.gd` | no | **verified for the 24 Verbs and 12 Subjects** (verbatim transcription, cited) |
| 4.4 | Demons and watchdogs | partial — demons referenced in hacking | partial | no | **absent** |
| 4.5 | Servers and architecture | partial — node linking in `hacking.gd` | yes | **no — no node-link screen** | **absent** |

## What the table says plainly

- **One section is verified against the text**: §4.3, and only its catalogue half — 24 Verbs, 12 Subjects,
  transcribed verbatim with the SRD cited. Everything else is code that *may* be right.
- **Seven sections remain structurally absent or data-only / without playable implementation**:
  contacts (1.4), Foci (1.6), lifestyle costs (3.2), drugs (3.5), drones as a played system (3.8),
  demons/watchdogs (4.4), and the node-link screen (4.5). PR #865 adds kernels for chases (2.6),
  crafting (2.8), and cyberware Alienation (3.6), but does **not** establish end-to-end playability or SRD parity.
- **"Playable" is the weakest column.** Most rules exist as procedures with tests and are reachable from
  the session/campaign scenes only indirectly. A rule a player cannot invoke is not parity.

## Out of scope, itemized (not silently dropped)

| Item | Why |
|---|---|
| §5.1–5.6 antagonists, reaction rolls, morale, NPC blocks | not published on the linked site (the site manager states they were left out) |
| §6.1–6.4 magic, summoning, the Graced, magical items | optional rules, absent from the linked site; the base game is cyberpunk |
| SWN psionics | present (`psionics.gd`, `psychic_effort.gd`, `swn_progression.gd`) but governed by SWN Revised, deliberately **not** counted as CWN parity |

## The next honest increments, in order

1. **§4.5 node-link screen** — the hacking subsystem is the only one with a verified catalogue and no way
   to play it. Wiring the screen converts three sections (4.2, 4.3, 4.5) from partial to playable.
2. **§3.6 cyberware** — Alienation arithmetic now has a kernel (PR #865); finish the d12 implant-complication table, playable integration, and SRD verification.
3. **§1.4 contacts and §1.6 Foci** — character creation is where the other ten rows' assumptions are set.
4. **§2.6 chases and §2.8 crafting** — now have kernels, but still need playable integration and source-by-source verification. **§3.2 lifestyles and §3.5 drugs** remain missing.
5. **Parity verification pass** — take each "unverified" row and compare procedure against the SRD text,
   one at a time, recording the exact section and the test that proves it.

No row may move from **unverified** to **verified** without a citation to the SRD section and a test that
fails when the rule is changed.
