# Law of One RPG — Phase 1 rules inventory

> **Phase gate:** this is the *inventory* #1124 requires before any implementation. **No Python, no rulebook
> merge, no NoöPunk changes.** Implementation is gated on review of this document.

**Separate artifact, separate namespace.** The Law of One RPG is not a NoöPunk supplement. Nothing here modifies
`rulebook/`, `RULEBOOK.md`, `docs/rules/`, `src/rules/`, the CWN baseline or any existing NoöPunk document. The
repository path proposed for the standalone game is `law_of_one/` at the repo root (rulebook, module and tests
under it); until that is approved, these Phase 1 documents live in `docs/law_of_one/`, which already reads as a
namespace of its own.

**Scope boundary.** The cyberpunk side is deliberately absent. **Cyber is out of scope**: the layers here are
Physical and Astral only. Compatibility, reskinning and integration are later, separately authorised work.

## How every claim in this document is labelled

The repository already has a discipline for this in `docs/research/LAW_OF_ONE_LORE_NOTES.md`; this inventory
keeps it:

- **(A) RA CLAIM** — what the channeled text says, cited `session.question` or a category page.
- **(B) DESIGN READING** — our interpretation for play. Not in the source.
- **(C) NOT SUPPORTED** — a popular gloss or overreach the primary text does not carry. Do **not** implement.

The Ra Material is a channeled esoteric text (Rueckert/Elkins/McCarty, 1981–84). It is the game's fictional
metaphysical source. It is **not** a claim about the real world, and nothing here presents it as fact.

## Sources actually consulted for this pass

| Source | Use |
|---|---|
| [Synopsis](https://www.lawofone.info/synopsis.php) (Wheelock, rev. 2020-02-27) | Every heading inventoried verbatim below |
| [Categories](https://www.lawofone.info/categories.php) | Complete category list used as the omission check |
| [Densities](https://www.lawofone.info/c/Densities) | Density definitions and boundaries |
| [Energy Centers](https://www.lawofone.info/c/Energy+Centers) | Ray structure, activation, blockage |
| [Time/Space](https://www.lawofone.info/c/Time/Space) | Realm distinction and its constraints |
| [Higher Self](https://www.lawofone.info/c/Higher+Self) | Guidance as a mid-sixth-density relationship |
| [Harvest](https://www.lawofone.info/c/Harvest) | Campaign context, not advancement |
| `docs/research/LAW_OF_ONE_LORE_NOTES.md` (#191) | Session-cited prior work, reused rather than redone |

**Not consulted in this pass, and therefore not cited as if I had:** the Glossary and Definitions pages were not
read line by line, nor were the Meditation, Healing, Service to Others, Archetypical Mind, Confederation,
Wanderers and White Magic category pages. `SOURCE_COVERAGE_MAP.md` records that honestly as an explicit gap
rather than filling it with plausible-sounding citations.

---

## 1. Essential playable core

### 1.1 Catalyst, Free Will, Integration

| Field | Content |
|---|---|
| **Source** | Free will as the first distortion / Law of Confusion [13.12, 15.21, 27.8, 27.10, 99.5]; distortion as movement away from unity, in either direction [synopsis] |
| **Faithful meaning (A)** | Free will is the *limit of the viewpoint*: the Creator knows Itself only through a creation free to choose. "Distortion" is **not** a synonym for error or pathology — it is any movement away from undistorted unity, including toward love. |
| **Rules needed?** | **Yes — core.** |
| **Priority** | Essential |
| **Minimal state** | A *catalyst* record (situation, stake, who is affected) and an *integration* record (what the character understood). No score of its own. |
| **Procedure (B)** | Scene produces catalyst → player chooses → consequences are narrated → reflection/integration scene → possibly one Distortion tag is added, transformed or released. |
| **Interactions** | Feeds Polarization (was another-self served or used?) and Awareness (was anything understood?). |
| **Non-goals** | No XP. No "good deed" counter. No automatic reward per scene. **No mechanical penalty for ordinary self-interest or mistakes.** |
| **Open questions** | How often may integration fire without becoming routine? Is integration always player-declared, or GM-declared with a player veto? |

### 1.2 Polarization (0–10, zero → NPC)

| Field | Content |
|---|---|
| **Source** | The two paths [7.15, 19.19]; 51% StO / 95% StS as *third-density graduation* context [17.31, 17.32]; the sinkhole of indifference [17.33]; judging another's polarity is inappropriate [93.3] |
| **Faithful meaning (A)** | Polarity is chosen service: toward others or toward self. Most entities are well along a path before realising they chose. Judging another's polarity is explicitly called inappropriate. |
| **Rules needed?** | **Yes — core.** |
| **Priority** | Essential |
| **Minimal state** | Integer 0–10, start **5** (proposal). One-line rationale recorded per change. |
| **Procedure (B)** | Changes are **rare** — tied to a resolved catalyst arc, not a roll. Informed intent, respect for others' free will and sustained pattern weigh more than the act itself. |
| **Interactions** | Modulated by Awareness (understanding ≠ virtue) and by the energy centers at stake. |
| **Non-goals** | **The 51%/95% figures are not a conversion formula for this 0–10 scale (C).** No StS player track. No clinical reading: depolarisation is not depression, disability or "low empathy". |
| **Open questions** | What restores polarization after a loss, and over what pacing? Does a compassionate act that overrides another's autonomy ever raise it? (Proposed: no, and it should be written down as an example.) |

### 1.3 Awareness (0–10, start 1)

| Field | Content |
|---|---|
| **Source** | Harvest and the veiling [77.17, 79.27]; density as state of evolution vs awareness as how fully it is experienced — the premise Tomi states in `design/LAW_OF_ONE_RPG.md` |
| **Faithful meaning (A)** | Third density is veiled so that seeking arises. Fourth-density awakening is *recognition of what is already the case*, not graduation. |
| **Rules needed?** | **Yes — core.** |
| **Priority** | Essential |
| **Minimal state** | Integer 0–10. Milestone list of perceptual permissions, not powers. |
| **Procedure (B)** | Rises on integrated catalyst and noetic experience; grants **story permissions** (what the character can notice, ask, or endure), not combat or social bonuses. |
| **Interactions** | Independent of Polarization; high Awareness **does not** prevent polarization loss. |
| **Non-goals** | Not a power stat. No generic sanity or trauma subsystem. |
| **Open questions** | Should Awareness be spendable at all, or purely descriptive? (Proposed: purely descriptive.) |

### 1.4 Distortion tags

| Field | Content |
|---|---|
| **Source** | Distortion as any movement from unity, either valence [synopsis]; balancing (category) |
| **Faithful meaning (A)** | A distortion is a *pattern of focus*, not a flaw to be optimised away. |
| **Rules needed?** | **Yes — core, minimal.** |
| **Minimal state** | 0–4 plain-language tags, each with an origin scene. No tree, no ranks. |
| **Procedure (B)** | A tag may make a choice harder or colour how a result is described; it never adds a numeric modifier by itself. |
| **Interactions** | Tags are what integration transforms. |
| **Non-goals** | No sprawling trait list. No mechanical equivalence between a tag and an illness. |
| **Open questions** | Cap of 4 arbitrary? Should tags decay without use? |

### 1.5 Individual SMC Connection vs collective development

| Field | Content |
|---|---|
| **Source** | Social Memory Complex (category); Confederation of Planets (category) |
| **Faithful meaning (A)** | An SMC is a group whose shared memory has become a being in its own right. |
| **Rules needed?** | **Yes — core, and split in two.** |
| **Minimal state** | *Individual*: SMC Connection 0–10, start **0**. *Collective*: one shared group sheet with its own stages. |
| **Procedure (B)** | Connection rises through consensual shared experience. The group sheet advances through 3–5 collective stages with friction, rupture and reconciliation. |
| **Interactions** | A strong individual connection does **not** make someone part of the SMC, and membership is never inferred from telepathy. |
| **Non-goals** | Telepathy, shared memory, membership and consent are **not** interchangeable. |
| **Open questions** | Can two PCs hold different Connection values to the same group without incoherence? (Proposed: yes.) |

### 1.6 Negative-path exit at Polarization 0

| Field | Content |
|---|---|
| **Source** | Two paths and the sinkhole [17.31–17.33, 19.19] |
| **Faithful meaning (A)** | The negative path is a valid cosmic choice made by other beings. |
| **Rules needed?** | **Yes — as an exit, not a track.** |
| **Minimal state** | Zero triggers a documented handoff. |
| **Procedure (B)** | Telegraph the threshold in-fiction and at the table; offer a fair recovery window; then the character passes to GM control as an NPC. |
| **Non-goals** | **No playable StS progression.** No surprise penalties. No moral diagnosis of the player. |
| **Open questions** | Recovery window length, and whether the player keeps narrative input after handoff. |

---

## 2. Fourth-density activities

### 2.1 Seven energy centers as attributes (design investigation)

| Field | Content |
|---|---|
| **Source** | [Energy Centers](https://www.lawofone.info/c/Energy+Centers); violet-ray exception at **15.12** and **39.10** (per #1124) |
| **Faithful meaning (A)** | Seven rays structure the mind/body/spirit complex. Activation ranges from rotating vortices in the lower centers to **crystal structures** as higher centers develop. **Violet ray is described as the total expression/register of the entity** — not balanced or manipulated like the others (15.12, 39.10). |
| **Rules needed?** | **Yes — but investigated, not assumed.** |
| **Priority** | Essential if it survives review |
| **Minimal state (proposal)** | Six trainable rays (red, orange, yellow, green, blue, indigo) with one state each — `open / blocked / strained` — plus a **violet ray that is derived, read-only**, computed from the whole configuration rather than raised. |
| **Procedure (B)** | A blocked ray constrains what a scene offers; balancing through meditation or accepted catalyst can open it. Special permissions (not fifth-density status) unlock at open green/blue/indigo. |
| **Interactions** | Green (love/compassion) and blue (communication) are the load-bearing pair for StO play; blockages there are the best story engine in the system. |
| **Non-goals** | **Seven competing currencies.** Numeric scores per ray are not assumed — a three-state tag is the default candidate precisely to avoid resource management. Violet is **never** spendable. |
| **Open questions** | Are the states enough to express "damage" without implying injury or illness? Does activation need any number at all? |

### 2.2 Prana / psychic energy

| Field | Content |
|---|---|
| **Source** | Energy Centers category; "intelligent energy" vocabulary in the synopsis (Light as third distortion, [13.9, 13.17]) |
| **Faithful meaning (A)** | The texts speak of intelligent energy and of energy centers; **they do not define an RPG-style point pool**. |
| **Rules needed?** | **Optional, and probably unnecessary.** |
| **Minimal state (proposal)** | Prefer the tag approach: `ready / strained / depleted`. A small pool only if playtesting demands it. |
| **Non-goals** | **Do not claim Ra defined a prana pool (C).** No daily regeneration farming, no resource bookkeeping per scene. |
| **Open questions** | Do PSI and White Magic share this energy? The source distinguishes the practices; sharing a pool would flatten that. |

### 2.3 Time/Space and Space/Time

| Field | Content |
|---|---|
| **Source** | [Time/Space](https://www.lawofone.info/c/Time/Space) — **70.14, 70.17, 71.6** (per #1124); 57.33 on the distinction applying mainly in third density |
| **Faithful meaning (A)** | Space/time has a tangible spatial framework; **time/space puts the inequity on time**, rendering entities and experiences intangible "in a relative sense". A lifetime may be seen whole, "as a book or record". The distinction is not a teleport system, and it does not dissolve into a featureless void. |
| **Rules needed?** | **Yes — first class, per the revised scope.** |
| **Minimal state** | A realm flag plus presence state; what the character can perceive and do; a return difficulty. |
| **Procedure (B)** | Entry/exit conditions, duration and correspondence to physical time, interaction rules, review/healing encounters, and what can carry between realms. |
| **Non-goals** | No travel-speed maths, no physics simulation, **no combat system**. Time/Space is **not** identical to density, dimension or "the astral". |
| **Open questions** | How is correspondence between realms tracked without a clock subsystem? |

### 2.4 Astral projection and ectoplasmic manifestation

| Field | Content |
|---|---|
| **Source** | Time/Space category; Glossary links ectoplasm with manifestation of the astral (green-ray) body (per #1124) |
| **Faithful meaning (A)** | The astral body is associated with the green ray; ectoplasm is its manifestation. |
| **Rules needed?** | **Yes — a first-class pillar.** |
| **Minimal state** | `embodied / projected` plus an optional `manifest` state; a link to the physical body and a strain or risk marker. |
| **Procedure (B)** | Projection procedure, astral perception and travel, meeting entities, interaction, manifestation (bounded, costly), and return. Public and institutionalised in-fiction, in the *Summerland* register — a **design premise (B)**, not a Ra claim. |
| **Interactions** | The same realm as Time/Space — **one travel abstraction, not several synonyms.** |
| **Non-goals** | Not every astral event is a fight. **No Cyber layer.** |
| **Open questions** | What happens to the physical body while projected, mechanically? Can another character interfere, and with what consent rules? |

### 2.5 Mind / Body / Spirit Complex

| Field | Content |
|---|---|
| **Source** | "mind/body/spirit complex" throughout (e.g. 17.30's radiating "that which is the essence or the heart of the mind/body/spirit complex"); body complexes in the Energy Centers material |
| **Faithful meaning (A)** | Mind, body and spirit are **aspects of one complex**, not three pools. |
| **Rules needed?** | **Yes — as ontology, not as three tracks.** |
| **Minimal state** | One complex with three aspect descriptors; no separate point pools by default. |
| **Procedure (B)** | Which aspect a scene addresses changes what catalyst it produces. |
| **Non-goals** | Not a clinical health model. Not three character classes. |
| **Open questions** | Tomi's **Luhmann** comparison (psychic / living / social systems) is a design analogy (B), not identity: social systems are relations and communication, which better describes the **SMC** level than the individual "spirit" component. Should the SMC sheet therefore be modelled as a communication system rather than a shared pool? |

### 2.6 Meditation, balancing, healing, teach/learning, non-interference

| Field | Content |
|---|---|
| **Source** | Meditation, Healing, Balancing, Teach/Learning, Service to Others (categories) |
| **Faithful meaning (A)** | Meditation and balancing are reflective practice; healing concerns the whole complex; service is "constant attempt to seek to share the love of the Creator... radiating" [17.30]. |
| **Rules needed?** | **Yes, lightweight.** |
| **Minimal state** | A scene type, not a resource. |
| **Procedure (B)** | Meditation/balancing can open a blocked ray or transform a tag when the player states what is being accepted. Healing is invitation-based: the receiver's autonomy is the gate. |
| **Non-goals** | No medical promises, no hit points, **no guaranteed cure**. |
| **Open questions** | Does teach/learning need mechanics at all, or is it a scene label? |

---

## 3. Optional narrativist tools

| Tool | Source | Proposed treatment |
|---|---|---|
| **Archetypical Mind / tarot** | Archetypical Mind, Tarot categories | Optional prompts and contemplation cards. **Not** a class system, **not** a random-power table. |
| **White Magic** | White Magic category | Compact ritual procedure: intention, preparation, harmony, focus, consequence. Extraordinary effects are GM-adjudicated, never listed as spells. |
| **Wanderer background** | Wanderers category | A tag meaning service mission and forgetting. **No unconditional powers.** |
| **Confederation encounters** | Confederation of Planets category | Consent, non-interference, calls for aid, conflicting readings of "service". |
| **Higher Self** | 70.8, 70.9 — "the entity of mid-sixth density which, turning back, offers this service to its self" | **Narrative relationship only.** Guidance arrives as dream, symbol, synchronicity or atemporal encounter, always interpretable. **Precognition is scripted only** — never player-triggered, never reliable. |
| **Group rites** | White Magic, SMC | Shared intention within the collective sheet. |

---

## 4. Setting principles only — no rules in the first module

These are recorded so nothing is *silently* omitted, and explicitly **not** mechanised:

- **One Infinite Creator / Infinite Intelligence / Intelligent Infinity** [4.20, 28.1, 13.13] — the ontology. **Not a power meter.** No extraordinary contact may treat the Creator as a stat or resource.
- **Illusion** [1.6, 106.23, 27.17] — engineered many-ness. Framing for perception and awakening, not an illusion-spell system.
- **Logos / Sub-Logoi / Sub-Sub-Logoi** [15.21, 27.12, 28.7, 13.13, 29.1, 29.2, 29.7] — nested creation. **No mandatory stats.**
- **Light as third distortion** [15.21, 78.9, 13.9, 13.17] — intelligent energy with an upward spiral. Narrative-only unless a specific fourth-density interaction justifies more.
- **Densities and the octave** [16.51, 28.15, 52.12, 41.16] — see §5.
- **Harvest and cycles** [17.29, 9.4, 40.8, 17.1, 62.29, 63.9] — campaign context.
- **The Veil** [77.17, 79.27] — explains third-density seeking; **not** assumed identical across densities.
- **"Always begin and end in the Creator, not in technique"** [52.11] — a **design constraint**: intention and relationship outrank optimising scores or ritual power. This belongs in the rules text as a principle the procedures must not violate.

## 5. Density handling

**(A)** Seven densities; the eighth is the next octave's first [16.51, 28.15]; the sixth is unity [33.20]; the seventh is completion [41.16]. **(B)** Player characters are **already fourth-density**, newly awakened: fourth density is love/understanding and the game is about *understanding the state they are in*. Density is **not** dimension. Fifth-density progression is outside this game.

---

## 6. What this inventory deliberately does not do

- No dice procedures for cosmological principles. The synopsis concepts in §4 get none.
- No generic RPG mechanics: no attributes, skills, classes, combat, equipment, hacking. Host games own those.
- No StS play, no other-density PCs, no fifth-density advancement, no multi-lifetime levelling.
- No numeric reproduction of the 51%/95% Harvest percentages as a player mechanic.
- No NoöPunk rulebook edits, no CWN changes, no merger.

## 7. Open questions for the reviewer (Tomi)

1. Is the **six-trainable-rays + derived violet** schema the right shape, or should rays stay pure fiction until playtesting demands states?
2. Should **Awareness be purely descriptive** (proposed) or spendable?
3. Does **Time/Space need its own clock/correspondence rule**, or is "one scene there costs one scene here" enough?
4. **Where should the standalone game live** — `law_of_one/` at the repo root, or `src/law_of_one/` plus a separate rulebook directory?
5. Should the **entity catalogue** be completed from sessions before Phase 2, or is the schema plus cited entries enough to start?

## See also

- `docs/law_of_one/SOURCE_COVERAGE_MAP.md` — every synopsis heading and category, with disposition and omissions stated.
- `docs/law_of_one/ENTITY_CATALOGUE.md` — source-cited names, with the not-yet-enumerated gap recorded.
- `design/LAW_OF_ONE_RPG.md` — Tomi's design premise (three scores, apocalypse-vs-awakening, campaign arc). This inventory is the source discipline underneath that design and does not replace it.
- `docs/research/LAW_OF_ONE_LORE_NOTES.md` (#191) — session-cited lore sheet, reused here.
- Related issues: #179, #191, #1044, #1007.
