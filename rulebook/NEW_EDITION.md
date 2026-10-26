> **Current mechanics (2026-10-26):** [Without Number baseline v1](WITHOUT_NUMBER_BASELINE.md) supersedes conflicting historical stats, dice and skill rules below. Preserve setting and characters; existing software still requires migration.

# NoöPunk RULEBOOK

## Humanity Is No Longer Alone

*The future of humanity is no longer human.*

**The year is 2045. Humanity has survived the greatest paradigm shift in its history. Reality itself has changed.**

The NHI Crisis shattered humanity's understanding of its place in the universe. We are no longer alone, no longer the most intelligent beings on Earth, and perhaps no longer masters of our own minds.

Hostile superintelligences, both extraterrestrial and artificial, threaten human civilization. Rogue artificial minds pursue incomprehensible goals. Alien infiltrators walk among us. Meanwhile, mysterious and seemingly benevolent extraterrestrial **Zookeepers** offer protection, guidance, and the possibility of a radically different future. But what do they really want?

Humanity is changing just as rapidly. Artificial intelligence, cybernetics, genetic engineering, and psionics are transforming our species into a multitude of humans, cyborgs, transhumans, and posthumans. The boundaries between human, machine, alien, and consciousness itself are dissolving.

In the face of existential threats, humanity has united under the **United Nations**. But political unity does not mean ideological consensus. Rival factions struggle to determine humanity's deep future: resist the transformation, control it, or embrace the emergence of a new civilization.

Three great paradigm shifts define the age:

- **AGI: Artificial General Intelligence.** The creation of minds beyond human intelligence, promising abundance and threatening extinction.
- **NHI: Non-Human Intelligence.** Contact with extraterrestrial and other mysterious intelligences, overturning humanity's understanding of reality and its place in the cosmos.
- **PSI: Psionics and Consciousness.** The discovery that mind and reality are stranger, more interconnected, and potentially more powerful than modern science imagined.

**NoöPunk** is a New Weird science-fantasy role-playing game and political strategy simulation about humanity's struggle for survival, transformation, and control over its own destiny.

Play as an individual investigating the impossible, or as a faction shaping the future of civilization. Explore a world where every technological breakthrough becomes a political crisis, every existential threat creates new ideologies, and every answer raises deeper questions.

**The old world is ending. The next one is still up for grabs.**

*Setting note: 2045 depicts the developed NHI Crisis era. The earlier strategy campaign begins around 2027, before these outcomes are settled, allowing players to shape the future rather than treating it as inevitable.*


**First edition: Narrative-focused tabletop role-playing game**  
**Status:** Playtest foundation. Only explicitly approved principles are fixed; unresolved mechanics are clearly identified.

## 1. Your character: six attributes

Every NoöPunk character has six attributes. They describe *how a character approaches the world*, not predetermined character classes.

**The base system is the *Without Number* shape** — author direction, 2026-10-26: *use CWN/SWN/AWN/WWN for everything; we will modify later*. The attributes are therefore the family's six, rated **3–18**, used the way that family uses them:

| Attribute | Modifier | What it describes |
|---|---|---|
| **STR** Strength | 3 → −2 · 4–7 → −1 · 8–13 → +0 · 14–17 → +1 · 18 → +2 | Physical prowess, melee, carrying, brute force |
| **DEX** Dexterity | same bands | Speed, evasion, manual precision, reaction, initiative |
| **CON** Constitution | same bands | Hardiness, enduring injury, tolerating cyberware |
| **INT** Intelligence | same bands | Memory, reasoning, technical skill, general education |
| **WIS** Wisdom | same bands | Noticing, judgement, reading a situation, intuition |
| **CHA** Charisma | same bands | Commanding, charming, being taken seriously |

Attributes work alongside **separately rated learned skills**, rated **level 0–4** — level-0 is basic competence, and a character without even level-0 takes **−1**. A check is `2d6 + attribute modifier + skill level ≥ difficulty`, on the ladder **6 · 8 · 10 · 12 · 14**, with situational modifiers of **−2 … +2** and aid worth at most **+1**. Saving throws are `1d20 ≥ 16 − level − the higher of the two listed attribute modifiers`, with a natural 1 always failing and a natural 20 always succeeding.

The values live in [`data/rules/wn_core.json`](../data/rules/wn_core.json), the implementation in [`src/rules/wn_core.py`](../src/rules/wn_core.py), and the contract in [docs/rules/WN_BASE_SYSTEM.md](../docs/rules/WN_BASE_SYSTEM.md).

The setting's earlier six attributes (**FIT / REF / INT / SOC / CYB / PSY**) are the *concepts* this sheet still describes — fitness, reflexes, intelligence, social presence, cybernetic affinity and psyche — and they survive as skills, Edges and fictional permissions rather than as attribute names. That migration is deliberately unfinished: its steps are listed as M1–M9 in the base-system document. Do not interpret **WIS** or **PSY** as automatically granting **PSI**: paranormal abilities require their own permissions.

**Still open by design:** the action economy (3 AP per exchange vs the family's Move + Main round), combat and injury numbers, cyberware tolerance, and advancement values. Playtest them; do not assume a number because a source book prints one.

## 2. What the game is about

You are a newly graduated **UNSA agent** assigned to a Helsinki investigative team with a long and unusual history. Your background, skills, beliefs and chosen call-sign affect how you approach the job. The setting is a reconstructed world after the NHI and rogue-ASI crises. You investigate strange occurrences while navigating institutional demands, human relationships and uncertain evidence.

NoöPunk's first edition emphasizes **investigation, conversation, character Psyche, relationships, choices and consequences**. It draws design inspiration from *Citizen Sleeper* and *Disco Elysium* without copying their rules. It includes genuine decisions under risk (Gamism) and a consistent world with limits on action and knowledge (Simulationism). Tactical-grid combat is deferred to a later optional expansion inspired by *Shadowrun: Dragonfall*.

## 3. Playing a scene

The players and game master describe a situation, what each character knows, and what they hope to do. Ask:

1. **What do you want?** A lead, a confession, someone's cooperation, a moment of safety, an understanding of yourself?
2. **How do you act?** Talk, examine evidence, consult a colleague, cross-reference records, navigate Cyber, seek a PSI perspective or withdraw?
3. **What could change?** Evidence, trust, time, exposure, obligations, Psyche or the direction of the case?

An ordinary action can proceed without a roll. A consequential uncertain action should lead to a meaningful new situation, including on failure. **Never make an essential clue depend on one successful check.** Different approaches can uncover different aspects of the same event. Keep observations, interpretations and established facts distinct.

*Example:* A witness reports a silent sphere over Helsinki. An empathetic interview may establish trust; comparing timestamps may reveal inconsistencies; network records may support a physical observation; an unsettling psychic impression remains an interpretation rather than conclusive proof. A colleague can respectfully disagree.

## 4. Relationships are a central system

The protagonist has evolving social relationships with **every regular companion and important NPC**. Companions also form and change relationships with one another. Shared experiences, trust, loyalty, respect, care, disagreement, professional duty and ideological conflict can affect the next scene and subsequent cases.

A relationship is **not just an approval number**. Characters have independent priorities and may disagree, withhold help, offer assistance, reconcile or act without the player's permission. Important conversations and actions should have continuity. Do not invent universal romance, loyalty or numerical relationship rules at this stage.

Your initial team includes **Laura Falk (“Minerva”)**, **Dr. Harri Romppainen (“Dirty Harry”)**, **Sebastian Virtanen (“Ukuli”)** and **Laura Univaara (“Hecate”)**. The PC chooses their own call-sign. Falk and the PC are Academy newcomers; the other three are veterans of Ö-Mappi, the Supo-origin team transferred to UNSA. The full character brief is [#264](https://github.com/TomiToivio/NooPunk/issues/264).

## 5. Psyche is a central system

The **PC and other party members** have changing inner lives: feelings, motivations, exhaustion, hopes, fears, convictions, self-image, uncertainty, coping, dreams and personal transformation. These shape decisions and dialogue over multiple cases.

Thoughts and inner voices are **perspectives, not infallible facts**. Emotional distress is never a shortcut to declaring someone unreliable, and trauma is not a simplistic punishment. Characters can recover, seek support, set boundaries or revise deeply held ideas. Psyche is psychological experience; extraordinary PSI phenomena require independent evidence and permissions.

*Example:* An apparently successful investigation leaves Falk fearful for civilians, Univaara exhausted by competing duties, and Romppainen convinced an official report obscures a deeper pattern. The player must choose how to respond to each person, not merely whether to mark the case closed.

## 6. Investigation and time

Investigation is the core adventure structure: briefing, witnesses, evidence, competing hypotheses, field or remote inquiry and debrief. A case can progress through several leads; missed opportunities create new complications instead of ending the game. Time, deadlines, recovery, responsibilities and long-running projects may produce meaningful choices. Their **precise clocks and resource rules remain undecided**.

## 7. Physical, Cyber and Astral

The same world can be experienced through three interacting realities: **Physical** (bodies, places and material evidence), **Cyber** (devices, communication and networked systems), and **Astral / Noöspace** (extraordinary psychic experiences and interactions, where available).

Access does not imply omnipotence. A remote Cyber contact needs a communication pathway; an Astral impression need not establish a material fact; projected characters do not simultaneously gain unrestricted bodily action. **Social interaction and Psyche operate across these realities**, rather than needing a separate physical dimension.

## 8. Conflict and danger

Conflicts may be interpersonal, institutional, digital, psychic or physical. The first edition resolves them through clear stakes, choices, consequences and lightweight uncertainty procedures once approved. There is **no mandatory battle grid, extensive positioning or tactical encounter economy**. Violence is possible and consequential, but not the default solution.

## 9. A first UNSA case

Start with a briefing at the local UNSA HQ, investigate a witness account, follow at least one Cyber or Astral lead where access permits, and return for a debrief. Other agents may accompany you or provide plausible remote support. The outcome should change both **case knowledge** and **relationships/Psyche**. Use the existing *First Day in Ö-Mappi* source as a reference, reconciling its earlier introductory framing with the current UNSA Academy protagonist.

## 10. Editions and source material

The next expansion may add **deeper Gamist/Simulationist tactical gameplay** inspired by *Shadowrun: Dragonfall*: tactical combat, builds, equipment and positioning. These are optional later additions to the same narrative world, not first-edition prerequisites.

The complete historical rulebook and all supporting documents remain available via [the frozen pre-#265 archive branch](https://github.com/TomiToivio/NooPunk/tree/archive/pre-265-full-rulebook-2026-10-10). The [migration register](docs/rulebook_consolidation/NARRATIVE_EDITION_MIGRATION.md) records sources and deferred work. Existing research, setting material and contributors' work remain valuable and retrievable.

**Authority:** [#262](https://github.com/TomiToivio/NooPunk/issues/262), [#263](https://github.com/TomiToivio/NooPunk/issues/263), [#264](https://github.com/TomiToivio/NooPunk/issues/264), [#265](https://github.com/TomiToivio/NooPunk/issues/265). Unresolved details are intentionally not presented as finished rules.
