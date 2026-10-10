# Cybernetic Systems

This chapter defines the player-facing cybernetic and psychotronic capabilities explicitly specified for the default Helsinki / UNSA campaign. It does **not** define numeric gear statistics. The cyberspace surface itself is specified below, in **Cyberspace: the four access modes** (issue #222).

## Standard UNSA augmentation package

A new UNSA graduate is normally offered a government augmentation package. The package is defined by **capability**, not by mandatory invasive hardware.

### Secure interface

The agent receives a secure BCI or non-invasive equivalent supporting:

- encrypted silent communications;
- HUD / AR presentation;
- authenticated access to issued systems;
- direct control of authorized tools;
- access to the embedded forensic AI.

### Local compute, storage and intelligence augmentation

Standard issue includes encrypted local compute and storage sufficient for:

- evidence caching;
- secure AI-copilot operation;
- live translation;
- semantic search;
- evidence cross-referencing;
- attention and workflow support.

COMPUTE, INTERFACE, NETWORK, storage, bandwidth and hardening are properties of devices, implants and agents, not additional character STATs.

### Forensic sensorium

The standard visual/sensor suite can expose three overlays on the same environment:

1. **Physical** — low-light, thermal/multispectral, depth, biometric, trace-evidence and material overlays.
2. **Cyber** — local networks, nearby devices, cameras, drones, cyberware and machine-authentication state.
3. **Astral / Noetic** — psychotronic warnings, gross noetic anomalies, psychic residues and possible Noöspace bleed-through where detectable.

The layers can be filtered or combined. They produce evidence and uncertainty, not automatic answers.

### Secure sensory streaming

Authorized sensory feeds can be shared with:

- the agent's local forensic AI;
- the field partner;
- a remote human controller;
- other authorized team members.

Some missions may require continuous streaming for evidence integrity, officer safety or X-Risk oversight. Compromise, spoofing, disconnection and legal restrictions remain possible.

### Psychotronic protection

Standard graduates receive basic psychotronic defensive capability:

- psychic-intrusion warning;
- basic shielding;
- emergency dampening/firewall mode;
- grounding and cognitive-stabilization support;
- gross anomaly detection.

This supports the trained **Psychic Defence** skill. It does not grant specialist PSI powers.

## Biological-purity and non-invasive characters

Implants are common but not compulsory.

Where practical, UNSA offers the same professional capability through smart contacts/glasses, wearables, external BCI, hardened handheld systems, cyberdecks and portable psychotronic sensors. A character who rejects invasive augmentation remains fully playable.

The trade is fictional and situational: external systems may be less seamless, while implanted systems create their own security, privacy and compromise risks. No numeric modifier is defined here.

## Embedded forensic AI

Standard field agents have access to a limited multimodal forensic AI.

It is **not AGI**. General reasoning remains below the 2026 frontier-multimodal benchmark used as a design reference, while narrow forensic tools may exceed human performance in specific tasks.

The AI may analyze and advise. It may not autonomously establish personhood, declare NHI status certain, authorize lethal force or replace the investigator's judgment.

## Quick access versus deep hacking

Ordinary issued interfaces may support routine authenticated access, device inspection and simple field interactions.

**Deep hacking is specified below, in [Cyberspace: the four access modes](#cyberspace-the-four-access-modes)** (issue #222). Nothing in the standard augmentation package creates a free-form instant-hack button or silently restores older withdrawn BCI/Compute/Connection/Infosec mechanics.

## Standard rookie field kit

A newly graduated field agent normally has access to:

- service firearm and ammunition;
- stun baton / less-lethal option;
- restraints;
- concealable ballistic protection;
- environmental mask / respirator;
- UNSA credentials and encrypted communications;
- body/sensor recorder;
- evidence collection kit;
- portable forensic scanner;
- compact reconnaissance drone;
- hardened offline storage;
- CBRN/radiation sensor;
- psychotronic detector;
- small anomalous-evidence containment package.

Heavier armor, specialist weapons, large drones, vehicles, advanced containment systems and other mission-specific hardware are issued as required rather than treated as permanent personal inventory.

This list defines **availability and function only**. Equipment statistics remain undefined.

---

## Where things live

- **Implant catalog** — the campaign-facing list of cybernetic and psychotronic implants is
  `rulebook/9_FIELD_CATALOGS.md` §3 (light descriptions; no slot limits, no numeric stats).
- **Resleeving, continuity and the immortality gap** — `RULEBOOK.md` §45 (Confederation,
  Orion, resleeving and elite immortality).
- **Psychotronics as a category** — `RULEBOOK.md` §46 and `rulebook/6_PSYCHIC.md` §A.
- **Cyberspace, graph hacking and the shared action economy** — this chapter, *Cyberspace: the four access modes*. The shared action-point system itself is #217/#225; cyber hardware statistics are #221/#228; PSI special powers are #223; astral projection legality is #224; evidence handling is #226. **The shared action-point economy is now specified in [`rulebook/18_CROSS_DOMAIN_STATE.md`](18_CROSS_DOMAIN_STATE.md)**, which is the one canonical contract this chapter's DRAFT clock defers to; it does not redefine the clock here.

**Continuity is a loaded setting question, not a respawn button.** Cortical-stack-like
technology, backup/restore, resleeving and continuity ledgers record and move minds — but
whether they transfer consciousness or only copy memory is **deliberately unresolved**
(`RULEBOOK.md` §45). Do not implement automated resurrection.

---

## Cyberspace: the four access modes

**Status: NOÖPUNK NATIVE — issue #222.** Every number below is **DRAFT pending calibration**, and the action-point economy is **provisional until #217/#225 fix it**.

Access is not one activity. The same character, in the same hour, moves between four modes with different reach, latency and risk. A mode is chosen by **where the character is and what path they use** — never by a skill rating, and never by a single "hack" action.

| Mode | Precondition | Reach | Latency | Authority |
| --- | --- | --- | --- | --- |
| **1. Global WWW / telepresence** | any networked device, no local presence | planetary public services, open data, remote-operated platforms | WAN (high) | none — a guest everywhere |
| **2. Embodied local AR + WLAN** | physically inside the local RF envelope | cameras, doors, vehicles, wearables, local mesh, qualified IoT | LAN (low) | local trust: physical presence **is** the privilege |
| **3. Node/edge graph hacking** | a foothold in a segmented network | the deep subsystem below | segment | earned per node, one tier at a time |
| **4. Immersive VR** | a full-sensorium dive rig | a gestalt view of an entire segment | lowest | inherited from the dive, not the body |

**Mode 4 trades the body for the network.** While fully immersed, the character's physical body is present and vulnerable but **cannot be controlled by the projected consciousness** until the dive ends. That is the explicit price of the deepest access, not a footnote; the same legality rule governs astral projection (#224).

Modes 1 and 2 are ambient and mostly legal; mode 1 is what an ordinary phone or laptop does, and mode 2 is what walking into a building does. Only modes 3 and 4 are *intrusions*, and only they use the procedure below.

## Graph hacking: nodes, edges and privilege

**A node card is the tabletop object, and the computer-game graph UI renders the same card one-to-one** — no hidden state, no separate computer rules.

A node card carries: `id`; `zone` (its network segmentation); `hardening` (a difficulty value from the core ladder); `privilege` tiers reachable; `ice` (see below); `defenders` (software agents, humans, AI); `edges` (neighbours and traversal cost); and `containment` (what fires when Trace fills).

Privilege is **earned per node, one tier at a time** — a foothold somewhere does not grant anything elsewhere, and segmentation is what stops a graph from being one big door:

- **T0 Observe** — read, watch, fingerprint.
- **T1 Operate** — command what the node already trusts.
- **T2 Escalate** — change the node's own rules, reach its neighbours.
- **T3 Control** — act as the node's owner, within its zone.
- **T4 Own** — rewrite the node and its containment.

Each tier above T0 is its own check. **DRAFT: +2 to the node's hardening per tier above T0.**

### Procedure, on the shared action clock

**DRAFT (provisional until #217/#225):** every participant — intruder, software agent, human or AI defender — has **3 actions per exchange**, spent from **one shared clock**. There is no separate hacking turn.

1. **Map** — find edges and zones. `INT + Infosec + 1d10` against a difficulty set by the zone's *concealment*, not its hardening.
2. **Approach** — take T0 on one node. `CYB + Infosec + 1d10` against that node's hardening.
3. **Escalate** — climb exactly one tier. `CYB + Program + 1d10` against hardening plus the tier surcharge.
4. **Act** — do what that tier actually permits. Nothing above it is available.
5. **Cover** — erase traces. Opposed `INT + Infosec + 1d10` against the defender's counter-roll.

**Trace is the detection clock** (DRAFT 0–8). A failed check adds 1; a loud action adds 1–2. When Trace fills, the node's `containment` fires — and containment is written on the card, so the intruder can read the risk before taking it.

**ICE**, in original terms, describes behaviour rather than a stat block:

- **Sentry** — watches. Raises Trace, never chases.
- **Barrier** — denies. Blocks a tier; does not pursue.
- **Hunter** — counter-attacks the intruder's session directly (software damage, see below).
- **Warden** — contains. Locks the segment and holds the intruder inside it.

**Defenders are actors, not statistics.** A software agent has its own actions and a script it follows; a human defender rolls normally with their own skills; an AI defender can be faster but is **capped by its permissions** — it cannot exceed the authority the node gave it, which is exactly why segmentation still works.

## Software, hardware, and *conditional* wetware

Damage runs down a ladder, and it **stops before the brain unless a real neural path exists**.

1. **Software** — session-level. Lost privilege, burned exploit, a closed session. Recoverable by re-entry.
2. **Hardware** — device-level. A bricked deck, a fried implant, corrupted storage. Requires physical access and repair time.
3. **Wetware** — reachable **only through an actual vulnerable connected neural path**. An invasive BCI on an unhardened gateway is the *precondition*; a hardened deck, an external device, or a character with no BCI makes wetware **unreachable, whatever the attacker rolls**.

> **Device compromise is not brain compromise.** There is no universal brain-hack, and no check reaches a mind the network cannot physically reach.

**Emergency disconnect is always available and always costs something.** You leave the dive, you lose uncommitted work, and a session that was *crashed* rather than closed may leave you stunned.

**Cybersecurity without a BCI is fully playable.** A character using a phone, laptop or cyberdeck operates in all four modes; their exposure is to software and hardware damage and their **wetware risk is zero**. This is the setting's mainstream rather than a lesser build: after the malevolent Singularity many people reject implants entirely and use phones, laptops, or nothing networked at all.

**Neurotechnical gateways** are the narrow, guarded exceptions that make wetware risk realistic without making it normal — a medical neural bridge, a military dive rig, a cheap badly-hardened BCI. They are named in fiction and audited in play, not assumed.

## Worked example: one intrusion on the shared clock

All numbers **DRAFT**. Target: a clinic's records segment. Intruder: `CYB 6`, `INT 7`, `Infosec 4`, `Program 3`. Node: hardening **13**, zone concealment **15**, a **sentry** ICE, containment *"lock the segment, alert the human operator at Trace 4"*.

| Exchange | Action | Roll | Result |
| --- | --- | --- | --- |
| 1 | **Map** (1 AP) | `INT 7 + Infosec 4 + 1d10(5) = 16` vs concealment 15 | success — two edges, one to the records node |
| 1 | **Approach** (1 AP) | `CYB 6 + Infosec 4 + 1d10(4) = 14` vs 13 | **T0 Observe** on the records node; Trace 0 |
| 2 | **Escalate → T1** (1 AP) | `CYB 6 + Program 3 + 1d10(6) = 15` vs 13+2=15 | **T1 Operate**; Trace 0 |
| 2 | **Act** — pull one record (1 AP) | — | loud: **Trace 1** |
| 3 | **Escalate → T2** (1 AP) | `CYB 6 + Program 3 + 1d10(3) = 12` vs 13+4=17 | **failure** — **Trace 2**; the sentry wakes |
| 3 | **Cover** (1 AP) | `INT 7 + Infosec 4 + 1d10(6) = 17` vs defender 14 | traces brushed — **Trace 1** |
| 4 | *(defender's clock)* | sentry spends its actions | **Trace 2** |
| 4 | **Emergency disconnect** (1 AP) | — | session closed before Trace 4; work kept, no stun |

The example is the point of the section: the intruder has a **hard budget of three actions per exchange**, the defender spends from the *same* clock, and the run ends on a decision the player made — disconnect at Trace 2 rather than gamble on Trace 4 — not on a hidden dice roll.
