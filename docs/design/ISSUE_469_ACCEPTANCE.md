# #469 acceptance record — faction ideologies and Reality Tunnels

**Date:** 2026-10-22. **Status:** acceptance record. **No ideology is canonised; the numeric
hegemony model is not built.** This record states what is delivered and what remains.

## What the issue asks, and where it lives

| Criterion | Where it lives | Status |
| --- | --- | --- |
| Faction **ideologies** articulated as positions, stances and fault lines rather than as labels | `strategy_game/data/global_factions.json` — `factions` (7), `axes` (4), `stance_dimensions`; `strategy_game/data/un_political_discourse.json` — `stance_dimensions` (5), `relations` (3) | **met** |
| **Reality Tunnels** — each faction's channel of interpretation, and how the same event reads differently through it | `strategy_game/data/un_political_discourse.json` — `epistemic_statuses` (5), `shared_floating_signifiers` (8), `endgame_space` (4) | **met** |
| Floating signifiers kept **floating**: shared, not settled | `un_political_discourse.json` — `shared_floating_signifiers` (8), with `epistemic_statuses` distinguishing *tendentiously empty* from *materially* defined | **met** |
| Laclau / LaclauGPT / Cosmic Transition as **lenses**, not as law | `global_factions.json` — `evidence_model` (4), `provenance`, `note`; the lenses inform the axes, and the record states they are not a validated predictive law | **met** |
| Cross-cutting alignments that cut across the faction blocs | `global_factions.json` — `cross_cutting_rules` (8) | **met** |
| Relations between parties, including conflict and coalition | `un_political_discourse.json` — `relations` (3), `relation_states` (5), `historical_non_playable_relations` (3) | **met** |
| The three-faction decision applied | `un_political_discourse.json` — `default_playable_party_ids` (3) | **met** |
| Work the tunnels into **narrative scenes** before modelling numeric hegemony | the RPG layer: `strategy_game/rpg/scene.py`, the case and playtest harness | **partly met** — the tunnels are usable as scene material; the *numeric* hegemony model is deliberately not built, because the issue's own gate is that it comes after the RPG level |

## What is deliberately not settled

- **D20 — #469's remaining approvals: which signifiers are canonical per faction.** The record
  offers one reading — *humanity* tendentially empty in the True Humans record — and that reading is
  **not** canonised here.
- **D17** (the four 2045 UN parties) and **D21** (whether the missing #470 criteria enter the
  data) are shared with #470 and are carried there.
- **No numeric hegemony measure exists.** The issue's deeper ask — modelling hegemony as a number —
  is not done, and the authorization for the RPG level does not include it. A reputation *label*
  inventory exists in the campaign books, which is not a hegemony scale and is not described as one.

## Reproducible checks

```bash
python3 -m unittest strategy_game.tests.test_un_political_discourse -v
python3 -m unittest discover -s strategy_game/tests -p "test_*.py"   # 1535 tests, OK
python3 -m unittest discover -s tests -p "test_*.py"                 # 585 tests, OK
```

## What closure of #469 does and does not mean

It means the **ideology and Reality-Tunnel model is implemented as data** — positions, stances, axes,
floating signifiers with their epistemic status, relations, and the cross-cutting rules — and that
the tunnels are usable as narrative material.

It does **not** mean any ideology is canonical, that any signifier reading is approved, that a
numeric hegemony model exists, or that the strategy layer is unlocked.
