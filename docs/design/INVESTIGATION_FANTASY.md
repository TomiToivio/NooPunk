# Investigation fantasy: the default NoöPunk investigative cell and loop

> **Status: design specification for issue #162.** This document captures the default
> NoöPunk player fantasy and investigation loop: the distributed investigative cell
> (field investigator, partner, controller, embedded AI), the four layers of a crime
> scene, the NHI detection-and-classification protocol, the lethal-force doctrine, and
> the recurring antagonism of the Orion-associated Men in Black.
>
> It builds on `RULEBOOK.md` §38 (UNSA), §4 (the canonical Skills, issue #159),
> `docs/design/UNSA_ACADEMY.md` (issue #158, the graduate baseline) and
> `FACTIONS.md` / `rulebook/8_FACTIONS.md`.
>
> **This entire document is fictional alternate-history lore. Real people, governments,
> companies and institutions are used as fictionalized setting elements; the events
> described here are not claims about real-world history or evidence.**
>
> **Chronology is scenario-local and no future year is assigned.** The setting is **20XX**.
>
> **This entire document is fiction, including the design references.** *Blade Runner*,
> *The X-Files*, *Ubik*, *Men in Black*, *Cyberpunk 2077*, *Disco Elysium*, *Nobody Wants
> to Die* and *Observer* are named as creative prompts only. **Nothing is imported from
> them**: no characters, factions, terminology, mechanics or text. NoöPunk is an
> independent system.

---

## 1. The pitch

> **NoöPunk is a cyberpunk paranormal-investigation RPG. You are a post-Singularity
> anomalous-threat investigator hunting dangerous non-human intelligences across physical
> reality, cyberspace, social networks and Noöspace. Think Blade Runner and The X-Files
> with Ubik psionics and Cyberpunk 2077 hacking.**

Or, more concretely:

> **A Blade Runner-style detective with a partner, a controller and a limited forensic AI
> investigates NHI, cybercrime and psychic threats in post-Singularity Europe.**

**The core role is not a generic cyberpunk adventurer.** It is a **post-Singularity
anomalous-threat investigator** operating where crime, intelligence, AI, cybernetics,
psionics and NHI overlap.

---

## 2. The default case shape: one scene, four layers

A normal case begins with something mundane — murder, a missing person, a hacked implant, a
corporate intrusion, an unidentified drone, cult activity, an intelligence leak, an
anomalous body, strange surveillance footage. It then opens into overlapping layers.

**The major NoöPunk signature: the same crime scene exists simultaneously across all four
layers.** The investigator's central skill is moving between them and reconciling what they
disagree about.

| Layer | What lives there | Canonical skills that read it |
| --- | --- | --- |
| **Physical** | bodies, crime scenes, residue, vehicles, buildings, weapons, movement, ordinary forensic evidence | **Perceive**, **Investigation**, **Forensics**, **First Aid**, **Medicine** |
| **Cyber** | local networks, cameras, implants, drones, access points, AIs, logs, malware, data trails | **Infosec**, **Interface**, **Program**, **Hardware**, **Research** |
| **Social** | factions, contacts, institutions, ideologies, cults, corporations, intelligence services, reputation | **Talk**, **Kinesics**, **Connect**, **Deceive**, **Provoke**, **Counterintelligence**, **Intelligence Analysis** |
| **Psychic / Noöspace** | psychic signatures, remote influence, possession/control, anomalous entities, altered perception, consciousness-level effects | **Psychic Defence**, **ESP**, **Telepathy**, **Noöspace**, **Perceive** |

**Why four and not one:** canon already divides the world this way (`RULEBOOK.md` §36, the
four Luhmannian systems). The investigation loop is the **gameplay application** of that
ontology: the four layers are the four systems, seen from a crime scene. This document
adds no fifth layer and no new ontology.

**The `Cyber` layer maps to the Cybernetic system** and the `Psychic` layer to the Psychic
system; as `rulebook/2_ATTRIBUTES.md` ("Cybernetic hardware statistics") notes, the
cybernetic layer is the one where the *equipment* matters more
than the character — which is exactly why a cyber investigation is read through
`Infosec`/`Interface` plus hardware.

---

## 3. The default investigative cell

**The player character should normally not work alone.** The cell has four roles, and the
whole architecture exists to make the setting's central uncertainty survivable *and*
dramatic.

### 3.1 Player character — the field investigator

Physically present at the scene. Makes the judgement calls and remains the actual
protagonist. **The player is always the one who decides.** Every other role exists to
inform, challenge or support that decision, never to replace it.

### 3.2 Partner — the reality anchor

A permanent or semi-permanent field partner, closer to a long-term investigative
counterpart than to a disposable squadmate.

Functions:

- independent witness;
- second opinion;
- backup in dangerous encounters;
- challenge the player's interpretations;
- repeat scans independently;
- **sanity/reality anchor during psychic or psychotronic attacks**;
- a social relationship that evolves over the campaign.

> **The partner is essential because the player's own perception can become compromised.**

The defining exchange:

> **PC:** "There is someone standing in the doorway."
>
> **Partner:** "There is no doorway."

**Mechanically:** the partner is the second `Perceive`/`Investigation` reading that the
Triangulate-Reality doctrine (§7) requires. The partner is **not** a second player and does
not get a turn economy — they are a fiction-forward reality check whose **independent
observation is evidence**, and whose disagreement is a mechanical signal that the scene
needs triangulation.

**The partner must not be an oracle.** They can be wrong, tired, frightened, compromised, or
absent. A partner who is always right would be the AI problem (§4) in a human costume.

### 3.3 Controller — the remote operator

A remote institutional operator / dispatcher.

Functions: police and intelligence databases; legal support; warrants and procedure;
satellite and camera feeds; tactical coordination; NHI case archives; coordination with
backup; mission control.

**The controller is also a source of uncertainty.** Communications can be intercepted,
spoofed, censored, or institutionally compromised — which is the hook for the Men in Black
(§8) and for the campaign's institutional-paranoia thread.

**Mechanically:** the controller is the channel through which `Research`,
`Intelligence Analysis`, `Know (Law)` and database access arrive **without the investigator
being at a desk**. A controller is one of the two channels that can satisfy the
Triangulate-Reality requirement (§7) — and, critically, **a compromised controller can
supply a false confirmation.**

**One controller supervises several agents.** The issue is explicit that the controller is
not an omnipresent personal handler; this preserves the sense that the cell is a unit
inside a larger institution, not a private army.

### 3.4 Embedded AI agent — the instrument

An always-available AI assistant.

> **It must not be an AGI.**

It is a highly capable but deliberately limited multimodal model, **somewhat below 2026
frontier multimodal LLM capability**, combined with advanced narrow-AI tools. Full
specification — capabilities, failure modes, and what it is legally forbidden to do — is in
`docs/design/UNSA_ACADEMY.md` §6. The load-bearing points:

- it has excellent **curated domain knowledge** and specialised tools that exceed its
  general reasoning (spectral analysis, trajectory reconstruction, packet analysis,
  psychotronic sensor processing, and so on);
- it is **an extraordinary instrument, not the detective**;
- it can flag that an observed pattern "is consistent with three known Orion-associated
  incidents"; it **must not** conclude "therefore this person is an Orion operative".

**The AI is the fourth role and the weakest authority.** Its most useful output is a
warning, not an answer, and it is legally barred from any decision reserved to a sworn
human officer.

---

## 4. NHI detection is not an instant-answer button

This is the design rule that keeps the whole genre from collapsing.

Cybernetics and psychotronics may be **very good at detecting anomalies**. They must **not**
identify every NHI with certainty.

**What sensors may report:** non-baseline cognition; anomalous neural telemetry; possible
nonlocal coupling; abnormal psi-field activity; biometric inconsistency; unknown cybernetic
architecture; probability and confidence scores.

**What can produce a false positive or an ambiguous classification:**

- human psychics;
- transhumans;
- uploaded humans;
- AGIs using biological or synthetic bodies;
- hybrids;
- possession;
- remote control;
- psychotronic influence;
- deliberate sensor spoofing;
- Orion operations;
- damaged or compromised sensors.

**Therefore the question is never "Is this NHI?"** It is:

> **"What kind of agent is this, what is controlling it, and is it actually hostile?"**

**Mechanically:** a sensor result is an **evidence item with a confidence value**, not a
verdict, and it is always falsifiable by one of the categories above. The GM should be able
to name *at least one* alternative explanation for any positive reading, and should name it.

---

## 5. The Voight-Kampff-style protocol

A formal NoöPunk investigative procedure for cognition assessment.

**Naming.** The issue offers four candidates: *Nonhuman Cognition Assessment Protocol*,
*Ontological Interview*, *Sentience Differential Test*, *Anomalous Cognition Examination*.
**Recommendation: `Nonhuman Cognition Assessment Protocol (NCAP)` as the formal name**, with
**`Ontological Interview`** as the field term for the interview format. Characters may
still colloquially call it a **Voight-Kampff**; the setting would plausibly use the
nickname, and using it in dialogue is fine, but it is **not the canonical name** and the
proprietary term should not be the rulebook's own vocabulary.

**Channels it combines** (no single channel is definitive):

- psychophysiological responses;
- language and semantic anomalies;
- microexpressions (`Kinesics`);
- memory consistency;
- cybernetic telemetry;
- psychic resonance (`ESP`);
- empathic reactions;
- symbolic and archetypal stimuli;
- contradictory-information tests;
- AI-assisted behavioural analysis.

**The investigative sequence:**

> **Detection → suspicion → examination → classification → authorisation**

**Mechanically:** the protocol is a **structured skill challenge**, not a single roll.
Each channel is one line of evidence; the classification step is where the investigator
weighs them, and `Investigation` + `Intelligence Analysis` + `Kinesics` are the natural
pairs. **The `authorisation` step is a human legal decision, never a test result** — it is
where §6 applies.

**The machine gives a probability, not metaphysical certainty about what counts as
"human".** False positives and contested legal status are **desirable**, and the protocol
must be able to be *wrong*.

---

## 6. Lethal force and ethics

> **NHI status alone is not grounds for lethal force.**

This is the setting's most important normative rule, and it is what prevents NoöPunk from
collapsing into extermination fiction.

**Possible entities include:** benign NHI; neutral NHI; Earth-born nonhuman minds;
artificial persons; hybrids; awakened humans; entities with incomprehensible motives;
hostile NHI.

**The relevant police and intelligence question is:**

> **Is this entity committing or imminently threatening serious harm?**

**Not:** "Is this entity human?"

**For irreversible decisions, NoöPunk requires triangulation of reality.** The operational
doctrine:

> **Never authorise lethal force solely from augmented perception.**

### 6.1 Triangulate reality before acting (see §7)

Independent confirmation from **two or more channels** where feasible:

- physical evidence;
- partner observation;
- cyber evidence;
- psychic evidence;
- controller intelligence;
- formal cognition testing (the NCAP, §5).

**This doctrine is consistent with the Law-of-One-inspired setting.** `RULEBOOK.md` §9.3
already tracks **Polarization** on a service-to-self / service-to-others continuum and
states that it changes through *sustained meaningful action* rather than chosen alignment.
A field doctrine that refuses to convert "non-human" into "shootable" is exactly the kind
of sustained institutional choice that produces an StO-polarized organization — and a
compromised or Orion-influenced officer who shortcuts it is where StS polarization begins.

**This is also a mechanical hook, not only theme:** the Triangulate-Reality rule is the
reason the partner/controller/AI architecture is *functionally necessary* rather than
decorative (§3), and it is the reason a lone investigator is in genuine danger.

---

## 7. Psychic and psychotronic attacks on the player

**The player is a target.** Not occasionally — structurally, because a post-Singularity
investigator is the most instrumented mind in the room, and instrumented minds can be
attacked through their instruments.

Attack forms: psychic attack; psychotronic attack; hallucination; memory manipulation;
emotional manipulation; sensor spoofing; false AR overlays; implanted thoughts; dream
intrusion; altered perception; communications spoofing.

**This is what makes the cell architecture mechanically useful rather than decorative.**
When the player's own feed is compromised, the partner's independent eyes and the
controller's separate channel are the only remaining ground truth.

**Representative HUD warning** (the issue's own example, adopted as the canonical form):

> PSI INTRUSION DETECTED
> Source: UNKNOWN
> Visual-feed integrity: 81%
> Memory continuity anomaly detected
> Recommendation: avoid irreversible decisions

### 7.1 The key theme

> **Advanced technology does not remove uncertainty. It creates more dimensions in which
> uncertainty can attack you.**

**Mechanically:** an intrusion is a **contested check** — the attacker's relevant PSY skill
(§4: hostile PSI uses `Telepathy` or `Psychokinesis`) against the defender's **`Psychic
Defence`**. This is why `Psychic Defence` is the academy's Core baseline
(`docs/design/UNSA_ACADEMY.md` §3.6): every graduate can resist; only a specialist can
retaliate.

**Design rule:** a compromised feed **degrades information quality**, it does not simply
subtract a number. The GM should describe *what is now untrustworthy*, so the player
triangulates rather than arithmetic-ing their way out.

---

## 8. Men in Black and the Orion Group

> **Do not make the player organization simply "the Men in Black."**

In the Law-of-One-inspired setting, **the Men in Black are associated with the Orion
Group** and work better as **recurring antagonists**.

They can function as: hostile intelligence operatives; psychic enforcers; disinformation
agents; infiltrators; evidence suppressors; fake officials; handlers of compromised humans;
agents who arrive **after or before** the investigators.

**Capabilities** (and the paranoia they create): extremely convincing credentials; memory
interference; psychic pressure; sensor spoofing; command-channel manipulation; fabrication
of evidence; **attempts to provoke humans into attacking peaceful NHI**.

> **This creates the campaign's strongest recurring paranoia: even valid-looking
> institutional orders may be compromised.**

**This is why §3.3's controller is a *possible* source of false confirmation, and why the
Triangulate-Reality doctrine cannot be satisfied by any single institutional channel.**

**Canon note — and a naming caution.** `RULEBOOK.md` §38 records that UNSA personnel are
nicknamed "Men in Black" in popular usage, and that **"MJ-12" is not an acceptable
nickname** because UNSA doctrine remembers MJ-12 as a legacy network of traitors. The
Orion-associated Men in Black of this section are a **different in-world thing** from the
UNSA nickname: the nickname is what the public *calls* UNSA; the antagonists are what
UNSA *hunts*. A scenario that conflates the two has misunderstood the setting, and this
distinction is worth stating explicitly in play.

---

## 9. Europe-focused default campaign

**Do not overbuild the world.** For the initial campaign, ignore the detailed political
future outside Europe unless a case requires it.

The institution may be Europol, a future evolved Europol, or a fictional successor
European security/police agency. **The exact name is less important than the structure.**

The default chain:

> **European-level agency → Helsinki field office → anomalous-threat / Ö-Mappi-style unit
> → PC + partner + controller + embedded forensic AI**

**This is already canon.** `RULEBOOK.md` §38 gives the Helsinki operational chain as
*Finnish authorities / Suojelupoliisi → Europol / EU federal security structures → UNSA*,
and `FACTIONS.md` §"Default Helsinki / UNSA affiliation" names UNSA plus Suojelupoliisi and
Europol as the institutional spine. This document adds the cell composition on top; it does
not change the chain.

**The rest of the world stays deliberately blurry** and enters only through intelligence
reports, refugees, corporations, NHI incidents, black-market technologies, foreign
operations and occasional missions.

---

## 10. The design principle to preserve

> **The player should have access to extremely powerful information technology, cybernetics
> and psychotronics, but these should deepen investigation rather than trivialise it.**

The recurring gameplay question:

> **Which version of reality is actually true?**

The recurring procedure:

> **Triangulate reality before acting.**

**These two sentences are the acceptance test for every future subsystem.** Any mechanic
that makes either question disappear — a sensor that identifies the answer, an AI that
solves the case, a power that removes the need for a second witness — is out of spec, no
matter how well it fits its own domain.

---

## 11. What this document does and does not settle

**Settles (as the default campaign template):**

- the four-layer crime scene and its skill mapping;
- the four-role cell: field investigator, partner, controller, embedded limited AI;
- NHI detection as anomaly, never verdict;
- the NCAP / Ontological Interview procedure and its sequence;
- the lethal-force doctrine and the Triangulate-Reality requirement;
- the Orion-associated Men in Black as recurring antagonists, and the UNSA-nickname
  distinction;
- the Europe/Helsinki default chain, on top of existing §38 canon.

**Does not settle:**

- the exact mechanical formulation of the NCAP (which skills, what DVs, how many channels
  constitute confirmation) — that is a rules pass;
- whether the controller is a single named NPC or a rotating role — a campaign decision;
- the partner's and controller's own stat blocks — character generation;
- **the Cortical Stack question**, which `docs/design/UNSA_ACADEMY.md` §10 records as
  deliberately open because it changes the stakes of death that this document's lethal-force
  doctrine depends on. If agents can be restored cheaply, §6's ethics change meaning.
  **The two documents are coupled, and both escalate that decision to the author.**

**This document promotes nothing here to hard setting canon by itself.** It is the default
campaign *template*; the author promotes any element of it deliberately.
