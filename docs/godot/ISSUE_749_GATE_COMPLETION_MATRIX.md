# Issue #749 gate completion matrix — measured, not claimed

**This is a measurement, not an acceptance record.** It exists because #750–#753 were closed with
contradictory comments: three separate threads contain *"leave this issue open"*, *"not ready to
close"* and *"a rules defect that blocks this gate"*, and the closing comments then asserted
completion. There was no single place that said what the vertical slice actually does.

Measured **2026-10-30** in a clean worktree of `origin/main` at **`36df421`**, Godot **4.7.2**:

```
git worktree add --detach /tmp/np749chk origin/main
godot --headless --path . --import
godot --headless --path . --script res://godot/tests/run_tests.gd
→ 254 checks, 0 failed
```

The import pass is required: without it the global class cache does not exist and six suites fail to
load (already documented in `docs/GODOT_MVP_AUDIT.md`). That is an environment artifact, but it means
a headless run without `--import` reports failures that are not defects.

## Corrections to the record

Three things were claimed in the issue threads that do not survive measurement. They matter because
the issues were closed on them.

1. **"→ 253 checks, 0 failed … verified 2026-10-28"** appears in the closing comments of #751 and
   #752. The issues were created **2026-10-30T08:35**, so a verification dated 2026-10-28 cannot be
   evidence for them. The figure on `main` at `36df421` is **254**, because #768 has since added
   checks. The number moved; the claim was stale when written.
2. **#752's invented trace meter was real.** `godot/core/hacking.gd` implemented
   `trace_per_action`, `trace_on_failure` and `alarm_threshold` — a linear per-action meter, which
   #752 explicitly forbids ("no invented … trace-die hacking minigame"). **#768 removed it**: the
   clock now comes from `data/rules/cwn_hacking.json`, a contract shared with
   `src/rules/cwn_hacking.py` (`FAILURES_PER_ALERT_ACTION`, `ALERT_ACTIONS_TO_TRIGGER`). Verified
   absent on `main`. This is the one substantive defect in the set and it is now fixed.
3. **"enemy turns"** was claimed for Gate 2. `godot/core/combat.gd` exposes no AI: `end_turn()`
   advances the order and resets the two per-turn flags. Whatever drives enemies is the caller's
   job, and nothing in `godot/` does it.

## Gate 1 — campaign state, transitions, saves (#750)

| criterion | artifact | status | evidence |
| --- | --- | --- | --- |
| new campaign start at Romppainen's home | `src/godot/campaign_state.gd`, `godot/core/scene_flow.gd` | **verified** | `test_campaign_state.gd` — start location |
| Lakkahaltia entry point retained | `src/godot/title.gd` offers both | **verified** | legacy suites + ward smoke in the same CI job |
| Home → HQ → mission → debrief | `scene_flow.gd` (`HOME/HQ/MISSION/DEBRIEF`) | **verified** | `test_scene_flow.gd` |
| versioned serialization, incompatible saves rejected | `CampaignState.to_data/from_data` | **verified** | `state serialization`, `incompatible versions rejected` |
| idempotent journal / duplicate events | `record_once` | **verified** | `idempotent journal entry` |
| save/load roundtrip | `save`/`load_save` | **verified** | `save/load roundtrip` |
| undecided build choices stay choices | `character.json` `choices` list | **verified** | four named choices, no invented values |
| autoload audit | `GODOT_MVP_AUDIT.md` §7 | **verified** | one autoload (`GameState`), MVP path never references it |

**Gate 1 is complete.** One caveat worth keeping: its central suite could not load until #764
preloaded the class, so these seven checks had never run before that fix.

## Gate 2 — character, gear, tactical encounter (#751)

| criterion | artifact | status | evidence |
| --- | --- | --- | --- |
| initiative | `combat.gd start()` (1d8 + DEX) | **verified** | `test_combat.gd` |
| movement on a grid | `move()`, Chebyshev, one Move per turn | **verified** | `test_combat.gd` |
| attack rolls through the adapter | `attack()` → `RulesAdapter.attack_roll` | **verified** | `test_combat.gd` |
| cover | target `cover` added to AC | **verified** | `test_combat.gd` |
| HP, down state, encounter end | `_refresh_over()` | **verified** | `test_combat.gd` |
| peaceful completion | mission data + investigation gate | **verified** | `test_session.gd` two-path end-to-end |
| **Main / Move / On Turn / Instant action types** | — | **unimplemented** | `combat.gd` has only `moved`/`acted` booleans; no action vocabulary exists |
| **ammo / reload** | — | **unimplemented** | `ammo` appears in **zero** files under `godot/` or `src/godot/` |
| **trauma / shock / injury in the Godot kernel** | — | **unimplemented** | trauma exists in Python and in `lakkahaltia` *scenario data*, not in `godot/core/combat.gd` |
| **two ACs (melee/ranged)** | — | **unimplemented** | `combat.gd` carries one `ac` |
| **legal level-1 creation UI** | — | **unimplemented** | `campaign_screen.gd:4` states it itself: *"CWN operator creation … belong to later gates"* |
| enemy turns | — | **unimplemented** | no AI function anywhere in `godot/` |

**Gate 2 is partial.** The encounter works and is deterministic, but four of #751's named
requirements — action types, ammo, trauma, two ACs — are not in it, and the creation UI does not
exist.

## Gate 3 — node-link hacking view (#752)

| criterion | artifact | status | evidence |
| --- | --- | --- | --- |
| authoritative CWN clock (not a trace meter) | `data/rules/cwn_hacking.json` + `cwn_hacking.gd` | **verified** | #768; trace keys absent from `godot/core/hacking.gd` |
| access / connectivity / program / CPU procedure | `godot/core/hacking.gd` | **verified** | `test_hacking.gd` |
| separate node/edge view | `src/godot/network_map.gd`, instantiated in `campaign_screen.gd:94` | **verified (read-only)** | #767; renders, does not drive actions |
| persistence of hacking state | `session.gd` save/load | **verified** | `test_session.gd` |
| air gap / range / wireless / VR penalties | penalties in the contract; **no air-gap case in the slice** | **partial** | wireless and VR are modelled; an air-gapped network is not exercised |
| alert escalation and consequences back in the physical scene | escalating clock; no scene consequence wired | **partial** | the clock works; the consequence does not reach the physical view |

**Gate 3 is substantially complete on rules and partial on the demo.** The invented mechanic is gone,
which was the blocking defect.

## Gate 4 — PSI fixture, art, end-to-end validation (#753)

| criterion | artifact | status | evidence |
| --- | --- | --- | --- |
| SWN psychic fixture, separate from Romppainen | — | **unimplemented** | `godot/scenarios/mvp_romppainen/` holds `character.json` and `mission.json` only |
| Effort / discipline / technique gates | `godot/core/psionics.gd`, `psychic_effort.gd` | **partial** | resource layer exists and is tested, but no fixture exercises it in the MVP |
| original art with provenance | procedural tiles in `mvp_game.gd` | **partial** | no imported asset, so no licence burden — but also no pixel art |
| headless suite | 254 checks, 0 failed | **verified** | this document |
| windowed Linux playthrough of the full loop | — | **not recorded** | no log, transcript or screenshot of a current build |
| completion matrix + source/licensing ledger | this file | **delivered** | — |

**Gate 4 is the least complete.** The honest summary is: no PSI fixture, no windowed verification,
art by construction rather than by asset.

## What closing these issues would require

Ranked by what blocks a truthful "MVP is playable end to end" claim:

1. **A windowed playthrough record** (Gate 4). Everything else is headless; nobody has shown the
   loop running on screen for the current build.
2. **The creation UI** (#751) — the operator is currently a JSON file with its choices undecided.
3. **Action types, ammo, trauma, two ACs** in `combat.gd` (#751) — the encounter is thinner than CWN.
4. **A PSI fixture** (#753) — the Effort layer has no MVP consumer.
5. **An air-gapped network case and a scene-level alert consequence** (#752).

Nothing on this list is architectural. Each is additive to a green, deterministic base, and item 1 is
the only one that cannot be done headlessly.
