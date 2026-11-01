# The Rules Constitution (#1006)

**Status: permanent author decision, 2026-11-01. This file is the authority; the tier table beside it
is generated.** `docs/rules/RULES_BASIS_LOCK.md`, `RULES_FOUNDATION_POLICY.md` and
`docs/design/FOUNDATIONAL_LOCK_897.md` remain as the history of how the decision was reached — they are
not a second opinion, and where they differ from this file, this file wins.

**The decision in one sentence:** *NoöPunk runs on vanilla Cities Without Number with Stars Without
Number psionics as its essential companion; every other source module is optional and opt-in, and
everything NoöPunk adds is an overlay that sits on top of that base.*

## 1. Authority order

| # | Tier | What it is | Rule |
| --- | --- | --- | --- |
| 1 | `cwn-core` | **Cities Without Number, as written** — attributes, creation, skills, checks, saves, combat, injuries, System Strain, equipment, cyberware, hacking, advancement | The baseline. Nothing overrides it. |
| 2 | `swn-companion` | **Stars Without Number**, imported whole-procedure — psionics first and essentially, the rest when a gap needs filling | Its own module, never blended into CWN skills or combat |
| 3 | `optional-source` | **Worlds Without Number** and **Ashes Without Number**, when CWN genuinely has no equivalent | Opt-in, one procedure, documented in the module's own docstring |
| 4 | `noopunk-mod` | **Original NoöPunk overlays** — Noösphere, ontological shock, GUMSHOE investigation, narrative layer, ideology and factions, reputation and relationships | Reads core state, adds narrative state, **never computes core resolution** |

Three tiers exist beside these and are not playable material: `infrastructure` (boundary and
vocabularies), `experimental` (prototypes that are explicitly not canonical), `legacy` (retired code
kept so old imports do not break).

**Precedence.** CWN governs. Where sources disagree, `cwn-core` wins; an `optional-source` module may
override only inside the procedure it owns and must say so; a `noopunk-mod` may never change a CWN
target number, die, band or progression cost. If a mod appears to need that, the mod is wrong.

## 2. What "vanilla is still playable" means, and how it is proved

**Vanilla NoöPunk = `cwn-core` + `swn-companion`.** Turning every overlay off must leave a functional
faithful CWN game: create a character, resolve a check, a save, an attack and a wound, keep System
Strain, advance.

That sentence is worth nothing as prose, so it is a test:
`tests/test_rules_constitution.py` runs the vanilla slice in a subprocess whose import hook **refuses
every module the constitution classifies as `noopunk-mod`**. If the baseline ever grows a dependency on
an overlay, the test fails and names the module. A second test proves the hook actually bites, so the
first cannot pass by importing nothing.

## 3. How the constitution is kept true

* `data/rules/rules_constitution.json` — every module under `src/rules/` classified **exactly once**.
* `tools/rules_constitution_audit.py --check` — fails when a module is unclassified, duplicated,
  phantom, or when a `cwn-core` module imports a `noopunk-mod` one.
* `docs/rules/RULES_CONSTITUTION_TIERS.md` — generated from that registry; never edited by hand.
* `tests/test_rules_constitution.py` — the audit plus the vanilla-with-overlays-blocked proof.

```
modules: 68
  cwn-core        25      swn-companion    9      optional-source  2
  noopunk-mod     20      infrastructure   4      experimental     5      legacy 3
OK: every module has exactly one tier, and no baseline module imports an overlay
```

**A new rules module must be classified in the same commit.** That is the whole maintenance cost of
this constitution, and it is deliberate: an unclassified module is a rule nobody has agreed to.

## 4. What this constitution does not do

* It does not decide **which optional modules are switched on** for a given campaign — that is content,
  not the constitution.
* It does not re-open the attributes, the skill list, the dice, or the progression. Those are settled
  and the author has asked for the cycle to end.
* It does not license quoting source text. CWN and WWN SRDs are CC0 in this repository's ledger; SWN and
  AWN are **not verified open**, so their mechanics are re-expressed and their text never copied
  (`data/sources/game_system_rights.json`).
* It does not apply to the Godot tree's own adapter: that reads the same `data/rules/` contracts and is
  maintenance-only under #950.

## 5. The two questions this leaves with the author

* **D68 — may a NoöPunk mod add a new *skill*?** Empathy/Awareness as additional mod skills (never as
  replacements for `Notice`, `Know` or `Work`) is the one place where "overlay, not edit" is genuinely
  arguable.
* **D69 — which optional-source modules are in the shipped game?** `wwn_projects` and `awn_survival`
  exist and pass their tests; whether the base game includes them, or they stay opt-in modules, is a
  content decision.

Both are queued in `docs/design/AUTHOR_DECISION_QUEUE.md`.
