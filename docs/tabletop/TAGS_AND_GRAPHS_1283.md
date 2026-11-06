# Tags and graphs: the portable NoöPunk layer (#1283)

> **Status: author decision, written out for table use.** NoöPunk uses **Cities Without Number**
> as its default tabletop system. CWN owns skills, action, combat, equipment and hacking. This
> document owns the portable layer above it: **five starting tag families** and **four graphs**.
> It adds no dice, ranks, point pools, power lists, emotion meters or separate Astral map.
>
> **Source:** author decision of 7 November 2026 (#1283). The earlier draft in the issue is kept
> there as history; its question about adopting tags is answered here.
>
> **Open-ended rule:** the five families are a starting vocabulary, not a closed list. Name a new
> family only when a campaign needs it and the table agrees what it records. Do not invent one in
> advance.

## 1. The five starting tag families

| Family | What it records | What it is not |
| --- | --- | --- |
| **Clue** | Something the investigators can follow up, with its source | proof, or a guaranteed lead |
| **Social** | A relationship fact that affects an interaction — trust, obligation, access | a reputation score or a universal attitude meter |
| **Goal** | An outcome a character or faction is pursuing | XP, a quest log, or an ideology score |
| **Psyche** (formerly Personality) | A character's inner life: enduring traits, values, fears, habits, and temporary states of mind | a modifier, an alignment, or a mind-control switch |
| **Astral** | A fact about the Noösphere that affects what someone can perceive, attempt or change | a PSI power list, a rank, or an automatic effect |

### 1.1 Clue

A Clue Tag records **what the character has**, **where it came from**, and **how far it can be
trusted**. The underlying clue content may live in a case file or the GM's notes; the tag is the
playable handle.

- A statement from a presence is a Clue once it is recorded — including the fact that it came from
  that presence.
- A clue is not proof. “The presence said a name” and “the name is verified” are different facts.
- Use the existing evidence ladder (`witness`, `public`, `authenticated`, `conflicting`,
  `anomalous`) when reliability matters.

### 1.2 Social

A Social Tag is a fact about a **specific relationship**, not a general reputation. “Owes Laura a
favour over the leaking warrant” is a Social Tag; “Europol likes him” is not.

- Name both parties.
- State the fact in plain language.
- Add a source or expiry when the table will need to remember why it is true.
- A Social Tag can describe what a particular tie means **today**; it can change when events change.

### 1.3 Goal

A Goal Tag is an intended outcome plus the obstacle that matters now.

- A blocked goal names its blocker; an open goal does not carry blockers.
- A faction can own a Goal Tag; the same structure works for a character.
- A political ideology is better represented as an actionable long-term Goal than as a new
  ideology attribute.
- Goal completion can gate a Story Graph transition; it does not grant XP by itself.

### 1.4 Psyche (formerly Personality)

A Psyche Tag records **inner life**, not an action modifier.

- *Protective of sources* can shape Laura across cases.
- *Shaken after the ambush* can fade as events unfold.
- *Will not cover for a colleague* is a boundary; breaking it is a decision, not a rounding error.
- Temporary states and enduring traits use the same family; the table says which is which in the
  wording.
- A Psyche Tag never forces a player character's reaction. It informs portrayal and gives the GM a
  consistent brief for an NPC.

**Compatibility:** the code keeps the historical class name `PersonalityTag` for existing saves and
dossiers. New text calls the family **Psyche** and may use `PsycheTag`; the two names refer to the
same records.

### 1.5 Astral

An Astral Tag is a **fact about the Noösphere** attached to a person, place, device or
relationship. It covers PSI, Magick, psychotronics, panpsychism and Law of One phenomena without
turning any of them into a separate subsystem.

Examples:

- a stairwell: *Someone is still waiting here*;
- Tony's implant: *Picks up abandoned intentions*;
- a witness: *Dreams in a register he does not speak*;
- a room: *The cold has a direction*;
- a relationship: *A promise made in a previous life*.

What an Astral Tag does:

- establishes what a character can **notice**, **attempt** or **change** in the fiction;
- can be invoked by a player or the GM when it is relevant;
- can become a Clue when its content is recorded and followed up;
- can coexist with a Psyche Tag (the impression and the person's reaction are different facts).

What it does **not** do:

- grant a PSI rank, Effort, a technique, a bonus or an automatic success;
- replace the Astral Body rules in #1261 when a scene actually projects;
- create a navigable Astral Graph. **Astral Tags are not an Astral Graph.** The graph remains
  deferred until an approved scene needs navigable astral locations.
- decide whether a presence is truthful, benevolent or even real.

## 2. The four graphs

| Graph | What its connections mean | Tag join |
| --- | --- | --- |
| **Physical** | Routes between places characters can physically reach | A place can carry an Astral or Clue Tag; movement is resolved by the host RPG |
| **Cyber** | Network connections between devices and systems; anchor devices to physical locations | A device can carry an Astral Tag; CWN resolves a hack |
| **Story** | Relationships and progression among series, episodes and scenes | Goal Tags gate transitions; Clue Tags point to scenes |
| **Social** | Ties among people, groups and institutions | Social Tags describe what a particular tie means today |

**Use them together:** the graphs answer **who or what is connected**; the tags answer **what is
possible and what matters**. The host RPG's procedure answers **whether an uncertain action
succeeds**.

## 3. The table procedure

1. **Frame the situation.** What does the character perceive, and what do they want?
2. **Read the graphs.** Who is connected to whom, what route reaches the place, which device holds
   the record, which scene comes next?
3. **Read the tags.** Does a Clue, Social, Goal, Psyche or Astral Tag establish that the action is
   possible, relevant or blocked?
4. **If the outcome is uncertain, roll the host RPG's procedure.** CWN by default; another
   cyberpunk RPG if the table has agreed. Do not invent a second resolver.
5. **Record what lasts.** A new fact becomes a tag; a changed fact edits or removes one. Do not
   record every sentence.

**Admissibility, not difficulty:** a tag usually decides whether an action is possible at all. If
it is possible and uncertain, the host procedure sets the difficulty. A tag never adds +1.

## 4. Worked example: Kurvi

Laura is escorting a witness through Kurvi. The stairwell carries the Astral Tag *Someone is still
waiting here*. Tony's implant carries *Picks up abandoned intentions*.

Together the tags let Tony recognise a presence expecting a reply. That is a **perception**, not a
roll. He can:

- keep pace with Laura and the witness; or
- stop and answer the presence.

If he stops, the presence might reveal whom it expected. That statement becomes a **Clue Tag** with
the presence as its source. The Social Graph identifies who could introduce Tony to that person;
the Physical Graph tells him where to go; if he tries to recover corroborating camera footage, the
Cyber Graph locates the recorder and CWN resolves the hack.

Laura and the witness keep moving on the same scene clock. CWN handles a chase if Tony falls behind.
The Astral Tag did not create a new turn, a new map or a new dice pool.

## 5. Keeping the families apart

| Question | Family | Not |
| --- | --- | --- |
| What can I follow up? | Clue | proof |
| How does this relationship stand today? | Social | reputation score |
| What are we trying to achieve? | Goal | XP or alignment |
| What is this person like inside? | Psyche | a modifier or mind control |
| What does the Noösphere let me perceive or attempt? | Astral | a power list or rank |

**Conversions are explicit:**

- An Astral impression becomes a **Clue** when its content is recorded and someone can follow it.
- A Clue about a person can be **leverage** in a Social scene; that is a use of the clue, not a
  new Social Tag.
- A repeated behaviour can become a **Psyche** trait; a single choice does not.
- A Goal can be blocked by a **Social** fact or a missing **Clue**; the blocker is named, not
  inferred.

Do not silently promote an Astral Tag into a verified Clue. The source line is the difference
between “a presence said it” and “the record confirms it”.

## 6. What happens to the earlier Astral rules?

- **#1261 Astral Body** remains the procedure when a character actually projects, enters an astral
  state or uses a PSI technique with a mechanical effect. Astral Tags are the lighter layer for
  ordinary scenes.
- **#1164** scene/tag architecture remains the source for scene types and graph links. This page
  applies the author's final family names; it does not replace the scene procedures.
- **Astral Graph** remains deferred. A tag can say *the stairwell remembers a door*; it cannot by
  itself make the stairwell a navigable astral location.
- **CWN core** remains immutable. No CWN skill, attack, save, Effort or equipment number changes.

## 7. Playtest questions

1. Can one simple procedure handle a fleeting impression, an ongoing relationship such as a Social
   Memory Complex, and a city-scale psychotronic effect? Which distinctions actually matter in
   play?
2. Who can see a tag, who can invoke it, and who decides what it means? Try leaving an entity's
   intention with the GM while giving the player the sensory impression the character actually has.
3. When does an Astral Tag become an ordinary Clue, Social or Goal Tag? Record a clue's source once,
   so another scene can distinguish testimony from verification.
4. What earlier proposals can be retired if this works? Compare the same encounter using tags and
   the procedures in #1261: one embodied encounter, one brief projection. Keep what creates a
   meaningful choice and expresses something distinctive about NoöPunk.
5. Does the table ever need a sixth family? If so, what does it record that the five cannot?

## 8. Implementation map

| Piece | Where |
| --- | --- |
| Portable five-family records | `src/rules/scene_tags.py` — `ClueTag`, `SocialTag`, `GoalTag`, `PersonalityTag`/`PsycheTag`, `AstralTag` |
| NPC dossier records and tag book | `src/world/narrative_tags.py` — the four NPC-side families plus `AstralTag`; `PsycheTag` aliases the historical `PersonalityTag` |
| Graphs | `src/world/graphs.py` — Physical, Cyber, Social, Story; Astral remains deferred |
| Existing scene procedures | `docs/tabletop/` and `docs/rules/SCENE_TYPES_1184.md` |

No new resolver, no automatic tag effect, no Astral Graph.

## 9. Cross-references

- [#1261 Astral Body](ASTRAL_1261.md) — the procedure when projection actually happens.
- [#1164 scene and tag architecture](../design/DRAFT_GRAPH_SCENES_1164.md) — scene types and graph links.
- [#1178 world graphs](../rules/WORLD_GRAPHS_1178.md) — the four graph families.
- [#1280 Eclipse Phase inspiration](../rules/EP2_CONVERSION_1280.md) — optional ideas, not a second system.
- [Scene types](../rules/SCENE_TYPES_1184.md) — the procedures that read these tags.

## 10. What this document does not do

- It does not implement an Astral Graph, a PSI power list, a new skill or a new dice procedure.
- It does not rename serialized fields or break existing `PersonalityTag` saves.
- It does not make Astral Tags true by fiat: they are facts the table agrees to, and their source
  still matters.
- It does not decide the open playtest questions above.

## What the code adds to this page

`src/rules/scene_tags.py` carries the five families and two open questions the text above raises, as fields rather
than as advice:

* **`PsycheTag.duration`** — `enduring` or `temporary`. *Protective of sources* endures across cases; *shaken after the
  ambush* passes. A word, not a timer: nothing expires a tag by itself and nothing rolls for it.
* **`AstralTag.domain`** — `perceive`, `attempt` or `change`, the three the author named. A fourth kind of claim belongs
  in a new family; the field is closed so it cannot be widened by accident.
* **`register_family(name, meaning)`** — the list is open in practice, not only in prose: a sixth family can be added by
  name, and it must come with a one-line meaning.

`src/world/narrative_tags.py` keeps the richer per-character record (leverage, behaviour under pressure, taboo) and
projects it onto the portable tag with `to_family_tag()`, so a scene carries the short form while the store keeps the
detail. Tests: `tests/test_tag_families_1283.py`.
