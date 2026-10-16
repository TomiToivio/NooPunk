# Issue #506: research-project integration notes

PR #507 was reconciled with the already-merged, more complete implementation from PR #508. The **existing** `strategy_game/projects.py`, `strategy_game/research.py`, `strategy_game/research_slice.py`, `strategy_game/campaign/state.py`, and `strategy_game/tests/test_research_projects.py` remain the source of truth. Do not introduce a second incompatible ResearchProject, TechNode, resource ledger, or research save format.

## Author simplification: ONE SCIENCE skill

All research domains use **one SCIENCE skill** on the faction-agent sheet; do not introduce separate physics, biotechnology, parapsychology, archaeology, data-analysis, engineering or knowledge ratings. The existing strategic roster proposal spells the identifier `science` (lowercase); this is the same single skill concept, not another skill. Specialist domain labels are optional context or permissions, **not** a second numerical skill and **not** a universal required TAG.

Project differences arise from authored evidence/prerequisites, available facilities and resources, difficulty, work-clock length, ideological choices and payoff. Alien reverse engineering and mundane technology transfer therefore share one competence gate: the existing Fate-based strategic-project check.

## Reconciliation notes

The initial PR #507 independently introduced a standalone `ResearchState` and `ResearchProject` in a file that PR #508 also created. Keeping both implementations would overwrite the working campaign integration and break the existing APIs. For this merge, the PR #508 implementation was retained and the superseded standalone tests were not brought into `main`.

**Follow-up:** The current `ResearchProject.__post_init__` requires domain TAGs or an explicit waiver for any project with a lead. This conflicts with the author's later clarification that domain TAGs are optional, so remove the universal requirement and adjust executable tests. Update documentation that describes domains as required. Preserve project prerequisites only when fiction and authored data warrant them.

For existing integration and test commands see `strategy_game/docs/RESEARCH_PROJECTS.md` and `strategy_game/tests/test_research_projects.py`.

## Status

The RPG-first research and strategic-project implementation is already represented by PR #508. This merged documentation records #507's reconciliation and the single-SCIENCE direction. Issue #506 remains open for the domain-TAG simplification, extended tech-tree content and future X-COM / Terra Invicta strategy phases.
