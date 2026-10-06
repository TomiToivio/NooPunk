# UNSA Academy: core training, standard augmentations and rookie equipment

> **Status: design specification for issue #158.** This document defines the universal
> **UNSA Police Academy** baseline that every player character graduates with, the
> standard augmentation packages the Agency offers, and the standard rookie field kit.
>
> It uses the canonical universal Skill vocabulary from issue #159
> (`data/rules/skills.json`, `RULEBOOK.md` §4) and the six base STATs from issue #131
> (`RULEBOOK.md` §9.2). It defines **no new universal Skills** and **no new STATs**: where
> the issue lists a candidate skill that canon already folds into another, the fold is
> named explicitly below rather than recreated.
>
> **This entire document is fictional alternate-history lore. Real people, governments,
> companies and institutions are used as fictionalized setting elements; the events
> described here are not claims about real-world history or evidence.**
>
> **Chronology is scenario-local and no future year is assigned.** The setting is **20XX**.
>
> This document does not settle the Cortical Stack question (§10 below records it as
> **deliberately open** and explains why). Names, levels and specific devices remain
> editable while drafting.

---

## 1. Academy concept

UNSA agents are trained simultaneously as:

- law-enforcement officers;
- criminal investigators;
- counterintelligence officers;
- X-risk responders;
- NHI / anomalous-phenomena investigators;
- armed federal agents;
- entry-level cyber operators;
- entry-level psionic operators.

**Design principle: a fresh graduate is already impressively competent.** They are not
ordinary beat cops. The academy baseline should let a day-one agent do real investigative
work, and should stop well short of a specialist in any single domain.

The governing sentence:

> **A UNSA graduate is a competent generalist in eight fields and a specialist in none.**

---

## 2. Method: the academy teaches the canonical Skills at a graduated baseline

Issue #158 asks what every graduate is trained to do, "which NoöPunk skills represent that
training", and the starting levels. The answer is a **baseline tier** applied to the
existing canonical skills — not a parallel academy skill list.

Three baseline tiers are used, on the canonical **1–10** Skill scale (§4):

| Tier | Rating | Meaning |
| --- | --- | --- |
| **Foundation** | **3** | Trained, reliable, unremarkable. The agent can do this unaided under ordinary pressure. |
| **Core** | **4** | Solid professional competence. The agent is genuinely good at this for a graduate. |
| **Emphasis** | **5** | The academy's signature subjects. One step below where a specialist track begins. |

For calibration, `RULEBOOK.md` §10.4's probability pass uses "Professional STAT 6 + Skill
5" as a working professional. A graduate with a relevant STAT of 5–6 and an Emphasis skill
of 5 succeeds at a Difficult (15) task about half the time, and at an Everyday (13) task
most of the time. That is the intended feel: **competent, not miraculous.**

A specialist academy track (§9.4 of the rulebook) then raises a narrow set of skills from
this baseline to 6–7, which is where "professional practitioner" begins.

### 2.1 The fold: candidate skills the issue lists that canon already covers

The issue deliberately over-lists candidates and asks for collapse. The canonical folds
(§4's "Deliberate overlap boundaries") settle most of them:

| Issue's candidate | Canonical home | Why |
| --- | --- | --- |
| **Law** | **Know (Law)** | §4: "Law is not a separate Skill." |
| **Police Procedure** | **Work (Police Officer)** + Know (Law) + Investigation | §4 names this fold explicitly. |
| **Observation / Perception** | **Perceive** | Already canonical, PSY-based; augmented vision modes use it. |
| **Interrogation / Interview** | **Talk** + Kinesics + Deceive + Provoke | §4: "Interview and Interrogation are not separate Skills" — method chooses the skill. |
| **HUMINT** | **Connect** + Talk + Kinesics + Counterintelligence | Source handling is the social skills applied to intelligence work. |
| **OSINT** | **Research** (+ Know fields) | §4: "OSINT is not a separate Skill." |
| **Deception / Detect Deception** | **Deceive** (to lie) / **Kinesics** (to detect) | Social applications, not independent skills. |
| **Cryptography** | **Know (Cryptography)** as a field, **Program** to implement | No standalone skill; §4 keeps fielded depth in Know. |
| **Networks** | **Interface** (operate) + **Infosec** (attack/defend) | Splitting operation from security is already the canonical boundary. |
| **Cybertech** | **Hardware (Cyberware)** | Hardware is the fielded skill for building and repairing technology. |
| **Hacking** | **Infosec** | Canonical intrusion/exploitation skill. |
| **Unarmed Combat** | **Unarmed** | Canonical. |
| **Melee Weapons** | **Melee** | Canonical; the stun baton is a Melee weapon. |
| **Athletics / Fitness** | **Athletics** (FIT) | Canonical. |
| **X-Risk / NHI Studies** | **Know (X-Risk Studies)**, **Know (NHI Studies)** | Fields of Know, per §4's example list. |
| **Forensics** | **Forensics** | Canonical, and already covers "physical, biological, digital, cybernetic and anomalous evidence". |
| **Psionics** | The PSY skills: **Psychic Defence**, **ESP**, **Telepathy**, **Noöspace** | §4: "Psychic Attack is not a separate Skill." There is no single "Psionics" skill. |
| **Tactics** | **Tactics** | Canonical, INT-based, untrained-forbidden. |

**The result:** the issue's ~17-candidate list collapses to the canonical vocabulary with
**zero additions**. That is the correct outcome; §16 of the issue asks for a clean list
"without recreating Cyberpunk RED's enormous catalogue."

---

## 3. Universal academy skill package

Every UNSA graduate leaves the academy with the following. Ratings are the baseline tier
from §2.

### 3.1 Combat and officer survival

| Skill | Stat | Tier | Rating |
| --- | --- | --- | --- |
| **Guns** | REF | Emphasis | 5 |
| **Unarmed** | FIT | Core | 4 |
| **Melee** | FIT | Core | 4 |
| **Athletics** | FIT | Core | 4 |
| **Fray** | REF | Core | 4 |
| **Tactics** | INT | Foundation | 3 |
| **First Aid** | INT | Core | 4 |

**Sidearms first.** The issue is explicit that graduates are competent with a sidearm and
familiar with long arms. `Guns` is one skill, so the sidearm emphasis is a **fiction and
equipment** matter, not a second skill: the graduate has the rating, and long-arm use is
covered by the same rating with the usual situational handling.

**On `Tactics`** — the issue asks whether it should be universal or specialist. The answer
here: **Foundation (3), universal.** Reason: §4 makes `Tactics` untrained-forbidden, so a
graduate with no rating could not attempt room entry or ambush recognition at all, which
contradicts "armed federal agent". Rating 3 keeps the SWAT track (6–7) clearly meaningful
while letting a graduate do basic team movement. **Basic arrest operations are not Tactics
at all** — they are `Unarmed` plus `Work (Police Officer)`.

**On `Fray`** — added to the issue's list deliberately. A police officer's survival skill is
not only shooting; §4 gives `Fray` the dodging and immediate-danger reaction, which is what
"surviving close-quarters attacks" actually tests.

### 3.2 Basic law-enforcement work

| Skill | Stat | Tier | Rating |
| --- | --- | --- | --- |
| **Investigation** | INT | Emphasis | 5 |
| **Perceive** | PSY | Emphasis | 5 |
| **Work (Police Officer)** | Variable | Emphasis | 5 |
| **Forensics** | INT | Core | 4 |
| **Know (Law)** | INT | Core | 4 |
| **Sneak** | REF | Foundation | 3 |
| **Pilot (Ground Vehicles)** | REF | Foundation | 3 |

Notes:

- **`Investigation` and `Perceive` are the academy's signature subjects.** The whole
  campaign is investigation (§ #162), so these are the two Emphasis skills every graduate
  shares. This is the single most important calibration decision in this document.
- **`Work (Police Officer)`** carries arrests, report writing, chain of custody and
  coordination with local police — the issue's "Police Procedure", folded per §4.
- **`Know (Law)`** carries criminal procedure, arrest powers, evidence rules, warrants,
  UNSA jurisdiction and NHI/X-risk emergency authorities. It is a field of `Know`, so a
  graduate who later becomes a prosecutor's liaison can deepen it.
- **`Surveillance`** folds into `Sneak` (physical) + `Perceive` (observation) + `Research`
  and `Interface` (camera and drone networks). §4 gives no standalone surveillance skill,
  and creating one would be exactly the proliferation the issue warns against. **Physical
  countersurveillance is `Sneak` opposed by the observer's `Perceive`; camera-network work
  is `Infosec` + `Interface`.**
- **`Pilot (Ground Vehicles)`** is included because a field agent drives. It is Foundation
  so it does not encroach on the TECH track's `Pilot (Drones)` / `Pilot (Aircraft)`.

### 3.3 Basic intelligence and counterintelligence

| Skill | Stat | Tier | Rating |
| --- | --- | --- | --- |
| **Intelligence Analysis** | INT | Core | 4 |
| **Counterintelligence** | INT | Core | 4 |
| **Research** | INT | Core | 4 |
| **Talk** | SOC | Core | 4 |
| **Kinesics** | SOC | Foundation | 3 |
| **Deceive** | SOC | Foundation | 3 |
| **Connect** | SOC | Foundation | 3 |

Notes:

- **`Intelligence Analysis` and `Counterintelligence` are Core but not Emphasis.** The
  issue asks what "every elite federal counterintelligence officer knows even if they are
  not an analyst or case officer" — that is source evaluation, uncertainty estimation,
  competing hypotheses, insider-threat recognition and deception awareness. It is not the
  full analyst's tradecraft, which is the Intelligence-analyst specialist track.
- **`Talk` at Core** covers ordinary interviewing and rapport. Hostile interrogation is
  `Provoke` + `Deceive` + `Kinesics`, which the graduate has only at Foundation — so a
  graduate can conduct an interview, but a skilled interrogation is visibly a specialist
  activity. That gap is deliberate and is where the social specialist tracks earn their
  place.

### 3.4 X-risk and NHI training

| Skill | Stat | Tier | Rating |
| --- | --- | --- | --- |
| **Know (X-Risk Studies)** | INT | Core | 4 |
| **Know (NHI Studies)** | INT | Core | 4 |
| **Survival** | INT | Foundation | 3 |

Notes:

- **`Containment Protocols` and `Information-Hazard Awareness` fold into `Know (X-Risk
  Studies)`.** Both are bodies of learned procedure, and §4 puts learned domain knowledge
  in `Know`. Executing a containment procedure is `Know (X-Risk Studies)` + the relevant
  practical skill (`Hardware`, `First Aid`, `Investigation`).
- **`Anomalous Phenomena Investigation` folds into `Investigation` + `Know (NHI Studies)`.**
  The issue itself suggests this may be "a single broad academy skill such as
  Anomalistics" — but that skill does not exist in canon, and distinguishing fraud from
  genuine anomaly *is* what `Investigation` does (`RULEBOOK.md` §4: "reconstructing
  events, following evidence, generating hypotheses"). **Do not create `Anomalistics`.**
- **`Know (NHI Studies)` is the field that carries contact protocols, evidence
  preservation, avoiding anthropocentric assumptions and memetic/psychic contamination
  precautions.** Issue #158's own §4 asks whether this becomes one broad skill; the answer
  is that it is already one field of an existing skill.

### 3.5 Basic cyber training

| Skill | Stat | Tier | Rating |
| --- | --- | --- | --- |
| **Interface** | CYB | Core | 4 |
| **Infosec** | CYB | Foundation | 3 |
| **Program** | CYB | Foundation | 3 |
| **Hardware (Cyberware)** | CYB | Foundation | 3 |

Notes:

- **The issue's own calibration is adopted verbatim:** "academy-level hacking should make
  an agent dangerous to ordinary civilian systems but nowhere near a specialist
  netrunner." `Infosec 3` against a hardened corporate target is not a serious attempt,
  which is correct.
- **`Interface` is Core because every graduate operates a BCI, a cyberdeck, drones and
  the AI assistant.** Operating is not attacking.
- The issue asks how much of this belongs to **CYB** rather than skills. The answer:
  **CYB is the aptitude; the skills are the trained tradecraft; computer hardware
  statistics are the equipment.** This is the same three-way split `rulebook/2_ATTRIBUTES.md` (§"Cybernetic hardware statistics")
  establishes for the cybernetic layer, and the academy package is consistent with it.
  A graduate with CYB 5, Interface 4 and Infosec 3 is a competent operator and a poor
  intruder, which is exactly the intent.

### 3.6 Basic psionics training

| Skill | Stat | Tier | Rating |
| --- | --- | --- | --- |
| **Psychic Defence** | PSY | Core | 4 |
| **ESP** | PSY | Foundation | 3 |
| **Noöspace** | PSY | Foundation | 3 |

Notes:

- **`Psychic Defence` at Core is the load-bearing decision.** The issue wants every
  graduate "harder to psychically dominate without turning every graduate into a full
  psionic operative". Psychic Defence is the resistance skill (§4), so the baseline is
  *defensive competence*, and it is the academy's third signature subject.
- **There is no `Psionics` skill.** §4 lists four PSY skills (Psychic Defence, ESP,
  Telepathy, Noöspace, plus Precognition and Psychokinesis). A universal "Psionics" skill
  would duplicate them. **Telepathy, Precognition and Psychokinesis are deliberately NOT
  in the universal package** — they require the PSI specialist track, natural talent, or
  awakening. This is what keeps the baseline from creating a cadre of psychics.
- **A non-psionic graduate cannot use `ESP` or `Noöspace` meaningfully even at 3** unless
  they have PSY potential. The ratings represent *training in what the phenomena are and
  how to behave around them*, and the GM should treat them as "knows the procedure"
  rather than "can do the thing" for a PSY-ordinary character. This is the honest reading
  of the issue's requirement that elementary psionic training be universal: **everyone
  learns to recognise and not panic; almost no one learns to do.**

### 3.7 The complete package, in one table

Fifteen canonical skills. No additions.

| Skill | Stat | Rating |
| --- | --- | --- |
| Guns | REF | 5 |
| Investigation | INT | 5 |
| Perceive | PSY | 5 |
| Work (Police Officer) | Variable | 5 |
| Unarmed | FIT | 4 |
| Melee | FIT | 4 |
| Athletics | FIT | 4 |
| Fray | REF | 4 |
| First Aid | INT | 4 |
| Forensics | INT | 4 |
| Know (Law) | INT | 4 |
| Intelligence Analysis | INT | 4 |
| Counterintelligence | INT | 4 |
| Research | INT | 4 |
| Talk | SOC | 4 |
| Interface | CYB | 4 |
| Psychic Defence | PSY | 4 |
| Know (X-Risk Studies) | INT | 4 |
| Know (NHI Studies) | INT | 4 |
| Tactics | INT | 3 |
| Sneak | REF | 3 |
| Pilot (Ground Vehicles) | REF | 3 |
| Kinesics | SOC | 3 |
| Deceive | SOC | 3 |
| Connect | SOC | 3 |
| Survival | INT | 3 |
| Infosec | CYB | 3 |
| Program | CYB | 3 |
| Hardware (Cyberware) | CYB | 3 |
| ESP | PSY | 3 |
| Noöspace | PSY | 3 |

**Calibration check against §16 of the issue.** A graduate can: arrest a suspect (Unarmed +
Work (Police Officer)); shoot competently (Guns 5); defend themselves (Fray 4, Unarmed 4);
investigate a crime scene (Investigation 5, Forensics 4, Perceive 5); interview witnesses
(Talk 4, Kinesics 3); recognise bad evidence (Investigation 5, Forensics 4); perform basic
forensic work (Forensics 4); analyse an intelligence problem (Intelligence Analysis 4);
recognise surveillance or hostile intelligence activity (Counterintelligence 4, Perceive 5);
perform basic cyber operations (Interface 4, Infosec 3); defend against basic psychic
attack (Psychic Defence 4); recognise an NHI/X-risk incident (Know fields 4); use advanced
augmented sensors (Perceive 5, Interface 4); work securely with AI and networked systems
(Interface 4, Infosec 3).

And they do **not** equal a SWAT operator (Tactics 3 vs 6–7), master hacker (Infosec 3 vs
6–7), professional psychic (no Telepathy/Psychokinesis), senior analyst (Intelligence
Analysis 4 vs 6–7), surgeon (no Medicine) or forensic scientist (Forensics 4 vs 6–7).

**This is the issue's §16 design target, satisfied on the existing skill list.**

---

## 4. Starting level summary and the specialist hand-off

- **Universal baseline:** the 31 rows in §3.7.
- **Specialist tracks** (rulebook §9.4: SWAT, PSI, TECH, NHI Academy) raise a narrow set of
  these to **6–7** and add the fields they need. The tracks are defined separately; this
  document fixes only the shared floor.
- **STATs are not granted by the academy.** The six STATs are the character's own aptitude
  (§9.2), assigned in Lifepath; the academy grants Skills.
- **Untrained-forbidden skills remain untrained-forbidden.** A graduate with no `Medicine`,
  `Exotic Skill` or `Telepathy` rating may not attempt them; §4 governs, and the academy
  does not create an exception.

---

## 5. Standard cybernetic augmentation package

A new graduate is offered the following government suite. It may include technology not
available on civilian markets. **Implants are offered, never compulsory** (§7).

### 5.1 Wireless BCI
Secure encrypted neural interface; silent communications; HUD/AR; direct control of
equipment; AI copilot access.

**Rules effect: none beyond enabling use.** The BCI is what lets the character use
`Interface` hands-free and receive the AI assistant's output. It grants no Skill rating and
no bonus — it removes the "you need a keyboard" obstacle. This is deliberate: the issue's
own principle is that technology should deepen investigation rather than trivialise it.

### 5.2 Cybernetic compute package
Modest compute, network and interface capability; encrypted local storage; a secure AI
runtime.

**Rules effect.** This is the character's **computer hardware** — and `RULEBOOK.md` §9.2
with `rulebook/2_ATTRIBUTES.md` is explicit that **COMPUTE / INTERFACE / NETWORK / STORAGE /
HARDENING are equipment statistics, not character attributes.** The academy package therefore has a **hardware
profile**, recorded with the gear, exactly as a weapon has a damage rating. A character's
cyberspace capability is `CYB + Skill + this hardware`.

**Because the issue's own §5 asks whether COMPUTE/INTERFACE/NETWORK are character stats:
they are not, and the academy does not create a second stat block.** The hardware profile
is the answer.

### 5.3 Intelligence augmentation
Memory assistance; semantic search; attention management; live translation; evidence
cross-referencing; probabilistic and analytical support.

**Rules effect: it is the AI assistant (§6).** The intelligence augmentation is the
hardware substrate for the embedded agent, and its capabilities are the agent's
capabilities, not a bonus to the character's `INT` or `Research`. **Do not grant a
skill bonus.**

### 5.4 Augmented vision — the forensic sensorium
This is the **defining equipment of the setting** and the issue's §17 tri-layer vision.

Three overlays, each toggled, filtered or combined:

1. **Physical** — low-light, infrared, ultraviolet, magnification, polarization,
   multispectral, lidar/depth, biometric highlighting, trace-evidence enhancement,
   chemical/particulate visualisation, blood/bodily-fluid detection, material stress and
   damage visualisation, trajectory reconstruction, facial/gait identification,
   cybernetic-device detection, wireless-emission visualisation.
2. **Cyber** — AR overlays, local network topology, nearby wireless devices, connected
   cyberware, cameras/drones/access points/vehicles/smart infrastructure, device ownership
   and trust status, UNSA database overlays, potential intrusion targets.
3. **Astral / Noetic** — enabled by the psychotronic implant: perception of noetic
   presences, psychic residues where detectable, hostile psychic influence, anomalous
   entities, possible Noöspace bleed-through.

**Rules effect, and the crucial constraint:** every mode is an **information channel, not
an answer.** `Perceive` is the skill that reads them, and §8 below applies — **no single
sensory channel is definitive, and the Astral overlay is the least reliable of the three.**
The tri-layer view is the setting's signature interface *because* it creates the game's
central question ("which layer do you trust?") rather than settling it.

**Platform question from the issue (implant vs contacts vs glasses vs variable):** the
academy offers **all four**, and the choice is a character decision, not a rules one —
implanted (best integration, worst hacking exposure), smart contacts (middle), external
glasses or visor (least invasive, vulnerable to removal), or a platform that varies by
mission. **All four grant the same information; they differ in vulnerability and
convenience.** This keeps §7's biological-purity option genuinely playable.

### 5.5 The augmented-vision constraint

> **Augmented vision never authorises action on its own.**

An overlay can show a heat signature, a network node or a noetic residue. It cannot show
whether the person is hostile, whether the node is a trap, or whether the residue is
current. The **Triangulate-Reality doctrine** applies (see
`docs/design/INVESTIGATION_FANTASY.md` §6–§7): **triangulate reality before acting.**

---

## 6. The embedded AI agent

Every standard agent has a persistent AI assistant monitoring their sensory feeds and
cybernetic systems.

### 6.1 What it is — and what it must not be

**It is not an AGI.** The issue is explicit, and the specification is:

> **a highly capable but deliberately limited multimodal model, somewhat below 2026
> frontier multimodal LLM capability, combined with advanced narrow-AI tools.**

This is a deliberate **de-powering** relative to the real 2026 frontier, and it is the
single most important design decision in this document. The AI is **an extraordinary
instrument, not the detective.**

### 6.2 Capabilities

Curated domain knowledge: forensic science, criminal investigation, law and police
procedure, medicine/emergency triage, biometrics, weapons, cyber forensics, network
analysis, languages, known NHI incidents, psychotronic signatures, evidence handling,
institutional databases.

Specialised tools that exceed its general reasoning: spectral analysis, biometrics,
trajectory reconstruction, voice comparison, packet analysis, anomaly detection, forensic
imaging, psychotronic sensor processing.

Operational support: observation support, note-taking, transcription, evidence indexing,
translation, database queries, tactical warnings, memory assistance, report drafting,
forensic triage, cyber threat detection, scheduling and procedural reminders.

### 6.3 The failure modes (which is where the gameplay is)

The AI **can** say:

> "Observed pattern is consistent with three known Orion-associated incidents."

It **must not** safely conclude:

> "Therefore this person is an Orion operative. Shoot them."

It can misclassify, lack context, generate false positives, be fooled, be disconnected, be
legally restricted, and encounter genuinely anomalous phenomena outside its models.

### 6.4 What the AI is legally forbidden to do

The issue asks this directly. The answer:

> **The AI may not make any decision that the law reserves to a sworn human officer.**

Concretely, it may not:

- authorise or recommend **lethal force** (it may report sensor state; it may not say
  "shoot");
- make an **arrest decision**;
- declare a legal **classification** (human / non-human / synthetic) for record purposes;
- authorise an **intrusion**, a **warrantless search**, or a **containment action**;
- override a human officer's judgement;
- act autonomously as an agent in the field.

It **may** flag, warn, recommend avoidance, request human review, and refuse an
irreversible action. This is the "recommendation: avoid irreversible decisions" behaviour
the issue's HUD example shows, and it is why its most common useful output is a warning
rather than a conclusion.

**Why:** because the setting's central question is *"which version of reality is true?"*
If an unaccountable model could answer it, the game would end. The legal restriction is
both a setting-flavour element and the mechanical guarantee that the human remains the
detective.

### 6.5 Continuous sensory streaming

Feeds may stream to the local AI, remote UNSA AI systems, a human controller, and
authorised team members. In some missions or jurisdictions streaming is **compulsory**
(accountability, evidence integrity, officer safety, X-risk monitoring); in others it is
denied or degraded. This is a **scene-level dial**, not a fixed rule, and it is the
mechanism by which the setting raises privacy, oversight and compromised-command tension.

---

## 7. Standard psychotronic augmentation package

Modest baseline abilities, not a psionic career:

- basic ESP augmentation;
- perception of obvious noetic presences;
- detection of strong psychic anomalies;
- warning of some forms of psychic intrusion;
- modest psychic defence;
- stabilisation and grounding assistance;
- interface with psychotronic equipment.

**Rules effect: it is `Psychic Defence`'s and the Astral overlay's hardware substrate.** It
grants **no PSI skill rating** and **no advanced psionic powers**. Powerful abilities
require additional specialist implants, natural talent, psionic skills, training, or
unusual exposure/awakening.

The intended baseline, in the issue's own words:

> **Every UNSA agent can notice that something psychic is happening and has some
> protection against it. A true psionic specialist can actually do something sophisticated
> about it.**

### 7.1 Other enhancement options

The academy routinely offers, and characters may accept or decline individually:
cognitive gene therapy, accelerated-learning treatment, neural-plasticity enhancement,
memory enhancement, stress-resilience enhancement, anti-fatigue treatment, physical gene
therapy, reflex enhancement, toxin/radiation resistance, endocrine control, enhanced
healing.

**All are reversible or non-implant where physically possible**, which is what makes §8
work. **Rules effect: none of these grants a Skill or STAT rating.** They are narrative and
equipment-layer colour; a graduated-learning treatment does not raise `Know`. Mechanically
granting bonuses here would let a player buy competence the academy's calibration
deliberately withholds.

---

## 8. Biological-purity and no-implant characters

Implants are common but **not compulsory**. Refusal is normal in NoöPunk for philosophical,
religious, political, medical, privacy or security reasons.

UNSA must therefore provide **non-invasive equivalents**:

- AR glasses or a visor;
- smart contact lenses;
- an external BCI headband/collar;
- wearable psychotronics;
- a handheld forensic scanner;
- a hardened phone or cyberdeck;
- a dedicated AI-assistant device.

**A purely biological PC is fully playable and receives the same information** — the same
tri-layer overlays, the same AI support, the same forensic sensorium. The **trade** is:

| | Implanted | Non-invasive |
| --- | --- | --- |
| Integration and convenience | high (silent, hands-free, always-on) | lower (gear can be removed, seized or lost) |
| Attack surface | larger (cyberware can be hacked, tracked, spoofed) | smaller (nothing inside to hack) |
| Vulnerability to removal | none | real (the visor can be taken) |
| Vulnerability to psychic/cyber intrusion | higher exposure | reduced exposure |

**This is a genuine trade, not a penalty.** The biological character is harder to hack and
harder to spoof; the augmented character is faster and better integrated. Neither is
strictly better, which is what keeps the choice meaningful.

---

## 9. Standard rookie field equipment

### 9.1 Weapons
Service firearm; spare magazines; stun baton/club (`Melee`); a less-lethal weapon;
restraints.

### 9.2 Protection
Concealable ballistic vest; heavier tactical armour when required; eye/hearing protection;
environmental mask/respirator.

### 9.3 Identification and police equipment
UNSA credentials; badge; encrypted comms; restraints; evidence bags; forensic sampling
tools; body camera/sensor recorder; flashlight.

### 9.4 Investigation
Portable forensic scanner; evidence collection kit; compact drone; secure tablet/cyberdeck
(if implants refused); augmented-vision hardware (if not implanted).

### 9.5 X-risk / NHI kit
Psychotronic detector; anomalous-material container; emergency neural/psychic shielding;
radiation/chemical/biological sensors; isolation bag/mini containment system; a hardened
"do not connect this to the network" storage device.

### 9.6 Equipment design principle

From the issue, adopted verbatim as the test for any future addition:

> **UNSA gear should make a rookie feel like an elite near-future investigator without
> eliminating player agency.**

It should expand what the character can perceive, provide better evidence, connect the
character to powerful institutions, create new tactical options, introduce cyber and
psychic vulnerabilities, generate legal and ethical constraints, and sometimes overwhelm
the character with too much information.

The target feel is **not** "magic gadget solves scene" but:

> **You can see far more than a contemporary investigator, but now you must decide which
> layer of reality you trust.**

### 9.7 Research note (honest status)

The issue asks for "a research/design pass on what modern federal agents and detectives
actually carry, then extrapolate it into NoöPunk." **That pass has not been done.** The
lists above are the issue's own suggestions, organised and de-duplicated; the items are
plausible extrapolations and **have not been checked against real current federal-agent
kits**. This is recorded so a later contributor does not mistake the list for a researched
inventory. Doing that pass properly is a follow-up, not something to be inferred here.

---

## 10. The Cortical Stack question

**Decision: deliberately open. This document does not settle it.**

The issue asks whether a cortical stack or equivalent backup is standard, optional,
restricted, or unreliable, and warns that the answer "radically changes the stakes of
death". That is exactly why it cannot be settled inside an equipment document.

What canon already establishes, and what constrains any answer:

- **Cortical stacks exist in the setting.** `RULEBOOK.md` §33 records that roughly **25% of
  humanity** has one, and roughly half of those have resleeved at least once.
- **Adoption varies radically** by region, class, ideology, religion and legal regime
  (glossary: *Cortical stack*).
- **Cortical-stack continuity, full resleeving, morph catalogs, forks/backups and
  infomorph edge cases are explicitly deferred** by `RULEBOOK.md` §9.4 pending a
  deliberate design pass.
- **The metaphysics is unresolved in-world.** The glossary states plainly that
  "informational continuity can be verified more easily than continuity of consciousness",
  and gives the fork/merge/backup vocabulary precisely to keep that question live.

**The tension the author must resolve:** if every UNSA graduate is routinely backed up,
then death becomes an equipment failure — which is coherent for the setting but removes
the stakes from an investigation game whose whole theme is that advanced technology does
not remove uncertainty. If backup is restricted or unreliable, death keeps its weight but
elite agents are oddly unprotected relative to 25% of humanity.

**Recommended shape (offered, not imposed):** UNSA offers stacks as an **opt-in with
caveats** — standard-issue hardware, but restoration is **legally and Noetically
contested**, and the "is it you?" question is not answered. That keeps both the
capability and the uncertainty, which is the setting's signature.

**This is a decision for the author.** It is recorded here as open, with the constraints,
so that a later session does not quietly pick one.

---

## 11. The UNSA police uniform

Field agents normally wear civilian clothes or operate undercover. The formal uniform is
mostly used for ceremonies; public-order duties; visible policing; situations where federal
authority must be unmistakable; and temporary assignment to ordinary police work.

Academy culture:

> Being told to put the uniform back on is associated with rookies, routine assignments, or
> an experienced agent being dumped back into boring ordinary police work after screwing
> something up.

This is a running setting joke. **It must not make uniformed policing itself incompetent or
unserious** — the joke is about the *agent's* status, not the *work*.

---

## 12. Fictional competency references

Design prompts, **not** conversion targets. None of these characters or organizations is
imported into canon.

| Reference | Competency areas to examine | What it is useful for |
| --- | --- | --- |
| **Rick Deckard** (*Blade Runner*) | investigation, interviewing, interrogation, observation, recognising artificial/non-human persons, firearms, pursuit, street knowledge, evidence interpretation, reading behaviour | the detective hunting entities that may look completely human |
| **Mulder** (*The X-Files*) | investigation, anomalistics, profiling, intelligence analysis, interviewing, theory-building, recognising patterns others dismiss, NHI/paranormal knowledge, fieldcraft | the anomalous investigator / intelligence analyst archetype |
| **Scully** (*The X-Files*) | investigation, medicine, pathology, forensics, scientific reasoning, firearms, interviewing, evidence evaluation, skeptical hypothesis testing | keeping anomaly investigation grounded in forensic and scientific method even where strange things are real |
| **Men in Black** | investigation, NHI recognition, counterintelligence, concealment/cover stories, advanced technology use, firearms, pursuit, interrogation, contact protocol, anomalous evidence handling, public-information control | the federal NHI containment / secrecy / response agency dimension |

**The Scully row is the load-bearing one.** It is the design constraint that stops the
Triangulate-Reality doctrine (§5.5) from becoming an excuse for credulity: an anomaly that
is real still has to be established forensically.

---

## 13. Deliverables checklist

- [x] Review the current NoöPunk skill list and map academy competencies onto existing skills — §2.1, the fold table.
- [x] Avoid unnecessary skill proliferation — §2.1; **zero new skills**.
- [x] Define the universal UNSA academy skill package — §3.7.
- [x] Define starting proficiency levels — §2 (three tiers, 3/4/5) and §3.7.
- [x] Define specialist academy tracks separately — §4 (hand-off; tracks defined in rulebook §9.4).
- [x] Define standard cybernetic augmentation package — §5.
- [x] Define standard psychotronic augmentation package — §7.
- [x] Define augmented-vision forensic modes — §5.4, and the tri-layer model.
- [ ] Decide Cortical Stack / backup status — **§10: deliberately open, escalated to the author** with the constraints.
- [x] Define non-invasive alternatives for biological-purity characters — §8.
- [x] Define standard rookie field equipment — §9.
- [x] Use Blade Runner, The X-Files, Men in Black and Observer as design references — §12; Observer explicitly in §5.4.
- [x] Integrate the final decisions into character creation and the default campaign academy background — §3.7 is the package; the Lifepath step "UNSA Police Academy basic training" (`RULEBOOK.md` §9.1, step 13) applies it.

**Two items are deliberately not closed:** the Cortical Stack question (§10) and the
real-world equipment research pass (§9.7). Both are flagged rather than silently resolved.
