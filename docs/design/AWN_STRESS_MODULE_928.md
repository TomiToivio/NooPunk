# AWN Stress, Breakdowns and Hardening — optional CWN overlay (#928)

> **Status: implemented, optional, off by default.** Issue
> [#928](https://github.com/TomiToivio/NooPunk/issues/928). The core ruleset is
> **Cities Without Number** and stays the core (`docs/design/FOUNDATIONAL_LOCK_897.md`, `AGENTS.md`
> #848 / #897 override). This module adds one character meter and its consequences; it does not
> replace attributes, checks, saves, combat, damage, System Strain, Alienation or progression.

> **Read this with [`AWN_STRESS_RECONCILIATION_928.md`](AWN_STRESS_RECONCILIATION_928.md).** A second
> implementation of the same rule landed in `godot/core/awn_stress.gd` (#929) minutes after this one
> (#930). Both are on `main`; the duplication and the one rule difference between them (whether
> ontological shock is Stress) are recorded there, and the placement ruling is row **D58** in
> [`AUTHOR_DECISION_QUEUE.md`](AUTHOR_DECISION_QUEUE.md).

## Where it lives

| Artefact | Path | Role |
| --- | --- | --- |
| Rules contract | `data/rules/awn_stress.json` | every value, in original wording; `not_transcribed` records what was left out |
| Rules service | `mods/noopunk/stress.gd` | the arithmetic and the state; no dice, no core imports |
| Tests | `godot/tests/test_noopunk_stress.gd`, `godot/tests/test_noopunk_stress_screen.gd` | registered in `godot/tests/run_tests.gd` |
| Screen | `scenes/stress_screen.tscn` + `godot/ui/stress_screen.gd` | reached from `scenes/main.tscn` → `godot/ui/main_menu.gd` |
| Registry | `data/mods/registry.json` | `awn_stress` listed as an overlay that may not claim the baseline |
| Matrix | `docs/design/CORE_VS_MOD_MATRIX_897.md` §D | the row that says so |

## Source and rights

Kevin Crawford, *Ashes Without Number*, **Deluxe edition, 2025-11-06**, printed **pp. 56–58** (Stress;
Breakdowns, Stress and Hardening, Psychic Scars; Addiction and Recovery). The author supplied the PDF;
it is **not** in the repository.

AWN has **no verified open licence** — see `docs/licenses/ISSUE_569_WITHOUT_NUMBER_RIGHTS.md`. So the
contract is a **re-expression of the procedure in NoöPunk wording with the numeric values preserved**:
no source sentence, no table heading or column label, no example character, no page image. Mechanically
identical numbers are the rule; the publisher's expression is not reproduced. The provenance is recorded
in the contract's `source` block and audited with
`tools/audit_without_number_expression.py` (10-word containment against the PDF; see *Verification*).

## The rules, in NoöPunk wording

**Gaining Stress.** A character from a peaceful society carries an emotional limit. When a scene ends,
every character who **took part** in something that violates their moral or cultural expectations gains
Stress. Presence alone is not participation: a character who never attacks may escape the guilt of a
firefight, but one who attacks and misses does not. A table warns a player before an obviously
stress-inducing choice. Stress is applied **at the end of the scene**, not in the heat of it.

| Event | Stress |
| --- | --- |
| Killing another human being | 2 |
| — and it is the first kill | +1d6 |
| — and more than one person dies in the scene | +1 |
| — and the victim was not threatening the character's life | +2 |
| — and the victim was helpless or non-violent | +2 |
| A friend suffers a mortal wound | 1 |
| — and then dies | +2 |
| The character suffers a mortal wound | 2 |
| — and takes a major injury from it | +2 |
| Stealing from someone who is not an enemy | 1 |
| — and they will probably die without it | +1 |
| Witnessing an atrocity or a massacre site | 1 |
| Committing an act of great cruelty | 1–3 |
| Hunger or severe privation | 2 per week |

**The ceiling.** The ceiling is the character's **CWN WIS score**. Equal to WIS is safe; **above** it is
not. When a new dose leaves the total above WIS, the character owes a **Mental save at −2**, made at the
end of the scene. Until the total is back at or below WIS, **each further check is another −2 worse**
(−4, −6, …). A successful save holds the line but **removes no Stress**, so the next one is harder. Back
at or below the ceiling, the escalation resets.

**Breakdowns.** A failed save owes a Breakdown, and the player picks one that fits the Stress. While it
lasts the character gains **no further Stress**, and it ends when Stress is at or below WIS.

| Breakdown | What it does |
| --- | --- |
| Deathwish | cannot willingly retreat; −2 maximum HP per level, floor 1 per level |
| Withdrawal | fights only in self-defence; cannot use skill checks; simple tasks only |
| Indulgence | consumes every food and drug available; fights only to save their own life; −2 to skill checks; cannot refuse an offered indulgence |
| Cowardice | cannot fight; flees or hides from all significant physical peril |
| Confusion | cannot act on their own initiative; needs direction from someone they trust, one scene at a time |

**Hardening — the alternative.** When a Breakdown is owed, the player may **Harden** instead: Stress
drops to **zero**, the character ignores the **first point of Stress in every future scene**, and gains
a **psychic scar**. It stacks — each Hardening adds one more point of resistance and one more scar — and
it is **irreversible**. The scars, with their mechanical effects, are in the contract
(`scars.options[].effects`); they are data, not flavour text.

**Recovery.** A day of safe, familiar comfort (−1); an evening of heavy indulgence (−1, and 1 System
Strain instead of any other recovery); an hour of supportive conversation, once a day, on a
Cha-or-WIS/**Heal**-or-**Lead** check against difficulty 9 (−1, and the *helper* gains 1 Stress on a
failure); accomplishing a major personal or community goal (−1d10, worth at least one adventure). The GM
may allow other means.

**Addiction — a separate, opt-in submodule.** Never enabled by the Stress module and never on by
default. It needs the *Addicted* scar or an explicit table decision; it has daily doses and hours,
privation and no rest recovery on a missed day, 1 Stress that Hardening does not resist, −1 to incoming
Stress and 1d4 Stress removed per indulged day per addiction, a monthly Physical save whose failure
locks a point of System Strain, and a weekly save to get clean with a helper's Heal skill allowed.

## CWN compatibility

- **Reused vocabulary, not a second system:** WIS, the d20 Mental save, 2d6 skill checks, Heal and Lead,
  System Strain, HP per level, CON and CHA scores. The overlay asks for these; it never re-implements
  them.
- **The overlay does not roll.** `mods/noopunk/stress.gd` reports the penalty it wants and takes the
  outcome back in (`resolve_save(tracker, success)`), and the `1d6` / `1d4` / `1d10` inside the subsystem
  arrive from the caller. `tests/test_foundational_lock_897.py` enforces the no-core-coupling half; the
  service's own tests enforce the no-dice half.
- **Adjacency to Alienation, not replacement.** `godot/core/cwn_alienation.gd` already governs
  cyberware-induced psychosis with a Wisdom ceiling and a Mental save. Stress is a **second, separately
  tracked meter with its own ceiling**: a character can be over one and not the other, and neither
  module reads the other's number. Do not merge them.
- **No new save category and no second wound track.** A Breakdown's HP effects are CWN modifiers applied
  by the table; System Strain is the core's resource and is named, never re-derived.
- **State lives beside the core save.** `user://awn_stress_state.json`, versioned by the module
  (`to_dict` / `from_dict`, with a migration hook). The core save's schema is not the module's to
  migrate, and `GameState` / `NooPunkCampaignState` are untouched.

## NoöPunk triggers — separate from the source's list

These are **NoöPunk's own entries**, marked `system: "noopunk"` in the contract, with values authored
for this project and documented with a rationale. They are never presented as the source book's
entries, and they live in a separate id space (`noopunk_events`).

| Trigger | Stress | Rationale |
| --- | --- | --- |
| Learning that the NHI presence is real, and that the institutions knew | 2 (+1 if it is unfolding publicly while the character must work) | the moral weight is withheld knowledge, not metaphysics |
| Being contacted directly by an NHI | 3 (−1 if the character sought the contact) | consent changes the residue; the anomaly itself is Psyche exposure |
| Surviving a rogue AGI incident that killed people | 2 (+2 if the deaths were preventable) | sized against the source's own mortal-wound and atrocity entries |
| Terminating, wiping or abandoning a construct known to be sapient | 2 (+3 if it asked to live) | the setting's analogue of killing a person; the modifier mirrors the helpless-victim rule |
| A PSI or noosphere operation the character ran injured someone | 2 (+2 if the target had not consented) | moral injury from professional practice, not from the anomaly |
| Working a death scene or a disappearance that cannot be resolved | 1 (+1 if the victim was known) | routine investigative work should accumulate, not break an agent |
| Carrying out, or covering for, an order the character believes to be wrong | 1–3 (+1 if concealed from colleagues) | same shape and range as the great-cruelty entry |

**Ontology shock is not Stress.** Ontological shock, noosphere exposure and PSI pressure belong to the
**Psyche overlay** (`mods/noopunk/psyche.gd`, `docs/design/FOUNDATIONAL_LOCK_897.md`). Stress scores what
a character **did or witnessed because of** the anomalous, never the anomaly itself. Folding the two
together would make a worldview crisis and a moral injury the same currency — and would let Hardening
erase the former.

## Consent, register and tone

The module is about moral injury, not diagnosis. Its Breakdowns and psychic scars are **fictional game
consequences**: they are not clinical categories, are not modelled on any diagnosis, and make no claim
about real mental illness. The table agrees to the module before play (session zero: violence, death of
companions, addiction, mental distress), keeps an X-card available, and picks an intensity dial from the
contract: `off` · `stress_only_no_breakdowns` · `full_with_hardening` · `full_with_addiction`.

## Worked scene — Romppainen, the Lakkahaltia cellar

Etsivä Romppainen, **WIS 4**, Stress 0, module on, addiction off.

1. **Scene: the cellar.** A colleague takes a mortal wound and dies (1 + 2). Two gangers die in the
   exchange and Romppainen fired and missed (2 + 1 for more than one). No first kill. Scene total **6**.
   At the end of the scene 6 > 4, so a **Mental save at −2** is owed; the GM rolls it against the CWN
   save target.
2. **The save fails.** The player picks **Withdrawal**. Stress stays at 6 and the character cannot use
   skill checks until it is back at 4 — which is what "he cannot work the case" looks like mechanically.
3. **The next day.** A safe day at home (−1 → 5), then an hour with a colleague who passes the Heal
   check (−1 → 4). At 4 the Breakdown ends and the escalation resets to a first-check −2.
4. **Later, the order.** Romppainen is told to keep a confirmed NHI disclosure from the family of a
   witness. `moral_injury_ordered` (2) + concealed from colleagues (+1) = **3**: not over the ceiling,
   no check, but the next ugly scene will be.

Had the player chosen **Hardening** at step 2 instead: Stress 0, the first point of every later scene
ignored, and one scar — say *Nightmares* (−1 CON modifier, −2 on all saves) — explaining how he lives
with the cellar.

## What this deliberately does not define

- **No values for the source's unprinted cases.** Where the book leaves a number to the table (the
  cruelty range), the contract carries the range and the caller supplies the value.
- **No automatic wiring into combat or the core sheet.** Awarding Stress is a table act: the core does
  not know this module exists, which is the point of an overlay.
- **No PC-facing psychological automation.** The screen is a ledger for the table, not a mood engine.
- **No second addiction economy.** Drugs, their prices and their effects are CWN's
  (`cwn_drugs.gd`); the submodule only adds the dependency state.
- **No claim that AWN's Stress is NoöPunk's core.** #897's four homebrew classes are the limit; this
  module is an optional import, and the registry says so.

## Verification

```sh
godot --headless --path . --script res://godot/tests/run_tests.gd          # 1804 checks, 0 failed
python3 -m unittest discover -s tests                                       # 1652 tests, OK
python3 tools/audit_without_number_expression.py --source "/path/AshesWithoutNumber_Deluxe_061125.pdf"
```

The audit is an operator tool, not a CI gate: the book stays on the operator's disk. It reports the
number of 10-word runs shared with a licence-blocked source, our file and line, and never prints the
matched text.
