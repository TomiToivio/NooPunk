# NoöPunk permanent foundation: issue #897

**Author decision, 2026-10-31.** CWN is the rules *engine*, NoöPunk is its modular science-fantasy / narrative extension, and an imagined **1974** is the production visual language. Supersedes the top-down/tactics-as-primary direction in #848, but **retains its vanilla CWN/SWN rules** and one-Godot-project constraint. Do not interpret a story module as permission to replace core rolls or attributes.

## Source-of-truth matrix

| Domain | Governing rules | New NoöPunk addition | Constraint |
| --- | --- | --- | --- |
| Character, skills, saves, attacks, growth | CWN | Academy background and moral arcs | Preserve six attributes, CWN resolution/advancement |
| Cyberware, hacking, equipment, combat | CWN | Graph interface, dialogue-driven combat scenes | Same rules, different UI |
| Psionics/space/factions | SWN Revised where CWN silent | Noösphere story, UNSA politics | Document source and conversion |
| Otherworld/occult exploration | selective WWN | Noetic locations and encounters | Adapter, not alternate core |
| Survival/crisis | optional AWN | NHI incident survival | Adapter, not alternate core |
| Detective investigations | CWN checks | GUMSHOE-inspired guaranteed core clues, cost/complication on failure | Never replace 2d6 check |
| Social relationships/reputation | CWN social mechanics | Trust, obligations, faction credibility and narrative flags | Mod-only state |
| Ideology and factions | CWN/SWN factions as appropriate | LaclauGPT-inspired discourse, competing identification and antagonism | No mandatory ideological alignment |
| Psyche / ontological shock | CWN/SWN strain/PSI as appropriate | Fictional stress and noösphere exposure | No real-world psychiatric claims |

**Unresolved design choice:** PC active PSI. Tentatively limit PC to passive/minor PSI; retain powerful active PSI for NPCs pending playtesting.

## One-project Godot plan

Canonical: `project.godot`, `scenes/main.tscn`, `godot/core/`, `godot/ui/`, `godot/tests/`. Do not create a second game. Existing top-down missions, hospital case, tactical scenes and saves remain reachable until a tested migration. Temporarily **deprioritize** tactical-grid combat and direct walking.

The intended game loop is **Helsinki location map → discover/investigate/interview → evidence and NPC relationships → choose destination or mission → bring 1–4 UNSA agents → CWN checks / non-tactical encounter / node-link hacking → consequences, reputation, new leads → home or UNSA HQ**.

Start PC: newly graduated, deliberately morally uncommitted UNSA agent. Potential growth includes empathy, idealism, corruption and fanaticism with consequences; Romppainen is a central independent NPC who can sometimes join a party or become controllable. No moral trajectory is the default. Important investigation clues cannot be permanently lost solely because of a failed roll.

## Implementation milestones

1. **Authority**: this decision, README and AGENTS directive; record core-vs-mod source per feature.
2. **Art system**: define original tokens, period typography and legibility rules; build a coherent city map, character sheet and hacking-graph look.
3. **Location prototype**: reuse existing campaign/HQ state and UI, wire Helsinki destinations, discovery, action choices, travel and journal; do not create rival save/state ownership.
4. **Investigation + social mod**: dialogue, clue board, party recruitment/availability, contact/reputation and ideological tracking built on CWN.
5. **CWN character sheet**: attributes, skills, class, equipment, progression; display mod fields separately.
6. **Graph hacking**: route graph node actions through existing CWN cyberdeck/hacking kernels rather than invented roll outcomes.
7. **Non-tactical combat**: apply CWN combat with narrative combat choices and transparent roll results; leave legacy tactical code dormant.
8. **Playable Helsinki vertical slice**: novice UNSA agent, HQ briefing, clue, interview, recruitable agent, node-link hack, encounter, return and saved consequences.

## Verification and migration gates

Each code PR identifies the one canonical module, original CWN/SWN rule authority, any optional overlay, affected saves and executable tests. Run root Godot headless suite, import, scene navigation and save/load before merging. No automated tests for prose/canon. Do not claim a full vertical slice from a planning document. Read `docs/NOOPUNK_BASELINE_848.md` as the historical baseline *except* its superseded top-down UI/vanilla-only extension ban.

## Copyright

Design original UI, original prose, original illustrations and licensed sound/font assets. Cite permitted CWN SRD rules and attribute Worlds Without Number/Stars Without Number where applicable. Inspirations do not grant rights to reproduce film stills, comics panels, game art or commercial recordings.
