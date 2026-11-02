# SWN Psionics and Factions now; the rest on demand (#1043)

**Status: scope decision recorded. No rule numbers implemented — and that is deliberate.**

## The decision, restated

Implement **only** *Psionics* (printed p. 29 ff.) and *Factions* (printed p. 211 ff.) from *Stars Without Number:
Revised Edition, Deluxe Edition*. Every other SWN chapter is **low priority / on demand**. CWN stays the
permanent core; SWN is an additive module and never rewrites character creation, skills, combat, advancement,
equipment or any locked rule.

## Why this file contains no mechanics yet

The book is the source, and **the book is not in this repository**. Transcribing Effort costs, discipline
levels, technique lists, FacCred tables or faction action costs from memory would produce a rule set that *looks*
authoritative and is wrong in exactly the places a player would notice — a cost off by one, a technique available
one level early.

So the implementation order is:

1. **Transcribe the tables into data**, from the licensed PDF, with the printed page number recorded per table.
2. **Implement the engine against that data** — Effort accounting, discipline/technique gating, and for factions
   the unmodified Force/Cunning/Wealth turn procedure.
3. **Test the invariants that do not depend on the numbers**: a technique may not be used above the Effort
   available; a discipline may not grant a technique above its level; a faction may not take two actions in one
   turn; a mission may not mint a free faction action.

Those invariants are the part that can be written *now* and still be correct after the tables land.

## Data contract for the psionics module

```
data/rules/swn/psionics.json
  disciplines[]        id, label, page
  techniques[]         id, discipline, level, effort_cost, duration, page
  eligibility          Psychic | Partial Psychic | none, with the delay rule and page
  effort               how the pool is computed, and which attributes feed it (page)

data/rules/swn/factions.json
  attributes           Force, Cunning, Wealth (page)
  ratings[]            attribute -> dice/score mapping (page)
  assets[]             id, attribute, cost, upkeep, hp, attack, notes, page
  actions[]            id, cost, effect, page
  goals[]              id, rewards, page
  turn                 sequencing and the one-action cap (page)
```

A table without a `page` field should fail review: an uncited number is a guess with a version number.

## Boundary with #1042 and #1008

- **#1042** owns ideology, reputation and the character-level social model.
- **#1008 Phase 3** owns the strategic layer and already states the rule this file repeats: **the SWN engine is
  unmodified, and a player mission never purchases a faction action.**
- **This file** owns the two chapters themselves, and nothing else.

## What I will do on instruction

Given the PDF (or a path to it), transcribe both chapters into the two JSON files above, implement the engine,
and pin the invariants with tests. Until then this stays a scope decision, not a half-built subsystem.
