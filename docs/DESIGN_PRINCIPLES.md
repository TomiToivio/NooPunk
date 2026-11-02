# NoöPunk design principles and portable architecture

**Status: binding project direction (2026-11-03).** Applies to tabletop rules, Python gameplay libraries, mods, engines, AI integrations and documentation. This supersedes older Godot-first or Evennia-coupled architecture instructions where they conflict. See also issue #1006 (rules lock), #1025 (CWN parity), #1037 (single-player first), #1042 (LaclauGPT mod) and #1045 (AWN inventory).

## 1. Never alter the published rules baseline

- **Cities Without Number (CWN) is the immutable primary RPG rules system.** Do not modify its attributes, character generation, skills, checks, combat, hacking, advancement or other baseline mechanics to accommodate a mod or engine.
- **Stars Without Number (SWN), Worlds Without Number (WWN), and Ashes Without Number (AWN)** provide additional published rules/toolkits when needed: especially SWN psionics and later faction turns, WWN occult/fantasy options, and AWN survival, stress and regional crisis systems.
- Preserve each source's rules faithfully in the corresponding implementation. Resolve overlaps through explicit, documented choice of applicable subsystem; never silently merge incompatible variants or change CWN.
- The term *core library* means the implementation of published rules, **not** permission to redesign those rules. Keep source provenance and a rules-coverage matrix; respect the licenses and avoid redistributing non-open deluxe text.

## 2. Add mods, never rewrite CWN

- NoöPunk-specific mechanics live in **separate optional mods**. Mods should be CWN- and OSR-compatible and may be inspired by PbtA (Noösphere and ontological apocalypse), GUMSHOE (investigations), LaclauGPT (ideology, discourse and relations), and small narrative tag systems.
- **Prefer simplicity over adding another full rules engine.** Even lighter tags, clocks, prompts and narrative procedures are welcome; their simplicity does not authorize changing a published CWN roll or character rule.
- Each mod declares what it adds, where it hooks into CWN, its tabletop procedure, its input/output state, any dependencies, and how to turn it off. A mod may resolve its own narrative question more simply than CWN, but must not silently override a CWN procedure.
- Example optional modules: investigation/clues, Noösphere/PbtA clocks, ideological/faction tags, AWN regional crisis, and a **NoöPunk Tarot deck** with documented card meanings and paper-play procedures (high-priority design objective).

## 3. Tabletop RPG is the reference implementation

- **Everything essential must be playable with a rulebook, pencils, paper character sheets, ordinary dice and, where a mod specifies them, cards or tokens.** A NoöPunk-specific Tarot deck is permitted and strongly desired, but provide a printable/proxy or lookup procedure for accessibility.
- No required LLM, server, database, network connection, live agent or bespoke screen. Digital automation implements the tabletop procedure; it does not invent a different mandatory ruleset.
- Mods may also support standalone board games, card games and miniature wargames. The SWN faction-strategy layer may eventually need such components. These are optional expansions, not blockers for the initial campaign.
- Maintain tabletop rules and automated implementations in parity through shared examples, hand-playable test scenarios and character sheets.

## 4. Python rules-as-library, not engine-as-rules

**The CWN/SWN/WWN/AWN rules and NoöPunk mods must be implemented as importable Python libraries independent of the game engine or UI.** Do not bury domain rules in Evennia typeclasses, Pygame handlers, Concordia agents, web routes or terminal prompts. Reuse one canonical implementation across all presentations.

Recommended *target architecture* (illustrative; inspect current files before migration):

```text
noopunk/
  rules/
    cwn/                 # faithful immutable CWN baseline
    swn/                 # selected published SWN rules
    wwn/                 # selected published WWN rules
    awn/                 # selected published AWN rules
  mods/
    investigation/
    noosphere/
    ideology/
    crisis/
    tarot/
  campaign/
    state.py             # engine-neutral character/world/quest state
    actions.py           # domain commands and results
    quests/              # single-player UNSA campaign and side quests
  adapters/
    console/             # reference plain-text Python CLI
    evennia/             # persistent MUD frontend (correct spelling: Evennia)
    concordia/           # LLM/social simulation integration
    pygame/              # optional graphical standalone frontend
```

- **Dependency direction:** frontends/adapters → application/campaign → rules and mods. Rules/mods must not import frontend packages.
- Use a narrow, typed domain API: actions such as `roll_check`, `resolve_attack`, `apply_effect`, `advance_scene`, `inspect_clue`, or `draw_tarot`, and deterministic state transitions/events. Examples are conceptual, not preexisting API promises.
- Inject dice/RNG and clocks to allow reproducible tests. Persist portable versioned game state; adapter-specific sessions/maps/database models stay outside the canonical domain schema.
- Support **scripted, human, and LLM-controlled actors** via the same legal action/validation interface. An LLM may propose narrative or actions but cannot bypass the rules or become mandatory to finish a case.
- Console, Evennia, Concordia and Pygame must be able to call the same Python packages; avoid forks or copy-pasted combat, skill or mod implementations. An Evennia server may host a campaign, but it does not own the rules.
- Existing Godot code is legacy/reference, not the sole rules authority. If a Godot edition is revived, it needs a deliberate adapter/interop strategy rather than a second, drifting implementation.
- Check each third-party framework's actual extensibility before promising integration; the portable rules API is the stable contract.

## 5. Delivery order: playable single-player first

1. **First playable milestone:** a complete single-player UNSA investigation/campaign slice with character creation, checks, combat where relevant, NPCs, clues, quests, progression, save/load and side quests. It must work offline in the **plain-text console**, without human or LLM GM.
2. Validate faithful CWN operation and selected SWN psionics, then the minimum optional mods that improve that first campaign. Publish a usable tabletop version of the same scenario.
3. Connect the same library to **Evennia** for the text MUD, preserving campaign behavior; add optional Concordia LLM NPCs/GM tools and a Pygame UI only when they add value.
4. **Later**, add richer factions/ideology strategy, SWN faction turns, board/card/wargame modules, multiplayer sandbox, other player factions and deeper social simulations. None may delay the first completed campaign.

These are priority phases, not separate rule systems or an excuse for another engine rewrite. Engines and UIs are replaceable; the Python rule/mod libraries and tabletop specification endure.

## 6. Acceptance tests for every rules/mod change

- [ ] Published CWN baseline unchanged; supplementary SWN/WWN/AWN behavior explicitly sourced and scoped.
- [ ] Mod is additive, optional, and either compatible with CWN or a strictly simpler standalone procedure that does not override CWN mechanics.
- [ ] Can be described and played with physical tabletop tools (and includes a paper-play example).
- [ ] Same domain-rule unit tests work headlessly, with no Evennia/Concordia/Pygame or network dependencies.
- [ ] Console reference adapter can execute the feature.
- [ ] Save/load, seeded randomness, and rule/event results are compatible across adapters as appropriate.
- [ ] Implementation and documented rulebook/character sheet remain synchronized.
- [ ] Work advances the single-player playable slice or is explicitly marked deferred.

**Invariant:** **Locked CWN + selected published Without Number additions + optional lightweight NoöPunk mods + portable Python libraries + interchangeable interfaces + tabletop parity.**
