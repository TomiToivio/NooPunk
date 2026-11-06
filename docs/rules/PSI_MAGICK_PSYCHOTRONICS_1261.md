# PSI, Magick and Psychotronics: author approval draft (#1261)

> **Status: DESIGN ONLY, awaiting Tomi's approval.** This document addresses the expanded PSI/Magick/device work in #1261 without silently installing new skills, prices, damage rules, Effort pools or abilities. The immutable Cities Without Number (CWN) core remains unchanged. NoöPunk quantum-consciousness mechanics are **fictional setting technology**, not established physics or medicine.
>
> **Precedence:** the newest author superskill specification and `docs/rules/ASTRAL_SUPERSKILL_1261.md` override earlier incompatible Astral Projection ladders. Only ranks 0–1 are playable; ranks 2–4 remain design-only.

## 1. Existing implementation versus proposed expansion

| Feature | Existing source / confirmed status | Next step |
| --- | --- | --- |
| Astral Body, single actor/body, scripted projection, perception, astral targeting | `src/rules/astral_body.py`; tested in `tests/test_issue_1261_astral_body.py` | Reuse, do not duplicate |
| Astral location graph and relationship semantics | `src/rules/astral.py` and `tests/test_astral_graph_1261.py` | Astral location nodes, conscious agents as occupants |
| Astral superskill levels 0–4 and 0–1 MVP gate | `src/rules/astral_progression.py`, `data/rules/astral_progression_1261.json` | Preserve access boundaries |
| Two illustrative projection scenes | `tests/test_astral_two_scenes_1261.py` | These are tests, not approved campaign prose |
| Astral damage to CWN HP | `apply_astral_damage` **deliberately raises**; not approved | Author selects damage bridge |
| SWN psychic techniques targeting Astral Bodies | Not whitelisted in the Astral Body contract | Verify technique by technique against the licensed source |
| Rookie AntiPSI-0 + ESP-0 implant, heavy fields, BCI bridge, projection tank | **Proposals in #1261**, not verified as existing executable systems in this audit | Approve equipment contracts, then inspect catalog and implement only missing items |
| Native Astral Projection, ESP, Electrokinesis skill expansions | Proposed, not authorized as universally selectable disciplines | Choose PC-access option A or B first |
| CWN Spellcaster/Summoner and SWN Psychic overlap | Compatibility is requested, not an authorization to share mechanics | Use separate resources and explicit source references |

**Source classification:** Existing code above is implemented behavior. The abilities/equipment below are *NoöPunk proposals*. Analogies to Psi-punk and Shadowrun are design inspiration, **not transplanted rules**. Published SWN/CWN effects must be checked directly before any technique whitelist or rule implementation.

## 2. Recommended character creation gate: Option A

Recommend **A, incremental and device-first**, subject to Tomi's explicit decision. A Europol rookie who is not Psychic may use **two device-supplied level-0 effects** from their standard implant, but this is **equipment permission**, not a trained SWN skill rank or entitlement to higher techniques. This avoids changing the existing PC discipline restriction in #1178 by accident.

- **AntiPSI-0 (equipment):** a limited local warning/protective response to specified PSI intrusion. It does not make the wearer immune to Telepathy, does not grant Metapsionics progression and does not generate Psychic Effort.
- **ESP-0 (equipment):** a bounded, scene-scoped anomalous signature cue. It can prompt Notice/Know/Program or an investigative scene; it is not thought-reading, a suspect identity, a recording of objective afterlife evidence or remote surveillance.
- **Electrokinesis:** initial access only through a specific authored device, authorized Focus/Edge, or later approved native skill; electronic disruption never grants network credentials.
- **Astral Projection:** keep scripted events and psychotronic facilities as initial entry options alongside the already defined rank-0/1 Astral-domain superskill. Do not confuse an equipment-enabled projection with a free SWN Psychic class or a higher rank.
- **Option B (deferred):** admitting ESP, Electrokinesis and Astral Projection as new native selectable SWN-style disciplines requires a separate complete specification for prerequisites, training, 0–4 techniques, actions, Effort, target eligibility, range, saves, limits and balance tests. AntiPSI should remain a Metapsionics-derived interpretation, not a redundant new discipline.

**Decision A1:** Approve Option A or B. Until then the document adds **zero new character choices**.

## 3. SWN-style technique design cards (not executable grants)

Every proposed technique must use this template before implementation:

```text
Name:
Source: published SWN / NoöPunk homebrew / equipment effect
Discipline and minimum skill rank (or equipment permission):
Prerequisites and class/Focus eligibility:
Action and timing:
Range, target category and target cap:
Duration and termination:
Effort commitment / device capacity / recharge:
Resisted save, ward, AntiPSI and counterplay:
Legal/Europol permissions and forensic trace:
Applicable Physical / Astral / Cyber targets:
Explicit forbidden outcomes:
Tests for denial, interruption, repeat use and cross-domain abuse:
```

**Proposed level concepts, not approved abilities:**

| Discipline | Level 0 | Level 1 | Levels 2–4 (design-only) |
| --- | --- | --- | --- |
| AntiPSI / Metapsionics-linked | local intrusion cue or defensive ward | bounded active counter | progressively stronger *specific* interference/resistance, preserving published SWN Metapsionics and Psychic Static/Refinement semantics |
| ESP | nearby anomaly/astral-presence clue | focused concealed-presence sensing | anchored scrying, tracked signatures, rare deep information observations, never omniscience |
| Electrokinesis | sense nearby powered electronics | brief, limited simple circuit interaction | targeted device disruption, specifically guarded BCI/electronics operations, rare capped QIP hardware effects; never a Program bypass |
| Astral Projection | Near Astral, awkward embodied-interface interpretation | lucid flight, Lower Astral and constructed dreams | rank 2 ROTE/Learn Ident; rank 3 Use Ident/authorized editing; rank 4 higher planes and cosmological research (follow existing superskill document) |

The Astral Projection superskill table is **authoritative**, not this summary. It does not grant extra Physical/Cyber powers. Level-2/3/4 techniques are **inaccessible in the MVP**, even if a gate can describe them.

## 4. Device catalogue proposals and explicit constraints

Every item needs a canonical CWN-compatible equipment record with availability, cost, installation/removal, optional System Strain, maintenance, authorization, lawful use, failure conditions, audit trail and source classification. **Do not assign numerical prices, Strain or Effort until approved.**

| Candidate | Scene-level permission | Must never silently grant |
| --- | --- | --- |
| **Europol rookie psychotronic implant** | AntiPSI-0 local alert/limited defensive ward; ESP-0 anomaly clue, calibrated/activated by an authorized operator | Psychic class, permanent discipline ranks, unlimited Effort, perfect detection |
| **Protective AntiPSI implant** | device-specific ward against named telepathic/astral intrusions, failure and bypass possible | invulnerability to all PSI |
| **Heavy AntiPSI area field** | installed/vehicle/facility ward, defined radius, startup, interference with friendly PSI, power and alarm state | planet-scale suppression or indiscriminate psychic immunity |
| **AntiPSI BCI/cyber security hardware** | psi filter on a protected neural/cyber interface; separate from conventional auth/encryption | root login, decryption or remote consciousness access |
| **Astral Projection Tank** | authorized session trigger with sensory isolation, BCI telemetry, two-way *device-mediated* conversation, body monitoring, life support, operator interruption and optional authored mode transition | free permanent rank increases, guaranteed return, arbitrary afterlife contact |
| **Forensic PSI sensor/recorder** | logs device measurements and uncertain signals for a case | objective proof of identities or narrative events experienced astrally |

The tank's **DMT infusion** is strictly fictional lore. There are **no real-world doses, administration instructions or claims that DMT causes projection**.

**Capacity decision D1:** device-specific finite charges/capacity (recommended), published equipment resource or approved shared Psychic Effort? Non-Psychic users **must not** receive a fabricated infinite Effort pool. Each item should fail closed on inactive, uncalibrated, unauthorized, depleted, tampered or disconnected state.

## 5. PSI ⇄ Magick ⇄ Cyber compatibility (no mechanical equivalence by default)

| Intent | Primary rules authority | Narratively related possibility | Hard boundary |
| --- | --- | --- | --- |
| Unarmed astral-body strike | CWN Punch, existing Astral targeting gate | SWN PSI may be attempted only if a published/approved technique targets that entity | No new Astral Combat skill; astral→body injury bridge unapproved |
| Mind-to-mind contact or influence | Published SWN Telepathy (when applicable) | CWN Spellcaster/Summoner may have a similarly described ritual after separate spell verification | No free conversion of spellcasting into Psychic Effort |
| AntiPSI ward/counter | SWN Metapsionics where published; otherwise explicit device/homebrew effect | Magical ward after separate spell verification | Not blanket immunity; no duplicated Psychic Static |
| Astral sensing | Device ESP-0 proposal / approved psychic ability | Assensing-style narrative clues | Not verified physical sight or evidence |
| Astral projection | `astral_body.py` and superskill progression; approved tank scene | Homebrew ritual only if Tomi authorizes an explicit spell/ritual | Not a free Spellcaster class feature |
| Program / BCI software intrusion | CWN Program, hacking actions, alarms and credentials | Electrokinesis may affect hardware via an explicit power | A hardware signal is not root access or a downloaded memory |
| Spirit encounter | Authored Astral/Story Scene | Summoner-like ritual where an actually applicable spell is verified | No compulsory dead-person contact or identity proof |

**PSI** is primary NoöPunk terminology; **Magick** is an in-world interpretation. Their fictional ontology can overlap without merging classes, dice, spells, Psychic Effort or action economies.

## 6. Three distinct intrusion lanes: playable case exercise

**A. Human / social:** A Europol investigator obtains permission to interview a lab technician using CWN Talk, Connect or Administer. The technician's statements and approvals go to the *case record*, not a psychic truth oracle.

**B. Cyber / BCI:** A specific device becomes a target through an already-authorized CWN Program action; log credentials, alarms, access time and technical evidence. A successful hack controls only **functions the device actually exposes**. Brain memories do not become digital files by default.

**C. PSI / Astral:** A named, approved Telepathy, AntiPSI, ESP or projected-Astral effect may reveal a *lead*, with ward/resistance, consent and jurisdiction constraints. A separate psychic bridge is required to affect an agent through a BCI, even if its software was compromised. A disrupted neural interface need not mean a penetrated mind.

**Exercise outcome:** GM reveals a corrupted sensor log and two inconsistent witness accounts; the PC must corroborate physical and cyber observations before alleging a culprit. Keep four separate data types: (1) admissible forensic artifacts, (2) device telemetry, (3) fallible PSI observations, and (4) GM-only cause. No lane may automatically override another.

## 7. Acceptance tests to add *after authorization*

1. A **non-Psychic** rookie can trigger exactly the allowed implant level-0 effects, cannot select skill 1 or spend unearned Psychic Effort, and cannot use a depleted/disabled implant.
2. A hostile actor can attempt a *named* ward-resisted power; defense and countermeasure failure are observable, never automatic immunity.
3. Astral Projection rank 0 does not fly or enter Lower Astral; rank 1 does; neither receives ROTE, Ident jump or higher planes.
4. Astral unarmed targeting uses the existing contract and CWN Punch; physical shots cannot harm an intangible apparition; Time/Space does not expose Physical objects.
5. A Cyber compromise does not imply PSI access, a PSI hardware disturbance does not grant Program privileges, and no memory download is inferred.
6. Device data/PSI impressions are **not** converted into admissible proof without a separate corroboration process.
7. Psychotronic tank operator interruption, monitoring, access denial, loss of signal and safe-return policy are deterministic.
8. Published SWN spells/techniques only appear in a whitelist if the exact source's targeting, limits and Effort text was checked; verify no regression to CWN core.

## 8. Outstanding author decisions

- **A1:** incremental device-first PC access (A) or full native selectable disciplines (B)?
- **D1:** finite device capacity versus approved shared Effort mechanism?
- **D2:** any numeric implant price, Strain, service interval or tank operation costs?
- **A2:** Astral injury result: shared CWN HP, temporary condition, forced return, coma, or another explicit bridge?
- **A3:** which *published* SWN Telepathy/Telekinesis/Metapsionics techniques may target Astral Bodies? Verify each before implementing.
- **A4:** manifestation channels; dead-contact repeatability and cost; Ident consent and AntiPSI logging?
- **A5:** projection durations, projection Effort mode, rank-1 Time/Space scope, rank-3 editing ownership and audit?
- **A6:** who may activate Europol AntiPSI fields and tanks, and what are their legal and practical constraints?

Do not close #1261 until author decisions are recorded and the approved subset passes tests, tabletop/code parity review, and the existing CWN constitution audit.
