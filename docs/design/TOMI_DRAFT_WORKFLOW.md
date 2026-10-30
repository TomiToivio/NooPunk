# Tomi-draft workflow (meta-issue #814)

**Status:** standing process, not a task. The meta-issue stays open permanently.

Tomi is the designer and authorial source of truth. Agents implement each draft in **two synchronised
forms** — the tabletop rulebook and the Godot RPG — and record every point where the two intentionally
differ.

## The loop

1. **Draft.** Tomi writes one manageable section: a rules change on the CWN/SWN baseline, or a scenario
   section.
2. **Task.** Tomi hands the draft plus an explicit implementation scope. Agents may flag ambiguity or
   trade-offs; agents do **not** substitute their own creative decision for an open question.
3. **Tabletop.** The draft becomes playable, internally consistent rules or scenario text: procedures,
   examples, cross-references, licensing respected, no reproduction of non-open rulebook text.
4. **Godot.** The same intent becomes data, logic, UI or scenes, with automated tests. Test the
   executable behaviour, not the prose (per `AGENTS.md`).

## Scope rules

- **One section or scenario at a time.** No speculative expansion into neighbouring sections.
- Every draft gets its **own child issue**, linked back to #814, with the PR linked as well. History has
  to stay traceable.
- **Never close #814**, including via `Fixes #814` / `Closes #814` in a PR. Only child issues close.
- Where a rule and its scenario disagree with an earlier decision, the **newer authorial draft wins**, and
  the superseded text is archived rather than silently rewritten.

## Definition of done for a child task

- [ ] Tomi's draft and its scope are linked.
- [ ] Tabletop text updated, with references to the CWN/SWN baseline it departs from.
- [ ] Godot implementation updated, where the draft applies to the computer RPG.
- [ ] Examples/tests cover the key decisions, the edge cases and **tabletop–Godot parity**.
- [ ] Unresolved questions, departures from the draft and deliberate platform differences are recorded
      for Tomi's ruling — not quietly resolved.
- [ ] PR merged through the usual workflow; the PR and child issue are linked here.

For a scenario draft, the tabletop deliverable may be a playable scenario rather than a rules chapter;
the Godot deliverable covers the corresponding playable content.

## Where things live

| Deliverable | Location |
|---|---|
| Rules procedures (shared, engine-neutral) | `src/rules/` — the tabletop and Godot source of truth for mechanics |
| Rule data and catalogues | `data/rules/` |
| Tabletop prose | `rulebook/`, `docs/rulebook_segments/`, `RULEBOOK.md` |
| Godot rules layer (canonical) | `godot/core/` — see [`../godot/CANONICAL_GODOT_TREE.md`](../godot/CANONICAL_GODOT_TREE.md) |
| Godot tests | `godot/tests/run_tests.gd` (headless) |
| Scenarios | `godot/scenarios/`, `docs/scenarios/` |

## What "synchronised" has meant in practice

Two examples worth keeping as precedent:

- **Party design (#806/#808).** The rule (one persistent PC, 1–4 members, companions join and leave)
  lives in `src/rules/party.py` with tests; the Godot wiring is the remaining work, and the issue says so
  instead of pretending the rule is playable.
- **Field-agent generation (#809/#811).** CWN's dice and the single swap are pinned by tests so a later
  customisation cannot change them by accident; the NoöPunk part — agency choice — is asserted to change
  **no** attribute, because that is the obvious way a background choice drifts into a hidden stat bonus.

## The one thing agents must not do

Invent a rule to fill a gap in the draft. An unimplemented gap is a question for Tomi; a plausible
invention is a defect that later has to be found. When something is undecided, the code says so and the
issue records it as pending.
