# Issue #482 — acceptance record

**What this file is.** The criterion-by-criterion verification of the two-layer Fate work that #482
authorises, read against the merged artifacts on `main`. The issue's own last criterion is *"commit
through a focused PR; seek design review before canonizing unresolved strategic-skill details; close
only after accepted and verified"*, so this record exists to make the state checkable — **including
the one item that is not mine to verify and is the reason the issue stays open.**

**What landed it.** PR **#484** (the two skill layers, the proposed roster, the faction turn),
PR **#485** (the verified Terra Invicta mission model as a reference column) and PR **#486** (the
capability gate enforced, and both scales through the scene resolver). A fourth PR on the same issue,
**#483**, was an independent implementation of the same architecture; it was closed in favour of
these, with **two of its ideas adopted and credited**: the capability gate as a first-class parameter,
and the observation that a context-checked action should carry the kernel's scene features rather
than call the bare dice.

## The nine acceptance criteria

| # | Criterion | Evidence | Status |
| --- | --- | --- | --- |
| 1 | Read the supplied **Fate Core**, **Transhumanity's Fate** and **Eclipse Phase 2e** rulebooks, using their actual mechanical sections | **Fate Core:** verified from the SRD — the default list is 18 skills and the Great pyramid rates ten ([skills](https://fate-srd.com/fate-core/skills)), each of the eighteen per-skill pages resolves, the four actions and the invoke/refresh rules are on their own pages, licence CC BY 3.0 on the SRD's licensing line. **Eclipse Phase 2e:** the six aptitudes come from the issue's own table. **Transhumanity's Fate: the work's own skill list is verified** — 24 names, matching the recorded names one for one, checked against its front-matter skill-list pages as reproduced in three independent copies; the count once recorded as unresolved is a units error (25 *starting skill points*, not 25 skills). The purchased book's prose was still not read and is not needed for the list. The evidence is the two records that name their own basis: `transhumanitys_fate_mapping` (24 names, each marked individual / strategic / both with a reason) and `transhumanitys_fate_verification` (the sources checked; the parts that stay unverified, including the exact count). See the criterion below and the revised evidence in [`SKILL_LAYERS_AND_DECISIONS.md`](../../strategy_game/docs/SKILL_LAYERS_AND_DECISIONS.md) §4 (PR #489) | **met** (list verified; the book's own prose not read and not needed) |
| 2 | Create a playable NoöPunk-specific crossover rulebook, without importing EP/TF setting or copying licensed lore | [`strategy_game/RULEBOOK.md`](../../strategy_game/RULEBOOK.md) — eleven sections covering the issue's suggested nine-part organisation (scope/licensing, the sheet, individual skills, strategic skills as a proposal, dice and actions, aspects/points/stunts, stress and recovery, play at both scales with worked examples, advancement and deferrals, Python API). No Firewall, Fall, exsurgent origin, resleeving presumption, EP faction or EP technology baseline appears anywhere; §1 states the exclusion and the attribution | **met** |
| 3 | Add exactly the six named **COG, INT, REF, SAV, SOM, WIL** individual Fate skills, documented and represented in Python | [`rpg/skills.py`](../../strategy_game/rpg/skills.py) `INDIVIDUAL_SKILLS` carries the six with the issue's own scope text; the rulebook §3 tabulates them. They are used as **Fate-rated skills**: no percentile value, no second attribute scale, and **no duplicate** — the parallel Fate Core *Physique*/*Will* do not survive beside SOM/WIL (§3.1 crosswalk). **Their starting allocation is recorded as unspecified** rather than filled in: Fate Core's great pyramid assigns ten distinct ratings and cannot apply literally to six skills, so §3 says so and defers the allocation and advancement rule (PR #487, a sibling's correction of an error in the first draft; register item 10, queue row D23) | **met** (allocation deliberately deferred) |
| 4 | Research TI Councilors; propose a compact *strategic skills* roster and a mapping from the remaining TF skills; record what is a proposal and what has author approval | [`data/strategic_skills.json`](../../strategy_game/data/strategic_skills.json) + [`strategic_skills.py`](../../strategy_game/strategic_skills.py): seven proposed skills, an 18-row Fate-side mapping, the secondary-source, names-only, uncertainties-preserved `transhumanitys_fate_mapping` (24 names) that **covers the "mapping from the remaining TF skills" this criterion names**, the verified `terra_invicta_missions` reference column, and **two** verification records stating what was verified and what was not (`terra_invicta_model`, `transhumanitys_fate_verification`). `status: PROPOSAL` and `provenance.approved: false`; the loader refuses the file if that stops being true; **nothing numeric is taken from TI** and the refusals are listed by name | **met as a proposal** — the roster is deliberately **not** approved (see the last criterion) |
| 5 | Reusable Python RPG core: seeded Fate rolls, four actions, aspects/Fate points, stunts, stress/consequences, separate action contexts | the approved kernel [`rpg/fate.py`](../../strategy_game/rpg/fate.py) plus [`rpg/skills.py`](../../strategy_game/rpg/skills.py): `ActionContext.INDIVIDUAL` / `FACTION_AGENT` select the list, a cross-layer name is refused before any dice, `Character` gained `strategic_skills`, `refresh` and `refresh_to_baseline()`, and a context-checked action runs through the scene resolver so free invokes, rerolls and the permission flag work at both scales | **met** |
| 6 | Integrate cleanly with the existing `strategy_game/` scaffolding, #389 and #461, preserving **one leader / four agents** and **one strategic order per character** | [`rpg/roster.py`](../../strategy_game/rpg/roster.py): five seats, one action per **character** per turn (not per seat); the RPG layer still imports no strategy engine module and reads no roster file, per [`rpg/boundary.py`](../../strategy_game/rpg/boundary.py)'s pinned contract. `council.json`'s `roster_size` and `founder_authority` are **untouched** — the structure is implemented, neither question is settled | **met as structure** |
| 7 | Test individual and strategic resolution paths, competence gates and mechanical invariants; **do not write tests that enforce unapproved lore** | [`tests/test_rpg_skills.py`](../../strategy_game/tests/test_rpg_skills.py) — **57 tests**: contexts reading their own list, both directions of the cross-layer refusal, the unknown name refused rather than rated at zero, the pending-roster refusal, the four actions in both contexts, invokes/refresh, the capability gate before any spend, scene features, the five seats and the one-action turn, and the proposal's shape (not its prose). No document wording is asserted anywhere (#271) | **met** |
| 8 | Licensing/attribution documentation; distribution obligations verified before incorporating CC BY-NC-SA material; no copying of protected prose or artwork; Fate Core attribution correct | rulebook §1's three-source table (Fate Core CC BY 3.0 = chassis; TF and EP2e CC BY-**NC**-SA = design study and reference, no expression imported), [`rpg/ATTRIBUTION.md`](../../strategy_game/rpg/ATTRIBUTION.md) + [`rpg/attribution.py`](../../strategy_game/rpg/attribution.py), [`docs/ATTRIBUTION_POLICY.md`](../ATTRIBUTION_POLICY.md), and `docs/licenses/RELEASE_CLEANUP_AUDIT.md`'s packaging guard. No licensed PDF, artwork or NC-SA text is bundled, and **the distribution licence remains the author's decision** (#200 / row D10) — not chosen here | **met** |
| 9 | Commit through a focused PR; seek design review before canonizing unresolved strategic-skill details; close only after accepted and verified | focused PRs, all merged with CI green on their heads — **#484**, **#485**, **#486** for this work, plus **#487** and **#489** for the corrections they made to the same artifacts; the design review is **outstanding and is the author's** — **row D22** of [`AUTHOR_DECISION_QUEUE.md`](AUTHOR_DECISION_QUEUE.md) (*accept / amend / replace* the seven strategic skills and their mission kinds, with primary-source TF validation still desirable). **This closure is therefore not claimed and #482 stays open** | **PRs met; closure pending one decision** |

## Transhumanity's Fate source gap, resolved

The work's own **skill list is verified**: **24 names**, matching the `transhumanitys_fate_mapping` names one for
one, checked against its front-matter skill-list pages as reproduced in **three independent copies**. No
description, prose or artwork was reproduced - names and reasons only, the discipline this repository keeps for the
Terra Invicta reference column too, and for the same reason (CC BY-NC-SA).

**The count discrepancy is resolved, and it was a units error.** The figures the reproductions carried are the
work's starting **skill points** (it states a character starts with 25 points under a Great (+4) cap), not a count
of skills. Two reproductions appeared to disagree because they were answering different questions.

**What that changes, and what it does not.** The decision-relevant finding stands: the list is almost entirely
scene-shaped and consolidates into the six individual skills, so **the strategic seven cannot be derived from it** -
that layer is a reference-system-informed design choice, which is why it is a proposal. What the verification adds
is a clean crosswalk: the work **renames** Fate Core's *Physique* to **Somatics**, *Empathy* to **Kinesics** and
*Stealth* to **Infiltrate**, and folds *Contacts* and *Resources* into Cred, Civ Rep and Eye Rep - which is why the
shared names **Somatics** and **Will** mean something different on each side, and why exactly one of each survives
here (`RULEBOOK.md` §3.1).

Still unverified, and not asserted: whether any skill changed between printings (the copies agree but may share an
edition), and the work's prose and setting material, which this crossover does not use.

## Not claimed, and not part of these criteria

* **The six skills' starting allocation is not specified.** Fate Core's great pyramid assigns ten
  distinct ratings and cannot be applied literally to a six-skill list, so the rulebook §3 records the
  allocation as **not yet specified** and defers the allocation-and-advancement rule (queue row D23).
  Nothing here invents a six-skill distribution, and no test pins one.
* **No strategic rule, roster, mission kind, probability, cost or effect is approved.** The roster is
  `status: PROPOSAL`; the mission kinds it names are proposals; nothing moves any of the six
  quantities.
* **Gate B (political simulation) and Gate C (strategy rules)** of
  [`RULE_SYSTEM_RESEARCH.md`](../../strategy_game/docs/RULE_SYSTEM_RESEARCH.md) are untouched. #482
  opens the RPG half of Gate A, not the rest.
* Deliberately deferred, and registered in
  [`SKILL_LAYERS_AND_DECISIONS.md`](../../strategy_game/docs/SKILL_LAYERS_AND_DECISIONS.md) §5:
  advancement, the full stunt catalogue, equipment statistics, the GM's adjudication beyond the stated
  permissions, whether the strategic map crosses the pinned `LeaderRPG` payload, whether the older
  kernel demonstrations are restated in the six, and whether EP2e's simulationist material is ported.
* **The kernel's own demonstrations** (`demo_investigation`, `demo_netrunning`) still use plain
  Fate skill names, because that layer is setting-independent; that is recorded as a decision, not
  presented as the crossover's skill list.

## Verification method

Original evidence was inspected on `main` (`f69e670`); the TF mapping and decision queue were subsequently reconciled with newer `main`, plus execution for every claim that is executable:
both suites were run on a **fresh clone of `main`** — root **531 tests OK**, strategy **1262 tests OK**
— and the workflow's own steps (`python -m unittest discover -s tests -p "test_*.py"`,
`-s strategy_game/tests`, and the view-model, text-runner and Concordia smoke checks) pass locally.
CI is green on `main` and on all three merges (`Python game-code checks`, CodeQL). One guard was
**sabotage-proven** rather than merely repaired: the RPG boundary test now parses `fate.py` with `ast`
and fails on an `import ..session` and on a reference to `WorldState`, with the restore verified
byte-identical by sha256.

— Ai (愛)
