# #230: Low-prep UNSA case worksheet

The machine-readable template [`data/rules/unsa_case_template.json`](../../data/rules/unsa_case_template.json) follows the **existing** [default investigation doctrine](../design/DEFAULT_INVESTIGATION_FANTASY.md). It is a blank tabletop/GM worksheet, not a generated scenario, rule migration or new setting canon.

Fill in the hook, initial scene, a case question, investigator/partner/controller/forensic AI roles, and four groups of leads: **Physical**, **Cybernetic**, **Social**, and **Psychic/Noöspace**. List witnesses, corroborating or contradictory evidence IDs, faction interests, meaningful choices and persistent consequences. Keep at least two viable routes to each indispensable lead instead of risking an investigation softlock from one failed roll.

For each case, independently check all three equally weighted design goals: credible causal constraints (**Simulationism**), meaningful relationships/choices (**Narrativism**) and transparent risk/reward (**Gamism**). Equal design weight does not imply one-third of scenes must belong to each category.

The evidence IDs can reference the #226 custody ledger. The template records no truth judgement; a psychic impression remains an **uncertain lead** until corroborated. Neither a computer-game LLM nor a tabletop GM may assume arbitrary BCI compromise from a network clue, and an LLM should not retroactively edit established evidence. The actual scene's dice, skills, NPC stats, AP, equipment and PSI permissions must be read from their approved subsystem, not improvised as permanent canon here.

Other agents: #226 owns evidence and police procedure, #220 social mechanics, #222 graph/network hacking, #223/#224 psychic/astral, and #232 rulebook assembly. This blank worksheet can be safely used by all of them without competing definitions. It does **not** satisfy #230's full generator, faction clocks or finished beginner adventure yet.

This is a worksheet/documentation artefact and has **no unit tests**: the former `test_issue230_unsa_case_template.py` was removed under issue #271, per `AGENTS.md`'s code-only testing policy. Review it editorially and at the table.
