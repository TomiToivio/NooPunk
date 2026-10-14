# Reality Tunnels — the ideology model (issues #469 and #470)

**Where this lives.** The model is implemented in `strategy_game/un_political_discourse.py` and its data
`strategy_game/data/un_political_discourse.json`, with the roster in `data/world/un_parties.yaml` and the
contracts in `strategy_game/tests/test_un_political_discourse.py`. This document explains it; it adds no
mechanic.

## 1. The apparatus

Laclau's concepts carry the discourse layer: **articulation**, **nodal points**, **demands** and the
**antagonistic frontier** each party constitutes — plus the eight **shared floating signifiers** the data
records (`humanity`, `freedom`, `security`, `consciousness`, `sovereignty`, `progress`, `nature`,
`survival`), whose meaning the parties contest. The data states the rule that keeps the vocabulary honest:
a floating signifier has contested meaning, while an empty signifier must represent a **chain of
equivalences**, not merely be vague.

## 2. Reality Tunnels, with an epistemic status

Wilson's tunnels are implemented as a *reading with a status*, not a claim: each party carries an
`interpretation`, an `evidence_status` drawn from the five the data defines — **observed, corroborated,
contested, alleged, unknown** — and `may_change_with_evidence: true`. That last field is the design
commitment: a tunnel is not a fixed belief, and evidence is allowed to move it.

`interpret_event(event_id)` is the executable form of the deliverable "contrasting readings of the same
evidence": it returns each party's stance on one event's topic together with that party's tunnel and the
status of what it thinks it knows. It is a view. It never asserts an event is true.

## 3. The 2026 baseline (sourced)

The model begins from real formations: the **accelerationist/tech-right** camp and its split from **MAGA
populists**; **safetyists** and **effective altruists**, themselves split between *shut it down* and *build
carefully*; the **AI-populist/ethics** camp defined by *who has power* rather than prediction; and **"AI as
a normal technology"**. Sources: Politico (April 2026), GPB's faction guide (Sept 2026), Kate Gage's
*Political AI Field Guide*, El País (May 2026), and the project's own
[LaclauGPT Phase 1 paper](https://github.com/TomiToivio/LaclauGPT/blob/main/paper/PHASE_1_PAPER.md).

The load-bearing observation is the **cross-cutting geometry**: the anti-AI left and the doomers converge
on *brake*, while abundance centre-left and e/acc converge on *build*.

## 4. Writing guidance

A faction's tunnel should be **recognisable from the inside and absurd from the outside**, and the same
event should read differently in two voices without the narration settling which is right. Where a party
claims something unproven, the data already marks it — the Libertarians' alleged capture, the Noösphere's
confidence in the Confederacy — and the writing must keep that mark.

## 5. Keep the issue open

#469's own final criterion asks for iterative review with the author, so it stays open. Nothing here
closes it.
