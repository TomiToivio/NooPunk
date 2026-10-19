# #516 — Core RPG design decision packet for Tomi

**Status: FOR AUTHOR DESIGN AND APPROVAL; no new canonical rules here.** Relevant approved crossover baseline: `strategy_game/RULEBOOK.md` (Fate 4dF, four actions, aspects, stress/consequences, **six** individual Fate-rated skills COG/INT/REF/SAV/SOM/WIL; one leader + four agents). Legacy FIT/REF/INT/SOC/CYB/PSY attributes belong to a separate RPG and **must not be silently mixed** with this crossover sheet.

## A documented priority conflict

Issue #516 explicitly requests **50% narrative / 25% gamist / 25% simulationist** *as qualitative emphasis*. The older project invariant in `docs/archive/DESIGN_PRINCIPLES.md` §1 says equal thirds. These are **not currently the same instruction**. Treat #516 as a proposed later direction, **not a stealth rewrite** of the older canonical document. Tomi must decide whether to amend that invariant, whether #516 applies only to the crossover, and how to record the change. No numerical weighting is implemented.

## System choices to preserve vs decisions still open

| Topic | Existing / safe to reuse | Author decision or playtest needed |
| --- | --- | --- |
| Resolution | Approved crossover Fate foundation: 4dF + individual Fate skill; four actions (overcome, create advantage, attack, defend); Fate points, aspects | Final challenge/contested-stakes and mixed-success presentation; no second PbtA dice pool |
| Individual skills | Six COG/INT/REF/SAV/SOM/WIL; specialty via competence tag or stunt, not seventh skill | Starting allocation, how science competence is represented; do not add SCIENCE to crossover skill ladder without explicit approval |
| Characters | Same five-seat faction roster, player = leader, four agents; individual vs strategic layer have distinct namespaces | Strategic skills and agent progression, still unapproved |
| Physical conflict | Existing stress/consequence structure | Danger calibration, cover, line of sight, initiative, tactical action costs, healing |
| Cyber | Network reachability in `strategy_game/cyber.py`, equipment permissions, C/I/N as possible hardware descriptors rather than PC attributes | Whether/how device C/I/N modifies a roll; trace/latency mechanics; BCI risk tables |
| PSI | Natural PSI setting premise; Physical/Cyber/Astral description | Named permission, conflicts, costs and causal boundaries |
| Persistence | #502 proposed Case / MissionOutcome and one WorldState | Mutations, quantities, politics linkage and authority to write outcomes |

## Reference-to-mechanic matrix (seven computer games)

| Reference | Adopt | Simplify | Avoid | Layer |
| --- | --- | --- | --- | --- |
| Citizen Sleeper | Pressure, resource clocks, consequential choices | Represent pressure via existing aspects/scene stakes initially | Parallel dice-allocation system | RPG |
| Disco Elysium | Investigative and conversational consequence; failure that creates new leads | Skill-informed descriptions with six broad skills | Large specialized skill tree | RPG |
| X-COM | Four-agent selection, spatial stakes, persistent injury | Small optional tile maps | Every case becoming mandatory combat | Tactical |
| Cyber Knights: Flashpoint | Stealth, security topology, multiple insertion routes | Access path via #344 reachability | Full separate stealth/hacking minigame | Tactical |
| Shadowrun: Dragonfall | Dialogue, investigation and combat in one mission | 8-bit map with one resolution kernel | Separate dungeon/quest engine | RPG/tactical |
| Crusader Kings III | Relationships, traits and personal motives shaping politics | Named aspects and recorded events | Simulating every character's genealogy | Faction |
| Terra Invicta | Councilor operations and long-term geopolitical consequences | One leader + four agents, discrete outcomes | Global micromanagement as initial MVP | Strategy |

Tabletop systems: Fate Core/Transhumanity's Fate inform fiction-first aspects and the bounded Fate chassis; PbtA suggests GM consequences and partial-success *fiction* but not another roll engine; Cities/Stars/Worlds Without Number suggest clear risk, procedures and optional squad constraints; Eclipse Phase suggests durable injury and identity/technology causal consistency **without** importing its numbers or proprietary setting.

## Candidate procedure to playtest (no new mechanical constants)

1. Player describes **intent, method, stakes** and whether this is a scene or strategic mission.
2. GM identifies an attainable action, applicable skill/permission tag, environmental aspect, available resources, opposition and **actual** reachability for cyber targets.
3. Use the **currently approved Fate resolution**; narrate success, tie and failure according to that engine rather than improvising a second probability scale.
4. Choose a consequence consistent with the fiction: evidence, time/attention, social relationship, stress or lasting wound. Negative outcomes should create decisions rather than simply stall clue discovery.
5. Record the outcome once with provenance and let RPG/tactical/strategy views project it. No presentation layer directly changes political power.

### Worked playtest prompts (fictional examples, not resolved mechanical results)

- **Investigation:** a witness withholds camera logs; use dialogue to find the access policy, or inspect the public record. A setback exposes a supervisor's involvement rather than hiding the only clue.
- **Social:** a station chief fears Panopticon monitoring; learn their concern and offer enforceable safeguards rather than treating conversation as mind control.
- **Cyber + PSI:** a hacker cannot reach an offline archive remotely. A field agent plants a physical interface; an unusual Astral impression may suggest a location but grants **no network session**.
- **Combat:** a four-agent team reaches a guarded laboratory. Cover and escape routes matter; injury persists even if the mission succeeds. Turn structure, target numbers and harm values **are deliberately undecided**.
- **Mixed four-agent mission:** two agents interview a caretaker; one inspects a device; one scouts a service entrance. Their clues combine into one Case and MissionOutcome; the faction receives only adjudicated consequences.

## Human-led playtest sheet

Record: scene goal, action chosen, skill, obstacle, permission/tags, roll/outcome under the already-approved rules, approximate scene duration, meaningful options, wounds/complications, GM ambiguities, faction implications. Run one noncombat investigation and one optional encounter with a four-agent party. Evaluate whether narration dominates without erasing tactical choices, and whether the same Fate outcome vocabulary works at each scale.

## Author sign-off checklist

- [ ] Resolve #516's 50/25/25 target versus the older equal-thirds invariant (scope and canonical source).
- [ ] Confirm shared crossover skill model; decide if SCIENCE is competence tag or an approved replacement.
- [ ] Approve core action/scene outcomes and how success-with-cost is expressed.
- [ ] Approve danger, action economy, hardware modifiers, PSI permissions and agent mission integration.
- [ ] Playtest and approve the final tabletop rules **before** digital mechanics are treated as canonical.

**No authorization or playtest is implied by this packet.** Related: #200, #280, #389, #461, #482, #502, #515, #517.

## Deliverable 1 in detail: what to borrow, adapt and reject, system by system

The issue asks for a comparison that names **specific mechanics** with reasons, not a family-level impression. The table below is that comparison. Every row is a *recommendation for the author to accept, amend or reject* — nothing here is a decision, and no mechanic below is implemented anywhere in the repository.

### Narrative systems

| System | Mechanic | Verdict | Reason |
| --- | --- | --- | --- |
| **Fate Core** | The 4dF ladder (−4…+4, centred on 0) with a small skill range | **Adopt** as the candidate kernel | It is already the approved crossover foundation in `strategy_game/RULEBOOK.md`; replacing it would be a second resolution system, not a synthesis |
| | Four actions (overcome, create advantage, attack, defend) | **Adopt** | One vocabulary serves social, investigative, physical, cyber and astral framing without inventing per-domain rules |
| | Aspects and fate points | **Adopt** | The cheapest way to make "the scene matters" mechanical without a modifier table |
| | Stress boxes + consequence slots | **Adapt** | Keep the shape; the number of boxes and the severity ladder are author calibration, and Eclipse Phase's durability (below) argues for fewer, longer-lasting consequences |
| | Skill pyramid / long skill list | **Reject** | Six individual skills is the stated anti-bloat target; a pyramid is a second progression economy |
| **Transhumanity's Fate** | Ego/morph separation (who you are vs what you are wearing) | **Adopt** | It is the cleanest existing expression of NoöPunk's body-swap, fork and resleeve questions, and it costs one extra field rather than a subsystem |
| | Its 24-skill list | **Adapt, not import** | The *coverage* is a useful checklist (does the six-skill set cover Xeno-Contact, Infosec, Kinesics?); the *list* would double the sheet |
| | Morph-specific stunt packages | **Adapt** | Useful as equipment/permission tags on a morph, not as a parallel advancement track |
| **Eclipse Phase** | Durable harm: wounds that persist across scenes and change what a character can attempt | **Adopt** (as design intent) | It is the simulationist 25%: a mission that costs nothing teaches nothing |
| | Coherence / stress from body and identity change | **Adapt** | The *pressure* is right for this setting; a second track with its own arithmetic is not, so express it through consequences whose content is identity strain |
| | Psychosurgery, forks, backups as plot-legal operations | **Adopt** (fiction + permission) | They are setting-defining and need no new dice |
| | d100 percentile resolution | **Reject** | A second kernel; the issue explicitly asks for one coherent resolution mechanic |
| **PbtA (selected titles)** | "Success with a cost" as the *normal* middle outcome | **Adopt** (as fiction, not as dice) | Fate's *tie* already carries this; the PbtA contribution is the discipline of making the cost interesting rather than the roll being binary |
| | Moves as named procedures | **Adapt** | Useful as *checklists* ("when you hack a hostile host, ask…") bound to the four Fate actions, not as a separate move engine |
| | Clocks / fronts as visible pressure | **Adapt** | Excellent for investigation pacing and for the strategic layer's long horizon; express them as scene aspects or faction-level progress, not a second resource economy |
| | 2d6+stat with 6−/7-9/10+ bands | **Reject** as a kernel | Choosing it would replace 4dF, not complement it — see the one-kernel note below |

### Gamist and procedural systems

| System | Mechanic | Verdict | Reason |
| --- | --- | --- | --- |
| **Cities Without Number** | Explicit mission procedure (brief → approach → objective → extraction) | **Adopt** | It is the structure #515's four-agent mission needs, and it is system-neutral |
| | Shock / trauma severity on a hit | **Adapt** | The *idea* of a severity band that outlives the scene maps onto consequence slots; the numbers are calibration |
| | System strain from cyberware | **Adapt** | The pressure is right for a cyberware-heavy setting; one number per implant is cheaper than a strain economy |
| | Class/level progression with ability trees | **Reject** | Fights fiction-first character definition and adds a second advancement axis beside aspects/stunts |
| **Stars Without Number** | Faction turn: factions act on a cadence with assets and goals | **Adapt** (strategic layer only) | A useful cadence reference for the faction simulation; the asset/economy arithmetic is the strategy layer's own design problem |
| | 2d6 + skill + attribute resolution | **Reject** | A second kernel again |
| | Saves as a separate resistance scale | **Reject** | Fate already resolves resistance as an opposed or passive defence; a third scale is bloat |
| **Worlds Without Number** | Foci (a compact bundle of competence + permission) | **Adapt** as the model for stunts | Closer to NoöPunk's "one tag that changes what you may attempt" than a tree of feats |
| | Partial-class / multiclass stitching | **Reject** | Character identity here is faction, morph and ideology, not class arithmetic |
| | Shock damage for melee | **Reject** | Combat lethality calibration is an author decision and a subsystem this project does not need at MVP scale |

### The one decision that cannot be deferred

Every "adapt" above is cheap because it rides on an existing kernel; the **kernel itself** is the fork that determines what the rest costs:

- **4dF ladder (current foundation).** Keeps `strategy_game/RULEBOOK.md`, existing tests and the six-skill sheet valid. Cost: coarse granularity, and PbtA-style "partial success" must be expressed through ties and consequences rather than a dedicated band.
- **2d6 + stat bands (PbtA or Without Number style).** Buys explicit partial-success bands and a familiar OSR feel. Cost: every existing Fate-rated artefact becomes legacy, and the issue's "one coherent resolution mechanic" becomes a migration rather than a synthesis.

The packet does not choose between them. What it can say is that the *synthesis* the issue asks for is achievable either way, because the adopted items above (mission procedure, ego/morph, durable harm, clocks-as-pressure, foci-as-stunts) are **kernel-neutral**: they change what a roll is *about*, not how a roll works.

### What would count as evidence that the 50/25/25 balance holds

A balance claim is only checkable if it is falsifiable at the table. Candidate tests for the playtest sheet this issue already defines:

- In a session transcript, **count the decisions**: if more than half the meaningful choices were "which ability to use", narrativism did not lead.
- **Count the procedures actually consulted**: a gamist quarter is present when the mission procedure is followed without the GM inventing it; if it is never consulted, the quarter is decoration.
- **Count the consequences that outlived their scene**: simulationism is present when harm, exposure and identity cost persist; if nothing persists past the scene, the simulationist quarter is absent regardless of how detailed the injury table is.
- **Check the mixed mission**: one four-agent mission must be resolvable with the same skills, the same four actions and the same consequence vocabulary at narrative, tactical and strategic zoom. A second vocabulary appearing at any zoom is the failure mode this issue exists to prevent.
