# The four fictional tag families (#1164, #1184)

> **Status: implemented.** `src/world/narrative_tags.py`, tested by `tests/test_narrative_tags.py`.
> This is the complete tag layer: **Social, Goal, Clue and Personality**. CWN's own tags (attributes,
> skills, statuses, equipment) are untouched and remain the character sheet.

CWN already answers "what can this character do?" These four families answer different questions:

| Family | Question | Not |
| --- | --- | --- |
| **Social** | how does this party stand toward that one? | a reputation score |
| **Goal** | what is the character trying to do, and what is in the way? | XP, or a quest log |
| **Clue** | what does this character actually know, and how do they know it? | proof |
| **Personality** | what will this NPC do under pressure? | an alignment |

## The three rules

1. **A tag is a fact, not a modifier.** Nothing here adds a number to a roll. A tag is true or it is
   not, and the procedure that reads it decides what truth buys. This mirrors
   `src/rules/psi_access.py`: an option is admissible or it is not.
2. **No invented vocabulary.** Social polarity, goal state and clue reliability all reuse words the
   repository already uses — the evidence ladder comes from the Helsinki gazetteer.
3. **The families stay apart.** A goal is not a clue; a clue is not proof; an NPC's personality is not
   a social stance. Keeping them separate is what makes *"what do I know?"* answerable at the table.

---

## Social tags

```python
SocialTag(id="social.falk.ledger", holder="npc.falk", target="pc.rookie",
          fact="owes a favour over the leaking warrant",
          polarity=Polarity.FAVOURABLE, source="scene.briefing")
```

A social tag records **a fact about a relationship**, in words, plus a polarity. It is not a number:
`favourable` does not mean +1, and two favourable facts do not make +2. What it does is make a social
check **admissible at all** — see the lever rule below.

`holder` and `target` must be different parties. A tag may name an expiry (an episode or scene ref),
because "owes me a favour" is not permanent.

### The lever rule

`run_social_scene()` refuses to roll when the character has **no lever**: no social tag between the
two of them, and no clue they hold that is *about* the person they are asking. A conversation with no
lever is not a hard conversation — it is a conversation that does not move, and rolling dice at it
would only pretend otherwise.

A clue about a warehouse is evidence of an act. A clue **about a person** (`bears_on`) is leverage over
that person. The distinction is the whole reason `bears_on` exists.

---

## Goal tags

```python
GoalTag(id="goal.find_courier", text="Find the courier before the shift change",
        owner="pc.rookie", state=GoalState.BLOCKED, blocked_by=("goal.warrant",))
```

Four states: `open`, `blocked`, `done`, `abandoned`. Two invariants are enforced because getting them
wrong is how a quest log becomes fiction:

- a **blocked** goal must name its blockers; "blocked" with nothing blocking it is a mood, not a state
- an **open** goal may not carry blockers; clear them when the state changes

`TagBook.completed_goal_ids()` returns exactly the shape `StoryGraph.available(completed=...)` expects,
so the story graph can gate scene transitions on goals without a second goal system.

---

## Clue tags

```python
ClueTag(id="clue.warehouse.pallet", clue_id="clue.pallet", holder="pc.rookie",
        fact="A pallet left after midnight", route="document", reliability="public",
        bears_on=("npc.falk",), scene_ref="scene.warehouse")
```

The clue's **content** stays in the case file (`src/rules/investigation.py`). This tag records that a
particular character has it, how they got it, and how far it can be trusted.

**Routes** — how it arrived: `observed`, `told`, `document`, `forensic`, `surveillance`, `informant`.
Informant work and surveillance are separate on purpose: the first is a person's word, the second is a
record.

**Reliability** — the gazetteer's evidence ladder, weakest to strongest:

`witness` → `public` → `authenticated` → `conflicting` → `anomalous`

This is deliberately **not a number**. "Authenticated" is a different kind of claim from "witnessed",
not a bigger one; a conflicting record is *stronger evidence* than a clean one only when the
conflict is the point.

---

## Personality tags

```python
PersonalityTag(id="personality.falk", npc="npc.falk", trait="procedural",
               lever="a clean paper trail",
               under_pressure="narrows the case to whoever signed",
               taboo="cover for a colleague")
```

`trait` is what they are like; `lever` is what actually moves them; `under_pressure` is what they do
when it costs something; `taboo` is what they will not do even then. A referee reads this instead of
guessing, and an NPC who acts against it is a **decision**, not a rounding error.

---

## The tag book

`TagBook` holds all four families and checks the joins a caller can afford to check: unknown
characters, unknown scenes, goals blocked by goals that do not exist. It is deliberately small — four
dictionaries and the joins between them. It is **not** a character sheet (CWN owns that) and **not** a
knowledge base (the case file owns that).

`to_dict()` / `from_dict()` round-trip, so a campaign can be serialised without a database.

---

## What this does not do

- It does not roll dice. `run_social_scene` borrows `rules.social`; everything else reads a tag.
- It does not grant clues. `run_investigation_scene` borrows `rules.investigation`, which already
  guarantees that core clues are not gated behind luck.
- It does not give NPCs an AI. A personality tag is a brief, and the referee is the interpreter.

## Cross-references

- [`SCENE_TYPES_1184.md`](SCENE_TYPES_1184.md) — the five scene procedures that read these tags
- [`WORLD_GRAPHS_1178.md`](WORLD_GRAPHS_1178.md) — the graph families the tags point into
- [`PSI_ACCESS_1178.md`](PSI_ACCESS_1178.md) — the same "admissible or not" discipline applied to powers
