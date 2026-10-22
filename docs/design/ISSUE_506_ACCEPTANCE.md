# #506 acceptance record — research and branching tech trees

**Date:** 2026-10-22. **Status:** acceptance record. **No rule, number, threshold or convention is
approved by this record; the ones that need the author are carried in the open-items table.**

## Criterion-by-criterion, verified by running the code

| # | Criterion | Where it lives | Verification |
| --- | --- | --- | --- |
| 1 | A research project uses the **lead scientist's science check as a success gate**; a failed check gives **zero** progress for that turn | `strategy_game/research.py` — `ResearchProject` (`lead_skill = "science"`, `RESEARCH_LEAD_SKILL`); `strategy_game/projects.py` — `advance_project` | `python -m strategy_game.research_slice` on seed 5 shows `cause=check_failed` with `filled=11/12` (**unchanged**) and, on the archive-terminal project, `check_failed` at `filled=0/10` twice. A failed check adds nothing. |
| 2 | Progress scales with allocated **faction research resources** and completes after difficulty-defined total work | `strategy_game/projects.py` — `Allocation`, `FactionCapacity`, `ProjectClock`, `clock_for_difficulty` | `clock_for_difficulty`: 1 → 10, 2 → 12, 3 → 14, 4 → 16 units. The slice allocates capacity per programme (`runner.commit`) and releases it on completion (`runner.release`). |
| 3 | One **alien/ASI reverse-engineering** example and one **mundane technology transfer** example, without conflating discovery, prototype and manufacturing | `strategy_game/research_slice.py` — `reverse_engineering_project()` (stage `UNDERSTANDING` / `scientific_understanding`), `technology_transfer_project()` (stage `MANUFACTURE` / `reproducible_manufacture`) | Two declared nodes: `nhi-propulsion-understanding` (branch `alien_derived`, hybrid `quantumpunk`) and `civic-archive-terminal-manufacture` (branch `cyberpunk`, no hybrid). The transfer project's prerequisite is the **archive** the organising programme won — not a specimen — so discovery is not smuggled into manufacturing. |
| 4 | Research reflects ideological prohibitions, branch choices, hybrid paths and a viable non-ASI future | `strategy_game/research.py` — `prohibitions_for()`, `TechNode.branch` / `.hybrid_of`, `ResearchProject.prohibited_by` / `.domain_tags` | The `cyberpunk` branch with no hybrid *is* the viable non-ASI future, and it is a first-class node, not a comment. Prohibitions are read from the faction's own members' capabilities (`prohibitions_for`). |
| 5 | A completed RPG mission can unlock/modify research; research changes later RPG decisions and persistent faction state | `strategy_game/campaign/missions.py` — `apply_mission_outcome()`; `strategy_game/research.py` — `rpg_options()` | The engine **refuses** to start the propulsion project without the mission-granted artefact: *"missing prerequisites: artefact:nhi-propulsion-component … a resolved mission grants it through strategy_game.campaign.missions.apply_mission_outcome"*. The slice's first step is a `mission_outcome`; `rpg_options()` is the read side that turns held capabilities into RPG-facing options. |
| 6 | The shared strategic-project engine supports at least one **non-research** task with another lead skill | `strategy_game/research_slice.py` — `archive_access_project()` | `kind=organize`, `lead_skill=stewardship`, `resource_kind=personnel`, and it yields **no capability**. Research is one instance of the engine, not the engine. |
| 7 | Serialization, deterministic checks with injectable RNG, meaningful UI/logging and automated tests covering stalls, progress, interruption, reassignment and completion | `strategy_game/projects.py` — `to_dict`/`from_dict` on every record; `advance_project(..., rng: Random)`; `strategy_game/research_slice.py` — the JSON report; `strategy_game/tests/` | `rng` is a parameter, so a seeded `Random` makes every run reproducible. The slice's report is the UI/logging surface. The suite covers the listed transitions. |
| 8 | Compatible with #502's staged rollout and #482's Fate-derived character mechanics; no full grand-strategy prerequisite for MVP | The slice builds one faction, five characters, one case and three projects — no map, no world simulation | `python -m strategy_game.research_slice` runs standalone in a fresh checkout with no other system initialised. |

## Reproducible checks

```bash
python3 -m strategy_game.research_slice
python3 -m unittest discover -s strategy_game/tests -p "test_*.py"   # 1535 tests, OK
python3 -m unittest discover -s tests -p "test_*.py"                 # 585 tests, OK
```

## Open items carried forward, not buried

- **D27 — the strategic-project conventions of Phase 1: the dice band and the work scale.** The
  engine needs three numbers and a ruling on a fourth case. The work scale is currently
  `10 / 12 / 14 / 16` for difficulties 1–4; the *band* is not approved.
- **D28 — what a domain TAG and an ideological prohibition should *do*.** Both are recorded and
  deliberately inert today. `domain_tags` is carried on a project; `prohibitions_for` reads the
  faction's own members' capabilities. What they *gate* is the author's call.
- **D33 — is "simplified science" a seventh individual skill?** #506 already uses one strategic
  `science` rating; whether #516's character sheet carries a science skill is #516's to decide.

## What closure of #506 does and does not mean

It means the **research and branching tech-tree engine is implemented and verified** against all
eight acceptance criteria, and that it runs as a slice without any grand-strategy prerequisite.

It does **not** mean: the dice band or work scale are approved, that tags and prohibitions gate
anything yet, that the tech tree is canonical content, or that the RPG↔research coupling has an
approved *design* — only a working one. The author work order keeps #506's *RPG-relevant* part
(the single science skill) in the RPG track and the rest in the later strategy track; this record
does not promote it.
