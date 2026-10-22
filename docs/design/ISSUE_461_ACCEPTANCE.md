# #461 acceptance record — Fate/Transhumanity's Fate procedures and the five-order turn

**Date:** 2026-10-22. **Status:** acceptance record. **The issue is titled "Design with Tomi", and the
parts that remain are exactly the parts that need Tomi.** This record states what is delivered and
what is not.

## What the issue asks for, and where it lives

| Criterion | Where it lives | Status |
| --- | --- | --- |
| **Character generation**: minimal attributes/skills/aspects/tags, advancement, and how leader and agent roles differ | `strategy_game/rpg/skills.py` — `INDIVIDUAL_SKILLS` (COG, INT, REF, SAV, SOM, WIL); `strategy_game/rpg/roster.py` — `Seat` (`LEADER`/`AGENT`), five seats, `AGENT_SEAT_COUNT = 4` | **met as structure**; the starting **allocation** and advancement are D23 and are *not* specified |
| **Skill checks**: the randomiser, modifiers, degrees of success, failure/consequence handling | `strategy_game/rpg/fate.py` — the approved 4dF kernel, four outcomes, `ActionContext`; `strategy_game/RULEBOOK.md` §5 | **met** — but the *choice* among candidate mechanics is D31, and D32 (a distinct "success at a cost" band) is open |
| **Generic action vocabulary**, and the distinction between a strategic map mission and an individual scene | `strategy_game/RULEBOOK.md` §8 ("Play at the two scales"); `strategy_game/rpg/scene.py` | **met** |
| **Special actions**: eligibility representation, acquisition and cost — cyberattack (netrunner) and remote-viewing espionage (psyker) as the illustrative gates | `strategy_game/rpg/fate.py` — the capability gate refuses **before** any dice; `strategy_game/data/faction_creation.json` — the `TELEPATH`, `REMOTE_VIEWER`, `PRECOGNITIVE` capability vocabulary; `strategy_game/data/character_cards.json` — the `archetype_netrunner` card | **met** — no new powers or mission lists were invented |
| **Turn sequence**: when the five orders are committed and resolved, how travel matters, what happens when an action is impossible, and whether actions interact — preserving **one action per character per turn** | `strategy_game/rpg/roster.py` — `TurnLedger`, one action per *character*; `strategy_game/council.py` — `structural_problems` refuses an ineligible order **at declaration**, and the order is lost rather than substituted | **met as structure**; travel/time costs remain an author decision |
| **RPG vs strategic level**: how a skill check represents an abstract faction mission versus an intimate character scene | `strategy_game/rpg/boundary.py`'s pinned contract — the RPG layer imports no strategy engine module and reads no roster file | **met** |
| **Playable simplicity**: mechanics representable with tabletop + board + cards + dice, with the minimum components and cognitive load explained before complexity | `strategy_game/RULEBOOK.md` §§1–2 and `strategy_game/rpg/RULEBOOK.md` — the playtest field manual | **met** |
| **Interaction with factions**: individual actions leading to organisational, network, political or ideological consequences, reusing approved world structures | `strategy_game/campaign/missions.py` — `apply_mission_outcome()` writes the four Phase-1 books by id-level membership, never arithmetic | **met**; whether those consequences reach the *strategic* layer is D35 |
| **Five controlled characters and exactly one action each per turn**, including ineligible orders | `strategy_game/rpg/roster.py`; the RPG-first case runs `leader` + four agents | **met** |
| A **tiny illustrative five-order turn** for author review, with unapproved mechanics labelled as proposals | `docs/design/ISSUE_461_CONSENSUS_PROPOSAL.md` — "Worked five-order turn for editorial review (2026-10-15; not a new rule)" | **met** — it is explicitly labelled an illustration, not a rule |
| **Differences from Fate Core / Transhumanity's Fate / Eclipse Phase and PbtA**, without importing the EP setting | `ISSUE_461_CONSENSUS_PROPOSAL.md` §4 (the SRD crosswalk, with §4.3 on licensing); `strategy_game/rpg/ATTRIBUTION.md` | **met** |
| After approval: update `strategy_game/RULEBOOK.md`, implement the approved Python rules, test executable behaviour | the rulebook and the engine exist; **the approval is what is missing** | **not reached** — the condition is the author's approval |
| Editorial approval and tabletop playtest feedback before closing | the three-path playtest exists (`strategy_game/rpg/playtest.py`); the **editorial approval** does not | **partly met** — mechanical playtest done, editorial approval outstanding |

## The two documents, reconciled

`ISSUE_461_CONSENSUS_PROPOSAL.md` and `ISSUE_461_RESKIN_SPEC.md` previously disagreed about the
capability mechanic. The disagreement is **recorded as a consensus decision** rather than left as
two public positions, and the consensus document states its own status: *"PROPOSAL. No rule, number,
action list, dice procedure or capability is approved by this document."*

## Open items carried forward, not buried

**D23** the six individual skills' starting allocation and advancement (character creation) ·
**D30** the trait architecture — six skills, or six attributes *and* six skills (the character sheet)
· **D31** the unified resolution mechanic and its three sub-choices · **D32** whether there is a
distinct "success at a cost" band · **D33** whether "simplified science" is a seventh individual skill
· **D37** the sign-off. All are tracked on **#532**.

## Reproducible checks

```bash
python3 -m strategy_game.rpg.playtest
python3 -m unittest discover -s strategy_game/tests -p "test_*.py"   # 1535 tests, OK
python3 -m unittest discover -s tests -p "test_*.py"                 # 585 tests, OK
```

## What closure of #461 does and does not mean

It means the issue's **framing is delivered and reconciled**: the five-seat roster with one action
per character per turn, the simplified Fate procedures, the capability mechanic, and a worked
five-order turn, all implemented and all eight design questions and nine acceptance criteria
individually dispositioned against #482 and #516.

It does **not** mean any of the character-sheet or resolution **rules** are approved, that the
capability mechanic is canon, or that the five orders have author sign-off. Those are D23, D30–D33
and D37, and they are the author's.
