# NoöPunk Character Tags: Personality, Goals and Reputation

> **DRAFT — TOMI REVIEW REQUIRED — NOT AUTHOR APPROVED.** Issue [#1137](https://github.com/TomiToivio/NooPunk/issues/1137); researched 2026-11-04. Planning only; do not implement, modify the CWN core, or copy a published ruleset. **Evidence labels:** [E] empirical/approved; [X] experimental; [H] contested theory or parapsychology; [F] fictional 2045 premise; [P] draft mechanics. Tomi edits this proposal first, then separately authorizes matching tabletop and Python implementation.

## Preflight: what already exists for this subsystem

**The tag machinery is already implemented. This document must extend it, never duplicate it.**

| Component | Where | What it already does |
|---|---|---|
| Unified tag model (#51) | `src/rules/tags.py` — `Tag`, `TagStack`, `build_stack`, `stat_rating` | Stacking, keys, stat ratings |
| Tag-based attributes (#821) | `src/rules/noopunk_tags.py`, `data/rules/noopunk_tags.json` | Tag types, roll modifiers, conversion proposal |
| **Goal tag (#1119)** | `src/rules/goals.py` — `Goal`, `Progress`, `Award`, `GoalLog`, `record_progress`, `award_xp`, `paper_line` | A complete goal lifecycle |

The practical consequence: the open question for goals is **whether the existing `Goal` needs a horizon field**,
not how to design a goal system. Author canon for the rest lives in [`design/BIONICS.md`](../../design/BIONICS.md)
(the −4…+4 reputation range, and the `Pacifist-1` / `Pacifist-2` definitions).

## Goals
Minimal **tabletop-friendly character-sheet/database tags** extending CWN but **not replacing attributes, saving throws, skills, foci, social checks or player choice**. Grounded in author's [BIONICS.md](../../design/BIONICS.md) and the incremental Goal-tag issue: inspect current implementation first, **never create a parallel goal manager**.

## [P] Shared minimal tag record
`Tag{id,kind,subject,label,value?,time_horizon?,status,visibility,source_event,created_at,updated_at,expires_at?,evidence}`. Types have separate semantics: personality = enduring tendency; goal = intended future; reputation = *particular faction's perception*; relationship = *particular person's* perspective. Values do **not** automatically transfer among types. The tag is a character-sheet line, not a new meter for every behavior.

### A. Personality: patterns formed through repeated decisions
- Record stable traits such as `Humanitarian-1`, `Authoritarian-1`, `Reckless-1`, `Pacifist-1`; tags arise from repeated observed decisions or deliberate roleplay declarations, **not** a random identity assigned before play.
- A tag can license specific contextual consequences, dialogue and **at most a bounded ±1 modifier** when explicitly approved. Do not stack several tags into unlimited bonuses and do not automatically override CWN's published resolution.
- **Author's Pacifist example preserved for review:** `Pacifist-1` may prohibit initiating combat and impose a small penalty on aggression; `Pacifist-2` was proposed as dropping a weapon and fleeing/surrendering. These action-forcing consequences are **not yet approved**; discuss how to represent severe involuntary dispositions without taking control of the PC away. Recommendation: an explicit player consent/session-zero agreement or an opt-in scripted personality constraint, never a surprise GM command.
- Personality should be *reversible* through meaningful roleplay and catalyst; it is not medical diagnosis, cosmological polarity or a moral score.

### B. Goals: short, medium and long horizon
| Horizon | Example [P] | Progress representation |
|---|---|---|
| Short | `Finish incident report` | `active/achieved/abandoned`, optional evidence note |
| Medium | `Earn trust of Finnish police liaison` | Simple 0–3 milestone labels *only if needed* |
| Long | `Protect Helsinki residents while keeping integrity` | Named character aspiration, revisable without punishment |

- A goal is **player-owned** (sometimes declared by the PC, sometimes inferred with explicit player acceptance) and may change after revelations. No massive XP farming for completing routine chores; CWN progression remains canonical.
- The pre-incarnate Wanderer mission is **GM-secret authored plot**, **not** a selectable starting `Long Goal` and cannot leak into the early player UI. Act IV revelation and campaign ending remain gated.
- Preserve the existing goal issue's schema and migration path; this draft is a semantics proposal, not a replacement database.

### C. Reputation: per faction, from −4 to +4
- Create a reputation entry **only when an event establishes actual reputation with the named faction**. No global reputation by default. `Europol:+1`, `Finnish Police:-1`, `Local Mutual Aid:+2` can coexist. Not everyone in a faction necessarily knows or agrees.
- Levels are **author's proposed scale**: `−4` actively vilified → `−2` distrusted → `0` recognized neutral → `+2` respected → `+4` celebrated/insider. Specific thresholds and effects require Tomi's approval. Absence ≠ 0: *unknown* is distinct from *known neutral*.
- Add metadata `public|internal|secret`, `evidence`, `last_contact`, `source_event` and optional decay policy. Reputation does not grant free authority or override Finnish police jurisdiction; it influences access, introductions, social reactions and stakes.
- Treat **institutional/collective** reputation separately from **personal** rapport, and from **cosmic StO**. StS factions may regard the protagonist as an enemy after discovering Wanderer identity; they are not joinable.

## Resolution policy (compatible with CWN)
1. Tags provide **fictional positioning** before rolls: known contacts, scene permissions, NPC motive and narrative consequences.
2. When an actual skill check is needed, CWN's original 2d6 + relevant skill + attribute modifier applies; an optional **single situational ±1** is permissible *only if the approved tag text explicitly grants it* and ordinary CWN stacking conventions allow.
3. Important core investigation clues follow the established competence/access/inquiry boundary; no tag grants unlimited evidence or open exit conditions.
4. A personality change requires a named event and player-visible reflection. Do not invisibly auto-tag illegal or romantic decisions as a permanent trait.
5. Use ordinary human choices, substance dependence, romance, politics, professional corruption and social trust as story complications, **never** as a route to StS for the fixed StO Wanderer protagonist.

## Tiny tabletop examples
**A difficult interview:** The rookie has `Europol:+1 (internal)` and `Finnish Police:-1 (local unit)`; a Finnish officer can be annoyed while the employer remains satisfied. The PC may request cooperation under CWN Talk/Connect; neither tag supplies a warrant. An established `Patient Listener-1` might change the NPC's initial response, with no check modifier unless explicitly designed.

**Choosing a goal:** `Short Goal: Submit the evidence report` is completed; `Medium Goal: Repair trust with colleague` remains active; `Long Goal: Stay useful to ordinary Helsinki residents` can be reevaluated after fourth-density awakening. No cosmic alignment check or goal-experience farming.

**Pacifist tension:** the player has deliberately adopted `Pacifist-2` as a binding personal rule. During armed confrontation, player and GM discuss the authored retreat/surrender constraint; if the player has *not* opted in, the tag instead prompts a difficult choice and social cost rather than forcing the avatar to flee.

## Future Python data/interface proposal (NOT CODE)
`add_tag`, `update_tag`, `expire_tag`, `query_by_kind`, `get_reputation(character,faction)`, `record_goal_milestone`, `derive_scene_permissions`, `apply_approved_single_modifier`. Require immutable source-event log, snapshot on scene change, UI visibility filters for secret tags. Integrate with existing tags/goal code instead of a new central state store.

## Alternatives/questions for author
- Should personality strengths be `0–2` only, `−2…+2`, or loose descriptive tags? Author examples imply ordered levels, but exact range remains open.
- Is `Pacifist-2` *binding* even if player disagrees mid-scene, or a strong roleplaying prompt? Recommend opt-in binding constraints only.
- Should a known reputation score `0` appear, or store only nonzero entries? Author says **only after reputation earned**, so missing and neutral must stay distinct.
- What rewards, if any, attach to goal completion? Prefer narrative/story permissions before extra XP.
- Can one event change multiple reputation factions, and how are their knowledge channels modeled? Proposal: source-event propagation, not instant global broadcast.
- Which extant tag/goal API should be adapted and which code owns it? Audit before implementation.

## Source and status notes
- Author-origin mechanics: [BIONICS.md](../../design/BIONICS.md), #1137, earlier tag/goal issues.
- WN baseline: [CWN immutable core](../rules/CWN_IMMUTABLE_CORE_1068.md); [Europol frame](../world/EUROPOL_HELSINKI_1114.md).
- This subsystem makes **no scientific claim** about personality prediction from physiology. Personality/goal/reputation tags are **fictional narrative records**, not validated psychological instruments.

**Next gate:** author revision first. There is no automatic translation from these tags to positive/negative polarization. Rulebook and Python can be changed only after explicit approval.
