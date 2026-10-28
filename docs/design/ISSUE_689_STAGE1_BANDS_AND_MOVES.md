# Stage 1 — outcome bands and the closed move set (#689)

**Status: PROVISIONAL specification.** Every number is marked where it is a proposal rather than a
derived value. Nothing here edits the rulebook; Stage 1 produces the table that a later rulebook edit
will copy from.

Stage 0 (`ISSUE_689_STAGE0_REANCHOR.md`) established the one non-negotiable fact: on `2d6`, a numeric
`+1` is worth 16.7 pp at a contested target and **0.0 pp** at the cap, so "one step" must mean **one
band**.

---

## 1. The bands

The check is unchanged: `2d6 + attribute modifier + skill level` against a difficulty (6/8/10/12/14).
The band is read from the **margin**, i.e. `total − difficulty`:

| margin | band | meaning |
|---:|---|---|
| **+2 or more** | **clean** | you do it, and you do it well enough to choose one detail |
| **0 or +1** | **cost** | you do it, and the world takes something for it |
| **−1 or worse** | **miss** | you do not do it; the fiction moves against you |

`+2` for "clean" is chosen because it is the smallest margin that cannot be reached by the dice alone
without beating the target by two — and because it makes the clean band **16.7 %** at a contested
target, which is where Stage 0 measured the curve's steepest point. **PROVISIONAL: the +2 boundary.**

**Bands are the same arithmetic as the rulebook's existing success/failure split**; only the middle
band is new. A table may switch bands off and read `margin ≥ 0` as success — see §5.

## 2. The closed move set

Eight moves. Each is a *procedure*, not a new skill: it names when to roll, which skill to use, and
what the three bands mean. All eight map onto existing skills from `data/rules/core.json`.

### 2.1 Read a Sitch
- **Trigger:** you stop and study a situation, person or room for leverage.
- **Skill:** `Perceive`, or `Investigation` when reading a scene rather than a person.
- **Clean:** ask the referee two questions from a fixed list; both are answered truthfully.
- **Cost:** one question answered, and something notices you asking.
- **Miss:** the referee answers a question you did not ask — true, but not useful, or useful but not
  true. One clock advances.

### 2.2 Apply Pressure
- **Trigger:** you demand, threaten, charm or bargain for something a person does not want to give.
- **Skill:** `Provoke` (force) or `Talk` (leverage). `Deceive` when the leverage is a lie.
- **Clean:** they give it, and do not mark you for it.
- **Cost:** they give it, and they remember. Write their name on the sheet.
- **Miss:** they refuse and harden; the pressure clock advances.

### 2.3 Hold Steady
- **Trigger:** something in the fiction would make you flinch, freeze, flee or break.
- **Skill:** `Psychic Defence` for noetic pressure; the **Mental save** for ontological exposure
  (Stage 3 owns the shock procedure; this move is the general case).
- **Clean:** you hold, and you may name the one thing you refuse to look at.
- **Cost:** you hold, and take a temporary Condition (Stage 3, §5).
- **Miss:** you break — the referee chooses one: flee, freeze, or comply.

### 2.4 Cross a Threshold
- **Trigger:** you enter a place, network, jurisdiction or ontology that is not yours.
- **Skill:** `Sneak` (physical), `Interface` (network), `Noöspace` (noetic), `Survival` (wilderness).
- **Clean:** you are in, and you know one way out.
- **Cost:** you are in, and something on the other side knows you came.
- **Miss:** the threshold is closed, and the alarm clock advances.

### 2.5 Set Up
- **Trigger:** you do something that makes an ally's next action easier.
- **Skill:** whatever the setup actually is.
- **Clean:** your ally's next check gains **one band** (never more).
- **Cost:** one band, and you are exposed while they act.
- **Miss:** no band, and your ally's next check is at **−1** (a WN circumstance penalty).

### 2.6 Ground Yourself
- **Trigger:** a scene of rest, a trusted person, a hospital, a ritual, a dose.
- **Skill:** `Connect`, `Medicine`, or `Perform` for ritual.
- **Clean:** cancel one **temporary** Condition.
- **Cost:** cancel one temporary Condition, and it costs something material (time, money, a favour).
- **Miss:** nothing is cancelled, and the next grounding attempt this session is at −1.

### 2.7 Contact the Noösphere
- **Trigger:** you reach for what is not in the room.
- **Skill:** `ESP`, `Telepathy`, `Precognition` or `Noöspace` — whichever the character actually has.
- **Clean:** contact, and one true impression.
- **Cost:** contact, and the impression arrives with something attached (a presence, a price).
- **Miss:** contact with something that was also reaching. Stage 3 exposure.

### 2.8 Withdraw
- **Trigger:** you disengage from a scene, fight or network without being followed.
- **Skill:** `Sneak`, `Fray` or `Interface`.
- **Clean:** you are out clean.
- **Cost:** you are out, and you leave something behind (evidence, a person, a trace).
- **Miss:** you do not get out this exchange.

## 3. Why this set and not a catalogue

Eight moves cover the loop the game actually runs — look, push, endure, enter, help, recover, reach,
leave. A larger set would be a second skill system wearing narrative clothes, which #689 §11 forbids.
**PROVISIONAL: the eight, and their skill bindings.**

## 4. What the moves must not do

- They must not replace a skill check. Every move *is* a skill check; the move only says which
  three outcomes mean what.
- They must not grant flat bonuses that stack with WN circumstance (−2..+2) or aid (+1). **Set Up**
  grants a *band*, never a number, precisely so it cannot stack with them.
- They must not exist in a vacuum: if a move's trigger does not fire, no roll happens.

## 5. Bands on or off

**Proposal (P2):** bands are **on by default in social, investigation, psychic and environmental
play**, and **off by default in combat**, where CWN's Shock/Trauma already punish partial success
twice. A table may turn bands on everywhere, and the referee must say so at session zero.

Rationale: combat already has a cost band — it is called *being shot*. Adding a narrative cost on top
double-charges the same moment.

## 6. Worked example (bands on)

> Mira is trying to get a hospital archivist to open a ward log. `Talk 2`, `CHA +1`, total **+3**,
> difficulty **10** (the archivist is afraid). She rolls **8** → margin **+1** → **cost**.
> She gets the log, and the archivist's name goes on her sheet: someone will ask him about it.
>
> Had she rolled **10** (margin +2), it would be clean — she gets the log and he never mentions it.
> Had she rolled **6** (margin −1), the log stays closed and the ward's clock advances.

## 7. What Stage 1 does not do

- No rulebook edit, no code, no tests. The move set is a specification for a later implementation
  issue, per #689 §9.
- No playtest evidence: §6 is an illustration, not data. Stage 4 is where the set gets measured.
