# Romppainen's four sides, politics, and the controllable UNSA party (source: #1038)

<!--
PROVENANCE: transcribed from the author's own issue text, unedited in substance.

STATUS: EXPLORATORY. Character and party-design notes, not a locked implementation specification.

RULES OF READING, taken from the source itself:
- Romppainen is the protagonist of the Etsiva Romppainen fiction but NOT the default player character.
- Do not pre-decide his final allegiance.
- Do not turn him into a dour generic intelligence chief, and do not strip the humour.
- The older stories established his personality; the NooPunk version is older, more mature, still him.
-->

# Brainstorm: Inspector Harri Romppainen and the controllable UNSA party

> **Exploratory character and party-design notes, not a locked implementation specification.** Preserve the established CWN-based rules, Evennia-first direction, and initial single-player UNSA campaign. Related literary brainstorming: #1037.

## A. Inspector Harri S. Romppainen: the central authored NPC

**Romppainen is the protagonist of Etsivä Romppainen fiction, but NOT the default MUD player character.** His personality is too established and his experience too great for a tabula-rasa rookie protagonist. He is the PC's boss, mentor, occasional companion, and arguably the most important NPC in the game. In special scripted situations he can become a player-controlled party member.

**Continuity:** Romppainen's underlying personality hasn't changed substantially from the older humorous Etsivä Romppainen stories. The NoöPunk version is older, more experienced, more balanced and mature, but still eccentric, anarchistic, irreverent, inquisitive, and recognizably Romppainen. Do not turn him into a dour generic intelligence chief.

### Four overlapping drives (and social networks)

1. **Revolutionary anarchist — political idealism.** Strongly anti-authoritarian, opposed to exploitation, imperialism, hierarchy and surveillance even when justified by socialist Europe or the survival of humanity. He is politically connected to the EU's democratic-socialist/red-green leadership. Explore a fictional Finnish socialist EU leader inspired by the public political archetype of Sanna Marin, not a claim about the real person's future. She and Romppainen may be long-standing friends or allies, and **it is possible that his UNSA/Europol position partly resulted from political patronage**. This is intentionally ironic: a revolutionary anarchist benefits from connections at the top of the state, yet increasingly distrusts its institutions. Do not assume the governing coalition eliminates authoritarian contradictions.

2. **Academic intellectual — scientific curiosity.** A scientist/psychologist/intellectual compelled to investigate PSI, NHI, consciousness, AI, anomalous cognition, and the post-Singularity world. Access to otherwise inaccessible knowledge may keep him employed even when he finds his institution's politics unacceptable. Curiosity can be a weakness, not merely a virtue.

3. **Investigator — protection and anti-colonial resistance.** Investigates exploitation of humanity by rogue ASI, NHI powers, corporations, human elites etc. This is the part of policing he can justify through his revolutionary ideals: protecting people, especially against domination and colonization. But the institution may gradually equate its own authority with “defending humanity,” causing a moral crisis.

4. **Hedonistic party/street cop — escape from the job.** A veteran investigator who needs to blow off steam in Helsinki's seediest pubs, clubs and underground circles. Relationships with drug dealers, sex workers, underground musicians, criminals and marginalized or bohemian people can be real, complex, reciprocal connections, not merely transactional informant tokens. Explore histories or risks of substance/alcohol dependence or compulsive behavior as a **possibility**, not a mandated checklist of simultaneous addictions or a cheap punchline. Show personal, professional and relational costs without stereotyping these communities.

These four facets provide four partially overlapping NPC networks: political elites/radicals; academics/noetics; UNSA/Europol/people under threat; street-level underworld/nightlife. Trust, secrets, debts, reputation and ideological conflicts could feed the future social simulation.

### Institutional and political contradiction

- A revolutionary anarchist may find working for an increasingly authoritarian **UNSA/Europol** morally intolerable even if socialist Europe is fighting for human survival.
- Romppainen's position is inherently unstable: he could be an internal dissident, protector of civilians, unauthorized investigator, occasional leaker, or eventually an independent investigator. **Do not pre-decide his final allegiance.**
- Speculative geopolitical arc: a democratic-socialist-led EU and Europol are among the few institutions still treating UNSA as a legitimate cooperative authority. They discover that many national UNSA partners are rogue states, failed states, captured administrations or governments in name only. This could precipitate a severe crisis of legitimacy and the fragmentation of UNSA, leaving a European branch as an institutional successor. Not a locked canon outcome.
- Explore the tension between genuine professional talent and political appointments. His EU leader relationship must have consequences and competing loyalties.

## B. Proposed controllable character / party roster

**Important distinction:** “Controllable” means a party member the player may direct within the game's command/AI architecture. It does **not** imply the roster is all present on every mission, or that the NPC loses their own history or personality. Preserve a manageable party size (earlier concept: 1–4 active members) and role-based availability.

### 1. PC — tabula-rasa UNSA rookie (primary protagonist)
- Main player character; personality and politics emerge from choices rather than fixed backstory.
- Human or eventually LLM-controlled through the same rules/action interface.
- Primarily an investigator; can build CWN skills. Do not grant the rookie arbitrarily powerful active psionics.

### 2. Agent Laura Wendt — rookie partner, veteran soldier
- The PC's near-permanent/usually available partner and party companion.
- Rookie **as a UNSA field agent**, but already a trained military/SWAT veteran; determined, capable and heroic.
- Her military background makes her more tactically credible than the PC without turning the story into a military action RPG.
- Strong independent personality and dialogue; not an expendable generic escort NPC.

### 3. Inspector Harri S. Romppainen — boss and major NPC
- Senior inspector, mentor, political/intellectual troublemaker, and recurring narrative anchor.
- **Sometimes** available as a controllable party member for specific missions, not a permanent default companion.
- His experience should be reflected in abilities, contacts and narrative authority, but he must not trivialize player choices or solve every mystery automatically.

### 4. Psionics asset(s) — mission-specific specialist
- Available when investigations/operations genuinely require active PSI.
- **Only the designated psionic asset(s) should have strong active psionics in the party.** PC, Laura, and Romppainen may acquire *latent/passive* psychic sensitivity or use psychotronics, but they must not turn into powerful active psions.
- Useful, bounded *mechanical* powers may include **telepathy** in investigation/interrogation, limited influence/manipulation, and **telekinesis** during combat.
- **Remote viewing, precognition, astral projection and other expansive powers should be pre-scripted scenario/GM events**, not general-purpose unlimited player commands. Their open-ended implications are too hard to implement consistently and they risk destroying mystery design.
- Tie PSI capabilities, costs and limits to the locked CWN/SWN framework and Noösphere overlays; never silently rewrite core psionics rules. If a capability requires a scenario-only restriction, document it as a NoöPunk module.

### 5. Technical asset(s) — specialist support
- Mission-available **netrunner/hacker** when PC capabilities are insufficient.
- Possibly other technical experts, e.g. electronics, drones, sensors, cyberware, forensics or psychotronics.
- Specialists should unlock options or overcome technical bottlenecks, not render the player's own relevant CWN skills irrelevant.
- Consider remote support where bringing a full extra party member would be cumbersome.

### 6. SWAT asset(s) — high-risk tactical support
- Paramilitary (“para”-military) police/SWAT personnel for scenarios that require force.
- **NoöPunk is fundamentally a detective/cop show, not an action movie or tactical war simulator.**
- Combat should be relatively simple, quick, and **extremely deadly**, consistent with CWN/OSR expectations: street brawls, short confrontations, occasional rapid lethal gunfights, strong incentive to avoid combat through investigation and preparation.
- Avoid routinely deploying entire squads in individual CWN initiative. Consider treating a team as a single abstract supporting unit or as off-screen/tactical scene resources where that preserves speed.
- Escalated SWAT deployment should have narrative, political, institutional and reputational consequences.

## C. Party/gameplay principles to brainstorm

- **Default team:** PC + Laura. Romppainen and specialist assets appear by mission and availability; roster size capped/configurable rather than an unwieldy permanent squad.
- **Narrative ownership:** PC is the main decision-maker. Highly skilled NPCs support, disagree and occasionally refuse unlawful/unethical orders; player control is mediated by their expertise, agency and loyalties.
- **Mission preparation:** choose or requisition available specialists based on intelligence and assessed threat; this can become a small investigative-planning system without adding a separate action-game layer.
- **Investigation before combat:** GUMSHOE-inspired clue access, interviews and evidence; technical and PSI specialists supply distinctive ways to approach problems. The same case should have paths that don't require every asset type.
- **Strong PSI rarity is a design constraint:** other three regular characters remain human-scale, and extreme mental/temporal/distant effects remain authored scenes.
- **Danger has meaning:** tactical assets prevent unnecessary deaths but do not turn missions into combat farming.
- **Shared implementation:** all actors use the unchanged CWN-derived base action/rules engine and compatible human/LLM/scripted controllers; special event abilities are explicitly scenario modules.
- **Solo-first, multiplayer-ready:** the roster/companions should function in the first self-running UNSA campaign without a live GM; later human/LLM multiplayer may add ways to control or recruit characters without undermining the narrative canon.
- **Cross-media storytelling:** Romppainen can be the main character in authored fiction and a major NPC in the corresponding playable case, giving two perspectives on the same story.

## Open questions / design spikes

- What are the precise rules for switching to or commanding an NPC party member, and for NPC refusal/autonomy?
- Is PC + Laura + up to two specialists the useful default active-party cap?
- What narrative triggers make Romppainen personally accompany the team?
- How do strong active psionics interact with CWN/SWN limits while keeping remote viewing and precognition scripted?
- Which technical and SWAT abilities should be represented through party actors vs. off-screen support?
- Can a short, lethal combat scene be resolved through normal CWN mechanics rather than a new subsystem?
- How does Romppainen's connection to the socialist EU leader complicate UNSA operations and his political credibility?
- How are addiction, strain, recovery, professional misconduct and street contacts written without glamorization or caricature?

**Goal:** establish a flexible narrative and gameplay blueprint that preserves a blank-slate rookie protagonist, an almost always available Laura, an exceptional but non-dominating Romppainen, and rare mission-specific PSI/technical/SWAT support, while keeping the political satire, social simulation and noir humor alive.

**Related:** #1037 (NoöPunk as literary and social-science writing project).
