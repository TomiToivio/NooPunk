# NoöPunk as fiction, social-science writing and playable simulation (source: #1037)

<!--
PROVENANCE: transcribed from the author's own issue text, unedited in substance.

STATUS: EXPLORATORY. This is creative direction, not a locked specification, and not authorization to change
the architecture. Specifically, per the source: it does not authorize replacing the Evennia-first direction,
unlocking the CWN rules core, or forcing a premature book/game production plan.

AUTHORSHIP: Finnish fiction is Tomi's. Agents may help with English implementation, structure, editing and
adaptation. Do not write the prose for him, and do not treat this file as a brief to do so.
-->

# Brainstorming: NoöPunk as literature, RPG and social-science simulation

> **Status: exploratory / creative direction, not a locked specification.** Notes from a November 2026 brainstorming conversation. Preserve the author's voice and leave room for experiments.

## 1. The two long-standing ambitions

Tomi originally learned programming roughly 10–20 years ago to pursue two complementary goals:

1. **Build a social data-science pipeline:** now represented by **LaclauGPT**, for analyzing real-world discourse, political identities, ideologies, actors, and networks.
2. **Combine RPGs with computational social science:** now represented by the **NoöPunk MUD**, a playable fictional society with agents, institutions, ideology, networks, and emergent social interactions.

Both are also *writing* ambitions:
- **LaclauGPT:** academic and methodological nonfiction, research papers, and potentially a nonfiction book.
- **NoöPunk:** speculative nonfiction/futurology, *in-universe* social-scientific nonfiction, fiction, and playable RPG storytelling.

The long-term connection is between **empirical social science** (observe and explain society) and **generative social science** (simulate possible societies, explore mechanisms and let humans inhabit the simulation). These are complementary projects, not the same codebase. Simulated plausibility must not be confused with empirical validation.

**Core idea:** coding and writing should reinforce each other, rather than writing merely documenting software or software replacing writing.

## 2. One world and story across two media

**The same Romppainen/UNSA story can be developed as both prose and an interactive RPG campaign.** This is desirable, not redundant.

- Write a short scene, episode, report or story; adapt it into an Evennia quest, dialogue, clue, NPC, location or event.
- Conversely, let interesting simulated encounters, faction dynamics and play sessions suggest new prose scenes.
- Share canon, characters, Helsinki locations, timeline, worldbuilding and investigations; adapt pacing, agency and endings to the medium.
- Don't mechanically transcribe the book into the game or force every prose story to become a quest.
- Keep authorship of Finnish fiction with Tomi; agents can help with English implementation, structure, editing and adaptation. The initial game can retain its established Finnish/Finglish approach.
- Write small pieces independently of implementation. **Finishing a story must never require finishing another software subsystem first.**

A book (or linked collection) and a MUD campaign might thus become two versions of the same universe and partially the same stories, each expanding the other.

## 3. Literary voice: humorous pulp + serious social-scientific speculation

Tomi has long written journalism, academic and technical nonfiction easily, but experienced writer's block with *serious* fiction. Humorous **Etsivä Romppainen** stories were the exception. **Do not try to cure that by forcing solemn literary fiction.** Let comedy and parody remain the main fictional voice.

The original Etsivä Romppainen drew on **early Stewart Home**, Situationism and détournement: postmodern stylistic collage, intentional bad pulp, genre parody, exaggeration and ironic reuse of clichés. **Quentin Tarantino** offers another comparison for playful genre recombination, dialogue and shifts of register. **Philip K. Dick** contributes ontological uncertainty, paranoia, mundane encounters with metaphysics and absurdity. These are points of reference, not templates to imitate mechanically.

Three registers can coexist within the same work:
1. **Humorous Romppainen detective pulp:** deliberately excessive, absurd, dialogue-heavy, occasionally parodying detective stories, cosmic horror, cyberpunk, conspiracy fiction and bureaucratic thrillers.
2. **Serious fictional nonfiction:** sociological accounts of the NHI Crisis, UNSA research reports, historical analyses, futurology, intelligence assessments, essays on consciousness, technology, ideology, social change and extraterrestrial political economy.
3. **Documentary / Situationist collage:** intercepted messages, news, fake advertisements, memos, faction propaganda, fragments of interviews, reports and official forms.

The fictional world, its politics and its philosophical questions may be treated seriously even when the **characters and institutions are ridiculous**. Serious theory can sit next to intentionally trashy detective fiction. The juxtaposition is a feature.

Possible framing: *a serious social-science-fiction universe told partly through an absurdist detective comedy*; potentially a fragmentary postmodern anti-novel, linked short-story collection, or episodic novel.

## 4. Romppainen: continuity of character

**Important clarification from Tomi:** Romppainen's personality has *not* fundamentally changed from the original Etsivä Romppainen stories. The NoöPunk incarnation is simply **older, more experienced, more balanced and mature**, while retaining the characteristic humorous outlook, eccentricity and recognizable core personality. Do not rewrite him as an unrelated grimdark cyberpunk hero or strip away his original comic sensibility.

As an UNSA inspector, he can confront cosmic horrors and profound epistemological puzzles while dealing with absurd Helsinki bureaucracy, colleagues, petty crimes, bad coffee and institutional incompetence. The comedy should emerge from character and situation, not only one-liners.

## 5. ADHD-friendly, mosaic-like writing structure

Rather than requiring one huge linear plot, create an **episodic, fragmentary mosaic**:
- Romppainen mysteries and adventures (e.g. short 1,000–3,000-word stories).
- Short scenes and conversations (even 200–800 words).
- Standalone faux-academic texts, UNSA dossiers, historical chapters and futurological essays.
- Microfragments: adverts, headlines, propaganda, overheard dialogue, brief memos.
- Larger arcs may connect the fragments, but **each fragment need not advance a master plot**.
- Write in whichever order interest and energy support; brief, finishable units are a strength, not a defect.

A humorous detective chapter can follow a totally serious sociological paper about the post-NHI political order. The form itself can reflect fragmented media, discourse and the experience of a world after ontological rupture.

Potential playful working title: **“Etsivä Romppainen ja ontologisen kriisin yhteiskunnalliset seuraukset”** (illustrative, not approved final title).

## 6. MUD direction and audience

A classic text-only MUD may have a niche audience, but the goal is not merely to reproduce a traditional MUD. **NoöPunk is an inhabitable social-science simulation with RPG mechanics.**

Proposed principle: **multiplayer-ready by architecture, single-player first in playable content, simulation-first in design.**

- **Near term:** a fully playable single-player UNSA campaign and side quests with no mandatory human/LLM GM.
- **Underlying architecture:** Evennia persistent multiplayer world, permitting multiple human and LLM player characters later. Shared actor/action interface; human, scripted and LLM actors obey the same rules.
- **Simulation:** Mesa-style agent-based simulation of relationships, organizations, networks, institutions and factions; LaclauGPT-inspired ideological/discourse mechanics; selective LLM NPC reasoning rather than an LLM call for every NPC every tick.
- **Later:** shared multiplayer sandbox, expanded playable factions, human/LLM players and GMs, emergent institutional conflict and strategy.
- A shared persistent world and a private/instanced campaign can coexist to prevent multiplayer activity from breaking authored investigations.
- **Rules remain locked:** CWN/SWN/WWN/AWN-based OSR core, with GUMSHOE-inspired investigative and PbtA-inspired Noösphere/ontological-apocalypse overlays, plus modular faction/ideology systems; do not rewrite the baseline rules for literary experiments.

## 7. Possible graphical presentation without abandoning Evennia

While text remains especially suited to detailed dialogue and simulation, a **modest retro pixel-art browser frontend** could expand the audience without requiring a full Godot rewrite.

Explore (not commit to):
- 8-bit-inspired, 16×16 or 32×32 tile maps of Helsinki and simple sprites.
- Character portraits, dialogue panes, clickable clues, character sheets and social network maps.
- Agents, properly licensed open-source/commercial assets and selectively commissioned freelance art.
- Retain **1970s psychedelic retrofuturism / Mœbius-influenced sensibility**, avoiding generic 1980s neon cyberpunk.
- Keep the Python/Evennia world and simulation independent of graphical presentation; terminal/text mode should remain viable.

## 8. Shared workflow between writing, game and research

A possible virtuous cycle:

**Read / research → write an essay or fictional report → create a Romppainen episode → adapt it into an investigation → observe human/agent play → generate new questions and scenes → write again.**

Research content should remain careful about where documented empirical claims end and fiction/speculation begins. Game events can inspire hypotheses but do not establish real-world findings.

The game, literary world and social-science framework could share structured canon metadata (character, location, institution, timeline, faction, scene, quest) without forcing prose into code-shaped templates.

## Open brainstorming questions

- What is the first *small* Romppainen episode that works independently as a short story **and** a playable UNSA case?
- How can a literary scene translate into choices and consequences without losing its comic timing?
- Should the first book be linked short stories, a faux-UNSA document collection, or a hybrid?
- What minimal structured canon format lets prose and Evennia scenes cross-reference without becoming bureaucratic overhead?
- Could a browser-based pixel-art interface improve accessibility without distracting from text and simulation?
- How might LaclauGPT-derived *abstract* discourse/network patterns seed fictional factions while clearly separating actual research data from fictional content?

### Guiding principles

> **Write in the voice that actually works: humorous Etsivä Romppainen.**
>
> **Use serious nonfiction-style passages for the social-scientific and futurological depth.**
>
> **Keep pieces short and recombinable.**
>
> **Tell some of the same stories in prose and the MUD. Let coding and writing improve each other.**
>
> **Maintain continuity of Romppainen's character: older and wiser, still Romppainen.**

This issue is for exploration and creative direction, **not** authorization to replace the Evennia-first architecture, unlock the CWN rules core, or force a premature book/game production plan.
