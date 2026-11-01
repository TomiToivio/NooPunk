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
* Read root [`GLOSSARY.md`](../GLOSSARY.md) before writing or interpreting player-facing dialogue: it is the canonical vocabulary for real Stadin slangi, futuristic NoöPunk slang and universe terminology alike. Reuse Tomi's approved words naturally instead of inventing synonyms, and mark any new term with its category, provenance and spoiler tier so the generated game dictionary stays in step.
* Do one step at a time - do only what is described in the design document. 
* Sometimes dialogues etc. are described in a detailed fashion and you should implement them exactly as described. 
* Sometimes there are more open-ended tasks and you can use your imagination to implement them. 
* You should implement the Python code for NoöPunk MUD. 
* You should add implemented rules, campaign scenarios and lore to the NoöPunk tabletop RPG rulebook. 
