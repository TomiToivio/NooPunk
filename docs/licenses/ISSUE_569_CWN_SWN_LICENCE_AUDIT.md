# Issue #569 — CWN / SWN / WWN / AWN licence and attribution audit

**Status: audit record. No rule, code, or licence decision changes here.** Queue **D10** still owns
the choice of NoöPunk's own licence pair, and this file does not touch it.

Measured 2026-10-25 against `origin/main`.

---

## 1. Method

The rule this audit obeys is #200's, restated by #552/#556-era cleanup: **inspiration is not a
source.** Reading a book and writing down a mechanic are not the same act, and neither is importing
its text. So each source is classified per **document**, from its own licence page, with the URL and
access date recorded — never from memory, and never from "a sibling said it was CC".

The verdict vocabulary is the ledger's own (`data/sources/game_system_rights.json` →
`decision_vocabulary`), not an ad-hoc one, because the packaging guard reads that vocabulary and
fails when a policy decision is not in it.

---

## 2. The licence matrix

| Document | Decision | Permitted | Prohibited | Citation |
| --- | --- | --- | --- | --- |
| **Cities Without Number SRD** | `verified-public-domain` | SRD **text and mechanics**; commercial use; modification | The full commercial book, its art, its protected setting and faction names | Ledger `cities-without-number-srd`, checked **2026-10-10**; three agreeing readings incl. the publisher storefront quote |
| **Worlds Without Number SRD** | `verified-public-domain` *(new, this audit)* | SRD **text and mechanics**, verbatim and commercially | The full book, art, protected setting | `https://wwn.quadrifons.com/`, read **2026-10-25**. The SRD's own introduction: *"its copyright and related rights are waived via CC0"*; its purpose is *"to give other RPG designers an explicit document showing exactly what I consider to be freely-usable game mechanics"*, conferring *"the right to use its text verbatim in a commercial product"* |
| **Stars Without Number** | `blocked-unverified` | **Nothing.** Not the text, not the tables | Everything, until an SRD is located and read | Ledger `stars-without-number-srd`, checked 2026-10-10. No SWN SRD was located in two passes; Sine Nomine publishes a free **edition of the book**, which is not an SRD |
| **Ashes Without Number** | `blocked-unverified` *(new, this audit)* | **Nothing** | Everything, until an SRD is located and read | No AWN SRD located, **2026-10-25**. 2025 commercial release; the CWN/WWN CC0 dedications do not extend to it |

**The scope caveat is the point, and applies to both CC0 books:** an SRD dedication covers *the SRD*,
not the commercial book. `stars-without-number-srd` already recorded that CWN's CC0 is *"'the full
SRD, but not all parts of the original book'"*, and WWN's introduction says the same thing in its own
words — it is written *"largely devoid of examples or other instructional text"*, for designers, not
as a player resource.

**Net effect on #564:** the four-book family is **one book deep in practice**. CWN is the only source
this epic may adapt today; WWN's terms are now verified but its material is still *candidate* until
someone decides to use it; SWN and AWN are blocked.

---

## 3. Tree check — is anything imported that should not be?

**Result: no violation found.** What exists is *mention*, which is what the audit expects to find.

Six files use SRD-specific mechanic vocabulary (`Shock rating`, `Trauma Die`, `Trauma Target`,
`System Strain`, `Effort`, `Foci`):

| File | What it does | Verdict |
| --- | --- | --- |
| `legacy/ubiquitous_maniacs/docs/RULE_SYSTEM_BEST_OF_COMPARISON.md` | compares systems in Finnish; e.g. *"PSI:n kustannus ja kuormitus: Stars Without Number — Effort- ja System Strain -ajatuksen Noöpunk-muunnos"* | **Mention.** Mechanics are not copyrightable and naming one is not importing expression. No quoted or indented block; no claim to quote SRD text. |
| `docs/design/ISSUE_516_*` (3 files) | decision support comparing candidate chassis | **Mention / analysis.** |
| `docs/design/ISSUE_571_COMBAT_INJURY_TRAUMA.md` | reads the CWN SRD and paraphrases Shock/Trauma for measurement | **Paraphrase of mechanics**, permitted under CC0 and permissible even without it. |
| `docs/design/ISSUE_564_CWN_SWN_CHASSIS_MATRIX.md` | the disposition matrix | **Mention.** |

Nothing was deleted. A violation would have been **reported** rather than removed, per the issue.

---

## 4. What changed in the ledger

Two entries added to `data/sources/game_system_rights.json` (17 sources now):

1. **`worlds-without-number-srd`** — `verified-public-domain`. This closes a real gap: the
   `stars-without-number-srd` entry already observed *"the CWN and Worlds Without Number SRD listings
   both carry the CC0 waiver"*, but **WWN had no entry of its own**, so nothing in the repository
   actually recorded its terms. A claim inside another entry's prose is not a ledger entry.
2. **`ashes-without-number-srd`** — `blocked-unverified`, with the precedent recorded: a free edition
   is not an SRD.

The file round-trips byte-identically through `json.dumps(indent=2)`, verified before writing, so the
addition introduced no formatting churn.

---

## 5. Guard

`tools/release_packaging_guard.py` already reads this ledger:

- it **loads `data/sources/game_system_rights.json`** (`LEDGER_PATH`);
- it **reads `decision_vocabulary` from the ledger** rather than hard-coding a list, and fails with
  `excluded-decision-not-in-ledger` if the release policy names a decision the ledger does not
  define — so ledger and guard cannot silently diverge;
- its excluded-licence vocabulary is the ledger's, which is what makes `blocked-unverified` and
  `proprietary-out-of-scope` enforceable rather than decorative.

Audit run after the change: **PASS, 0 errors, 337 documented-licence warnings** — the same baseline
as before, so the two new entries neither broke the guard nor masked anything.

**What this means for a future import:** a blocked source is blocked *in the ledger*, and the guard
reads the ledger. Adding SRD text from SWN or AWN would therefore require editing the ledger to
promote the source first — a deliberate, reviewable act rather than an accident. That is the
"fails on violation" property the issue asked for, achieved by making the ledger load-bearing rather
than by adding a second, possibly disagreeing, guard.

---

## 6. Honest gaps

1. **The verbatim scan is sampled, not exhaustive.** The tree check inspected the substantive files
   that use SRD vocabulary and found no quoted blocks. A mechanical n-gram diff against the CWN and
   WWN SRDs would be stronger evidence, and would need the SRD text fetched and stored outside the
   tree. Not done here, and not claimed.
2. **AWN has no verified SRD.** Its decision stays `blocked-unverified` until one is read; the issue's
   own framing ("whatever SWN material is contemplated") applies doubly to AWN.
3. **Attribution is not yet drafted.** WWN being CC0 means no attribution obligation, and CWN's is
   likewise a public-domain dedication, but `docs/sources/ATTRIBUTION.md` should still record *that*
   the family influenced the design, for reader honesty rather than legal necessity. That is a
   separate edit, and it belongs with whatever the chassis decision authorises.
4. **This audit does not decide whether to use WWN material.** It records that we *may*. Whether the
   Foci/Effort/mutation procedures enter is the #564 ruling.

---

## 7. What this file does not do

- It does not select a licence for NoöPunk (**D10**).
- It does not import, delete or rewrite any third-party expression.
- It does not promote SWN or AWN, and it does not treat "the sibling listing says CC" as evidence.
- It does not approve a mechanic. Gates A–D stay open.
