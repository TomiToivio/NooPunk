# #470 acceptance record — the 2045 global factions

**Date:** 2026-10-22. **Status:** acceptance record. **The faction roster is a model with open
questions, not canon; the strategy level is gated behind the RPG.** This record states what is
delivered and what remains; it approves nothing.

## The roster decision, and what is implemented

The issue's latest author decision (2026-10-15) sets **exactly three playable human political
factions** — True Humans Party, Unity/Security/Stability Party, The Noösphere — with the Libertarian
Accelerationist Party removed from the default playable roster and retained as non-playable
antagonist material, and Orion / Confederacy / Swarm as the three non-playable NHI powers.

| Criterion | Where it lives | Status |
| --- | --- | --- |
| Three playable human factions, named | `strategy_game/data/un_political_discourse.json` — `default_playable_party_ids` (3), `parties` (3) | **met** |
| The removed faction is present as **non-playable** material, not deleted | `data/world/un_parties.yaml` — `libertarian_accelerationist` is still a row (4 parties in the world file); `un_political_discourse.json` — `non_playable_historical_parties` | **met** |
| Three non-human powers, non-playable | `strategy_game/data/global_factions.json` — `factions` (7 entries: 3 playable + the non-playable set), `entity_kinds`, `un_parliamentary_parties` | **met** |
| Cross-cutting alignments that cut **across** the blocs, allowing internal conflict, coalitions and splits | `global_factions.json` — `cross_cutting_rules` (8), `stance_dimensions`, `paradigm_shifts` | **met** |
| Wendt / Pasulka / Dolan as **different lenses**, with epistemic caution | `global_factions.json` — `evidence_model`, `epistemic_statuses` (5) in `un_political_discourse.json` | **met** — the sources are separated from the 2045 extrapolations by the epistemic-status vocabulary |
| Source-derived observations kept distinct from fictional extrapolations | `un_political_discourse.json` — `epistemic_statuses` (5); `global_factions.json` — `evidence_model` | **met** |
| Deep contradictions surfaced **inside** the umbrellas | `global_factions.json` — `axes` (4), `stance_dimensions`; `un_political_discourse.json` — `relations` (3), `endgame_space` (4), `shared_floating_signifiers` (8) | **met** |
| Event seeds that make the factions playable rather than described | `global_factions.json` — `event_card_seeds` (11), `paradigm_event_seeds` | **met** |
| The 2026 baseline's missing half and the roster's scope | `docs/design/ISSUE_470_FACTION_DEPTH_AND_THE_2026_GAP.md` | **delivered as a record; the decisions are D18, D21** |

## What is deliberately *not* settled

- **The four-vs-three contradiction is still replicated inside the data.** `un_parties.yaml` carries
  four party rows while the playable set is three. That is the known inconsistency, and reconciling
  it is a *content* decision (D18: complete roster at start, or the starting three) rather than a
  code fix. This record does not resolve it by editing data to make it look consistent.
- **D17 — the four 2045 UN parties**: succession, formal names versus colloquial labels, the
  self-name/hostile-exonym question. Each part is left visibly unresolved in the records rather than
  answered.
- **D19 — the True Humans Party's record**: how the issue's style references (Unabomber, Linkola,
  Yudkowsky) are filed — a §6.1 attribution row, a `references` entry, or both. A packaging and
  attribution decision, not a design one.
- **D21 — whether the missing #470 criteria enter the data** at all.
- **D24 — which 2045 opening snapshot is the default** (see #468).

## Reproducible checks

```bash
python3 -m unittest strategy_game.tests.test_un_political_discourse -v
python3 -m unittest discover -s strategy_game/tests -p "test_*.py"   # 1535 tests, OK
python3 -m unittest discover -s tests -p "test_*.py"                 # 585 tests, OK
```

## What closure of #470 does and does not mean

It means the faction model, its axes, its cross-cutting rules, its event seeds and its
epistemic-status vocabulary are **implemented and verified as data**, with the three-faction
decision applied to the playable set.

It does **not** mean the roster is final, that the four-vs-three contradiction is resolved, that any
party name or succession is settled, or that the strategy layer is unlocked. The author's own
sequencing keeps the Strategy level behind the RPG gate.
