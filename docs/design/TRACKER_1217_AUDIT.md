# #1217 line 1: the character-creation audit

*"Audit the currently implemented CWN character creation, Europol Academy background, approved Edges/Foci, Social/Goal/
Personality Tags, inventory and equipment. Reuse `rulebook/14_CHARACTER_GENERATION.md`,
`docs/design/DRAFT_EUROPOL_ROOKIE_BUILD_1174.md` and `docs/design/DRAFT_NOOPUNK_EUROPOL_CHARACTER_GENERATION.md`; no
parallel engine."*

The audit's answer, in one line: **the engine exists and is not duplicated — what is missing is data, not code.** Every
creation rule lives in exactly one module, the two draft documents are prose around those modules, and the one real gap
is a verified catalogue of CWN Edges, which is why the player-facing flow cannot yet offer a choice.

## What owns what

| question | module | what it decides | state |
|---|---|---|---|
| attribute scores | `src/rules/cwn_character.py` | the array, 3d6 rolling, the substitute 14, modifier floor/ceiling | complete |
| skill picks during creation | `src/rules/cwn_character.py` (`SkillPool`) | level-0, level-1, and the refusal of a second level-1 pick | complete |
| Backgrounds | `src/rules/cwn_backgrounds.py` | free skill plus two Learning picks; "Any Skill" is not a legal specific pick | complete |
| Edges and Focus slots | `src/rules/cwn_edges_foci.py` | two Edges at start, a third at level 5, the Underdog Rule and its power-Edge exclusion, one Focus (two with Focused) | complete |
| the CWN Focus list | `src/rules/cwn_foci.py` | the twenty-six published Foci with their level counts | complete |
| which Edges a PC may take at all | `src/rules/psi_access.py` | the four psi Edges, the discipline ceiling, scripted-only effects | complete for those four |
| the join of the two budgets | `src/rules/rookie_build.py` | a build is legal only if CWN's slots **and** the policy agree; Mentalist may not sit beside Spellcaster/Summoner | complete |
| the authored lifepath | `src/rules/europol_lifepath.py` | fixed facts, three recruitment routes, delegated validation, aggregate violations | complete (builder core) |
| AWN Mutant | `src/rules/awn_mutant.py` | Europol approval, no automatic Hybrid origin, mutation-point arithmetic | complete except the printed tables |
| AWN Mentalist | `src/rules/awn_mentalist.py` | arts per level, Effort accounting, greater-art prerequisites, nerve-cyberware bar | complete |
| SWN Psychic Training | `src/rules/psychic_training.py` | bonus skill, free rank-1 technique, Effort +1, level-2 points | complete (#1217 line 11) |
| tags | `src/rules/scene_tags.py`, `src/world/graphs.py`, `src/rules/goals.py`, `src/rules/investigation.py` | Social, Personality, Goal and Clue — four types, no fifth | complete |
| inventory and kit | `src/world/items.py` | issue, fault, activate, the first-day required set | complete |
| equipment | `src/rules/cwn_equipment.py`, `tests/test_cwn_traceability_1068.py` | CWN equipment tables, pinned by the CWN baseline | complete |

## What the audit found

1. **No parallel engine.** Nothing under `src/` re-implements attribute generation, skill picking or Edge slots; the
   builder in `europol_lifepath.py` calls the modules above rather than copying them, which is visible in its
   `provenance` output and asserted by its tests.
2. **Two Focus systems, correctly separate.** CWN Foci (`cwn_foci.FOCI`) and the SWN focus (`psychic_training`) are
   different games' rules; a character takes one or the other. The lifepath builder's `foci` argument is CWN-only, and
   `psychic_training` refuses to touch `cwn_foci`.
3. **One real data gap: CWN Edges.** `psi_access.PC_EDGES` names four Edges; there is no catalogue of the ordinary ones,
   so `build_lifepath(edge_catalogue=…)` takes the list from its caller. A flow cannot *offer* a legal Edge until that
   list exists, and `psi_access.edge_decision` consequently refuses every ordinary Edge as *"not a known Edge"*.
   Transcribing the published Edge list is the single unblocking task for the tracker's line 2.
4. **One licence gap: AWN mutation tables.** `awn_mutant.py` encodes the *rules* (two Mutation Points, no more than three
   negatives, Stigma consequences) and refuses to invent mutation names; the printed tables are not in the repository.
5. **Tags are complete and already used.** Social, Goal and Clue tags have their own modules and tests; Personality is a
   descriptive tag with no mechanical effect, as `scene_tags` states.
6. **The equipment list for the opening is authored, not invented.** `items.py` carries the eight first-day items named
   in #1217 and refuses anything else.

## What this means for the remaining tracker lines

* Line 2 (flow) is blocked on item 3 above, plus the tag offer lists, which are an authoring decision.
* Lines 9 and 13 are blocked on item 4 and on book-verified tables respectively.
* Everything else on the opening list is either done or blocked on an author decision, not on code.

The derived status, with the evidence paths checked on every run, is
[`TRACKER_1217_STATUS.md`](TRACKER_1217_STATUS.md).
