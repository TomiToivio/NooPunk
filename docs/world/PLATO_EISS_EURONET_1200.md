# Project Plato / EISS and EuroNET: European cybernetic defence (#1200)

> **Status: canonical setting and operational reference.** Read alongside [Fortress Europe](CANON_FORTRESS_EUROPE_1113.md) and the [Europol Helsinki campaign frame](EUROPOL_HELSINKI_1114.md). This is worldbuilding and scene guidance, **not a new rules engine**. In case of a question about individual investigators' authority, the Europol campaign frame governs.

## Naming and history [CANON]

**Project Plato** was the original project; **European Information Security System (EISS)** is the official name of the operational, continent-scale system. **Plato** is standard operational shorthand. **Panopticon** is a *critical unofficial nickname*, used by journalists, dissidents and privacy advocates, not the system's formal designation. Historical uses of “Panopticon” to mean an official European AI refer to Plato/EISS instead. Do not confuse it with a rogue ASI.

EISS was built *before* the NHI Crisis to secure European information networks and maintain the continental perimeter. The official name of that perimeter in operational documents is the **Plato/EISS perimeter**. **AEGIS is not established canon**: no separate firewall AI or independently named subsystem is required.

Pre-Crisis cybersecurity telemetry, network access controls and defensive monitoring gradually became civil defence, intelligence correlation, investigatory surveillance and psychotronic support infrastructure. Its protective origin and the later expansion of surveillance are both true. It works well enough for Europe to have survived the Crisis, but that fact cannot settle the arguments about proportionality, privacy or coercion.

## What Europe built [CANON]

The United States' comparatively advanced AGI/ASI acceleration ended in catastrophe. Europe's regulatory constraints, slower deployment and insistence on human review became a survival advantage rather than evidence of a more advanced European AGI. **Mistral is the only EU company permitted to work on systems approaching AGI**, under strict controls, censorship limits and human supervision. Its AI is not superior to the old American frontier.

Plato is a *heterogeneous cybernetic bureaucracy*, not a single thinking supercomputer: decades of Lisp and Prolog code, manually programmed GOFAI and expert systems, rule engines, audit trails, narrow AI, human analysts, operators, software maintainers and supervisors. Some parts are brittle or incompatible; others are remarkably resilient. **Bounded, preauthorised defensive automation** can react at machine speed. Consequential investigation, intrusive collection, escalation and extraordinary intervention require identifiable human authorization and review. The huge human workforce both slows the system and prevents unilateral runaway operation.

The European comparative advantage is **experimental quantum computing, quantum-consciousness science, psionics, psychotronics, biopunk and solarpunk**. Quantum and psychotronic installations complement old-fashioned conventional systems; they do not magically eliminate unreliable inputs, political conflict or scarcity. A claimed capability may be verified, officially exaggerated, secret or still controversial. Show these statuses distinctly.

## Connectivity model [CANON]

| Layer | Access and risk | Investigation consequence |
| --- | --- | --- |
| **Old Internet** | Broken, dangerous and largely outside the EU perimeter, with autonomous agents, rogue AI and compromised infrastructure | Air-gapped handling, exceptional access controls, containment and hazardous attribution |
| **EuroNET** | EU-maintained *public* network behind EISS; intentionally conservative and reminiscent of 1990s email, blogs, forums and directories | Public OSINT, lawful communication and information discovery, not a seamless global cyberspace |
| **Closed organizational networks** | Isolated agency, corporate and laboratory networks, sometimes entirely offline | A warrant and a remote address do not create connectivity; physical entry, local terminals, credentials, media or implants may be needed |
| **Physical data couriers** | Trusted people transporting storage media, sometimes between entirely disconnected networks | Chain of custody, courier interception, tampered media, contradictory manifests and physical surveillance |

EuroNET is *not* a single omnipotent police database. The restricted public network, EISS internal records, member-state registries and sealed private networks have separate access paths and authorization levels. The perimeter is an **EISS service**, not an extra autonomous super-AI. Avoid the global always-online architecture of *Cyberpunk 2077*; *Cyberpunk RED* and *Johnny Mnemonic* are closer analogies.

## Relation to Safenet and the Blackwall — and one word this page must not use

`rulebook/22_CYBERSPACE_AFTER_THE_CRISIS.md` (#517, transcribed from the author's #344 text) already
names three things, and it names them before #1200:

- **the Blackwall** — the containment regime that separates the quarantined old Internet from human
  infrastructure. Not a magical software barrier: severed backbones, air gaps, one-way exchanges,
  hardened facilities, manual authorisation, offline verification (§22.3).
- **Safenet**, colloquially **Slownet** — the UN-backed **global** public network built after the Crisis,
  satellite-backed, rationed and deliberately bad (§22.4).
- **a terminology rule**: *"Firewall is not an in-world name"* — `RULEBOOK.md` §34 retired it as an
  Eclipse Phase-derived term — and *"Great Firewall … is unrelated and must not be confused with it"*
  (§22.3).

So this page does not call the European perimeter the "Great Firewall". **The Plato/EISS perimeter is the
European operational component of the Blackwall**, and "Great Firewall" survives only as a journalistic and
legacy phrase, on the same shelf as "Panopticon". `data/world/terminology_1200.json` records the terms and
their status so a later document cannot quietly promote one.

**[OPEN — author decision] EuroNET and Safenet.** #1200 introduces **EuroNET** as the EU-maintained public
replacement network; #344 already has **Safenet** as the global public network. Two readings are
consistent with both texts:

1. **EuroNET is the European service on Safenet** — same constellation and gateways, with the EU's own
   portal, registration and content rules on top. Users experience "EuroNET"; the transport is Safenet.
2. **EuroNET is an EU-only network behind the perimeter**, with Safenet as the slower global link beyond
   it. Two hops, two jurisdictions, and a clean explanation for why European services feel faster than
   the global network and stop at the border.

Reading 1 is cheaper for continuity; reading 2 is sharper for the setting's politics and gives the
perimeter something to *do*. This page does not choose. Until it is chosen, write "EuroNET" for what
European users see and "Safenet" only when the global transport is the subject, and do not state in new
text that they are the same network.

## Institutions and authority [CANON at policy level]

**European institutions** set the legal mandate and retain democratic and administrative oversight of the civilian security infrastructure; independent judicial, parliamentary and data-protection review can inspect or challenge use. Specific statutes and chains of appointments are **[OPEN]**, not invented here.

**Europol** is the principal civilian *operator and investigatory user* of EISS/Plato and its cyber-defence and psychotronic stabilization services, subject to EU-level governance, auditors and national legal partners. Its cyber investigators are the setting's NetWatch/Turing Cops: skilled at identifying rogue agents, protecting networks, performing forensic correlation and executing *authorized* infiltration. Operating infrastructure does **not** grant a field officer unrestricted search or arrest powers.

**Eurodef** owns the military-defence side of cyber and strategic-threat operations. Cross-boundary incidents need interagency coordination rather than a universal command override. **UNSA** handles cross-border existential/NHI risks under contested and limited mandates, and may request cooperation; it does not own Europol or override national law. **Finnish police and national authorities** retain ordinary coercive powers on Finnish soil, as the Europol campaign frame explains.

Operational authorization is deliberately graduated:

1. **Public EuroNET OSINT:** ordinary lawful access; source, date and provenance still matter.
2. **Internal records:** role-based, logged and purpose-bound searches with data-minimization obligations.
3. **Intrusive surveillance or private-system search:** case-specific judicial or otherwise competent legal authorization and relevant national cooperation.
4. **Offensive cyber infiltration:** explicit authorization, target and scope restrictions, proportionality, audit trail and a lawful route to local access.
5. **Emergency containment:** tightly bounded defensive measures under pre-existing emergency protocols, with prompt notice, independent review and avenues for challenge; not a blank cheque.

These are **fictional operational categories**, not claims about the exact legal powers of real-world Europol. A successful hack is not proof of admissible evidence, and access to a system is not authority to arrest a person.

## Psychotronic defence [CANON at functional level]

Europol operates major civilian psychotronic facilities built for **detection**, **monitoring**, **stabilization** and **emergency containment** after the Crisis. Maintaining population-level psychological stability is a critical service. Powerful systems can still generate false positives, coercive pressure, unforeseen feedback, side effects and political abuse. Routine population-wide manipulation is *not* presumed harmless or lawful. Independent review, documented scope, proportionality, consent where practicable, time limits and post-incident scrutiny are story-relevant safeguards. Do not claim a definitive scientific explanation for every anomalous signal.

## Gameplay integration: existing graphs, scenes and tags only

Plato is a **fallible investigative UI** inspired by *Orwell: Keeping an Eye on You*: a search panel and linked-record view for persons, locations, institutions, devices, events, leads, authorizations and provenance. Results are **claims and evidence with sources**, never direct access to canonical truth. No universal reputation scores, automatic convictions, predictive guilt or new surveillance points.

- **Social graph:** witnesses, targets, institutional contacts and interagency relationships; Social and Personality Tags guide conversation and access.
- **Cyber graph:** EuroNET services, isolated organizational systems, credentials, terminals, evidence stores, EISS interfaces and permitted connections. Missing edges mean *no remote access*, even for skilled hackers.
- **Physical graph:** offices, server rooms, substations, courier routes, terminals and guarded premises; physical movement creates or removes cyber access opportunities.
- **Story graph:** the existing Series → Episode → Scene progression with Goal Tags and Clue Tags.

Use existing **Investigation, Social, Exploration, Cyber and Action scenes**. CWN hacking resolves uncertainty in Cyber scenes; the CWN core remains immutable, and graph/tag systems remain the existing NoöPunk overlays. No new hacking, psychotronic, warrant or surveillance rules engine is authorized by #1200. The Astral graph remains postponed.

**Case loop:** case assignment and legal basis → public OSINT or approved records → connect graph leads → interview or visit site → warrant/authorization if needed → existing CWN cyber or physical procedure → independent evidence assessment → coordinated lawful action or bounded emergency response → logged consequences and scrutiny. Evidence may be wrong because of contamination, human error, rogue operators, outdated expert systems or psychotronic side effects.

### Helsinki / European starter cases

1. **Sörnäinen courier:** an ordinary stolen courier case reveals storage media destined for a closed medical network. EuroNET traces the sender; the records system cannot read the air-gapped destination. Finnish police must handle the search, while a compromised courier log becomes a Clue Tag.
2. **Ratakatu false positive:** an EISS alert associates a resident with a rogue agent. A Prolog inference rule is outdated; a clerk's translation compounds the error. Europol must check sources and obtain a lawful basis before taking the matter further.
3. **Helsinki–Tallinn psychotronic anomaly:** two monitoring stations disagree on whether a distress signal is an external attack, faulty sensors or a human emergency. Eurodef is consulted but does not take over civilian investigative authority. The case may conclude without any cosmic revelation.
4. **Old-Internet incursion:** an attempted penetration meets preauthorised firewall automation immediately; investigating its origin needs logged human review, specialist containment and perhaps access to a disconnected European lab.

## Consistency / implementation checklist

- Treat **EISS = Project Plato**; “Panopticon” is always an unofficial critique, not official branding.
- **EuroNET = public**; EISS records are restricted; closed organization networks do not silently become remotely accessible.
- Europol **operates civilian** defences, Eurodef handles **military** defences, UNSA coordinates **X-risk**, Finnish police keep **national coercive authority**.
- Human review is real but never described as blocking automated packets one by one.
- Preserve Mistral's regulated near-AGI monopoly, Europe's leadership outside AGI, and epistemic uncertainty about psychotronics.
- Model investigative leads with **existing graphs/tags/scenes** only; do not create a second evidence model.
- Existing canon and code remain the source for rules and scene behavior; this text provides content/interaction guidance.

**Terminology record:** [`data/world/terminology_1200.json`](../../data/world/terminology_1200.json) — which word is the name, which is a nickname, which is retired, and which question is still open.

**Related:** #1200, #1113, #1114, #1178, #1184, #1194, #517.
