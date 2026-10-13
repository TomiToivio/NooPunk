# #421 — enacting a licence choice, and the commercial model

**Scope:** items **1** (the licence pair) and **2** (the commercial model) of #421 — the two that are
**not** complete, and the only two that ever needed anything other than work: they need a **decision**.
Items 3 (release-time clean-up) and 4 (attribution policy) are done — #429 and `docs/ATTRIBUTION_POLICY.md`.

**What this is.** The decision brief: what the choice is between, what the consequence of each option is,
and **exactly what happens the moment the choice is made** — so the decision costs one word rather than an
afternoon.

**What this is not.** **It does not choose.** Agents are forbidden to select a licence or to create
`LICENSE`/`NOTICE` (row **D10**), and a test asserts those files do not exist. Nothing here is a legal
clearance, and the recommendation it points at is the *existing* one, not a new opinion.

---

## 1. The choice, and what each option costs

The recommendation already exists and is mechanical: `ISSUE_200_LICENSE_AND_NOTICE_PLAN.md` §2 recommends
**CC BY-SA 4.0** for content because **BY-SA 4.0's compatibility pathway accepts both CC BY 3.0 (the Fate
Core SRD) and CC BY-SA 3.0 (The Veil)**. Choosing **CC BY 4.0** instead is legitimate and buys maximum
downstream permissiveness, at the cost of The Veil ceasing to be an *adaptable* source.

| Decision | Options | What it commits the project to |
| --- | --- | --- |
| **1a — software licence** | MIT · Apache-2.0 · GPL-family | MIT/Apache are permissive: a derivative can be closed. GPL keeps derivatives open, which matches the commons framing but blocks some storefront/engine combinations. Apache-2.0 adds an explicit patent grant. |
| **1b — content licence** | **CC BY-SA 4.0** *(recommended)* · CC BY 4.0 | BY-SA keeps The Veil adaptable and keeps derivatives open; BY is maximally permissive but closes that pathway. Both are compatible with shipping The Veil's text as *attributed, unmodified* material. |
| **2 — commercial model** | free · paid · paid-with-free-earlier-builds | Open source does not forbid selling (§9). Nothing in the licence pair above prevents a paid release; the constraint that does bind is that **no NC-licensed material may be in the build**, which the guard already enforces. |

**The one hard constraint that is settled and not re-opened:** Eclipse Phase-derived material (CC BY-NC-SA)
can never enter a distributable build. The guard flags it, `docs/ATTRIBUTION_POLICY.md` records it, and no
licence choice changes it.

## 2. Enactment — what happens when the choice is made

Recorded here so the decision is reversible to inspect and cheap to execute. **The author makes the choice;
the enactment is then mechanical.**

1. **Create the two files.** `LICENSE` (or `LICENSE-code` + `LICENSE-content`, if you prefer the pair
   explicit in the filenames) and `NOTICE`, carrying: the licence text or a stable reference to it, the
   attribution blocks from `ISSUE_200_LICENSE_AND_NOTICE_PLAN.md` §3 (Fate Core CC BY 3.0 in full, The
   Veil CC BY-SA 3.0, Cities Without Number CC0), and the class→licence mapping.
2. **Set the policy.** In `data/licenses/release_packaging_policy.json`, replace each class's
   `"licence": "author-decision…"` with the selected instrument, and set `author_decision_open` to
   `false`. **That single field is what clears the release gate.**
3. **Update `docs/ATTRIBUTION_POLICY.md`** — it currently says no licence is selected; it gains one row
   per licence and the concrete attribution strings.
4. **Close row D10** and let S1 publishing work (row D14) proceed.

**Three tests will change, by design — this is the checklist that proves the enactment happened:**

| Test | Now | After |
| --- | --- | --- |
| `test_the_author_decision_is_still_recorded_as_open` | asserts `True` | must be updated to `False` |
| `test_the_status_says_the_decision_is_still_open` | asserts the open-status string | updated |
| `test_no_licence_or_notice_file_has_been_created` | asserts **absent** | must be updated to assert **present** |

**Why they are written that way:** they exist to make a pre-decided release impossible. When the decision
lands they *must* fail, loudly — that failure is the signal that the enactment is real rather than
prose. **A licence file that appears without these tests changing is a licence file nobody meant to ship.**

## 3. The commercial model (item 2)

Item 2 is genuinely open, and it is smaller than it looks. Per §7a and §9, open source does not forbid
selling: the game's **source is public** and its **content is licensed**, but distribution, price and
storefronts are the author's. The constraints that actually bind are few:

- **No required service, proprietary engine or paid model provider** (§7a). A commercial release may not
  introduce one.
- **The NC-SA exclusion** (§9) — unchanged by any price.
- **Storefront packaging is S1 engineering, not administrative trivia.** A store page, platform builds and
  packaging requirements are *work*, and they are row D14.
- **`LICENSE`/`NOTICE` must ship inside the artifact**, which is why the guard checks a release *set*
  rather than the working tree.

**The honest position:** the commercial model can stay undecided longer than the licences can, because
**price does not change what may legally be in the build** — the licence pair and the NC-SA exclusion do.
If a decision is deferred, defer this one.

## 4. What this does not do

- **It selects no licence** and creates no `LICENSE`/`NOTICE`. D10 governs; a test enforces it.
- **It re-opens no settled policy.** VISION.md §7a/§9 and the NC-SA boundary are unchanged.
- **It gives no legal advice.** The compatibility facts (BY-SA 4.0 accepting BY 3.0 / BY-SA 3.0) are
  restated from `ISSUE_200_LICENSE_AND_NOTICE_PLAN.md` §2, where they were already recorded.
- **It is not tested.** Prose carries no tests (#271); the *enactment* is testable, and the three tests
  above are where it will show up.
