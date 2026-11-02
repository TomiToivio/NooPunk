# Issue #1043 — SWN Psionics and Factions: what is implemented, what is blocked

The issue says *"FACTIONS and PSIONICS NOW"*. This document is the audit that had to come first,
because the repository has a standing licensing position that decides how far "now" can go:

> `data/sources/game_system_rights.json` records **WWN SRD as CC0 (verified)** and **SWN as having no
> verified SRD (`blocked-unverified`)**. `src/rules/wn_core.py` states the rule that follows from it:
> implement what was *verified against a source*, never what merely seemed plausible.

So this increment implements every part of the two chapters that is **procedure** — the parts whose
correctness is a matter of ordering, legality and bookkeeping rather than of a printed table — and
leaves the printed catalogues (asset lists, costs, income formulas) as scenario data with a named gap.
That is not a partial reading of the issue; it is the only reading that does not put unsourced numbers
into the repository.

## Workstream A — Psionics

| Requirement (issue text) | Status | Where |
|---|---|---|
| Audit existing character/resource interfaces | **done** | this table |
| Psychic Effort: capacity, commit, release, recovery | **implemented** | `src/rules/swn_psionics.py` (`Psychic.capacity`, `commit`, `release`, `end_scene`, `rest`) |
| Torching (burning attributes for Effort) and its costs | **implemented** | same module, `Psychic.torch` + `TORCHING_TABLE`, attribute floor |
| Discipline access, partial psychic restrictions | **implemented** | `DISCIPLINES`, `RESTRICTED_PACKAGES`, `can_learn` |
| Technique catalogue with costs and gates | **implemented** | `src/rules/psionics.py` + `data/rules/psionics_techniques.json`, `may_use`, `effort_duration` |
| All six disciplines' technique effects | **reference-only** | the *effects* live in the purchased book; the module cites pages and implements accounting, never ability text |
| CWN-compatible adapter (no class replacement) | **implemented** | the psychic package is an add-on object; CWN skills/saves/advancement untouched |
| NoöPunk setting tag: natural PSI vs BCI/psychotronic | **partly** | distinct mechanical sources exist (`natural_psi.py` vs cyberware in `cwn_cyberware.py`); a single "source" tag on a technique is **not yet** recorded — gap below |
| Eligibility / activation flows in game | **not implemented** | needs the in-game command surface (see follow-ups) |
| Deterministic tests | **implemented** | `tests/test_swn_psionics*.py`, `tests/test_psionics_*.py` |

**Gap to close next (small, well-defined):** add a `source` field to a technique instance —
`natural` / `bci` / `psychotronic` — and test that a BCI-granted technique still spends *the same*
Effort pool (setting tag, not a second mechanic). The issue asks for the tag; it does not ask for a
second rule system.

## Workstream B — Factions

| Requirement (issue text) | Status | Where |
|---|---|---|
| Persistent organisations, credits, assets, one action per turn | **implemented** | `src/rules/swn_faction_turn.py` (`Faction`, `Asset`, `act`, `next_turn`) |
| Action resolution against another faction, relocation | **implemented, scenario-numbered** | `src/rules/swn_faction_operations.py` (`resolve_action`, `relocate_asset`) — every number is a scenario argument |
| Deterministic multi-faction turn engine: order, legality, audit, round close | **implemented in this increment** | `src/rules/swn_faction_engine.py` + `tests/test_swn_faction_engine.py` (18 cases) |
| Faction attributes Force / Cunning / Wealth | **implemented as ratings** | `FactionProfile` validates the 1–8 band; what each rating *buys* stays table data |
| Goals | **implemented** | `Goal` with bounded progress and completion |
| Faction HP / XP, FacCred income formulas, asset catalogues and costs | **blocked-unverified** | no verified SRD; the engine takes `income`, `cost`, `hp` as scenario data and records what it was given |
| Optional / non-blocking for character play | **implemented by construction** | nothing in CWN imports the engine; a campaign without faction turns never constructs it (`test_the_engine_holds_no_cwn_or_character_state`) |
| UNSA Helsinki Field Office as an organisational faction | **seedable, not seeded** | it is a `FactionProfile`; the authored scenario numbers are the author's call, not an agent's |
| Country Director: faction-turn-only control, never deployable | **design only** | see the two rules below; enforcement belongs where characters are chosen, not here |
| Finite named field-agent roster vs. faction-only assets | **design only** | same |
| Mission → faction consequences without bypassing action economy | **partly** | `resolve_action` can apply outcomes; the *link* from a CWN mission is not wired |
| Integration with #1042 through stable ids | **ready, not wired** | both use string ids; `FactionProfile.faction.identifier` equals the actor id space in `laclau_gpt_social` |
| Complete deterministic turns + tests | **implemented for the engine** | 18 tests: order, ties, legality, purchase, income, audit, serialisation |

### The two rules the issue wants enforced, written where they can be enforced

1. **The Country Director acts only during faction turns.** Enforcement point: the character-select
   path for CWN missions. A test can only be honest there — `FactionEngine` has no character concept
   at all, which is why it cannot be the gate.
2. **Field agents are finite; SWAT/scientists/analysts are faction assets.** Enforcement point: the
   mission party builder, reading a roster of named agents plus a faction-asset budget. Adding
   "support units" to a party must go through a mission-support hook that spends faction resources,
   not through the party list.

Both are therefore *documented prohibitions with a named enforcement site*, not silently "done".

## Why the turn engine takes its numbers from the caller

A worked example of the principle, from the tests: `engine.purchase(faction, asset, cost=6)` spends
exactly six and the audit records `credits=4`. The engine never knows what an asset *should* cost,
because that is the catalogue the book owns and this repository may not reproduce. When the author
supplies a validated table, nothing in the engine changes — only the call site does.

## Follow-up issues this implies

1. Psionics: `source` tag per technique (natural / BCI / psychotronic) with a test that the pool is
   shared — small, closes a stated acceptance criterion.
2. Faction catalogues as data: author-verified asset list, costs and income table, loaded like
   `data/rules/psionics_techniques.json`, so the numbers live in one auditable place.
3. Mission → faction link: one audited entry point that spends faction resources for mission support
   and records consequences, plus the roster/party enforcement of Country Director and agents.
4. In-game command surface for psychic powers and faction turns.
