# Stage 3 — the mind system (#689, Option A: Conditions)

**Status: PROVISIONAL specification.** Option A is the one the register marks as needing **no canon
override**, so it is the one specified here. Options B (two pans) and C (EP-grade) remain on the board
as alternatives (P3).

The design goal, in the author's words, is *psychiatric drama in the style of PKD, Maniac and Riget*:
minds warped by repeated ontological shocks. So the system must model **what a person can no longer
see straight**, not how many sanity points are left.

---

## 1. The loop

**Exposure → save → Condition → integration → a different person.**

Five steps, one roll, and a sheet that changes permanently.

## 2. Exposure

A scene declares an **ontological exposure** and its **tier** (1–4):

| tier | what it is | example |
|---:|---|---|
| 1 | an anomaly one person can dismiss | a timestamp that is wrong by a minute |
| 2 | an anomaly a professional cannot explain | a body that is not the body that walked in |
| 3 | a paradigm that was load-bearing turns false | the ward's patients were never patients |
| 4 | the world's own account of itself fails | the dead answer, and are right |

The world's baseline tier comes from the paradigm ledger (Stage 2, §3): a society whose capability
outran its legitimacy raises everyone's floor.

## 3. The save

**A Mental save** — the existing 1d20 grammar from `src/rules/cwn_core.py`. No new dice, no new scale.

**Penalty: −2 per tier of gap** between what the exposure demonstrates and what the character has
already integrated, **maximum −4**.

**Holding evidence removes one step of the penalty.** This is why the evidence ledger
(`src/rules/investigation_evidence.py`) matters: a character who has already documented the impossible
is harder to break with it.

| gap | penalty |
|---:|---:|
| the character has already integrated this class | 0 |
| adjacent to something integrated | −2 |
| entirely new class | −4 (cap) |

## 4. Outcomes

| result | outcome |
|---|---|
| **pass** | nothing. The character has seen it and it did not cost them. |
| **pass by 5+** | a **permission**: "you read the pattern now" — a permanent, narrow capability. |
| **fail** | a **Condition**. |
| **fail by 5+** | a Condition, **and** an armed compel (Stage 1 §2.3 / Fate layer §6). |

## 5. What a Condition is

A Condition is **TF-shaped and bounded**. It has exactly five fields and no numbers:

| field | content |
|---|---|
| **statement** | one sentence, in the character's voice — "the ward breathes when nobody is watching" |
| **scope** | which checks it touches: a skill, a place, a kind of person |
| **duration** | `temporary` (one scene) or `lasting` (until integrated) |
| **effect class** | **permission** (you can attempt X), **denial** (you cannot attempt Y), or **one step** (a band against you on scope) |
| **cancellation** | what specifically would lift it, written when it is taken |

**Cap: three Conditions at a time.** A fourth replaces the oldest *temporary* one — or, if all three
are lasting, the character cannot take a fourth and the exposure resolves as a scene instead.

**No boxes. No accumulation. No numbers.** The moment a Condition grants +1/-1 to anything, it has
become a modifier and the system has become a second skill tree.

## 6. Integration — the character is not restored

Integration is a **WWN major project**: therapy, study, a cult, a support network, or fieldwork, run as
a project with segments. On completion, a Condition converts into a **permission aspect** —
*reframed* — and **the character is permanently different**.

This is the design's spine and its answer to PKD/*Maniac*/*Riget*: you do not get the old self back.
You get a working one, and the sheet says what it cost.

## 7. Fast recovery

**One scene of grounding** — sleep, a trusted person, a hospital, a ritual — plus a successful check
(Stage 1 §2.6) cancels **one temporary** Condition. Lasting Conditions do not clear this way.

## 8. The abuse case, stated so it can be tested

**The exploit:** a player farms Conditions to farm compels (a compel earns narrative currency).

**Two defences, both mechanical:**

1. **One armed compel per scene**, regardless of how many Conditions are held.
2. **Every Condition in the `one step` class is a band against the character on its scope** — hoarding
   hurts immediately, in the exact situation the Condition names.

A third, social defence is not a rule but a table convention: the referee states the Condition's
statement in the *player's* words, not their own. A Condition the player does not recognise is
bookkeeping.

## 9. Safety procedure (non-negotiable)

Material about psychosis, dissociation and institutional psychiatry is not abstract. Before play:

- **Lines and veils** are set at session zero and are immutable for the campaign.
- **The X-card is honoured without discussion.**
- **No Condition may be used to remove a player's authorship of their character's mind.** The referee
  describes what the character *perceives*; the player says what the character *does*.
- **Real diagnostic labels are not stat blocks.** No "you are schizophrenic" as a mechanic.

## 10. Worked scenes

**Integration succeeds.** Mira fails a tier-3 exposure: Condition *"the ward breathes when nobody is
watching"* — scope: `Notice` in the hospital; lasting; effect: one step against; cancellation: a
WWN project proving what the breathing is. Three sessions later the project completes: it becomes a
permission, *"you can hear a building lie"*, and it never goes away.

**Integration fails.** The same character, later, fails by 5+: the Condition stays, and an armed compel
is added — the referee offers a complication for currency. Refusing it is legal and costs nothing but
the currency.

**A compel is refused.** The player declines. The fiction does not move against them; they simply do
not get the point. A refused compel is not a failed save.

## 11. What Stage 3 does not do

- No rulebook edit, no code, no tests.
- No claim that this models real mental illness. It models **what a fictional character can no longer
  see straight**, and §9 exists so that it does not do more than that.
