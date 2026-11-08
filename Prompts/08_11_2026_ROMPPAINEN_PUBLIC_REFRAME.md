# Prompt: reframe NoöPunk publicly as Etsivä Romppainen ja Uusi Paradigma

- **Date:** 2026-11-08
- **Topic:** issue #1322
- **Source:** Tomi's own issue text in NooPunk, <https://github.com/TomiToivio/NooPunk/issues/1322>
- **Archive status:** original author prompt, retained verbatim. It states the current public framing; the archive itself
  grants no further scope and modifies no canon.

## Original prompt (verbatim issue text, transport formatting normalised)

## Goal

Update the root `README.md` and the published GitHub Pages site so the public-facing introduction explains **why NoöPunk exists** and clearly communicates the **new, much smaller creative goal**:

# NoöPunk: Etsivä Romppainen ja Uusi Paradigma

A **cyberpunk noir detective interactive-fiction story/adventure** set in Helsinki in 2045, not an attempt to build a complete tabletop/computer RPG.

This documentation issue complements [#1310](https://github.com/TomiToivio/NooPunk/issues/1310), the current story-first development tracker. **Use the title above in the updated public-facing presentation**; #1310 still carries the earlier working title *Etsivä Romppainen ja ei-inhimillinen älykkyys*. Align relevant story-title references deliberately, without rewriting Tomi's author-only manuscript or inventing canon.

## Philosophical and personal motivation

Explain in approachable **first-person authorial terms** that NoöPunk is a creative way to explore and process the author's **own philosophical paradigm shift and ontological shock**, notably a turn toward **idealism and quantum-information panpsychism**, along with the sense that three profound changes may converge by **2045, in some form**:

1. **AGI/ASI: What is intelligence?** Rapid real-world progress in AI, potential general/superintelligence and human augmentation, with accelerationist, doomer and other social responses.
2. **UFO/UAP/NHI: Are we alone, and what counts as nonhuman intelligence?** The ongoing UAP/disclosure controversy and movements; the author takes NHI seriously and finds **Jacques Vallée's** less narrowly extraterrestrial interpretation especially interesting. Distinguish real disclosure-related events, claims and investigations from independently established NHI explanations.
3. **Consciousness/PSI: What is consciousness?** The author's developing **idealist / quantum-information-panpsychist** philosophy, with **Bernardo Kastrup, Donald Hoffman and Federico Faggin** as significant influences; PSI as a speculative technological application within the fictional scenario. The **Telepathy Tapes** can be mentioned as part of the current popular conversation, not scientific confirmation of telepathy.

The author's belief that all three will develop substantially by 2045 is a **personal forecast and creative premise**, not a statement of scientific consensus. Present philosophical alternatives seriously and charitably while keeping the distinction between established technologies, live research, contested claims and fictional extrapolation.

**Central thematic proposition:** three simultaneous challenges to prevailing understandings of **intelligence, nonhuman agency and consciousness**, experienced at an individual and societal level. NoöPunk explores their **social and political consequences**: ideological struggle, radicalization, competing narratives and responses by governments, science, media, corporations, religions and ordinary people. LaclauGPT-informed discourse/ideology analysis remains a storytelling lens, not a mandatory computational engine.

This project is also about making sense of uncertainty through **fiction, play, humor and detective investigation**, not proving the author's metaphysics. The investigator can be skeptical or indifferent and uncover competing explanations.

## Explain explicitly why a full RPG is paused

Be candid that the old RPG ambition became **almost absurd in scope**:

- The ordinary **Cyberpunk** side could run on any competent existing cyberpunk RPG system.
- The **Noösphere** side (UFO/NHI, PSI, idealist/panpsychist metaphysics) would demand difficult and very extensive new rules.
- **Physical / Cyber / Astral** layers overlap; agents, identities, interactions and evidence can cross them. A universal simulation of all that, alongside the ideologies, factions and global setting, is not a realistic prerequisite to telling one detective story.
- More worldbuilding, rulebooks and mechanical systems have repeatedly displaced the actual creative goal: writing and playing the story.

**Current decision:** preserve `NooPunk-RPG/` as a paused archive, with no new RPG implementation work. Avoid presenting CWN, Evennia/MUD, cross-plane rules or a fully integrated LaclauGPT simulation as the current game or mandatory future roadmap.

## Present the smaller adventure clearly

- **Title:** *NoöPunk: Etsivä Romppainen ja Uusi Paradigma*.
- **Format:** short, old-fashioned **text-based cyberpunk detective interactive fiction**, with possible later adaptation into a science-fiction novel.
- **Setting:** Helsinki **2045**, after repeated **AGI, PSI/consciousness and UAP/NHI-related paradigm-shift controversies**, **before** the full catastrophic NHI Crisis of older lore. Extraordinary phenomena are encountered mostly via human witnesses, intermediaries, institutions, ideologies and investigative evidence.
- **Protagonist:** Etsivä Harri Romppainen; grounded police/Europol-style investigation, OSINT, interviews, dossiers, clues and meaningful choices.
- **Storytelling:** start with one small investigation, introduce the three shifts gradually through character conflicts and contradictory evidence, and preserve noir uncertainty and a bit of absurdist humor.
- **Implementation:** reuse the already working lightweight interactive-fiction CLI / simple Story, Choice, Clue and Case state. Optional small social/ideology graphs may support a specific scene. **No full RPG, required PSI mechanics, world-spanning simulation or universal Astral/Cyber/Physical engine.**
- **Authorship boundary:** `NooPunk-Story/Story/` and `NooPunk-Simulator/Paper/` remain **Tomi-only, agent read-only**. Don't create or edit story prose there. Keep `NooPunk-RPG/` untouched.

## Documentation tasks

- [ ] Audit the current root `README.md` and the source of the published GitHub Pages site; identify their actual entry points/build configuration before editing.
- [ ] Rewrite the **opening public introduction and motivation** around the three paradigm shifts and the author's philosophical motivation, in readable language for non-developers.
- [ ] Make the new title and **detective interactive-fiction scope** prominent on both README and GitHub Pages.
- [ ] Explicitly describe why the full RPG is paused and why the overlapping Physical/Cyber/Astral Noösphere is **story background**, not a rules implementation mandate.
- [ ] Resolve **contradictory legacy copy** in the README and relevant Pages navigation: old “primary game = Evennia MUD,” “CWN-first active RPG,” “2045 after the NHI Crisis,” “full computer RPG and social simulation,” and similar claims must not masquerade as the current roadmap. Preserve old designs through clearly labeled archival links where useful.
- [ ] Keep a compact **Play the prototype / Read the story / Historical RPG archive** navigation; verify actual paths and current CLI command against the repo.
- [ ] Maintain an accessible distinction between *real-world developments*, *personal philosophical interpretation*, *contested claims* and *NoöPunk's fictional 2045 premises*.
- [ ] Verify Pages build/navigation and README links, then deliver documentation changes in a focused PR.

## Acceptance criteria

A new reader of either landing page should quickly understand **(a)** why the author is exploring the three ontological shocks, **(b)** that *Etsivä Romppainen ja Uusi Paradigma* is a **small, story-first cyberpunk detective adventure**, **(c)** why full RPG rules/simulation are paused, and **(d)** how to find or run the current prototype.

**Scope guard:** This issue is about public documentation and framing, not implementing new rules, rewriting author-only story, or redesigning the game. See #1310 for story/adventure implementation.
