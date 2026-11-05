# Scene types: what exists, what is proposed, and why (#1178)

> **Status: proposal for author decision.** Five scene kinds are implemented in `src/world/scenes.py`
> and refused/accepted by the `Scene` record: **Social, Investigation, Exploration, Action, Cyber.**
> **Astral** is deferred by decision (#1178 §2). This document answers the open question: do we need
> **Interrogation**, **Data Collection** and **Data Analysis** scenes, and should GUMSHOE shape the
> investigation mechanics?

## 0. The test every proposed kind must pass

A new scene kind is only worth adding if it needs a **different contract**: a different set of graphs,
a different tag requirement, or a different resolution path. If it is a *tone* of an existing kind, it
is a scene, not a kind. That rule exists because the alternative is six scene systems that each
half-work, which is exactly the "outdated complex version" this repository is moving away from.

| Proposed kind | Needs a different contract? | Verdict |
| --- | --- | --- |
| **Interrogation** | No — it is Social + Investigation with a Clue pressure loop | **A mode, not a kind** |
| **Data Collection** | Yes — Cyber + Social, and it consumes the city's surveillance layer | **Add as a kind** |
| **Data Analysis** | Yes — no location, no participants in the physical sense; the graph *is* the play | **Add as a kind** |
| **Astral** | Yes — different topology, different rules | Deferred (#1178 §2) |

## 1. Interrogation — a mode, not a kind

*Silicon Dreams* is the reference Tomi named: an interrogation where the pressure is knowing what the
subject is hiding, and where the interface is a conversation with a machine that reads stress. What
makes it work is not a new subsystem; it is that **every question is a bet against evidence you
already hold**.

That is precisely what `Social` + `Investigation` already do here:

- a **Social scene** supplies the room, the participants and the negotiation (CWN Talk/Connect);
- **Clue tags** supply the leverage, because a contradiction is a fact with provenance;
- **Personality tags** supply the read — "guarded", "procedural", "breaking" — which is what an
  interrogator actually exploits;
- and the failure consequence is **time and heat**, not information: the subject lawyers up, the
  shift ends, the supervisor asks why you are still in that room.

Adding a sixth kind would create a second social resolver with its own modifiers, which the
architecture forbids ("an interface never invents a mechanic", #1184). **Recommendation:**
`Interrogation` becomes a named *scenario template* — `Social` scene whose tag requirement includes at
least one contradiction pair — documented as a worked example, with no new contract. If the graphical
client wants an `INTERVIEW` app, that app renders a Social scene, not a new kind.

**Concretely, the loop:** present a Clue tag → the subject must either explain it (a new claim, i.e. a
new `claimed` clue) or contradict an existing one (a registered contradiction). A CWN Talk or Connect
check decides cost and consequence. No stress meter: `pressure` on the personality tag is set by the
author, and the GM narrates it.

## 2. Data Collection — add as a kind

*Orwell* is the reference: not "solve the murder", but "watch the city's feed and decide what matters".
NoöPunk already has the three inputs this needs, and none of them is a physical scene:

| Channel | Where it lives | What it produces |
| --- | --- | --- |
| **OSINT** | public records, media, dossiers, breach data | `claimed` clues with public provenance |
| **Panopticon** | Europol's surveillance layer: camera feeds, movement logs, device telemetry — the **Cyber** graph made social | `observed`-*appearing* clues whose provenance is institutional, not personal |
| **HUMINT** | informants: Social graph + Social tags (`relation: informant`) | `claimed` clues with a fragile `source_ref` that can be burned |

**Why it is its own kind:** it is played entirely on the Cyber and Social graphs with *no physical
presence of the investigator*, its currency is time and authorisation rather than hit points, and its
characteristic failure is not "you missed the clue" but **"you collected it in a way that cannot be
used"**. That last point is the whole ethical engine: Panopticon access is logged, and a clue obtained
by an unauthorised query is a clue the prosecutor will not touch.

**Contract sketch:**

- uses: `cyber`, `social`; references physical places only through device location
- requires: nothing mandatory, but a scene with no `clue` tag out is a wasted scene
- resolution: CWN `Program` (records/breach), `Connect` (informants), `Know` (institutional knowledge),
  `Notice` (feed triage), `Administer` (authorisation)
- produces: `claimed` or `observed` clues, **never** `hypothesis`
- refuses: no surveillance minigame, no "hack the mainframe" ladder, no point economy, and no
  consequence-free watching — every Panopticon scene writes a log entry the story graph can use later

## 3. Data Analysis — add as a kind

This is the case-board scene, and it is the one the interface plan already assumes: **almost
everything is a graph**. The player is not rolling to have an idea; the player is *assembling* the
graph — linking clue tags into a hypothesis, spotting a contradiction, and deciding which link is
worth taking to a prosecutor.

**Why it is a distinct kind:** it has no location, no participants in the physical sense, and its
subject matter is the *player's own collected knowledge*. It is also the only scene kind that can fail
without the world changing: an analysis that leads nowhere costs the shift, not the case.

**Contract sketch:**

- uses: `story` (the case), plus whatever graphs the clues reference
- requires: at least one `clue` tag, and at least two for a meaningful scene
- resolution: **no roll to solve.** CWN `Know`/`Program` may be rolled to *notice that two facts cannot
  both be true* — the idea itself comes from the player. When a hypothesis is filed, a CWN check
  (typically `Administer` or `Connect`) decides whether the institution accepts it, which is the
  procedural risk, not the intellectual one.
- produces: `hypothesis` clues, which are explicitly the weakest register, and a `GoalTag` update
  ("close the case" moves to `met` only after a Data Analysis scene names the offender)
- refuses: no point economy, no "connect-the-pipes" minigame with one solution, no gating of the plot
  behind a puzzle the player cannot see

## 4. GUMSHOE: what to borrow, what to refuse

GUMSHOE (Robin D. Laws, Pelgrane Press) is the right *structural* reference for investigation and the
wrong *economic* one for this game. Quoted principles are paraphrased, not reproduced; the SRD and the
published games remain the authority.

**Borrow:**

1. **Core clues are never gated behind a roll.** If the case cannot proceed without it, the players
   find it; the roll decides time, cost, noise or an extra detail. Our `Investigation` contract already
   says this, and it is now enforced by `validate_scene` requiring a `core` clue.
2. **Investigative abilities are ways of asking, not gates.** GUMSHOE's ability list is a good
   vocabulary for what a clue-hunting character *does*: search, research, surveillance, interrogation,
   data retrieval, cryptography, forensic accounting, streetwise. Mapped onto CWN skills, this becomes
   the `resolution` tuple in each contract — no new skill list.
3. **The question is "what does it cost", not "do you succeed".** GUMSHOE's best idea is that
   information is cheap and consequences are expensive. Our registers (observed / claimed / disputed /
   hypothesis) and the Panopticon log are the same idea in a different currency.
4. **Prepared clues per scene.** A scene should know, before play, which clues it can yield — that is
   what makes "core clues" checkable in code.

**Refuse:**

- **point pools and spends** (Investigation points, General ability spends) — a second economy
  competing with CWN's skills, and explicitly ruled out by #1184 ("no investigation-point economy");
- **a parallel skill list** — CWN's skills are the immutable baseline;
- **"spend to be right"** — the player's reasoning, not a resource, decides the case;
- **the guarantee** that a failed roll always yields a clue: CWN's failure states are real, and the
  contract's job is only to keep the *case* alive, not to make every attempt succeed.

## 5. Recommendation

| Kind | Status | Why |
| --- | --- | --- |
| Social, Investigation, Exploration, Action, Cyber | **implemented** | contracts in `src/world/scenes.py` |
| **Data Collection** | **add** | distinct graphs (cyber+social), distinct failure ("unusable evidence"), distinct ethical engine |
| **Data Analysis** | **add** | the case-board scene; no location; the only kind that can fail without the world moving |
| Interrogation | **mode of Social** | Silicon Dreams-style pressure is a clue/personality loop, not a new resolver |
| Astral | deferred | #1178 §2 — scripted projection first, graph later |

If both additions are approved, `IMPLEMENTED_SCENE_KINDS` becomes seven, and the interface plan's app
map stays unchanged: Data Collection renders in `OSINT` and `TERMINAL`, Data Analysis in `CASE`, an
Interrogation mode in `INTERVIEW`.

## 6. Decisions needed from the author

1. Approve **Data Collection** and **Data Analysis** as scene kinds (and therefore as contracts), or
   fold them into Investigation as modes.
2. Confirm **Interrogation stays a mode** — or name the mechanic that a Social scene cannot express.
3. Whether a Panopticon clue obtained without authorisation should be **refused by the prosecutor**
   (a hard mechanical consequence) or merely **cost Heat** (a softer one). This is the one decision
   that changes what the game is about.
