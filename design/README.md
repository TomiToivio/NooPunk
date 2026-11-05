# Design Workflow

This is the design workflow: 

1) Tomi creates a design document in this directory. 
2) Tomi makes an issue of the document. 
3) Agents implement Tomi's design document. 

## Document Types
There will be several types of documents:
* Day - these documents describe daily events. If there is no daily document that day has no special events. This is for events that will happen regardless of player's progress in the main storyline.
* Character - these are non-player characters of the game world. 
* Mission - these are the scripted missions the PC and his party will perform.
* Interaction - these are dialogues and social encounter scripts. 
* Storyline - this is the main storyline of the game. The storyline proceeds as the character advances.
* Missions - this contains side missions for the player. Some of these could be procedurally generated and repeating. Some are scripted side quests.
* Location - these documents describe locations the character can visit. There are three levels of locations: Helsinki -> UNSA HQ -> Dr. Romppainen's Office
* Rules - these are additional rules to be implemented as mods on top of the CWN rules. These may also describe equipment etc.
* Encounters - this is for random encounters that are not related to the main storyline. 
* Events - this is for random events that are not related to the main storyline.

## Guidelines
* Preserve Tomi's Finnish/Finglish dialogue and descriptions exactly; never translate, edit or normalize them.
* The MUD has one canonical language: Finglish, with no separate localizations (#996). For player-visible material, agents write English-led Finglish with occasional contextual Finnish and other loanwords; never translate Tomi-authored prose. All other agent-written material (including design documents and tabletop rulebooks) remains plain English. See `docs/FINNISH.md`.
* Do one step at a time - do only what is described in the design document. 
* Sometimes dialogues etc. are described in a detailed fashion and you should implement them exactly as described. 
* Sometimes there are more open-ended tasks and you can use your imagination to implement them. 
* You should implement the Python code for NoöPunk MUD. 
* You should add implemented rules, campaign scenarios and lore to the NoöPunk tabletop RPG rulebook. 

## Vocabulary

[`GLOSSARY.md`](../GLOSSARY.md) at the repository root is the canonical vocabulary for player-facing
text. Design documents may use those terms freely; a design document that needs a **new** term should
propose it there rather than assume it.

## Issue #1137: Agent-authored rule proposal drafts (NOT author-approved)

These five *separate* draft documents are available for Tomi's edits and approval. They are **not** the author's binding design files and **must not** be implemented in rulebook/Python without Tomi's explicit later instruction:

- [Psionics: SWN / AWN Mentalist / WWN / CWN Hacking, Astral Projection](../docs/design/DRAFT_NOOPUNK_PSIONICS.md)
- [Psychotronics: QIP, BCI and neurotech](../docs/design/DRAFT_NOOPUNK_PSYCHOTRONICS.md)
- [Bionics: engineered AWN-style biological traits](../docs/design/DRAFT_NOOPUNK_BIONICS.md)
- [Europol rookie character generation and issued kit](../docs/design/DRAFT_NOOPUNK_EUROPOL_CHARACTER_GENERATION.md)
- [Personality, Goals and Reputation tags](../docs/design/DRAFT_NOOPUNK_CHARACTER_TAGS.md)

[Tracking issue #1137](https://github.com/TomiToivio/NooPunk/issues/1137). The author's [BIONICS.md](BIONICS.md) remains intact and authoritative for author decisions; these are proposals only.

## Issue #1141: Human-readable Helsinki setting worksheets — Phase 1 reworked, Phase 2 awaiting author

**Four distinct documents, one canonical worksheet per concern.** These are agent-authored, **human-readable Markdown writing templates**, not setting canon. Each contains natural-language fictional examples, writing prompts and clearly marked **Your version (Tomi writes here)** sections. No YAML, JSON or Python editing is required. Replace example content only when Tomi authors it; examples are never approved lore.

| Author worksheet | Single owner of | Source basis |
| --- | --- | --- |
| [HELSINKI_WORLD.md](HELSINKI_WORLD.md) | Campaign-facing world context, themes and short indexes, without repeating city records | CWN *Creating Your Dystopia* |
| [HELSINKI_CITY.md](HELSINKI_CITY.md) | Helsinki city, district sheets, Physical/Cyber/Astral layer and location records | CWN *The City* |
| [HELSINKI_FACTIONS.md](HELSINKI_FACTIONS.md) | Local factions with SWN turn stats, goals and assets | SWN Revised *Factions* |
| [HELSINKI_FACES_XENOBESTIARY.md](HELSINKI_FACES_XENOBESTIARY.md) | Encounter-facing people and NHI records, not duplicate character biographies | CWN *Faces On the Street*; SWN *Xenobestiary* |

**Document deduplication:** The same subject must not be independently defined in multiple worksheets. Keep its full record in the owning document and use a link/stable ID in the others. Before creating another Helsinki document, check [the document register](../docs/DOCUMENT_REGISTER.md), existing `design/` and `docs/world/` documents and related open issues/PRs. Consolidate overlapping *agent-authored* content in its owner, preserving all unique material and attribution. Do not edit, relocate, delete, or overwrite author-written `design/ZONES.md`, `design/GREATER_HELSINKI_2045.md` or other author drafts without explicit authorization.

**Phases and gates:** Phase 1 is complete as a set of prose worksheets: every section has a written
example, a visible place to write your own version, and no YAML, JSON, field names or internal identifiers. Phase 2 (Tomi writes and approves authored content) is pending. Phase 3 (tabletop rulebook, engine-neutral Python and Evennia integration) requires separate explicit authorization after Phase 2; **never implement example content as canon**. Existing [Greater Helsinki government draft](GREATER_HELSINKI_2045.md), [ZONES](ZONES.md) and [Europol campaign authority](../docs/world/EUROPOL_HELSINKI_1114.md) retain their established precedence. See [issue #1141](https://github.com/TomiToivio/NooPunk/issues/1141).

## Issue #1164: Graph rules and scene authoring proposal (NOT author-approved)

[Read the five-graph CWN-first design proposal](../docs/design/DRAFT_GRAPH_SCENES_1164.md). It maps Physical/Cyber/Astral/Social/Story graph schemas, a Series→Episode→Scene authoring format, GUMSHOE-lite investigation adapters, GoalLog reuse and bounded PSI Verb×Target permissions to current code and rules. This is an agent draft for Tomi to edit. No implementation is authorized; the original [graphs README](graphs/README.md) remains the author's unchanged source.

## Issue #1168: Crisis narrative method and Nordic secret history (reviewable memo, NOT canon)

[Read the design memo](../docs/design/MEMO_CRISIS_NARRATIVE_NORDIC_1168.md). It records the three authorial modes, *consistent consequences / flexible seriousness*, the CWN+AWN activation boundary, the 50/25/25 reaction heuristic, three competing 1946 contact models and the checked real-world Ghost Rocket/Hessdalen record. The memo is a proposal for Tomi to edit, approve or reject; it does not change the timeline, rulebook, world documents or code. `rulebook/7_TIMELINE.md`, `rulebook/20_FIRST_CONTACT_AND_PSI_AWAKENING.md`, `docs/world/` and the author's [ZONES](ZONES.md) remain authoritative.
