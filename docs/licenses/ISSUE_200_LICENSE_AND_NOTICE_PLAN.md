# Issue #200: licence, NOTICE and attribution plan

**Status: PROPOSAL — awaiting the author's selection. No `LICENSE` file is added by this
document, and no agent will add one.** Relicensing a repository is a one-way legal act; the
issue requires the choice to be made explicitly, and that choice belongs to the author.

Companions: [`ISSUE_200_CC_RELEASE_GATE.md`](ISSUE_200_CC_RELEASE_GATE.md),
[`../sources/GAME_SYSTEM_RIGHTS.md`](../sources/GAME_SYSTEM_RIGHTS.md),
[`../../data/sources/game_system_rights.json`](../../data/sources/game_system_rights.json).

This is the itemization #200 asks for: *"rule text/data/art/worldbook license decisions should be
itemized"*, plus *"a detailed LICENSE/NOTICE/attribution map"*.

## 1. Artifact classes, itemized

NoöPunk is not one artefact, and the issue is explicit that one licence cannot cover it: a CC
instrument applied automatically to source code is a category error, and the data files raise a
question the rulebook does not.

| Artifact class | Paths | Proposed licence | Status |
| --- | --- | --- | --- |
| Rulebook prose + original setting/worldbook | `RULEBOOK.md`, `rulebook/**`, `FACTIONS.md`, `README.md`, `THEORY.md` | **CC BY-SA 4.0** (alt: CC BY 4.0) | **author decision** |
| Audit / provenance records | `docs/sources/**`, `docs/licenses/**` | same as the rulebook | author decision |
| Design records | `docs/design/**` | same as the rulebook | author decision |
| Game data | `data/**` (`core.json`, `skills.json`, `unsa_academy.json`, `campaign_skill_fields.json`, `world/**`) | same as the rulebook — it is *rule text in another syntax*, not code | author decision |
| Source code | `src/**`, `scripts/**`, `tests/**` | **separate software licence**: MIT / Apache-2.0 / GPL | author decision |
| Fixtures, deploy descriptors, Godot scenes | `fixtures/**`, `deploy/**`, `scenes/**`, `project.godot` | follows the code licence; Godot project files are code, not prose | author decision |
| Third-party art/assets | *(none present)* | n/a | **nothing to license: no third-party art is in the tree** |

**Why the data files are grouped with the rulebook and not with the code:** `data/rules/*.json`
*is* the rule text in machine-readable form (the six STATs, the Skill vocabulary, the Academy
package). Splitting it under a software licence would licence the rules twice under two
instruments with different obligations, which is the kind of ambiguity a release gate exists to
prevent.

## 2. Recommended selection, and the cost of the alternative

**CC BY-SA 4.0.** The reason is mechanical, not ideological: BY-SA 4.0 accepts **CC BY 3.0** and
**CC BY-SA 3.0** material in its compatibility pathway, which is exactly the Fate Core SRD
(BY 3.0) and The Veil (BY-SA 3.0) route.

**If CC BY 4.0 is preferred instead, The Veil's CC BY-SA 3.0 text may not be adapted** — the
BY-SA pathway closes, and the Narrativist corner loses one of its two named sources as an
*adaptable* one. That is a legitimate choice (maximum downstream permissiveness), but it should
be made knowing the cost.

Either way the **rulebook keeps its own choice and the code gets a separate licence.**

## 3. Required attribution blocks

Three sources could be adapted rather than merely imitated. Attribution text belongs in the
project's `NOTICE`/attribution file **and** on the copyright page of any release.

### Fate Core / FAE SRD — CC BY 3.0 (attribution required)

> This work is based on the Fate Core System and Fate Accelerated Edition, products of Evil Hat
> Productions, LLC, developed, authored, and edited by Leonard Balsera, Brian Engard, Jeremy
> Keller, Ryan Macklin, Mike Olson, Clark Valentine, Amanda Valentine, Fred Hicks, and Rob
> Donoghue, and licensed for our use under the Creative Commons Attribution 3.0 Unported licence.

The licence is **not viral**: NoöPunk's derived work need not be open. Attribution is the whole
obligation. Logo/art are **not** covered by the text grant.

### The Veil — CC BY-SA 3.0 (attribution + ShareAlike)

> Contains material adapted from *The Veil*, by Fraser Simons (Samjoko Publishing), licensed under
> the Creative Commons Attribution-ShareAlike 3.0 Unported licence.

**ShareAlike consequence:** the adapted portions — and the work as a whole — must remain under a
compatible ShareAlike licence. This is one more reason the recommended target is BY-SA.

> **Per-portion exclusion, not an attribution footnote:** The Veil's own statement records that
> some moves are *"tweaked or lifted straight from Apocalypse World … used with his permission"*.
> That permission was granted **to that project**. Those portions are **not** covered by The
> Veil's licence and may **not** be adapted even though the surrounding text may be.

### Cities Without Number SRD — CC0 1.0 (no attribution required)

CC0 places no attribution obligation. A **courtesy credit** is still proposed, because
acknowledging the inspiration is the project's stated intent and because CC0 is a waiver, not a
request for anonymity:

> Game procedures informed by the *Cities Without Number* System Reference Document (Sine Nomine
> Publishing), released under CC0 1.0 Universal.

**Scope reminder that belongs in the NOTICE too:** the CC0 waiver covers the **SRD**, not the
published book.

## 4. Exclusions — no expression from these sources

These may be named as design influences and credited. **No text, table, formula or art from them
may enter the release.**

| Source | Why excluded |
| --- | --- |
| **Fudge SRD**, **Psi-Punk SRD** | OGL 1.0a Open Game Content cannot be relabelled Creative Commons |
| **Fudge 1995 core PDF** | separate restrictive free-distribution licence |
| **Eclipse Phase 2e**, **Transhumanity's Fate** | CC BY-NC-SA — NonCommercial cannot enter a commercially reusable release |
| **Apocalypse World** | no CC grant; the PbtA policy is a per-request permission, not a licence |
| **Cyberpunk RED / 2020, CY_BORG, Shadowrun, GURPS, NCO, Metro: Otherscape** | proprietary; out of the rule bases entirely |
| **Computer-game references** (Citizen Sleeper, Disco Elysium, Dragonfall, Midnight Protocol, Blade Runner, Observer, 2077, Deadeye) | abstract design lessons only; no assets, code or proprietary worlds |

## 5. The licence scan the issue requires before the release

*"Require reproducible tests, license scan and valid attribution before marking done."*

A release gate needs an executable check, not a promise. What such a scan must assert:

1. each adaptable source has its attribution block present in the NOTICE;
2. each excluded source is listed in the exclusions, with its reason;
3. no file in the tree carries an OGL/NC/proprietary header or an unrecorded third-party notice;
4. no `LICENSE` file exists until the author selects, and once selected, that it matches the
   ledger's recorded choice;
5. the `data/` and code split from §1 is respected.

Items 1, 2 and 4 are mechanically checkable and are guarded by
`tests/test_issue200_license_notice_plan.py`. **Items 3 and 5 need a scan over the tree for
third-party notices and licence headers**, which is a follow-up: it is a text-matching problem
over ~400 files and belongs in its own increment, not smuggled into a documentation change.

## 6. What this plan does not do

- It does not select the licence, add a `LICENSE`, or relicense anything.
- It does not claim any third-party expression is present — none is.
- It does not resolve the unverified entries (Stars Without Number; see the audit).
- It does not decide the code licence, the art question (moot: no third-party art present), or
  any mechanic.
