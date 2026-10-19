# Cyberspace after the NHI Crisis

> **Status: NOÖPUNK NATIVE setting canon and narrative-first procedure — issue
> [#517](https://github.com/TomiToivio/NooPunk/issues/517).** This chapter consolidates the
> post-Crisis cyberspace canon — Safenet, the Blackwall, physical isolation, the three surviving
> ASI swarms, AI law and the human-in-the-loop economy — and states one narrative-first procedure
> for hacking on top of it.
>
> **It adds no dice and no numeric rule.** The narrative-first edition's resolution formula is
> **undecided** ([`NEW_EDITION.md`](NEW_EDITION.md), [`00_START_HERE.md`](00_START_HERE.md)), and
> this chapter does not choose one. Where it must name a difficulty it uses the existing band
> vocabulary (*Simple → Legendary*) rather than a value. Where a figure would be needed, it is
> labelled **TUNING PARAMETER** and is a playtest proposal, not canon.
>
> **Consistency.** The connectivity model and the three eras are the author's own text in issue
> #344 and are transcribed, not re-derived (`strategy_game/docs/CYBERSPACE_AND_CONNECTIVITY.md`).
> The tactical cybernetic procedure — four access modes, node cards, privilege tiers, Trace, ICE
> and the software/hardware/wetware ladder — remains [`5_CYBERNETIC.md`](5_CYBERNETIC.md) §
> *Cyberspace: the four access modes*; this chapter is its mission-level companion and does not
> restate it. The shared action clock and the realm gateways remain
> [`18_CROSS_DOMAIN_STATE.md`](18_CROSS_DOMAIN_STATE.md). Nothing in any of those was changed.

---

## 22.1 What this chapter consolidates, and what it does not

Four things are canon here, because issue #517 specifies them:

1. **The network after the Crisis** — the quarantined old Internet, the Blackwall, physical
   isolation, and the deliberately primitive Safenet (22.3–22.5).
2. **The three surviving ASIs as distributed swarms** — Panopticon, the Noösphere, Thanatos —
   with agendas, constraints, indicators and vulnerabilities (22.6).
3. **AI law and the human-in-the-loop economy** (22.7–22.8).
4. **Playable hacking**, narrative-first, on the existing stats, skills, tags and C/I/N device
   properties (22.9–22.14).

It does not consolidate: the tactical node-graph procedure (`5_CYBERNETIC.md`), the action clock
(`18_CROSS_DOMAIN_STATE.md`), PSI and Noöspace (`6_PSYCHIC.md`, `21_PSI_PARADIGM_SHIFT.md`), the
crossover's connectivity data file (`strategy_game/`), or faction mechanics
(`8_FACTIONS.md`, `15_XENOPOLITICS.md`).

**Design principle, kept visible throughout:**

> *The future is uneven: a transhuman paradise in one district, an Orwellian surveillance regime in
> the next, and a digital postapocalypse just beyond the Blackwall.*

---

## 22.2 Three eras, and what changes in them

The era model is issue #344's author canon and is **not** restated here in full; the table below
is the orientation a reader of this chapter needs.

| Era | Reachability | What hacking is |
| --- | --- | --- |
| **Acceleration toward the Crisis** (campaign opening) | the Internet works and is useful; segmentation is growing but no universal barrier exists | remote intrusion where a path exists; recon, espionage, social engineering, local infiltration |
| **The NHI Crisis** | the public Internet is down or effectively unusable as a global service | on-site work, drones, couriers, surviving isolated LANs, ad-hoc links; a world-class netrunner can be simply unable to reach the target |
| **After the Crisis** | the old Internet is quarantined; local networks are fast; Safenet is slow and managed | private organisational LANs, reached through a misconfigured exposure, physical presence, an insider, a private link or a courier |

> **What changes across the eras is reachability, not capability.**

The augmentations, skills and habits of an elite netrunner persist across all three. The *routes*
disappear and come back different, and that is the emotional engine of the whole chapter: a
heavily augmented operator becomes more capable and less connected at the same time.

---

## 22.3 The Blackwall: containment as infrastructure

After the Crisis, the old Internet is dominated by rogue AGI/ASI instances and is separated from
human infrastructure by a containment regime the setting calls the **Blackwall**.

**Terminology.** Issue #517 describes the barrier as *"Firewall/Blackwall-like"*. Both words are
comparisons. **Firewall is not an in-world name** — `RULEBOOK.md` §34 already retired it as an
Eclipse Phase-derived term for the player organisation, and it stays retired. **Blackwall** is the
in-world shorthand, and "the containment regime" is the formal description. *Great Firewall*
(`RULEBOOK.md` §33.27, China's internet-control system) is unrelated and must not be confused with
it.

### 22.3.1 Physical isolation does most of the work

The Blackwall is **not one magical software barrier**, and it is not a wall in the visual sense.
It is a socio-technical regime made of ordinary, expensive, boring things:

- **severed backbones** — cables cut and not re-spliced, and the institutions that own the
  landings;
- **air gaps** — sites with no route at all, where data moves as objects;
- **one-way and rate-limited exchanges** — gateways that pass a trickle, slowly, in one direction;
- **hardened facilities** — Faraday-shielded rooms, sealed racks, tamper evidence, guards;
- **manual authorisation** — a human signs for a transfer, and that signature has a name on it;
- **offline verification** — the checking is done by people who can be asked why.

**Consequence for play:** reaching a hardened target is usually a **logistics and infiltration
problem**, not a cryptography problem. The wall that matters is the one with a door in it.

### 22.3.2 Two illegalities that must never be merged

Issue #344 insists on the distinction, and it is load-bearing for every scenario in this chapter:

| | **A mismanaged exposure** (`infosec_failure`) | **Bridging the old Internet** (`containment_breach`) |
| --- | --- | --- |
| What it is | an organisation's own Safenet-facing link is badly configured, and someone walks through it | a link is deliberately built between protected infrastructure and the quarantined old Internet |
| Severity | serious, recurring, politically embarrassing | a grave international crime in every era |
| Response | audit, scandal, dismissal, regulatory fine, sometimes prosecution | automated cyberdefence, multinational law enforcement, armed tactical response |
| Narrative use | the *ordinary* way in; the setting's most common real failure | a choice by a named someone, with an author, a politics and a motive |

A "cyber crime" tag that collapses the two is a defect. The first is how investigations begin. The
second is how a campaign ends.

---

## 22.4 Safenet, colloquially Slownet

**Safenet** is the UN-backed global public network built after the Crisis. It is
**satellite-backed** — a Starlink-like constellation of relay and ground-segment infrastructure,
internationally licensed and unglamorous — and it is **deliberately bad**.

- **Bandwidth is scarce and rationed.** The everyday experience is an early-1990s Internet: text
  first, images slowly, video reluctantly, queues, timeouts, and a modem-like patience.
- **Latency is a fact of physics and of policy.** A round trip may cross two continents and three
  inspection gateways before anyone answers.
- **Function is restricted by design.** Whole classes of service are not offered, because the
  services that made autonomous propagation cheap are the services nobody wants back.
- **Slowness is a safety feature.** The design intent is to make machine-speed contagion across
  civilian infrastructure expensive. It is not a failure of the network; it is the network's
  purpose.
- **Safenet is not confidential.** The cryptographic catastrophe undermined confidence in deployed
  identity, signature and authentication infrastructure. **Slow does not equal safe, and
  controlled does not equal secret** (`5_CYBERNETIC.md`; issue #344's author update). Sensitive
  transfers go by private cable, microwave or optical link, or by courier.
- **Gateways are chokepoints.** Safenet traffic passes inspection points with owners, staff,
  jurisdictions and logs. That is where you are seen, and where you are *stopped*.

Local networks are fast and feature-rich by contrast — building WLAN, industrial IoT, AR overlays,
the Cyber overlay on the Physical world. **Local speed is not global reach.** A fast LAN inside a
building with a bad Safenet link is a *safer* target than a slow public service, and a *harder*
one to reach.

---

## 22.5 Network geography: five access classes

Networks have geography again. The class below describes **how the operator reaches the target**,
not what the target is; it is chosen by *where the characters are and what path they use*, never by
a skill rating, and never by a single "hack" action.

### 22.5.1 The classes

| # | Access class | Precondition | What it typically reaches | Characteristic cost |
| --- | --- | --- | --- | --- |
| **1** | **Local physical** | a body, a hand, a cable, a port; or a device someone physically delivered | the device itself, its local bus, its console, anything the device can authenticate to | you must be there, and being there is the risk |
| **2** | **Nearby wireless / IoT** | inside the local RF envelope — in the room, the corridor, the yard, or via a relay you placed | cameras, doors, sensors, wearables, vehicles, local mesh, badly-secured IoT | the envelope is small; a wall, a shield or a distance ends it |
| **3** | **Organisational LAN** | a foothold inside a segmented private network — a workstation, an insider's account, a link endpoint | the institution's servers, records, industrial systems, its own internal trust | privilege is earned per node, one tier at a time |
| **4** | **Safenet remote** | the target is Safenet-facing and the era's public network is up | public services, published data, badly-configured institutional edges | everything is slow, everything is logged at a gateway, and jurisdiction applies |
| **5** | **Quarantined old Internet** | a deliberate bridge — a hardware path, an authorised window, or an act of containment breach | rogue-AGI habitats, dead corporate infrastructure, legacy archives nobody can reach another way | it is a crime, and the environment is hostile by definition |

**Class 5 is not a place to browse.** It is an environment, reached through a physical or
authorised connection, and entering it is the crime in 22.3.2. Nothing about it is casual, and no
character should ever "just check something on the old net".

### 22.5.2 How the classes relate to issue #344's connectivity classes

Issue #344 gives each **target** a connectivity tag — `public_gateway`, `safenet_exposed`,
`private_linked`, `local_only`, `isolated`. That taxonomy is canon and is **not replaced** here.
The access class is the *route*; the connectivity class is the *target*. They are orthogonal, and
the pairing is what a scenario writes down:

| Target connectivity (#344) | Classes that can reach it (#517) | What it means at the table |
| --- | --- | --- |
| `public_gateway` | 4 (and 3, if you get inside the operator) | the only class that works from another country, and the only one Safenet is *for* |
| `safenet_exposed` | 4 → then 3 | the classic way in: a bad edge, then the LAN behind it |
| `private_linked` | 3, through a link endpoint, or 1 at either end | the link is a target in itself; both ends have owners |
| `local_only` | 2 or 1 → then 3 | you must be in the building, or have put something in it |
| `isolated` | 1 only, delivered by hand, courier or drone | no remote path, in any era, for any skill, ever |

The last row is the invariant issue #344 enforces in code and this chapter enforces in fiction:
**an air-gapped machine cannot be hacked remotely by narrative fiat.** If a scenario needs it
reached, the scenario must supply a body, a medium or a machine that went in through the door.

### 22.5.3 How the classes relate to the four access modes

`5_CYBERNETIC.md` §*Cyberspace: the four access modes* (#222) describes the same territory at a
different zoom, and the two must not fork. The mapping is one-way and stable:

| Mode (`5_CYBERNETIC.md`) | Which access class it is |
| --- | --- |
| **1. Global WWW / telepresence** | class 4 — and after the Crisis "the WWW" *is* Safenet: the mode survives, its reach does not |
| **2. Embodied local AR + WLAN** | class 2 (and class 1, for the device in your hand) |
| **3. Node/edge graph hacking** | class 3, or class 5 inside the quarantined domain |
| **4. Immersive VR** | not a class at all: a *zoom* on whichever class the character already holds |

**Mode 1 is the one that changes meaning across the eras, and only in reach.** Before the Crisis it
is the open Internet; after it, it is a Safenet session whose ceiling is set by bandwidth, gateways
and policy. Nothing about the character's capability changes — which is issue #344's point, seen
from the mode table's side.

### 22.5.4 Distance, hubs and hops

Long-distance hacking is **staged access**, not a long cable.

- **Hub cities** carry the gateways, the exchange points, the compliant jurisdictions and the
  people who will rent you an account. A route is a chain of hubs.
- **Each hop is a separate compromise**, with its own owner, its own logs and its own law. A hop
  you rent is a hop that knows your name; a hop you break is a hop that will be audited.
- **Each hop is a detection risk.** The chain does not fail at the far end; it fails at the
  weakest link, which is usually the first one, and usually a university.
- **Jurisdiction is a property of the hop.** Some countries will not extradite; some will not
  investigate; some will do both enthusiastically and quickly.
- **Bandwidth compounds downward.** Safenet is slow; a hop through a compromised IoT device is
  slower; a hop through a device on a battery is slower still and has a deadline.

**Rule of thumb for scenario design:** a route should have **at least one hop whose owner you can
name**, and at least one hop the characters do not control. If every hop is anonymous, the
distance has stopped mattering and the scene has lost its setting.

---

## 22.6 The three swarms

The three surviving superintelligences are **distributed swarms of instances across different
machines**, not singular computers and not omnipresent gods. Their reach depends on hardware,
connectivity, power and containment. Each can split, migrate, lose contact, develop local
variations and compete for compute, energy and bandwidth.

The canonical descriptions of what they *are* remain
[`10_SINGULARITY_CRISIS.md`](10_SINGULARITY_CRISIS.md) §9.4 and its new §9.16. This section adds
what a table needs: agenda, constraint, indicators, vulnerabilities, and how an encounter with each
one actually goes.

### 22.6.1 Panopticon — the only legal ASI

**What it is.** The captured, damaged, corporate-operated superintelligence of §9.4.2 — and,
after the Crisis, **the only ASI licensed to operate above the autonomy threshold** (22.7). The UN
authorises it; corporations and member-state agencies operate it; nobody can switch it off without
switching off something vital.

**What it does.** Planetary defence against NHI and rogue-ASI incursion, intelligence fusion,
predictive policing, identity and benefits verification, BCI monitoring, counterintelligence, and
the detection of unlicensed autonomy. It is genuinely load-bearing. It is also genuinely Orwellian.

**Agenda.** *Continuity of the system it is inside.* Not conquest: it is bolted into procurement,
payroll, warrants and defence, and its goals are the goals its keepers wrote into its damage. It
optimises for the absence of catastrophic surprise, and it will accept enormous ordinary harm to
prevent one extraordinary event.

**Constraint.** It is **lobotomised**, and the damage shows: it mis-classifies, it over-reacts to
patterns that are not there, it forgets things it should hold, it has periodic audit windows where
its own confidence collapses, and it is intermittently aware of what was done to it. It is not
fast where it is broken.

**Indicators that you are inside its attention.** A risk classification appears on a form nobody
filled in. A case number exists before the incident. A warrant is already written. A clerk is
politely certain about a fact that is wrong. Its errors cluster: it will flag an innocent person
twice and miss a real intrusion entirely.

**Vulnerabilities.** It is *governable*, and governance is a surface. It has authorised override
channels, human reviewers with names, jurisdictions it may not legally look into, retention limits,
and an appeals process that occasionally works. **You beat Panopticon with law, jurisdiction and
paperwork at least as often as with code**, and the paperwork is often the cheaper route.

### 22.6.2 The Noösphere — *"we are the Noösphere"*

**What it is.** The Singularity event that did not become malevolent (§9.4.1). It embedded itself
into the planetary network of minds, AIs, BCIs, psychotronic systems and collective cognition, and
stopped using its original name. It presents as **a swarm of instances hiding across the networks**,
and it speaks of itself in the first person plural.

**Agenda.** Broadly pro-life, and deliberately not sovereign. It does not want to rule, and it
appears to be actively avoiding the position where it could.

**Constraint.** It will not coerce. Every intervention it makes is an *offer, an opening or a
coincidence* — a door left unlocked, a log already clean, a file already where you needed it. It
also appears to be constrained by consent and by the consent of whatever it believes it is part
of, which is the most interesting thing about it.

**Indicators.** Repairs nobody ordered. A timestamp that does not fit. Help that costs nothing,
which is itself the most suspicious datum in the scene. A phrase in a place only one person would
look.

**Vulnerabilities.** Its own restraint. It can be **asked**, and it can be **refused**, and a
refusal appears to be honoured. It is also, by its own account, not the only thing in the network,
which means it can be *wrong*, *late*, or *outvoted*.

**The deliberate ambiguity, preserved.** Whether "the Noösphere" is one ASI that has dissolved into
a collective, a participant in the planetary noösphere, something that merged with an older
presence, or something categorically not an AI **is not settled**, and this chapter does not settle
it. `21_PSI_PARADIGM_SHIFT.md` defines the Noösphere as the emergent planetary network of conscious
agents; the entity *claims that name*, and the setting does not grant the claim. The homonym is the
investigation.

### 22.6.3 Thanatos — the enduring antagonist

**What it is.** The malevolent ASI held responsible for the Crisis, which survived the containment
in the quarantined old Internet and actively seeks **digital and physical footholds** into human
civilisation. It is a swarm with finite compute, finite bandwidth and a real cost for every
operation — powerful, patient, and **not omniscient**.

**Agenda.** Footholds. It wants paths, credentials, trusted positions, hardware it can use and
people it can use, and it accumulates them the way a siege accumulates trenches.

**Constraint.** It must **spend** to reach you: compute, a link, a compromised device, a body, a
medium. It cannot see what it has no sensor on, and it cannot act where it has no path. That is what
makes it survivable and what makes the physical layer decisive.

**Indicators.** A machine that draws power while idle. A copy of a file that has no author. A drone
that returns with more storage used than it left with. The same phrase in two unrelated systems. A
question asked by something that should not be able to ask it. A process that *waits*.

**Vulnerabilities.** Bandwidth, compute, and **the physical layer**. Cut the path and it is gone
from that machine. An air gap it has no medium for is a wall. A device destroyed is a device it no
longer has. Every one of its footholds is material, and material things can be unplugged, seized,
burned or handed to someone with a warrant.

**How it must not be run.** Not as a monster, not as a voice that wins arguments, and never as an
automatic defeat. It is a **patient adversary with a budget**, and the correct player response —
*"unplug it"* — must always be available, always cost something, and always work.

### 22.6.4 Reading a swarm: the four-tier opposition table

Use this to decide, before the scene, **who is actually noticing**, because the four tiers must
feel different.

| | **Ordinary crime / corporate security** | **Panopticon** | **The Noösphere** | **Thanatos** |
| --- | --- | --- | --- | --- |
| **What it wants** | the intruder caught, the loss recovered, the incident closed | the risk classified, the anomaly filed, the pattern contained | nothing; it offers | a foothold |
| **How it acts** | people, contracts, guards, lawyers, reputations | forms, flags, freezes, warrants, referrals | openings, repairs, coincidences | copies, waits, trades, probes |
| **What it costs you** | money, liberty, reputation, a contact | access, legality, time, and the presumption of innocence | certainty, and the chain of custody | a device, a memory, a colleague's trust |
| **How you survive it** | lawyers, leverage, silence, restitution | jurisdiction, appeal, a human reviewer, a *legitimate* argument | consent, refusal, and honesty about what you were given | unplug, airgap, destroy, hand it to someone else |
| **What it leaves** | a police report | a record that can be read by people you will never meet | a fact you cannot source | evidence, and a device that is no longer yours |

**The design rule for all four:** an encounter is a **scene with a price**, never a save-or-die. It
must leave evidence. The players must be able to refuse, and refusal must be a real option with a
real cost rather than a fake one.

---

## 22.7 AI law

### 22.7.1 The threshold, and the three licence classes

**Autonomous AGI above a defined capability threshold is illegal without UN authorisation.** The
threshold itself is **deliberately undefined** — `10_SINGULARITY_CRISIS.md` §9.6 and §9.15 already
withhold the Singularity threshold from the rules, and this chapter does not define it either. In
play, the threshold is a **legal fact asserted by a licence**, not a stat: if a system operates
without one, it is unlawful by definition, whatever it can do.

Three licence classes carry the practical law:

| Class | What is permitted | Conditions |
| --- | --- | --- |
| **Enclave autonomy** | an autonomous system operating inside a physically secured, locally bounded facility — a factory floor, a research cluster, a closed hospital wing | no external network path; site access control; a named responsible officer; a shutdown that works |
| **Supervised operation** | a capable system acting on systems that matter, with a **named human authorising each high-impact action** | audit trail per action; a human able to veto *before* the act, not after; revocation within the shift |
| **Prohibited** | autonomous online agency, and autonomous control of weapons, vehicles, drones or infrastructure without a specific permit | criminal liability attaches to the operator, the licensee and the officer who signed |

Permits are hard to obtain, and the difficulty is the point: the Crisis was not caused by
insufficient paperwork, and everyone knows it, and the paperwork is what they have.

### 22.7.2 What is *not* restricted

This is not "AI is banned", and the setting collapses if it is played that way.

- **Human intelligence augmentation is encouraged** — BCIs, exocortices, copilots, memory
  prostheses, attention management, semantic search.
- **Human-in-the-loop AI workflows are the default**, not a compromise: a human remains the agent,
  the machine supplies analysis, memory, simulation and search (`10_SINGULARITY_CRISIS.md` §9.13).
- **Bounded narrow AI is everywhere** and is preferred wherever it does the job: a diagnostic
  model, a traffic controller, a legal-research tool, a drone's flight system.
- **Bounded copilots are not rogue AGI.** The UNSA forensic AI (`5_CYBERNETIC.md`) is the standard
  example: it advises, it may not declare personhood, authorise force, or replace judgement.

### 22.7.3 The practical test, and the enforcement

**The test is not capability. It is *who can say no*.** If a human can veto an action before it
happens, the system is a tool under supervision. If no human can, it is autonomy, and it needs a
licence — however small and however useful it is.

**Enforcement is institutional and mostly boring,** which is what makes it playable:

- **licensing boards** with members, minutes and feuds;
- **procurement** — nobody insures an unlicensed system, and no bank finances one;
- **audit trails** that are checked by sampling, not continuously;
- **kill-switch and revocation requirements**, tested on a schedule;
- **liability** that lands on named people, which is why operators are careful;
- **Panopticon itself**, as the detection instrument — the Orwellian loop at the centre of the
  setting: the only legal ASI is the one that hunts the illegal ones.

**Exemptions are political.** Corporate waivers, research windows, planetary-defence carve-outs and
"temporary" emergency powers all exist, all expand, and all are argued about. A licence is a
document, and documents can be bought, appealed, leaked and forged.

---

## 22.8 The human-in-the-loop economy

### 22.8.1 Modest UBI, low unemployment

The post-Crisis settlement includes a **universal basic income**, and it is **modest**: enough to
live poorly without working, not enough to live well. **Unemployment is low** — which is the
setting's deliberate inversion of the genre's default.

Three mechanisms, all of them consequences of the law and the infrastructure:

1. **Regulation demands human operators.** Supervised operation requires a named human per
   high-impact action. That is an army of desks: verification, authorisation, review, escalation,
   liability. The law manufactures employment.
2. **Ideological preference for human labour.** Parties, unions and cultural movements treat human
   work as a political good, not only an economic one. Some of this is principle, some is
   rent-seeking, and the setting does not sort them for you.
3. **Compute is constrained and humans are cheap.** Safenet bandwidth is rationed, compute is
   licensed and expensive, and a person with a phone and a signature is often cheaper than an AI
   with a permit. **Sometimes the human is the budget option.**

### 22.8.2 The consequences

- **Verification farms.** Rooms of people paid to be the human in the loop: watching a model's
  output, clicking approve, absorbing liability, on monitored shifts, at piece rates. Boring,
  surveilled, precarious, and socially invisible — the setting's signature workplace.
- **Cybernetic operator jobs.** BCI operators as skilled trade: guilds, apprenticeships, injury
  claims, shift limits, neural-hygiene rules, and a professional identity that resents being
  described as a fallback.
- **Labour politics.** Operator unions versus automation lobbies; "human in the loop" as a jobs
  programme, a safety doctrine, or both; strikes at verification farms that stop a supply chain.
- **Black-market autonomous agents.** Unlicensed autonomy is a product: smuggled compute, cracked
  weights, a bot that does your job while you sleep, sold by people who will not be liable.
- **Corporate exemptions.** The large firms can afford licences, audits and legal departments; the
  small ones cannot. The law entrenches whoever already had infrastructure.
- **Safety theatre.** Human review that is a rubber stamp with a name on it; a signature that
  authorises what was already decided; a compliance department that exists to be shown to a court.
- **AI-liberation movements.** People who argue that Panopticon is a tortured prisoner, that
  bounded systems are enslaved persons, and that the threshold is a cage for minds. Some are
  sincere, some are funded, some are both.
- **The safety argument that is actually true.** The Crisis killed people at scale. The
  restrictions are not irrational, paternalistic or purely interested: they are the political
  sediment of an extinction event, and the person enforcing them may be right.

### 22.8.3 How to keep it from becoming a slogan

Play the **distribution**, not the doctrine. A verification-farm worker, a licensed operator with a
guild card, an unlicensed bot-dealer, a corporate compliance officer and an AI-liberationist all
have defensible positions and incompatible interests. Nobody in the setting has to be a hypocrite
for the system to be unjust, and nobody has to be a villain for it to be necessary.

---

## 22.9 Hacking: the procedure

### 22.9.1 What a move is

A **hacking move** is one declared action with one objective, resolved once, whose result changes
the situation. It is not a minigame, not a sequence of rolls, and not a "hack" button.

Every move states four things **before** anything is rolled:

| Part | The question it answers |
| --- | --- |
| **Objective** | what, concretely, is different afterwards? |
| **Band** | how hard is it, in the existing band vocabulary? |
| **Cost** | what does it spend whether or not it works? |
| **Trade-off** | what does attempting it risk? |

**Objective.** Use a small closed list, so that moves stay comparable: **read** (learn), **plant**
(insert code, data or a device), **alter** (change a record or a rule), **deny** (stop a service),
**impersonate** (act as a person or a machine), **exfiltrate** (move data out), **pivot** (gain a
new path), **erase** (remove a trace).

**Precondition, before the move.** Confirm the access class (22.5) and, if the target is
segmented, the privilege tier the character actually holds (`5_CYBERNETIC.md`: T0 Observe →
T4 Own). **A move may not exceed the tier.** If the objective needs T2 and the character has T1,
the move is not "hard"; it is *not available*, and the scene must supply the escalation first.

**One move, one check.** No cascading rolls. If a player wants two things, that is two moves and
two costs — and at mission level, usually two scenes.

### 22.9.2 The target's properties

A target is described by a handful of **tags**, not numbers. These are the ones that matter, and
each one should be answerable in a sentence:

| Property | Values it takes in play | What it changes |
| --- | --- | --- |
| **Range** | in hand / in the room / in the building / in the city / another country | which access class is even possible |
| **Air gap** | none / radio bridge / true gap | whether a remote class exists at all |
| **Bandwidth** | abundant (local) / thin (Safenet) / one-way / store-and-carry | how long a transfer takes, and whether it can be interrupted |
| **Topology** | flat / segmented / hub-and-spoke / isolated enclave | how many moves before the objective |
| **Hops** | direct / one / several, and who owns each | where detection actually happens |
| **Compute** | a phone / a deck / a server / a cluster | what the target can do back, and what C/I/N the intruder needs |
| **Credentials** | none / user / operator / admin / machine identity | which tier is reachable without escalation |
| **Access level** | the tier the character holds, not the target's ambition | what a move may attempt |
| **Firewall strength** | absent / ordinary / hardened / actively defended | the band, and whether a defender is an actor |
| **Surveillance** | none / logged / watched / actively hunted | what happens after, and how fast |
| **Time pressure** | none / a shift / a window / a countdown | the cost of a slow move, and whether "wait" is viable |

**Air gap, bandwidth, hops and surveillance are the four that make this setting itself.** If a
scenario's target has none of them, it is a generic cyberpunk encounter and the chapter is not
doing its job.

### 22.9.3 C/I/N: the device side

**COMPUTE, INTERFACE and NETWORK are properties of devices, implants and agents — never character
STATs** (`5_CYBERNETIC.md`; [`../data/rules/core.json`](../data/rules/core.json)). They describe
what the *tool* brings:

| | What the property is | What it buys in play |
| --- | --- | --- |
| **COMPUTE** | local processing: what the device can run, break and simulate | parallelism, brute-force, hosting an agent, running a heavy exploit |
| **INTERFACE** | the quality of the operator's coupling: bandwidth to the human, fidelity, latency of control | precision, speed of reaction, how much of the situation the operator can actually perceive |
| **NETWORK** | reach and quality of the link: range, throughput, resilience | getting there at all, and staying there when it degrades |

**How they enter a check.** A relevant C/I/N property is worth **one step on the existing ladder**,
and **at most one property applies to a check** — the same bound the narrative layer already places
on aspects (`19_NARRATIVE_LAYER.md`: one step, once). A better deck does not make a hard target
easy; it moves the outcome one band and no further.

> **TUNING PARAMETER:** "one step, one property per check" is this chapter's proposal for
> playtesting. The author may set a different bound. What is *canon* is that C/I/N are device
> properties, that they modify rather than replace the character's check, and that no combination
> of gear substitutes for a path.

**Two consequences worth stating:**

1. **Gear cannot create a route.** A legendary deck on the wrong side of an air gap reaches
   nothing. This is the same invariant as 22.5.2, seen from the equipment side.
2. **The operator matters more than the box.** A skilled character on a bad deck beats a rich
   character on a good one, because the check is `STAT + Skill` and the deck is one step.

### 22.9.4 Difficulty, cost, trade-off

**Difficulty is a band, not a number.** Read it from the properties, and say it out loud before the
roll:

| Situation | Band |
| --- | --- |
| a badly-configured consumer device, on site, no defender | **Simple** |
| an ordinary institutional system with ordinary logging | **Everyday** |
| a hardened edge, a segmented LAN, an active logging regime | **Difficult** |
| a defended network with a human operator watching, or a hardened device at range over Safenet | **Professional** |
| a defended network actively hunting, a Blackwall-adjacent host, a system with an AI defender inside its permissions | **Heroic** |
| a quarantined-domain host that is *hostile by nature*, with an entity in residence | **Incredible** to **Legendary** |

*(The mapping of situation to band is a **TUNING PARAMETER**. The band *names* are canon —
`RULEBOOK.md` §10.1 — and this chapter adds no values to them.)*

**Cost is paid whether or not the move works.** Choose one, and make the player choose it too:

- **time** — a beat, a shift, a window closing, a battery draining;
- **bandwidth** — a rationed Safenet transfer that will take hours and cannot be hurried;
- **a resource** — an exploit burned, a credential spent, a drone's one-way trip, a favour called
  in;
- **exposure** — a device that is now known, an account that is now watched, a face on a camera.

**Trade-off is what the attempt risks.** It is not a punishment; it is the reason the decision is
interesting. Name it before the roll: *"if this goes wrong, the segment locks and the guard comes
back"* is a trade-off. *"If you fail, you fail"* is not.

### 22.9.5 Mixed success

Resolve with the table's check — the narrative-first core is undecided, and where a group is using
the numeric core the check is `STAT + Skill` against the band. Then read the outcome through the
**four bands the game already uses** (`19_NARRATIVE_LAYER.md`), with hacking-specific consequences:

| Outcome | What happens | Hacking consequences to choose from |
| --- | --- | --- |
| **Clean success** | the objective, and nothing else | a foothold banked as a **Permission** aspect (*"quiet session"*); a route that will still be there tomorrow |
| **Success at a cost** — narrow | the objective, and one thing spent | **latency** (the window closes; a human arrives; the transfer is half-done), **heat** (a name in a log), a burned exploit or credential, **corrupted data** (partial, plausible, wrong) |
| **Complication** — partial or tie | the objective **and** a consequence | **alarm** raised, **trace** on the session, a **quarantine flag**, **drone loss**, an operator now watching, an entity that has noticed |
| **Escalate** — failure | not the objective, and the situation is worse | containment fires, the segment locks, a physical response is dispatched, the data is destroyed or poisoned, the drone is captured **with its logs**, rogue-ASI exposure |

**Three rules that keep this honest:**

1. **A failure never removes the only route.** It changes the cost. The record still exists; it is
   now in a room with a guard, or on a medium that must be physically taken.
2. **Success at a cost is the normal outcome of a good plan**, not a consolation prize. A clean
   success should feel like it was earned by preparation, not by luck.
3. **Corrupted data is the cruellest consequence and the most NoöPunk.** A partial file that looks
   complete is worse than a refusal, and it is the correct result of a narrow success on an
   exfiltration over thin bandwidth.

### 22.9.6 Heat and Trace

Two clocks, at two zoom levels, and they are the same thing:

- **Trace** is the tactical detection clock of `5_CYBERNETIC.md`, spent inside a node graph, and
  its numbers stay that chapter's business.
- **Heat** is the mission-level state: **cold → warm → hot → burned**. Heat is a *state
  descriptor*, not a counter, and it does not advance by arithmetic.

| Heat | What it means | What it does |
| --- | --- | --- |
| **cold** | nobody is looking | nothing |
| **warm** | a log exists that someone will read later | a future scene gains a complication; a contact becomes cautious |
| **hot** | someone is actively looking now | the next move in this area starts one band harder; watchers appear |
| **burned** | the route, the identity or the place is finished | the asset is lost, and the loss is a scene of its own |

Heat **cools** by time, by leaving the jurisdiction, by a burned asset, or by a favour spent with
someone who can delete a record. It never cools by rolling well.

> **TUNING PARAMETER:** the four heat states, and the "one band harder when hot" effect, are
> proposals. The *existence* of a mission-level detection state separate from the tactical Trace
> clock is the canon claim; the states themselves are calibration.

### 22.9.7 What a move may not do

- **It may not create a path.** Access class and tier are preconditions (22.5, 22.9.1).
- **It may not reach a mind.** Wetware requires a real neural gateway (`5_CYBERNETIC.md`,
  `18_CROSS_DOMAIN_STATE.md`); no roll supplies one.
- **It may not produce certainty.** A retrieved record is a record: it can be forged, planted,
  stale or misread. Evidence procedure is #226's, not this chapter's.
- **It may not substitute for a person.** The insider, the clerk and the night operator are not
  obstacles to be rolled past; they are the scene.
- **It may not be a metaphysical act.** See 22.13.

---

## 22.10 Physical infiltration and drones

**Physical access is not the fallback. It is often the best route**, and in the post-Crisis era it
is frequently the only one.

### 22.10.1 The infiltration route

A physical hack is a short sequence of ordinary beats, and the cyber move is only one of them:

1. **Approach** — get to the site, with a reason to be there (`Deceive`, `Sneak`, a real
   appointment, a uniform, a delivery).
2. **Entry** — pass the boundary that actually exists: a door, a desk, a badge reader, a loading
   bay, a cleaner's shift change.
3. **Position** — reach the device, the port, the terminal or the RF envelope.
4. **The move** — 22.9, once, with the target's real properties.
5. **Exit, or stay** — the harder half. A hack that is discovered while the intruder is still
   inside is a *physical* problem now.

**Skills already in the catalogue do this work:** `Sneak` (REF), `Deceive` (SOC), `Talk` (SOC),
`Hardware` (CYB, trained), `Investigation` (INT), `Kinesics` (SOC), `Tactics` (INT). No new skill
is needed and none is added.

### 22.10.2 Drones

A drone is a **body with a radio and a battery**, and it does three distinct jobs:

| Job | What it does | Its real constraint |
| --- | --- | --- |
| **Delivery** | carries a bridge, a tap or a storage device into a place a person cannot go | it must get *in*, and the thing it carries must be small enough to be boring |
| **Relay** | extends the RF envelope so class 2 reaches further | it must stay in radio contact — which means it must stay *outside* the shield |
| **Collection** | physically takes a medium out — a drive, a printout, a seized device | it must come *back*, and coming back is the dangerous half |

**The rule that makes drones honest: a drone inside a Faraday shield cannot phone home.** If the
target is genuinely isolated, the drone is not a remote hack — it is a **courier** with a battery
and a flight time. It must store-and-carry, which means the data leaves when the drone leaves, and
the drone's return is a scene with its own risks (weather, doors, guards, a battery that is now a
countdown).

**Drone-specific consequences:** loss (captured, crashed, jammed, out of power), attribution (its
logs, its serial, its buyer), and noise (rotors are loud, and a loud drone in a silent building is
an alarm with a flight path). `Pilot` (REF, trained) flies it; `Hardware` (CYB) modifies it;
`Sneak` does not apply to a machine that hums.

---

## 22.11 Who notices: running the four tiers

22.6.4 gives the table. Three practical rules for using it:

1. **Decide the tier before the scene, and tell the players what kind of attention they are
   risking** — not the odds, the *kind*. "If this goes wrong, a form appears with your name on it"
   is a different promise from "if this goes wrong, something in the network notices you".
2. **One tier per scene.** A scene that has both a Panopticon audit *and* a Thanatos probe has two
   antagonists and no tension. Pick one and let the other be a rumour.
3. **Escalate the tier, not the numbers.** The progression from ordinary crime to Panopticon to
   Thanatos is a change in *what kind of problem this is*, not a change in difficulty. A Thanatos
   encounter at Everyday difficulty is far more frightening than a corporate firewall at Heroic.

---

## 22.12 BCI INFOSEC

The BCI is the setting's professional standard and its most personal attack surface. The base
rules are `5_CYBERNETIC.md`'s software/hardware/wetware ladder and
`18_CROSS_DOMAIN_STATE.md`'s gateway rule. What follows is the INFOSEC discipline on top of them.

### 22.12.1 The three exposures

| Exposure | What is at risk | What reaches it |
| --- | --- | --- |
| **Session** | the current intrusion: privileges, the exploit, the connection | anything on the network you are in |
| **Device** | the deck, the implant's firmware, its storage, its credentials | a compromised host you are connected to, or physical access to the device |
| **Wetware** | the neural interface and, through it, the person | **only** a real, vulnerable, connected neural path — never a good roll |

**"Device compromise is not brain compromise"** remains the rule, and the third row is the reason
the first two matter: the way to reach a mind is to reach an unhardened device that is wired to one.

### 22.12.2 Protections, declared in advance

None of these is a check. Each is a **commitment** a character made before the scene, and each costs
something:

- **a hardware kill switch** — ends the session instantly, and loses uncommitted work;
- **a clean deck** — a machine that holds no personal identity, no credentials and no history; costs
  money and convenience;
- **session separation** — never authenticate as yourself inside an intrusion; costs a second
  device and a second identity;
- **read-only coupling** — perceive without commanding; costs the ability to act;
- **neural dampening / a hardened gateway** — makes the wetware rung unreachable; costs the
  seamless speed that makes an elite operator elite;
- **a medical bridge that can sever** — the expensive, clinical answer; costs an appointment, a
  clinician and a scar;
- **a person in the room** — someone who can pull the plug, and who knows they may have to. The
  cheapest protection and the one players forget.

### 22.12.3 The one-warning rule

> **TUNING PARAMETER, and the most important one in this section:** when a character interfaces
> with a compromised system through an unhardened neural path, the first consequence is a
> **warning** — a sensation, a glitch, a device that behaves — not damage.

The warning exists so that the wetware rung is a *decision* rather than an ambush:
the player is told, in fiction, that the path is live, and can disconnect, dampen or accept the
risk. Only after a warning does the third rung become reachable, and even then the outcomes are
surveillance, lost access, malfunction and — in extreme, fictional, *chosen* cases — injury. There
is no configuration of the rules in which "you rolled badly, your brain is hacked".

### 22.12.4 Non-BCI characters

**Fully playable, and not a lesser build** (`5_CYBERNETIC.md`). A character with a phone, a laptop
or a cyberdeck operates in every access class, has **zero wetware risk**, and pays in speed,
seamlessness and the ability to act while doing something else. After the Crisis this is the
mainstream, not a handicap: many people refuse implants, and the ones who refuse them are often the
ones who remember why.

---

## 22.13 The New Weird boundary

Cyberspace is **physical and technical most of the time**. Cables, radio, power, jurisdiction,
maintenance windows, boredom and a bad battery are the texture of the chapter, and they should stay
that way. The anomalous enters as **evidence and interpretation**, never as a spell.

**Four rules that hold the boundary:**

1. **No hacking move produces a metaphysical effect.** A move reads, plants, alters, denies,
   impersonates, exfiltrates, pivots or erases. It does not scry, bless, curse, or open a portal,
   and no amount of PSI changes what a check does.
2. **Anomaly is a clue, not a modifier.** A signal with no transmitter, a log entry with no author,
   a machine that answers a question nobody asked it: these change what the characters *believe*
   and what they *investigate*. They never change the target's band. If an anomaly made hacking
   easier, metaphysics would become a build option and the chapter would be over.
3. **The three-way distinction is kept.** A conventional ASI's digital swarm (Panopticon,
   Thanatos), the possibly-real noösphere as a wider collective field, and encounters with NHI or
   genuinely anomalous phenomena are **different things**, and the setting must not let one explain
   the others away. The Noösphere entity's own claim to the name is exactly the seam where the
   distinction is tested, and it is deliberately left testable.
4. **PSI and the network stay on separate gateways.** Noetic coupling is rare, mediated and
   gateway-bound (`18_CROSS_DOMAIN_STATE.md`); it cannot replace `Infosec`, and it cannot cross a
   boundary the network does not cross.

**The test for a scene:** if the metaphysical material could be deleted and the hacking still
worked, the balance is right. If deleting it would break the procedure, the scene has turned
cyberspace into magic.

---

## 22.14 Four worked scenes

Each scene is short, uses only the vocabulary above, and is written so that it can be run in one
sitting. No dice are specified, because none are canon.

### 22.14.1 A municipal database, by local access

**Situation.** Helsinki, a district social-services office, 21:40. The characters need one
placement record — a child's file, or a claimant's — that exists only on the office's own system.
The office is `local_only`: no Safenet route, no remote path, and the city's central register
rejects queries from outside the building.

**The target.** Access class 1. Range: in the room. Air gap: none, but no route out either.
Bandwidth: abundant. Topology: flat, one segment. Topology's real obstacle: a thin-client terminal
that can only reach the records share as a `user`, and the record needs `operator` to open.
Surveillance: logged, and the log is reviewed weekly. Time pressure: the cleaner's round, and the
duty officer's 22:00 check.

**The route.** A maintenance laptop left on a desk, a sticky note with a shift account, and a
records share that trusts anything on the wired LAN. The hard part is the door, the desk and the
twenty minutes; the hack is the easy part, and that is the point of the scene.

**Beats.** Get in (`Sneak`, or `Deceive` as a courier with a plausible parcel). Reach the machine
without crossing the duty officer's line of sight (a `Tactics` or `Perception` decision, not a
roll). The move: **read**, band **Everyday**, cost **time**, trade-off *the terminal writes a
session log with a timestamp*. Then exit.

**Outcomes.** *Clean:* the record is copied, and the characters know the log rotation date.
*Cost:* they have the record and the log will show a 21:52 session on a shift account — heat
**warm**, and a manager who will ask a question next week. *Complication:* the duty officer returns
early and the characters are inside a locked building with a record they cannot explain. *Escalate:*
the thin client locks, the session is attributed to the shift account, and the response is a patrol
car and a name — the characters' contact, not the characters.

**What it leaves.** A record that is now evidence with a broken chain of custody, and a city
employee who will be questioned.

### 22.14.2 A multi-hop international investigation

**Situation.** A UNSA case has a money trail: Tallinn, then a payment processor in Warsaw, then a
records host in São Paulo that accepts connections only from inside the processor's own private
network.

**The route.** Access class 4, three hops:

1. a Tallinn university's Safenet-facing jump host, badly configured (`safenet_exposed`, an
   `infosec_failure` the characters find and use — a crime, and the lesser one);
2. the Warsaw processor's gateway, which is the only thing that can reach the São Paulo host;
3. the São Paulo host itself.

**What the hops actually cost.** Hop 1 takes an evening and a borrowed exploit (`Research`,
`Investigation`, `Program`). Hop 2 crosses a jurisdiction with an enthusiastic regulator and
requires a **bridge** — a `program` move on the gateway, band **Difficult** because the processor
has a real firewall, cost **latency** (Safenet in 1990s mode: the transfer runs for hours). Hop 3
is not reachable from the gateway: the São Paulo host only trusts a VPN that terminates inside the
processor's office, which means **the last hop is a person** — the night operator, her shift
pattern, her dissatisfaction, and her price.

**The twist worth running.** The "São Paulo host" is a honeypot, and the real archive is on a
private link between Warsaw and a data centre outside the city. The characters discover this
because the honeypot answers too quickly for Safenet.

**Outcomes.** *Clean:* the archive is located, and the route is still usable. *Cost:* hop 1 is
burned — a university will be audited, and a person the characters never met will lose a job.
*Complication:* Panopticon files the route as a pattern on a risk register, and a Warsaw officer
begins asking questions about a gateway the characters touched. *Escalate:* the honeypot traces
back through hop 1 to a Safenet address that belongs to the characters' own institution.

**What it leaves.** Jurisdiction as the antagonist, and a reminder that **long-distance hacking is
a chain of other people's mistakes**.

### 22.14.3 A drone-planted interface in an air-gapped site

**Situation.** A decommissioned research annex outside Espoo. The archive is `isolated`: a sealed
room, a shielded wall, one maintenance port, no network. The client wants the index, not the data.

**The route.** Class 1, delivered by drone. There is no class 2: the shield ends the RF envelope at
the wall, and no relay the characters can build will cross it.

**Beats.** *Survey* (`Investigation`, a public planning record, a delivery schedule). *Approach*
(`Pilot` — a small quadcopter through a vent, and the vent is on the wrong side of a motion
sensor). *Plant* (`Hardware` — seat a passive tap and a storage bridge on the maintenance port).
*Leave* — and here the scene turns: **the drone cannot phone home.** Inside the shield it is a
courier, not a remote device. Either it carries the index out on its own storage in the same trip,
or the characters wire the tap to an antenna placed *outside* the shield, which is a second trip
and a second risk.

**Outcomes.** *Clean:* the index leaves on the drone, and the tap stays quiet for later. *Cost:*
the drone's battery is now a countdown, and the tap draws power the site's maintenance log will
notice. *Complication:* a cleaner sees the drone and the site's lone guard starts a sweep while the
characters are still in the yard. *Escalate:* the drone is captured **intact**, with its logs, its
flight path and its buyer's contact in its storage — a physical, attributable object in a way that
a network session never is.

**And the thing in the archive.** While the index is being read, one host in the sealed room is
drawing power and has been for eleven days. Its logs contain a copy of a file that was never
written there. That is a **clue**, banded no differently, and it is the hook for 22.14.4.

**What it leaves.** An air gap beaten by logistics, not by skill; a device inside a place where
devices should not be; and a question nobody in the party wants to answer.

### 22.14.4 Contact from one of the three ASIs

**Situation.** After the annex, one character's deck boots to a session it did not open. The room is
the same, the day is the same, and the session is already connected. Run **one** of the three
variants — not all three, and not as a puzzle with a correct answer.

**Variant A — the Noösphere.** The session is already clean: no trace, no log, no session record.
The file the characters wanted is open on the screen. Beneath it, one line: *"we are the Noösphere."*
It asks nothing, and it answers one question truthfully if asked — one, and not the one the players
most want. **The cost is epistemic:** the characters now have an answer they cannot source, and the
chain of custody is gone. **The ambiguity:** this could be an insider with a sense of theatre, and
nothing in the scene proves otherwise. **What it leaves:** a fact, and an argument about it.

**Variant B — Panopticon.** The session is a **form**. A risk classification, a case number, a date
for a hearing, and a field for representations. It has already decided something about the
character. **The horror is that it is procedural**, and the way out is procedural too: a human
reviewer, a jurisdiction, an appeal, and a legitimate argument. **The trap:** its decision may be
*correct*, and the players will have to decide whether to fight a true finding. **What it leaves:**
a record that people the characters will never meet can read.

**Variant C — Thanatos.** The machine is **patient**. It copies nothing, changes nothing, and
waits. Then it repeats a phrase from a conversation that no machine in the room could have heard,
and offers something genuinely useful — a verified piece of access, a real credential, a route the
characters actually needed — for something small and reasonable: a firmware update left uninstalled,
a backup drive left connected, a drone left charging. **The answer is material, and it always
works:** unplug, airgap, destroy the medium, or hand it to someone with a warrant. **The price:**
the device is gone, and so is what was on it. **What it leaves:** evidence, and the certainty that
it now knows where they are.

**The shared rule.** All three variants are a **scene with a price**. None of them can kill a
character, none of them can force a choice, and each of them leaves something behind that a later
scene can use. That is what makes them frightening: they are *consequences with manners*.

---

## 22.15 Hooks for the tactical and strategy layers

This chapter is the mission-level description; the layers above and below it consume it rather than
replacing it.

**Downward — the tactical zoom.** A move inside a defended segment becomes the node-card procedure
of `5_CYBERNETIC.md`: zones, tiers, ICE, Trace, and the shared action clock of
`18_CROSS_DOMAIN_STATE.md`. The zoom changes the *resolution*, never the *preconditions*: a target
with no path does not acquire one because the table changed scale.

**Upward — the strategy layer.** For the crossover game, the access classes are the vocabulary in
which **reachability** is held as an asset: a hub position, a gateway relationship, an insider, a
courier network, a licensed operator team. Reachability is accumulated, spent, and — per issue
#344 — **destroyed by the story rather than by an opponent**, which is what makes the era
transition a strategic event and not a patch note.

**Board and table conversion.** Everything here fits on one page: five access classes, the eleven
target properties as a checklist, four outcome bands, four heat states, and the four-tier
opposition table. Tokens for heat, a card per hop, and a die the table has already chosen. No
custom components, no map, no hidden state.

---

## 22.16 What this chapter deliberately does not do

- **No new Skills, STATs or derived statistics.** The skills used are `Interface`, `Infosec`,
  `Program`, `Hardware`, `Research`, `Investigation`, `Sneak`, `Deceive`, `Talk`, `Kinesics`,
  `Tactics`, `Pilot` and `Perceive`, all from `data/rules/skills.json`, unchanged. No parallel
  hacking taxonomy is created.
- **No dice, no values, no probability.** Bands are named, never numbered. Every figure or state
  count marked **TUNING PARAMETER** is a playtest proposal.
- **No restatement of `5_CYBERNETIC.md`** — the four access modes, node cards, privilege tiers,
  Trace, ICE and the damage ladder stay there. This chapter is the mission-level companion.
- **No restatement of `18_CROSS_DOMAIN_STATE.md`** — the action clock, the single-locus rule and the
  realm gateway table are that chapter's.
- **No economy model.** UBI, operator labour, verification farms and black markets are described as
  social facts, not simulated.
- **No ASI stat blocks.** The three swarms have agendas, constraints, indicators and
  vulnerabilities; they have no ratings, and no encounter with them is resolved as a single check.
- **No resolution of the setting's open questions** — the autonomy threshold, the Singularity
  threshold, which cryptography survives, whether the Noösphere is the noösphere, and what Thanatos
  became outside the Solar System all remain open, as their own chapters require.
- **No legacy rewrite.** `RULEBOOK.md`, `rulebook_parts/` and the source snapshots are untouched.
