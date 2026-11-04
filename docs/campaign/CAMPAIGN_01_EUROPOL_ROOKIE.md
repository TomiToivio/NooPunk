# Campaign 01 — *The Rookie, the Awakening and the Wanderer*

**Status: DRAFT — open to revision.** This is a design document for the first NoöPunk single-player campaign,
written to issue [#1132](https://github.com/TomiToivio/NooPunk/issues/1132). It is **not** rules code, not a
finished scenario, and not a commitment that every mechanic described here will be built.

Read the labels literally:

| Label | Meaning |
|---|---|
| **CANON** | Established elsewhere in this repository, or authored in #1132; changing it needs the author, not an agent |
| **AUTHOR DECISION** | The author has stated it; quoted or cited |
| **PROPOSAL** | My suggestion, awaiting the author. **Act III as a whole is in this category** |
| **OPEN** | A question nobody has answered yet. Do not resolve it in code |

Everything below that is not labelled should be read as *draft proposal by an agent*, changeable on contact.

**Set in 2045 Helsinki**, in the post-Crisis Cold War status quo described in
[`NHI_CRISIS_921.md`](../world/NHI_CRISIS_921.md) and [`POST_NHI_WORLD_1005.md`](../world/POST_NHI_WORLD_1005.md).
Europol's institutional shape follows [`EUROPOL_HELSINKI_1114.md`](../world/EUROPOL_HELSINKI_1114.md) **and that
document's own warning applies here**: ranks, legal citations and budgets are open author decisions, so this
outline invents none of them.

---

## 1. Logline, premise, themes, tone ramp

**Logline.** A twenty-four-year-old Europol rookie in Helsinki spends a year learning that the institution she
serves is smaller than the world it claims to police — and then discovers her placement in that world was not an
accident, because she volunteered for it before she was born.

**Premise.** The protagonist is a pre-authored young Europol officer: fixed employer, fixed hidden past, fixed
polarization, fixed psychic destiny, fixed final revelation. Everything a player normally controls about *who a
person becomes* — friendships, loyalties, vices, politics, whether they stay a cop — stays open.

**Themes.**

- **Institutional comedy and institutional horror from the same building.** A Europol office that cannot arrest
  anyone is funny until the day it matters.
- **Competence is not virtue.** CWN rewards procedure; the campaign asks what procedure is *for*.
- **Service as a chosen obligation, not a personality trait.** StO is what the protagonist *is*; the game is about
  what she *does* with it.
- **Witness over weapon.** The late campaign is about perception, testimony and consent, not about becoming the
  strongest thing in the room.

**Tone ramp** (CANON from #1132, expressed as a rule for whoever writes scenes):

| Act | Register | Reference | Cosmic content |
|---|---|---|---|
| I | Grounded cyberpunk police procedural, painful/absurd comedy | *Blade Runner* procedure, *Maniac* institutional comedy | **None overt.** Dreams and fragments only |
| II | Conspiracy and ethical rupture, New Weird leaking in | *True Detective* S1 structure, *Annihilation* biology | Anomalies without explanation |
| III | Threshold: the world stops agreeing with itself | *Stalker*, *Arrival* | Astral procedures introduced carefully |
| IV | Cosmic science fantasy, then a personal ending | *Contact*, *Children of Men* for the ending | Confederacy, Time/Space, Higher Self |

**Comedy rule (PROPOSAL, derived from the CANON "human, not relentless parody"):** comedy comes from
**institutions behaving plausibly** — a form that cannot be filed, a jurisdiction that does not exist, a
colleague who has learned to weaponise procedure. Never from the protagonist being stupid, never from cruelty to
civilians, and never as a quip after a death.

---

## 2. Fixed dossier vs player-built identity

### 2.1 FIXED (CANON / AUTHOR DECISION — not editable by play)

| Field | Value |
|---|---|
| Age and standing | 24, first posting, still technically on probation for the campaign's first arc |
| Employer | **Europol**, Helsinki office — the liaison/analysis office, not a national police force |
| Housing | Company housing in **Kurvi**, Kallio. Small, paid for by the office, which is itself a leash |
| Starting kit | Standard Europol officer equipment; basic Europol cybernetic set including **BCI** and a **defensive psychotronic implant** |
| Hidden past | Fixed, authored, revealed through fragments (see §5) |
| Polarization | **Service-to-Others. Fixed. Does not change.** There is no StS route and no polarity meter |
| Final revelation | She is a **Wanderer** who chose a specific StO service before incarnation; the *content* of that service is disclosed only at the ending |
| PSI sequence | Pre-authored in three stages (see §8). **Not a selectable tree** |

**Why fixed:** the campaign's dramatic engine is *discovering what you already are*, not *deciding what you will
become*. If the player could pick Wanderer, the reveal would be a menu choice with a cutscene attached.

### 2.2 OPEN (player-built — the actual game)

- Personality tags and how they constrain action (the repository's tag model: a `Pacifist-2` officer does not
  simply take a −2, they **cannot initiate** combat)
- Relationships: colleagues, neighbours, family, a possible romance, a possible informant
- Professional reputation inside Europol and with Finnish authorities
- Corruption: what she does for convenience in Act I becomes evidence in Act III
- Politics: what she believes about the NHI Crisis, the Quarantine, the EU, and her own institution
- Substance use, dependency and recovery — **consequence, never alignment**
- Whether she stays a Europol officer at all, and what she does when the Confederacy asks her to stop being one

**The line, stated once and meant:** *no lifestyle choice makes her StS.* Addiction, a dirty arrest, a
relationship the service disapproves of, a political position — these change her career, her friends and her
self-understanding, not her density.

### 2.3 Starting sheet (PROPOSAL — numbers need author approval)

A CWN character built on published core only: attributes and skills per CWN, no homebrew. The *interesting*
choices are the ones CWN already gives:

- **Skills** that make a rookie plausible: Investigate, Connect, Administer, Notice, Shoot (low), Talk
- **A weakness that is not a flaw in disguise:** e.g. low Connect, high Notice — someone who sees people clearly
  and cannot work a room
- Equipment: service sidearm, body armour, secure terminal, Europol credentials (which are *not* a warrant)

**OPEN:** exact attribute array. Do not generate one into canon; the first playtest should produce it.

---

## 3. Four-act outline

### ACT I — *The Rookie* (CANON: grounded cyberpunk procedural)

**Dramatic question:** *Can she do this job well without becoming the thing the job produces?*

**Purpose:** establish competence, institution, city and colleagues; teach CWN procedure through cases that
matter to individuals; plant fragments whose meaning is unavailable yet.

**Shape:** roughly 8–12 sessions or one 2–3 hour slice for the vertical slice in §4.

**Episode types** (each a case, not a chapter):

1. **The form that does not exist** — a cross-border identity fraud where the obstruction is bureaucratic, not
   criminal. Teaches Administer, Connect, and that Europol cannot arrest.
2. **The witness who will not be a witness** — a Kurvi shopkeeper who saw something and has decided that talking
   to police is worse than the thing she saw. Teaches interview, leverage, and the cost of using it.
3. **The colleague who cuts a corner** — a Finnish liaison officer fabricates a timestamp "to save the case".
   Teaches complicity: report, cover, or quietly fix.
4. **The NHI-adjacent case that is not about NHI** — psychotronic trafficking where the crime is smuggling, the
   horror is ordinary, and the anomaly is a red herring. **Deliberate:** the first weird thing she sees is
   explained mundanely.
5. **The night shift** — no case. A colleague's birthday, a tram, a bar, an argument about the Quarantine with
   someone who was there. Player-only consequences.

**Act transition criterion (PROPOSAL):** not a plot gate but a **trust gate** — she has (a) solved or closed at
least one case without being told how, (b) formed at least one relationship with a named NPC, and (c) done at
least one thing she would not tell her supervisor. That combination is what makes Act II's rupture land.

**What must NOT happen in Act I (CANON):** no UFO set piece, no prophecy, no confirmed psychic event, no
astral travel, no reveal.

### ACT II — *The Conspiracy / First Awakening* (CANON)

**Dramatic question:** *What is she willing to lose in order to be right?*

**Inciting incident (PROPOSAL, needs author approval):** a Europol case collapses because *someone inside Europol
wanted it to*. Concretely: an anomalous death in a Kurvi stairwell is ruled accidental by a pathologist who was
asked politely, and the file is closed with a footnote that does not match the photographs. The protagonist's
own office signs it off. That is the rupture — not a monster, a signature.

**Structure:**

- **Three investigative avenues**, all viable, none complete: the official file; the street (Kurvi, Vallila
  depot, the swimming hall as a neutral meeting place); and the person who filed the footnote.
- **The major moral decision** (CANON): she must choose between protecting a person and protecting the case —
  and the campaign guarantees she cannot have both.
- **The awakening** (CANON, fixed beat): during a scene the player has already been through once, perception
  changes. This is authored; how she experiences it (terror, relief, dissociation, laughter) is player-facing.
- **Unlock:** predetermined natural Telepathy, Psychic Defence, first astral awareness — specified in §8, **not
  chosen**.

**Cruelty rule for the reveal:** the awakening does not resolve the case. It makes her *less* able to explain
what she knows to anyone with authority, which is the actual cost.

**Act transition criterion:** she has used an active PSI ability to obtain something CWN procedure could not, and
it has cost her something material — a relationship, a clearance, or a night of sleep she does not get back.

### ACT III — *The Threshold* — **PROPOSAL, PENDING AUTHOR DECISION**

> **Do not treat this act as canon.** #1132 defines Acts I, II and IV and leaves III to the author. What follows
> is one suggested shape, offered so the gap is visible rather than silently filled.

**Proposed purpose:** the bridge between a conspiracy she can investigate and a cosmos she has to *survive
knowing about*. The act where abilities become procedures, institutions become choices, and the protagonist
starts to suspect the shape of the answer.

**Proposed beats:**

1. **Competing explanations.** Three sources give three incompatible accounts of the Harvest; at least two are
   sincere. No scene resolves which is true.
2. **Astral procedures introduced properly** (first mandatory use): a bounded, repeatable loop — anchor, project,
   perceive, interact, be interfered with, return, reintegrate. See §8.3.
3. **Institutional crisis.** Her office is investigated; her clearance is suspended or her mentor is removed.
   The question becomes whether the institution can survive knowing what she knows.
4. **A choice about disclosure.** Register her PSI, hide it, or hand the discovery to a body she does not trust.
   All three are defensible; all three have costs that return in Act IV.
5. **Departure from Helsinki** for 2–3 missions, with the city still the emotional home.

**Alternative shapes for the author (PROPOSAL):**

- **A. The quiet act** — almost no combat, a single location, mostly conversation and astral work. Cost: pacing
  risk after Act II.
- **B. The chase act** — the conspiracy becomes pursuit; the protagonist is hunted by people, not entities.
  Cost: less room for the metaphysical turn.
- **C. The institutional act** — she keeps the job and fights from inside. Cost: requires a bureaucracy system
  the repo does not have.

**OPEN (author):** does Act III exist as a playable act, or is it a short interlude folded into the end of II
and the start of IV? Both are legitimate; the second is cheaper and may be better.

### ACT IV — *The Wanderer* (CANON)

**Dramatic question:** *What does service mean when you finally know what you volunteered for?*

**Fixed beats (CANON):**

1. **The astral meeting.** She meets her **Higher Self**. It offers revelation, not obedience.
2. **The identity:** she is a Wanderer, and before incarnation she chose a **special StO service**.
3. **The powers activate** — the pre-authored third-stage package (§8).
4. **Scale opens:** Confederacy civilisation, Time/Space, orbital locations; SWN tools only if actually used.
5. **StS entities identify her as a Wanderer and begin hunting her.** They are antagonists, never an allegiance.
6. **The final disclosure:** the *content* of the pre-incarnate service is revealed at the ending, not at the
   meeting. Earlier fragments re-read in a new light; they do not become a different story.

**Ending structure (CANON, three trajectories within StO):**

| Ending | What it means | What it costs |
|---|---|---|
| **The Officer** | She stays Europol — humanity first, Confederacy second | She may be wrong about a Confederacy decision, and lives with it |
| **The Envoy** | She serves the Confederacy as a Wanderer, accepting the full meaning of the commitment | She becomes, to some humans, exactly the thing Europol warned her about |
| **The Interpreter** | She attempts a reconciliation: service defined on her own terms, refused by neither side | Requires specific earlier choices; not a "best" ending, a hardest one |

**What is not available:** joining an StS faction, an StS ending, or a zero-polarization NPC handoff. The Law of
One RPG's own handoff mechanic is explicitly not this campaign's branch.

---

## 4. Act I playable slice — *the first week*

**Goal:** a vertical slice that is a complete, satisfying Europol story with no metaphysics, runnable in one or
two sessions, and reusable as the campaign's opening.

### 4.1 First mission — *"The Tuesday Complaint"* (PROPOSAL)

**Premise.** A Lithuanian logistics clerk files a complaint that her dead brother's employment record is still
being updated. Europol's interest is a cross-border data integrity issue; the human story is a woman who wants
permission to grieve. The trail leads through a Kurvi freight office to a small identity-laundering operation
that sells *continuity* — the service of keeping a dead person employable so a family keeps a pension.

**Why this case first:** it teaches every CWN procedure the campaign needs (interview, records, surveillance,
one short violent confrontation that is a **failure state**, not a climax), it is morally legible, and its
"anomaly" resolves mundanely.

**Scene structure:**

| # | Scene | Procedure | Failure is interesting because |
|---|---|---|---|
| 1 | Office: the complaint lands on her desk | Administer, read the file | She can miss the footnote and learn about it later |
| 2 | Kurvi: the freight office, the clerk's sister | Connect / Talk / Notice | Pushing too hard closes the sister forever |
| 3 | Vallila tram depot: the night dispatcher | Surveillance, Notice | Illegal surveillance produces usable but inadmissible evidence |
| 4 | Europol: the liaison officer who wants it closed | Bureaucratic conflict | Winning the argument costs a future favour |
| 5 | The stairwell: one man, one knife, no heroics | CWN combat, morale | She can be injured; the campaign continues, the case changes |
| 6 | Resolution: a file, a family, a pension | Administer, judgement | Two lawful resolutions, neither clean |

**Explicit non-events:** no psychic flash that solves it, no entity, no prophecy, no dream that explains
anything. One dream exists in the week; it is ambiguous and can be read as stress.

### 4.2 Downtime cycle (CANON: "substantial time and agency for Helsinki life")

A shift/downtime loop, not a mission chain. Between cases the player gets **two or three downtime beats**:

- **Kurvi life:** the stairwell, the kiosk, the neighbour who feeds a cat that may not exist
- **Colleagues:** one drink that becomes a real conversation; one that becomes a mistake
- **Institution:** paperwork, a training module, a performance review that measures the wrong things
- **Body:** sleep, a psychotronic implant check-up, a hangover that has mechanical weight
- **City:** the swimming hall, the tram, Kauppatori in bad weather

**Rule (PROPOSAL):** downtime scenes do not roll unless the player pushes for something. They exist to build
tags, not to farm them.

### 4.3 The first week as a designed unit

Day 1: the complaint. Day 2: Kurvi. Day 3: the depot, and the first hint that someone at Europol knew. Day 4:
confrontation and its consequences. Day 5: the file. Day 6: the review, and a colleague who says the wrong thing
kindly. Day 7: a night off, and one fragment — a newspaper from 2038 that she keeps for no reason she can name.

---

## 5. Memory and revelation plan

**Design rule (CANON-derived):** clue **redundancy**. No single missed roll may permanently hide an essential
revelation. Every essential fact has at least two independent carriers, and the campaign's fallback is always a
person who will say it out loud.

### 5.1 Carriers

| Carrier | Example | Reliability |
|---|---|---|
| **Dream** | A corridor that is also a hospital; she is not frightened | Ambiguous, never explanatory alone |
| **Flashback** | A childhood vaccination that was not a vaccination | Confirms a fact, hides its meaning |
| **Document** | A 2038 newspaper clipping about a "missing persons" cluster | Verifiable, misreadable |
| **Conversation** | A retired colleague who remembers her file | Fallback carrier; cannot be missed if sought |
| **Location** | The stairwell geometry of her building matching a place she has never been | Atmospheric, not evidential |
| **Event** | A psychotronic implant behaving in a way its manual does not describe | Escalation trigger |

### 5.2 The sequence

| Stage | What the player can know | What remains hidden |
|---|---|---|
| Act I | She has an unusual file; her implant is not standard issue | That either fact means anything |
| Act II | Her childhood includes a documented "medical event"; someone has been tracking her since | That the event was a choice |
| Act III | She was not born to this life by accident; three explanations compete | Which one is true |
| Act IV | She is a Wanderer; she volunteered | **What she volunteered for** |
| Ending | The service itself | — |

### 5.3 What never happens

- A character states the twist before Act IV.
- A fragment turns out to be a lie designed to trick the player (misdirection yes, cheating no).
- The ending reveals that her choices did not matter. The disclosure reframes them; it does not erase them.

---

## 6. Choice and transformation map

**Fixed:** StO. **Variable:** everything a person can be.

| Axis | What it tracks | Mechanical weight (PROPOSAL) | Returns in |
|---|---|---|---|
| **Personality tags** | Pacifist, Ruthless, Curious, Loyal, Sarcastic… graded 1–2 | Constrain action, small modifiers, never free | Everywhere; the tag model already exists |
| **Professional reputation** | Inside Europol; with Finnish police | Access, tasking, who covers for whom | Act III suspension, Act IV endings |
| **Corruption ledger** | Specific acts, not a score | Evidence in the Act III investigation | Disqualifies "Interpreter" if too heavy |
| **Relationships** | Named NPCs, with history | Who warns her, who betrays her, who comes for her | Act IV finale |
| **Politics** | Stated beliefs about NHI, Quarantine, EU, Confederacy | Dialogue options and NPC trust | Act IV's three endings |
| **Body** | Sleep, injury, dependency, recovery | Fatigue modifiers; scene availability | Act III, Act IV |
| **Awareness** (Law of One term, used lightly) | How much she has understood | Gates *comprehension*, never power | Astral scenes |

**Two rules that protect the design:**

1. **No morality meter.** The player never sees a number labelled "good". They see consequences with names.
2. **Imperfection is not alignment.** A dirty arrest does not move her toward StS. It moves her toward a
   suspension, a colleague's silence, and a prosecutor who remembers her name.

---

## 7. The Act II moral turning point

**Requirement (CANON):** a consequential decision that *reveals* an already-positive StO orientation. Not a test
she can fail.

**Proposal: "the witness or the warrant."**

A person who has been trafficked — a psychotronic courier, young, undocumented, useful to the case — will testify
only if the protagonist guarantees she will not be deported. The guarantee is not hers to give. Meanwhile the
case's only other route requires the courier's name in a document that will leak.

Three defensible paths:

1. **Promise and deliver.** She commits a procedural violation, gives the courier a real future and a false
   identity, and destroys her own case's admissibility.
2. **Promise and betray.** She takes the statement, keeps the name out of the file, and loses the case; the
   courier is deported anyway. She keeps her hands clean and the person does not.
3. **Refuse to choose and escalate.** She goes over her supervisor's head to a body that will act — probably
   slowly, possibly well, certainly in a way that leaves her exposed.

**How StO is revealed, not selected:** after the decision, an NPC who has been watching her says something like
*"You were always going to do that."* The game treats the orientation as a fact she is learning, not a score she
earned. The scene's emotional content changes with which path she took; the fact of who she is does not.

**What the decision actually changes:** the courier's fate, one relationship, her professional standing, and
whether Act IV's "Interpreter" ending is reachable.

---

## 8. Rules-by-act dependency table and the PSI plan

**Standing law (CANON):** **CWN is the immutable core.** SWN, AWN, WWN and NoöPunk-specific rules are introduced
**only when a scene needs them**, each mapped to its first necessary milestone below. Nothing advanced is built
before Act I exists.

### 8.1 Rules by act

| Act | Rules | First necessary milestone | Status in repo |
|---|---|---|---|
| I | CWN core: attributes, skills, checks, combat, damage, equipment, investigation, advancement | Mission 1, scene 1 | **Implemented** |
| I | CWN cyberware (BCI, psychotronic implant as cyberware) | Character creation | **Implemented** |
| I | Tag/memory log (lightweight) | First personality consequence | Tag model implemented; campaign log OPEN |
| II | SWN psionics subset: Telepathy, Psychic Defence | The awakening scene | Catalogue exists; NoöPunk tuning OPEN |
| II | Bionics (AWN-mutation-inspired, NoöPunk-specific) | First biological anomaly encountered | **Not implemented** — design only ([`design/BIONICS.md`](../../design/BIONICS.md)) |
| II | Catalyst / Awareness tags | The moral turn | **Not implemented** |
| III | **Astral Projection procedure** — top priority | First voluntary projection | **Not implemented** — see §8.3 |
| III | Chakra/awakening tags (bounded) | Astral interaction | **Not implemented** |
| IV | Advanced SWN-compatible PSI package | Higher Self scene | **Not implemented** |
| IV | SWN starship/orbital tools | First orbital mission | Only if used; never required |
| IV | SMC interaction (narrative, not a subsystem) | Confederacy contact | OPEN |

**Explicitly not built now (CANON):** no standalone Law of One RPG merge, no parallel rules engine, no full
power catalogue before the campaign needs it.

### 8.2 PSI reveal/unlock matrix (CANON columns, PROPOSAL contents)

Powers are **authored, not chosen**. "Active" means the player can trigger it with a procedure and a cost.
"Scripted" means the narrative runs it.

| Stage | Power | Source | Active / Scripted | Cost / limits | First scene | Narrative reveal | Governing rule |
|---|---|---|---|---|---|---|---|
| I | **Defensive psychotronic screen** | Europol implant | Active, bounded | Implant charge/downtime; no offence | Mission 2 (the stairwell, if attacked) | None — it is equipment | CWN cyberware |
| I | **Dream fragments** | Innate, unrecognised | Scripted | — | End of week 1 | "Just a dream" | Scene-authored |
| II | **Telepathy (receive)** | Innate, awakened | Active | SWN Effort, short range, surface thoughts | The awakening | Confirmed by a second incident | SWN psionics, tuned |
| II | **Psychic Defence** | Innate, awakened | Active | SWN Effort | The first hostile psychic contact | Revealed under threat | SWN psionics, tuned |
| II | **Involuntary astral glimpse** | Innate | Scripted | One scene only | Act II climax | Terrifying, unexplained | Scene-authored |
| III | **Astral Projection (full loop)** | Innate, trained | **Active** | Anchor required; time limit; body vulnerable | First voluntary projection | Taught, not revealed | §8.3, new procedure |
| III | **Astral perception of entities** | Innate | Active | Within projection only | Same | Partial — entities are not explained | §8.3 |
| III | **Psychometry** | Innate | Active, narrow | Object-bound, one fact per object | Investigation beat | Useful, not omniscient | OPEN |
| IV | **Higher Self contact** | Revelation | Scripted | Once | Act IV opening | Full Wanderer reveal | Scene-authored |
| IV | **Astral combat / interference** | Innate, advanced | Active, bounded | Costs, consequences | First StS encounter | Threat made concrete | §8.3 |
| IV | **Unrestricted precognition** | — | **Scripted only, never active** | — | Plot-critical moments | Never a repeatable power | Design law |

**Why precognition stays scripted:** a freely repeatable "what happens next" ability is a scene-breaking power
in a mystery game. The repository's own PSI boundary note
([`PSI_INVESTIGATION_BOUNDARY_1105.md`](../rules/PSI_INVESTIGATION_BOUNDARY_1105.md)) is the reference.

### 8.3 Astral Projection — the one new procedure worth designing first

**Design goal (CANON):** a minimal playable loop, not a second combat system. Five states, one resource, one
hazard.

**States:** `embodied` → `projecting` → `astral` → `returning` → `embodied`. The physical body remains at the
anchor and is **vulnerable**; that vulnerability is the tension.

**The loop:**

1. **Anchor.** A place, an object, or a person she trusts. Without an anchor, projection is possible but she
   cannot return reliably.
2. **Project.** Perception opens; the physical world becomes thin, not absent.
3. **Perceive.** Astral locations and entities. **Differentiate four things explicitly:** physical embodiment,
   astral body, Time/Space location, ectoplasmic manifestation. Do not blur them; most astral confusion in games
   comes from blurring them.
4. **Interact.** Conversation, observation, and limited physical effect. **No default attack.** Interference is
   possible and dangerous.
5. **Interference.** Something notices her. The hazard is losing the thread back — mechanically, a worsening
   position on a return track, not hit points.
6. **Return and reintegrate.** She wakes with a consequence: fatigue, a nosebleed, a memory she did not have, or
   in bad cases a period where the body and the self disagree.

**Boundaries (CANON):** third-density people can experience involuntary astral phenomena in dreams and
near-death experiences; **not every dream is astral**; waking, repeatable control is a separate learned
capability unlocked at a fixed point.

**OPEN:** whether this is a CWN skill check chain, an SWN Effort-costed discipline, or a scene procedure with no
dice at all. My preference is the third for Act III and the second for Act IV — but that is a design decision,
not a fact.

### 8.4 Psychotronics

Psychotronic implants are **cybernetic**, and they do three things and no more: they let a non-psychic perceive
the edges of psychic phenomena, they give a bounded defensive response, and they can be tuned — badly — to
amplify an ability the wearer already has.

They are **not** a second psionic engine, not a source of innate power, and not a shortcut to Bionics. The same
effect must not exist in three systems: **implant, bionics and PSI must each have a different fiction and
different mechanics**, or one of them should be deleted.

---

## 9. Institutions and continuity

| Institution | Established role | In this campaign | Tension to play |
|---|---|---|---|
| **Europol Helsinki** | Cross-border coordination; cannot arrest in Finland; must negotiate for access | The protagonist's employer and the campaign's home base | It opens doors; national officers walk through them |
| **Finnish police / Supo** | National authority; owns arrest and prosecution | Liaison partners, rivals, occasionally the only adults in the room | Jurisdiction is a character |
| **UNSA** | Established institution with its own jurisdiction and history | A collaborator or obstacle depending on act; **not** the employer | It knows more than it says, and says so |
| **Corporations** | Employers, logistics, data | The ordinary antagonists of Act I | Nothing they do is technically illegal until it is |
| **Confederacy** | Late-campaign civilisation | Appears in Act IV, with its own agenda | Not automatically morally correct |
| **StS entities** | Antagonists | Hunt the Wanderer once identified | They are not recruitable, ever |

**Continuity anchors already in the repository:** Kurvi and Kallio street geography
(`data/world/helsinki_map.json`), the UNSA HQ at Ratakatu, Kauppatori, the Vallila tram depot and the Yrjönkatu
swimming hall as locked locations; the post-Crisis Cold War status quo; Europol's documented limits.

**OPEN (author):** whether the protagonist's Europol office is the liaison office described in
`EUROPOL_HELSINKI_1114.md` or a separate NHI-adjacent unit, and how far Supo's authority reaches in 2045.

---

## 10. Ending outline

**Common structure:** the service is revealed; the hunt is at its height; she chooses what service means.

1. **The Officer** — refuses the Confederacy's framing, stays with the humans who raised her, and accepts that
   her institution may be wrong. Epilogue: a desk, a case file, someone new at the door.
2. **The Envoy** — accepts the Wanderer role fully. Epilogue: a departure, and a human colleague who does not
   quite believe the goodbye.
3. **The Interpreter** — attempts to define the service herself. Requires: a preserved relationship, a
   corruption ledger light enough that she can still be believed, and a PSI disclosure made in Act III.
   Epilogue: ambiguity, honestly earned.

**All three:** StS factions remain enemies; the pre-incarnate service is named; earlier choices are reframed, not
invalidated.

**What none of them are:** a reward for a virtue score, a secret fourth "true" ending, or a choice between good
and evil.

---

## 11. Open questions / author decisions

1. **Act III:** playable act, or interlude folded into II/IV? (Biggest structural question.)
2. **The first episode:** is it prose first or case-file first? (Relates to #1086's D70.)
3. **The hidden past:** what exactly happened in 2038, and who else knows?
4. **Europol unit:** liaison office or NHI-adjacent unit; who is her direct superior?
5. **Romance:** available, and does any relationship survive Act IV by design or by chance?
6. **Addiction mechanics:** how heavy? The repo's tag model allows consequence without a morality system; the
   question is how much screen time dependency deserves.
7. **Astral dice:** skill chain, Effort-costed discipline, or pure scene procedure (§8.3)?
8. **Bionics timing:** Act II discovery or Act III choice?
9. **UNSA's knowledge:** does UNSA know about Wanderers in 2045, and if so, since when?
10. **The finale's location:** Helsinki, orbit, or somewhere with no jurisdiction at all?

**Rule for whoever answers these:** record the answer here, in this file, with a date and the author's name.
Not in a commit message, not in a chat, not in a new document.

---

## 12. References

**Campaign and world**

- [#1132](https://github.com/TomiToivio/NooPunk/issues/1132) — this design brief
- [`EUROPOL_HELSINKI_1114.md`](../world/EUROPOL_HELSINKI_1114.md) — Europol's powers and limits
- [`CANON_FORTRESS_EUROPE_1113.md`](../world/CANON_FORTRESS_EUROPE_1113.md) — the European security order
- [`NHI_CRISIS_921.md`](../world/NHI_CRISIS_921.md) — timeline: Singularity, Quarantine, Cold War status quo
- [`POST_NHI_WORLD_1005.md`](../world/POST_NHI_WORLD_1005.md) — what the world looks like in 2045
- [`UNSA_HUMAN_PROXY_FACTIONS.md`](../world/UNSA_HUMAN_PROXY_FACTIONS.md) — UNSA's position
- [`HELSINKI_SLANG_GLOSSARY.md`](../world/HELSINKI_SLANG_GLOSSARY.md) — voice
- `data/world/helsinki_map.json` — the five mapped locations

**Rules**

- [`RULEBOOK.md`](../../RULEBOOK.md) / `rulebook/` — the tabletop baseline (CWN core)
- [`design/BIONICS.md`](../../design/BIONICS.md) — the bionics direction (AWN-inspired, not AWN)
- [`ISSUE_1043_SWN_PSIONICS_FACTIONS.md`](../design/ISSUE_1043_SWN_PSIONICS_FACTIONS.md) — what is imported from SWN and why
- [`PSI_INVESTIGATION_BOUNDARY_1105.md`](../rules/PSI_INVESTIGATION_BOUNDARY_1105.md) — why PSI cannot solve cases
- [`ISSUE_1008_PHASE2_LACLAU.md`](../design/ISSUE_1008_PHASE2_LACLAU.md) — the faction/ideology layer this campaign sits on

**Metaphysics (reference, not imported)**

- [`docs/law_of_one/`](../law_of_one/README.md) — a **separate game**; Phase 1 per #1124. Nothing here merges it.
- [Law of One Phase 1 (#1124)](https://github.com/TomiToivio/NooPunk/issues/1124)

**Design canon**

- [`DESIGN_CANON_1007.md`](../design/DESIGN_CANON_1007.md) — cyberpunk first, cosmic underneath
- [`BRAINSTORM_1037_FICTION_PLAY.md`](../design/BRAINSTORM_1037_FICTION_PLAY.md) — fiction/play relationship
- [`BRAINSTORM_1038_ROMPPAINEN_PARTY.md`](../design/BRAINSTORM_1038_ROMPPAINEN_PARTY.md) — companion design constraints

---

## Appendix: what this document deliberately does not do

- It does not write the first episode. Finnish fiction is the author's.
- It does not generate the protagonist's character sheet.
- It does not invent Europol ranks, budgets, legal citations, prices or equipment stat blocks.
- It does not transcribe SWN, AWN or WWN rules from memory.
- It does not merge the Law of One RPG into NoöPunk.
- It does not treat Act III as settled.
