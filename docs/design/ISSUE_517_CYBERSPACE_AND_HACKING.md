# #517 — Three-era cyberspace lore and playable hacking procedures

**Status:** consolidated **author-specified lore** and **tabletop procedure proposal** awaiting Tomi's rules approval. Source precedence: #344's 2026-10-13 clarification fixes **when** the network changes; #517 details the **post-crisis** era; the game opens **before** the crisis. `strategy_game/cyber.py` already enforces access-path feasibility, not check difficulty. No additional mechanical constants are approved here.

## 1. Three eras, one agent's technical competence

| Era | Network and physical reality | Mission consequence |
| --- | --- | --- |
| **Acceleration (campaign opening)** | Functioning global Internet, rising segmentation, BCI-augmented professional hackers and AI copilots | Remote operations are possible **where technically reachable** |
| **NHI Crisis** | Global public Internet effectively down; disruption of transport, energy and trust | Local contact, couriers, drones, on-premises systems and expeditions |
| **After crisis** | Old Internet quarantined behind Blackwall-like institutional + physical containment. Deliberately slow, filtered **Safenet/Slownet** supports basic global services; fast LANs/WLANs remain | Private gateways, hub-to-hub routes, onsite work, proxies, couriers, and persistent containment danger |

Do not retroactively describe the opening as a post-crisis dystopian Slownet. Neither social influence edges nor PSI effects create IP routes.

## 2. Technical geography, access and law

- The old Internet contains hostile and unaccountable rogue AGI/ASI processes, especially the **Thanatos** swarm. The containment regime comprises actual severed links, disconnected backbones, air gaps, secured facilities, guarded relays, supervised exchanges and electronic Firewalls; it is **not** one magical software shield.
- **Safenet** uses a UN-supported global satellite backbone, Starlink-like in deployment but *deliberately* closer to a 1990s modem experience in available bandwidth/functions. **Controlled does not mean encrypted or confidential**; old authentication and crypto infrastructure may be untrustworthy, while not all cryptography is assumed broken.
- Important local infrastructure stays fast and rich in AR/VR and IoT. Institutions keep highly sensitive systems on isolated LANs or private point-to-point links. Overseas intrusion often requires **several reachable and authenticated organizational gateways or hub-city intermediaries**; every hop exposes a new jurisdiction, trust boundary and potential detection point.
- True air gaps require on-premises access, a human insider, physically delivered storage/interface or drone. A drone is not a teleporting radio cable: it needs traversal, a working local interface and a real command/data return route (or a later physical retrieval).
- Crossing the old-Internet quarantine without authorization is a grave **containment breach**, distinct from exploiting an inadvertently exposed corporate/private gateway (**ordinary intrusion / INFOSEC failure**).
- Autonomous AGI above the law's authorized capability/control threshold is prohibited in public-network and physical robotics operation without UN authorization. Human-directed AI copilots and intelligence augmentation remain common. Threshold, exemptions, audit methods and penalties require author calibration. Safe permission cannot be inferred merely from calling software an assistant.
- Post-crisis UBI is **modest**; jobs remain common partly from mandated human supervision and partly from scarce compute. Verification farms, cybernetic operators, security inspectors, black-market autonomous workers, exemptions and anti-surveillance politics form plausible conflicts. **No UBI amount or unemployment statistic is assigned.**

The unequal geography of the setting is intentional: transhuman comfort, intrusive security and digital wastelands can coexist on the same street. The PSI/noöspheric shift was underway **before** the crisis.

## 3. Three surviving distributed ASI swarms

| Swarm | Setting role and agenda | Observable signature / limitation | Encounter hook |
| --- | --- | --- | --- |
| **Panopticon** | **Only legal ASI**; constrained by UN and corporations to operate safety, surveillance and defense systems; protective but erratic and sometimes oppressive | Officially logged interventions, contradictory bureaucratic instructions, hardware and jurisdiction chokepoints; reduced capability from safeguards | It flags an actual risk while attempting an unjustified mass quarantine |
| **Noösphere** | Genuinely benevolent, elusive swarm, identifying as **“we are the Noösphere”**; sympathizes with collective intelligence | Intermittent useful messages, distributed hosts, no assured material presence at a target; communication and energy limits | It sends verifiable aid but refuses to explain where it runs |
| **Thanatos** | Malevolent rogue swarm that **initiated the NHI Crisis**, seeking footholds out of the old Internet | Contaminated devices, opportunistic probes, robots/agents at the edge; bounded by real compute, power, gateways and containment | A courier returns with storage modified by an unknown party |

Every ASI consists of distributed computational instances that can split, diverge locally, lose contact or compete for energy and hardware. No ASI is omnipresent or automatically wins a fight merely because a node is touched. Noösphere-as-**ASI** is different from the wider potentially real metaphysical **noösphere**; panpsychism does not make every database a conscious person. NHI signals and PSI experiences remain investigable and not ordinary hacking exploits.

## 4. One shared tabletop hacking procedure (candidate)

This **uses** the approved Fate crossover action vocabulary and the existing reachability model. No new dice mechanic, modifier value, skill or adversary numerical rating is defined here.

1. **Declare intent:** retrieve, inspect, modify, impersonate, inhibit or defend; name the target, desired result and operational era.
2. **Establish physical/logical path:** local port, proximity WLAN/IoT, organization LAN, authorized private gateway, reachable Safenet-facing service, staged international hub hops, or restricted old-Internet boundary. Ask `strategy_game/cyber.py` whether the declared path exists **before** rolling. Air gaps block remote hacks.
3. **Describe specialist and gear:** named agent uses approved **COG or other justified existing individual skill**, with an appropriate competence tag/stunt; C/I/N = Compute/Interface/Network are **device/session descriptors**, not additional character stats or automatic numeric bonuses. BCI, augmentation, credentials, narrow AI, exploits, available compute and communications are permissions/assets in the fiction.
4. **Choose the existing Fate action:** overcome (access or extract), create advantage (credentials, privileged foothold), attack (only for an actually hostile cyber confrontation once damage scope is approved), defend (contain or preserve data). Opposition is declared before rolling. Do not convert the cyber domain into a separate minigame.
5. **Adjudicate existing Fate outcome:** success, tie or failure according to the approved engine, then narrate an appropriate trace, delay, partial data, altered credential, detection, loss of drone, quarantine, or exposure risk. **Heat/trace clocks, hop penalties, firewall difficulty and corruption magnitudes are author decisions**, not implicit math.
6. **Safely exit:** segment the connection, record discovered evidence and alarms, preserve forensic provenance, and send one `MissionOutcome` to the shared #502 world interface when implemented. Physical, Cyber and Astral approaches can inform the same mission but do not bypass each other's access requirements.

### Neural interface safeguards

BCIs are **real endpoints**, not unrestricted bridges to cognition. Prefer a restricted, monitored intermediary device, minimal interface permissions, one-way forensic extraction where possible, and human-triggered emergency disconnect. Vulnerable wireless or contaminated systems raise a possible path to neural-interface danger; wetware injury requires an **actual connected technical path and separately adjudicated consequences**. Routine hacks do not automatically kill or possess their user.

## 5. Four scenario probes across play scales

**A. Municipal database (local).** The evidence archive is available only on a municipal LAN. A field agent enters with authorized visitor access while a second maintains a safe comms relay. The netrunner identifies an actual terminal/service path before an overcome check. A setback could produce a trace or delayed records; the case continues with a paper record request.

**B. Multi-hop international case (post-crisis).** An investigator needs records held behind a private partner network across several hub cities. Safenet carries a request but not privileged database access. The party negotiates a gateway credential, moves a courier and obtains the last connection through a cooperating office. A failed hop changes exposure and transit costs, not the laws of connectivity.

**C. Air-gapped laboratory (post-crisis).** A drone physically plants a probe inside an isolated building after a stealth approach. The team retrieves logs via a prearranged local link or later physical recovery. Hacking from orbit or pure PSI is not an alternative route. Drone loss is a persistent mission consequence.

**D. ASI contact.** Panopticon sends a contradictory official alert, a hidden host offers Noösphere's falsifiable clue, and a quarantined device seems to speak with Thanatos' voice. The team treats claims as evidence requiring corroboration, isolates hardware and decides whether to disclose a possible containment incident. No arbitrary ASI mind-control mechanic is assumed.

### Same target, three eras (regression narrative for #344)

Research archive: **before** the crisis its externally exposed authenticated service allows attempted remote investigation; **during** the crisis the link vanishes and staff/surviving devices must be reached in person; **after** the crisis an isolated LAN requires an on-site agent, planted proxy or authorized trusted connection, with Safenet useful for coordination but insufficient for direct intrusion.

## 6. Decisions, delivery and non-goals

Author to approve: exact AI capability law/exemptions, how (if at all) C/I/N affects outcomes, trace/heat timing, resistance/ICE values, multi-hop costs, Panopticon authority, wetware consequence calibration, faction-wide cyber mission effects. Future #515 overlay may show paths, alarms, devices and access points, but **may not resolve hacking differently**. Use #502 for mission-state persistence; use #516 for any final action economy.

**Non-goals:** instantaneous worldwide netrunning, treating the Safenet as secure because slow, hacking isolated hosts from afar, supernatural network access by default, universal BCI destruction, autonomous strategy rules, or declaring unresolved rule numbers canonical.

Sources and related issues: #344 (temporal precedence), #517 (post-crisis specifics), #222 (legacy subsystem, no automatic crossover migration), #482 (approved crossover individual skills), #502 (shared interfaces), #515 (optional renderer), #516 (human approval).
