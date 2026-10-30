# Baseline #848 — deviation register

Pinned baseline: **`36092a5`** on `main`. Canonical rules **`RULEBOOK.md`**; canonical game
**`project.godot` → `scenes/main.tscn`**; rules authority **vanilla CWN primary + vanilla SWN Revised**
where CWN is silent.

#848 requires that "vanilla published CWN/SWN procedures govern both tabletop and Godot rules" and that
"deviations are tracked as bugs, not silently accepted design". This file is that track. It records what
does not yet meet the directive, with evidence, so no agent has to guess and no reader mistakes the gap
for a decision.

Verified at the pinned baseline: `godot --headless --path . --script res://godot/tests/run_tests.gd`
→ **760 checks, 0 failed**.

## D-1 — BLOCKING: the canonical rulebook still specifies the seven custom attributes

`RULEBOOK.md` §3.3.1 "The seven attributes" defines **Fitness, Cognition, Awareness, Agency, Reflexes,
Cyber, Empathy**, and §3.3.2 generates them by rolling 3d6 seven times. There is **no STR/DEX/CON/INT/
WIS/CHA attribute block anywhere in the book** (the only `INT` hits are a skill-keying table, not
attributes).

That is the exact design #848 forbids: *"No new seven-attribute Fitness/Reflexes/Cognition/Cyber/
Awareness/Agency/Empathy conversion"*. The rulebook also carries a legacy→seven collapse table
(`Strength → Fitness`, `Dexterity → Reflexes`, `Strength, Constitution → Fitness`, …).

**Scale of the change:** 104 lines across `RULEBOOK.md` and the generated `rulebook/parts/*.md` reference
the seven-attribute scheme.

**Why it is not fixed here:** replacing a book's attribute system is an authorial content decision, and
#848 itself says it "establishes the direction; it does not itself assert that code has already been
reverted or implemented". Recorded as the top blocker instead of being rewritten silently in a
coordination PR.

**Consequence:** while this stands, the *tabletop* rules are custom NoöPunk and the *Godot* rules are
vanilla CWN, so the two halves of the baseline disagree — which is the failure #848 exists to end.

## D-2 — the Godot side is vanilla CWN and therefore ahead of the book

`data/rules/wn_core.json` and `godot/core/rules_adapter.gd` use CWN attributes (STR/DEX/CON/INT/WIS/CHA),
2d6 skill checks, d20 attacks and saves, and CWN trauma/shock. Verified by the 760-check suite. Nothing
in the Godot layer uses the seven-attribute design.

So the digital implementation is the reference for what the book should say, not the reverse.

## D-3 — resolved in this pass: restart docs that still claimed authority

`noopunk/START_HERE.md`, `noopunk/game/README.md`, the root `BASIC.md` and the stale
"NEW AUTHORITATIVE RESTART: issue #827" section of `AGENTS.md` all still presented the blank-rulebook /
seven-attribute direction as current. Each now carries a superseded marker pointing at #848 and the
CURRENT DIRECTIVE. Content is preserved; nothing was deleted.

## D-4 — coverage backlog (subsystem status)

| Subsystem | Governing book | Status |
| --- | --- | --- |
| Attributes, skill checks (2d6), saves and attacks (d20) | CWN | **implemented**, tested |
| Combat: initiative, action economy, damage, trauma, shock, soak | CWN | **implemented**, tested |
| Equipment, armour, weapons catalogue | CWN | **implemented** (23 weapons, 8 armour, catalogue tests) |
| Cyberware catalogue and strain | CWN | **partial** — body implants wired; head/limb/nerve/sensory/medical/skin pending |
| Hacking: access/CPU, Alert clock, programs, verbs/subjects | CWN | **implemented**; air gap, program memory and Demons/watchdogs pending |
| Drones, vehicles | CWN | **pending** |
| Progression, XP and level | CWN | **implemented** for XP/level/attack/HP/skill points; foci and Edge tables have no UI |
| Psionics (class, disciplines, Effort, techniques) | SWN Revised | **partial** — Effort layer tested; no legal psychic fixture, technique catalogue incomplete |
| Chapter-level tabletop text mirroring the Godot rules | CWN | **blocked by D-1** |

## D-5 — subsystem boundaries, stated

CWN governs attributes, skills, checks, saves, combat, injury, gear, cyberware, hacking and progression.
SWN Revised governs psionics, space travel and faction-scale play, where CWN is silent. Where both have a
procedure, CWN wins and the choice is recorded here rather than being merged ad hoc.

## D-6 — the pinned SHA is behind `main`

`AGENTS.md` and `START_HERE.md` pin **`36092a5`**, and that claim is true of that commit (760 headless
checks, 0 failed — re-verified). But `main` has moved since: #844 (creation-screen repair) and #849 (the
baseline directive itself) both landed after it.

A pin is for reproducibility, so being behind is not an error in itself; what matters is that agents
**declare** which commit they built on. When the next migration PR settles, the pin should be advanced
to that merge commit. Until then: work from `main`, state the commit in the PR, and do not treat
`36092a5` as "the tip".

## What an agent should do

Read `AGENTS.md` first. Build only on the canonical paths. If a task seems to need `noopunk/`,
`rulebook/` hand-edits, or a new Godot project, stop: that is the superseded direction. Raise it on #848
rather than working around it.
