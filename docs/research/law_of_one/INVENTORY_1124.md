# Law of One RPG — Phase 1 rules inventory (#1124)

> **Status: Phase 1 research + design inventory. Not a rulebook. Nothing here is implemented.**
>
> The issue's gate is explicit: *inventory first; implementation only after review.* This document
> answers **what the Law of One specifically requires from a game**, what is optional, what is
> narrative-only, and what must not be mechanised. It does not add a NoöPunk rule, change CWN, or
> create the Law of One rulebook yet.
>
> **Source labels used throughout:**
>
> - **(S) SOURCE CLAIM** — what the Ra transcripts/synopsis actually say, cited `session.question`.
> - **(I) RPG INTERPRETATION** — our reading for a fourth-density StO game; not Ra's words.
> - **(M) PROPOSED MECHANIC** — new design, to be tested; explicitly not a claim about the source.
>
> Primary text: <https://www.lawofone.info/>. Synopsis: <https://www.lawofone.info/synopsis.php>.
> Categories: <https://www.lawofone.info/categories.php>. Glossary:
> <https://www.lawofone.info/glossary.php>. Definitions:
> <https://www.lawofone.info/c/Definitions>.

## 0. Phase gate and hard separation

**This phase delivers only this inventory and the companion entity catalogue.** It does **not**
create `rulebook/law_of_one/`, add anything to `RULEBOOK.md`, add a `src/rules/law_of_one.py`, or
touch CWN/SWN/WWN/AWN.

Proposed non-overlapping paths for Phase 2, subject to author review:

```
law_of_one_rpg/                     # new top-level artifact, never under rulebook/ or src/rules/
  rulebook/                         # standalone fourth-density rulebook
  src/law_of_one/                   # standalone Python namespace
  tests/                            # standalone tests
  examples/                         # starter scenario + play sheets
docs/research/law_of_one/           # Phase 1 research (this directory)
```

The package may later expose a host-agnostic adapter, but it must not import NoöPunk, CWN, UNSA,
cyberware, hacking or any cyberpunk subsystem. **Physical/Astral only**; Cyber is out of scope.

## 1. Source coverage method

Read and cross-checked on 2026-11-03:

| Source | Use |
| --- | --- |
| [Synopsis](https://www.lawofone.info/synopsis.php) | 8 major sections + 8 sub-sections; every heading appears in §3 |
| [Categories](https://www.lawofone.info/categories.php) | 39 top-level categories; disposition map in §4 |
| [Definitions](https://www.lawofone.info/c/Definitions) | 20 definition subcategories; disposition map in §4 |
| [Glossary](https://www.lawofone.info/glossary.php) | term check, especially *distortion*, *polarize*, *prana*, *space/time*, *ectoplasm* |
| Topic pages | Higher Self, Meditation, Service to Others, Harvest, Healing, Energy Centers, Archetypical Mind, Confederation, Densities, Wanderers, White Magic, Time/Space, Balancing, Two Paths, Veil, Teach/Learning |
| [Lore notes](../LAW_OF_ONE_LORE_NOTES.md) | existing NoöPunk source sheet; cited where it already audits a session, never copied as canon |

**Citation rule:** a session number without a checked passage is not a citation. This inventory
uses the synopsis and topic pages to identify the passage, then names the session/question. Where
the source is a category or definition page rather than a session, that is stated.

## 2. The minimum playable core (what the first module must contain)

The issue's Group 1 is the only part that must work on its own. Everything else is layered.

| Concept | Source | Faithful meaning (S) | Needed? | Priority | Minimal procedure/state (M) | Interactions | Explicit non-goals | Open questions |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| **Catalyst** | [54.17](https://www.lawofone.info/s/54), [42.16](https://www.lawofone.info/s/42) | Experience offered to a mind/body/spirit complex for growth; not intrinsically good or bad. | Core | P0 | A scene states situation + stakes; player chooses; consequence is narrated; a reflection step may change a tag or score. No roll required. | Feeds Polarization, Awareness and Distortion tags. | XP for “good deeds”; random catalyst tables; morality points per action. | How often may a scene produce a score change? |
| **Free Will / Law of Confusion** | [27.10](https://www.lawofone.info/s/27), [13.12](https://www.lawofone.info/s/13), [15.21](https://www.lawofone.info/s/15) | The first distortion; choice is the mechanism of experience. | Core constraint | P0 | Every catalyst scene offers a real choice. NPCs and SMC members cannot be overridden without consent/ consequence. GM cannot script the player's moral conclusion. | Limits healing, guidance, telepathy, SMC and Higher Self. | A “free will meter”; a dice roll to resist mind control as a default. | How does the game represent coercion by another PC? |
| **Integration / balancing** | [15.8](https://www.lawofone.info/s/15), [42.16](https://www.lawofone.info/s/42) | Experience is metabolised through reflection and acceptance, not merely suffered. | Core | P0 | End-of-scene or downtime reflection: name the catalyst, the choice, the cost; choose whether to accept, resist or reframe. A sustained pattern may move a Distortion tag. | Modifies tags; qualifies Awareness gains; can restore balance. | Generic “therapy” subsystem; clinical diagnosis; automatic healing. | Is integration always player-declared, or can the GM call for it? |
| **Polarization** | [17.30](https://www.lawofone.info/s/17), [17.34](https://www.lawofone.info/s/17) | Orientation toward service to others or service to self; the positive path is the game's player path. | Core | P0 | 0–10, starts 5. Changes only for sustained, informed choices with real cost; ordinary selfishness or mistakes do not move it. Visible warnings below 3. | Gated by Free Will; informs SMC trust; zero handoff. | Literal 51%/95% conversion; per-scene morality points; equating low score with mental illness. | Are increases as rare as decreases? Can a player contest a change? |
| **Zero / NPC handoff** | [17.34](https://www.lawofone.info/s/17) (sinkhole context) | The source describes a “sinkhole of indifference” between the paths, not an RPG control threshold. | Core contract | P0 | At 0, control transfers to the GM/NPC system after a transparent warning, a final choice scene and a table discussion. The character persists as an NPC. | Ends PC arc; SMC consequences; no silent removal. | Surprise loss; punishment for one decision; medical framing. | Exact warning cadence and whether 1 is a “last chance” state. |
| **Awareness** | [43.13](https://www.lawofone.info/s/43) (fourth-density context) + issue design | How fully fourth-density consciousness is recognised and integrated — not whether the character is fourth density. | Core | P0 | 0–10, starts 1. Milestones at 0–2 / 3–4 / 5–6 / 7–8 / 9–10 unlock perception and scene permissions, not raw power. | Time/Space, astral, Higher Self, archetypes; not Polarization. | Fifth-density advancement; automatic superpowers; a “wisdom stat” that solves mysteries. | Do milestones cost anything, or are they purely narrative? |
| **Distortion tags** | [Synopsis: Distortion](https://www.lawofone.info/synopsis.php), [1.6](https://www.lawofone.info/s/1) | A movement away from undistorted unity; can be “good” or “bad”. Not a synonym for pathology. | Core | P0 | 3–6 plain tags per character, e.g. `fear`, `need for control`, `humility`, `attachment`. Tags colour scenes and may be accepted, balanced or intensified. | Catalyst, integration, energy centres, SMC friction. | A skill tree; clinical labels; “insanity” tags. | Tag vocabulary: free-form or a closed list? |
| **Individual SMC Connection** | [20.36](https://www.lawofone.info/s/20), [48.6](https://www.lawofone.info/s/48) | Degree of participation in shared consciousness; distinct from being a member of a group. | Core | P0 | 0–10, starts 0. Rises through consensual shared experience, trust and coordination; can fall through rupture. | Group SMC, telepathy, memory sharing. | Automatic telepathy; membership = connection; consent-free mind reading. | Is connection one score or one score per relationship? |
| **Collective SMC development** | [48.6](https://www.lawofone.info/s/48), [20.36](https://www.lawofone.info/s/20) | A social memory complex is a group-level being; the group track is not the sum of individual scores. | Core | P0 | A shared sheet with 4 narrative stages (forming → resonant → shared → mature) and explicit consent/boundary fields; group scenes can advance, stall or rupture it. | Individual connection, astral, collective memory. | A civilization simulator; automatic hive-mind; erasing member agency. | Minimum group size? Can an SMC split without losing the campaign? |
| **Negative path** | [17.34](https://www.lawofone.info/s/17), [16.31](https://www.lawofone.info/s/16), [19.16–19.19](https://www.lawofone.info/s/19) | A real path in the setting; the source treats it as a distinct orientation, not a lack of empathy. | NPC/setting only | P1 | No PC track. StS figures are antagonists, tempters or cautionary mirrors; their choices follow the same catalyst logic without player-facing scoring. | Polarization contrast; SMC conflict. | Playable StS progression; “evil” as mental illness; alignment detection. | Do NPC StS scores exist at all, or only behaviour? |

### 2.1 Group 2 — fourth-density activities

| Concept | Source | Faithful meaning (S) | Rules needed? | Priority | Minimal procedure/state (M) | Interactions | Non-goals | Open questions |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| **Meditation** | [17.40](https://www.lawofone.info/s/17), [36.11](https://www.lawofone.info/s/36) | No single “best” method; practice opens the channel. | Fourth-density activity | P1 | Reflective scene: intention → what surfaces → optional stabilisation of a centre/tag. No roll, no daily buff. | Energy centres, Integration, Awareness. | Regeneration farming; meditation as precognition. | Does it need a scene cost or can it be downtime? |
| **Seven energy centres** | [15.12](https://www.lawofone.info/s/15), [39.10](https://www.lawofone.info/s/39), [15.8](https://www.lawofone.info/s/15) | Rays can be blocked/balanced/activated; violet is the total register, not balanced like the others. | Core state model | P0 | One state per ray (blocked/strained/stable/open); violet = register only. | Healing, astral, Polarization, SMC. | Seven currencies; chakra = density; trainable violet. | One state per ray enough? |
| **Balancing** | [15.8–15.13](https://www.lawofone.info/s/15) | Reflection/acceptance of self and other-self. | Core reflection | P0 | Name the distortion; accept or reframe; may clear a strain. | Tags, centres, Integration. | Clinical therapy; automatic balance. | Player-declared or GM-called? |
| **StO service dilemmas** | [17.30](https://www.lawofone.info/s/17), [15.6–15.7](https://www.lawofone.info/s/15) | Self-knowledge, opening to other-self, radiating love, respecting free will. | Core decision frame | P0 | Scene with a real cost and a free-will boundary; judge context/intent/pattern, not act count. | Polarization, tags, SMC. | Good-deed XP; saintly caricature. | Who adjudicates ambiguous cases? |
| **Love / understanding (fourth density)** | [20.36](https://www.lawofone.info/s/20), [48.6](https://www.lawofone.info/s/48) | Fourth density is love/understanding; not a quantity. | Narrative principle | P1 | Scene permissions and NPC reactions, not a stat. | Awareness, SMC, StO. | “Love points”; generic affection meter. | Does it need any mechanical hook at all? |
| **Shared mind / telepathy** | [20.36](https://www.lawofone.info/s/20), [48.6](https://www.lawofone.info/s/48) | SMC participation can share emotion/intention/memory; consent matters. | Core with SMC | P0 | Only through SMC connection/consent; content is chosen, not omniscient. | SMC, Free Will, deception. | Automatic mind-reading; consent-free memory theft. | Can a non-SMC telepath exist? |
| **Healing / energy transfer** | [2.3](https://www.lawofone.info/s/2), [4.8–4.14](https://www.lawofone.info/s/4) | Invitation, intention, conditions; the receiver's autonomy matters. | Optional activity | P1 | Invitation → intention → condition/cost → outcome; no guaranteed cure. | Green ray, prana, consent. | Hit points; clinical claims; forced healing. | How does strain manifest? |
| **Teach/learning** | [1.10](https://www.lawofone.info/s/1), [42.20](https://www.lawofone.info/s/42) | Teaching is reciprocal; the teacher learns. | Optional activity | P2 | Scene where both parties change a tag/understanding; no XP. | Awareness, SMC, StO. | Teaching as a buff; lecture-as-lore-dump. | Can it raise Awareness? |
| **Higher Self** | [70.8–70.13](https://www.lawofone.info/s/70) | Mid-sixth-density self; protects/guides when asked; does not manipulate. | Scripted narrative | P0 | GM-triggered or sought dream/symbol/synchronicity; interpretation left to player. | Awareness, Veil, precognition. | Summonable oracle; reliable future knowledge. | How often may it appear? |
| **Non-interference** | [27.10](https://www.lawofone.info/s/27), [12.3–12.7](https://www.lawofone.info/s/12) | Quarantine/contact is consent-gated, not coercive. | Core constraint | P0 | Any outside aid requires invitation/consent; refusal is respected. | Confederation, healing, SMC. | “Good” entities overriding free will. | What counts as invitation? |
| **Veil / memory** | [77.17](https://www.lawofone.info/s/77), [78.x](https://www.lawofone.info/s/78) | Forgetting/seeking; third-density Veil is not identical to fourth-density awareness. | Optional memory layer | P2 | Occasional flash/dream/symbol; player interprets; no reliable recall. | Higher Self, Wanderer, Awareness. | Memory as a skill; past-life wiki. | Which memories are safe to reveal? |
| **Wanderer background** | [12.26–12.32](https://www.lawofone.info/s/12), [89.33–89.35](https://www.lawofone.info/s/89) | Service volunteers; forgetting/drift is the failure mode. | Optional background | P2 | Tag with narrative obligations; no free powers. | Veil, Higher Self, StO. | Species/class; power upgrade; detector. | Does it change score starts? |

### 2.2 Group 3 — optional narrativist tools

| Concept | Source | Faithful meaning (S) | Rules needed? | Priority | Minimal procedure/state (M) | Interactions | Non-goals | Open questions |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| **Archetypical contemplation** | [42.16](https://www.lawofone.info/s/42), [66.21](https://www.lawofone.info/s/66), [67.28](https://www.lawofone.info/s/67) | Archetypes are resources for self-knowledge, not classes. | Optional | P2 | Draw/prompt a card or symbol; ask what it mirrors; optional tag insight. | Meditation, Awareness. | Class system; fixed bonuses. | Tarot deck or free prompts? |
| **White Magic** | [41.2](https://www.lawofone.info/s/41), [42.13–42.19](https://www.lawofone.info/s/42) | Intention, preparation, harmony, focus, consequence; bounded by free will. | Optional ritual | P2 | Five-step compact ritual; effects are small or plot-level. | Prana, energy centres, consent. | Spell list; combat magic. | How explicit may procedures be? |
| **Confederation encounters** | [6.24](https://www.lawofone.info/s/6), [7.1–7.12](https://www.lawofone.info/s/7) | Positive contact respects non-interference and interpretation. | Optional | P1 | Encounter scene with a consent/communication boundary; no automatic alliance. | Free Will, SMC, Orion. | Ally generator; war combat. | How to represent non-human motives? |
| **Orion encounters** | [7.14](https://www.lawofone.info/s/7), [12.2–12.21](https://www.lawofone.info/s/12) | Catalyst/temptation/infiltration; thought-forms and constructs. | Optional | P1 | Social/psychological scene; no tactical combat required. | Polarization, tags, MIB. | Generic alien combat. | Are Orion NPCs always deceptive? |
| **Group rites / collective practice** | [42.13–42.19](https://www.lawofone.info/s/42), [48.6](https://www.lawofone.info/s/48) | Shared intention and harmony can focus energy. | Optional | P3 | Group scene with consent + shared aim; small effect. | SMC, White Magic. | Ritual buff stacking. | Minimum participants? |
| **Noetic episodes** | [42.16](https://www.lawofone.info/s/42), [66.21](https://www.lawofone.info/s/66) | Extraordinary experience can transform understanding. | Optional | P2 | Scripted scene/permission; no repeatable skill. | Awareness, Integration. | Generic sanity/trauma subsystem. | Who triggers them? |
| **Sexual energy transfer** | Category: Sexual Energy Transfer | A distinct form of energy transfer; source treats it seriously. | Narrative/optional | P3 | Fade-to-black or narrative consequence; no point economy. | Energy transfer, SMC. | Explicit mechanical sex system; clinical claims. | Include at all in the first book? |
| **Tarot** | Category: Tarot; [66.21](https://www.lawofone.info/s/66) | Archetypal symbols used for contemplation. | Optional tool | P3 | Same as archetype prompts. | Archetypes, meditation. | A separate divination minigame. | Which deck/imagery? |

### 2.3 Group 4 — setting principles only

| Concept | Source | Faithful meaning (S) | Rules needed? | Priority | Minimal procedure/state (M) | Interactions | Non-goals | Open questions |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| **One Infinite Creator / Intelligent Infinity** | [4.20](https://www.lawofone.info/s/4), [28.1](https://www.lawofone.info/s/28) | The ground of being; one, infinite, unpolarised. | Narrative-only | — | No state. | All cosmology. | Creator meter; channeling power stat. | None; keep it unsystematised. |
| **Illusion** | [1.6](https://www.lawofone.info/s/1), [106.23](https://www.lawofone.info/s/106), [27.17](https://www.lawofone.info/s/27) | Manifestation/separateness is appearance for the Creator's self-knowledge. | Narrative-only | — | Framing device for perception/awakening. | Awareness. | Illusion-spell system. | None. |
| **Logos / Sub-Logoi / Sub-sub-Logoi** | [27.12](https://www.lawofone.info/s/27), [28.7](https://www.lawofone.info/s/28) | Nested creative intelligences. | Narrative-only | — | Context for archetypes/entities. | Cosmology, archetypes. | Playable tiers; summonable gods. | None. |
| **Light / Third Distortion** | Synopsis; [15.21](https://www.lawofone.info/s/15) | Intelligent energy; a cosmological principle. | Narrative-only | — | No resource. | Physics/ritual colour. | “Light points” or generic light magic. | None. |
| **Densities 1–3, 5–8** | [16.51](https://www.lawofone.info/s/16), [28.15](https://www.lawofone.info/s/28), [13.16](https://www.lawofone.info/s/13), [9.13](https://www.lawofone.info/s/9), [25.11](https://www.lawofone.info/s/25), [33.20](https://www.lawofone.info/s/33), [16.22](https://www.lawofone.info/s/16), [52.12](https://www.lawofone.info/s/52) | Seven densities, eighth as next octave; fourth is love/understanding. | Setting; fourth fixed | — | Context only; no progression UI. | Awareness, Harvest. | Fifth-density PC play; multi-lifetime levelling; density = dimension. | None for this module. |
| **Harvest / cycles / percentages** | [1.9](https://www.lawofone.info/s/1), [6.14–6.19](https://www.lawofone.info/s/6), [47.3](https://www.lawofone.info/s/47), [17.34](https://www.lawofone.info/s/17) | Third-density graduation context; 51% StO / 95% StS are source figures. | Setting/optional scenes | — | Background events; optional help for third-density others. | Two Paths, campaign frame. | PC 3→4 level-up; literal score conversion; real-world dates. | None until author review. |
| **Two Paths / Sinkhole / StS** | [16.31](https://www.lawofone.info/s/16), [19.16–19.19](https://www.lawofone.info/s/19), [17.34](https://www.lawofone.info/s/17) | Positive and negative orientations; indifference is a “sinkhole”. | Setting/NPC; zero handoff | P0 for zero contract | StS is NPC only; zero transfer is the only player-facing edge. | Polarization, NPCs. | Playable StS; illness metaphor; alignment detection. | Exact zero warning cadence. |
| **The Original Thought** | Category: The Original Thought | Cosmological/creative principle. | Narrative-only | — | None. | Cosmology. | A “creativity stat”. | None. |
| **Cosmology (galaxy, sun, spiritual mass)** | Definitions: Galaxy/Sun/Spiritual Mass | Source cosmology, not physics. | Narrative-only | — | Flavour/context. | Logos, densities. | Space travel physics; spiritual-mass score. | None. |
| **Ra contact / UFO history** | Category: Ra Contact, UFOs | The contact narrative and its reports. | Setting/history | — | Background; no vehicle combat. | Confederation, Orion. | Generic UFO combat; real-world claims. | None. |
| **Pyramids / objects** | Category: Pyramids/Objects | Source-attested sites/objects with noetic significance. | Setting/optional | — | Location/site colour; no generic loot. | White Magic, noetic episodes. | Equipment catalogue. | None. |
| **Earth history / People** | Category: Earth History/People | Civilizations and historical persons. | Reference only | — | Entity catalogue; no playable ancestries. | Campaign frame. | Playable races; historical simulation. | Later catalogue expansion. |

## 3. Synopsis coverage audit

Every heading in the synopsis and every concept the issue names explicitly. “Indirect” means the
concept is represented by a mechanic without being named as a stat.

| Synopsis concept | Source | Disposition | Where it lives |
| --- | --- | --- | --- |
| **One Infinite Creator / Intelligent Infinity / Infinite Intelligence** | [4.20](https://www.lawofone.info/s/4), [28.1](https://www.lawofone.info/s/28) | Narrative-only / setting principle | §5.1. No Creator meter, no channeling power stat. |
| **Illusion** | [1.6](https://www.lawofone.info/s/1), [106.23](https://www.lawofone.info/s/106), [27.17](https://www.lawofone.info/s/27) | Narrative-only / framing | §5.2. Perception and awakening, not an illusion-spell system. |
| **Distortion** | Synopsis; [1.6](https://www.lawofone.info/s/1) | Core tag mechanic | §2, §5.3. “Distortion” is not “bad”. |
| **Free Will / First Distortion / Law of Confusion** | [13.12](https://www.lawofone.info/s/13), [15.21](https://www.lawofone.info/s/15), [27.10](https://www.lawofone.info/s/27), [99.5](https://www.lawofone.info/s/99) | Core constraint | §2, §5.4. Consent and non-interference are procedural. |
| **Love / Logos / Second Distortion** | [15.21](https://www.lawofone.info/s/15), [27.12](https://www.lawofone.info/s/27) | Narrative-only / setting | §5.5. Logos is not a Polarization bonus or generic affection. |
| **Light / Third Distortion** | Synopsis; [15.21](https://www.lawofone.info/s/15) | Narrative-only | §5.6. No generic “light magic” resource. |
| **Logos, Sub-Logoi, Sub-sub-Logoi** | [27.12](https://www.lawofone.info/s/27), [28.7](https://www.lawofone.info/s/28) | Setting / archetype context | §5.7. Nested creation is not a ladder of playable tiers. |
| **Densities (all seven, octave/eighth)** | [16.51](https://www.lawofone.info/s/16), [28.15](https://www.lawofone.info/s/28), [13.16](https://www.lawofone.info/s/13), [9.13](https://www.lawofone.info/s/9), [13.21](https://www.lawofone.info/s/13), [20.36](https://www.lawofone.info/s/20), [25.11](https://www.lawofone.info/s/25), [33.20](https://www.lawofone.info/s/33), [16.22](https://www.lawofone.info/s/16), [52.12](https://www.lawofone.info/s/52) | Setting; fourth playable | §5.8. Density ≠ dimension. No routine fifth-density advancement. |
| **Two Paths / Positive and Negative Polarization / Sinkhole of Indifference** | [17.34](https://www.lawofone.info/s/17), [16.31](https://www.lawofone.info/s/16), [19.16–19](https://www.lawofone.info/s/19) | Core StO path; StS NPC | §2, §5.9. Sinkhole informs the 0 threshold; it is not a literal 0–10 source scale. |
| **Third-density percentages (51% StO / 95% StS)** | [47.3](https://www.lawofone.info/s/47), [17.34](https://www.lawofone.info/s/17) | Setting context only | §5.10. Not a conversion formula for the 0–10 fourth-density score. |
| **Harvest / cycles / graduation / planetary transition** | [1.9](https://www.lawofone.info/s/1), [6.14–6.19](https://www.lawofone.info/s/6), [17.34](https://www.lawofone.info/s/17) | Campaign context; optional scenes | §5.11. PCs already started in fourth density; no 3→4 level-up. |
| **How to be of Service to Others** | [17.30](https://www.lawofone.info/s/17), [15.6–15.7](https://www.lawofone.info/s/15) | Core decision framework | §2, §5.12. Self-knowledge, other-self, radiating love; no act-count farming. |
| **Veil / Veiling of Mind / forgetting and seeking** | [77.17](https://www.lawofone.info/s/77), [78.x](https://www.lawofone.info/s/78) | Optional memory/revelation layer | §6.7. Not a sanity mechanic; fourth-density Veil differs from third-density forgetting. |
| **Practical advice: begin and end in the Creator, not in technique** | Synopsis, “Helpful Advice” | Design constraint | §5.13. Relationships and intention outrank score optimisation. |
| **Higher Self** | [70.8–70.13](https://www.lawofone.info/s/70) | Scripted narrative relationship | §6.5. No summon, oracle or player-activated precognition. |
| **Meditation** | [17.40](https://www.lawofone.info/s/17), [36.11](https://www.lawofone.info/s/36) | Fourth-density activity | §6.1. Reflective scene, not a daily buff. |
| **Healing** | [2.3](https://www.lawofone.info/s/2), [4.8–4.14](https://www.lawofone.info/s/4) | Optional activity | §6.6. Invitation, consent, conditions; no guaranteed cure or hit points. |
| **Energy Centers** | [15.12](https://www.lawofone.info/s/15), [39.10](https://www.lawofone.info/s/39), [15.8](https://www.lawofone.info/s/15) | Core state model | §6.2. Seven rays; violet is a register, not a trainable stat. |
| **Archetypical Mind** | [42.16](https://www.lawofone.info/s/42), [66.21](https://www.lawofone.info/s/66), [67.28](https://www.lawofone.info/s/67) | Optional narrative prompts | §6.8. No class system; tarot-like cards at most. |
| **Confederation of Planets** | [6.24](https://www.lawofone.info/s/6), [7.1–7.12](https://www.lawofone.info/s/7) | Optional encounters / setting | §6.9. Non-interference and consent; no automatic allies. |
| **Wanderers** | [12.26–12.32](https://www.lawofone.info/s/12), [89.33–89.35](https://www.lawofone.info/s/89) | Optional background tag | §6.10. No unconditional powers; forgetting is the canonical failure mode. |
| **White Magic** | [41.2](https://www.lawofone.info/s/41), [42.13–42.19](https://www.lawofone.info/s/42) | Optional ritual procedure | §6.8. Intention, preparation, harmony, focus, consequence; no spell list. |
| **Catalyst** | [54.17](https://www.lawofone.info/s/54) | Core loop | §2. |
| **Balancing** | [15.8–15.13](https://www.lawofone.info/s/15) | Core reflection / energy-centre procedure | §2, §6.2. |
| **Distortion / Free Will / Positive Path** | See above | Core | §2. |
| **Teach/Learning** | [1.10](https://www.lawofone.info/s/1), [42.20](https://www.lawofone.info/s/42) | Optional activity | §6.6. Reciprocal; no teaching XP. |
| **Social Memory Complex** | [20.36](https://www.lawofone.info/s/20), [48.6](https://www.lawofone.info/s/48) | Core group mechanic | §2, §6.4. |
| **Time/Space and Space/Time** | [70.14](https://www.lawofone.info/s/70), [70.17](https://www.lawofone.info/s/70), [71.6](https://www.lawofone.info/s/71) | **First-class mechanic** | §6.3. Not narrative-only, not ordinary teleportation. |
| **Astral projection / ectoplasm** | Glossary (“ectoplasm”); [47.8](https://www.lawofone.info/s/47) | **First-class mechanic** | §6.3. Physical/Astral only; no Cyber layer. |
| **Mind/Body/Spirit Complex (MBSC)** | [Definitions: Mind, Body, Spirit](https://www.lawofone.info/c/Definitions) | Core ontology | §6.11. Three aspects, not three pools or classes. |
| **Prana / vital energy** | [59.11](https://www.lawofone.info/s/59), [Definitions: Vital Energy](https://www.lawofone.info/c/Definitions) | Optional resource | §6.12. Prefer a 3-state tag over a point pool unless play proves otherwise. |

### 3.1 Synopsis sections not named in the issue table

The synopsis also has **The Archetypical Mind**, **The Energy Centers**, and **Helpful Advice** as
major sections; all three are covered above (§6.8, §6.2, §5.13). **The Two Paths** and **The
Harvest** are covered in §5.9–§5.11. Nothing in the synopsis is left without a disposition.

## 4. Categories and definitions coverage

### 4.1 Categories (39 top-level)

| Category | Disposition |
| --- | --- |
| Archetypical Mind | Optional prompts (§6.8) |
| Balancing | Core reflection (§6.2) |
| Before the Veil | Setting/narrative (§6.7) |
| Books | Out of scope (bibliography) |
| Confederation of Planets | Optional encounters (§6.9) |
| Cosmology | Narrative-only (§5) |
| Definitions | Source vocabulary (§4.2) |
| Densities | Setting; fourth playable (§5.8) |
| Earth History | Setting/reference catalogue |
| Earth Present | Setting/reference catalogue |
| Energy Centers | Core state model (§6.2) |
| Harvest | Campaign context (§5.11) |
| Healing | Optional activity (§6.6) |
| Higher Self | Scripted narrative (§6.5) |
| Law of One | Governing principle (§5) |
| Meditation | Fourth-density activity (§6.1) |
| Miscellanea | Case-by-case; no automatic mechanic |
| Negative Path | NPC/setting only (§2) |
| Not Answered | Out of scope (absence of source answer) |
| Objects | Setting; not a generic equipment system |
| Orion | Antagonist/setting (§6.9) |
| People | Historical persons; reference only, not playable species |
| Positive Path | Core StO frame (§2) |
| Pyramids | Setting/optional noetic site |
| Ra | Source voice/Confederation member (entity catalogue) |
| Ra Contact | Setting/history, not a mechanic |
| Science | Setting; no generic tech system |
| Service to Others | Core decision framework (§2, §6.6) |
| Sexual Energy Transfer | Narrative/optional; not a generic energy-point subsystem |
| Solar System History | Reference catalogue |
| Tarot | Optional archetype tool (§6.8) |
| Teach/Learning | Optional activity (§6.6) |
| The Original Thought | Narrative-only (§5.7) |
| The Two Paths | Core/NPC distinction (§2, §5.9) |
| Third Density | Setting/context; not a PC progression track |
| Time/Space | **First-class mechanic** (§6.3) |
| UFOs | Setting/encounters; no vehicle combat |
| Wanderers | Optional background (§6.10) |
| White Magic | Optional ritual (§6.8) |

### 4.2 Definitions (20 subcategories)

| Definition | Disposition |
| --- | --- |
| Concept Complex | Narrative/archetype vocabulary |
| Crystallized Entity | NPC/setting trait; no generic stat |
| Density | Setting + fixed PC value (§5.8) |
| Energy Transfer | Healing/SMC exchange (§6.6, §6.4) |
| Galaxy | Narrative cosmology |
| Higher Self | Scripted guidance (§6.5) |
| Honor/Responsibility | Narrative duty; no duty meter |
| Inspiration | Narrative permission, not a buff |
| Intelligent Infinity | Narrative-only (§5.1) |
| Ipsissimus | NPC/setting title |
| Karma | Narrative consequence; no karma points |
| Mind, Body, Spirit | Core ontology (§6.11) |
| MBSC Totality | Setting/Higher Self context |
| Social Memory Complex | Core group mechanic (§6.4) |
| Spiritual Mass | Narrative cosmology |
| Sun | Narrative cosmology |
| Time/Space | First-class mechanic (§6.3) |
| Unconscious Mind | Narrative/Integration colour |
| Unmanifested Being | Narrative-only |
| Vital Energy | Prana resource (§6.12) |

## 5. Setting principles (narrative-only unless noted)

These are **not** mechanics. They answer what the game is about, and they forbid a mechanic that
would turn a cosmological principle into a power meter.

1. **One Infinite Creator / Intelligent Infinity (S: 4.20, 28.1).** The ground of being. No
   “Creator favour” score, no channeling power stat.
2. **Illusion (S: 1.6, 106.23, 27.17).** Manifestation and separateness are appearances; the game
   uses this to frame perception and awakening, not to add an illusion-spell list.
3. **Distortion (S: synopsis).** A movement from unity, either toward love or toward ill health.
   The tag system (§2) is the only mechanical use; it does not mean “bad” or “pathological”.
4. **Free Will (S: 13.12, 15.21, 27.10).** The governing constraint on guidance, healing, SMC and
   NPC intervention. It is enforced by procedure, not by a “willpower” stat.
5. **Love / Logos (S: 15.21, 27.12).** The creative principle. Do not reduce it to a Polarization
   bonus or to interpersonal affection; a character's compassion is not the Logos.
6. **Light (S: synopsis).** Intelligent energy. Narrative-only unless a specific fourth-density
   interaction is authored later.
7. **Logos / Sub-Logoi (S: 27.12, 28.7).** Nested creation. Context for the Archetypical Mind and
   the entity catalogue; not a ladder of playable tiers.
8. **Densities (S: 16.51, 28.15).** Seven densities, eighth as the next octave. **Fourth density is
   love/understanding and the fixed PC condition.** Fifth density is outside normal play; no
   multi-lifetime levelling. Density is not dimension.
9. **Two Paths / Sinkhole (S: 17.34, 16.31, 19.16–19).** The player path is StO. StS is NPC/setting.
   The “sinkhole of indifference” informs the zero-handoff contract; it is not a literal source
   formula for a 0–10 score.
10. **51% / 95% (S: 47.3).** Third-density Harvest context. Do not convert it into a fourth-density
    score formula or a real-world claim.
11. **Harvest (S: 1.9, 6.14–6.19).** Background/campaign context. PCs start already fourth density;
    assisting third-density others is an optional scenario, not the PC level-up.
12. **Service to Others (S: 17.30).** Self-knowledge, opening to the other-self, radiating love,
    respecting free will. No act-count farming.
13. **Practical advice (S: synopsis, “Helpful Advice”).** Begin and end in the Creator, not in
    technique. Design rule: relationships and intention outrank score optimisation.

## 6. Fourth-density activities and the first-class mechanics

### 6.1 Meditation

**S:** [17.40](https://www.lawofone.info/s/17) (“Is there a best way to meditate?” — “No.”),
[36.11](https://www.lawofone.info/s/36).

**M:** A reflective scene, not a daily buff. Choose an intention (stillness, self-examination,
compassion, listening); narrate what surfaces; optionally clear a temporary Distortion or stabilise
an energy centre. No roll; no resource regeneration loop. Meditation cannot grant precognition,
solve a mystery, or replace a player decision.

### 6.2 Energy centres (revised as attributes)

**S:** [15.12](https://www.lawofone.info/s/15) and [39.10](https://www.lawofone.info/s/39) are the
fidelity anchors: the violet ray is the total expression/register of the entity and is **not**
manipulated or balanced like the other centres. The other rays can be blocked, unbalanced or
activated; [15.8](https://www.lawofone.info/s/15) gives the balancing practice.

**M (proposal):** seven rays, but **not seven currencies**. Use one state per centre:

| Ray | State vocabulary | What it does in play | Notes |
| --- | --- | --- | --- |
| Red | blocked / stable / strained | embodiment, survival, sexuality, safety | damage ≠ physical injury |
| Orange | blocked / stable / strained | self/other-self polarity, emotion, personal power | no “emotional HP” |
| Yellow | blocked / stable / strained | social/group identity, law, institutions | ties to SMC friction |
| Green | blocked / stable / open | love/compassion, healing, astral body | central for healing/ectoplasm |
| Blue | blocked / stable / open | communication, truth, teaching | care with free will |
| Indigo | blocked / stable / open | gateway, noetic perception, archetypes | high state can unlock permissions |
| Violet | **register only** | total expression, not trainable | never a spendable stat |

**M:** A centre can be *blocked* (narrative constraint), *strained* (temporary cost after
overreach), or *open/balanced* (permission). Recovery comes from integration, meditation, healing
or a meaningful choice — not a daily tick. Higher activation may unlock a specific ritual/perception
permission, **not fifth-density status**: open green ray → healing/ectoplasm scenes; open blue ray →
teaching/communication with consent; indigo → archetype/noetic perception. These are permissions,
not a power ladder.

### 6.3 Time/Space, Space/Time, astral projection, ectoplasm

**S:** [70.14](https://www.lawofone.info/s/70), [70.17](https://www.lawofone.info/s/70),
[71.6](https://www.lawofone.info/s/71); glossary **space/time** = ordinary physical experience;
**ectoplasm** is linked to the manifestation of the astral (green-ray) body; [47.8](https://www.lawofone.info/s/47)
discusses the bodies.

**M:** two realms, one transition procedure.

- **Space/Time:** ordinary embodiment, physical causality, the host game's normal resolution.
- **Time/Space:** metaphysical experience; perception is not limited by physical distance, causality
  is not identical, and returning is not automatic.
- **Projection:** state intention, have a tether/anchoring condition, choose a destination or
  question; the astral body perceives and interacts; the physical body remains vulnerable. Return
  requires a scene action and can fail/be complicated.
- **Ectoplasm/manifestation:** under specific conditions (green-ray open, consent, cost), the astral
  body becomes apparent or can interact with the physical. This is rare, bounded and consequential —
  not a second combat body.
- **Carry rules:** memory and emotional residue carry; physical objects do not by default; injury
  to the astral body affects the physical through strain, not hit points.
- **No Cyber layer.** Physical/Astral only.

### 6.3a Awareness milestones

**S:** fourth density is love/understanding; Awareness is our measure of how fully the character
can recognise and integrate that condition. The bands below are **proposed**, not Ra's numbers.

| Awareness | Perception / permission | Does **not** grant |
| --- | --- | --- |
| 0–2 | Latent fourth-density perception; ordinary human experience with occasional “wrongness”. | Any reliable PSI, astral travel or future knowledge. |
| 3–4 | Recognition of noetic phenomena; can notice energy-centre states and symbolic patterns. | Automatic lie detection; mind reading; authority over others. |
| 5–6 | Conscious interaction with fourth-density reality; can participate in a consenting SMC scene and seek Higher Self guidance. | Fifth-density status; immunity to polarization loss; plot-solving insight. |
| 7–8 | Advanced integration; can hold multiple perspectives and recognise archetypal patterns. | Control over other minds; automatic healing; certainty about the afterlife. |
| 9–10 | Mature fourth-density awareness; the character can act as a stable anchor for a collective. | Ascension; replacement of player choice; a power stat. |

Awareness rises through **transformative experience + integration**, not through repetition. It is
independent of Polarization: a highly aware character can still fall to zero.

### 6.3b Astral society (campaign premise, not core rule)

The issue suggests a society where astral existence is public, institutionalised and part of
everyday life, tonally inspired by *Summerland*. Treat this as an **optional campaign frame**, not
a default setting fact: hospitals may have astral wards, insurers may ask about projection risk,
and schools may teach return protocols. The core rules only require the projection procedure; the
institutions are scenario colour. Do not convert them into a second technology tree.

### 6.4 Social Memory Complex (individual + collective)

**S:** [20.36](https://www.lawofone.info/s/20), [48.6](https://www.lawofone.info/s/48).

**M:** individual `SMC Connection` 0–10 and a separate group sheet with **four stages**:
`forming → resonant → shared → mature`. The group sheet records:

- members and their consent scopes (emotion / intention / memory / coordination);
- shared intention and current collective goal;
- trust and boundary state;
- rupture/reconciliation log;
- what the collective remembers that individuals do not.

Entry is opt-in. A strong telepath is **not** automatically a member. Withdrawal is allowed;
reconnection is a scene, not a toggle. The group can act as a persistent narrative entity without
erasing member agency.

### 6.5 Higher Self, Veil, Wanderers, glimpses

**S:** Higher Self [70.8–70.13](https://www.lawofone.info/s/70); Veil [77.17](https://www.lawofone.info/s/77)
and [78.x](https://www.lawofone.info/s/78); Wanderers [12.26–12.32](https://www.lawofone.info/s/12),
failure mode [89.33–89.35](https://www.lawofone.info/s/89).

**M:** Higher Self is a **scripted narrative relationship**. The GM may use a dream, symbol,
synchronicity, déjà vu or atemporal encounter when the player seeks guidance or the story demands
it. It never gives certain future knowledge, never solves a choice, and is not summonable.
**Precognition is scripted only** — no trainable, repeatable, player-activated prediction skill.
A **Wanderer** background is a tag: service mission, forgetting, responsibility. It grants no
unconditional power; the canonical failure mode is drift and karmic entanglement.

### 6.6 Healing, teach/learning, service dilemmas

**S:** Healing [2.3](https://www.lawofone.info/s/2), [4.8–4.14](https://www.lawofone.info/s/4);
teach/learning [1.10](https://www.lawofone.info/s/1), [42.20](https://www.lawofone.info/s/42);
StO [17.30](https://www.lawofone.info/s/17).

**M:** Healing is a scene with **invitation, intention, consent, conditions and cost**. The healer
offers conditions for healing; the receiver's body/psyche decides. No guaranteed cure, no hit
points, no clinical promises. Teach/learning is reciprocal: the “teacher” also changes; no XP.
Service dilemmas are judged by context, informed intent, respect for free will and sustained
pattern — not by counting good acts. Include examples: compassionate intervention that overrides
autonomy; boundaries/self-care; failure with good intentions; deliberate coercion.

### 6.6a Worked adjudication (the hard cases)

These are the cases that decide whether the Polarization system is fair. **No case changes a score
automatically**; each is one input to a pattern, and the player may contest it.

| Case | StO reading | StS reading | Proposed handling |
| --- | --- | --- | --- |
| **Compassionate intervention that overrides autonomy** | The character acts to prevent serious harm and accepts the cost. | The character decides for another without consent because they “know better”. | Ask: was there time to ask? Was the harm imminent? Did the character restore agency afterwards? A single act does not move the score; a pattern of paternalism may add a `need for control` tag. |
| **Boundaries and self-care** | Refusing an unsustainable demand is not a failure of service. | — | No penalty. The game must not reward self-destruction as StO. A boundary can be a condition for sustainable service. |
| **Failure with good intentions** | The intention and the attempt matter, but consequences are real. | — | No automatic loss; the failure may create a Distortion tag (guilt, fear) and a new catalyst. The player decides how to integrate it. |
| **Deliberate coercion** | — | Using another's fear, dependency or mind to force compliance. | A serious marker. It can reduce Polarization only if it is informed, sustained and resisted correction; the table should discuss it openly rather than ambush the player. |

The GM records the **reason**, not just the number. A player who disagrees can state the case; the
table decides. The score is legible or it is not a fair contract.

### 6.7 Distortion tags and Integration

Distortion tags are plain adjectives/nouns with a short trigger and a possible resolution. A tag
can be **accepted**, **balanced**, **intensified** or **released** through play. Integration is the
scene where a character names what happened and chooses what to do with it. Tags are not skills,
not defects, and not a hidden alignment system.

### 6.8 Archetypical Mind, contemplation, White Magic

**S:** [42.16](https://www.lawofone.info/s/42), [66.21](https://www.lawofone.info/s/66),
[67.28](https://www.lawofone.info/s/67); White Magic [41.2](https://www.lawofone.info/s/41),
[42.13–42.19](https://www.lawofone.info/s/42).

**M:** Archetypes are optional narrative prompts: a card, a role-reversal, a symbol, a
contemplation question. They are not classes and grant no fixed bonuses. White Magic is a compact
ritual procedure:

1. state the intention in plain language;
2. prepare the place/self (harmony, focus, consent);
3. enact the ritual;
4. resolve by the smallest fitting consequence, with free-will and backlash limits;
5. record what changed.

Extraordinary effects are plot/GM adjudication, not a spell catalogue.

### 6.9 Confederation, Orion and encounters

**S:** Confederation [6.24](https://www.lawofone.info/s/6), [7.1–7.12](https://www.lawofone.info/s/7);
Orion [7.14](https://www.lawofone.info/s/7), [12.2–12.21](https://www.lawofone.info/s/12).

**M:** Encounters are optional scenes. Positive Confederation contact respects non-interference,
consent and interpretation; it is not an ally generator. Orion-associated entities offer catalyst,
temptation or distortion; they do not require tactical combat rules. **Species, faction, density,
dimension and temporal origin are separate fields** (see entity catalogue).

### 6.10 Wanderers

Optional background tag, never a power upgrade. The character may have flashes of memory,
responsibility or homesickness; the GM may use these as catalyst. No identity detector, no
“starseed scan”, no automatic telepathy.

### 6.11 Mind/Body/Spirit Complex (MBSC)

**S:** [Definitions: Mind, Body, Spirit](https://www.lawofone.info/c/Definitions) — the three are
“inextricably intertwined”; [Definitions: MBSC Totality](https://www.lawofone.info/c/Definitions)
places the totality as a resource for the Higher Self.

**M:** one character with three **aspects**, not three pools/classes:

- **Mind** — thought, feeling, intention, the reflective loop;
- **Body** — embodiment, energy centres, physical/astral presence;
- **Spirit** — orientation, will, the channel to the Creator.

Mechanically, aspects colour which scenes can address a Distortion or energy centre. The Luhmann
analogy (psychic / living / social systems) is a **design analogy**, not a one-to-one mapping;
social systems are most useful at the SMC/group layer, not as a third character pool.

### 6.12 Prana / vital energy

**S:** [59.11](https://www.lawofone.info/s/59); [Definitions: Vital Energy](https://www.lawofone.info/c/Definitions);
glossary **prana** = life force/vital energy. The source describes vital energy as a complex of
mind/body/spirit energy, not an RPG point pool.

**M:** default to a **three-state tag** — `ready / strained / depleted` — rather than a numeric
pool. Deliberate PSI, healing, projection or ritual may strain it; balancing, meditation and rest
restore it. No daily regeneration tick, no farming, no “spend 3 prana” economy unless playtesting
proves a pool is needed. PSI and White Magic remain **different practices** that may share the
energy model; do not flatten them into one spell system.

## 7. Proposed minimal state (for review, not implementation)

A plain-data character record:

```
density: 4                      # fixed
polarization: 5                 # 0..10, zero -> NPC handoff
awareness: 1                    # 0..10
smc_connection: 0               # 0..10
distortions: [tag, ...]
energy_centers: {red, orange, yellow, green, blue, indigo, violet}
prana: ready|strained|depleted
astral: {projected: bool, tether: str, manifestation: none|ectoplasm}
higher_self: {contacted: bool, unresolved_symbols: [...]}
wanderer: bool
```

A group record:

```
smc_stage: forming|resonant|shared|mature
members: [...]
consent: {emotion, intention, memory, coordination}
shared_goal: str
trust: low|steady|deep
ruptures: [...]
collective_memory: [...]
```

A catalyst record:

```
situation, stake, choice, consequence, integration, tag_change?, score_changes?
```

**Change discipline (M):** score/tag changes are **rare** (typically not more than one per scene,
and not every scene), must be legible, and may be contested by the player. The GM records the
reason. Ordinary selfishness, mistakes or bad luck do not equal StS. Zero is telegraphed and
handled as a table contract.

### 7.1 Resolution principle (host-agnostic)

**Roleplay first.** Most Law of One events are resolved by the situation, the choice and the
narrated consequence. When uncertainty genuinely matters, use one of:

1. the host game's existing resolution (preferred when the module is attached);
2. a simple three-outcome prompt — cost, complication, or opening — with no new dice;
3. a single transparent check only if the host already has a check system.

**No new universal dice grammar** is introduced by this module. A Law of One scene should not
require the player to learn a second combat/skill system. Physical and social task resolution
belongs to the host; the Law of One module owns state, permissions, consent and consequences.

### 7.2 What a generic host engine handles, and what this module owns

The module is host-agnostic. It must not become a second generic RPG.

| Layer | Host engine (CWN, another OSR/narrative game, or a VTT) | Law of One module |
| --- | --- | --- |
| Task resolution | Checks, dice, combat, contest maths | No new universal dice; may call the host or use the three-outcome prompt |
| Physical harm / gear | Hit points, weapons, armour, equipment, vehicles | No gear catalogue; astral strain is not hit points |
| Social procedure | NPC reaction, persuasion, faction reputation | StO dilemmas, consent boundaries, SMC trust |
| Character sheet | Attributes, skills, classes, inventory | Density fixed at 4; Polarization/Awareness/SMC Connection; Distortion tags; energy-centre states; prana tag |
| Timekeeping | Scene/turn/downtime clock | Catalyst/Integration triggers; Time/Space scene duration and return |
| Persistence | Its own save format | Plain-data state + event log; adapter maps in/out |
| Content | Its own setting/bestiary | Law of One entities, scripted guidance, archetype prompts |

**Rule of thumb:** if the host can already do it, the module delegates. If it is specific to
fourth-density Law of One experience, the module owns it.

## 8. Duplicates and contradictions resolved

| Existing artifact | Relationship |
| --- | --- |
| [`design/LAW_OF_ONE_RPG.md`](../../../design/LAW_OF_ONE_RPG.md) | Tomi's authored design intent. This inventory treats it as the authorial brief, not a competing ruleset; it is not restated or overwritten. |
| [`docs/research/LAW_OF_ONE_LORE_NOTES.md`](../LAW_OF_ONE_LORE_NOTES.md) | NoöPunk's source-evidence sheet. Used for citation auditing only; the RPG inventory does not copy its setting conclusions. |
| `RULEBOOK.md` / `rulebook/` | **NoöPunk.** Hard separation: no Law of One content is appended, no CWN rules are imported, no UNSA frame. |
| `src/rules/` | **Host rules.** The Law of One package will be standalone; adapters later, never a second CWN core. |
| #179, #191, #1044, #1007 | Cross-referenced for existing lore/noetic material; no mechanics are duplicated here. |

**Contradictions handled:**

- *Fourth density vs dimension:* density is evolutionary stage; dimension is a separate property.
  The module never uses them interchangeably.
- *Violet ray as chakra vs trainable stat:* source says it is the total register, not balanced like
  the others; the proposal keeps it non-trainable.
- *SMC individual vs group:* two records, not one score.
- *Awareness vs virtue:* high Awareness can coexist with low Polarization; no automatic power.
- *Harvest percentages vs 0–10:* source context only; no conversion.
- *Higher Self vs precognition:* both scripted; neither is a player-activated skill.

### 8.5 First-playable architecture (the review gate)

The issue's revised Phase 1 asks for the **smallest necessary first-playable set**, not every
ability or civilization. This is that set, in build order:

| # | System | State | Player-facing procedure | Explicitly not in the first module |
| --- | --- | --- | --- | --- |
| 1 | **Core evolutionary loop** | Catalyst record, Polarization, Awareness, Distortion tags, Integration | scene → choice → consequence → reflection → rare tag/score change | XP, morality farming, random catalyst decks |
| 2 | **MBSC + seven-ray states** | three aspects; seven centres (violet as register); prana tag | colour a scene by aspect/centre; block/strain/open as permissions; balancing scene | seven currencies; chakra = density; violet training; clinical model |
| 3 | **Physical/Astral + Time/Space** | embodiment vs projection; tether; manifestation | project, travel, perceive, interact, return; ectoplasm only under conditions | Cyber layer; tactical astral combat; teleport network |
| 4 | **Collective consciousness** | individual SMC Connection + group sheet | opt-in shared emotion/intention/memory; rupture/reconciliation | civilization simulator; automatic hive-mind |
| 5 | **Scripted mystery** | Higher Self, Veil, Wanderer flags | GM-triggered dream/symbol/synchronicity; player interprets | summonable oracle; player-activated precognition |
| 6 | **Small optional activities** | meditation, healing, teach/learning, White Magic, archetype prompts | one scene each; consent and consequences | generic spell list; generic sanity/trauma system |
| 7 | **Reference catalogue** | entity catalogue; densities; cosmology | lookup only | playable species; faction stats; other-density PCs |

**If a proposed rule does not fit one of these seven, it is not in the first module.** It can be
recorded as a later optional system; it cannot delay the core.

## 9. Open questions for author review

1. **Score change cadence:** is one change per scene too generous? Should changes require a
   dedicated integration scene?
2. **Energy centres:** is one state per ray enough, or do green/blue need separate “open” and
   “balanced” values? (Proposal: one state, with narrative colour.)
3. **Prana:** tag or pool? The proposal defaults to tag; a pool only if playtests demand it.
4. **Astral tether:** what anchors the projection (body, place, relationship, object), and what
   happens when it is severed?
5. **SMC consent:** per-scene opt-in or standing scopes? Can a member veto a collective memory?
6. **Zero handoff:** exact warning cadence and whether the player may retire the character before 0.
7. **Catalyst records:** player-facing or GM-only? The proposal keeps them player-visible for
   legibility.
8. **Archetype tool:** tarot-like cards, free prompts, or both?
9. **White Magic:** how explicit may ritual procedures be without becoming a spell list?
10. **Host interface:** what is the minimal adapter contract (state in/out, scene events) for a
    later host game?

## 10. Phase gate

**No implementation, no rulebook, no Python, no merge** until this inventory is reviewed.

On approval, Phase 2 should produce, in order:

1. a standalone fourth-density rulebook under `law_of_one_rpg/rulebook/`;
2. the matching `law_of_one_rpg/src/law_of_one/` state/event module;
3. tests for ranges, zero handoff, SMC individual vs group, scripted-only Higher Self, save/load;
4. one starter scenario (same event as apocalypse for third-density NPCs and as awakening/catalyst
   for fourth-density PCs), one collective-conscience scene and one polarization dilemma.

No Cyber layer. No StS PC track. No fifth-density progression. No NoöPunk merge.
