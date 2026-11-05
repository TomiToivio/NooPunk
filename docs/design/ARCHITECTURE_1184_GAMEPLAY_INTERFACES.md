# Gameplay interfaces and rules architecture (#1184)

> **Status: architecture summary — design only, no rules change.** This consolidates decisions that are
> already made across #1164, #1178, #1054, #704 and #728. It does not rewrite CWN, and it does not
> introduce a subsystem.
>
> **Companion:** [`PYTHON_GUI_PLAN_1184.md`](PYTHON_GUI_PLAN_1184.md) — how the graphical front end is
> actually built.

---

## 1. Genre definition

**NoöPunk is apocalyptic cyberpunk science fiction.**

- **Primary genre:** apocalyptic cyberpunk SF.
- **Constituent modes:** cyberpunk, science fiction, post-apocalyptic fiction.
- **Not a fantasy RPG.** Fantasy, science-fantasy and New Weird are *tones and techniques*, never
  headline genre labels, and none of them justifies importing fantasy mechanics for symmetry with the
  other Sine Nomine games.
- **WWN is not required.** CWN + SWN + AWN are the relevant source families. Psychic and "magickal"
  effects are science-fictional and ontological phenomena, not a reason to add a ritual system. The
  existing CWN Spellcaster and Summoner Edges remain available in their agreed PSI/Magick role.
- The 1970s psychedelic retrofuturist aesthetic, the satire and the eeriness all stay.

---

## 2. Design invariants

1. **CWN-first.** Characters, skills, checks, hacking, combat and standard actions follow Cities
   Without Number. Its core is not altered.
2. **One world state, several interfaces.** Physical, Cyber, Social and Investigation views reference
   the same entities and relations. Canonical world facts stay distinct from what the player has
   *found*, *been told* and *suspects*.
3. **Tags are small.** Social, Goal, Personality and situational tags carry fictional state and small
   modifiers. They must fit on a tabletop sheet and in the computer game, and must not grow into a
   second economy.
4. **Interfaces are not rules engines.** They decide how a player sees and acts on the world. CWN
   resolves consequential uncertainty.
5. **Tabletop, text CLI and Evennia web client remain viable** against the same Python library. Rich
   visualisation is optional, never required.
6. **CWN's abstract combat works without a tactical map** for the MVP.

---

## 3. The graphs

| Graph | What it represents | Edges mean | Resolved by |
| --- | --- | --- | --- |
| **Physical** | world → city → district → location → room | routes, doors, containment | CWN movement, exploration, **action** |
| **Cyber** | systems, services, access | network routes, rights, control | CWN Hacking |
| **Social** | people and local factions | trust, obligation, ideology, goal | CWN Talk/Connect/Lead + tags |
| **Investigation** | evidence, claims, sources, hypotheses | supports, contradicts, attributes | CWN Notice/Know/Admin + evidence model |
| **Story** | series → episodes → scenes | prerequisites, branches | GoalLog and scene flags |

**One graph, several projections.** The Investigation view is a *player-facing view of discovered
evidence*, not a second copy of every canonical entity.

---

## 4. Gameplay interfaces

| Interface | Inspirations | What the player does | Rule boundary |
| --- | --- | --- | --- |
| **Online investigation / OSINT** | *Orwell*, *Song of Farca*, *Blade Runner* (1997) | Search records, messages, dossiers, media; collect evidence, compare claims, unlock leads | No investigation-point economy. Restricted systems use CWN Hacking |
| **Dialogue / interrogation** | *Silicon Dreams*, narrative RPGs | Ask, present evidence, challenge contradictions, extract testimony | **Evidence-focused, not an emotion simulator.** No meters, no lie detector, no minigame |
| **Cyber / hacking** | *Hacknet*, *DROP - System Breach*, *Midnight Protocol* | Navigate a graph of systems, links and access controls | **CWN Hacking rules only**; the reference games' mechanics are not imported |
| **Physical exploration** | *Disco Elysium*, *Citizen Sleeper*, *Shadowrun: Dragonfall* | Locations, encounters, dialogue, decisions, tags | CWN character creation, advancement, action resolution |
| **Action** | *Hill Street Blues* (see §5) | Arrest, pursue, contain, enter, de-escalate, call backup | CWN combat and opposed checks; abstract spatial relations; **no tactical grid** |
| **Dream / Astral / anomalous** | *Observer*, NoöPunk fiction | Scripted encounters and scene graphs | Authored scenes only. No general-purpose player-operated astral simulation |

**GUMSHOE is an influence, not a package.** Essential clues are not gated behind arbitrary failed
rolls: appropriate actions find core clues; CWN rolls govern risk, cost, extra detail and consequence.

---

## 5. Action scenes, not combat scenes

**The rename is the point, not a synonym.** #1184 renames the scene kind; CWN combat rules still resolve
it, but the fiction is Finnish policing in a functioning EU capital, not an American firefight.

**What an action scene is:** an arrest that goes wrong; a pursuit through Kallio at 2 a.m.; a door that
has to come off its hinges with a warrant in hand; a crowd that will not move; a man with a knife in a
stairwell; a vehicle stop where the risk is a traffic lane, not a rifle.

**What it is not:** armed civilians with assault rifles, mass-casualty set pieces, or gunfights as the
default punctuation. Firearms exist, are carried, and are **exceptional and consequential** — drawing
one changes the scene, the paperwork and the officer's career.

**Design consequences:**

- **Abstract positions, not a grid.** `engaged`, `near`, `far`, `cover`, `contained` — enough for CWN's
  abstract combat, and no tactical map is required for the MVP.
- **A pressure track, not just hit points.** Escalation, bystanders, time, and the arrival of backup
  matter more than damage. Officers still have CWN hit points; the *scene's* tension is measured by
  what is about to go wrong.
- **Pursuits are graphs.** Road and tram nodes, closing distance, hazards, radio coverage. A chase is a
  path problem under time pressure, not a driving minigame.
- **Every action produces paperwork.** Arrests, use of force and pursuits generate institutional
  consequences that persist into later scenes; that is a NoöPunk signature and a Hill Street Blues one.
- **De-escalation is a legitimate winning move**, and the rules must make it worth attempting.

---

## 6. Evidence and knowledge model

Five things stay distinct, always:

1. **World truth** — what actually happened.
2. **Source claims** — what a document, witness or faction asserts.
3. **Collected evidence** — what the player holds, with provenance.
4. **Player knowledge** — what the player has actually understood.
5. **Hypotheses** — what the player currently believes, explicitly provisional.

Evidence may be incomplete, misleading, fabricated or mutually contradictory. **A source's claim is
never promoted to truth by being collected.** Interrogations yield statements, documents, contradictions
and leads — never an emotional score.

Multiple investigative paths must exist; a failed discretionary check costs something and does not
dead-end the case.

---

## 7. PSI, Magick and player access

**Magick is PSI and PSI is Magick** — different framings of related phenomena, never competing systems.

| Source | Use | Player access |
| --- | --- | --- |
| **SWN Psionics** | disciplines and Psychic Training | **Telepathy and Telekinesis only** |
| **AWN Mentalist** | PSI-flavoured alternative, preferred inspiration | Only within the Telepathy/Telekinesis scope |
| **AWN Mutant** | Mutants of varied or unknown origin | **NPC-only**; players may not take it |
| **CWN Spellcaster** | Magick read as PSI | In the reference; not a route around PC limits |
| **CWN Summoner** | Summoning read through PSI ontology | In the reference; not a route around PC limits |

**Scripted, never selectable:** Astral Projection (authored dreams, OOBEs, NDEs, psychotronic events),
teleportation, precognition, and other high-impact disciplines.

**Psychotronic implants** are technological means of producing PSI effects and obey the same limits. A
narrative exception is a scripted event, not a permanent grant.

**Law of One is lore, not rules.** Densities, polarisation and Social Memory Complex may inform history,
cosmology and interpretation. They do **not** produce a subsystem, a Density progression or a meter.

**Mutant vs Hybrid.** *Mutant* is the general term for AWN Mutant Edge NPCs; *Hybrid* is one possible —
and unprovable — explanation. Mutation alone establishes neither PSI, NHI ancestry nor infiltration.

---

## 8. Implementation order

1. One Helsinki Europol rookie investigation end to end: OSINT → interview → physical lead → limited
   CWN hacking → report to Romppainen.
2. Shared evidence/claim/hypothesis representation and graph navigation.
3. Evidence-first dialogue and interrogation.
4. All scenes call the **same** CWN action resolver; tabletop and CLI parity retained.
5. A small PSI/Edge availability matrix (above) in code and in the rulebook.
6. Explicitly deferred: tactical maps, procedural dream systems, full social simulation, custom
   investigation subsystems.

---

## 9. Definition of done for this issue

- The design is documented and cross-linked from the issues it consolidates.
- Interface and rule boundaries are explicit, including the Action rename.
- The first mission can be implemented without a new rules engine per activity.
- The Python graphical front end has a concrete plan and a buildable first milestone
  ([`PYTHON_GUI_PLAN_1184.md`](PYTHON_GUI_PLAN_1184.md)).

---

## 10. Cross-references

- [`DRAFT_GRAPH_SCENES_1164.md`](DRAFT_GRAPH_SCENES_1164.md) — scene kinds, including the Action rename
- [`FOUR_GRAPH_IMPLEMENTATION_1178.md`](FOUR_GRAPH_IMPLEMENTATION_1178.md) — graph implementation
- [`../../design/graphs/README.md`](../../design/graphs/README.md) — graph model
- [`../../design/graphs/RULES.md`](../../design/graphs/RULES.md) — rules per graph
- [`PYTHON_GUI_PLAN_1184.md`](PYTHON_GUI_PLAN_1184.md) — the front end
