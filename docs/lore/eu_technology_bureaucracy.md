# EU technology, bureaucracy and operational culture (#1236)

> **Status: canonical setting, extended.** This is the design bible for the European Union, Europol and Eurodef: what
> their hardware looks like, why it looks that way, what the law forbids, who operates the machines, and how a field
> team actually works. It is worldbuilding and scene guidance, **not a rules engine**, and it does not alter the
> immutable CWN core.
>
> It **extends** [Project Plato / EISS and EuroNET (#1200)](../world/PLATO_EISS_EURONET_1200.md) rather than replacing
> it: #1200 owns the connectivity model, the perimeter and the authorisation ladder; this page owns the war, the design
> language, the capability ceiling, the institutions' division of labour, the field team and the kit.

**Status key.** Every substantive claim below carries one of these.

| marker | meaning |
|---|---|
| **[CANON]** | stated by the author in `design/POLICE.md`, in this issue, or in a canonical page (#1200, #1113) |
| **[PROPOSED]** | a design synthesis an agent wrote to make canon usable; needs Tomi's yes/no |
| **[CONTESTED]** | true *in-universe* as testimony, rumour or propaganda — not as fact the setting guarantees |
| **[OPEN]** | a real question the text does not answer; listed again in §9 |

**Related:** [#1200](../world/PLATO_EISS_EURONET_1200.md) · [Fortress Europe](../world/CANON_FORTRESS_EUROPE_1113.md) ·
[Europol Helsinki frame](../world/EUROPOL_HELSINKI_1114.md) · [EU networks](../world/EU_NETWORKS_AND_PLATO_1200.md) ·
[Cyber space after the Crisis](../../rulebook/22_CYBERSPACE_AFTER_THE_CRISIS.md) ·
[ontology](../../rulebook/11_ONTOLOGY.md) · [campaign frame](../campaign/CAMPAIGN_01_EUROPOL_ROOKIE.md) ·
[rookie build](../design/DRAFT_EUROPOL_ROOKIE_BUILD_1174.md) · [PSI access](../../src/rules/psi_access.py)

---

## 1. World War Three and the end of Russia

### 1.1 What is canon

**[CANON]** When the NHI Crisis began, **the EU and Ukraine were fighting Russia**. Europeans remember this as **World
War Three**. The Russian front had already collapsed.

**[CANON]** Former president **Dmitry Medvedev** staged a successful coup: four **Mil Mi-8** helicopters carrying
**VDV** paratroopers raided **Putin's Palace**. Medvedev then tried to order a nuclear launch — and discovered the
order was futile, because **extraterrestrial intervention had already disarmed the Strategic Rocket Forces of the
Russian Federation, and every nuclear weapon on Earth**. The same intervention neutralised **every frontier AI
laboratory then capable of restarting the acceleration toward ASI**.

**[CANON]** Medvedev died by suicide. This is **the end of Russia as an effective state** in this timeline.

### 1.2 What is contested, and must stay contested

**[CONTESTED]** That Medvedev **personally strangled Putin**, and that he then **had everyone identified as a Putin
loyalist executed**.

The setting's own source material tells this as a story with a narrator's relish — the long table, the laughter, the
growl, the terror of the man under it (`design/MEDVEDEV.md`). That is exactly what makes it *testimony* rather than
record: it has the shape of a legend already. Keep all of the following live:

* the coup succeeded and Putin died — **canon**;
* the manner of his death — **contested**, and different witnesses give different accounts;
* the executions — **contested**, and possibly a retrospective justification;
* the claim that the nuclear order was *attempted* rather than merely *available* — **contested**;
* whether Medvedev's suicide was despair, a decision, or something done to him — **open, and it should stay open**.

This is where the **Mandela Effect** material (#1113, and the earlier contradictory-memory work) earns its keep: two
Europeans can both be certain, both be sincere, and describe different deaths. A game table should be able to produce
a document that contradicts the briefing without anyone lying.

### 1.3 Two drafts of the same war — a real contradiction, named

Two author documents describe the adversary differently, and this page will not paper over it:

| source | adversary | result |
|---|---|---|
| `design/POLICE.md` (and this issue) | **Russia**; "the Russian front had collapsed"; Medvedev's coup; "the end of Russia" | Russia ceases to be an effective state |
| `design/MEDVEDEV.md` | the **Soviet Union** invaded Ukraine; Medvedev's coup was "to save Soviet Union" | EU defeats the Soviet Union in **Operation Barbarella II**; President **Sanna Marin** as war leader; a defeated Russia becomes a vassal |

They cannot both be literally true about the same state. Three readings are available:

1. **[PROPOSED — recommended] "Soviet Union" is the *revanchist self-naming* of the Russian state.** The regime calls
   itself the Union, restores Soviet symbols, and its officers mean it; European press uses "Russia" because that is
   what the country is. Medvedev is a Soviet restorationist who believes he is saving a union that no longer exists.
   This costs nothing, explains the vocabulary, and makes the coup's pathos sharper: he killed a man to inherit a
   country that had already stopped existing.
2. **Two wars.** A Soviet invasion defeated earlier, then a Russian war during the Crisis. Heavier, and it invites a
   chronology nobody has written.
3. **Deliberate contradiction.** Keep both, and let in-universe documents disagree the way real archives do. Consistent
   with §1.2, but it makes "the end of Russia" ambiguous in a way the design consequence below does not need.

**Either way, do not rewrite either source document.** Reading 1 is a note for whoever writes the next canon page, not
an edit.

### 1.4 The design consequence

**[CANON]** European military and civilian systems were designed for — and often deployed during — a continent-scale
war *and* the NHI Crisis. Much European technology is, in the most literal sense, **WW3 field equipment**.

Four properties follow and every later section assumes them:

1. **Repairable** — a part is replaceable by a technician with a manual, not by a factory with a supply chain.
2. **Redundant** — two ways to power it, two ways to talk to it, and a written procedure for when both fail.
3. **Shockproof** — built to keep working through electromagnetic interference, cyberattack and infrastructure loss.
4. **Distributed** — no single cabinet whose loss ends the service.

---

## 2. The European design bible

### 2.1 Hardware: military-survivable retrofuturism

**[CANON]** Europol, Eurodef and ordinary EU governmental hardware **looks like sturdy, EMP-resistant military field
equipment intended to survive WW3 — because much of it really was.**

**[CANON]** Bulky does not mean primitive. A world-leading quantum processor, a psychotronic probe or a neural
imaging array may sit inside an enormous field-hardened case with **manual controls, interlocks and warning labels**.

**[CANON — engineering, not magic]** EMP hardening is a *system*, and it fails partially:

| measure | what it buys | what it does not |
|---|---|---|
| screened enclosure, bonded seams | stops radiated coupling into the case | does not protect a cable leaving it |
| filtered power entry | blocks conducted transients on the mains | does not survive a direct strike on the feed |
| shielded, keyed connectors | controlled interfaces, no accidental patching | connectors wear, and a damaged shield is invisible |
| surge arrestors, sacrificial stages | cheap parts fail instead of expensive ones | each event consumes a stage |
| offline mode + local storage | the device keeps working when the network dies | data synchronises later, or not at all |
| spare modules, tool kits, printed manuals | field service by a technician | assumes the technician and the part exist |
| supply-chain maintainability | the same part in ten years | assumes the procurement worked |

Write failures as consequences of a specific measure being absent, damaged or overloaded. "EMP-proof" is a marketing
claim a character can be punished for believing.

### 2.2 Three hardware families, one design language

**[CANON]** Distinguish civilian investigative, military/strategic and public administrative technology while
preserving a common family resemblance.

| family | user | character | example |
|---|---|---|---|
| **Investigative** | Europol, national detectives | portable, evidence-facing, chain-of-custody obsessed; built to be carried up four flights of stairs and logged | forensic multimode scanner in a foam-lined case; a cyberdeck with a physical evidence-bag clip |
| **Strategic / military** | Eurodef | racked, vehicle-mounted or dug in; redundant power, hardened masts, manual override everywhere | a field communications shelter; a hardened drone control station |
| **Public administrative** | ministries, clerks, citizens | cheaper, quieter, still over-engineered; laminated instructions taped to the side | a benefit-office terminal with a chip-card reader and a sticker saying *do not switch off during audit* |

The family resemblance is deliberate: a citizen recognises a Europol case by its **latches, labels and cable
discipline** before reading the badge.

### 2.3 Art direction: palette, materials, type, silhouette

**[PROPOSED]** — a starting kit for artists and writers, not a rule.

* **Palette.** Warm bone and ivory casings; deep navy and slate; a single saturated accent per institution (Europol:
  oxblood; Eurodef: signal amber; civilian administration: teal). Warning markings in the standard European yellow,
  never neon.
* **Materials.** Anodised aluminium, powder-coated steel, phenolic and bakelite for controls, thick ABS, real glass
  over displays, braided cable with strain relief, leather and canvas for carry. Nothing glossy, nothing seamless.
* **Typography.** A neutral grotesque for labels, a monospace for anything a machine prints, and the institution's name
  in a restrained serif on the plate. All-caps only on warning labels. Bilingual plates where the setting's politics
  make that a scene.
* **Silhouette.** Boxy with visible fasteners, a carry handle that is structural, feet that are rubber, a lid that
  opens to become a shade or a shelf. Instruments cluster at the top, storage at the bottom, and the whole thing looks
  like it could be dropped from a moving car.
* **The tell of New European Idealism.** One beautiful element per object: a machined bezel, an engraved line, a
  proportion that is quietly classical. The EU does not make ugly equipment; it makes *formidable* equipment with a
  good line, and then bolts a plastic label holder to it.

**What to avoid:** generic 1980s neon cyberpunk; chrome; holographic UI; featureless white slabs; "future" as a
synonym for "thin". The Crisis did not produce sleekness. It produced things that survive.

### 2.4 New European Idealism — philosophy and style

**[CANON]** **New European Idealism** is both a central philosophy of the EU and a recognisable architectural,
graphic and industrial design movement. Its philosophical references explicitly include **Spinoza, Kant and Hegel**,
idealist theories of mind, **Quantum Information Panpsychism (QIP)**, quantum consciousness, psionics, psychotronics
and astral projection.

**[CANON]** The design movement draws on the **18th-, 19th- and early-20th-century European imperial periods**, and
transforms those references into something **elegant, futuristic, minimalistic and idealistic**.

**[CANON — the tension that makes it usable]** The European aesthetic is simultaneously **beautiful and formidable,
authoritarian-seeming and sincere, noble in aspiration and absurd in execution**. A ministry corridor can be sublime
and its filing system a catastrophe; both are the same building.

**[PROPOSED]** How to write it without either celebrating empire or flattening it into a critique:

* the movement's own claim is **universal reason with a European accent** — Spinoza's substance, Kant's public use of
  reason, Hegel's history as a process that Europe believes it is *inside*;
* its critics say the accent is the point: a universalism that keeps producing European buildings, European law and
  European chairs;
* the movement contains both, sincerely. A committed Idealist can be a genuine anti-colonialist who has never noticed
  what the cornice is quoting, and a sharp critic can love the building.

Three concrete motifs, so the style is describable rather than merely named:

1. **The colonnade that is also a corridor.** Porticos, arcades and processional axes scaled to a clerk's working day.
2. **The engraved line.** A single machined rule across a surface — the only ornament, and it is load-bearing.
3. **The luminous interior.** Light as a moral claim: white, diffuse, faintly warm, and always slightly too bright for
   the hour, because the institution is always open.

---

## 3. Capability map: what Europe permits, and what it deliberately cannot do

### 3.1 The ban, defined by capability rather than size

**[CANON]** After the catastrophes of AGI/ASI acceleration, the EU maintains a **strict ban on research, development
and operation of systems approaching AGI**, and an especially strong prohibition on **independent autonomous AI
agents**. **Autonomous robotics is subject to still more severe restrictions.**

**[CANON]** Policy is defined by **capability, autonomy, tool access, self-improvement and integrated multi-agent
behaviour** — not by parameter count.

**[CANON]** The proposed ceiling for permitted general-purpose LLM assistance is approximately **a 2026 desktop
Ollama-class Gemma 4 31B in practical breadth and autonomy**. Later **narrow** systems may greatly exceed that ceiling
on a domain-specific task.

**[PROPOSED]** The test a licensing officer applies, in the order that produces denials:

| question | denied when | example of a permitted system |
|---|---|---|
| can it act without a human decision? | it initiates consequential action itself | a spam filter that labels; a clerk who deletes |
| can it choose its own tools or targets? | its scope is open-ended | a rules engine that only answers the question it was built for |
| can it improve itself or write its own successor? | yes, at all | a model retrained by a licensed team on a fixed corpus |
| does it coordinate with other systems into a composite capability? | several narrow systems are chained without a human between them | a workflow with a signature at every join |
| does it generalise outside its licence? | it answers well outside its declared domain | a translation system that refuses poetry |

That table is a *scene generator*: a prosecutor can argue about which row a system fails, and a technician can be
right about the mechanism and wrong about the law.

### 3.2 Bounded automation is not autonomy

**[CANON]** The text must distinguish **autonomous decision-making** from **preauthorised bounded automation**, or
conventional cyberdefence and industrial control become impossible. Human-in-the-loop must be **genuine,
consequential and auditable**; emergency defensive interlocks must not absurdly require a clerk's click per
microsecond.

**[PROPOSED]** The line, written the way an operator would say it: *"a reflex may fire without me; a decision may
not."* Dropping a hostile packet, throttling a flood or isolating a segment happens under a written protocol at
machine speed. Taking down a hospital, raiding a private network, naming a person an enemy or authorising force does
not. #1200's authorisation ladder is the same distinction at the level of paperwork.

### 3.3 The rest of the map

| capability | status | what it is good at | what it is not |
|---|---|---|---|
| **Symbolic GOFAI** (Lisp, Prolog, expert systems) | **[CANON]** core of Plato | auditable inference, rule trails, decades of encoded procedure | brittle, and its failures are *confident* |
| **Narrow ML** | **[CANON]** | detection, classification, anomaly flags inside a declared domain | cannot explain itself the way a rule can, and cannot leave its domain |
| **Permitted LLM assistance** | **[CANON]** ceiling above | drafting, summarising, query help, translation-in-domain | no autonomy, no tool access beyond the licence, no self-improvement |
| **Quantum computing & sensing** | **[CANON]** Europe's comparative advantage | cryptanalysis, simulation, materials, sensing — *specific* tasks | **not** a general intelligence, and not a replacement for one |
| **Quantum consciousness / QIP science** | **[CANON]** a real European research programme | the setting's licence for PSI, psychotronics and astral phenomena | not a solved science; claims are contested in-world |
| **Cybernetic augmentation** | **[CANON]** | operators, analysts, field officers; see §7 | not a path to permitted autonomy |
| **Psychotronics** | **[CANON]** | detection, stabilisation, interrogation support, defensive implants | fallible, coercive, politically explosive |
| **Autonomous robotics** | **[CANON — most severely restricted]** | nothing the EU will license | a drone that chooses a target is a crime, not a product |
| **AGI / ASI** | **[CANON — banned]** | — | the thing the whole apparatus exists to prevent |

**[PROPOSED]** The honest cost of all this, which a scene should show: **the apparatus is slow where speed is
convenient and fast where speed is dangerous.** A records request takes four days; a hostile packet is dropped in
microseconds. Citizens experience the first and never see the second.

---

## 4. Plato / EISS: an institution that happens to be infrastructure

**[CANON — #1200]** **Project Plato** is the project name; **European Information Security System (EISS)** the formal
deployed system; **Plato** the operational shorthand; **Panopticon** a critical nickname, never the official name.
Plato is **not a unified AGI or ASI**. It is a sprawling institution and infrastructure: manual **Lisp/Prolog GOFAI**,
symbolic rules, knowledge graphs, expert systems, old-school cybernetics, specialised narrow ML, qualified 2026-scale
LLM assistants, quantum computing and sensing, and extraordinary psychotronic systems.

**[CANON]** It is operated by an **army of human beings** — cyborgified operators, analysts, Lisp and Prolog
programmers, electricians, hardware engineers, network personnel, auditors and field technicians. **Repair and
operating labour is highly visible.**

**[CANON]** The separation of systems and permissions is a **deliberate firebreak** against recombining independent
capabilities into de facto AGI.

### 4.1 What the firebreaks cost

**[PROPOSED]** — the trade-offs, written as a table an investigator can feel:

| firebreak | benefit | price |
|---|---|---|
| separate systems, no shared state | no emergent composite capability | the analyst re-enters the same name into four systems |
| human signature at every join | accountability, and a person to blame | delay, queues, and a signature given by someone tired |
| symbolic rules preferred over learned ones | the reason for a decision can be read | the rule is old, and its author has retired |
| data minimisation and purpose binding | the state cannot browse | the answer exists and cannot be joined to the question |
| maintenance by hand, in-house | the system cannot be replaced by a vendor's black box | the knowledge lives in twelve people's heads |
| deliberate siloing | no single point of coercion | the left hand investigates what the right hand already knows |

The last row is the most useful: **Plato is often wrong in a way that is fully documented**, and the documentation is
the scene.

### 4.2 Mistral — the reconciliation #1236 asks for

**[CANON conflict, stated plainly]** #1200 says **Mistral is the only EU company permitted to work on systems
approaching AGI**, under strict controls, censorship limits and human supervision, and that its AI is not superior to
the old American frontier. This issue says there is a **strict general ban** on research, development and operation of
anything approaching AGI, and asks that the two be reconciled rather than assumed compatible.

Three readings; the first is recommended.

1. **[PROPOSED — recommended] A single licensed containment programme.** The ban is on *operation* and on
   *development toward deployment*. Exactly one licensee — Mistral — is permitted to run **containment research**: a
   sealed, audited, non-networked programme whose output may not be deployed, copied into products, or connected to
   any agent. It exists so that Europe can recognise the thing it fears, which is also why it is the most audited
   institution in the setting. This keeps #1200's sentence literally true ("permitted to work on systems approaching
   AGI") without making the ban decorative.
2. **A classified deviation.** Mistral does more than the law allows, and a small number of officials know. Sharper
   for noir, and it makes every Plato scene a potential hypocrisy scene; it also converts a policy into a conspiracy,
   which is a bigger commitment.
3. **Outdated lore.** #1200's sentence predates the strict-ban formulation and should be softened to "the only EU
   company permitted to work on *near*-frontier systems". Cheapest, but it loses the most interesting pressure.

**The design consequence if reading 1 is taken:** Mistral is not Europe's OpenAI. It is Europe's *containment lab* —
the place where the thing is kept, studied, and never shipped. Its staff are the only Europeans who have seen an
answer to the question everyone else is forbidden to ask.

---

## 5. Governance: surveillance as procedure, not as a button

**[CANON — #1200]** The authorisation ladder runs from routine public OSINT through internal records, intrusive
surveillance, offensive infiltration, to bounded emergency containment, with a named signer at each rung.

**[CANON]** **Surveillance permission is substantive gameplay.** Public OSINT can be routine; private communications
interception, access to restricted records, covert tracking and **especially consciousness scanning** require
*differentiated* legal powers and documented approval.

**[CANON]** **Authorization is a Task**: case number, evidence, Clue Tags, necessity and proportionality assessment,
supervisor approval, legal review, judicial or special psychotronic permission as appropriate, scope, expiry, logging
and recourse. Fast-track emergency exceptions exist and remain reviewable.

### 5.1 The rungs this page adds

**[PROPOSED]** #1200's ladder covers networks and records. Two categories it does not yet name need their own rung,
because they are not "surveillance" in the ordinary sense:

| rung | action | authority | note |
|---|---|---|---|
| **2a** | **neural / BCI monitoring** of a consenting officer | the officer's written consent + duty supervisor | routine for field teams, and revocable at any time |
| **2b** | **neural or psychotronic assessment** of a subject (RFOAS, §7.5) | judicial or special psychotronic authorisation, higher than ordinary interview | the subject's rights are the scene |
| **2c** | **consciousness scanning** | the highest tier the setting has: judicial + independent psychotronic review | never routine, never silent, and its results are evidence *claims*, not verdicts |

**The guardrail that keeps this from becoming a superpower:** a scan produces a **record with provenance**, and a
record can be wrong, contested or excluded. The EU's own doctrine says an anomaly is a hypothesis, not an identity
verdict (§7.5).

### 5.2 OSINT and Clue provenance

**[CANON]** OSINT and social/discourse/network analysis are fundamental investigative capabilities. **Clue Tags** store
evidence and claims with **provenance, credibility and access scope**.

**[PROPOSED]** The four-part provenance a Clue Tag should always be able to answer, because the setting's whole
politics lives in it: *who says this*, *how did they come to know it*, *who is allowed to see it*, and *what would
falsify it*. A clue that cannot answer the last question is a rumour with a case number.

**[CANON]** Distinguish original evidence, source statements, competing hypotheses and verified conclusions. Political
extremist ideologies are **investigated**, not automatically inferred from dissent.

### 5.3 The satire, kept useful

**[CANON]** Bureaucratic friction creates real Plot, Task and Story opportunities — and must not make every
investigation impossible. The design target: *"Under heavy fire, an officer may have quantum-assisted forensic
resources, a defensive psychic implant and instant contact with a skilled controller — and still need a signed
permission for a surveillance record."* Useful and absurd in the same breath.

---

## 6. Europol, Eurodef and everyone else

| body | mandate | hardware family | may not |
|---|---|---|---|
| **Europol** | civilian intelligence and law-enforcement operations: OSINT, investigations, counterintelligence, digital evidence, cyber-defence cooperation, authorised surveillance, psychotronic operations, Plato/EISS operational interface | investigative | arrest on Finnish soil without national authority; grant itself a warrant; treat infrastructure access as search power |
| **Eurodef** | military cyber defence, WW3-hardened infrastructure, theatre operations, military intelligence, military-grade psychotronic and quantum interfaces | strategic / military | take over a civilian investigation; command civilian police |
| **National authorities** (Finnish police, courts, data protection) | ordinary coercive powers on their soil; judicial authorisation; review | public administrative + investigative | be bypassed by an EU agency's convenience |
| **UNSA** | cross-border existential / NHI risk coordination | mixed, contested | own Europol, override national law, or command either |
| **European institutions** | legal mandate, democratic and administrative oversight of the civilian security infrastructure | — | be assumed to have signed anything not written down |

**[CANON]** Interoperation is **coordination, not a universal command override**. **[PROPOSED]** The practical test a
scene can use: *who is allowed to say no to whom, and what happens when they do?* If the answer is "nobody, ever", the
scene has lost the setting.

**[CANON — #1200]** "Panopticon" is always an unofficial critique. The perimeter is the Plato/EISS perimeter, not the
"Great Firewall" (a retired, Eclipse-Phase-derived term; `rulebook/22_CYBERSPACE_AFTER_THE_CRISIS.md` §22.3).

---

## 7. The field team: Tony German, Laura Wendt, Salla Sotavaara

**[CANON — supplied by this issue]** Field Agents **Tony German** and **Laura Wendt** operate with a **real-time
connection** to **Field Controller Salla Sotavaara**.

**[CANON]** Salla is a **human field controller**, not an autonomous agent and **not an AI**. She monitors live feeds
and authorised sensor data, performs human analysis, liaises with Plato personnel, requests permissions, directs
support resources and relays alerts. She **cannot silently bypass legal clearance** — she is the person who has to ask
for it.

**[PROPOSED]** What that role feels like from the field: a voice that is calm because she has already read the file,
who says "stop" when the officer has not yet seen why, and who is the one who has to say "no" and then explain the
paperwork. She is not a quest-giver and not an oracle. Her authority is real and **borrowed**, and the campaign should
be able to cost her some of it.

### 7.1 Always-on body cameras — and what "always on" honestly means

**[CANON]** Body cameras are **always on** and stream live to HQ under normal operating conditions. Interruptions in
connectivity, power or physical damage must be **visible as incidents**, never silently treated as continuous
transmission. Where an uplink is lost, the camera **continues recording locally where technically possible** and
synchronises securely afterwards; the HQ live feed is marked **unavailable** until restored.

**[PROPOSED]** The three states a scene should be able to distinguish, because each is a different story:

| state | HQ sees | the record shows | what it means for the case |
|---|---|---|---|
| **live** | the feed | continuous, timestamped | the controller was a witness |
| **recording, uplink lost** | a gap with a reason code | continuous local file, synced later | the controller was *not* a witness; the file may be challenged |
| **not recording** | an incident | nothing | someone has to explain why, and "damage" is a claim |

**Cybernetic eyes** may replace or supplement body cameras and vehicle cameras **[CANON]**, provided they meet the
same always-on recording, authentication, tamper-resistance, chain-of-custody and oversight requirements. Do **not**
double-count the inventory when they do. Cybernetic-eye output is **not** a mind-reading feed, and saying otherwise is
how a defence lawyer wins.

### 7.2 The radio fallback, and the honest bandwidth

**[CANON]** The police car carries a **Nokia PoliisiSanomalaite**, an encrypted police-radio data and communications
terminal linking the vehicle to HQ when **EuroNET or mobile connectivity is unavailable**. The author's fuller name for
the system is the **Nokia PoliisiRadioSanomaJärjestelmä M 45**; the terminal in the car is the Sanomalaite.

**[CANON]** Failover precedence is **EuroNET → mobile network → encrypted police radio**, choosing the best available
*authenticated* channel.

**[CANON]** Do not pretend narrowband radio carries unlimited high-definition video. On radio fallback: live HD and
dense forensic streams are **degraded, summarised or stored locally**; high-priority voice, text, alerts and small
metadata remain available where coverage permits.

**[PROPOSED]** The bandwidth table, as an engineering document the players can read in the car:

| channel | carries | latency | what silently stops working |
|---|---|---|---|
| EuroNET | everything the case allows: HD video, evidence upload, Plato queries | seconds | nothing, until it fails |
| mobile | same, with coverage holes and congestion; a plausible urban baseline | seconds | in a basement, a tunnel, a rural cell edge |
| **encrypted police radio** | voice, short text, alerts, GPS, small metadata; still images if patience allows | tens of seconds to minutes | HD video, live forensic streams, large queries |
| local only | recording, cached records, onboard analysis | instant | everything that needs the network |

**The scene rule:** a character who does not know which channel they are on will promise HQ something the radio cannot
deliver. That is not a rules failure; it is the job.

### 7.3 Vehicles and drones: a human at the stick

**[CANON]** The police car and drone are capable of **remote human operation**. A human operator — at the vehicle or
at HQ — must be in control. **Bounded stabilisation, collision avoidance and safety interlocks may exist as
non-agentic control systems, but AI cannot drive, pilot, target, pursue or act independently.**

**[CANON]** Plato may monitor authorised incoming streams and **alert** Salla or the officers to anomalies. Its
automatic detection is a narrow monitoring function, **not command authority and not a warrant**.

**[PROPOSED]** Link-loss behaviour, written as procedure: the vehicle coasts to a stop under its own interlocks; the
drone holds position or returns to a pre-briefed point, never "decides"; the operator's console shows the loss as an
incident with a timestamp; and a human decides what happens next. A drone that improvises is a scandal, and the report
that follows is a scene.

### 7.4 From cyberdeck to evidence — the workflow

**[CANON]** The seven-step loop: authenticate through the **external cyberdeck** (or an authorised alternative: an
optional implanted deck, or a rugged tablet-style interface) → default permissions on the **Europol internal shared
case/reference database** and public OSINT → **evidence submission** with provenance → **restricted access** requires a
permission request and bureaucratic approval, tracked with justification, authority, scope, expiry and audit history →
**Plato** searches, flags and *notifies humans* → **Salla** triages and escalates → discoveries become Clue Tags and
update the story, character and faction loops.

**[PROPOSED]** Where each step lives in the existing code, so nobody builds a second system:

| step | existing mechanism |
|---|---|
| connectivity and permission class | `src/world/networks.py` — `can_attempt(network, remote=…, on_site=…, has_credential=…)`, `requires_warrant(action)` |
| hacking resolution | `src/rules/cwn_hacking.py` + `data/rules/cwn/hacking_catalogue.json` (CWN, immutable) |
| evidence as claims with provenance | `src/rules/investigation.py` (`Clue`) |
| the case as a story | `src/world/graphs.py` story graph; `src/console/world_session.py` |
| authorisation as a task that costs time | `src/simulation/scheduler.py` + `src/simulation/clock.py` (#1230 Phase 1) |
| shift and duty time | `src/rules/cwn_mission_time.py` |

**Nothing in that table is new.** The workflow is a *procedure over existing systems*, which is the whole point of the
issue's last acceptance criterion.

### 7.5 RFOAS — the Romppainen–Fujita Objective Assessment System

**[CANON]** A complicated, specialised interrogation and identity-assessment device combining **neural imaging and
psychotronic technology**, inspired in operation and atmosphere by *Blade Runner*'s Voight-Kampff examination. It
records synchronised **video, audio and neural feeds** for the full examination. It is useful for ordinary
interviews and for the detection and investigation of **unregistered Hybrids and Androids**. It is normally a
controlled interview-room or laboratory device; a transportable variant exists only if a document says so.

**[CANON]** No magical certainty: physiological, neural or psychotronic anomalies create **evidence and hypotheses**,
not automatic guilt or proof of NHI identity.

**[CANON]** **Europol must produce admissible evidence when identifying a person as NHI.** Superficially obvious
differences or a system suspicion are not a substitute for documented evidence. Distinguish **biological hybrid
status**, **android identity** and **NHI origin claims** rather than conflating them.

**[CANON]** Operator-mediated: the interrogator and a trained human analyst supervise all inferences. Plato may assist
with narrow pattern detection but **cannot render an autonomous identity verdict**.

**[CANON]** It is a regulated, intrusive psychotronic technology with a **higher permission tier** than routine
interviewing, reviewable records and rights safeguards.

**[PROPOSED]** What it does mechanically, in existing terms only: it is a **Social or Investigation scene** with a
recorded transcript, and its output is **Clue Tags plus labelled hypotheses**, resolved by CWN checks where
uncertainty is meaningful. There is **no separate interrogation minigame, no lie-detector stat, and no "detect lie"
button.**

**[PROPOSED]** The three failure modes a session should be able to hit, because they are what makes it interesting:
the anomaly is real and innocent; the anomaly is absent and the subject is lying; the device is right and the
authorisation is wrong.

### 7.6 Equipment catalogue

**[CANON]** The standard set for a trained field officer is practical, rugged, EMP-resistant where possible, modular,
accountable and readily serviceable. **[CANON]** Do **not** invent a separate combat or stat system; map game-use gear
to established CWN/SWN/AWN equipment and scene mechanics.

| item | class | deployment | power / connectivity | data, retention, security | authorisation | existing rule mapping |
|---|---|---|---|---|---|---|
| **Smart credentials** | standard | person | offline-capable, chip + biometric | identity, logged use | role-based | none needed (narrative access; `networks.py` credential check) |
| **Encrypted earpiece / microphone** | standard | person | battery, radio or EuroNET | ephemeral voice | duty | narrative; radio fallback §7.2 |
| **BCI** | standard | person | body power, paired | **neural data — highest tier** | consent for own BCI; §5.1 rung 2a | narrative + permission rung; no new mechanic |
| **Always-on body camera** | standard, **mandatory** | person | battery, HD uplink; local buffer on loss | video + timestamps, tamper-evident, retained per case | duty; access gated per case | Clue/provenance (`investigation.py`) |
| **Cybernetic eyes** (alternative to camera) | optional | person | implant power | as body camera; **not** neural read-out | as body camera + implant licence | `cwn_cyberware.py`; same evidence rules |
| **External cyberdeck** | **standard, mandatory** | person | battery, EuroNET/mobile/radio | case data, logs | case credentials | `cwn_hacking.py`; `networks.py` |
| Implanted cyberdeck | optional | person | implant power | as above, covert | implant licence + case | `cwn_cyberware.py`, `cwn_hacking.py` |
| Rugged tablet interface | optional | person | battery | as above | case | none (an interface, not a capability) |
| **Defensive psychotronic implant** | standard, **at least defensive** | person | implant power | minimal, local | implant licence | `src/rules/psi_access.py`, `psionics.py` (defence is a device property, not a discipline) |
| **Cognitive augmentation** | specialist, varies | person | implant | varies by operator | licence + clearance | `cwn_cyberware.py`; no universal bonus invented |
| **Forensics Multimode Scanner** | standard | person | battery; direct evidence transmit | physical, biological, chemical, digital; chain of custody | case | Investigation scene + `investigation.py` Clue; `cwn_equipment.py` |
| **RFOAS** | specialist / HQ, transportable if documented | interview room or lab | mains; recorded | video + audio + neural; sealed retention | §5.1 rung 2b | Social/Investigation scene + Clue Tags; no new mechanic |
| **Service weapon** | standard | person | — | ballistic record | duty rules of engagement | `data/rules/cwn_equipment.json` firearms, `cwn_combat.py` |
| **Less-lethal assortment** | standard | person | — | use logged | duty | `cwn_equipment.py`, `cwn_special_maneuvers.py` |
| **Protective clothing / armour** | standard by assignment | person | — | — | duty | `data/rules/cwn_equipment.json` armour |
| **First aid, evidence bags, field tools** | standard | person | — | chain of custody for bags | — | `cwn_healing.py`, `cwn_injury_procedure.py` |
| **Police vehicle** | standard | vehicle | hardened power, radio, local storage | vehicle logs, camera footage | duty | `cwn_mission_time.py`; `networks.py` connectivity |
| **Human-controlled drone** | standard | vehicle / HQ | battery, line-of-sight + relay | footage, flight log | duty + airspace | `cwn_drones.py` |
| **PoliisiSanomalaite** | standard | vehicle | vehicle power, encrypted radio | voice/text logs, buffered | duty | §7.2 fallback; no new mechanic |
| **Spare power, shielding, offline storage** | standard | person / vehicle | — | — | — | narrative reliability (§2.1) |

**[CANON]** Specify Tony's and Laura's typical kits without assuming identical cognitive augmentations. **[PROPOSED]**
They differ in *preference*, not in authority: one carries the external deck because they like the screen, the other
runs an implanted deck because they dislike carrying it; both have the defensive implant, the body camera, the
scanner, the service weapon and the radio. Any difference beyond that is a character choice the author has not made.

### 7.7 Field survival, when the city stops working

**[CANON — #1230]** In stable Helsinki, food, water and shelter are assumed and auto-resolved. During outages,
imprisonment, travel, evacuation, siege or infrastructure collapse, supplies become explicit: quantities,
encumbrance, unsafe water, cold, rest, and consequence through **System Strain and physical saves** per AWN
pp. 62–63. Existing module: `src/rules/awn_survival.py`; the book's values must be read from the licensed source, not
paraphrased into mechanics.

---

## 8. Gameplay bridges

**[CANON]** The setting must map onto existing mechanics rather than inventing parallel ones. What exists today:

| concept in this document | existing mechanism | status |
|---|---|---|
| always-on feed, connectivity loss, permission class | `src/world/networks.py` (four connectivity classes, authorisation rungs) | implemented (#1200) |
| evidence, claims, hypotheses | `src/rules/investigation.py` Clue Tags | implemented |
| interview, interrogation, RFOAS | Social / Investigation scenes + Clue Tags | scene-level, no new mechanic |
| hacking, forensic access | `src/rules/cwn_hacking.py` (CWN) | implemented, immutable |
| PSI restrictions, defensive implants, discipline ceiling | `src/rules/psi_access.py` | implemented (#1178) |
| time cost of authorisations, shifts, deadlines | `src/simulation/clock.py`, `scheduler.py` | implemented (#1230 Phase 1) |
| **Dream** as a sixth scene type | — | **not implemented** (#1230 Phase 4, #1152) |
| daily loop, task loop, faction loop, NPC loop | — | **not implemented** (#1230 Phases 2, 6, 7) |
| AWN enclaves, faction turns | `src/rules/swn_faction_assets.py` (assets only) | partial; turns unimplemented |

**Do not claim more than the table.** The setting is ready; most of the loops are not, and a document that says
otherwise is the kind of optimism this issue exists to prevent.

---

## 9. Open decisions and contradictions

1. **Mistral (§4.2).** Licensed containment programme (recommended), classified deviation, or soften #1200? This is
   the single decision that most changes what Plato *is*.
2. **The war's adversary (§1.3).** "Soviet Union" as revanchist self-naming (recommended), two wars, or preserved
   contradiction?
3. **Putin's death (§1.2).** Which details stay contested forever, and is there any document the setting treats as
   authoritative?
4. **Psychotronic scan tier (§5.1).** Is "consciousness scanning" a rung above neural assessment, or the same rung
   used with a higher court?
5. **The LLM ceiling (§3.1).** Is "2026 desktop Gemma 4 31B" a *legal* limit, a *technical* one, or a rule of thumb
   that prosecutors argue about?
6. **Salla's rank and authority (§7).** Can she authorise anything herself, or only request? (The brief implies
   request.)
7. **Laura Wendt's role details.** Her kit, seniority, specialisation and relationship to Tony are **not** specified
   anywhere in the repository; this page deliberately did not invent them.
8. **The radio's real capacity (§7.2).** Are the numbers above acceptable, or should the Sanomalaite be even more
   limited?
9. **The imperial reference (§2.4).** How far the design movement may quote a colonial vocabulary before the text must
   name the critique, not merely permit it.

**Cross-references for editorial reconciliation:** #1200 (Plato, EuroNET, perimeter, ladder), #1113 (Fortress Europe,
chronology), #1114 (Europol Helsinki), #517/#344 (cyberspace after the Crisis, Blackwall, Safenet), #1178 (PSI scope),
#1196 (device PSI), #1230 (loops, clock, Dream scenes), #1121 (Greater Helsinki), #1086 (institutions),
`design/MEDVEDEV.md` (conflicting war draft), `design/POLICE.md` (the author's own brief, the primary source here).

---

## 10. What this document does not do

* It does **not** alter CWN core rules, or any existing rule module.
* It does **not** implement code, a second faction system, a second evidence model or an interrogation mechanic.
* It does **not** present the war, the coup or the intervention as real-world history, or as claims about present-day
  EU law or Europol's actual powers.
* It does **not** resolve the contradictions in §9 — it names them, which is the job of a document written before the
  author has decided.
