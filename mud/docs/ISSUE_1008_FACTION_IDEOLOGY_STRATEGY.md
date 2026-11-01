# Issue #1008: Faction and ideology roadmap (Evennia)

## Fixed architectural boundaries

- **CWN remains the unmodified character rules baseline**, including its dice, advancement and combat.
- **SWN Revised Factions remains the unmodified strategic faction engine** when Phase 3 is implemented. Do not blend SWN faction attributes with player reputation or faction rank. A player's operational command does not create extra SWN faction actions.
- First playable campaign: young UNSA rookie, rank **0**, gradual cyberpunk-first disclosure. PC-facing details must respect spoiler gating and canonical Finglish conventions. Agents' internal docs use English.
- Phase 1 stores game state in Evennia Attributes via `nopunk_mud.faction_tags`; it has **no autonomous simulation or GM dependence**. Network-scoped reputation is not equivalent to network access.
- Distinguish **institutional rank**, **social reputation**, **faction Force/Cunning/Wealth**, **ideological articulation**, and **actual strategic power**.

## Phase 1: implemented base and explicit integration limits

`mud/nopunk_mud/faction_tags.py`: persistent-state dictionary, default UNSA membership rank 0, promotion validation, command scope permission, per-target scoped reputation (-4..4), initial reactions given an external 2d6 and modifier, goals, privacy visibility, audit trail. `mud/typeclasses/characters.py`: new PCs receive the default state. `mud/commands/default_cmdsets.py`: `faction`/`factions`/`rank`, `reputation`/`rep`, `goals` read the state. Pure-Python tests cover invariants.

This is **an MVP substrate**, not a completed institutional gameplay loop. Rank permissions, promotion rewards and goal changes require authored mission/admin event handlers; no player-facing promotion command is exposed. `promote` returns **pending** XP for the existing CWN progression service rather than generating XP autonomously. There is not yet an NPC dialogue hook to `reaction()`; NPC scripts must choose the one known relevant reputation and call the canonical CWN reaction roll (without double-adding Charisma) before using the addon modifier. Existing save migration is non-destructive: old characters without a tag state are displayed with the default UNSA rank but have not yet been permanently migrated.

**Reputation namespaces:** UNSA, SipuliVerkko, SuomiNet, Internet (dangerous segregated AI network, not freely accessible), MarsNet Hype; also `faction`, `local` and `person` target scopes. Reputation is not Heat, wanted status, trust, objective fame or affiliation. A value of zero is neutral/unknown; `known` controls whether the NPC has heard of it. Select at most one relevant tag for each reaction. Positive/negative trait tags are optional, non-mechanical until deliberately adjudicated.

**UNSA rank ladder:** 0 individual (one agent), 1 partner (two agents), 2 team (four agents), 3 local teams, 4 global teams. Permission additionally needs institutional approval and sufficient personnel; the number never overrides resources or the SWN turn economy. Promotions trigger **proposed** pay/equipment/training/XP packages, which must later be authorized and wired to existing CWN XP rules. No automatic level-up.

### Phase 1 completion gaps before claiming full gameplay integration

1. Wire authorized promotion decisions to campaign quest events, pay/requisition services and existing CWN XP progression, with one-time award tracking.
2. Add canonical NPC reaction-roll integration after verifying CWN Deluxe's specific attribute/reaction instructions; avoid double Charisma and test the large +/-4 effect.
3. Add administrative write controls and object-level knowledge authorization; do not expose owner-only reputation/goal entries to other players.
4. Backfill legacy single-value `db.reputation` and faction saves through a tested migration; do not silently destroy saves.
5. Add headless-to-Evennia integration tests and verify all new player commands with an Evennia harness.

## Phase 2: LaclauGPT Phase 1 methodology as a sane *ideology mod*

Source of truth: [LaclauGPT Phase 1 Paper](https://github.com/TomiToivio/LaclauGPT/blob/main/paper/PHASE_1_PAPER.md). **Its contribution is a conceptual / validation-oriented methodology, not a proven empirical classifier.** Crucial premises: AI is a contested sociotechnical signifier; ideologies are *emergent political articulations*, not fixed static labels; AI can act as a nodal, floating, or tendentially empty signifier (not synonymous); Laclau/Mouffe, Palonen's conditional Formula of Populism and sociotechnical imaginaries provide interpretation. The paper emphasizes source spans, uncertainty, explicit abstention and human review. Convert these into gameplay constraints, not claims of empirical validation.

### Minimal graph schema

- `Actor(id, type, faction_affiliations, visibility)` and `Audience(id, network, reach, access)`.
- `Statement(id, speaker_id, text, event_id, timestamp, audience_id, claimed_position, evidential_span, source_type, certainty, review_status)`. Distinguish quotations, irony, lies and tentative claims.
- `Signifier(id, label, aliases, meanings_by_context, role_candidates)`; **roles are contextual hypotheses**, never automatically assigned because a word is common.
- `Demand(id, issue, proposed_change, beneficiaries)`, `Articulation(statement_id, actor_id, signifier_id, demand_id, relation, valence)`.
- `PoliticalProject(id, chain_of_equivalence, collective_subject_candidate, frontier_candidate, imaginaries, resources)`; populism only when supported by suitable evidence.
- `FactionDiscourse(faction_id, statement_ids, audience_ids, evaluation_timestamp)`, distinct from SWN faction state.
- `Interpretation(id, candidate_code, exact_span, original_source, model_digest, prompt_version, uncertainty, contradictory_evidence, human_review)`.
- Rejected/superseded candidate codes and codebook aliases retained. Never silently promote a proposed LLM label to accepted canon.

### Small deterministic game-loop

1. An authored mission results in a world event (e.g. UNSA discloses a corporate AI cover-up).
2. Factions publish statements to **specific networks**. Source, speaker, time, audience and visibility remain recorded.
3. A bounded interpretation step proposes signifier–demand and actor–concept–stance edges, with evidence and status `proposed`. Can be manually authored without an LLM.
4. Review/validation accepts or rejects candidate edges. Only **accepted** explicit relations can feed deterministic graph summaries.
5. Audience-specific salience and dispute measures are calculated from accepted edges and known reach, *not just raw statement frequency*.
6. Narrative policy maps selected political outcomes to **authored events**: news, rumors, mission options, reputation changes, faction goals. No instantaneous mind-control bonuses or automatic universal ideological alignments.
7. Record immutable input/event/decision/provenance so the state can be reconstructed.

**Prototype metrics, not theory claims:** network-weighted articulation counts, issue salience, stance congruence/conflict, coalition reach, demand support, frontier visibility. Hegemony should not be reduced to one scalar ideology meter. Allow multiple publics, contradictory messages, failed articulations, ideological realignments, and partial ignorance. Keep an operationally tractable subset (3–5 factions, 5–10 signifiers and 2–3 networks) for the first simulation. No LLM in deterministic resolution; models propose text and candidate codings only.

### Relevant tabletop / card design lenses (inspiration only)

- **Twilight Struggle**: event cards and competing influence in places, with historical contingency. *Borrow* event-driven agenda shifts and regional contestation, **not** its binary superpower ideology assumption.
- **COIN series** (e.g. *Andean Abyss*, *Cuba Libre*): asymmetrical factions, distinct victory conditions, event choices and populations. *Borrow* asymmetry and cross-cutting coalitions, not full counterinsurgency complexity.
- **Pax Pamir (Second Edition)**: shifting coalitions/allegiances, patronage and dominance. *Borrow* unstable alliances, not its full tableau rules.
- **Root**: highly asymmetric faction action economies. *Borrow* faction identity and motive-specific powers, not separate subsystems for every small faction.
- **The King's Dilemma**: council votes, hidden agendas and persistent consequences. *Borrow* political decision cards and institutional legitimacy.
- **Netrunner**: hidden information, asymmetric security and evidence discovery. *Borrow* confidential information and bluffing only; no duel-based gameplay core.
- **1960: The Making of the President**: campaign messaging and issue framing. *Borrow* geographically/network-segmented opinion and media narratives without a two-party election simulator.
- **Dune: Imperium** (board/deckbuilder) and **Dune RPG (agent/architect)**: influence, intrigue cards and agent allocation; borrow *action presentation* and council decisions, not deckbuilding/2d20 resolution.

**Design recommendation:** choose an **event-card / agenda-card overlay**, not a collectible card game. A card is a typed, authored event with `prerequisites, public_narrative, secret_truth, audiences, statements, decisions, consequences, cooldown, spoiler_tier`. Card resolution invokes existing CWN checks for PCs and **only later** legal SWN actions for macro strategy. Cards are optional presentation/data packages, not a separate dice engine.

## Phase 3: SWN strategy core + political interface

SWN Revised Deluxe *Factions* (printed pp. 211 onward): map canonical **Force, Cunning, Wealth, HP, FacCreds, assets, goals, experience, faction tags, turns, upkeep and asset actions** into persistent SWN entities exactly. Preserve book procedures and legal faction turn actions. A separate **NoöPunk Adapter** maps setting locations (e.g. Helsinki, orbit, Mars), network infrastructure, institutions and PCs into/from SWN asset events without changing dice, faction stats or legal actions.

**State layers:**
- `SWNFactionState`: canonical stats, assets, goal, money, moves and completed turn action; deterministic, source-faithful.
- `NooFactionState`: membership rank, permissions, goals, network reputations and ideology graph, never conflated with core values.
- `TurnEvent`: signed intent, preconditions, verified actor authorization, SWN action, mechanical outcome, resulting game events and ledger entry.
- `WorldNews` and `MissionOffer`: audience/scoped projections of those events without exposing hidden identities.

**Turn order:** propose intents via PC missions or strategist interface; validate resources and permissions; resolve one legal SWN faction action following the exact book rule sequence; persist transition and event log; generate bounded missions/news/rumors; then apply separately specified social/ideology narrative effects. Quest activity is **not another SWN action**. A rank-0 PC receives one-agent assignments, rank-1 partner jobs, rank-2 team commands, rank-3 local planning, rank-4 global strategy dashboards. Senior characters may propose a faction action but cannot unilaterally command an unowned faction or circumvent canonical SWN procedure.

**Dune House management influence:** optional organizational dossiers, assets/holdings, staff, house ambitions, patronage, prestige, favors and political deliberation; carefully avoid duplicate currencies and separate dice engines. Dune agent/architect is an interface distinction rather than a rule conversion.

### Practical vertical slice

Seed UNSA, a criminal syndicate and one corporation. One AI infrastructure disaster triggers a news/agenda card with two conflicting claims of *Security*, *Freedom* and *Humanity*. PC discovers evidence, publishes or withholds it, receives a bounded reputation change in SuomiNet or SipuliVerkko, and influences an **authored** faction goal. Later, a normal SWN faction turn may result in a propaganda/intelligence or asset operation, producing a playable UNSA assignment. Test that a PC's rank-up never changes SWN's legal action count.

### Implementation milestones and guards

1. Write a source-rule conformance matrix keyed to SWN Revised page references; do not distribute copyrighted full book text.
2. Implement SWN core with fixture tests around every legal action, economic state transition, asset movement/conflicts and turn sequencing.
3. Implement adapter and typed event log, with replay, rollback and invariant tests.
4. Add graph, reviewed annotations and agenda/event cards with provenance controls.
5. Expand from Helsinki factions to planetary/NHI factions as spoilers unlock, then later multiplayer or Mesa if desired.

**Licensing:** verify each game's relevant license before copying any text or rules data. References are for design inspiration, not license grants. Avoid vendor-specific mechanics or proprietary card text in released content.

**NoöPunk design rule:** Strategically deep behind the scenes, narratively simple to the player. Reveal the world by investigation, not a faction spreadsheet.
