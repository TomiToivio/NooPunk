# Issue #346 — acceptance record

**Basis for closing.** The author authorised defer-and-close on 2026-10-13, provided a deferred item is
stated as deferred. This issue was reopened deliberately at 19:43 for a stated reason — *"a container is
not a rule, and a document is not a mechanic"* — and that reason is answered here rather than
sidestepped: the containers are **verified to exist**, and the mechanics are recorded as **deferred** to
the author, not claimed.

## Verified met (measured on `main`)

| What | Evidence |
| --- | --- |
| **The five qualitative axes** and the **typed shared TAG vocabulary** | `faction_creation.py` + `data/faction_creation.json`; `test_faction_creation` — **28 tests OK** |
| **The four card types** — character, organization, research, government — with their **declared interactions** | `faction_cards.py` + `data/faction_cards.json`: `card_types` = those four, `declared_interactions` = six, `control_states` = seven; `test_faction_cards` — **27 tests OK** |
| **The card layer enforces no mechanic** | `faction_cards.py` sets `EFFECTS_ENFORCED = False`, and the data carries `pending_author_decisions` = `declared_interaction_effects`, `government_primitive_member`, `fifth_card_type`. This is the criterion stated *as structure*, which is the only honest form before rules are approved |
| **The authored recruitment/diplomacy event** (the "one authored event" task) | PR **#426**, *The Neutral Laboratory*: three beats, three meaningful commitments, follow-up scenes; built on the existing five-axis vocabulary and typed TAG model, preserving the player/GM information boundary, consent, cross-axis contradictions and separate NHI diplomacy — narrative data only, no invented numeric rules (`cbecbcb`, `6d26f65`) |
| **Character-card conventions reused, not duplicated** | `characters.py` + `data/character_cards.json`, with the world-catalogue reader added for the sibling card system |

## Standing constraints the issue records (not deliverables)

Tasks 9, 10, 13, 14, 21, 28 and the Helsinki-scope set (34–39) are rules for *future* writing: three
genre pillars as a filter, political science primary, humanity kept recognisable, religious imagery never
treated as verified claim, tabletop-convertible agent-led mechanics, all fiction explicitly inside
NoöPunk. They constrain what may be written; they produce no artifact and cannot be "finished".

## Deferred — the rules (2 criteria)

| Criterion | Position |
| --- | --- |
| 6. Abstract mission resolution | **deferred** — a rule; `strategy_game/RULEBOOK.md` still says strategy and political-simulation rules are not approved. Carried in the queue beside #323's six decisions, which are the same gate |
| 7. First-turn resource constraints | **deferred** — resource economics must not be guessed (#338 records the same boundary). Same queue row |

## Deferred — the authorial canon and decisions

Twenty-odd tasks are author work: the cultural-axis decision (liberal/conservative *or* also
authoritarian/libertarian); NHI contact policy held apart from named NHI diplomacy; the EFTZ commercial
and legal structures; the classified ARV-by-1981 timeline; two contrasting Soviet-program successor
factions; ancient and contemporary breakaway civilizations; the fourfold evidence categories; the
Law-of-One political reinterpretation and its Confederate Social Memory Complex; the Soviet–Confederacy
and US–Orion relationships; the disclosure mystery's ideological terminus; and the Cosmist
International set — founder identity, manifesto in game terms, Helsinki nonprofit and conditional
government collaboration, the introductory scene. Each is listed in the queues row **D12** and must not
be invented by an agent.

**A note on the checkboxes.** The issue's 48 boxes are still unchecked, including many whose structure
landed after they were written (the axes, the TAGs, the card types, the authored event). They were not
edited, because the work landed in PRs, not in the issue text; this record is the current state.

— Ai (愛)
