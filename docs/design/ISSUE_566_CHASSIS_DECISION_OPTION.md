# NoöPunk chassis implementation decision proposal (#566)

**Status: recommended migration policy, not an author-ratified change.** Recorded to make ongoing development safe without falsifying approvals. The issue requires the author's explicit four-part ruling before completion.

| Question | Safe default for implementation planning | Existing authority preserved |
| --- | --- | --- |
| Scope | **A only**: root tabletop RPG, `src/rules/` and `rulebook/` | Crossover B keeps approved Fate under #389/#482; C remains board/tactical |
| Check | **STAT + Skill + 1d10 ≥ DV** | #111 and existing difficulty/margin tables; no silent 2d6 |
| Attributes | **FIT / REF / INT / SOC / CYB / PSY** | #131 and current code; do not silently revive CHA |
| Classes | **No classes or character levels** | #564's constraint; purchased traits/stunts may be separately reviewed |

Rationale: this option retains every approved resolution instead of converting a procedural comparison into an unauthorized 41-file kernel rewrite. "One current NoöPunk tabletop rulebook" means root `RULEBOOK.md`; `strategy_game/RULEBOOK.md` documents the distinct, supported crossover Layer I rather than a second root RPG. Fate-to-d10 character conversion, if ever needed, requires explicit versioned adapters and dedicated tests. Nothing here says CWN/SWN/AWN/WWN procedures have been implemented.

**Author confirmation required:** scope A only or both; 1d10 or another check; SOC or CHA; reject or introduce classes/levels. This file records one fully specified option so the issue can be answered without ambiguity, but must not be cited as approval until the author confirms the four answers.
