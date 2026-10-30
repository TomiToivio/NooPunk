# Decision #848 — restored vanilla baseline: audit and canonical paths

**Date:** 2026-10-30 · **Status:** decision executed; coverage expansion continues · **Issue:** #848

This note records what was audited, what was chosen, and what was superseded. It exists so the next
agent does not have to re-derive the answer from a dozen contradictory files.

## The audit

Several parallel sessions produced competing foundations. What `main` actually contains:

| Candidate | Path | What it is | Verdict |
| --- | --- | --- | --- |
| **Root game** | `project.godot` → `scenes/main.tscn` | the CWN/SWN top-down RPG: 28 rule modules in `godot/core/`, 760 headless checks, a working title screen and the Lakkahaltia case | **canonical** |
| Godot rules | `godot/core/*.gd`, `src/godot/` | CWN kernels (`rules_adapter`, `cwn_catalogue`, `combat`, `cwn_combat_rules`, `cwn_hacking`, `cwn_strain`, `cwn_healing`, `cwn_injury`, `cwn_character`, `cwn_party`, psionics) | **canonical**, with `src/godot/` as compatibility only |
| Rulebook | `RULEBOOK.md` (root) | the full authored rulebook, with `rulebook/` chapters generated from it | **canonical**, restored from `archive/` |
| Restart tree | `noopunk/` | blank rulebook + minimal movement game from #827/#835, including the seven-attribute sheet | **superseded**, preserved |
| Legacy/archive | `archive/`, `legacy/`, `docs/` | earlier material, still readable | reference only |

**Baseline commit:** `36092a5` — the state in which
`godot --headless --path . --script res://godot/tests/run_tests.gd` reports **760 checks, 0 failed**.
A commit SHA is pinned rather than "the tip of main" so that a later regression is attributable.

## The decision

Vanilla **CWN** primary, vanilla **SWN Revised** for psionics/space/factions, one top-down Godot game.
No seven-attribute design, no alternate difficulty ladder, no custom mechanics.

### Canonical paths

```
RULEBOOK.md                    the rules, authored
rulebook/                      generated chapters (python tools/split_rulebook_twelve.py --apply)
project.godot                  the game
scenes/main.tscn               startup scene
godot/core/                    rule kernels
data/rules/                    rule data (wn_core.json is the contract)
godot/tests/run_tests.gd       engine tests
docs/rules/CWN_GODOT_COVERAGE.md   coverage matrix
```

## What changed in this pass

1. **`RULEBOOK.md` restored to the repository root** from `archive/`, where the restart had moved it.
   The generated chapters in `rulebook/` are produced from it and were never the source.
2. **`AGENTS.md` opens with the CURRENT DIRECTIVE**: pinned SHA, canonical paths, vanilla-CWN/SWN
   statement, the superseded list, and an instruction not to re-litigate the decision in code.
3. **`START_HERE.md` rewritten** to describe the canonical game instead of the restart.
4. **`noopunk/` marked superseded** in its README, preserved in place.

## Triage of work produced under the superseded direction

| Work | Fate |
| --- | --- |
| `noopunk/` runtime (movement, character sheet, seven attributes) | preserved as history; **not** wired into the game |
| Seven-attribute modules (`cwn_tags.gd`, `noopunk_tags.gd`, `noopunk/game/attributes.gd`) | preserved; not used by the canonical game |
| Blank `noopunk/rulebook/RULEBOOK.md` | preserved; the canonical rulebook is `RULEBOOK.md` |
| #821 tag model, #835 character sheet | superseded by this decision; their commits remain in history |
| Restart-era AGENTS/START_HERE sections | replaced by the directive above |

Nothing was deleted. Restoring the vanilla baseline means *not using* the restart tree, not erasing it.

## Coverage status — honest

Verified by the 760-check suite at the baseline: attributes and modifiers, skill checks, saves,
attack resolution, Shock and trauma, System Strain, major injuries, healing, encumbrance, hacking
kernel, drone/vehicle rules, party and campaign state, combat rounds and effects.

Known gaps and open questions, unchanged by this decision:

- **Progression** is implemented but not exercised end-to-end by a character-advancement test.
- **Cyberware installation/removal and Alienation** are contract-level only.
- **SWN psionics** follow the revised class/discipline rules, but no legal Psychic test character
  exists yet.
- **Coverage matrix** lists subsystems and modules; it does not yet prove every published table.
- **Desktop playtest** is not done: headless suites prove behaviour, not legibility.

Do not claim the rule system is complete. The matrix plus the tests are the evidence, and they are
partial by design at this stage.

## Handoff block

**Baseline commit SHA:** `36092a5`
**Canonical rulebook:** `RULEBOOK.md`
**Canonical Godot project:** `project.godot`
**Canonical startup scene:** `scenes/main.tscn`
**Verification:** `godot --headless --path . --script res://godot/tests/run_tests.gd` → 760 checks, 0 failed
