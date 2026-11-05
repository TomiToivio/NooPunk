# Scene proposals: interrogation, data collection, data analysis (#1184)

> **Status: proposal — nothing here is implemented.** The five live scene types are in
> [`SCENE_TYPES_1184.md`](SCENE_TYPES_1184.md). This document answers the author's four questions:
> do we need interrogations, data collection and data analysis as *separate scene types*, and how much
> GUMSHOE should the investigation layer take?

The test applied to every proposal below: **does a separate type buy a different procedure, or only a
different label?** A type that resolves exactly like another type is a synonym, and a synonym that
validates is a second vocabulary nobody documented.

---

## 1. Interrogation — **not a new type; a procedure inside two existing ones**

*Reference: Silicon Dreams (2020).*

**What makes Silicon Dreams work** is not the room. It is that an interrogation is a **dialogue puzzle
against evidence**: the suspect makes a statement, you hold a contradiction, and presenting it costs
you something if you are wrong. That is a Social scene (the exchange, the pressure, the Grievance) with
an Investigation spine (the clue tags you can present). Splitting it into a sixth type would give the
table two ways to ask the same question and no rule for which one applies.

**Proposal: an `interrogation` variant of the Social scene**, with three added verbs and one hard
constraint:

| Verb | Effect |
| --- | --- |
| `ask` | ordinary social exchange; needs a lever, as always |
| `present(clue_tag)` | put a clue in front of the subject |
| `corroborate(clue_tag)` | check the statement against a *second, independent* clue |

The hard constraint is already the repository's law: **Kinesics reads cues, not truth**
(`rules.social.detects_lie` — only independent evidence detects a lie). So an admission requires
**two clue tags with different routes** that both bear on the statement. One clue is one person's
word against another's; two are a case.

**Cost:** ~120 lines in `scenes.py`, no new vocabulary, no new type. **Verdict: worth doing, after the
five live types are exercised by a real scenario.** It is the cheapest of the three proposals and the
one with the most obvious table presence.

---

## 2. Data Collection — **yes, a separate type**

*References: Orwell (2016) for the Panopticon; OSINT and HUMINT for the methods.*

This one is different in kind, and the difference is why it deserves its own type: **collection is
repeatable, cumulative, and its cost is exposure rather than failure.** You do not "fail" to read a
feed; you read it and the log records that you did.

| Source | Method | Yields | Cost |
| --- | --- | --- | --- |
| Open sources | OSINT — public records, social media, procurement notices | low-rung clues (`public`) | time; nothing else |
| Panopticon | Europol's security system: cameras, plate readers, transit taps | `authenticated` clues | an audit trail that names the officer |
| Informatics | HUMINT — a person who tells you things | `witness` / `told` clues | a favour spent, and the source's risk |

**Design constraint that makes it a scene and not a dice roll:** each collection action returns a
**fact plus an exposure increment**, never "you find nothing". A null result is a fact too — *the
camera was offline* is a clue — and a procedure that can return silence teaches players to stop
collecting.

**Panopticon is the interesting one** because it is the setting's central political object: the system
that makes the investigation possible is the same system that makes everyone legible. Its rules should
make the trade explicit — access is cheap, accountability is not. Every Panopticon query writes a
record naming the officer who made it, and that record is available to Internal Affairs and to the
defence.

**HUMINT** ties directly to the tag layer: an informant is a `PersonalityTag` (what moves them, what
they will not do) plus a `SocialTag` (what they are owed). Asking costs the tag, and a source who is
burned is a fact the campaign keeps.

**Cost:** ~200 lines, one new vocabulary (sources, exposure), and it needs the `Action` scene's
"recorded reason" discipline to stay honest. **Verdict: yes — this is the type that most deserves to
exist, because no other scene model fits gathering.**

---

## 3. Data Analysis — **yes, but built on what already exists**

*Reference: the evidence board; Cyber Manhunt for the shape, not the minigames.*

The author's own description is the design: *"more like a puzzle: creating a case with the available
clues."* That is not a knowledge check, and it must not become one — a roll would make the player's
thinking irrelevant.

`rules.investigation` already has the pieces: `Hypothesis`, clue benefits with costs, and the core-clue
guarantee. **Proposal: an `analysis` variant of the Investigation scene whose pass condition is a
defensible case**, defined as:

1. at least **two clue tags** support the hypothesis, and
2. they come from **different routes** (a document and a witness, not two documents from the same
   filing cabinet), and
3. no held clue tag **contradicts** it without an explanation, and
4. the supporting clues are **held by the character presenting the case** — not by the party, not by
   the file.

That last clause is what makes the board a *character* scene rather than a table bookkeeping exercise.

**What to avoid:** the puzzle must not gate progress. A failed analysis closes a *route* (the
prosecutor declines, the warrant is refused) and the campaign continues; it never dead-ends. This is
the same rule as core clues, applied to conclusions instead of evidence.

**Cost:** ~150 lines plus a scenario that exercises it. **Verdict: yes, and it is the most Noöpunk
scene of the three — the player assembles meaning out of fragments, which is what the whole game is
about.**

---

## 4. GUMSHOE — already the spine; take no more

The investigation module is **already GUMSHOE-derived** and says so: competency buys the clue, core
clues are never gated behind luck, and extra information has an explicit cost (`Benefit` +
`benefit_cost`).

**What to keep taking:**

- the **no dead ends** rule — a scene with no reachable core clue is a broken graph, checked in `Case.validate()`
- **spend for extra** — the benefit/cost pair, paid in CWN terms (a check, a scene, a favour, credits)

**What not to take:**

- **point pools** (Investigative Ability spends). CWN already has its own resource economy; a second
  pool is a second economy, and the table would have to track both. The benefit/cost pair gets the
  same design value without a new currency.
- **the GUMSHOE skill list.** CWN's skills are the character sheet. Inventing a parallel list would
  duplicate the sheet.

**Licence status: unresolved and blocking.** The GUMSHOE SRD is OGL, while
`GUMSHOE_INVESTIGATION_LAYER.md` describes it as CC BY 3.0. Issue #932 asks which one applies. Until
that is answered, **no new GUMSHOE text should be copied**; the structural ideas already implemented
are design patterns, not transcribed text.

---

## 5. Astral — postponed, again

Not proposed here. It returns when a scripted Astral Projection scene needs a navigable graph. The
current refusal is deliberate and loud (`PostponedScene`), so nobody ships a scene that resolves to
nothing.

---

## Recommendation summary

| Proposal | Verdict | Why | Approximate cost |
| --- | --- | --- | --- |
| Interrogation as a **new type** | **No** | resolves exactly like Social + Investigation | — |
| Interrogation as a **variant** | **Yes, later** | dialogue puzzle against evidence; two independent routes for an admission | ~120 lines |
| **Data Collection** as a type | **Yes** | different failure model: cumulative, exposure-costed, never silent | ~200 lines |
| **Data Analysis** as a type | **Yes** | the puzzle is the point; built on `Hypothesis`, never gated on a roll | ~150 lines |
| More GUMSHOE mechanics | **No** | no second resource economy; licence unresolved (#932) | — |
| Astral scenes | **Postponed** | author decision | — |

**Order I would build them:** Data Collection → Data Analysis → Interrogation variant. Collection
feeds analysis, and the interrogation variant needs clue tags that actually exist in play before it has
anything to present.

## Cross-references

- [`SCENE_TYPES_1184.md`](SCENE_TYPES_1184.md) — the five implemented types
- [`NARRATIVE_TAGS_1184.md`](NARRATIVE_TAGS_1184.md) — clue routes and the evidence ladder these proposals rely on
- [`../design/ISSUE_1043_SWN_PSIONICS_FACTIONS.md`](../design/ISSUE_1043_SWN_PSIONICS_FACTIONS.md) — the investigation layer's own record
