# Carry-over status: what is done, what is blocked, and by what (#1196)

> **Status: audit, current as of this commit.** #1196 lists six items deferred from #1178, each needing
> its own approved scope. This page records, per item, what exists in code, what is impossible without
> material the repository does not have, and what remains. It exists so nobody re-derives the same
> answer — and so nobody implements a printed rule from memory, which the licence policy forbids.

## Summary

| # | Item | Status | Evidence |
| --- | --- | --- | --- |
| 1 | Astral Graph | **deferred, correctly** | no authored scene needs navigation; `tests/test_world_graphs_1178.py::test_astral_is_not_a_fifth_graph_in_this_slice` |
| 2 | AWN Mutant Edge | **blocked on the edition check**; NPC-only policy enforced | `src/rules/psi_access.py::NPC_ONLY_EDGES` |
| 3 | Mentalist / Spellcaster / Summoner | **selectable**; prerequisites **need an author ruling** | `src/rules/psi_access.py::PC_EDGES` |
| 4 | Device-granted psionic effects | **implemented as policy**; equipment accounting open | `Grant`, `device_grant()`, `selectable=False` enforced |
| 5 | Psychic Training Focus | **blocked on authorised text**; the loophole is closed | `PSYCHIC_TRAINING_FOCUS_AVAILABLE = False`, `focus_disciplines` check |
| 6 | Runtime wiring | **identity layer implemented**; the navigator remains open | `src/world/actor_registry.py`, `tests/test_actor_registry_1196.py` |

## 1. Astral Graph — not built, and that is the answer

#1178 §2 keeps projection **scripted**: OOBEs, NDEs and psychoneural sessions are authored Story
scenes. A graph is a navigation structure; building one before a scene needs to be navigated produces
topology nobody walks. `src/rules/astral.py` remains a prototype; `WorldGraphs` has four families and a
test pins that Astral is not a fifth.

**Reopens when:** an authored scene requires the player to choose a destination in a projected state.
Then: nodes are astral locations, projected agents are occupants, and the scene is the only thing that
instantiates it.

## 2. AWN Mutant Edge — blocked, and the reason is a licence, not a design

The Edge needs its published positive / negative / Pseudo-Psychic / Stigma tables. This repository
does **not** reproduce rulebook tables or prose from memory (`docs/licenses/ISSUE_569_WITHOUT_NUMBER_RIGHTS.md`,
#1043), and the AWN text has not been quoted into the private reference. Transcribing it now would be
exactly the failure the policy exists to prevent.

What *is* settled, and enforced in code:

- **Mutant is NPC-only** — a player character may not select it (`NPC_ONLY_EDGES`).
- **Mutation, ancestry and PSI stay independent facts.** A Mutant is not automatically psychic, and a
  Hybrid is a *possible origin*, not a diagnosis — the withdrawn mandatory Hybrid-only mutation
  packages must not be reintroduced.
- The Edge describes **Mutants**, not people known to be Hybrids.

**Unblocks with:** the edition checked against the physical book and the tables quoted into the private
rules reference, then an NPC template — never a player option.

## 3. Mentalist, Spellcaster, Summoner — allowed, prerequisites unresolved

All three are selectable Edges with their own published mechanics (`PC_EDGES`). Two things stop them
from being *safe* yet, and neither can be settled by writing code:

1. **Prerequisite interaction with the SWN Psychic / Partial Psychic classes.** Nothing may grant an
   unrestricted SWN discipline by accident. Today the guard is negative: `validate_selection()` refuses
   any discipline outside Telepathy/Telekinesis, so an Edge cannot smuggle one in. What is missing is
   the positive statement of each Edge's prerequisites, which is rulebook text.
2. **"No second progress track for the same power."** *Magick is PSI* is fiction, not a conversion
   rule: knowing Telepathy grants no spellcasting. No shared progress track is modelled, which is the
   safe default — but a deliberate check needs the published resource rules to compare against.

**Needs:** an author ruling on whether an Edge may coexist with a Psychic class on the same character,
and if so which track owns Effort.

## 4. Device-granted psionic effects — implemented as policy

A psychotronic device may do something remarkable without widening what the character may choose:

```python
grant = device_grant("Remote viewing", source="psychotronic.implant.mark2")
# Grant.selectable is False, always: __post_init__ refuses True.
```

That is the whole rule: **a grant never becomes a permanent character option, and a device never turns
a prohibited discipline into a free player choice.** Open work is accounting — attaching grants to the
existing equipment records — which needs the equipment schema decision, not a new subsystem.

## 5. SWN Psychic Training Focus — blocked, loophole already closed

The Focus's own level benefits (bonus psychic skill, level-1 technique, Effort +1, the level-2
point-per-level rule, retrospective accrual) are printed rules. `PSYCHIC_TRAINING_FOCUS_AVAILABLE` stays
`False` and the refusal names why. What *is* enforced is the loophole #1178 named: a Focus may not
become a back door to a second discipline — every discipline a Focus would advance must already be one
the character may hold (`validate_selection(focus_disciplines=…)`).

**Unblocks with:** the authorised wording quoted into the private reference, then a parity test — the
same path as every other printed mechanic.

## 6. Runtime wiring — the identity layer, now

The graphs were "a library, not a navigator": console and Evennia did not read them, and identity
between views was conventional — the same string reused everywhere with nothing checking it. That was
the actual gap behind the paper procedure's seventh check ("one actor, one sheet, across all views").

`src/world/actor_registry.py` now makes it explicit:

- a **canonical actor** owns one id, one label, and a set of **per-view handles** (physical, cyber,
  social, story, sheet) that may legitimately differ;
- a handle belongs to exactly **one** actor, and a handle may not be another actor's canonical id;
- an **avatar is a session, not a person**: it must name a known operator, and an avatar id that is
  also a registered actor is refused (#1178 node semantics);
- **one actor, one sheet**: two actors sharing a sheet is reported, not tolerated;
- `check_graphs()` reports every graph occupant and avatar that does not resolve.

It resolves identity **only**. CWN remains the action authority; a test asserts the registry exposes no
roll, modifier or resolution surface and imports nothing from `src/rules`.

**Remaining:** the console and the Evennia client reading `WorldGraphs` through this registry (the
navigator), reproducing the paper procedure — which is now possible, because the mapping it depends on
exists.
