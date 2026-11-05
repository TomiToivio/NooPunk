# Project Plato / EISS, EuroNET and the continental security architecture (#1200)

> **Status:** canonical setting direction, recorded from [#1200](https://github.com/TomiToivio/NooPunk/issues/1200).
> It defines the EU's information-security, network and psychotronic infrastructure and the powers that go with it.
> It does **not** change the immutable CWN core, and it introduces no new rules engine: cyber scenes use CWN
> Hacking, investigations use `src/rules/investigation.py`, and the world is represented with the existing
> Physical / Cyber / Social / Story graphs.

**Related:** [Europol Helsinki frame](EUROPOL_HELSINKI_1114.md) ·
[Alternate history](ALTERNATE_HISTORY_1114.md) ·
[Fortress Europe](CANON_FORTRESS_EUROPE_1113.md) ·
[Post-NHI world](POST_NHI_WORLD_1005.md) · [NHI Crisis](NHI_CRISIS_921.md) ·
[Noösphere](NOOSPHERE.md) · [cyberspace design](../design/ISSUE_517_CYBERSPACE_AND_HACKING.md) ·
[Nordic/Crisis memo](../proposals/CATASTROPHIC_NORMALITY_AND_NORDIC_1946_MEMO_DRAFT.md)

---

## 1. Naming: four words for one system, and one word you must not use for it

| name | status | who says it |
|---|---|---|
| **Project Plato** | the original project name, still used internally for the programme and its older subsystems | engineers, procurement, archives |
| **European Information Security System (EISS)** | the **official institutional name** of the deployed system; this is what statutes, audits and budget lines say | EU institutions, Europol, courts |
| **"Plato"** | natural operational shorthand | everyone who works with it |
| **"the panopticon"** (lower case, in quotes) | the **critical description** used by journalists, dissidents and privacy campaigners — a comparison, never an official name | press, NGOs, defendants |

### 1.1 The name collision, stated once

The rulebook already contains a **capital-P `Panopticon`**: a corporate ASI captured and damaged into
controllability ([`rulebook/10_SINGULARITY_CRISIS.md`](../../rulebook/10_SINGULARITY_CRISIS.md) §9.4.2, §9.16.1),
with its own legal position and its own horror — "both victim and oppressor".

**EISS is not that entity, and the two names must not be used interchangeably.** The convention:

* **`Panopticon`** (capitalised, no quotes) — the damaged corporate ASI and its infrastructure;
* **"a panopticon"** (lower case, quoted) — what a critic says EISS is like. It is an accusation, not a system.

**[OPEN for the author]:** the two readings are still compatible in one story — the EU's system could be described
by critics as "our Panopticon, only slower", and the ASI could be rumoured to run parts of it. That ambiguity is
good material, but it must stay an in-world *claim* until the author decides, because §9.16.1 gives that ASI a legal
status the EISS does not share.

---

## 2. What Plato is

A **huge, strange, deeply layered cybernetic information-security system**, built in time to protect Europe before
the NHI Crisis. Its original purpose was network security and keeping the European firewall; the monitoring
apparatus it already had grew — by mission creep, not by a single decision — into a continent-scale **defence,
intelligence, surveillance and psychotronic infrastructure**.

It is **not** an ASI, and it is not a single mind:

| it is | it is not |
|---|---|
| an unwieldy federation of legacy systems, hand-written **GOFAI**, rule engines, expert systems, limited modern AI, quantum machines and psychotronic subsystems | a unified superintelligence |
| operated by **enormous numbers of humans** — coders, analysts, operators, auditors, supervisors, translators | autonomous in its consequential decisions |
| **heavily regulated**: statutes, audit trails, authorisation levels, procurement law, parliamentary oversight | a secret cabal, though it contains secrets |
| **genuinely effective**: the EU is comparatively intact after the Crisis | omniscient; its picture is partial, delayed and often wrong |

**The political ambiguity is the point.** EISS is necessary *and* dangerous, and the setting holds both: the same
machinery that keeps the lights on makes dissent legible to the state. A story that resolves this into "evil
surveillance machine" or "benign protector" has thrown away the best material.

### 2.1 Why the European way survived

The EU survived partly **because its bureaucracy and regulation kept it out of suicidal AGI/ASI accelerationism**.
The United States led the race and the race ended catastrophically there; Europe's slower, supervised, paperwork-bound
approach turned out to be an existential advantage it did not intend.

**This is not a superiority claim.** European AGI is *not* better than the American systems were — it is smaller,
slower, censored, supervised and deliberately unambitious. **Mistral** is the only company permitted to develop
anything approaching AGI inside the EU, under strict limits and human oversight. Europe's real lead is elsewhere:
quantum computing, quantum-consciousness research, psionics, psychotronics, biopunk and solarpunk engineering.

The texture that follows: strategic infrastructure written in **Lisp and Prolog**, expert systems older than their
operators, AI output reviewed by a person with a stamp, evidence moved by courier, and a quantum-psychotronic
laboratory two floors above a canteen that has served the same soup since 2031.

---

## 3. Networks after the collapse of the old Internet

The topology is **Cyberpunk RED / *Johnny Mnemonic***, not a seamless global grid. Four classes of connectivity,
and the class decides what a scene can even attempt:

| # | network | what it is | who can reach it | game consequence |
|---|---|---|---|---|
| 1 | **Old Internet** | fragmented, semi-abandoned digital wilderness: autonomous agents, rogue processes, compromised infrastructure, dead services that still answer | anyone reckless enough to connect | connecting is a risk, not a resource; a scene there has no guarantee of return |
| 2 | **Closed organisational networks** | agencies, corporations, laboratories, hospitals: isolated private networks, often air-gapped | people physically present, with credentials, implants or media | **physical entry, an on-site terminal, a credential, removable media or a local access point is required before CWN Hacking can even be attempted** |
| 3 | **EuroNET** | the EU-maintained, comparatively safe **public** network behind the perimeter | any EU resident with an account | email, forums, blogs, OSINT, slow services; no unconstrained autonomous agents, no broad connectivity |
| 4 | **Couriers** | physical transport of storage media and of data held in people | whoever holds the media or the person | interception, handoff and authenticity are investigation beats |

**EuroNET is deliberately constrained**: 1990s-feeling, conservative, slow, hostile to automation. That is a
security trade-off made on purpose, not backwardness — and it is why a modern player used to frictionless networks
finds the setting uncanny in the right way.

### 3.1 The Great Firewall is the Plato/EISS perimeter

The continental firewall is **the perimeter of Plato/EISS**, not a separate superintelligence: filtering, protocol
control, egress rules, inspection and throttling, run by the same bureaucracy as everything else.

**Naming [OPEN]:** *AEGIS* has been floated as a designation for the firewall **subsystem**. It is **not canon** and
must not be used as a proper name until the author confirms it — other AEGIS uses may exist in the setting, and a
second capitalised acronym is exactly how a setting acquires two contradictory entities.

---

## 4. Who may do what: Europol, Eurodef, UNSA, national authorities

The state has immense technical capability; a **field agent has limited legal authority**. That gap is the game.

| actor | mandate | may | may not |
|---|---|---|---|
| **Europol** | EU cross-border **civilian** law enforcement and intelligence support; operates and secures Plato/EISS, digital defence, investigative surveillance and the EU's psychotronic infrastructure | coordinate investigations, request national action, operate EU systems, analyse, protect the perimeter | arrest or search in a member state on its own authority; ignore national prosecutors |
| **Eurodef** | EU **military** defence, including military cyber defence and strategic threats | defend military networks, act under defence authorisation | run civilian investigations; take over Europol's civilian systems |
| **UNSA** | UN **X-risk** jurisdiction | intervene on existential-risk events, coordinate globally | act as a world police force; replace member-state or EU authority |
| **National authorities** (e.g. Finnish police, Supo) | arrest, search, prosecute under national law | everything a sovereign police force may do | override EU fundamental-rights guarantees |

### 4.1 The authorisation ladder

Every intrusive action sits on a rung, and the rung is what a scene argues about:

| rung | action | authority required | who signs |
|---|---|---|---|
| 0 | routine **OSINT** on public EuroNET material | none beyond the case | the investigator |
| 1 | **authorised database search** (records, registries, Europol holdings) | case authorisation and a purpose test | the case officer's supervisor |
| 2 | **intrusive surveillance** (live intercept, location tracking, BCI monitoring) | a warrant | a judge or the designated review authority |
| 3 | **offensive hacking** against a third party's system | a warrant plus a Europol technical authorisation | judge + Europol operations |
| 4 | **emergency containment** (isolation, takedown, firewall closure) | a pre-authorised protocol for bounded actions; a human authorisation for consequential ones | duty officer within the protocol; a senior officer above it |

**Bounded defensive automation is not the same as a decision.** The perimeter may drop a hostile packet, throttle a
flood or isolate a segment at machine speed under a written protocol. It may not, on its own, take down a hospital,
raid a private network, identify a person as an enemy or authorise force. **That distinction is the whole design:**
the bureaucracy is the safety mechanism, and the paperwork is the scene.

**Accountability is real**: audits, inspectors, parliamentary questions, leaks, appeals, and cases that collapse
because evidence was obtained one rung too high. Every one of those is playable.

---

## 5. Psychotronic infrastructure

The EU runs psychotronic systems as **civil infrastructure** — the same way it runs the grid — and the reasons are
good and frightening at once: after the Crisis, population-level psychological stability is an emergency service.

| operational use | what it does | safeguard | risk |
|---|---|---|---|
| **detection** | identifies anomalous psychic activity and unlicensed psychotronic devices | sensor-level only; no attribution without a case | false positives, and the labelled person's life |
| **monitoring** | watches for destabilising phenomena and coordinated psychic events | retention limits and audit | mission creep into political surveillance |
| **stabilisation** | calm, ground and reintegrate populations after shocks | consent where possible, clinical oversight | dependence, dulling, "the state decides how you feel" |
| **emergency containment** | isolate a psychic event, shield a district, suppress a cascade | human authorisation and a declared end condition | the shield does not know who is inside it |

**Do not assume it works cleanly.** Psychotronic intervention is partial, side-effecting and contested; the
infrastructure has failures, and those failures are cases. **Do not assume it is evil.** Its operators are people
doing a job, some of them badly, some of them well. The ethics live in the gap between the two sentences.

---

## 6. Plato as the investigator's instrument

EISS is the campaign's **investigative UI**, in the spirit of *Orwell: Keeping an Eye On You*: records retrieved,
evidence correlated, people, places and systems followed, and a human deciding what to forward or act on.

The loop the campaign runs:

```
case authorisation → records / OSINT → graph exploration (Physical, Cyber, Social)
→ interviews and physical access → targeted cyber investigation (CWN Hacking)
→ evidence assessment → lawful action or emergency intervention → consequences
```

**The evidence graph is not truth.** Plato gives false positives, stale records, contaminated feeds, bad
translations, archaic expert systems, compartmentalisation, malicious operators and plain bureaucratic error. An
investigator who treats the graph as the answer is the antagonist of their own case.

### 6.1 Six scenes the architecture makes possible

1. **EuroNET OSINT** — public forums, a blog that stopped updating in 2038, a shipping notice; no warrant needed and nothing conclusive.
2. **Warranted search of a private system** — rung 2 or 3, a judge's signature, and a defence lawyer who will ask how the hash was preserved.
3. **Air-gapped corporate network** — no remote path exists; the team needs a terminal, a badge or a body in the room before CWN Hacking is legal or possible.
4. **Compromised data courier** — a person carrying the evidence; interception, authenticity and the courier's own motives.
5. **Rogue agent from the old Internet** — something on the abandoned net is reaching into EuroNET; the perimeter is holding, for now.
6. **Psychotronic anomaly** — a stabilisation field with a hole in it, or a false positive that has already labelled someone.

---

## 7. Texture and tone

Retrofuturistic European bureaucracy meets experimental quantum-consciousness technology:

* infrastructure in **Lisp and Prolog**, maintained by people who know what a macro is;
* **Mistral-class** models that are censored, supervised and visibly less capable than the American systems were;
* **couriers with media**, because the network cannot be trusted with the evidence;
* **auditors** who are characters, not scenery;
* **satire and stakes in the same scene** — the memo's rule, *consistent consequences, flexible seriousness*
  ([narrative memo](../proposals/CATASTROPHIC_NORMALITY_AND_NORDIC_1946_MEMO_DRAFT.md)).

Players are **the authorities**: they have formidable institutional tools and must still find a judge, a national
officer, a lab and a plausible lie. Not every case escalates; ordinary crimes stay ordinary, and the cosmic material
is earned.

---

## 8. Open decisions for the author

1. **`AEGIS`** — is it the firewall subsystem's name, or does the acronym already mean something else in the setting?
2. **EISS and the Panopticon ASI** — separate systems (this document's assumption), the same system seen twice, or rumour only?
3. **Who owns EISS** — the Commission, the Council, an inter-agency directorate, or Europol itself as operator?
4. **Mistral** — a single licensed vendor, or one of a small licensed list?
5. **Psychotronic stabilisation** — consent-based service, emergency power, or both depending on the district?
6. **EuroNET account tiers** — does ordinary public access differ from police/institutional access in kind or only in permission?
7. **Courier regulation** — a licensed profession, a black market, or both?

## 9. Inspirations

*Cyberpunk RED* (fragmented connectivity, local hacking, isolated networks) · *Johnny Mnemonic* (couriers,
transported data) · *Cyberpunk 2077*'s NetWatch as a **conceptual** analogy for Europol's digital-security role, not
its network architecture · *Orwell* (surveillance as investigation, and the analyst's responsibility) · the Turing
police of *Neuromancer* (institutional policing of dangerous AI) · *The Conversation* (surveillance as craft and
complicity).

## 10. What this document does not do

* No CWN change; no new surveillance, hacking or psychotronic rules engine.
* No new graph family: the world is still Physical / Cyber / Social / Story (the Astral graph stays deferred, #1178).
* No rewrite of `rulebook/10_SINGULARITY_CRISIS.md` §9.4.2 — the collision in §1.1 is flagged for the author, not resolved by an agent.
* No numbers: no bandwidth, no staff counts, no budget, no device statistics. Those are the author's.
