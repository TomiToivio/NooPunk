# Rules-engine license audit (issue #200)

What the games named in #200 actually permit, checked at the **publisher or the SRD itself**
rather than from a mirror, a wiki, or a community claim that a game "is CC". This is the
finding the issue asks for, and it is the gate that has to pass before any text is ported.

Machine-readable record: [`data/sources/rules_engine_rights.json`](../../data/sources/rules_engine_rights.json).
Every date here is real-world metadata, not in-world canon. **Nothing has been imported:**
no third-party text, table, art or code is present in this tree.

This file is the sibling of `EXTERNAL_SOURCE_LICENSES.md` (issue #60, the Eclipse Phase
question). That one governs source material for the *existing* EP-derived homebrew paths;
this one governs the **rules-engine direction** and the CC release.

## The one rule that decides everything

An entry may be adapted into a NooPunk release only when its license permits **commercial**
reuse **and** is compatible with the chosen CC license.

**A NonCommercial term cannot enter a commercially reusable CC BY/BY-SA release. OGL Open
Game Content cannot be relabelled as Creative Commons.** Neither is repaired by rewriting a
little; both are about permission, not wording.

## Findings

| Source | Verified license | Into a CC rulebook? |
| --- | --- | --- |
| Fate Core / FAE SRD (Evil Hat) | **CC BY 3.0** (Unported) | **Yes** — adapt with attribution |
| The Veil / Cascade (Samjoko) | **CC BY-SA 3.0** (Unported) | **Yes** — shares-alike, compatible with BY-SA 4.0 |
| Cities Without Number **SRD** (Sine Nomine) | **CC0 1.0** | **Yes** — no obligations (SRD only, not the book) |
| Stars Without Number SRD (Sine Nomine) | CC0 *indicated*, not verified here | **Not yet** — principles only until read |
| Fudge **SRD** (FudgeRPG) | **OGL 1.0a** | **No** — principles only |
| Fudge 1995 core PDF | special limited license | **No** |
| Psi-Punk **SRD** (Accessible Games) | **OGL 1.0a** + Product Identity | **No** — principles only |
| Eclipse Phase 2e (Posthuman) | **CC BY-NC-SA 4.0** | **No** — NonCommercial |
| Transhumanity's Fate (Posthuman) | CC BY-NC-SA 3.0 *(from the issue; not re-verified)* | **No** — NonCommercial |
| Apocalypse World (Lumpley) | **no CC grant**; all rights reserved | **No** — principles only |
| CP RED / 2020, Shadowrun, CY_BORG, GURPS, NCO, Metro: Otherscape | proprietary | **No** — excluded entirely |

## The three verified-as-adaptable, and their exact scope

### Fate Core SRD — CC BY 3.0, confirmed at the publisher

`fate-srd.com/official-licensing-fate/cc` describes the license as *"the most liberal one
possible"* and explicitly **not viral**: derived work need not be opened. Attribution is the
whole obligation, and each SRD file carries the required attribution bloc at the top.

Compatibility with CC BY-SA 4.0 runs **one way**: CC BY text may be adapted into a BY-SA work
with attribution; that says nothing about going the other direction.

### The Veil — CC BY-SA 3.0, and a trap inside it

The work's own statement: *"The text of The Veil: Cascade is licensed under the Creative
Commons Share-alike 3.0 Unported (CC BY-SA 3.0)."*

**The trap:** the same statement records that some moves are *"tweaked or lifted straight
from Apocalypse World ... used with his permission."* That permission was granted **to that
project**. It does not travel with The Veil's license, so the AW-derived portions inside The
Veil are **not** available to NooPunk even though the surrounding text is. Do not copy them.

This is also the concrete reason the recommended target is **CC BY-SA 4.0 and not CC BY 4.0**:
BY-SA 4.0 accepts BY-SA 3.0 material in the adaptation pathway, so The Veil can be drawn on
at all. Choosing CC BY 4.0 would close that door.

### Cities Without Number SRD — CC0, verified on the publisher's own storefront

The listing states the SRD is *"provided under a Creative Commons 0 waiver allowing
downloaders to copy, modify, reproduce, or otherwise use it for both personal and commercial
purposes. Later versions of this file may be released, but any released version may be used."*

**Scope matters more than the license here:** the waiver covers **the SRD**, not the published
book. The community summary of the same listing puts it plainly — *"the full SRD, but not all
parts of the original book."* Use the SRD, and only the SRD.

## The two that must not be copied, and why the distinction is not pedantry

**Fudge (OGL 1.0a).** `fudgerpg.com` confirms the SRD is released under the OGL, carries OGL
1.0a in Appendix I, and lists three compliance duties (include the license, update Section 15,
designate Open Game Content vs Product Identity). The 1995 core PDF is a **separate** work with
its own restrictive free-distribution license — the OGL release does not cover it.
Fudge's contribution to NoöPunk is the **Attribute/Skill distinction and the trait ladder**:
procedures, which may be implemented independently. Its **expression** may not enter a CC-only
rulebook without separate written permission, and the issue says exactly that.

**Psi-Punk (OGL 1.0a + Product Identity).** Two independent exclusions stack: OGC cannot be
relicensed as CC, *and* the SRD's own legal page reserves the Introduction, the setting chapter
and the sample adventure as Product Identity. Its value to NoöPunk is structural — it shows a
psychic/cyber/astral system built on a Fudge-style split — and structure is not expression.

## Apocalypse World: a lineage is not a license

`apocalypse-world.com/pbta/policy` says: *"If you're using our words, you need our
permission, per copyright law. If you aren't using our words, you don't need our permission."*
The 2010 core carries an all-rights-reserved notice. So "PbtA" is a **descriptive design
lineage**, not a grant. NoöPunk may call itself PbtA-inspired when that is accurate, and must
not imply affiliation or licensing.

## What is still unverified, stated as such

- **Stars Without Number's SRD** — community reports and the publisher's sibling listings (CWN,
  Worlds Without Number) all describe a CC0 waiver, but the SWN SRD's **own** listing was not
  located in this pass. Recorded as `principles-only` and promoted only after someone reads its
  license page. This is deliberate: the issue forbids treating "user reports CC" as a finding.
- **Transhumanity's Fate** — the entry is taken from the issue's classification; the material is
  not on disk and its own license page was not fetched.
- **The Veil's publisher site** — the license statement was read from the work itself in two
  independent copies; `samjokopublishing.com` was not fetched in this pass.

## Consequences for the repository

1. **The target is CC BY-SA 4.0** (see the direction record). It is the only choice that keeps
   both compatible adaptation pathways open.
2. **No LICENSE file is added by this audit.** Relicensing is a one-way legal act for the
   author, not an agent.
3. **Code is licensed separately** from rule text/data/art, as the issue requires — a CC
   license is the wrong instrument for source code.
4. **Every future port** adds a ledger entry before the text lands, not after.
