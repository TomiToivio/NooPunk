# NoöPunk: Etsivä Romppainen ja Uusi Paradigma

**A cyberpunk noir detective interactive-fiction story set in Helsinki, 2045 — not a full role-playing game.**

NoöPunk is my way of thinking through three changes that may converge by 2045: artificial general intelligence, non-human intelligence, and a new account of consciousness. The game is small on purpose. You are **Etsivä Harri Romppainen**, a grounded investigator working cases shaped by those changes. You collect evidence, interview people, follow contradictory leads and decide what to do. The metaphysics stays in the background until a case earns it.

[Play the prototype](#play-the-prototype) · [Read the story](NooPunk-Story/README.md) · [Why this changed](docs/adventure/PIVOT_1310.md) · [Historical RPG archive](NooPunk-RPG/README.md) · [Current development tracker (#1310)](https://github.com/TomiToivio/NooPunk/issues/1310)

> **Why the change?** The old full-RPG ambition became almost absurd in scope. A complete RPG would have to carry ordinary cyberpunk, the whole Noösphere side of the setting, and three overlapping Physical/Cyber/Astral layers — before anyone got to play a story. The RPG is now a paused archive. The adventure is the project.

## Why NoöPunk exists

This is a personal and philosophical project before it is a product. I am trying to make sense of my own paradigm shift: a turn toward idealism and **quantum-information panpsychism**, and the suspicion that intelligence, non-human agency and consciousness are all being re-described at once. Fiction, play, humour and detective work are how I explore that uncertainty — not a way to prove a metaphysics.

The three shifts are real public debates, not one settled story:

| Shift | The question | What the game takes seriously |
| --- | --- | --- |
| **AGI / ASI** | What is intelligence, and who controls it? | Acceleration, existential risk, augmentation, labour, corporate and state power. |
| **UFO / UAP / NHI** | Are we alone, and what counts as non-human intelligence? | Disclosure politics, human intermediaries, competing explanations, **Jacques Vallée's** less narrowly extraterrestrial reading. |
| **Consciousness / PSI** | What is consciousness? | Idealist and panpsychist philosophy — especially **Bernardo Kastrup**, **Donald Hoffman** and **Federico Faggin** — and PSI as a speculative application inside the fiction. |

The **Telepathy Tapes** are part of the current popular conversation, not scientific confirmation of telepathy. My expectation that all three will develop substantially by 2045 is a **personal forecast and creative premise**, not a claim of scientific consensus. The fiction keeps four things apart: established technologies, live research, contested claims and outright extrapolation.

**The central proposition:** three simultaneous challenges to the prevailing picture of intelligence, non-human agency and consciousness — experienced by institutions and ordinary people who still have to go to work. NoöPunk is about the social and political consequences: ideological struggle, radicalisation, competing narratives, and the ways governments, science, media, corporations, religions and neighbours respond.

LaclauGPT-informed discourse and ideology analysis is a **storytelling lens**, not a mandatory computational engine. The detective can be sceptical, indifferent or wrong; the case can end without a cosmic answer.

## The adventure

- **Title:** *NoöPunk: Etsivä Romppainen ja Uusi Paradigma*.
- **Format:** a short, old-fashioned text-based detective interactive fiction; a possible later science-fiction novel.
- **Setting:** Helsinki, 2045, after repeated AGI, PSI/consciousness and UAP/NHI controversies. **The catastrophic NHI Crisis of older lore has not happened.** Extraordinary phenomena reach the player through witnesses, intermediaries, institutions, ideologies and evidence.
- **Protagonist:** Etsivä Harri Romppainen. Police/Europol-style investigation, OSINT, interviews, dossiers, clues and meaningful choices — not a chosen-one arc.
- **Play loop:** receive a case; review leads; visit a few Helsinki locations; interview people; inspect records and objects; record testimony, hypotheses, contradictions and leads; choose what to do; live with the outcome.
- **Tone:** cyberpunk noir with a little absurdist humour. Start with one small investigation; let the three shifts emerge through character conflict and contradictory evidence.

The prototype is deliberately small: a Story/Scene graph, an Investigation/Clue graph, simple social tags, locations, case state, choices, save/load and an inspectable history. There are no skill trees, tactical combat, universal PSI/cyberspace rules or mandatory simulation pipeline. Optional small faction/social or hacking modules can come later; neither is required to finish a case.

## Why the full RPG is paused

The old ambition was not one game. It was several:

- the ordinary **cyberpunk** side could run on any competent cyberpunk RPG;
- the **Noösphere** side — UFO/NHI, PSI, idealist and panpsychist metaphysics — would need extensive new rules;
- **Physical, Cyber and Astral** layers overlap; identities, agents, evidence and consequences cross between them;
- the global setting, factions and ideologies add another universal simulation.

Building all of that before telling one detective story displaced the actual creative goal: writing and playing. **`NooPunk-RPG/` is preserved as a paused archive and is not being developed.** CWN, Evennia/MUD, cross-plane rules and a fully integrated LaclauGPT simulation are not the current game or a mandatory roadmap. Historical material remains available through clearly marked archive links.

## The three tracks

| Track | Role | Authorship |
| --- | --- | --- |
| **`NooPunk-Story/`** | The interactive-fiction script: scenes, dialogue, clues, choices, branching outcomes and case arcs. May later become a novel. | `Story/` is **Tomi's**, agent read-only. Agents may build adapters from author text; they do not write the manuscript. |
| **`NooPunk-Simulator/`** | The playable adventure plus optional small world/faction simulation support. | `Paper/` is **Tomi's**, agent read-only. |
| **`NooPunk-RPG/`** | Paused full-RPG archive. | Untouched by agents unless Tomi explicitly reactivates it. |

The pivot is recorded in [`docs/adventure/PIVOT_1310.md`](docs/adventure/PIVOT_1310.md). The current story-first tracker is [#1310](https://github.com/TomiToivio/NooPunk/issues/1310).

## Play the prototype

From the repository root:

```sh
python3 NooPunk-Simulator/Code/adventure.py
```

Use numbered choices; `notebook` shows evidence and provisional hypotheses; `save PATH` and `load PATH` persist a run; `quit` exits. The shipped case is a **synthetic development fixture**, not Tomi's story and not canon. When an author-written script exists, [`story_adapter.py`](NooPunk-Simulator/Code/story_adapter.py) converts its documented Markdown format into case JSON while preserving source attribution.

Read the current adventure notes in [`NooPunk-Simulator/Code/ADVENTURE.md`](NooPunk-Simulator/Code/ADVENTURE.md).

## Reality, claims and fiction

NoöPunk does not ask you to accept its metaphysics. It asks what people do when their institutions, evidence and categories stop agreeing. The fiction treats AGI, NHI and PSI as mainstream scientific and regulatory realities **inside the story**; that does not make any real-world claim true. Contested phenomena stay contested; personal philosophy stays personal; the detective can investigate without converting.

## Repository map

- [Story](NooPunk-Story/README.md) — author-owned manuscript and adaptation boundary.
- [Simulator](NooPunk-Simulator/README.md) — the playable adventure and optional small simulation modules.
- [Paused RPG archive](NooPunk-RPG/README.md) — preserved, not a current roadmap.
- [Design pivot](docs/adventure/PIVOT_1310.md) — why the project changed.
- [Campaign planning draft](docs/campaign/CAMPAIGN_01_EUROPOL_ROOKIE.md) — historical/background material, not the first playable story.
- [Prompt archive](Prompts/README.md) — substantial author design prompts, kept for reuse.

**NoöPunk = Noösphere + Cyberpunk.** The name remains; the scale changed. The next world is still up for grabs. You have to live in this one while you argue about it.
