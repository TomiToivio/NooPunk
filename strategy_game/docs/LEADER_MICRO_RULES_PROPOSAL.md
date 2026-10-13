# Leader and NPC micro-rules: author-review proposal (#295)

> **PROPOSAL ONLY, NOT CANON.** None of the numbers, attribute labels or procedures below are approved. This is a paper-playtest candidate, not the legacy RPG's STAT/TAG rules, and does not change executable game behavior.

## Design target and references

A player should be able to read one leader card and settle one consequential social choice in less than a minute. The crossover is **leader RPG + faction strategy + network politics in one tabletop-like game** (#347). The leader gives faction strategy a personal point of view, rather than spawning a second tactical role-playing subsystem.

- **NoöPunk legacy STAT/TAG (#280):** tags as a flexible way to characterize people, but **do not import** the six legacy STATs, 1–10 ratings or 1d10 rules without separate approval.
- **CK3:** interpersonal commitments, rivalries and character-driven dilemmas. Keep only the meaningful choice; no dynasty simulation.
- **Terra Invicta:** a small, consequential agent roster with distinct mission responsibilities. Do not introduce agent-spam or repetitive travel.
- **Dune house/agent lens:** leaders act personally and direct institutions; a successful personal check can create a *typed request* for a faction operation, never a free unbounded resource or automatic ideological conversion.
- **Citizen Sleeper:** one narrative scene, a choice, a visible roll, and an explicit lasting consequence. Do not copy its dice-pool rules.

## Candidate leader card

| Field | Illustrative leader “Dr. Mira Vale” | Status |
| --- | --- | --- |
| ID / name / faction | mira-vale / Dr. Mira Vale / Cosmist International | Example fictional identity, **not canon** |
| Reason / Nerve / Rapport | 2 / 1 / 3 | **Candidate** three attributes, integer 0–3 |
| Personality tags | “Academician”, “Gullible optimist” | **Example tags**, not a fixed taxonomy |
| Relationship | patron: Trust +1 | **Candidate** situational relation, not universal numeric reputation |
| Current dilemma | negotiate temporary access to an institute | Example scene, not canonical event |

Reason = research/inference; Nerve = functioning under pressure; Rapport = persuasion/rapport. Their names and count are explicitly up for review; an alternative is a **single capability score + descriptive tags**, with fewer bookkeeping costs.

## Candidate one-roll resolution (2d6 option A)

1. Player states **intent, target, stake, and which attribute**. GM reveals difficulty: **7 routine / 9 risky / 11 exceptional**, all *illustrative*.
2. Roll **2d6 + attribute (0–3)**. A relevant personality tag contributes **+1 once per roll** when the GM can explain how it helps. A harmful tag may impose **−1 instead**; never stack tags. Optional relevant relationship contributes +1, **but total situation modifiers are capped to +1**, including tag, to minimize optimizations.
3. **Total ≥ target** = intent succeeds, with a bounded consequence. Otherwise intent fails and a specific cost or changed situation is narrated; failure never means “nothing happens.”
4. No opposed double-roll: another character's resistance changes difficulty; the defending NPC is represented by the **same card** and a declared stake.
5. Record a **typed result**, not a direct state mutation: `LeaderOutcome(actor_id, action_kind, target_id, success, consequence_tag)` as a proposed interface. The faction/political system alone validates and applies downstream changes.

No reroll currency, leveling, wounds, combat, hacking or PSI subsystems are defined here. The same one-roll interface *might* later support personal encounters, but its use for physical/astral/cyber strategic operations is **not approved**.

## Worked 45-second example

Dr. Vale tries to convince the institute director to allow a one-day archival inspection. The GM sets the risky target **9** and states that a refusal will provoke an institutional review. Rapport **3**, “Academician” relevant **+1**. Dice **2 + 3 = 5**, final **5 + 3 + 1 = 9**: success. Outcome: the archive grants **temporary, limited access**. This does **not** automatically give Cosmist International institute ownership, political influence, a permanent asset, or an extra action. The GM records an invitation/access outcome for #296 to interpret once approved.

A second illustration: with dice **1 + 2 = 3**, final **7**, the director refuses and schedules a public ethics hearing. That is a consequence and a new story opportunity, not an arbitrary numeric influence loss.

## Minimal NPC procedure

1. NPC uses exactly the **same leader card format** and roll rule, without special GM-only attributes.
2. GM lists **one desire, one constraint, one relationship/tag** for this scene, publicly or in a sealed card.
3. NPC chooses between **agree / bargain / refuse** according to stated desire and constraint. No LLM necessary and no free-floating dice-based personality AI.
4. In an opposed exchange, set difficulty once from the declared resistance; do not give both parties extra action rolls.
5. Character relationship changes are logged as **proposed narrative consequences**, never automatic simulation effects.

## Paper-playtest checklist, not automated prose tests

- Can a new player understand a leader card in 30 seconds?
- Is the single roll readable without consulting a skill catalogue?
- Is the negative result interesting, and does it keep the turn moving?
- Is a tag situationally useful without encouraging a tag-hoarding arms race?
- Can the faction layer refuse or postpone a typed leader outcome without hidden coupling?
- Can two leaders with the same numbers feel different because of priorities and relationships?
- Is the founder/patron/court/four-field-agent composition from #346 supported without implying there are only four characters in the world?

## Decisions needed before any implementation

- **D1** Three attributes (Reason/Nerve/Rapport), a different set, or **one capability + tags**?
- **D2** 2d6 vs 1d10 vs no fixed die; target and modifier ranges?
- **D3** Should negative tag impact be player-invoked, GM-invoked or negotiated?
- **D4** Are explicit numeric relationships worth the tracking cost?
- **D5** Can one role card represent both faction council leadership and field operatives?
- **D6** What events, if any, may consume a character's action in a faction turn?
- **D7** Whether legacy STAT/TAG conversion exists at all; default is **no conversion**.

**Gate:** Once the author approves decisions D1–D7, update only `strategy_game/RULEBOOK.md`, add a small independently testable leader resolver and serialization tests, and then proceed to #296. Until then, **this file is strictly an example for discussion**.
