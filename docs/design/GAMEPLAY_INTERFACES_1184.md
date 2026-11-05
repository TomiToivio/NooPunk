# Gameplay interfaces and rules architecture (#1184)

> **Status: design summary, authoritative for interface boundaries.** It consolidates
> [#1184](https://github.com/TomiToivio/NooPunk/issues/1184) and defers to the implementation
> records it cites. It changes no CWN rule and introduces no new game engine.
>
> **Companions:** [four graph layers](FOUR_GRAPH_IMPLEMENTATION_1178.md) (what a node is, per family),
> [graph scenes draft](DRAFT_GRAPH_SCENES_1164.md), [Python graph interface plan](GUI_PYTHON_GRAPH_1184.md),
> [shared interfaces](ISSUE_502_SHARED_INTERFACES.md), [CWN core](CORE_VS_MOD_MATRIX_897.md).

## 1. Genre, in one paragraph

**NoöPunk is apocalyptic cyberpunk science fiction.** Cyberpunk, science fiction and the
post-apocalyptic are its constituent modes; detective noir, satire, horror, psychedelic weirdness and
ontological shock are *tones and techniques*, not competing genre claims. It is **not a fantasy RPG**
and does not need WWN: CWN + SWN + AWN are the source families, and PSI/Magick is a
science-fictional/ontological phenomenon rather than a reason to import a fantasy magic system. The
1970s psychedelic retrofuturist surface stays; the fantasy headline goes.

## 2. Invariants

1. **CWN is the immutable core.** Characters, skills, checks, hacking, combat and standard actions
   follow *Cities Without Number*. Nothing here re-balances it.
2. **One world state, many interfaces.** Physical, Cyber, Social and Story graphs reference the same
   entities; the interfaces are views, not engines.
3. **Truth is not knowledge.** World truth, source claims, collected evidence, player knowledge and
   working hypotheses are five different things (§5).
4. **Tags are small.** Social/Goal/Personality tags carry fictional state and simple modifiers, must be
   cheaper than CWN rules, and must work on a paper sheet and in code.
5. **An interface never invents a mechanic.** Consequential uncertainty is always resolved by CWN.
6. **Tabletop, text CLI and the Evennia web client stay viable** against the same Python library.
   Visuals are an option, never a requirement.
7. **No tactical grid in the MVP.** CWN's abstract spatial model is enough.

## 3. Interfaces

| Interface | Inspirations | What the player does | Rule boundary |
| --- | --- | --- | --- |
| **Investigation / OSINT** | *Orwell*, *Song of Farca*, *Blade Runner* (1997) | Search records, messages, media, dossiers; collect evidence; compare claims; unlock leads and interviews | No investigation-point economy. Restricted systems use **CWN hacking** |
| **Dialogue / interrogation** | *Silicon Dreams*, narrative RPGs | Ask, present evidence, challenge contradictions, extract testimony, documents and admissions | Social/Personality/Goal tags set context; **CWN Talk** resolves risk. **No emotion meters, no lie detector, no interrogation minigame** |
| **Cyber** | *Hacknet*, *Midnight Protocol*, *DROP - System Breach* | Move an avatar through a system graph, find access, act on devices | **CWN hacking rules, programs and constraints**; the graph is topology, not a new subsystem |
| **Physical exploration** | *Disco Elysium*, *Citizen Sleeper*, *Dragonfall* | Locations, encounters, dialogue, consequences | CWN creation, advancement and resolution; movement over the Physical graph |
| **Action** *(was "combat")* | *Hill Street Blues*, CWN | Arrests, pursuits, containment, restraint, door entries — very rarely a gunfight | **CWN combat rules** when force is used; abstract distances, no map. See §4 |
| **Dream / astral / anomalous** | *Observer*, NoöPunk fiction | Scripted encounters and scene graphs | Scripted, never a player-operated astral/teleport/precognition simulator |

**GUMSHOE is inspiration, not a package.** Core clues are never gated behind a failed roll: the right
action finds the clue, and CWN rolls decide cost, risk, extra detail and consequences. The player
assembles evidence through interfaces instead of spending investigative points.

## 4. Action scenes, not combat scenes

The scene kind is **Action**. "Combat" survives only as the name of CWN's own rules chapter, which the
action scene *calls* when force is unavoidable.

**Why the rename is not cosmetic.** The old name pulled the design towards an American gunfight
grammar: armed civilians, tactical maps, every case ending in a firefight. NoöPunk is a Finnish police
story. Finnish patrol work is *arrests, searches, pursuits, containment, negotiation, restraint and
paperwork*, in a country where a patrol officer's firearm is a last resort and civilians with assault
rifles are not a normal encounter. The tone reference is **Hill Street Blues**: an ensemble shift, a
radio, procedure, fatigue, jurisdiction and human mess — not a school massacre.

| Action scene | What the rules resolve | NoöPunk texture |
| --- | --- | --- |
| **Arrest** | Surprise, initiative, grappling/restraint, compliance, CWN attack rolls if force is used | Two officers, a stairwell, a warrant that may be wrong |
| **Pursuit** | Vehicle or foot chase as opposed checks and a distance/lead clock; CWN vehicle rules for damage and control | Tram tracks, harbour loading bays, a driver who knows the streets better than the map |
| **Containment** | Positioning on the Physical graph, doors, sightlines, time | Cordoning a block in the rain while the press arrives before the backup |
| **Search / entry** | CWN searches, forced entry, initiative order when it goes wrong | A warrant executed on the wrong flat, and the flat is not empty |
| **Public order** | Restraint, escalation, command decisions | A crowd that is right, a commander who is wrong, a camera recording |
| **Force** | Full CWN combat | Rare, short, consequential; the aftermath is a report, an inquiry and a colleague who will not look at you |

**Design rules.** No civilians with military weapons as set dressing. No tactical map in the MVP. No
new combat subsystem: positioning is graph distance and cover is fictional, as CWN already allows.
Lethality stays CWN's; the campaign's tone rule is that a firefight is a failure state with
paperwork, not a power fantasy.

## 5. Evidence and knowledge model

Five registers, never collapsed:

| Register | Meaning | Visible to the player as |
| --- | --- | --- |
| **World truth** | What actually happened in the fiction | Only through evidence; never narrated as fact by an interface |
| **Source claim** | What a document, witness or faction asserts | A claim card with a source, a date and a confidence |
| **Collected evidence** | What the player holds, with chain of custody | The inventory that can be presented |
| **Player knowledge** | What the player has understood | The investigation graph's revealed nodes and edges |
| **Hypothesis** | What the player has concluded | A player-authored note that can be wrong, and can be *shown* to be wrong |

Rules: evidence may be incomplete, misleading, fabricated or contradictory; a source's claim is never
auto-promoted to truth; interrogations yield statements, contradictions and leads, not emotional
scores; and every case has more than one investigative path, with failed discretionary checks costing
time, access or trust rather than ending the case.

## 6. PSI and Magick

**Magick is PSI and PSI is Magick** — two framings of one phenomenon, not two power systems.

| Source | Use | Player access |
| --- | --- | --- |
| **SWN Psionics** | Disciplines and Psychic Training focus | **Telepathy and Telekinesis only** |
| **AWN Mentalist** | Preferred PSI-flavoured alternative/extension | Only within the Telepathy/Telekinesis scope |
| **AWN Mutant** | Mutants of varied, often unknown origin; a Hybrid is one unproven explanation | **NPC only — PCs may not take it** |
| **CWN Spellcaster** | Magick read in-world as PSI | Reference and NPC/exceptional use; not a route around the PC limit |
| **CWN Summoner** | Summoning read through PSI/Magick ontology | Same |

**Scripted, not selectable:** Astral projection (authored dreams, OOBEs, NDEs, Monroe-style
psychotronics), teleportation, precognition, and the rest of SWN's out-of-scope disciplines.
Psychotronic implants are technology producing PSI effects and obey the same PC restrictions.

**Law of One is lore, not rules.** Densities, polarization and Social Memory Complexes inform history,
factions and how characters *interpret* anomalies. They add no density progression, no polarization
meter and no mechanical requirement. Psionics may be read in-world as the emergence of Fourth Density;
that reading is the fiction's, not the system's.

## 7. Implementation order

1. **One Helsinki Europol rookie case end to end**: OSINT → interview → physical lead → limited CWN
   hacking → report to Romppainen, using existing graphs and simple tags.
2. **Shared evidence/claim/hypothesis representation** plus graph navigation that reveals only what
   the player knows.
3. **Evidence-first dialogue**: present, contradict, unlock; no emotion mechanics.
4. **One resolver**: physical, cyber, social and investigation scenes call the same CWN action
   resolver, and the tabletop/CLI parity tests stay green.
5. **A small rules matrix** documenting PSI access (as above) so no later feature drifts.
6. **Out of scope for v1**: tactical maps, procedural dream/astral systems, full social simulation,
   bespoke investigation subsystems, and any second rules engine.

## 8. Definition of done

The architecture is documented and cross-linked (this page, the graph records, the GUI plan); every
interface names the rule boundary it may not cross; and the first mission can be implemented without
introducing a new rules engine per activity.

## 9. Open questions for the author

1. Which of the four graph views the rookie case *opens* in — case board, or the physical scene?
2. Whether the arrest is the campaign's default climax, or whether some cases end in a report nobody
   reads (the second is more Finnish, the first more playable).
3. Whether a firearm is ever drawn in the first mission. A campaign that goes ten sessions without one
   is a statement; a campaign that never can is a limitation.
4. How much of Romppainen's institutional obstruction is authored versus procedural.
