# Issue #1042 — LaclauGPT as a CWN character-level mod

Phase 1 of the issue, shipped as one deterministic module. Phase 2 (SWN faction play) and Phase 3
(aggregation, brokerage, autonomous agents) stay deferred, as the issue itself orders.

## What exists now

`src/rules/laclau_gpt_social.py`, tested by `tests/test_laclau_gpt_social.py` (21 cases).

| Issue requirement | Where it lives |
| --- | --- |
| Three layers that never collapse | `DiscourseProfile` (DA), `Stance` (DNA), `Tie` + `GameRelation` (SNA) are different types with no derivation path between them |
| Ideology with identities, values, demands, signifiers, antagonisms, goals | `DiscourseProfile`, goals typed by `GoalKind` (personal / institutional / ideological) |
| Actor–concept statements with polarity, date, source | `Stance`, stamped `evidence` / `fiction` / `outcome` |
| Agreement and conflict without friend/enemy conversion | `SocialWorld.compatibility()` returns counts and a score, writes nothing |
| Communication/affiliation graph separate from trust, access, reputation | `Tie` records what was observed; `GameRelation` is set only by `adjust_relation`, i.e. by play |
| Knowledge limits and fog of war | `decision_context()` returns only what is registered for that actor; absent stance is `None` |
| Traceability and persistence | append-only profile versions, dated stances, an event log per write, JSON snapshot with a schema version |
| Uncertainty and absent evidence | `Polarity.UNCERTAIN` is counted apart; no shared statement yields `score=None`, not `0` |

Two acceptance criteria are pinned as tests by name, because they are the whole design:

- `test_agreement_with_a_stranger_stays_agreement` — identical stances, no tie, no relation.
- `test_disagreement_with_a_trusted_colleague_stays_disagreement` — `score=-1.0` while trust stays 3.

## Mapping back to the LaclauGPT pipelines

The issue asks to adapt, not duplicate, the analysis steps. The correspondence is structural:

| LaclauGPT step | Mod equivalent | Deliberate difference |
| --- | --- | --- |
| step 6 — discourse analysis (`step_6_roihu_discourse_analysis.py`) | `DiscourseProfile` per actor | the analysis is authored once per profile version instead of recomputed per corpus |
| step 7 — discourse network analysis | `Stance` + `compatibility()` | only *meaningful events* ingest statements — a stance is an authored record, not an inference over every line |
| step 8 — social network analysis | `Tie` + `GameRelation` | the empirical edge and the game relation are separate tables; centrality is not control and a call is not trust |
| versioned schemas, stable IDs, provenance | `SCHEMA_VERSION`, `actor`/`concept` ids, `Provenance` | the game adds an `outcome` kind the research pipelines do not have |

Interpretation is bounded the same way the research pipeline bounds it: a statement is an observation
about what an actor *said*, never proof that anyone was persuaded.

## Deliberate non-goals in this increment

- No faction-level DA/DNA aggregation (Phase 2), no brokerage/switcher metrics (Phase 3).
- No LLM in the loop. Nothing here calls a model; authorship of a `Stance` or a `DiscourseProfile`
  happens outside and arrives with its `Provenance` set.
- No new CWN mechanics. The module is a world-state register; it does not touch skills, combat,
  strain or advancement.
- No in-game command yet. The engine hook (`decision_context`) is the interface a command or an NPC
  dialogue step would call; wiring it into `mud/nopunk_mud/campaign/engine.py` is the next small
  increment and needs an authored Helsinki scene to be worth its code.

## Next increments, in order

1. **Command surface**: `stance <actor> <concept>`, `network`, `dossier <actor>` in the solo campaign,
   gated by what the player character has actually learned.
2. **Event ingestion**: meaningful CWN events (a negotiation, a manifesto, an arrest) write `Stance`
   and `Tie` rows through one audited entry point.
3. **NPC reaction rule**: one deterministic table that consumes `decision_context()` and returns a
   disposition, so ideology and trust stay separate inputs rather than one blended score.
4. **Authored scene** for the acceptance criterion of a playable UNSA Helsinki investigation;
   the fiction is the author's, not the agent's.

## Why the module is not exported from `src/rules/__init__.py` yet

The package's `__init__` is the compatibility surface other modules import from; a module joins it when
it is consumed by engine code, not when it is first written. It joins in increment 1, together with
the command that uses it.
