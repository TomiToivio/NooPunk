# Law of One RPG — rules inventory (issue #1124, Phase 1)

**Status: inventory only.** No rule below is implemented, and none may be until the inventory is
reviewed. This file is generated from `data/law_of_one/rules_inventory.json` by
`tools/law_of_one_inventory_audit.py`; edit the data, not the table.

Every row separates **what the source says** (`Faithful meaning`) from **what the game would do**
(`Minimal procedure`). The first is a claim about the Ra material and carries session citations; the
second is ours, and is a proposal for playtest, not a claim that Ra wrote a rule.

**49 concepts inventoried** — core **23**, optional **13**, narrative_only **10**, out_of_scope **3**.

| priority | meaning |
|---|---|
| `core` | needed for the first playable version |
| `optional` | useful, bounded, can ship later or not at all |
| `narrative_only` | world understanding the game needs but must not mechanise |
| `out_of_scope` | explicitly excluded from this rules module, with a reason |

## Conventions the inventory holds itself to

* **density vs dimension** — Density is an evolutionary stage of the mind/body/spirit complex; dimension is a realm. Never interchangeable.
* **proposed vs source** — Every row's `faithful_meaning` is the source claim; every `minimal_procedure` is ours. The two must never be merged in play-testing reports.
* **scores are proposals** — 0-10 scales and starting values are design proposals for playtest, not Ra numbers.
* **no host rules** — This module defines no attributes, skills, hit points, combat or equipment; those belong to a host game.

## Coverage map summary

| source concept | rows |
|---|---|
| The One Infinite Creator / Intelligent Infinity / Infinite Intelligence (synopsis_heading) | `one-infinite-creator` |
| Illusion (synopsis_heading) | `illusion` |
| Distortion (synopsis_heading) | `distortion-tags` |
| Free Will / First Distortion / Law of Confusion (synopsis_heading) | `free-will-non-interference` |
| Love / Logos / Second Distortion (synopsis_heading) | `logos-second-distortion` |
| Light / Third Distortion (synopsis_heading) | `light-third-distortion` |
| Logos, Sub-Logoi, Sub-sub-Logoi (synopsis_heading) | `sub-logoi`, `logos-second-distortion` |
| Densities (all seven, octave/eighth) (synopsis_heading) | `densities-seven`, `density-four-profile` |
| Two Paths / Positive and Negative Polarization / Sinkhole of Indifference (synopsis_heading) | `two-paths-cosmology`, `polarization-positive`, `depolarization-and-npc-handoff`, `negative-path-as-npc` |
| Third-density percentages (51% StO / 95% StS) (synopsis_heading) | `third-density-percentages` |
| Harvest / cycles / graduation / planetary transition (synopsis_heading) | `harvest-context` |
| How to be of Service to Others (synopsis_heading) | `service-dilemmas` |
| Veil / Veiling of Mind / forgetting and seeking (synopsis_heading) | `veiling-cosmology`, `veil-and-forgetting` |
| Practical advice: begin and end in the Creator, not in technique (synopsis_heading) | `practical-advice` |
| Higher Self (topic_page) | `higher-self-scripted`, `precognition-scripted` |
| Meditation (topic_page) | `meditation` |
| Service to Others (topic_page) | `service-dilemmas`, `free-will-non-interference`, `polarization-positive` |
| Harvest (topic_page) | `harvest-context`, `violet-ray-register` |
| Healing (topic_page) | `healing-invitation`, `ectoplasm-manifestation` |
| Energy Centers (topic_page) | `energy-centres-seven`, `violet-ray-register`, `blockage-and-restoration` |
| Archetypical Mind (topic_page) | `archetypal-contemplation`, `teach-learning` |
| Confederation of Planets (topic_page) | `confederation-contact`, `smc-collective`, `entity-catalogue` |
| Densities (topic_page) | `densities-seven`, `density-four-profile`, `awareness-scale` |
| Wanderers (topic_page) | `wanderer-background`, `veil-and-forgetting` |
| White Magic (topic_page) | `white-magic-ritual`, `group-rite` |
| Time/Space (topic_page) | `time-space-presence`, `astral-projection` |
| Catalyst (topic_page) | `catalyst-loop`, `integration-reflection` |
| Balancing (topic_page) | `balancing-practice`, `blockage-and-restoration`, `score-change-pacing` |
| Positive Path (topic_page) | `polarization-positive` |
| Negative Path (topic_page) | `negative-path-as-npc`, `depolarization-and-npc-handoff` |
| The Two Paths (topic_page) | `two-paths-cosmology` |
| Teach/Learning (topic_page) | `teach-learning` |
| A. Seven Energy Centers as attributes (added_priority) | `energy-centres-seven`, `violet-ray-register`, `blockage-and-restoration` |
| B. Time/Space and Space/Time as rules (added_priority) | `time-space-presence` |
| C. Astral projection and ectoplasm (added_priority) | `astral-projection`, `ectoplasm-manifestation` |
| D. Mind/Body/Spirit Complex (added_priority) | `mind-body-spirit-complex` |
| E. Prana / psychic energy (added_priority) | `prana-energy` |
| F. Veil, Higher Self, Wanderers as bounded memory mechanics (added_priority) | `veil-and-forgetting`, `wanderer-background`, `higher-self-scripted` |
| G. SMC individual and group mechanics (added_priority) | `smc-connection-individual`, `smc-collective` |
| H. Catalogue of species, civilizations and entities (added_priority) | `entity-catalogue` |
| Fourth-density visibility and manifestation to third density (12.17) (cosmology_clarification) | `visibility-manifestation` |
| Density is not dimension / not four-dimensional space (21.5, 6.24, 17.1) (cosmology_clarification) | `density-not-dimension`, `density-four-profile` |
| Astral planes and subtle bodies are not the whole of Time/Space (43.7, 47.8) (cosmology_clarification) | `inner-planes-and-bodies`, `astral-projection`, `time-space-presence` |
| Fourth density is embodied physical life, not a ghost or astral state (43.16, 43.12) (cosmology_clarification) | `density-four-profile` |
| Embodied by default; projection, manifestation and the disincarnate state (cosmology_clarification) | `embodiment-modes`, `astral-projection`, `visibility-manifestation` |
| Which cited passages were read, which paraphrased, which unread or ambiguous (cosmology_clarification) | `density-not-dimension`, `visibility-manifestation`, `embodiment-modes`, `inner-planes-and-bodies` |

## 1. Essential playable core

### `density-four-profile` — Fourth-density character profile

* **Priority:** `core` · **rules needed:** yes · **page:** https://www.lawofone.info/synopsis.php
* **Source:** 12.17, 13.21, 17.1, 20.36, 21.5, 43.11, 43.12, 43.16, 6.24, synopsis: Densities
* **Faithful meaning (source claim):** Fourth density is the density of love or understanding; its inhabitants come together with others of like mind in a social memory complex (43.11). Density is an evolutionary stage of the mind/body/spirit complex, described by Ra in terms of vibrational conditions and spectrum (17.1) — not a place, not a dimension, and not an astral state: fourth-density beings live embodied physical lives (43.16). Fourth-density entities are, by choice, ordinarily invisible to third density and can manifest visibly, though holding third-density vibrational visibility takes effort (12.17). Ra also uses 'dimension' in metaphysical senses (21.5, 6.24); that is not a fourth geometrical coordinate. Verified verbatim: the fourth-density physical vehicle uses different chemical elements though the appearance is similar (43.16); fourth-density beings eat, as “a simple precondition of the space/time experience” rather than significant catalyst (43.17); and fourth density includes multiple incarnations with time/space experiences between them (43.12).
* **Minimal procedure / treatment (ours):** A character sheet carries: density (fixed at 4 for PCs), Polarization 0-10 (start 5), Awareness 0-10 (start 1), SMC Connection 0-10 (start 0), Distortion tags, a Catalyst log, and seven energy-centre states. Density never rises during normal play.
* **State fragment:** `character: {density: 4, embodiment: embodied|projected|manifesting|disincarnate, visibility_to_third_density: concealed|perceptible|manifest, polarization: int 0..10, awareness: int 0..10, smc_connection: int 0..10, tags: [str], catalyst_log: [...], centers: {red..indigo: {...}}, violet: {register_only: true}}`
* **Interactions:** Polarization gates the NPC handoff; Awareness gates perception permissions; SMC Connection gates collective scenes; centres gate optional abilities.
* **Non-goals:** No fifth-density progression, no multi-lifetime levelling, no density-as-dimension and no density-as-geometry (fourth density is NOT four-dimensional space), no free invisibility, no unlimited manifestation, no XP.
* **Open question:** Are three 0-10 scores legible at a table, or should Awareness be a milestone list? And should embodiment and visibility be tags rather than enumerated states?

### `catalyst-loop` — Catalyst, free choice, consequence, integration

* **Priority:** `core` · **rules needed:** yes · **page:** https://www.lawofone.info/c/Balancing
* **Source:** glossary: Catalyst, 15.12, 40.10, synopsis: Distortion
* **Faithful meaning (source claim):** Catalyst is 'an agent that provokes change or action'. Ra describes balancing as using experience to the utmost and then applying the balancing exercises, with the key being the 'unstudied, spontaneous, and honest response' to experience.
* **Minimal procedure / treatment (ours):** Scene procedure: (1) the Catalyst is named and its stakes stated; (2) the player chooses freely, and the choice is recorded; (3) consequences are narrated; (4) an optional reflection beat asks what was learned and what distortion it touched; (5) only then may a tag or score change, by table agreement.
* **State fragment:** `catalyst_entry: {scene, catalyst, stake, choice, consequence, reflected: bool, changed: [tag|score]}`
* **Interactions:** Integration writes into polarity/awareness/tags; the free-will rule constrains what another character may do to a PC.
* **Non-goals:** No XP for good deeds, no morality farming, no score change on every roll, no random morality dice.
* **Open question:** Should reflection be mandatory or opt-in when a scene was decisive?

### `free-will-non-interference` — Free Will / the Law of Confusion (first distortion)

* **Priority:** `core` · **rules needed:** yes · **page:** https://www.lawofone.info/c/Service+to+Others
* **Source:** 13.12, 15.21, 27.10, 99.5, 70.11, Service to Others category
* **Faithful meaning (source claim):** The first distortion is free will, also called the Law of Confusion. Ra is explicit that the Higher Self does not manipulate its past selves: 'it protects when possible and guides when asked, but the force of free will is paramount'. A working that abridges another's free will loses its magical nature (the evangelist example).
* **Minimal procedure / treatment (ours):** A standing table rule: no character, NPC or mechanic may decide another character's action, belief or feeling. Aid must be offered and accepted; a refused offer is a complete answer. The GM may present consequences but must not narrate a PC's choice.
* **State fragment:** `no new state; a table-rule flag on every social mechanic`
* **Interactions:** Bounds healing, SMC sharing, White Magic, Confederation contact, Higher Self guidance and every score change.
* **Non-goals:** Not a dice modifier, not a 'consent stat', not a licence to ignore consequences.
* **Open question:** How does the rule handle a player asking to be influenced — is prior consent enough?

### `integration-reflection` — Integration of catalyst

* **Priority:** `core` · **rules needed:** yes · **page:** https://www.lawofone.info/c/Balancing
* **Source:** 15.12, 40.10, synopsis: How to be of Service to Others
* **Faithful meaning (source claim):** Ra's balancing is retrospective: experience is used to the utmost and then balanced, and the violet-ray register is what an entity's totality looks like when it holds together.
* **Minimal procedure / treatment (ours):** Between scenes, or at session end, a player may take an Integration beat: name the catalyst, name the distortion it exposed, and either accept it (tag stays) or work it (tag may soften). Only an Integration beat can move a score, and only by one step.
* **State fragment:** `integration: {session, catalyst_ref, distortion, accepted: bool, score_delta: {polarization|awareness|smc_connection: -1..+1}}`
* **Interactions:** The only writer to Polarization/Awareness except the depolarization track.
* **Non-goals:** Not a journaling requirement; not a therapy exercise; not a reward for good prose.
* **Open question:** Should the GM or the table ratify a score change, or the player alone?

### `polarization-positive` — Positive polarization (Service to Others)

* **Priority:** `core` · **rules needed:** yes · **page:** https://www.lawofone.info/c/Positive+Path
* **Source:** 17.30, 17.31, 17.32, 17.33, 19.16, 93.3, synopsis: The Two Paths
* **Faithful meaning (source claim):** Third density is where a path is chosen; at least 51% service to others suffices for the positive path, 95% self-service for the negative, and between them lies the sinkhole of indifference. Ra also says it is impossible and inappropriate to judge another being's polarity.
* **Minimal procedure / treatment (ours):** Polarization 0-10 measures sustained StO orientation for the PC only. It rises through Integration beats when the choice was costly, informed and respectful of others' freedom; it does not rise from declared good intentions or from a single act.
* **State fragment:** `polarization: int 0..10 (start 5), with a short reasons log`
* **Interactions:** Feeds the negative-path handoff; never feeds a dice bonus.
* **Non-goals:** Do not convert 51%/95% into a 0-10 formula; do not score NPCs' polarity; do not equate low polarization with mental illness.
* **Open question:** Is 5 the right start for a newly awakened being, or should it be 3 to leave room to grow?

### `depolarization-and-npc-handoff` — Depolarization, warnings and the zero threshold

* **Priority:** `core` · **rules needed:** yes · **page:** https://www.lawofone.info/c/Negative+Path
* **Source:** 17.33, 19.19, issue #1124 (game abstraction)
* **Faithful meaning (source claim):** The 'sinkhole of indifference' names the region between the paths where an entity has not chosen. The 0-10 scale, the zero threshold and the NPC handoff are game abstractions, not numeric claims from the text.
* **Minimal procedure / treatment (ours):** Three telegraphed stages: at 1-2 the GM must show a visible warning beat; at 1 the table holds a short review and the player may spend an Integration beat to recover; at 0 the character leaves PC control and becomes an NPC. The player keeps the right to retire the character instead.
* **State fragment:** `polarization, warning_stage: none|watch|review, handoff: {at, to_npc: bool}`
* **Interactions:** Any mechanic that can spend polarization must route through this ladder.
* **Non-goals:** Not a surprise penalty, not a hidden track, not a mental-health state, not permadeath.
* **Open question:** Should the review at 1 be automatic or opt-in by the player?

### `distortion-tags` — Distortion tags

* **Priority:** `core` · **rules needed:** yes · **page:** https://www.lawofone.info/c/Balancing
* **Source:** glossary: Distortion, 15.9, 15.12
* **Faithful meaning (source claim):** In Ra's terms a distortion is anything that moves away from undistorted unity, and can be toward love or toward ill health; 'distortion' does not mean bad or pathological.
* **Minimal procedure / treatment (ours):** A character holds 3-6 plain-language tags (fear, attachment, humility, need for control, grief...). A tag is descriptive: it informs how the GM frames catalyst and may be invoked by either side for fictional positioning, never as a flat bonus.
* **State fragment:** `tags: [{name, note, since}], max 6; no numeric rating`
* **Interactions:** Catalyst names a tag; Integration may soften or resolve one; centres may explain a tag.
* **Non-goals:** No sprawling skill tree, no tag-shopping, no tag that silently adds dice.
* **Open question:** Is a tag rating (light/strong) worth the bookkeeping?

### `awareness-scale` — Fourth-density Awareness

* **Priority:** `core` · **rules needed:** yes · **page:** https://www.lawofone.info/c/Densities
* **Source:** 77.17, 79.27, 12.28, 12.30, synopsis: The Veil
* **Faithful meaning (source claim):** The veil separates conscious and subconscious mind in third density; fourth-density experience begins with an added awareness that third density cannot remember. Wanderers in particular carry forgetting and often a sense of alienation.
* **Minimal procedure / treatment (ours):** Awareness 0-10 is recognition of a consciousness already present, not a power stat. Each band grants narrative permissions: 1-3 notice synchronicity; 4-6 perceive energy-centre states in others by invitation; 7-9 enter Time/Space deliberately; 10 opens the gateway to intelligent infinity, once, as a story climax.
* **State fragment:** `awareness: int 0..10 + milestone list`
* **Interactions:** Gates Time/Space and astral entry; never grants polarization and never prevents its loss.
* **Non-goals:** Not a sanity score, not a power level, not a replacement for consent, no precognition.
* **Open question:** Should high Awareness ever *raise* the cost of a choice, to keep it from being strictly good?

### `smc-connection-individual` — Individual SMC Connection

* **Priority:** `core` · **rules needed:** yes · **page:** https://www.lawofone.info/c/Confederation+of+Planets
* **Source:** 20.36, 48.6, Confederation of Planets category
* **Faithful meaning (source claim):** Fourth-density entities of like mind come together in a social memory complex; the Confederation describes its members as having each voluntarily placed their data in a central thought complex available to all.
* **Minimal procedure / treatment (ours):** SMC Connection 0-10 measures one character's participation: 0 none, 1-3 receptive, 4-6 contributing, 7-9 co-resonant, 10 fully in the complex. Joining, sharing and leaving are explicit player choices, scene by scene, and leave a record.
* **State fragment:** `smc_connection: int 0..10, consents: {share_emotion, share_memory, coordinate_action, share_location}`
* **Interactions:** Feeds the collective sheet; telepathy is not membership, and membership is not consent to any given act.
* **Non-goals:** Do not equate Connection with telepathy, loyalty, or group membership; no automatic mind-reading.
* **Open question:** Is per-channel consent (emotion/memory/action) too fine-grained for play?

### `smc-collective` — Collective SMC development (group sheet)

* **Priority:** `core` · **rules needed:** yes · **page:** https://www.lawofone.info/c/Confederation+of+Planets
* **Source:** 20.36, 48.6, Confederation of Planets category
* **Faithful meaning (source claim):** A social memory complex is a group that shares a single memory and identity without erasing its members; Ra describes the Confederation forming exactly this way, voluntarily.
* **Minimal procedure / treatment (ours):** A one-page group sheet: shared purpose, shared memory (facts the group holds as one), trust 0-5, boundaries list, and 4 stages — Gathering, Resonating, Remembering, One Voice. Rupture and reconciliation are explicit procedures, and any member may withdraw without losing their own connection score.
* **State fragment:** `smc_sheet: {name, purpose, members[], trust 0-5, shared_memory[], boundaries[], stage 0..3, ruptures[]}`
* **Interactions:** Distinct from individual Connection; feeds scenario outcomes, never replaces a character's own state.
* **Non-goals:** No assimilation, no hive-mind override of a PC, no collective score that can spend an individual's polarization.
* **Open question:** Can a group lose its stage? What does a failed One Voice attempt do?

### `negative-path-as-npc` — The negative path is not a PC track

* **Priority:** `core` · **rules needed:** yes · **page:** https://www.lawofone.info/c/Negative+Path
* **Source:** 19.19, 7.15, 93.3
* **Faithful meaning (source claim):** The two poles of consciousness are service to others and service to self; Ra says judging another's polarity is neither possible nor appropriate.
* **Minimal procedure / treatment (ours):** StS characters exist as GM-run NPCs with stated intentions. They are never modelled with a mirror score, and their actions are not scored by the game.
* **State fragment:** `npc: {intent, methods, leverage} only`
* **Interactions:** Provides antagonists, temptation and catalyst without tactical combat rules.
* **Non-goals:** No mirror StS progression track, no 'evil points', no equating StS with illness or disability.
* **Open question:** How much StS screen time does a positive-path campaign need before it stops being one?

### `score-change-pacing` — When a score may change

* **Priority:** `core` · **rules needed:** yes · **page:** https://www.lawofone.info/c/Balancing
* **Source:** 40.10, 15.12, issue #1124 §2
* **Faithful meaning (source claim):** Ra's emphasis is on sustained pattern and honest response rather than on discrete tallies of acts; balancing is a practice, not a transaction.
* **Minimal procedure / treatment (ours):** One step per scene at most; the reasons are written down; a player may contest a change and the table decides; no mechanic may force a change without a preceding warning beat.
* **State fragment:** `score_log: [{scene, score, delta, reason, contested: bool}]`
* **Interactions:** Applies to Polarization, Awareness and SMC Connection alike.
* **Non-goals:** No automatic change from a roll, no change to punish a rules question, no hidden adjustments.
* **Open question:** Who ratifies: GM, table, or player-with-notice?

### `visibility-manifestation` — Fourth-density visibility and manifestation to third density

* **Priority:** `core` · **rules needed:** yes · **page:** https://www.lawofone.info/c/Densities
* **Source:** 12.17, 17.1, 43.16
* **Faithful meaning (source claim):** Ra, 12.17 (checked verbatim): “The fourth density is, by choice, not visible to third density. It is possible for fourth density to be visible. However, it is not the choice of the fourth-density entity to be visible due to the necessity for concentration upon a rather difficult vibrational complex which is the third density you experience.” Note what this is and is not: invisibility is a choice, visibility is possible, and the cost is concentration on a third-density vibrational complex — not a claim that fourth density is a separate spatial dimension. Ra adds (12.18) that no Confederation or Orion entities are currently walking among humans, and that Orion works through thought-forms and constructs.
* **Minimal procedure / treatment (ours):** Three states, no numbers: concealed (the default), perceptible (third-density observers can sense something without full form), manifest (fully visible, chosen, and costly to sustain). Moving to a visible state is a deliberate act with a cost or condition the GM states before the roll; dropping back is free. Ordinary play never requires visibility, and scenes that do are exceptional.
* **State fragment:** `character.visibility_to_third_density: concealed|perceptible|manifest (+ optional source_scene reference)`
* **Interactions:** Scene-level perceptibility for NPCs and cameras; interacts with astral manifestation and with any scene about being seen; never grants an attack or movement advantage.
* **Non-goals:** No free invisibility, no unlimited manifestation, no extra-dimension movement, no stealth subsystem, no combat use.
* **Open question:** Is a three-state tag better than a number? Should manifestation cost prana, a centre condition, or only narrative effort?


## 2. Fourth-density activities

### `energy-centres-seven` — The seven energy centres as character state

* **Priority:** `core` · **rules needed:** yes · **page:** https://www.lawofone.info/c/Energy+Centers
* **Source:** 15.9, 15.12, 38.5, 41.x (rotational speed and violet imbalance), glossary: Malkuth, solar plexus
* **Faithful meaning (source claim):** Ra describes the mind/body/spirit complex as a web of energy centres: red (Malkuth/earth), orange (emotional/self), yellow (ego/solar plexus), green (heart/universal love), blue (communication), indigo (pineal). Each may be blocked, and balancing is the work of understanding and accepting them. In a balanced entity 'each energy center is balanced and functioning brightly and fully'.
* **Minimal procedure / treatment (ours):** Six usable centres (red, orange, yellow, green, blue, indigo), each a single state word — blocked / strained / open / bright — rather than a number, to avoid seven currencies. A centre is described in one line of fiction; only green (love/compassion) and blue (communication) may grant a bounded permission when bright.
* **State fragment:** `centres: {red|orange|yellow|green|blue|indigo: 'blocked'|'strained'|'open'|'bright'}`
* **Interactions:** Explains and can soften a Distortion tag; bright indigo gates Time/Space entry; bright green gates healing and ectoplasm.
* **Non-goals:** Do not make centres numeric pools; do not let centre states grant density; do not model blockage as illness.
* **Open question:** Is a four-state word enough, or does play want a 0-3 number that maps 1:1 to the words?

### `violet-ray-register` — Violet ray: a register, not a trainable stat

* **Priority:** `core` · **rules needed:** yes · **page:** https://www.lawofone.info/c/Energy+Centers
* **Source:** 38.5, 40.x (brilliance not considered above violet-ray balance), Harvest category (violet-ray emanation)
* **Faithful meaning (source claim):** Ra describes the violet ray as the unique spectrograph of the whole entity and as the surrounding register of the entire system; brilliance of the centres is explicitly 'not considered above the balanced aspect or violet-ray manifestation' when judging harvestability. The violet ray is therefore not balanced or activated like the others.
* **Minimal procedure / treatment (ours):** Violet is *derived*: one line computed from the six centres and the current tags, shown but never spent, raised or trained. It is the summary a healer reads and the register the harvest scene looks at.
* **State fragment:** `violet: {register: str, derived_from: [centres, tags]}, read-only`
* **Interactions:** Read by healing and harvest scenes; cannot be a prerequisite for any ability.
* **Non-goals:** No violet stat, no violet XP, no 'unlock violet' step, no violet-based power tree.
* **Open question:** Should the derived register ever be a *penalty* signal (a visible warning of depolarization)?

### `blockage-and-restoration` — Blockage, strain and restoration

* **Priority:** `core` · **rules needed:** yes · **page:** https://www.lawofone.info/c/Energy+Centers
* **Source:** 15.9, 15.10, 15.12
* **Faithful meaning (source claim):** Ra names blockages per centre and their typical manifestations (eccentricity, power and manipulation, difficulty expressing universal love, difficulty accepting communication, unworthiness at the indigo centre), and says those blocked in the first three centres have continuing difficulty in further seeking.
* **Minimal procedure / treatment (ours):** A centre becomes blocked or strained through play, with the manifestation named in fiction. Restoration is a scene of honest response or a meditation/balancing beat, not a purchase. A blocked low centre suppresses the *permission* of a higher bright one; it never removes a character's agency.
* **State fragment:** `centre state + one-line manifestation + cause`
* **Interactions:** Explains tags; gates permissions; never gates a player's choice.
* **Non-goals:** No hit-point model, no medical claims, no random blockage, no permanent loss without a review beat.
* **Open question:** Should a blockage cost anything mechanical at all, or only permissions?

### `meditation` — Meditation

* **Priority:** `optional` · **rules needed:** yes · **page:** https://www.lawofone.info/c/Meditation
* **Source:** 17.40, 49.7, 43.31, 42.13
* **Faithful meaning (source claim):** Asked for a best way or a recommended technique, Ra answers 'No' twice; asked about a special room, Ra calls a Faraday cage 'a gadget' and commends a place apart from distractions used for no other purpose.
* **Minimal procedure / treatment (ours):** A meditation beat: the player states what they are seeking (not a technique), and the GM may offer a symbol, a quieting, or nothing at all. It can open an Integration beat or clear a strained centre. It never produces a reliable answer to a question.
* **State fragment:** `meditation: {scene, intent, outcome: silence|symbol|clearing}`
* **Interactions:** Feeds Integration and centre restoration; may precede Higher Self contact.
* **Non-goals:** No optimal technique, no meditation dice, no resource regeneration on a timer.
* **Open question:** Should an empty result be common enough to be the default, and how does the table take that?

### `balancing-practice` — Balancing exercises

* **Priority:** `optional` · **rules needed:** yes · **page:** https://www.lawofone.info/c/Balancing
* **Source:** 15.9, 15.12, 40.10
* **Faithful meaning (source claim):** Balancing is the retrospective work of understanding and accepting each energy centre; the key is the 'unstudied, spontaneous, and honest response' to experience.
* **Minimal procedure / treatment (ours):** After a catalyst the player may balance a centre by describing its opposite and accepting both sides; on the table's agreement the centre improves one step.
* **State fragment:** `balancing: {scene, centre, opposite_described: bool}`
* **Interactions:** Alternative to meditation for restoration; both feed Integration.
* **Non-goals:** Not a repeatable daily buff; no balancing for someone else without consent.
* **Open question:** Can another character guide a balancing, and does that violate free will if unasked?

### `prana-energy` — Prana / vital energy

* **Priority:** `optional` · **rules needed:** yes · **page:** https://www.lawofone.info/glossary.php
* **Source:** glossary: Prana, glossary: Élan vital, issue #1124 §E
* **Faithful meaning (source claim):** The glossary defines prana as 'the life force or vital energy' — a definition, not a point pool. Ra does not define an RPG-style Prana reserve.
* **Minimal procedure / treatment (ours):** Three tags instead of a pool: ready / strained / depleted. Deliberate PSI, healing or a long projection strains prana; meditation or a night's rest restores it. Depleted prana forbids further workings until restored; it never harms the character.
* **State fragment:** `prana: 'ready'|'strained'|'depleted'`
* **Interactions:** Costs for healing, projection, White Magic and sustained SMC work.
* **Non-goals:** Do not call it Ra's numbers; no numeric pool by default; no farming by waiting.
* **Open question:** Do PSI and White Magic draw on the same prana, given Ra treats them as related but distinct practices?

### `healing-invitation` — Healing and energy transfer

* **Priority:** `optional` · **rules needed:** yes · **page:** https://www.lawofone.info/c/Healing
* **Source:** Healing category, 42.18, 15.12 (green ray)
* **Faithful meaning (source claim):** Ra: healing occurs when a mind/body/spirit complex realises, deep within itself, the Law of One — the healer offers a channel, and the recipient must open to it. Ra also notes a green-ray centre can be 'overly open' through an intensive desire to serve, at cost to the self.
* **Minimal procedure / treatment (ours):** The healer states an intention and offers; the recipient may accept, decline or set terms. On acceptance the scene may clear a strained centre, ease a tag, or set conditions for recovery. No guaranteed cure, no roll that overrides the recipient's choice.
* **State fragment:** `healing: {healer, recipient, consent, intention, outcome}`
* **Interactions:** Bright green centre; spends prana; can restore a blocked centre; the self-spending risk is a real cost.
* **Non-goals:** No hit points, no medicine, no clinical claims, no healing without consent.
* **Open question:** How should the 'healer spends themself' risk be represented without punishing kindness?

### `teach-learning` — Teach / learning

* **Priority:** `optional` · **rules needed:** yes · **page:** https://www.lawofone.info/c/Teach/Learning
* **Source:** Teach/Learning category, Archetypical Mind category (teaching via intuition)
* **Faithful meaning (source claim):** Ra frames teaching as the same act as learning, and describes teaching as arriving through intuition rather than instruction.
* **Minimal procedure / treatment (ours):** A teaching scene: the teacher states what they are trying to convey, the learner states what they are ready to hear, and the outcome is a new tag, a cleared distortion, or nothing. A lesson that is refused is still learned by the teacher.
* **State fragment:** `teaching: {teacher, learner, content, learner_ready: bool, outcome}`
* **Interactions:** Moves tags; may open an Awareness permission; symmetric in effect.
* **Non-goals:** No XP transfer, no skill training table, no lecturing bonus.
* **Open question:** Should a teacher gain Awareness when the learner refuses?

### `higher-self-scripted` — Higher Self guidance (scripted only)

* **Priority:** `core` · **rules needed:** yes · **page:** https://www.lawofone.info/c/Higher+Self
* **Source:** 70.8, 70.9, 70.10, 70.11, 70.12
* **Faithful meaning (source claim):** The Higher Self is the entity of mid-sixth density offering this service to its own past self; it does not manipulate: 'it protects when possible and guides when asked, but the force of free will is paramount'.
* **Minimal procedure / treatment (ours):** Guidance arrives only when the player asks (a meditation or a direct plea) or when the GM spends a prepared story beat. It is a symbol, a dream, a coincidence — never a fact, a map or a prediction. The GM must leave the interpretation to the player.
* **State fragment:** `guidance: {scene, sought_by_player: bool, form: symbol|dream|coincidence, interpreted_as}`
* **Interactions:** Follows the free-will rule; can open an Integration beat; cannot be invoked as a skill.
* **Non-goals:** No summoned NPC, no oracle, no reliable future knowledge, no player-triggered ability roll.
* **Open question:** May the GM use guidance to save a character from a choice the table regrets?

### `precognition-scripted` — Precognition (scripted only)

* **Priority:** `core` · **rules needed:** yes · **page:** https://www.lawofone.info/c/Higher+Self
* **Source:** 70.11, issue #1124 §7
* **Faithful meaning (source claim):** Ra explicitly denies that the Higher Self manipulates its past selves; any future knowledge in the material is framed as guidance, not as a forecast a character can operate.
* **Minimal procedure / treatment (ours):** Precognition exists only as a scripted story event: the GM shows a fragment, the player decides what it means, and the fragment must remain ambiguous until it resolves. No mechanic may roll for it, buy it or improve it.
* **State fragment:** `event: {scene, fragment, resolved_as} only`
* **Interactions:** Bounded by the free-will rule; cannot be used to bypass a scene.
* **Non-goals:** No precognition skill, no certainty, no repeatable divination, no advantage in resolution.
* **Open question:** How often can a scripted fragment appear before it becomes a mechanic in disguise?

### `service-dilemmas` — Service dilemmas and the limits of help

* **Priority:** `core` · **rules needed:** yes · **page:** https://www.lawofone.info/c/Service+to+Others
* **Source:** 17.30, Service to Others category (starving entity; evangelist working)
* **Faithful meaning (source claim):** Ra: the best service is the constant attempt to share the love of the Creator as known to the inner self, requiring self-knowledge and opening to the other-self without hesitation; and to a starving entity 'the appropriate response is the feeding of the body'. A working that abridges free will is blocked.
* **Minimal procedure / treatment (ours):** A dilemma frame with three explicit questions: what does this other-self actually need; whose choice is this; what does helping cost the helper. Interventions that override a free choice are permitted in play, but they cost polarization or a tag, and the table names why.
* **State fragment:** `dilemma: {other_self_need, whose_choice, helper_cost, chosen_intervention, table_note}`
* **Interactions:** The main writer to Polarization; tests the free-will rule against real urgency.
* **Non-goals:** No 'good act' menu, no alignment points, no automatic reward for self-sacrifice.
* **Open question:** How do you represent helping someone who cannot consent (unconscious, coerced, a child)?

### `time-space-presence` — Time/Space as a playable realm

* **Priority:** `core` · **rules needed:** yes · **page:** https://www.lawofone.info/c/Time/Space
* **Source:** 43.12, 43.7, 47.8, 70.14, 70.17, 70.22, glossary: Space/time, glossary: Time/space, glossary: inner planes
* **Faithful meaning (source claim):** Ra says time/space is 'no more homogenous than space/time. It is as complex and complete a system of illusions, dances, and pattern as is space/time and has as structured a system of what you may call natural laws.' The glossary calls it the environment of the inner planes and unseen worlds, reciprocal to space/time. The glossary also names inner planes (astral, devachanic); these are particular inner-plane environments associated with, but not necessarily identical to, the whole time/space domain (43.7, 47.8). 43.12 confirms the practical shape: a density may have ordinary space/time incarnation and time/space experience between incarnations, so realm and density are independent axes.
* **Minimal procedure / treatment (ours):** Time/Space is a second scene-mode with its own rules: entry by deep meditation or sleep (or astrally), perception that is symbolic rather than spatial, no physical action, communication by intent, and a return cost. Duration is measured in scenes, not distance, and returning is not automatic.
* **State fragment:** `mode: 'space_time'|'time_space', inner_plane: null|'astral'|'devachanic'|named, entry: {method, anchor, depth}, return: {difficulty, anchor_intact}, regional_conditions: [str]`
* **Interactions:** Carries astral projection, healing review, higher-self contact and SMC scenes; distinct from density.
* **Non-goals:** Not a void, not teleportation, not a second map, no travel-speed maths, no physics simulation. No assumption that all time/space is astral, or that every metaphysical region is reachable.
* **Open question:** Is 'depth' better as a tag than a number? What anchors a traveller?

### `astral-projection` — Astral projection and the astral body

* **Priority:** `core` · **rules needed:** yes · **page:** https://www.lawofone.info/glossary.php
* **Source:** 43.7, 47.8, glossary: Devachanic, glossary: Ectoplasm, glossary: Ka, glossary: astral body, glossary: ectoplasm, issue #1124 §C
* **Faithful meaning (source claim):** The glossary ties the astral to the green-ray body (ectoplasm is 'a manifestation of the astral body or green-ray body') and names the ka as the form-maker or indigo-ray body; the devachanic is 'the plane above the astral, corresponding to blue ray'. Ra distinguishes astral-plane thought-form entities from physically embodied subterranean entities (43.7), and the green-ray/astral body from the indigo form-maker body and other subtle bodies (47.8). The glossary links ectoplasm to the manifestation of the astral (green-ray) body.
* **Minimal procedure / treatment (ours):** Projection procedure: (1) settle and state intent, spending prana if forced; (2) leave a link to the body, which is the vulnerability; (3) travel in Time/Space by intent and symbol; (4) meet and speak, but not touch, unless manifesting; (5) return — a failed return is a scene of its own, not a death. Projection is public and institutional, part of ordinary life.
* **State fragment:** `projection: {body_location, link_integrity, body: astral|ectoplasmic, duration_scenes, prana, inner_plane: null|named}`
* **Interactions:** Requires Time/Space; bright blue/indigo centres; ectoplasm; SMC scenes; healing review.
* **Non-goals:** No combat layer, no separate character sheet, no free scouting of the physical world, no 'Cyber' layer. Astral projection is an activity and body-mode, NOT a density, and not another name for fourth density.
* **Open question:** Should link integrity be a number or a countdown of scenes?

### `ectoplasm-manifestation` — Ectoplasm / astral manifestation

* **Priority:** `optional` · **rules needed:** yes · **page:** https://www.lawofone.info/glossary.php
* **Source:** glossary: Ectoplasm, Healing category (green-ray over-openness)
* **Faithful meaning (source claim):** Ectoplasm is a manifestation of the astral or green-ray body; Ra's healing material ties the green ray to the adept's channel.
* **Minimal procedure / treatment (ours):** With a bright green centre and a settled link, an astral traveller may manifest enough to be seen or to speak, at a cost: the manifestation is legible to anyone present, and it spends prana. It cannot move objects or harm.
* **State fragment:** `manifestation: {visible: bool, audible: bool, prana_cost}`
* **Interactions:** A bridge between the astral and physical layers without merging them.
* **Non-goals:** No telekinesis, no combat, no physical immunity, no free invisibility.
* **Open question:** Who can perceive a manifestation without training — everyone, or the aware?

### `mind-body-spirit-complex` — Mind / Body / Spirit as one complex

* **Priority:** `core` · **rules needed:** yes · **page:** https://www.lawofone.info/c/Definitions
* **Source:** glossary: Mind/body/spirit complex, 15.9, 38.5, issue #1124 §D
* **Faithful meaning (source claim):** A mind/body/spirit complex is a self-aware incarnated being after the veiling; Ra treats the three as aspects of one complex, and speaks of coloured bodies distinguished from the ray centres.
* **Minimal procedure / treatment (ours):** The sheet has three columns — mind, body, spirit — that hold *state*, not separate pools: mind carries tags and attention, body carries the physical situation and prana, spirit carries awareness and the violet register. Any mechanic names which column it touches.
* **State fragment:** `complex: {mind: {...}, body: {...}, spirit: {...}}`
* **Interactions:** Everything else on the sheet belongs to one column; this is the ontology, not a fourth score.
* **Non-goals:** Not three classes, not three health pools, not a clinical model; the Luhmann analogy (psychic / living / social) is a design lens only.
* **Open question:** Does the body column need anything beyond prana and fiction, given there are no hit points?

### `veil-and-forgetting` — Veil, forgetting and glimpses

* **Priority:** `optional` · **rules needed:** yes · **page:** https://www.lawofone.info/synopsis.php
* **Source:** glossary: Veil, 77.17, 79.27, 12.28, 12.30
* **Faithful meaning (source claim):** The veil is the permeable separation between conscious and subconscious mind, introduced by this Logos to intensify seeking; fourth-density experience begins with an awareness third density cannot remember, and Wanderers in particular forget.
* **Minimal procedure / treatment (ours):** Occasional glimpses: a dream fragment, a symbol, a moment of recognition, a memory that is not yours. Each is a one-line scene permission granted by the GM or bought with a meditation beat. Nothing is guaranteed and nothing is explained.
* **State fragment:** `glimpse: {scene, kind: dream|symbol|memory, content, interpreted_as}`
* **Interactions:** Feeds Awareness and Wanderer backgrounds; never substitutes for a scene.
* **Non-goals:** No memory-point economy, no player-authored past, no reliable recall of another life.
* **Open question:** Should a Wanderer get more glimpses, or the same number with more resonance?

### `wanderer-background` — Wanderer background

* **Priority:** `optional` · **rules needed:** yes · **page:** https://www.lawofone.info/c/Wanderers
* **Source:** 12.26, 12.27, 12.28, 12.30, 12.31
* **Faithful meaning (source claim):** Wanderers are 'Brothers and Sisters of Sorrow' from elsewhere, drawn by the call; most are sixth density; the challenge is that they forget the mission and become karmically involved, and they commonly carry alienation or bodily difficulty from the mismatch with third density.
* **Minimal procedure / treatment (ours):** A Wanderer tag with three parts: a mission (stated by the player), a forgetting (what they no longer know), and a cost (an alienation or body detail that is fiction, not a stat penalty). It grants glimpses, not powers.
* **State fragment:** `wanderer: {mission, forgetting, cost_tag}`
* **Interactions:** Colours Veil glimpses and Higher Self contact; does not change density or scores.
* **Non-goals:** No free powers, no superior density, no exemption from the free-will rule, no clinical framing of the cost.
* **Open question:** Should the mission be player-chosen, GM-chosen, or discovered in play?

### `confederation-contact` — Confederation contact and calls for aid

* **Priority:** `optional` · **rules needed:** yes · **page:** https://www.lawofone.info/c/Confederation+of+Planets
* **Source:** 21.15, 21.16, 21.17, Confederation of Planets category
* **Faithful meaning (source claim):** The Confederation is roughly fifty-three civilizations and five hundred planetary complexes, including beings from Earth who have passed beyond third density; its members send love and light to those who call, and they do not intervene uninvited.
* **Minimal procedure / treatment (ours):** A call is a scene in which a character asks, sincerely, for aid. The response may be a presence, a symbol, a refusal, or silence — and the GM states which interpretation is the characters' and which is the world's. No summon, no bargaining table, no stat blocks.
* **State fragment:** `contact: {caller, sincerity, response_form, interpreted_by}`
* **Interactions:** Bounded by free will; overlaps Higher Self guidance and Time/Space; feeds SMC scenes.
* **Non-goals:** No alien combat, no technology trade, no automatic rescue, no guaranteed answer.
* **Open question:** What makes a call sincere in mechanical terms, if anything?

### `inner-planes-and-bodies` — Inner planes, astral and devachanic regions, and the subtle bodies

* **Priority:** `optional` · **rules needed:** no · **page:** https://www.lawofone.info/glossary.php
* **Source:** 43.7, 47.8, glossary: inner planes, glossary: astral body
* **Faithful meaning (source claim):** Ra distinguishes astral-plane thought-form entities from physically embodied subterranean entities (43.7), and the green-ray astral body from the indigo form-maker body and other subtle bodies (47.8). The glossary names inner planes including astral and devachanic.
* **Minimal procedure / treatment (ours):** Reference vocabulary, not a subsystem. Scenes that occur in time/space may name an `inner_plane`; the game never maps inner planes to a grid or asserts a rigid nested topology, because the source does not settle one. Astral travel uses the astral body; entering incarnation uses the indigo form-maker — a distinction the game preserves in naming, not in numbers.
* **State fragment:** `(reference only; scene.inner_plane may name astral, devachanic, or another named region)`
* **Interactions:** Informs the astral-projection and time-space rows; prevents 'all time/space is astral' and 'astral equals fourth density'.
* **Non-goals:** No plane-hopping map, no second travel system, no subtle-body attribute scores.
* **Open question:** Is any nested topology implied by the sources, or only a loose association? Unresolved.

### `embodiment-modes` — Embodied, projected, manifesting, disincarnate

* **Priority:** `core` · **rules needed:** yes · **page:** https://www.lawofone.info/glossary.php
* **Source:** 43.16, 43.7, 12.17, glossary: Ka, glossary: Ectoplasm
* **Faithful meaning (source claim):** Ra describes fourth-density beings as physically embodied — different chemical elements, similar appearance (43.16), eating (43.17) — while distinguishing astral-plane entities from physically embodied ones (43.7). The material names several bodies, not one: the green-ray or astral body, and the indigo-ray form-maker, the ka. Ectoplasm is the astral body's manifestation (glossary).
* **Minimal procedure / treatment (ours):** One field, four values, and the default is the first: `embodied` (the physical vehicle is where the character is — the normal condition of play), `projected` (awareness is in an astral body; the physical body is elsewhere and its link is the vulnerability), `manifesting` (a projected character is spending to be seen or heard in the physical realm), `disincarnate` (NPC-only, between lives). Projection sets the field to `projected`; manifestation sets it to `manifesting` for a scene and back. Nothing in play sets `density`.
* **State fragment:** `embodiment: 'embodied' (default) | 'projected' | 'manifesting' | 'disincarnate'; body: 'physical'|'astral'|'form_maker'; link: <anchor id>|null`
* **Interactions:** This is where astral projection lives: `astral-projection` says how to project, this row says what state that puts a character in. `visibility-manifestation` reads the perceptibility of a manifesting character; `ectoplasm-manifestation` prices it; `inner-planes-and-bodies` names where a projected character arrives.
* **Non-goals:** Not a second sheet, not a health model, not four parallel action systems, and no ghost PCs: `disincarnate` is not a playable option.
* **Open question:** Is the indigo/form-maker body ever playable, or always the shape of a review or healing scene?


## 3. Optional narrativist tools

### `archetypal-contemplation` — Archetypical Mind as contemplation

* **Priority:** `optional` · **rules needed:** yes · **page:** https://www.lawofone.info/c/Archetypical+Mind
* **Source:** Archetypical Mind category, glossary: Matrix, Potentiator, Significator
* **Faithful meaning (source claim):** The archetypes are presented as concept complexes that teach via intuition through a hierarchy of informers: subconscious, group or planetary mind, guides, higher self, archetypical mind, cosmic mind.
* **Minimal procedure / treatment (ours):** Optional card or prompt draws: the player names a situation, draws an archetype (Matrix, Potentiator, Significator, or a named figure), and answers one question from that stance. The answer is fiction, never a check.
* **State fragment:** `contemplation: {situation, archetype, question, answer}`
* **Interactions:** Can open an Integration beat; can be used with a tarot-like deck; no combat or class use.
* **Non-goals:** No class system, no divination mechanic, no stat bonuses, no 'archetype powers'.
* **Open question:** Is a deck required, or is a prompt list enough?

### `white-magic-ritual` — White Magic: a bounded ritual procedure

* **Priority:** `optional` · **rules needed:** yes · **page:** https://www.lawofone.info/c/White+Magic
* **Source:** White Magic category, 41.2, 42.13, 42.18, glossary: Lesser Banishing Ritual of the Pentagram
* **Faithful meaning (source claim):** Ra approves a banishing ritual as preparation for a working, describes visualisation of an inspiring shape or colour as the heart of the religious path of visualisation, and says of positively polarised entities that 'it is not well ... to work singly'.
* **Minimal procedure / treatment (ours):** A ritual has four stated elements — intention, preparation, focus, and consequence — and one outcome appropriate to its scale. Its reach is bounded by free will: it cannot compel a person, and a working that abridges choice simply does not take. Extraordinary effects are GM adjudication, not a spell list.
* **State fragment:** `ritual: {intention, preparation, focus, participants, prana_cost, outcome, free_will_respected}`
* **Interactions:** Spends prana; benefits from a bright blue/indigo centre; group rituals draw on SMC trust.
* **Non-goals:** No spell catalogue, no damage spells, no magical duels, no guarantee, no solo god-mode.
* **Open question:** Which rituals are worth writing as examples, and how many is too many?

### `group-rite` — Collective working

* **Priority:** `optional` · **rules needed:** yes · **page:** https://www.lawofone.info/c/White+Magic
* **Source:** 42.18, Confederation of Planets category (central thought complex)
* **Faithful meaning (source claim):** Ra's remark that positively polarised entities should not work singly, and the Confederation's voluntary shared thought complex, both point at collective practice as the norm.
* **Minimal procedure / treatment (ours):** A group ritual requires each participant's stated consent and one shared intention; the group sheet's trust sets the ceiling on what may be attempted, and a member may withdraw mid-working.
* **State fragment:** `group_rite: {participants[], consent_each: bool, intention, trust_ceiling, outcome}`
* **Interactions:** Bridges White Magic and the SMC sheet without merging them.
* **Non-goals:** No pooling of individual scores, no forced participation, no mass mind control.
* **Open question:** Does a group rite need a failure mode that is more interesting than 'nothing happens'?


## 4. Setting principles and out-of-scope material

### `one-infinite-creator` — The One Infinite Creator / Intelligent Infinity

* **Priority:** `narrative_only` · **rules needed:** no · **page:** https://www.lawofone.info/synopsis.php
* **Source:** 4.20, 28.1, 13.13, synopsis: The One Infinite Creator
* **Faithful meaning (source claim):** There is only one, and that one is the Infinite Creator, also called Infinite Intelligence; each portion of the creation paradoxically contains the whole.
* **Minimal procedure / treatment (ours):** Narrative framing only: the axiom behind every character's seeking; never a power meter.
* **Interactions:** Colours language; the gateway scene is the one bounded exception.
* **Non-goals:** No 'Creator favour' stat, no divine intervention dice, no cosmology subsystem.
* **Open question:** Should a one-off 'gateway to intelligent infinity' scene be written as a climax, or left to the table?

### `illusion` — Illusion and manifestation

* **Priority:** `narrative_only` · **rules needed:** no · **page:** https://www.lawofone.info/synopsis.php
* **Source:** 1.6, 106.23, 27.17, synopsis: Illusion
* **Faithful meaning (source claim):** All manifestation, the appearance of many-ness, is an illusion engineered so the Creator may know Itself.
* **Minimal procedure / treatment (ours):** Narrative permission for symbolic scenes; no illusion magic subsystem.
* **Interactions:** Frames Time/Space and archetypal scenes.
* **Non-goals:** No illusion spells, no reality-bending mechanics.

### `logos-second-distortion` — Logos / Love (second distortion)

* **Priority:** `narrative_only` · **rules needed:** no · **page:** https://www.lawofone.info/synopsis.php
* **Source:** 15.21, 27.12, 28.7, 13.13
* **Faithful meaning (source claim):** The second distortion is Love or the Logos, the creative principle that forms intelligent energy from the potential of intelligent infinity; a Logos may create a star system or a galaxy, each with its own natural laws.
* **Minimal procedure / treatment (ours):** Setting explanation only; Logos is not a character's compassion and not a polarization bonus.
* **Interactions:** Explains why other Logoi's archetypes are 'murky'.
* **Non-goals:** No 'Logos bonus', no cosmic-scale play.

### `light-third-distortion` — Light (third distortion)

* **Priority:** `narrative_only` · **rules needed:** no · **page:** https://www.lawofone.info/synopsis.php
* **Source:** 15.21, 78.9, 13.9, 13.17
* **Faithful meaning (source claim):** The third distortion is light, the first manifestation visible to the eye, intelligent and the building block of matter, with an upward-spiralling characteristic that impels evolution.
* **Minimal procedure / treatment (ours):** Narrative colour; no light-magic system.
* **Interactions:** Background for healing's 'light' language.
* **Non-goals:** No photon stats, no light-based powers.

### `sub-logoi` — Sub-Logoi and sub-sub-Logoi

* **Priority:** `narrative_only` · **rules needed:** no · **page:** https://www.lawofone.info/synopsis.php
* **Source:** 28.9, 29.1, 29.2, 29.7, 81.33, 91.3
* **Faithful meaning (source claim):** Our galaxy was created by a single Logos; our sun is a sub-Logos that individualises the natural laws and refines the cosmic mind into an archetypical mind; humans are sub-sub-Logoi.
* **Minimal procedure / treatment (ours):** Setting explanation for why this world's archetypes exist at all.
* **Interactions:** Grounds the Archetypical Mind row.
* **Non-goals:** No nested-creation generator.

### `densities-seven` — The seven densities and the octave

* **Priority:** `narrative_only` · **rules needed:** no · **page:** https://www.lawofone.info/synopsis.php
* **Source:** 16.51, 28.15, 28.16, 78.15, 13.16, 9.13, 76.13, 76.16, 6.15, 43.11, 25.11, 43.14, 33.20, 16.22, 52.12
* **Faithful meaning (source claim):** The creation has seven densities; the eighth is the first of the next octave. Third density is where the path is chosen; fourth is love/understanding; fifth is light/wisdom; sixth is unity; seventh is the gateway.
* **Minimal procedure / treatment (ours):** Context for the campaign and for NPCs. PCs remain fourth density; progression beyond is not a rule.
* **Interactions:** Explains the fixed PC density and the NPC ranges.
* **Non-goals:** No density advancement track, no fifth-density rules, no density-as-dimension.

### `two-paths-cosmology` — The two paths as cosmology

* **Priority:** `narrative_only` · **rules needed:** no · **page:** https://www.lawofone.info/c/The+Two+Paths
* **Source:** 19.19, 7.15, 16.31
* **Faithful meaning (source claim):** Consciousness has two poles, service to others and service to self, and the goal of third density is to choose one; Ra notes a positive society finds collective work easier.
* **Minimal procedure / treatment (ours):** Setting premise; the playable rules are the polarization rows.
* **Interactions:** Frames the NPC-only StS cast.
* **Non-goals:** No second playable path.

### `third-density-percentages` — The 51% / 95% figures

* **Priority:** `out_of_scope` · **rules needed:** no · **page:** https://www.lawofone.info/synopsis.php
* **Source:** 17.31, 17.32, 47.3
* **Faithful meaning (source claim):** Ra gives 51% service to others and 95% service to self as harvest thresholds for third density.
* **Minimal procedure / treatment (ours):** Cited as context only; explicitly not converted into the 0-10 fourth-density scale.
* **Interactions:** Colours Harvest scenes.
* **Non-goals:** No arithmetic mapping from percentages to the PC scale; no harvest calculator.
* **Open question:** If a table wants to model third-density NPCs' harvestability, does that need a rule at all?

### `harvest-context` — Harvest and cycles

* **Priority:** `out_of_scope` · **rules needed:** no · **page:** https://www.lawofone.info/c/Harvest
* **Source:** 17.29, 9.4, 40.8, 17.1, 62.29, 63.9, Harvest category
* **Faithful meaning (source claim):** Harvest is the graduation of entities whose lessons are complete; Ra gives 2011 as a probable nexus but declines confidence, and describes a 100-700 year transition it calls uncertain.
* **Minimal procedure / treatment (ours):** Campaign backdrop and optional scene frames; no dates, no advancement for PCs already in fourth density.
* **Interactions:** The violet register is what such a scene reads.
* **Non-goals:** No real-world date, no harvest percentage for anyone, no forced plot.
* **Open question:** What is the fourth-density equivalent of a harvest scene, if any?

### `veiling-cosmology` — Why the veil exists

* **Priority:** `narrative_only` · **rules needed:** no · **page:** https://www.lawofone.info/synopsis.php
* **Source:** 77.17, 79.27, 93.4
* **Faithful meaning (source claim):** This Logos veiled the subconscious to intensify seeking, and the result was a more vivid and varied experience of the Creator by the Creator.
* **Minimal procedure / treatment (ours):** Explains the design of the world; the playable rule is the glimpse mechanic.
* **Interactions:** Grounds Awareness and Wanderer forgetting.
* **Non-goals:** No veil meter.

### `practical-advice` — Begin and end in the Creator, not in technique

* **Priority:** `narrative_only` · **rules needed:** no · **page:** https://www.lawofone.info/synopsis.php
* **Source:** 52.11, 17.30
* **Faithful meaning (source claim):** Ra's stated advice to the group: 'Always begin and end in the Creator, not in technique.'
* **Minimal procedure / treatment (ours):** A design constraint on the whole game: intention and relationship outrank optimisation; no ritual or score is the point.
* **Interactions:** A review criterion for every other row.
* **Non-goals:** Not a mechanic; if a mechanic ever makes technique the path to progress, this row is the objection.

### `entity-catalogue` — Catalogue of named species, civilizations and entities

* **Priority:** `out_of_scope` · **rules needed:** no · **page:** https://www.lawofone.info/categories.php
* **Source:** Confederation of Planets category, 12.26-12.30, glossary: Maldek, Lemuria, Mu, Zeta Reticuli, Ra category
* **Faithful meaning (source claim):** Ra names a Confederation of roughly fifty-three civilizations and five hundred planetary complexes, Wanderers, Ra itself as sixth density, and various places and beings; the material does not present a taxonomy and does not equate a civilization with a species.
* **Minimal procedure / treatment (ours):** A separate reference catalogue (data/law_of_one/entity_catalogue.json): name, source, type, reported origin, density, affiliation, ambiguity. Reference only: no playable non-human options.
* **Interactions:** Setting reference for NPCs and scenario colour.
* **Non-goals:** No alien player characters, no stat blocks, no filling gaps from wider UFO lore or NoöPunk canon.
* **Open question:** Which named civilizations carry enough source detail to be more than a name?

### `density-not-dimension` — Density is not dimension (typing rule)

* **Priority:** `narrative_only` · **rules needed:** no · **page:** https://www.lawofone.info/synopsis.php
* **Source:** 21.5, 6.24, 17.1, synopsis: Densities
* **Faithful meaning (source claim):** Ra uses 'dimension' in metaphysical registers (21.5, 6.24) while density is discussed in terms of vibrational conditions and spectrum (17.1). The texts do not equate the fourth density with a fourth geometrical coordinate.
* **Minimal procedure / treatment (ours):** Not mechanised. The treatment is a typing constraint on every other rule: `density`, `realm` (space/time vs time/space), `body`, `inner_plane` and `visibility` are separate fields and may not be substituted for one another. Any future rule that reads density as a spatial axis or a realm is wrong by construction.
* **State fragment:** `(no state; a constraint on the schema)`
* **Interactions:** Governs the vocabulary of every row above; prevents 'fourth density = an extra dimension' drift.
* **Non-goals:** No physics engine, no dimensional travel rules, no geometry.
* **Open question:** Which Ra usages of 'dimension' are metaphorical and which describe a realm? Needs a passage audit; until then the game types them separately and says so.

## What this inventory deliberately does not do

* It defines **no attributes, skills, hit points, combat, equipment, classes or XP**. Those belong to a
  host game; this module is meant to attach to one, or to stand alone as a narrativist game.
* It does not reskin anything, does not touch the NoöPunk rulebook, and does not merge rulebooks.
* It does not turn cosmology into dice. Nine concepts are `narrative_only` and three are `out_of_scope`
  precisely so that no one later mistakes a placeholder for a mechanic.

## Phase gate

Phase 2 (the standalone playable rulebook) may start only after this inventory is reviewed. The
audit fails while any implementation module exists, which is how that gate is enforced rather than
remembered.

_Generated from 49 rows; source: The Law of One (Ra Material), via lawofone.info._
