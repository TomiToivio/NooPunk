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

## Helsinki setting templates (#1141) — drafts awaiting authoring

Four agent-written **templates**, not canon. Each has headings, one deliberately fictional example per
category, `<-- Tomi writes below -->` placeholders, and its own open decisions. Fill them in, replace the
examples, or delete them; the examples are scaffolding.

| document | concern | rules basis |
| --- | --- | --- |
| [`HELSINKI_WORLD.md`](HELSINKI_WORLD.md) | setting-wide context the campaign needs | CWN *Creating Your Dystopia* (pp. 106–130) |
| [`HELSINKI_CITY.md`](HELSINKI_CITY.md) | the city, its districts, and the Physical/Cyber/Astral model | CWN *The City* (pp. 196–217) |
| [`HELSINKI_FACTIONS.md`](HELSINKI_FACTIONS.md) | local actors that take faction turns | SWN Revised *Factions* (p. 211; assets pp. 219/221/223) |
| [`HELSINKI_FACES_XENOBESTIARY.md`](HELSINKI_FACES_XENOBESTIARY.md) | people in the street and non-human encounters | CWN *Faces On the Street* (p. 180); SWN *Xenobestiary* (p. 193) |

They do not replace the author's [`GREATER_HELSINKI_2045.md`](GREATER_HELSINKI_2045.md) or
[`ZONES.md`](ZONES.md), and they do not decide anything those files leave open.

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

## Issue #1141: Helsinki author-first city worksheets (NOT canon)

**Phase 1 only.** Four agent-authored, non-canonical example templates await Tomi's writing and explicit approval. Do **not** implement these examples in the tabletop rulebook, the engine-neutral Python library, or Evennia before the separate Phase-3 authorization.

- [The World: themes, setting context, district index, megacorps, gangs, NPCs](HELSINKI_WORLD.md)
- [The City: history, authorities, district sheets, Physical/Cyber/Astral site layers](HELSINKI_CITY.md)
- [Local Factions: SWN faction goals, Force/Cunning/Wealth assets and turn worksheet](HELSINKI_FACTIONS.md)
- [Faces in the Street / Xenobestiary: ordinary people and four NHI encounter taxonomies](HELSINKI_FACES_XENOBESTIARY.md)

These link to, and **never supersede**, Tomi's existing [Greater Helsinki government draft](GREATER_HELSINKI_2045.md) and [ZONES](ZONES.md). [Issue #1141](https://github.com/TomiToivio/NooPunk/issues/1141) tracks the gates.
