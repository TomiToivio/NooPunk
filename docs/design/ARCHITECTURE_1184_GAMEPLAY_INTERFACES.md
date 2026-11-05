# Gameplay interfaces and rules architecture — the #1184 summary

> **Status: design summary, not implementation.** This consolidates decisions that already exist in
> several issues and drafts into one place, so the first mission can be built without inventing a rules
> engine per activity. It changes no rule and no canon. Where it disagrees with an author document, the
> author document wins.
>
> **Related:** #1164 (graph scenes, Physical/Cyber/Social/Investigation/Astral), #1178 (four graphs +
> Edge simplification), #1054 (immutable core, multiple interfaces), #704 (CWN-first balance),
> #728 (computer-game influences). Implementation plan for the graphical client:
> [`GUI_PYTHON_1184_MINIMAL_GRAPH_UI.md`](GUI_PYTHON_1184_MINIMAL_GRAPH_UI.md).

## 1. Genre, stated once

**NoöPunk is apocalyptic cyberpunk science fiction.** Constituent modes: cyberpunk, science fiction,
post-apocalyptic. Satire, detective noir, horror, psychedelic weirdness and ontological shock are
*tones*, not competing genre labels. It is **not** a fantasy RPG, and it does not acquire fantasy
mechanics for symmetry with other Without Number games.

CWN + SWN + AWN are the relevant source families. WWN is not required. CWN Spellcaster and Summoner
Edges remain available in their agreed PSI/Magick role — as expressions of the setting's psychotronics
and psychic phenomena, not as a fantasy magic system.

## 2. One world state, six views, one resolver

There is **one** world state. Interfaces are ways of seeing and acting on it; they are not separate
games with separate rules.

| View | Graph family | What it shows | What the player does | What resolves it |
| --- | --- | --- | --- | --- |
| **Physical** | `physical` | Places, routes, who is where | Move, search, observe, interact, arrest | CWN (skills, saves, combat, movement) |
| **Cyber** | `cyber` | Devices, links, access controls, avatars | Traverse, probe, exploit, defend | CWN hacking (verbs/subjects, programs, access) |
| **Social** | `social` | People, factions, relationships (signed) | Talk, ask, press, ally, betray | CWN Talk/Connect/Command + Tags |
| **Investigation** | *derived* | Evidence, sources, claims, contradictions | Collect, compare, hypothesise, confront | CWN checks for *cost, risk, detail* — never for whether the core clue exists |
| **Story** | `story` | Series → episode → scene, prerequisites | Choose, act, transition | CWN + authored scene logic |
| **Astral** *(scripted)* | scene graph only | Dream/astral/NDE spaces | Explore a scripted space | Authored scene logic — **no player-activated astral power** |

**Canonical facts vs player knowledge is a hard boundary.** The world graph is truth. The investigation
graph is a *player-facing view*: what the character has established, from whom, with what confidence.
The interface must never render a fact the character has not acquired, including by making the absence
of a node conspicuous.

## 3. Interface catalogue — and the boundary each one must not cross

| Interface | Touchstones (#1184) | Boundary |
| --- | --- | --- |
| Online investigation / OSINT | *Orwell*, *Song of Farca*, *Blade Runner* (1997) | Search public records, messages, dossiers, media, databases; collect and compare. **No investigation-point economy.** Restricted systems are entered through CWN hacking. |
| Dialogue / interrogation | *Silicon Dreams*, narrative RPGs | Evidence-focused: ask, present, challenge contradiction, obtain testimony and documents. **No emotion meter, no lie-detector UI, no interrogation minigame.** |
| Cyber / hacking | *DROP - System Breach*, *Midnight Protocol*, *Hacknet* | Navigate a graph of systems and access controls, using **CWN's** verbs, programs and constraints — not the reference games' mechanics. |
| Physical exploration | *Disco Elysium*, *Citizen Sleeper*, *Shadowrun: Dragonfall* | Locations, encounters, dialogue, Tags, consequences; CWN character and resolution. |
| **Action** *(was "Combat")* | CWN + police procedurals (see §5) | CWN combat and abstract spatial relations. **No tactical grid or map required for the MVP.** |
| Dream / astral / anomalous | *Observer*, NoöPunk fiction | Scripted scene graphs. **No general-purpose player-operated astral, teleport or precognition simulation.** |

**GUMSHOE is a design principle, not a mechanics package.** Essential clues are never gated behind a
failed roll; CWN rolls govern risk, cost, extra detail and consequences. The player assembles evidence
through the interfaces instead of spending investigative points.

## 4. Evidence and knowledge model

Five registers, never collapsed:

1. **World truth** — what actually happened (the world graph, invisible).
2. **Source claim** — what a document, witness or database asserts.
3. **Collected evidence** — what the character has actually acquired, with provenance.
4. **Player knowledge** — what the player has read, been told, or inferred (may exceed the character's).
5. **Working hypothesis** — a link the player asserts; can be wrong, and the interface should let it be
   wrong without punishing curiosity.

```
world ──claim──▶ source ──collect──▶ evidence ──infer──▶ hypothesis
                      ▲                                    │
                      └────────── confront / test ──────────┘
```

**Rules that follow from it.** Evidence may be incomplete, misleading, fabricated or contradictory. A
claim is never promoted to truth by being repeated. A hypothesis is a player artefact, not a fact, and
must be retractable. Confronting a witness with a document is a *social action* with a CWN check, not a
UI trick that always works.

**Progress must survive failure.** Failed discretionary checks impose consequences — time, suspicion,
lost access, a relationship — rather than dead-ending the case. Multiple paths to every essential clue.

## 5. Action scenes: why the name changed, and what they are

**Decision (#1184, author's direction): "Combat" becomes "Action".** The scene type names what the
interface shows and what the player does, not a genre promise. In code:
`src/rules/four_graphs.py::SCENE_TYPES` now contains `Action`; `Combat` is refused, so the old name
cannot quietly return as a synonym (`tests/test_scene_types_1184.py`).

**The setting's action register is Finnish police work, not American gunfight cinema.** Finland is not
the United States: patrol officers do not carry rifles, civilians do not, and a scene in which several
people shoot at each other is a national emergency rather than a Tuesday. The touchstone is *Hill
Street Blues*: an ensemble, procedure under pressure, moral ambiguity, decisions that follow you into
the next episode.

| Action scene | What the player is doing | CWN handles | The interesting failure |
| --- | --- | --- | --- |
| **Arrest** | Presence, verbal commands, positioning, restraint, deciding when to go hands-on | Punch/Exert/Talk/Notice, initiative, morale | Excessive force, wrong person, escalation on camera |
| **Pursuit (foot)** | Route choice, obstacles, crowds, calling it off | Exert/Survive, notice, chase procedure | Losing them and lying about it; a bystander hurt |
| **Pursuit (vehicle)** | Speed vs risk, traffic, roadblocks, jurisdiction | Drive, vehicle damage, chase rules | A crash that ends a career |
| **Forced entry** | Warrant, timing, breaching, containment | Exert/Notice/Shoot as last resort | Wrong door; no warrant; someone inside who should not be |
| **Standoff / containment** | Negotiation, time, perimeter, media | Talk/Connect/Command, reaction | Shooting when talking would have worked |
| **Crowd / public order** | Lines, orders, proportionality, recording | Lead/Command, discipline | A baton that becomes a national story |
| **Evidence preservation** | Securing a scene under pressure | Investigation layer | Contamination that loses the case |

**Use-of-force ladder (fiction policy, not a new subsystem).** Presence → verbal → physical control →
less-lethal → firearm. Moving down the ladder is a decision with CWN resolution and institutional
consequences; it is never an automatic upgrade. Firearm use is rare, investigated, and remembered.

**What action scenes must not become.** Not a grid, not a cover-shooter, not an escalation fantasy, and
not a place where the rules reward killing. A scene that ends with nobody shot and the right person in
custody is the *good* outcome, and the design should make that legible.

## 6. PSI and Magick: access policy

Setting principle: **Magick is PSI and PSI is Magick** — different framings of related phenomena, not
independent power systems.

| Source | NoöPunk use | Player access |
| --- | --- | --- |
| SWN Psionics | Psychic disciplines; Psychic Training Focus | **Only Telepathy and Telekinesis** |
| AWN Mentalist Edge | PSI-flavoured alternative worth evaluating; preferred inspiration over SWN breadth | Only within the Telepathy/Telekinesis scope |
| AWN Mutant Edge | **Mutants**, of varied and often unknown origin; many may be Hybrids, but that must be discovered | **NPC only — player characters may not take it** |
| CWN Spellcaster Edge | Magick interpreted in-world as PSI | In the reference; must not become an evasion of PC limits |
| CWN Summoner Edge | Summoning through PSI/Magick ontology | As above |

**Scripted, never selectable:** Astral Projection (authored dreams, spontaneous OOBE, NDE, psychotronic
sessions), teleportation, precognition, and other high-impact effects. Psychotronic implants are
technological routes to PSI and obey the same access policy; a narrative exception is a scripted event,
not a permanent character-sheet grant.

**No Law of One subsystem.** Densities, polarization and Social Memory Complex are lore that explains
the fiction; there is no density meter, no polarization counter, no mechanical progression derived from
them. Psionics is the *fiction's* fourth-density awakening; the *rules* remain published CWN/SWN/AWN.

## 7. Interface independence — the invariant that keeps four clients possible

Tabletop, text CLI, Evennia and the graphical client are **four front doors to one library**.

```
                     ┌──────────────────────────────┐
                     │  domain: rules + world state │
                     │  src/rules, src/world        │
                     └──────────────┬───────────────┘
        ┌───────────────┬───────────┼───────────┬────────────────┐
   tabletop sheet   CLI console   Evennia    graphical client
     (paper)       (session.py)  (commands)   (src/ui)
```

Every front end submits a typed action and receives a typed result; none of them computes a rule. The
enforceable checks already exist (`tests/test_engine_independence_1053.py`, the boundary tool) and the
GUI must be added behind the same wall, not around it.

## 8. Implementation order (from #1184, with checkpoints)

1. **One case, end to end.** OSINT → interview → physical lead → limited CWN hacking → report to
   Romppainen, using existing character and graph systems plus simple Tags.
   *Checkpoint:* the case is playable in the CLI with no GUI.
2. **Shared evidence/claim/hypothesis representation** and graph navigation that reveals only
   player-known data. *Checkpoint:* a test proves an uncollected node cannot be rendered.
3. **Evidence-first dialogue.** Present/find evidence, unlock statements, no emotion mechanics.
   *Checkpoint:* an interrogation that succeeds and one that fails, both without a meter.
4. **One resolver for all scenes**, including action scenes, preserving tabletop/CLI parity.
5. **PSI access matrix documented and enforced** in character creation.
6. **GUI** (separate plan) — optional throughout.

**Definition of done for this issue:** the design is documented and cross-linked, the boundaries are
explicit, and the first mission can be built without a new rules engine per activity.

## 9. Out of scope, explicitly

Tactical maps; procedural dream or astral action systems; full social simulation; a custom investigation
subsystem; emotion or lie meters; an investigation-point economy; anything that changes a CWN procedure.
Sophisticated spatial UI may be added later without touching the rules.
