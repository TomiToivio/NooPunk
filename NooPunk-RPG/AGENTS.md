# Agent rules for NoöPunk RPG

The root [`AGENTS.md`](../AGENTS.md) applies, including the CWN foundational lock (#897) and the rules
constitution (#1006). This file states the RPG boundary in one place.

## CWN is immutable

Do not modify, rebalance, fork, rewrite, rename or replace Cities Without Number mechanics — attributes,
skills, checks, combat, hacking, equipment, progression, psionics or their numbers. `src/rules/cwn_*.py`,
`rulebook/WITHOUT_NUMBER_BASELINE.md` and `data/rules/cwn_*` are the locked surface;
`tools/rules_constitution_audit.py` and `tools/check_cwn_lock_1068.py` run in CI to prove it stayed that way.

**A reorganization is not authorization.** #1295 changes where things live and who owns them; it does not
open CWN to edits. Nor does a stale issue, an unchecked box, or an old design doc.

## Where NoöPunk gameplay is allowed

* The **overlay**: `mods/` (mod activation contract) and tag/graph records — `SocialTag`, `GoalTag`,
  `ClueTag`, `PersonalityTag` — that answer "how does this party stand", "what is it trying to do", "what
  does it know", "what will it do under pressure". A tag is a fact, not a modifier.
* **Campaign-scoped** rules, expressed as data (`data/rules/*.json`, `data/world/*.json`) with their own
  tests, never as a second resolver.
* **Adapters**, when the RPG reads Story Graph or simulator state. The adapter translates; it does not
  redefine either side.

## No second rules engine

One resolver, one console, one campaign model. Run `python3 tools/duplication_audit.py --all` before
writing a module; `docs/DUPLICATION_AUDIT.md` records what has already been merged. If two implementations
exist, decide which is canonical, delete the other and record the decision — never merge both.

## Moving things into `NooPunk-RPG/`

Stage P4, one area per pull request, with a compatibility shim for every public import path and the
path-addressed guards updated in the same commit. `mud/` is a separate environment with its own workflow
and its own dependency install; it moves last, if at all. The measured cost of a move is in
[the migration map](../docs/architecture/PIVOT_1295_MIGRATION_MAP.md).

## Tests

`unittest`, discovered by CI. Rules tests exercise executable code; prose, lore and canon are not tested
(#271). Preserve saves and behaviour when anything moves.
