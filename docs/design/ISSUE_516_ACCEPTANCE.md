# #516 acceptance record — the core RPG ruleset

**Date:** 2026-10-22. **Status:** acceptance record. **The ruleset is NOT canonical and the author
has not signed off.** This record states what is delivered and what remains; it approves nothing.

## The "Done when", and exactly how much of it is met

> Tomi has documented a single cohesive ruleset, demonstrated it in both narrative and tactical
> examples, tested its playability and explicitly signed off on the design.

| Part | Status |
| --- | --- |
| A single cohesive ruleset **documented** | **met** — the decision-support record and the rulebook sections exist as files |
| Demonstrated in **narrative** examples | **met** — the RPG-first investigation case, the three-path playtest, and the worked examples |
| Demonstrated in **tactical** examples | **met as far as the work order allows** — the tactical layer is renderer-neutral and combat is optional by the author's own sequencing; see the note below |
| **Tested for playability** | **met in the mechanical sense** — seeded, reproducible multi-path playtests with measured outcomes |
| **Explicitly signed off by Tomi** | **NOT met — D37 is open and unanswered** |

So four of five parts are met and the fifth is not. This issue is therefore closed as **deferred**,
carrying D29–D37, and the sign-off remains the author's.

## What is delivered, and where

| Deliverable the issue names | Where it lives |
| --- | --- |
| Compare Fate / Transhumanity's Fate / Eclipse Phase, Cities / Stars / WWN, PbtA — borrow, adapt or reject **with reasons** | `docs/design/ISSUE_516_CORE_RULESET_DECISION_SUPPORT.md` — 51 mechanic rows, 12 borrow / 15 adapt / 24 reject, with the rejects clustering on second economies (pools, strings, strain, reputation ratings) and second randomisers (d20, 2d6, d100) |
| The seven-game **reference-to-mechanic matrix** (adopt / simplify / avoid, and which layer each informs) | `docs/design/ISSUE_516_REFERENCE_MATRIX.md` — Citizen Sleeper, Disco Elysium, X-COM, Cyber Knights, Dragonfall, CK3, Terra Invicta |
| **One** unified core resolution mechanic for social, investigative, physical, cyber and PSI actions, with options, trade-offs and a recommendation **stated with its cost** | `ISSUE_516_CORE_RULESET_DECISION_SUPPORT.md` — one 4dF kernel, four outcomes, shape chosen pre-dice; the record also states that 4dF cannot express "very hard" in a single number |
| The **smallest usable character model**, reconciling the legacy FIT/REF/INT/SOC/PSY/CYB against the Fate skills, avoiding skill-list bloat | the same record — the bloat is **measured**, not asserted: ~40 legacy skills → the 18-name Fate Core default list → the six approved skills, with the duplicate (Physique/Will beside SOM/WIL) resolved and documented in `strategy_game/RULEBOOK.md` §3.1 |
| Player agency, GM adjudication, success-with-cost, complications, noncombat conflict (dialogue, investigation, hacking, PSI) | `strategy_game/RULEBOOK.md` §§2, 5, 8 and `strategy_game/rpg/scene.py`; the context switch is `ActionContext` in `strategy_game/rpg/skills.py` |
| **Fast, dangerous tactical combat** — action economy, cover, positioning, injury — without a tactical battle for every quest | `strategy_game/RULEBOOK.md` §8 and the tactical layer; the action-economy **rule** is D34, and combat is optional by the author's own work order |
| Coherent but lightweight PSI / psychotronics / cybernetics / hacking, with the **Physical / Cyber / Astral** layers | `strategy_game/rpg/` and `strategy_game/docs/CYBERSPACE_AND_HACKING.md`; the harm-model question is D36 |
| The **same** characters and outcomes connecting adventure missions to tactical maps and faction strategy | `strategy_game/rpg/boundary.py`'s pinned contract — the RPG layer imports no strategy engine module and reads no roster file; the tactical layer resolves through the same approved Fate kernel |
| A compact rules specification with **worked examples**: investigation, social conflict, PSI/hacking, combat, and a mixed four-agent mission | `strategy_game/RULEBOOK.md` §8 and the RPG-first case |
| **Playtest a short adventure and combat encounter, check pace/lethality/decision quality, revise** | `strategy_game/rpg/playtest.py` — three scripted trials (witness confidentiality, device provenance, PSI test) with seeded checks, saved-and-reloaded persistence and a reproducible report; `strategy_game/tests/test_rpg_first_playtest_runner.py` |

## On the tactical half of "Done when"

The issue's own "Done when" asks for the ruleset to be demonstrated in *narrative and tactical*
examples. It is demonstrated in both — but the tactical demonstration is the **optional
confrontation hook** and the headless tactical mission, not a pitched battle with a tuned action
economy. That is not a shortfall of the deliverable: the author's own work order (2026-10-19) makes
#515 *optional/future* until #516's RPG core is usable, and states there must be *"no alternate
tactical engine or mandatory combat"*. The action-economy rule itself is **D34** and is unanswered.
Claiming a tuned combat system here would be inventing a rule.

## Reproducible checks

```bash
python3 -m strategy_game.rpg --text
python3 -m strategy_game.rpg.playtest
python3 -m strategy_game.rpg.investigation_cli --save /tmp/noopunk-example-case.json
python3 -m unittest discover -s strategy_game/tests -p "test_*.py"   # 1535 tests, OK
python3 -m unittest discover -s tests -p "test_*.py"                 # 585 tests, OK
```

## Open items carried forward, not buried

**D29** which game the ruleset governs (legacy vs crossover) · **D30** six skills, or six attributes
*and* six skills · **D31** the unified resolution mechanic and its three sub-choices · **D32** whether
there is a distinct "success at a cost" band · **D33** whether "simplified science" is a seventh
individual skill · **D34** tactical combat's action economy · **D35** whether mission consequences
persist into the strategic layer, and who writes them · **D36** cyber/astral harm: a third stress
track and a cyberware capacity limit · **D37** **the sign-off itself**.

All nine are tracked on **#532**, the single board that replaced the closed issues.

## What closure of #516 does and does not mean

It means every deliverable an agent can produce is on `main`, verified and reproducible, and that the
issue was closed **as deferred** with the author's own ruling.

It does **not** mean the ruleset is canonical, that any proposed mechanic is approved, that combat
is tuned, or that Tomi has signed off. **D37 is open.** No rule, number, action list or dice
procedure became canon by this closure.
