# NoöPunk literature and cross-media storytelling (#1037)

**Status:** approved direction for exploration, not a production commitment. No game mechanics changed. See [character and party design](ROMPPAINEN_PARTY_1038.md) (#1038).

## Purpose and scope

NoöPunk is simultaneously (1) an author's speculative-fiction world, (2) an RPG set in that world, and (3) a generative social-science simulation. Its counterpart, LaclauGPT, is an empirical research pipeline studying real political discourse, ideological formation, institutions and actor networks. Keep the projects independently functional; exchange abstract models and research questions, not live personal data or an unvalidated claim that a fictional simulation reproduces society.

**Literature is not game documentation.** Writing and coding are creative peers. A case may be a Romppainen story and an interactive UNSA mission, each told through different points of view and media-specific agency. Never force a prose scene into an interactive cutscene unchanged.

## Three interleaving narrative registers

1. **Humorous Etsivä Romppainen pulp:** situationist détournement, early Stewart Home-style pastiche and intentionally overblown genre clichés, irreverent conversations and satirical police procedural scenes. Quentin Tarantino's recombination of genre conventions is another reference.
2. **Fictional nonfiction:** academically styled UNSA sociology, classified intelligence assessments, political-economic analyses, histories and speculative futurology. These may be written quite seriously, but must remain clearly labeled as in-world invented documents.
3. **Documentary collage:** ads, news excerpts, bureaucratic forms, propaganda, email exchanges, memos, intercepted messages and street gossip, juxtaposed with the other two registers.

PKD-like ontological uncertainty and consciousness questions belong in the world even when the dialogue is comic. Serious subject matter does not obligate serious-fiction prose. Pastiche is not permission to copy another author's protected passages.

## Fragment-first authoring

Prefer independent, finishable artifacts: 200–800-word conversations, short detective stories, fictional academic abstracts, case reports and tiny found-text fragments. The collection can grow into an episodic book or mosaic/anti-novel; no fragment is required to advance one overarching plot. There is no mandated writing cadence.

**Suggested content record, lightweight Markdown front matter, not a required schema:**

```yaml
id: case-kallio-001
status: idea
medium: [prose, mud]
point_of_view: romppainen
location: helsinki-kallio
spoiler_level: opening
linked_case: null
author: Tomi
```

Avoid generating machine-authored Finnish or “correcting” Tomi's drafts. Follow [the canonical Finglish policy](../FINNISH.md): agents write internal docs in English; player-facing texts are mostly English/Finglish while Tomi's Finnish/Finglish is preserved verbatim.

## Cross-media case workflow

1. Write any standalone literary fragment, or document an investigative situation.
2. Identify the **fictional truth**, what characters know, and what the reader/player may learn.
3. Adapt into a deterministic Evennia scene: initial hook, core clues, alternate investigative routes, choices and consequences. Avoid unintentional softlocks; do not require an LLM GM.
4. Reinterpret, rather than transcribe, the scene for PC + Laura. Romppainen may be the protagonist of prose but the senior NPC in the game.
5. Record optional play-derived ideas for later prose; do not canonize emergent simulation outputs without author review.

**First vertical slice proposal:** one humorous Romppainen case consisting of one brief prose scene, one fictional UNSA dossier, and one playable rookie-perspective investigation. Do not build a book publishing platform before the first case is playable.

## Technical/creative boundaries

- Evennia and single-player UNSA casework are the engineering priority; browser pixel-art rendering is optional and should be independent of the game rules.
- Keep CWN/SWN/WWN/AWN rules intact; GUMSHOE, Noösphere/PbtA, faction and social systems are modular overlays.
- Multiplayer-capable architecture, solo-first content; later NPC simulation via Mesa, LLM actors and other players must not break deterministic campaign scenes.
- Retro pixel art (e.g., simple 16×16 or 32×32 assets) is a **potential** interface, not a return to a Godot-first architecture. Keep the 1970s psychedelic retrofuturist aesthetic; check asset licensing and creator attribution.

## Short acceptance checklist

- [x] Distinct prose, fictional nonfiction and collage modes documented.
- [x] Romppainen as authored fiction protagonist vs. tabula-rasa game PC distinguished.
- [x] Finnish/Finglish authorship and spoiler conventions preserved.
- [x] Concrete small cross-media case workflow defined.
- [ ] A first authored story and playable case created, reviewed and tested (future work, not presumed done).

Related: #1037, #1038, #950.
