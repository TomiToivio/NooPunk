# #704 — the GUMSHOE-inspired investigation procedure

**Status:** design proposal for author review. Speaks **baseline v1** (2d6 + modifier + skill, CWN six
attributes). Adds no new attribute, no new die and no new ability score.

This document answers the research task #704 names: *should a character with the right competency who
performs the relevant inquiry automatically discover essential clues, while CWN rolls still adjudicate
danger, time, quality, resistance, costs and complications?* **It should, and the division can be made
sharp enough to implement.**

---

## 1. What the GUMSHOE SRD actually says

Read from the CC version dated 2024-12-09. Cited so each claim is checkable; **no SRD prose is copied
into NoöPunk**.

**Gathering clues (SRD p. 50).** Three conditions must hold: (1) get into a scene where relevant
information can be gathered, (2) have the right ability, (3) tell the referee you are using it. If all
three hold, *"you will never fail to gain a piece of necessary information. It is never dependent on a
die roll. If you ask for it, you will get it."*

**Core clues.** For each scene the referee designates the clue needed to reach the next scene. The
designated ability is *"just one possibility, not a straight jacket"* — if players propose another
plausible method, the information is given anyway. Passive clues are handed out without prompting when
the group is stuck.

**Special benefits.** Extra value from a clue is bought by spending points from the relevant
investigative pool — never for the core fact itself.

**Ratings versus pools.** The rating is static; the pool starts each case equal to the rating and is
spent down. General abilities refresh to rating at the start of a scenario; partial refreshes exist.

**General abilities.** Roll one d6 against a Difficulty Number (usually 4); each point spent adds 1 to
the roll.

**Why this design exists.** A failed "find the clue" roll stalls the plot and teaches players to stop
engaging; the SRD's own answer is that *failure belongs in the risky, contested, physical parts of the
story*, not in the reading of evidence.

## 2. The adaptation: **no roll to find, roll to explain**

NoöPunk keeps CWN resolution for everything dangerous, contested or costly, and removes the die from
one place only: **acquiring a clue you are competent to acquire.**

| question | who answers it | die? |
|---|---|---|
| Is there a clue here, and can I reach it? | scene access — CWN checks for stealth, entry, warrants, danger | **yes** |
| Do I have the competency? | skill rating | no |
| Do I get the core fact? | **guaranteed** | **no** |
| What else do I get? | investigative **spend** | no |
| What does it *mean*? | CWN skill check vs difficulty | **yes** |
| Do I believe my own reading? | the evidence, later | — |
| What does acting on it cost? | CWN consequences | yes |

This is the whole of the borrowing. Everything else in NoöPunk stays CWN.

### 2.1 The three conditions, in NoöPunk terms

1. **Access** — the character is in the scene and able to examine it. Getting there may have cost
   something (a Sneak check, a warrant, a favour, a bribe, a psychic risk).
2. **Competency** — the character has the relevant skill at a rating that covers the method. Untrained
   use (`untrained_modifier`) does **not** trigger the guarantee: you may still try, and then it is an
   ordinary check with ordinary failure.
3. **Declaration** — the player says what they are doing and how. *"I run the ward's access logs
   against the duty roster for the missing four hours"* is a declaration; *"I investigate"* is not.

### 2.2 Three grades of clue

| grade | guaranteed? | what it does | example |
|---|---|---|---|
| **core** | **yes**, if the three conditions hold | opens the next scene; the case cannot dead-end | the duty files are written in the future tense |
| **optional** | no — bought with a spend, or found by a declared extra method | corroborates, shortcuts, or unlocks a *better* ending | the ink is dated nine days before the admission |
| **colour** | free on arrival | atmosphere, motive texture, no mechanical weight | the ward smells of chlorine and old carpet |

### 2.3 No dead ends — an authoring rule, not a referee virtue

Every core clue must be reachable by **at least two** of:

- two different skills (e.g. `Forensics` *or* `Medicine` for a body; `Infosec` *or* `Interface` for a
  log), or
- two different scenes (the same fact obtainable in the ward and again in the archive), or
- one skill plus one **institutional** route (a contact, a warrant, an AI query) that costs something.

A core clue with exactly one path is an authoring defect and should be caught in review, not discovered
when a table stalls. This is the single most important rule in this document.

### 2.4 Spends without a new resource

GUMSHOE's investigative pools do not come across as a new economy. A **spend** in NoöPunk is one of:

- **time** — a scene's worth of work, which advances a pressure clock;
- **a resource** — a favour, a warrant, a consumable, a charge;
- **risk** — a check you would otherwise not have to make (the entry, the trace, the psychic contact);
- **credibility** — a social cost with an institution that will remember.

What a spend buys is always **optional** information: a second reading, a witness, a corroboration, a
shortcut, a name. It never buys the core fact, and it never buys the *truth* of an interpretation.

## 3. The clue is a fact; the reading is a hypothesis

The mechanism that keeps NoöPunk's uncertainty intact: **every clue is written twice.**

A clue record carries:

- **fact** — what is physically/socially/digitally there, stated without interpretation;
- **mundane reading** — the ordinary explanation a competent sceptic would reach;
- **anomalous reading** — the explanation that requires the weird;
- **discriminator** — the test, record or witness that would separate them, *named in advance*.

The guarantee attaches to the **fact**. It never attaches to a reading. A table that finds every fact
and still argues about what they mean is playing the game correctly.

### 3.1 The anomaly gate

A case may not be resolved as anomalous until every discriminator for the anomalous reading has been
**attempted and recorded** — including the ones that failed. "We couldn't think of an ordinary
explanation" is not a discriminator. This is what preserves #704's requirement that *the possibility
that an anomaly has an ordinary explanation* survives contact with play.

### 3.2 The uncertainty ledger

Each hypothesis carries supporting and contradicting clue ids. A hypothesis becomes **actionable** at
two *independent* supporting clues with no unaddressed contradiction; it becomes **closed** only when a
discriminator is resolved against it. Independence matters: two facts from the same document are one
fact wearing two hats.

---

## 4. The procedure at the table

Mapped onto the canonical loop in `docs/design/DEFAULT_INVESTIGATION_FANTASY.md` §9, which already fixes
the order (secure → physical → cyber → social → psychic → compare → hypothesise → test → classify → act
→ preserve).

1. **Frame the scene.** Name the four layers present. State which clues are passive (handed over on
   arrival) and which require declaration.
2. **Declare.** Player names method and target. Referee checks the three conditions.
3. **Fact.** If conditions hold: give the fact, plainly, once. No roll. If they do not hold: say what
   is missing (access, competency or specificity) — never "you find nothing".
4. **Spend, if offered.** Player may pay time/resource/risk/credibility for optional information.
5. **Interpret.** This is where dice live. A `Research`, `Forensics`, `Kinesiology`, `Intelligence
   Analysis` or `Talk` check establishes *which reading holds*, at a difficulty set by how much the
   evidence actually supports it.
6. **Complicate.** On a cost or miss band, the information is still true — but something else moves: a
   clock advances, an institution notices, a suspect learns.
7. **Record.** Update the ledger: clue added, hypotheses re-scored, contradictions noted.
8. **Test.** Run a discriminator. Only a resolved discriminator closes a hypothesis.

**Failure is never "you learn nothing."** Failure means: the reading you reach is incomplete or
overconfident, the cost is paid, or the world reacts. The clue was already yours.

---

## 5. Mystery graph — an example

Nodes are scenes; **bold** edges are core clues (guaranteed once reached); dotted edges are optional
clues that shortcut or enrich.

```
                    [1. Intake]
                         |
                   core: files in future tense
                         |
        +----------------+----------------+
        |                                 |
  [2. Ward office]                  [3. Morgue]
   core: duty roster gap             core: no lividity
        |                                 |
        +--------+--------------+---------+
                 |              |
          [4.Archive]      [5. Chapel]
        core: 1974 admission   optional: the choir's hymn book
                 |              |
                 +------+-------+
                        |
                  [6. Confrontation]
             requires: two independent supports
             and no unaddressed contradiction
```

Each core edge is reachable at least twice: scene 2 by `Infosec` (roster) **or** `Talk` (night nurse);
scene 3 by `Medicine` **or** `Forensics`; scene 4 by `Research` **or** `Administrate` (records request);
scene 5 by `Perceive` **or** `Kinesics`; scene 6 by the ledger, not by a die.

## 6. Worked case — Dr. Inspector Romppainen and the Lakkahaltia ward

Setting per the canonical investigation fantasy: UNSA investigator, field partner, controller, embedded
forensic AI, four analytical layers. Nothing below is canon; it is a design fixture, and the ward's name
follows the existing Northern Noösphere material.

### 6.1 The situation

Four admissions in eleven days at Lakkahaltia psychiatric hospital. One patient is dead. The duty files
for the last four admissions are written in the **future tense**; one describes what Romppainen will do
tomorrow.

### 6.2 Clue table

| # | scene | fact (guaranteed) | mundane reading | anomalous reading | discriminator |
|---|---|---|---|---|---|
| C1 | intake | four files use future tense | a documentation template bug, or a clerk writing prospective care plans | the files describe events before they occur | compare file timestamps to the hospital's template version history |
| C2 | ward office | duty roster has a four-hour gap for the night of the death | shift swap never logged | someone was present who is not on any roster | interview the night nurse; check door controller logs |
| C3 | morgue | body shows no lividity | position at death, or post-mortem movement | the body was placed, not found | `Medicine` check; ambient temperature log |
| C4 | archive | a 1974 admission with the same name and the same handwriting | a family name reused; a clerk's hand resembling another's | recurrence across fifty years | handwriting analysis; personnel file of the 1974 clerk |
| C5 | chapel | hymn book has a date nine days in the future | someone wrote the wrong date | a document from after the event | compare ink age by `Forensics`; check who holds the key |

### 6.3 The two hypotheses, both live

**H1 (mundane).** A records clerk with a prospective-care template, a genuine roster gap caused by an
unlogged swap, and a body moved after death by staff following an old protocol. Every fact has an
ordinary explanation; the "future tense" is a template artefact.

**H2 (anomalous).** The ward's documentation is precognitive, the 1974 file is the same document
recurring, and the death was known before it happened.

They are **not** distinguished by the facts — both explain C1–C5. They are distinguished by C1's
template-history check and C3's lividity test. Until those run, the ledger keeps both actionable and the
table can act only on what is common to both (protect the remaining patients, secure the files).

That is the design working as intended: **clues are guaranteed, truth is not.**

### 6.4 What the layers contribute

- **Physical** — C3, C5 (ink, body, room).
- **Cybernetic** — C1 (template version history), C2 (door controller logs, roster export).
- **Social** — C2 (night nurse), C4 (personnel file), institutional resistance from the hospital.
- **Psychic** — a `Telepathy` or `Precognition` probe is a **clue source**, never a verdict: it may
  produce a *new fact* (C1 corroborated by a second observer), and it may produce a *reading* that is
  indistinguishable from H1's. It cannot close the anomaly gate on its own.

### 6.5 A play transcript in miniature

> **Player:** I pull the template history for the admission forms — version, deployment date, who can
> edit. `Infosec`, I have it trained.
> **Referee:** Access is fine, competency is fine, declaration is specific. Fact: the future-tense
> template was deployed to this ward **six weeks after** the earliest of the four files. No roll.
> **Player:** Then the files were written against a template that did not exist yet. That's C1's
> discriminator, and it points at H2.
> **Referee:** It points. It doesn't close: the roll for the *reading* is `Research` at Difficult,
> because one deployment record is one document. Take the check, and we'll see whether you also notice
> that the deployment was rolled back — which is a contradiction you will have to address.

Note what happened: the **fact** was free, the **interpretation** cost a check, and the check produced a
complication that keeps H1 alive.

---

## 7. Overlay boundaries (Fate / PbtA)

| overlay | allowed | forbidden |
|---|---|---|
| **Fate aspects** | one invoke per roll; grants a **band**, not a number; compels create cost, not information | an aspect may never *find* a clue or *establish* a reading |
| **PbtA moves** | outcome vocabulary (clean / cost / miss), fronts as pressure clocks, "what do you do?" framing | a move list replacing skill checks; "success with complication" granting facts the scene does not contain |
| **Clocks** | institutional pressure (the hospital's lawyers, the press, the patient's decline) | clocks that secretly contain the solution |

The boundary in one line: **overlays colour the outcome; they never author the world.**

## 8. Psionics, cybernetics and BCI

- **SWN psionics** supplies *sources of clues* and *ways to reach scenes*: telepathy is an interview
  method, precognition is an evidence stream with its own reliability problems, psychometry is a
  forensic method on an object.
- **Effort** is spent inside the existing economy; psionics adds no second resolution die and no second
  difficulty ladder.
- **Cybernetics** contributes `Infosec`/`Interface` methods and device statistics (COMPUTE / INTERFACE /
  NETWORK are properties of hardware, not attributes — see the crosswalk).
- **BCI** is a *forensic surface*: neural logs are evidence like any other, with the same guarantee for
  the fact and the same checks for the reading.
- **Consent and personhood** stay live questions (the canonical fantasy's §6): a telepathic reading of a
  patient is evidence *and* an ethical act with consequences.

## 9. Verification plan

| criterion | how |
|---|---|
| core clues never dead-end | authoring lint: every core clue has ≥2 paths (implemented in `src/rules/investigation.py`, tested) |
| finding is free, interpretation is not | unit tests over the procedure model |
| mundane explanation survives | anomaly gate: resolution requires every discriminator attempted |
| tabletop | one session, three scenes, two referees; measure: minutes to first core clue, rolls spent on finding vs interpreting, whether both hypotheses stayed live |
| Godot | regression on existing tests; no engine change proposed here |
| migration | none — this layer reads skills by name and does not touch `core.json` |

## 10. Follow-ups this proposal implies

1. Migrate `core.json` to baseline v1 (2d6, CWN six, skill list) — blocks every later numeric module.
2. Implement the investigation runtime in Godot once the tabletop procedure has one playtest.
3. SWN psionic disciplines as clue-sources (needs the SWN licence question settled first).
4. A second worked case where the **mundane** reading is true, so the anomaly gate is exercised in the
   other direction — a design that only ever confirms the weird is not preserving uncertainty.
