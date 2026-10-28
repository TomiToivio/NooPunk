# #716 — attribute reskin: decision brief (A / B / C)

**Status:** the decision is the author's. This brief exists so it can be made in one reading, with the
migration surface visible. Nothing here changes canon, and no migration starts until the decision is
recorded.

The investigation layer does not depend on this. `src/rules/investigation.py` reads competencies by name;
whatever the six attributes are called, the layer works. That is why this issue is separate.

---

## The three candidates

**A — keep STR / DEX / CON / INT / WIS / CHA.** Presentation only: NoöPunk-flavoured descriptions and
examples. Nothing to migrate; every CWN citation stays checkable.

**B — aliases, canonical codes unchanged.** Sheets read Body Power / Coordination / Resilience / Reason /
Awareness / Presence, while `data/rules/*.json`, saves and rules references keep `STR…CHA`. A labelling
pass; the real risk is a half-renamed tree.

**C — a new set** (FIT/REF/INT/SOC/PSY/CYB, or the 2-physical/4-mental and 3/4 variants in
`ISSUE_712_LAYERS_AND_ATTRIBUTES.md`). A mechanical replacement, not a relabel.

## Why C is expensive *in this repository specifically*

The contract is machine-readable, so a rename is a data migration with a validation surface:

- `data/rules/without_number.json` — `attributes.names` (six codes), `saves.attributes`
  (Physical: STR+CON; Evasion: DEX+INT; Mental: WIS+CHA; Luck: none), `modifier_upper_bounds`.
- `src/rules/wn_core.py` — builds modifiers and save targets from those codes.
- `src/rules/cwn_core.py` — saves, Trauma/Shock and Strain capacity read CON.
- `src/rules/investigation.py`, `case_graph.json` — competencies, not attributes: unaffected either way.
- `tests/test_scenario_data.gd` — asserts every scenario check's attribute is in the baseline list, so a
  new code fails CI until the list changes.
- Case and NPC stat lines, character generation, advancement, gear, and every existing save.

Two sub-questions this issue raises can already be answered from canon:

- **CYB — no.** The baseline says cyberware is *equipment*, not a CYB score, and System Strain already
  prices the body's cost. A CYB attribute would double-count it and penalise unaugmented characters by
  definition.
- **PSY — no.** PSI is a trained capability (`swn_psychic` package with Effort), not an attribute.
  Ordinary mental stability is the mental save plus conditions (#698). An attribute called PSY invites
  "roll PSY to sense the anomaly", which breaks the anomaly gate.

## The cost table

| | data files | code | tests | sheets/saves | canon citations |
|---|---|---|---|---|---|
| **A** | none | none | none | none | intact |
| **B** | none if aliases live in presentation only | none | a lint that codes and labels cannot disagree | sheets only | degraded in print unless both are shown |
| **C** | all `data/rules/*.json` | `wn_core`, `cwn_core`, generation, NPCs | scenario attribute guard, every stat test | rebuilt, not converted | lost |

## Recommendation

**A now. B if a session shows the vocabulary obstructs play. C only as its own design issue.**

Reasoning: the corpus is mid-port, and A keeps every CWN citation checkable at the exact moment that
matters. B is available later and is genuinely reversible — codes never move. C is a different game, and
the honest way to get it is to argue it as such, with the save pairings, point buy, NPC generation and
legacy-character rebuild rule decided together rather than discovered during a migration.

## The decision

> Attribute model: **A / B / C** (if C: the six codes, the save pairings, and whether old characters are
> **rebuilt from concept** — the baseline's own rule — or converted).

Once written here, the follow-up work is mechanical. Until then, no file changes.
