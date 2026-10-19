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
