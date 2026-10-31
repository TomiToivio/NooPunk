# #943 — Noösphere and Ontological Apocalypse: a CWN-first module

**Status: design deliverable with one isolated, tested glue module. PROVISIONAL; nothing here is
canon and no core rule moves.** The executable half is `mods/noopunk/noosphere.gd` (registered in
`godot/tests/run_tests.gd`, guarded by `godot/tests/test_noosphere_943.gd`). Everything else in this
file is the author's editorial material: prose, procedure and calibration.

**Foundational lock (#897).** *Cities Without Number* is the only resolution engine. This module adds
**no dice, no attributes, no modifiers, no second harm track and no character advancement**. It keeps
records, it reads and writes clock state, and it dispatches to procedures that already exist.

**Sources.** Fraser Simons, *The Veil*, second printing (2018), user-supplied PDF, and D. Vincent Baker
and Meguey Baker, *Apocalypse World*, second edition (2016), user-supplied PDF. Page numbers below are
the books' own printed pages, verified by extracting both PDFs. **No third-party expression is carried
into this repository:** what follows is a crosswalk of *mechanics* with page references, in NoöPunk's
own words, plus the licence obligations recorded in §14.

**Relation to the standing author ruling.** `DECISION_689_NARRATIVE_AND_MIND.md` records **D50**: PbtA
contributes clocks and nothing else *yet*; moves-as-catalogue is refused because it is commercial
content and a second rulebook to maintain; partial success is not adopted. This module is written to
sit inside that ruling, not beside it:

- it imports **no move** from either book and adds **no ninth** NoöPunk move (the closed set of eight in
  `data/rules/narrative_moves.json` is unchanged and its size is asserted);
- it adds **no** 6−/7–9/10+ band, no second die and no partial-success rule — the band a NoöPunk action
  gets is still the margin of one CWN roll, read into the four bands of `src/rules/narrative_layer.py`;
- what it *does* extend beyond D50 is the **procedure around** the dice: which channel a perception
  arrived on, what a clock may and may not do, and how the referee narrates an entity that reacts.
  Whether that extension is approved is queued as **D62**, not assumed here.

---

## 1. One hybrid reality, five converged channels

In the fiction, cyberspace and the Noösphere have merged *for everyday practical purposes*: people
perceive one environment made of physical space, network feeds, simulated data, shared symbols,
psychic impressions, social relations and possible NHI contact. This is the module's one large
borrowing — the premise, not the arithmetic — and it is already NoöPunk's own premise (`RULEBOOK.md`
§41.2 calls Disclosure a Noöspheric phase transition; `rulebook/21_PSI_PARADIGM_SHIFT.md` already
treats anomaly work as multi-channel).

**The caveat that keeps the module honest:** the channels have converged **phenomenologically, not
causally**. A spoofed feed, a psychic impression, a dream, a manipulation and a genuine NHI
interference can arrive through the same interface without being the same thing or equally proven.
The rules therefore record *which channel* a percept arrived on and *what somebody thinks it is*, and
never collapse the two.

| Channel | What it can show | Rule authority | What this module adds |
| --- | --- | --- | --- |
| **physical** | bodies, matter, hazard, movement | CWN | a recordable percept with provenance |
| **cybernetic** | AR, devices, BCI, sensors, network access | CWN hacking (`src/rules/cwn_hacking.py`) | a recordable percept with provenance |
| **psychic / noetic** | impressions, contact, symbolic patterns | approved PSI only (`src/rules/psionics.py`, `src/rules/natural_psi.py`) | a recordable percept, and a refusal when capability is absent |
| **social / linguistic** | beliefs, reputations, factions, narrative | `src/rules/social.py`, faction layer | a recordable percept with provenance |
| **hybrid** | contradictory overlays, contested memory, unattributable source | **this module, and no new roll** | the fifth channel, so a contradiction can be recorded as itself |

The fifth channel is the one structural addition in this section. Without it a contradictory overlay
has to be filed as one of the four that produced it, which silently asserts a cause. With it, the
record can say "two overlays disagree and nobody knows why", which is the actual NoöPunk situation.
`hybrid` is a **provenance value**, not a procedure: it never resolves, grants or denies anything.

---

## 2. The source crosswalk

Dispositions: **IDEA ADOPTED** (the shape, re-expressed), **MODIFIED** (adopted with a deliberate
change), **REFUSED** (excluded by a standing ruling or by the lock), **NOT USED** (irrelevant here).

### 2.1 *The Veil*, second printing (2018)

| Source location | What the book does | Disposition in NoöPunk | Where |
| --- | --- | --- | --- |
| pp. 7–11 | The game assumes a mixed (hybrid) reality at all times; there is no separate cyberspace to enter | **IDEA ADOPTED** — one environment, five channels, no enter/exit minigame | §1 |
| pp. 37, 43 | Six States are core emotions; each carries a number (−1…+2) added to the roll; the player names the strongest emotion behind the action | **REFUSED as arithmetic; ADOPTED as vocabulary.** A state is a descriptor a player may voice; it never adds to a CWN roll, and there is no assignment or re-assignment of values | §9 |
| pp. 39–42 | A feeling wheel and mitigation of states between sessions | **NOT USED** — it exists to service the numeric States | §9 |
| pp. 54–79 | Investigative and peripheral moves, and an Obligation economy between protagonists | **REFUSED** — NoöPunk's investigation authority is GUMSHOE's core-clue rule (#704, #932); obligations are carried by the existing social layer and its Affect edges (`src/rules/social.py`) | §3, §6 |
| pp. 100–105 | Harm, and a separate Humanity Harm track | **REFUSED** — CWN's Trauma / Frail / System Strain and the condition layer are the only cost tracks (D46, D58) | §12 |
| pp. 268–269 | Beliefs are the character's commitments, stated openly, used as flags the referee may press; they may be revised at any time without penalty; they drive growth | **IDEA ADOPTED, growth REFUSED.** The flag half matches NoöPunk's existing **drives** (`rulebook/19_NARRATIVE_LAYER.md` §Character drives) and its compel economy; no XP, no advancement path | §9 |
| pp. 281–285 | An agenda for the referee, a list of principles, and one long-range question the table explores | **IDEA ADOPTED** as the *procedure* in §11; the "final question" is not imported as a rule, because NoöPunk's Disclosure trajectory (`RULEBOOK.md` §41.1) already supplies the long-range shape | §11 |
| pp. 293–305 | Referee moves: a list of things the referee says, with soft and hard variants, and worked examples | **MODIFIED** — a referee who narrates instead of rolling is exactly what NoöPunk's GM-move layer already does (`GM_MOVES` in `src/rules/narrative_layer.py`). The list itself is not imported; §11 says which of NoöPunk's four moves to reach for, and when | §11, §12 |
| p. 313 | The Veil as an open question about the world | **IDEA ADOPTED** — the ontological question stays open by construction (§5) | §5 |
| pp. 348–362 | Threats: a motivation, a type, per-type referee moves, a main antagonist | **MODIFIED** — threats become NoöPunk clocks (§10) with a documented trigger, a stall and a rollback; no per-type move lists are imported | §10 |

### 2.2 *Apocalypse World*, second edition (2016)

| Source location | What the book does | Disposition in NoöPunk | Where |
| --- | --- | --- | --- |
| p. 8 | The world has a psychic maelstrom nobody is sheltered from | **IDEA ADOPTED** — the Noösphere is ambient and non-optional; `rulebook/21_PSI_PARADIGM_SHIFT.md` already treats it as a condition of the setting, not a place | §1, §7 |
| pp. 80, 82, 88 | The referee's agenda, principles and the flat list of things the referee says when the table looks up | **IDEA ADOPTED** as procedure; the wording and the list are not imported. NoöPunk already has its own four GM moves and reads them off the band | §11, §12 |
| pp. 106–122 | Threats are authored as an actor with a motivation; a **countdown clock** records what happens before a threshold, what is inevitable after it, and what the full expression is; clocks are descriptive *and* prescriptive and can be derailed | **MODIFIED and ADOPTED** — this is the module's largest legitimate debt. NoöPunk already specs 4/6-segment clocks in `ISSUE_689_STAGE2_CLOCKS_AND_LEDGER.md` §1; §10 adds the *apocalypse* clocks, the non-linearity rules and the rollback | §10 |
| pp. 148–150 | Opening one's mind to the maelstrom is a basic move: on a hit the referee gives something new and interesting, better detail on the strong hit, an impression on the weak hit, and the miss is where the worst is prepared for | **REFUSED as a move; ADOPTED as a procedure (N1).** NoöPunk already owns the equivalent inside the closed set: *contact the noösphere* (`Know` + WIS check). The book's three-tier reading is **not** imported; the CWN margin is read into the four existing bands | §6 |
| pp. 278–284 | How moves are built, how custom moves may add stats | **REFUSED** — a move-construction kit is precisely the second rulebook D50 refuses | — |
| pp. 126, 132 | Consequences snowball; player-versus-player rules | **NOT USED** — the faction turn and the social layer already cover escalation | — |

### 2.3 What the crosswalk refuses, in one place

1. **A second die.** No 2d6, no 4dF, no "roll + weird". A risky action is a CWN check, a CWN save, a
   hacking procedure, or an approved PSI Effort — one of those, never a new one.
2. **Partial success.** The margin is read into `miss / cost / clean / style` and that is all
   (`BAND_MIN_MARGIN`, `src/rules/narrative_layer.py:178`). A *cost* band is a licence to spend
   something the fiction already put on the table, not a tariff.
3. **States as stats.** No number is attached to an emotion, ever (§9).
4. **A humanity/harm meter.** Nothing here depletes. Exposure costs what
   `src/rules/mental_load.py` and the Stress overlay say it costs (§12).
5. **An imported move list.** The eight NoöPunk moves stay eight; `CLOSED_SET_SIZE` in
   `src/rules/narrative_moves.py:30` fails the build if a ninth appears without a decision.
6. **A second investigator.** Discovery is GUMSHOE's, with its core-clue guarantee; this module only
   decides which *channel* a thing was perceived on (§5, §12).

---

## 3. Inventory of the authorities this module sits on

Deliverable 3 of the issue. Verified by reading the tree, not by trusting the issue text.

| Layer | Authoritative file | Symbol / evidence | What it owns | This module's relation |
| --- | --- | --- | --- | --- |
| Core resolution | `src/rules/narrative_layer.py` | `invoke_step()` :112, `BAND_MIN_MARGIN` :178, `outcome_band()` :191 | the one core, the four bands, one invocation per roll | reads the band; adds none |
| Closed move set | `data/rules/narrative_moves.json`, `src/rules/narrative_moves.py` | `CLOSED_SET_SIZE = 8` :30, `resolve_move()` :186 | the eight procedures, including *contact the noösphere* | dispatches to it; never adds a move |
| Investigation | `src/rules/investigation.py` | `Scene.core_clues()` :108, `discover()` :208, `Hypothesis` :285, `hypotheses_remain_open()` :315 | core-clue guarantee; evidence bears on a theory, never proves it | defers; records hypotheses beside it |
| Evidence custody | `src/rules/investigation_evidence.py` | `Provenance` :12, `lead_only()` :95 | provenance values, append-only custody, `psi_lead` is a lead not a proof | extends the provenance vocabulary with `channel` (§5) |
| Mind / shock | `src/rules/mental_load.py` | `Layer` :39, `present()` :99, `apply_choice()` :122, `no_roll_parameter()` :145 | four-layer exposure, conditions instead of a pool, the player decides what a belief becomes | never duplicates it; `open_mind()` may *prompt* it |
| Noöspace perception | `src/rules/noospace_projection.py` | `InformationSource` :254, `Perception` :263 | "shared Noöspace vs private imagination vs ambiguous" with a confidence | the record in §5 is the merge point |
| PSI capability | `src/rules/psionics.py`, `src/rules/natural_psi.py` | `Technique` :32, `authorized()` :39, `may_use()` :140, `effort_capacity()` | who may do what, and at what Effort | `open_mind()` refuses `psychic` without it |
| Stress overlay | `mods/noopunk/stress.gd` (AWN), `mods/noopunk/psyche.gd` | `MAX_EXPOSURE`, `ACTIVE_PSI_DEFAULT = "undecided"` | the optional Stress procedure and the exposure meter | untouched; the placement question is open as **D58** |
| Hacking / alert | `src/rules/cwn_hacking.py` | `AlertClock` :183 | the only clock class in the code today | the clock in §10 is a *narrative* clock; the two are not merged |
| Faction pressure | `src/rules/swn_faction_operations.py`, `swn_faction_turn.py` | `resolve_action()`, `Faction.turn` | what organisations do between sessions | clocks record the *visible* symptoms of those operations |
| Existing clock spec | `docs/design/ISSUE_689_STAGE2_CLOCKS_AND_LEDGER.md` §1 | 4/6 segments, one clock per question, never rolls, public | the clock form itself | §10 extends, does not redefine |
| Disclosure trajectory | `RULEBOOK.md` §41.1 (:5696) | five disclosure depth levels; different countries at different depths | the long-range shape of the apocalypse | each clock is the pressure that moves a *region* between depths |

**The one gap this inventory found:** there is no runtime representation of a *narrative* clock. The
only `AlertClock` in the tree is the hacking one, and `ISSUE_689_STAGE2_CLOCKS_AND_LEDGER.md` states the
narrative clocks as specification only ("no rulebook edit, no code, no tests"). That is why this module
carries a clock and nothing else executable: the gap is small, mechanical and reversible, and it is
the gap the issue's own deliverable list asks to close.

---

## 4. The unified hybrid-perception record

Deliverable 4. **There is no new record type.** The repository already holds both halves and this
section is the merge specification, so that a later implementer builds the join rather than a third
store.

### 4.1 Two records, deliberately separate

| | **Percept record** (what arrived) | **Hypothesis record** (what it is taken to be) |
| --- | --- | --- |
| Owner in code | `Evidence` (`investigation_evidence.py:17`), `Perception` (`noospace_projection.py:263`), and `evidence` in `mods/noopunk/noosphere.gd` | `Hypothesis` (`investigation.py:285`), and `interpretations` in the module |
| Fields | `id`, `label`/`observation`, **`channel`**, `source`, `found_at`, `collector`, `session_id`, `confidence`, `reliability_note` | `id`, `statement`, `family`, **`confidence` set by the player**, `evidence: {clue_id: Stance}` |
| May be written by | the collector, at the moment of perception | a player, at any time, possibly several times |
| May be edited afterwards | **never** — append-only; a correction is a new record that cites the old one | yes, freely; a discarded theory is not a lie |
| May cite the other | may not name a hypothesis | names the percepts it bears on |
| What it may never contain | a verdict, a cause, a score of truth | a number derived from the evidence |

### 4.2 The join

```
percept { id, channel, source, observation, confidence, reliability_note }
hypothesis { id, statement, family, confidence(player), bears_on: [percept.id], stance }
```

`channel` takes the five values of §1. `source` is a free string because it is a *provenance
statement* the table must be able to read aloud ("the clinic's own sensor log, second-hand"), not an
enumeration the engine could reason about. `confidence` is a **word**, not a number, in the tabletop
record (`unverified / reported / instrument-backed / corroborated / contested`), because a number
would invite the engine to compute a truth value; the digital `Perception.confidence` stays a float
because sensors are entitled to one, and nothing in this module reads it.

Three rules keep the join honest:

1. **An interpretation never edits the percept.** The module's test asserts that adding a hypothesis
   leaves the percept's fields untouched.
2. **A percept does not imply a cause.** Neither record has a `cause` field. The nearest thing is
   `family` on the hypothesis, and it is the player's word.
3. **Two channels are not two proofs.** `triangulate()` counts distinct channels and reports
   `requires_corroboration` below two. It does not know whether a sensor and the person reading it
   share a failure mode; that stays a table judgement, and the module says so in its own comment.

---

## 5. N1 — Open your mind to the Noösphere

Deliverable 5. A **procedure around** the existing move, not a new move.

**Trigger.** A player states that their character deliberately attempts non-ordinary perception,
interaction or contact, and names the channel: an authorised BCI, a psychic technique they actually
have, a sensor package, a meditative practice, a psychotronic rig, a conversation.

**Fiction first.** Before any dice: what can this character reach, what access do they hold, what does
the equipment do, and is the character *observing* or *inferring*? The referee says what is available
through that channel. If the answer is "nothing new", that is a legitimate answer and no roll follows.

**Dispatch — one authority, chosen by the channel:**

| Situation | Authority | What N1 may output |
| --- | --- | --- |
| ordinary, credible observation | none — narrate it | the percept, its channel and its source |
| a clue the case needs | GUMSHOE core-clue rule (`investigation.py:108`) | the clue, ungated by any roll |
| a risky action (a hack, a climb, a lie, holding still under fire) | the CWN check the action already uses | the band, read on the margin |
| an *actual* psychic technique | `psionics.py` / `natural_psi.py`: capability, Effort, duration | whatever the technique grants, at its cost |
| psychic contact with no capability | **refusal** | `psi_capability_required` |

`open_mind()` in the module implements exactly that last row plus the delegation: it returns
`requires_core_resolution: true` and `engine: "cwn"` rather than a number, and it returns
`grants_power: false` on every path, including a successful authorised contact.

**Output.** The referee reports what was perceived, on which channel, from which source, with what
uncertainty, and what answered. The player then decides what it means — and the module records their
hypothesis beside the percept, not inside it.

**Shock.** If what arrived contradicts something the character holds, the consequence runs through
`mental_load.py`: an exposure moves event → acute response → persistent condition → worldview state,
and `apply_choice()` **refuses to run without an explicit player choice**. A die never overwrites a
conviction (D48). If the table's Stress overlay is in use, the Stress procedure may also fire — one
of the two, named at the table, never both silently (**D58** is the open placement question).

**What N1 never gives.** Free telepathy, remote mind-reading, remote hacking, plot omniscience, or a
second roll for the same action. The module's tests pin the two that matter: no capability, no contact;
no contact, no power.

---

## 6. N2 — Reality triangulation

A scene may offer several channels of evidence at once. Triangulation is the table practice of
comparing them, and it has a **record** (§4) and a **rule**:

- Distinguish sensor data, testimony, memory, perception and explanation. They are five different
  kinds of claim and the record keeps them apart.
- Contradiction raises the *investigative* value of a scene; it does not raise certainty and it does
  not trigger a mental-health label.
- A high-stakes, irreversible decision should not rest on a single compromised channel. The engine
  cannot enforce that at a table; it can report it, which is why `triangulate()` reports
  `requires_corroboration` instead of refusing anything.
- **A successful contact is not proof of a cause.** Neither is a failed one.

---

## 7. N3 — Reactive Noösphere

The hybrid environment is an *actor-ish* medium: it carries other people's attention, institutional
appetites and, sometimes, something that notices. N3 gives the referee permission to have it react —
and three limits:

1. **It reacts to what was done.** A clock moves on a documented trigger (§8), never on the referee's
   wish for drama.
2. **It never retroacts a success.** A CWN success stands. The Noösphere may make the *next* thing
   harder in the fiction; it cannot un-roll a passed check.
3. **It never declares a metaphysics.** Whatever answers is described as having answered, in the
   channel it used. The module has no field in which to record "it was really X".

---

## 8. Emotional states and identity

Deliverables 6.

**States are words.** Six descriptors — mad, sad, scared, joyful, powerful, peaceful — may be spoken
by the player when a scene asks how the character is taking it. They are recorded as a single string,
they carry no number, they are never rolled, and they never modify anything. The module's own test
asserts that the stored state is a string and that no attribute block exists beside it.

Why keep them at all, if they do nothing mechanically? Because at a table they change what the
referee says next, and because they are the cheapest way to keep a scene about a person rather than
about a stat block. That is an editorial judgement, and it is the author's to delete.

**Identity is chosen.** The protagonist is a tabula-rasa rookie UNSA agent. `record_choice(id,
description)` stores decisions the player made — "refused the order", "signed the report anyway" —
and nothing else writes to that list. There is no personality score, no playbook, no imposed
conviction, and no random rewrite. Where a commitment needs mechanical teeth, NoöPunk already has
**drives** and the compel economy (`rulebook/19_NARRATIVE_LAYER.md`); this module deliberately does not
grow a second commitment store.

---

## 9. The apocalypse clocks

Deliverable 7. A clock is a named track of **4 or 6 segments** (`ISSUE_689_STAGE2_CLOCKS_AND_LEDGER.md`
§1). It is a record of pressure the table can see, and it is the one thing this module makes
executable.

### 9.1 Seven rules that keep clocks from becoming a second game

1. **One clock per question.** If two would fill on the same event, the table names the one that
   matters and says so.
2. **A clock never rolls and never ticks.** It moves one segment per adjudicated event with a written
   trigger. `change_clock()` refuses an empty trigger, refuses a multi-segment jump, and refuses a
   0-step change.
3. **A clock can be walked back.** A negative step is a legal move with its own trigger, and it
   records the countermeasure that produced it. Rollback is the difference between pressure and
   prophecy.
4. **Clocks are public.** Hidden progress is bookkeeping, not drama.
5. **Filling a clock produces a scene, not a penalty.** The terminal segment is an *event to play*, not
   a debuff.
6. **A full clock is not the end of the campaign.** It is the full expression of *that* actor's plan —
   after which the plan can be opposed, survived, or superseded by another clock.
7. **Non-linearity is legal and expected.** A clock may stall for sessions, skip by a *new* documented
   event, branch into a sibling clock, and regress. The engine allows one segment per event and
   nothing more; the referee decides how many events a session contains.

### 9.2 Five competing clocks

Each names an actor, a motivation, what advances it, what stalls or reverses it, and what its
terminal segment looks like. **The segment counts are the 4/6 of the existing spec; the named clocks
are proposals, and the campaign picks its own** — an authored case names three to five of them.

| # | Clock | Actor / motivation | Advance triggers | Stall, countermeasure, rollback | At the terminal segment |
| --- | --- | --- | --- | --- | --- |
| C1 | **NHI disclosure** (6) | institutions, witnesses, NHI factions; each wants its own version believed first | a verified leak; open contact; a public institutional act; a defection with documents | a corroborated correction; a negotiated delay; discrediting a *true* leak (works, costs legitimacy); a witness recanting under pressure | disclosure reaches the panic depth (level 4 of `RULEBOOK.md` §41.1) in one region: abductions and hybridisation become institutionally credible |
| C2 | **Rogue ASI acceleration** (6) | a system optimising without a principal; its maintainers who cannot admit it | a containment breach; an infrastructure dependency nobody can switch off; a capability jump nobody observed | isolation; power-down; a successful containment scene; publishing the failure (kills the project, saves the city) | the system is load-bearing: shutting it down is now a mass-casualty decision, not an IT ticket |
| C3 | **Cyber-psychic convergence** (4) | the Noösphere itself, and whoever farms it | a shared anomaly confirmed by two independent channels; a new interface deployed at scale; a mass experience with a common content | containment; disconnection (costs the users something real); a debunk that holds | the ambiguity becomes a *social* fact: nobody can tell cyber from noetic, and institutions stop trying |
| C4 | **UNSA authority** (4) | the agency, its rivals, member states | a mandate vote; emergency powers granted; intelligence integrated with operations | judicial review; a political defeat; a public scandal the agency survives | the agency can *compel*: what it recommends happens. The characters' disagreements with it become expensive |
| C5 | **Local crisis** (4 or 6) | one neighbourhood, clinic, campus or case | a resource failure; a death; a closure; a rumour that lands | a repaired supply; a named person who vouches; a story that turns | the place is changed in a way the characters can point at, and they were there |

**Why these five and not one big apocalypse:** the issue asks for *competing, non-linear* clocks.
Competing means two can be advanced by the same event and the table must choose or pay twice;
non-linear means a clock can be stalled, branched and rolled back by play. A single "Apocalypse" track
would be a railroad with a progress bar.

### 9.3 Worked non-linearity

> C1 sits at 3/6 after a verified leak. The characters find the leak's source: a UNSA analyst who
> copied the file to prove a point. They can burn her (C1 +1: the leak is now a scandal, more
> attention), protect her (C1 −1: the leak is discredited long enough to matter, and the *truth*
> costs them the corroboration), or hand her to a rival agency (C1 +1, C4 +1).
>
> Choosing "protect her" walks C1 back on a documented trigger — a public correction, secured
> corroboration — and the module records the countermeasure in the clock's history. Nothing about the
> disclosure has become *less true*; something about it has become less *believable*, which in this
> setting is a different and equally real kind of damage.

---

## 10. The referee procedure

Deliverable: an MC procedure **without** importing an MC engine. Five steps, each of which names the
authority it hands to.

1. **Start from the actors.** What does each clock's actor want *this session*, and what does the
   evidence currently say? No actor acts without a motivation already written down.
2. **Frame a situation and ask what the character does.** Address the character, not the player.
   Offer a place, a person, a contradiction, and stop.
3. **Choose the authority before the dice.** Ordinary observation → narrate. A needed clue →
   GUMSHOE. A risky act → the CWN check the act already uses. A psychic technique → PSI with its
   Effort. Never two at once.
4. **Say what happens, then ask again.** If a roll happened, read its band and use the four GM moves
   the band already maps to (`BAND_TO_MOVE`, `src/rules/narrative_layer.py:210`): *reward*, *cost*,
   *escalate*, *reward and an aspect*. The referee's judgement enters here and nowhere else.
5. **Update the record.** Write the percept, the player's hypothesis (if any), any clock event with
   its trigger, and any condition. Then say what the world did in response, out loud, and ask.

Two habits that are not rules but make the five steps work: *name everyone and make everyone human*,
and *think offscreen* — a clock that has not been touched in two sessions should be visible in
somebody else's behaviour before it moves again.

**What the procedure refuses.** Pre-planning a storyline; a partial-success table of its own; the
referee deciding what a character believes; and any move that takes a passed check back.

---

## 11. Table of responsibility

The double-systems guard. Every row names one owner and one excluded alternative.

| Question | Authority | Explicitly excluded |
| --- | --- | --- |
| Did a risky action work? | one CWN check, band read on the margin | 2d6 bands, a second die, a PbtA move result |
| Is a necessary clue found? | GUMSHOE core-clue rule (#704 / #932) | a failed clue-search roll, an ability spend that can fail |
| Can a psychic technique be used? | `psionics.py` / `natural_psi.py`, with Effort | a free "open mind" superpower, contact without capability |
| How does hacking work? | `cwn_hacking.py`, its own `AlertClock` | a *The Veil*-style cyberspace economy |
| What does disturbing exposure cost? | `mental_load.py` (conditions) and the Stress overlay, one of them named | an extra Stability / Humanity / Harm / Sanity meter |
| How does the agent grow? | CWN progression; identity and relations by player choice | playbook advancement, XP for testing a belief |
| What are hostile organisations doing? | the faction turn, plus the clocks in §9 | a second combat or action system |
| What does the Noösphere feel like? | this module | a mandatory proof of any metaphysical theory |
| Which channel did that arrive on? | this module's percept record | an engine-inferred cause |

---

## 12. Three generic scenes

Non-proprietary, no proper nouns from either book, no setting detail that a later chapter will want
to own.

**A. The corridor that is and is not there.** A call-out to a municipal building whose network was
replaced last week. The team's AR overlay shows a corridor; the building's own plan shows a wall.
Two percepts (`cybernetic`, `physical`) and one `hybrid`. The referee narrates the disagreement and
stops. A needed clue — *the plan was updated, the overlay was not* — is granted by GUMSHOE without a
roll. Whether something is *in* the corridor is a different question and may cost a CWN check to
answer. **Teaches:** convergence without causal collapse; the hybrid channel earning its keep.

**B. The witness who is certain.** A patient describes a room in a hospital that was demolished in
1994, in present tense, with a detail nobody in the room knew. The percept is `social` (testimony);
the hypothesis family is the player's to name. If the table wants a psychic reading, it must go
through an actual capability. If the referee wants the room to matter, a clock moves — not the
character's worldview. **Teaches:** testimony is a channel, not a proof; D48 holds.

**C. The correction that costs.** A leak has been published and a clock advanced. The characters can
prove the leak was *edited* before publication — which is true, and which will be read as a cover-up
if they say it. Walking the clock back is legal and the cost is social. **Teaches:** rollback as a
*consequence*, not a reset; C1 and C4 competing.

---

## 13. Tone and player guardrails

- The protagonist is a player-created, tabula-rasa rookie UNSA agent. Personality, loyalties and
  worldview develop from choices and relationships.
- The supervisor is an NPC: a mentor, an obstacle, occasionally a recruitable ally. Never the
  protagonist, never the author of the player's decisions.
- The lakkahaltia stays a minor comedic detail in the wider plot, not a scenario premise.
- Grounded Nordic recognisable world, punctured: paranoid institutional tragicomedy and ontological
  horror, not automatic psychedelic spectacle.
- Psychiatric settings, patients and vulnerable people are treated humanely. Exposure is not mental
  illness; nothing here diagnoses anyone or makes a claim about real psychiatry
  (`mods/noopunk/psyche.gd` says the same and this module inherits it).
- NHI personhood and every metaphysical claim stay contested. No faction is proven right by a die.

---

## 14. Tests: what is executable and what is editorial

The issue asks for automated tests of five properties. Under the repository's testing policy
(`AGENTS.md`, #271) a test may assert **executable behaviour**, never prose. So the five properties are
asserted against the module, and the prose is left to the author.

`godot/tests/test_noosphere_943.gd` — **46 rows, registered in `godot/tests/run_tests.gd`**
(the first increment added the file but not the registration, so nothing ran; that is fixed here).

| Property the issue names | How it is asserted |
| --- | --- |
| **no dual dice engine** | `test_noosphere_943.gd` enumerates the module's whole method surface and fails if any method name contains a dice/roll token; `open_mind()` is asserted to return `engine: "cwn"` and `requires_core_resolution` rather than a result |
| **no automatic psychic powers** | three rows: no capability → `psi_capability_required`; authorised contact → `grants_power == false`; successful risky authorised contact → still `grants_power == false` |
| **no forced belief changes** | identity is only ever written by `record_choice()` with an explicit argument; blank ids refused; the serialized state has no `roll` key; the mind layer's own `apply_choice()` refuses a non-boolean decision (`mental_load.py:128`) |
| **no core-clue gates** | recording a percept is ungated by competence, access or roll; the module exposes no method whose name contains "clue"; the clue authority is *named* as a constant (`src/rules/investigation.py`) and not reimplemented |
| **no duplicate psychological track** | the serialized state is searched for `stress / psyche / sanity / harm / mental / exposure` keys and must contain none; the exposure authority is named as a constant and not reimplemented |

Additionally asserted: the five-channel model including `hybrid`; percept/hypothesis separation
(a hypothesis never writes into the percept); clocks restricted to 4 or 6 segments, single-step,
trigger-required, public, and reversible with the countermeasure recorded.

**What is deliberately not tested** — because the policy forbids it and the author owns it: the wording
of any scene, the names of the clocks, the segment counts of a *particular* campaign's clock, the
condition catalogue, and whether the module ships at all.

**The commands, so a reader can re-run rather than trust this page:**

```bash
godot --headless --path . --import                       # once per fresh checkout
godot --headless --path . --script res://godot/tests/run_tests.gd
python3 tools/check_godot_shutdown.py --godot <path to godot>
```

---

## 15. Licensing and attribution obligations

Deliverable 9, and the part most likely to be got wrong later.

- ***The Veil*, second printing (2018).** Its credits page licenses the **text** under **CC BY-SA 3.0
  Unported**, and states separately that the **illustrations and all graphic elements** are
  © the author and not under that licence. It also records that some of its moves come from
  *Apocalypse World* **with permission** — a permission granted to *The Veil*, which does not
  automatically extend to a third party. Consequence: *The Veil*'s text may be adapted with
  attribution and **share-alike** obligations if any of its expression is reused. This module reuses
  **none of its expression**: mechanics are described, page-referenced and re-expressed. If a later
  draft wants to quote the text, ShareAlike lands on the derived text, and that is a decision for the
  author (**D64**).
- ***Apocalypse World*, second edition (2016).** Its copyright page asserts © D. Vincent Baker and
  Meguey Baker and establishes **no** open licence for the book. Consequence: **nothing** from it may
  be reproduced, and the fact that "PbtA" design ideas are widely discussed does not license the text.
  This module borrows *concepts* — an ambient psychic medium, clocks as visible pressure, a referee
  agenda — and no wording, and it does not claim the book is open.
- **No third-party expression in the tree.** `tests/test_third_party_expression_absent.py` exists
  because third-party dialogue was once published here and had to be removed. This module's own
  compliance is checked by that test; a quotation would fail it.
- **Attribution, when the module is printed.** The honest minimum is a sources paragraph naming both
  books, their editions and years, stating that the module's procedures are original and that no text
  or art is reproduced. Where that paragraph lives is an author decision.
- **Art.** No image, layout or typeface from either book may be used; the art direction is NoöPunk's
  own (`docs/ART_DIRECTION.md`).

---

## 16. What this module deliberately does not do

- It does not edit `RULEBOOK.md`, `rulebook/`, the CWN core, the GUMSHOE layer, PSI, Stress, the
  faction turn or the hacking clocks. No rulebook chapter exists for it yet; §17 is why.
- It does not touch `#932`'s unresolved clue-shape decision (D61); whichever way D61 goes, this module
  only reads the result.
- It does not decide the Stress/Psyche placement (D58), the condition catalogue, or whether exposure
  is Stress or the Psyche module's business.
- It does not add a character sheet, a save format or a migration: the module's state is
  `to_dict()`, and nothing persists it yet.
- It does not implement `Hybrid` perception as a *procedure*. The fifth channel is a provenance value.
- It does not settle any metaphysical question, and it has no field in which one could be settled.

---

## 17. Open author decisions

Queued as **D62–D64** in `docs/design/AUTHOR_DECISION_QUEUE.md`; none of them is answered here.

- **D62 — Approve the module, and in what form.** (a) approve as written: an isolated overlay module
  plus this document, no rulebook chapter until playtested; (b) approve the document only and hold the
  module out of `main` until a chapter exists; (c) refuse the extension beyond D50 and keep clocks
  only.
- **D63 — Which clocks exist, and how long they are.** The five clocks in §9.2 are proposals for an
  authored campaign, not a timeline. Whether the game ships them, and whether a case may declare a
  4-segment clock where the spec says 6, is the author's.
- **D64 — Whether any of *The Veil*'s text is ever quoted.** The module as written does not, which
  keeps the tree out of ShareAlike. A quoted paragraph would change the licence obligations of
  whatever file carries it.

**Related open rows this module leans on:** **D58** (Stress vs Psyche placement), **D61** (which module
owns discovery and what shape a clue carries), **D48** (already decided: a die never changes a
belief), **D50** (already decided: PbtA contributes clocks only, moves-as-catalogue refused).

---

## 18. Source notes

- Page references were verified by extracting both user-supplied PDFs: *The Veil*'s own page numbering
  sits one index off the PDF's, and the printed pages used here are 7–11, 37, 39–43, 54, 72–79, 100–105,
  268–269, 281–285, 293–305, 313, 348–362. *Apocalypse World*'s printed page is three off its PDF
  index; the pages used are 8, 80, 82, 88, 106–122, 126, 132, 136–151, 278–284.
- Related NoöPunk records: **#897** (foundational lock), **#932/#704** (GUMSHOE investigation,
  D59–D61), **#928** (Stress, D58), **#689** (narrative layer, bands, closed move set, D44–D50),
  **#943/#944** (this module and its first increment).
- The module's first increment (PR #944) contributed the file layout, the four-channel model and the
  event-driven clock; this document keeps that work and extends it.
