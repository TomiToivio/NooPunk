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
The band is read from the **margin**, i.e. `total − difficulty`.

**This section was reconciled on 2026-10-28 with the implementation that is now on `main`**
(`src/rules/narrative_layer.py`, stated in `rulebook/19_NARRATIVE_LAYER.md`, PR #695). The code and
the chapter are the authority; what follows is their rationale, and the three-band table this
document originally proposed is superseded.

| margin | band | GM move | meaning |
|---:|---|---|---|
| **−1 or worse** | **miss** | *escalate* | you do not do it; the fiction moves against you |
| **0 or +1** | **cost** | *cost* | you do it, and the world takes something for it |
| **+2 to +4** | **clean** | *reward* | you do it cleanly |
| **+5 or more** | **style** | *reward and an aspect* | you do it, and an aspect goes in your favour |

At a contested target (DV 8, modifier 0) the thirty-six outcomes fall **21 / 9 / 6 / 0** across miss,
cost, clean and style. One step moves six outcomes out of miss (**+16.7 pp**) and two steps land
exactly where an unmodified roll lands at DV 6 — which is why the layer allows one invoked step and no
more. `band_distribution()` recomputes those shares from the dice, so the table cannot drift away from
them without a test failing.

The `style` band exists because a very good roll needs somewhere to go that is better than *clean*
without being a second success; it is the one addition this reconciliation makes to the original
three-band proposal. **PROVISIONAL: the +2 and +5 boundaries (P2).**

A table may switch bands off and read `margin ≥ 0` as success — see §5.

## 2. The closed move set

Eight moves. The catalogue is the authority: `data/rules/narrative_moves.json`, resolved by
`src/rules/narrative_moves.py`, stated in `rulebook/19_NARRATIVE_LAYER.md`.

Each is a *procedure*, not a new skill: it names when to roll, which existing skill to use, and what
the four bands mean.

**Skill bindings are the Without Number list.** The original draft bound them to
`data/rules/core.json` — `Perceive`, `Investigation`, `Provoke`, `Deceive`, `Interface`, `Fray`,
`Noöspace` — which the 2026-10-26 baseline retired as tabletop authority. The shipped catalogue uses
`Notice`, `Talk`, `Sneak`, `Heal`, `Know` and the mental save, and validates every binding against
`data/rules/without_number.json` so a rename in the baseline cannot leave a move dangling.

| move | roll | trigger |
| --- | --- | --- |
| **Read a situation** | `Notice` + INT | you stop and study a place and ask what is really going on |
| **Read a person** | `Talk` + CHA | you watch someone under pressure and want the truth |
| **Apply pressure** | `Talk` + CHA | you demand, threaten, charm or bargain for what they do not want to give |
| **Hold steady** | mental save (`1d20`) | something in the fiction would make you flinch, freeze, flee or break |
| **Cross a threshold** | `Sneak` + DEX | you enter a place, network, jurisdiction or ontology that is not yours |
| **Set up** | whatever the preparation actually is | you spend your action making an ally's next action easier |
| **Ground yourself** | `Heal` + WIS | a scene of rest, a trusted person, a hospital, a ritual, a dose |
| **Contact the noösphere** | `Know` + WIS | you reach for what is not in the room |

Grants are banded and narrow: **questions** (*read a situation*, *read a person*, *contact the
noösphere*), **an aspect** (*set up*), **a cancelled temporary Condition** (*ground yourself*).
Nothing grants a modifier, which is what keeps *Set up* from stacking with the WN circumstance band
(−2..+2) or aid (+1).

Two differences from the original draft, both reversible by the author:

1. **`Withdraw` is not a ninth move.** Leaving a scene at a price is the **Concession** rule
   (#689 §4.4), which applies whether or not a move was rolled, so making it a move would give the
   same escape two procedures.
2. **`Read a person` takes the eighth slot** instead of `Withdraw`, because the investigation loop
   needs a person-reading procedure and `Read a situation` does not cover an interrogation.

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
