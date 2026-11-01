# Implementation crosswalk: #1008, #1007, #1006, #985, #981

## Authoritative decisions and conflicts

- #1006 is authoritative for immutable CWN and opt-in SWN/WWN/AWN mechanics. The existing `docs/rules/RULES_CONSTITUTION.md`, registry and boundary tests already encode the lock. SWN psionics remains listed as **planned**, not implemented.
- #1007 already has `docs/design/DESIGN_CANON_1007.md`. Opening remains grounded and revelation is earned through investigation, not an omniscient narrator.
- #985 already has `mud/nopunk_mud/consciousness.py`, `case_consciousness.py` and corresponding tests. These are an investigative prototype, not verified consciousness detection. The collaborating university scientist and the final protocol name are **author decisions pending**. Do not invent them.
- #981's separate Finnish/English localization and English-only agent language requirements were **superseded by #996**. `docs/FINNISH.md` and `mud/AGENTS.md` are canonical: one Finglish player-facing language, mostly English agent drafts with light vocabulary from `GLOSSARY.md`, and Tomi's Finnish/Finglish text immutable.
- #1008 phase 1 adds the pure-Python `mud/nopunk_mud/faction_overlay.py` and tests. It is a reusable state model **not yet wired to Evennia persistent character attributes, commands or NPC reaction handlers**. No claim of full feature completion.

## Phase 1 design contracts (#1008)

Membership is scoped per organization, ranks 0–4 are mission-lead authority, not CWN character levels or SWN actions. Default new overlay is UNSA rank 0. Promotion requires explicit authorization, evidence and one-step advancement. Suspension revokes authority. Salary, equipment, training and XP rewards must be mediated by existing CWN progression and mission resource systems; do not duplicate the XP economy.

Reputation is keyed by `scope:target` and constrained to −4…+4. The five named networks are UNSA, SipuliVerkko, SuomiNet, Internet and MarsNet Hype. NPC relationships may override network standing **only when the NPC knows of them**; the caller explicitly supplies ordered known contexts. Only one context applies. Default NoöPunk reaction modifier is capped at ±2 for balance pending CWN source-rule verification, and must be applied outside the canonical 2d6 reaction algorithm, never by rewriting that algorithm. Classified knowledge is not visible through public queries.

Goals have stable IDs, owner, description, target, priority, status, dependencies and progress; they have no direct dice bonus. Audit records accompany mutable state. JSON snapshots allow adapter-owned persistence and support migration.

## Phase 2 design only: LaclauGPT ideology adapter

Use separate records for `actor`, `concept/signifier`, `statement`, `articulation`, `audience network`, `source`, `confidence`, `visibility` and `valid_time`. Graph edge: `actor -> statement -> concept` with explicit support/oppose/ambivalent stance. Store reported speech separately from actor belief, truth and PC knowledge. Record empty/floating signifiers, chains of equivalence, antagonisms, and competing hegemonic projects as interpretive edges with provenance and review status.

Never infer positive standing from ideological agreement. Quest outcomes can propose bounded reputation changes only when validated by deterministic game events and observed in a relevant network. LLM suggestions are not authoritative events. No real-world LaclauGPT research dataset is imported as in-world truth.

## Phase 3 design only: SWN strategy boundary

Preserve SWN Revised's Force/Cunning/Wealth, FacCreds, HP, experience, tags, assets, movement, faction-turn sequence and one-action-per-turn baseline. Implement that source-verified engine in its own module at a later stage; do not prototype a competing economy.

Separate three time scales: individual PC missions, rank-authorized field team operations, and legal SWN macro turns. Missions may queue *proposals* (asset change, damage, goal progress, intel), not silently execute additional faction-turn actions. Use a deterministic transaction log with versioned turn snapshots, validated commands, explicit GM/player knowledge views, replay and rollback. Strategic outputs may seed spoiler-gated missions and public network rumors. Dune's architect/agent viewpoint is an interface inspiration only; no Dune 2d20 resolution.

## Outstanding gates before closing

1. Wire the overlay to the existing Evennia/campaign character persistence and expose `factions`, `rank`, `reputation` and `goals` commands.
2. Verify NPC reaction formula against licensed CWN reference before adding the optional reputation modifier.
3. Implement tests for promotions and replay, visibility to NPCs, access permissions and CWN XP rewards; audit any existing unfaithful core mechanics separately.
4. #985: author approves collaborator/name; integrate interview into opening mission and preserve guaranteed core clues.
5. #981: verify single-language fallback and glossary/help, preserve author-owned source and spoiler gates. Do not revive separate locale editions.
6. Source/page/license audit for SWN faction chapter and other proprietary inspiration before phase 3.
