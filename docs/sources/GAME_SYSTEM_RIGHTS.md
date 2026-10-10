# Game-system rights audit (issue #200)

What may enter a Creative Commons NoöPunk ruleset from the tabletop systems issue #200 names,
and under what terms. This is the first step #200 itself demands — **audit before deleting** —
and it deliberately changes no rules text.

Machine-readable record:
[`data/sources/game_system_rights.json`](../../data/sources/game_system_rights.json).
Companion to the Eclipse Phase set in
[`EXTERNAL_SOURCE_LICENSES.md`](EXTERNAL_SOURCE_LICENSES.md) (issue #60), which this file does
not repeat.

Every finding below is a **dated real-world observation**, not in-world canon.

**Nothing has been imported.** No rule text, table, formula or artwork from any source here
exists in NoöPunk. This document exists so that a later port is a decision rather than an
accident.

## The licence decision is the author's, and it is still open

#200 names a recommended target (**CC BY-SA 4.0**) and an alternative (**CC BY 4.0**), and asks
for the choice to be explicit. It is recorded as **RECOMMENDED, NOT RATIFIED**.

The choice is not cosmetic — it decides which influences may be adapted at all:

| If NoöPunk ships as | Fate Core (CC BY 3.0) | The Veil (CC BY-SA 3.0) |
| --- | --- | --- |
| **CC BY-SA 4.0** | adaptable, with attribution | adaptable, via the one-way 3.0 → 4.0 upgrade |
| **CC BY 4.0** | adaptable, with attribution | **cannot** be directly adapted |

**Code is licensed separately** (MIT / Apache-2.0 / GPL). A CC licence is not a software
licence, and `AGENTS.md` §15.5's provenance rule already points the same way.

## Findings

| Source | Licence (as established) | May enter a commercial CC release? |
| --- | --- | --- |
| **Fate Core SRD** | **CC BY 3.0** — read directly | **Yes**, with attribution |
| **Cities Without Number SRD** | **CC0** — SRD only | **Yes** — scope-limited to the SRD |
| Eclipse Phase 2E | CC BY-NC-SA 4.0 (#60) | **No** — NonCommercial |
| Transhumanity's Fate | CC BY-NC-SA 3.0 | **No** — NonCommercial |
| Fudge OGL SRD | OGL 1.0a — **blocked** | **No** — not a CC grant, not relabellable |
| Fudge 1995 PDF | special limited licence | **No** |
| Psi-Punk | OGL 1.0a — **blocked** | **No** |
| The Veil | CC BY-SA 3.0 — **unverified** | Only if verified, and only under BY-SA |
| Apocalypse World | **no CC grant established** | Copy nothing; implement concepts |
| Stars Without Number | **unverified** | Not until verified |
| Cyberpunk RED / 2020, CY_BORG, Shadowrun, NCO, Otherscape, GURPS, The Sprawl, The Expanse | proprietary | **No** — design lessons only |
| Computer games (Sleeper, Elysium, 2077, Dragonfall, …) | proprietary | **No** — abstract lessons only |

### Fate Core SRD — verified, CC BY 3.0

`https://fate-srd.com/fate-core`. The page states the material is *"licensed for our use under
the Creative Commons Attribution 3.0 Unported license"*, and repeats the statement for Fate
System Toolkit and Fate Accelerated. Read directly on 2026-10-10.

Two notes worth keeping: attribution is required, and the **site chrome is not the licensed
text** — the page is `(c) Amazing Rando Design` *except where otherwise noted*, while the rules
text is Evil Hat's CC BY 3.0.

### Cities Without Number SRD — verified, CC0, and the scope is the point

Two independent readings agree:

- the **publisher blurb**, as carried by the SRD's storefront listings, states the document is
  *"provided under a Creative Commons 0 waiver allowing downloaders to copy, modify,
  reproduce"*;
- the SRD mirror states *"The SRD is a free, open-source, and public domain document"*.

`cwnsrd.gordianblade.com` renders client-side, so its own licence text could not be read as
static HTML — that is why the storefront blurb carries the weight here, and why this finding is
recorded with its method rather than as a bare assertion.

**The CC0 dedication covers the SYSTEM REFERENCE DOCUMENT.** It is not a finding that the full
commercial book is CC0. Use the SRD, and only the parts it covers. #200 warns about exactly this
conflation, which is why the entry is scope-limited rather than a blanket "CWN is free".

### Fudge and Psi-Punk — blocked, and blocked is not a finding

`fudgerpg.com` returns **HTTP 403** at the licensing page and **HTTP 406** (Mod_Security) at the
site root, and the **Wayback Machine reports no archived snapshot**. Psi-Punk's licence could
not be read at an authoritative source either.

Recorded as **blocked verifications**, following #60's discipline: a fetch failure must never
silently become "no licence, fine to use". Nothing may be asserted about these terms, and
nothing may be imported from them.

Even if verified, **OGL 1.0a Open Game Content is not a Creative Commons grant**. It cannot be
relabelled CC, and its obligations are incompatible with a pure CC release. Fudge is therefore
NoöPunk's **first-rank structural inspiration** — the separate Attribute/Skill split and
flexible quantitative adjudication — and nothing more, absent separate written permission.

Note also that the **Fudge OGL SRD and the 1995 Fudge PDF are two different licences**. Do not
conflate them.

### Apocalypse World — no CC grant established

The publisher's own pages for Apocalypse World carry no Creative Commons statement. Being the
origin of the PbtA design movement, and appearing in free references, **does not by itself
establish a CC grant for the book** — which is precisely the assumption #200 tells us to test.

This is *not* a finding that reuse is forbidden. It is a finding that reuse **of expression** is
not permitted on this evidence. Narrativist concepts are independently implementable:
implementing a described idea is not copying its expression. **PbtA** remains a descriptive
design designation, not a licence, and NoöPunk is not obliged to use PbtA's dice mechanic.

### Stars Without Number and The Veil — still unverified

Both were rate-limited or unreachable from this environment (SWN's search returned HTTP 202).
They stay **unverified** rather than guessed. The Veil's author-stated CC BY-SA 3.0 would be
compatible with a BY-SA 4.0 release and **in**compatible with a BY-only one, so the licence
decision above has to be made before its text could ever be adapted.

### The closed systems — out of the rule bases, into the references

Cyberpunk RED/2020, CY_BORG, Shadowrun, Neon City Overdrive, Metro: Otherscape, GURPS, The
Sprawl and The Expanse are proprietary or have no established CC grant. #200's instruction is
specific: they **must not remain bases or implementation sources** for NoöPunk rules. Naming
them as design influences stays welcome; copying does not.

The computer-game references are in the same category, with one extra rule attached: abstract
gameplay design lessons only, and **no generalised universal neural hacking** — that is a
setting rule as much as a licensing one.

## The audit inventory: what currently claims a closed-system dependence

This is the "audit before deleting" step. **Nothing has been deleted.** These are the live files
that currently name a closed system as a rules base, reference or calibration point.
`docs/archive/*` is excluded on purpose — archived files are historical and are not edited.

**Author-owned (preserved unchanged, reported to the author):**

| File | Line | Claim |
| --- | --- | --- |
| `AGENTS.md` | 263 | §13.2 poles: CY_BORG (Gamism), Cyberpunk 2020 (Simulationism), The Sprawl (Narrativism) |
| `AGENTS.md` | 304 | §15.3 names Cyberpunk 2020/RED as a selective design reference |
| `tests/test_design_principles.py` | 34 | pins `"Gamism": "CY_BORG"`, `"Simulationism": "Cyberpunk 2020"` as build-failing invariants |

**Live claims to reword once the licence is ratified:**

`README.md` 216, 258, 262 · `rulebook/4_SOCIAL.md` 47 · `rulebook/2_ATTRIBUTES.md` 139 ·
`docs/design/RPG_CONVERSION_REFERENCE.md` 6 · `docs/sources/SOCIAL_SYSTEM_SOURCES.md` 18 ·
`data/rules/core.json` 9 · `data/rules/conversion_matrix.json` 534 ·
`data/world/tech_matrix.json` 454 · `docs/index.html` 73

**Test coupling to the old framing** — these must move with the reword, not after it:
`tests/test_issue101_sources_dedup.py` 108 · `tests/test_issue58_tech_matrix.py` 271

## The authority conflict

`AGENTS.md` §13 (design balances) and §15 (independent-system rule) are **author-owned**, and
#200 supersedes their framing:

- **§13.2** fixes the canonical reference poles, including CY_BORG and Cyberpunk 2020;
- **§13.9** and **§15.2** fix issue #111's 1–10 STAT + 1–10 Skill + 1d10 core as the active
  baseline;
- **§13.8** explicitly forbids *silently* redesigning the balances.

#200's own text resolves the procedure: *"Update `AGENTS.md`/locked-rule policy by
author-approved process."* That is an author decision, not an agent one, so **this increment
preserves the lock and reports the conflict** rather than editing around it.

There is a second reason not to improvise here: `AGENTS.md` §13, `docs/archive/DESIGN_PRINCIPLES.md`
and `tests/test_design_principles.py` are guarded **as a set**. The test fails the build if they
drift out of agreement, so a change has to move all three together, deliberately.

## Migration order

1. **Audit** — this ledger and inventory. *(this increment)*
2. **Licence choice** — the author selects CC BY-SA 4.0 or CC BY 4.0, with an itemized
   LICENSE/NOTICE/attribution map.
3. **Authority update** — `AGENTS.md` §13/§15 + `DESIGN_PRINCIPLES.md` + `test_design_principles.py`
   move together.
4. **Reword claims** — the inventory above, auditing before deleting and preserving original
   NoöPunk text and lore.
5. **Kernel prototype** — Fudge/Fate 6-STAT + separate Skills; test additive scaling, modifier
   stacking, opposed checks, combat lethality, high-end PSI and cybertool disparity; approve one
   resolution method.
6. **Migrate legacy** — the historical 1d10 code, only after that decision, keeping the six STATs
   and the Skill taxonomy and specialist policy.
7. **Subsystems** — Physical/Social/Cyber/Psychic/Astral/NHI/Investigative, in original drafting.
8. **Gates** — reproducible tests, licence scan, valid attribution.

## What this does not claim

It does not claim any closed system is "free", does not claim an SRD's licence covers its book,
does not treat a blocked fetch as a licence finding, and does not license NoöPunk as anything.
It records what could be established, how, and on what date — so that the next step is a
decision rather than an accident.
