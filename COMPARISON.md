# COMPARISON.md — Fate-first system comparison and conversion tables (issue #255)

**Status: IN PROGRESS.** This is a research/design gate, not a rule change. **No rule becomes
canonical from this document**, and nothing here authorises edits to `RULEBOOK.md`,
`data/rules/*` or any merged implementation. Author direction (2026-10-10): *drop Fudge/Psi-Punk
as a foundation; compare four families; write `COMPARISON.md` before committing to a core rules
conversion.*

> **Superseded premise, marked not deleted.** Issue #200's centre was **Fudge + Psi-Punk + Fate**.
> #255 supersedes that **for future comparison decisions**: Fudge is **out of scope** as an active
> source or chassis, Psi-Punk likewise, and #200's proposal is history rather than a baseline.
> Prior implementation work that assumed the old centre — including
> `docs/design/ISSUE_217_RESOLUTION_SEMANTICS_2026-10-10.md`, which proposed a partial-success
> policy for the Fudge-derived ladder — is **preserved untouched until audited** and is downstream
> of a premise that no longer holds. This document does not delete it and does not reconcile it.

---

## 1. Goals, design triangle, trade-offs, and scope boundaries

### 1.1 What this document is for

To decide **which family supplies the chassis**, how the four families' concepts map onto NoöPunk's
canonical six Attributes and 40 Skills, and what a conversion costs — *before* anything is locked.
The deliverable is a comparison, a set of conversion tables with honest labels, at least two
alternative numeric kernels with probabilities, and a rights matrix.

### 1.2 The GNS design triangle (a heuristic, not a classification)

GNS is a **subjective design map, not an objective rating**, and every game named here mixes
agendas. It is used here only to spread the design space.

| Position | Family | What it contributes | What it costs |
| --- | --- | --- | --- |
| **Centre — preferred chassis** | **Fate Core** (and *Transhumanity's Fate* as its transhuman application) | narrative aspects, stunts, stress/consequences, flexible actions | too simple as-is; **six separate Attributes AND separately rated Skills are mandatory**, which Fate Core does not provide |
| **Simulationist corner** | **Eclipse Phase 2e** | rich transhuman, hacking, PSI, injury, equipment and existential-risk procedures | too complex to import wholesale; **NC licence** |
| **Gamist corner** | **Cities Without Number / Stars Without Number** | concise playable OSR tactics, backgrounds/edges or foci, skills, mission and faction tools | avoid excessive D&D class/level assumptions; **SWN's free edition is not an open SRD** |
| **Narrativist corner** | **PbtA — The Veil, Worlds of Legacy** | fiction-first moves, hard choices, relationships, consequences, character drama | narrativist play must be explained to readers new to it; **AW itself grants nothing** |

Author's steer on the Narrativist corner: **The Veil is more thematically pertinent than
Apocalypse World** — and the rights matrix below shows this is also the corner where the licensing
is *cleanest* to reuse.

### 1.3 The trade-off this comparison exists to expose

**The preferred centre contains a NonCommercial work.** The author locks the chassis to *Fate Core
/ Transhumanity's Fate* — but **Transhumanity's Fate is CC BY-NC-SA**, so it cannot be copied into
NoöPunk's Creative Commons release. Fate Core itself is **CC BY and explicitly *not* viral**, so it
*can*.

That is the central tension of this issue and it shapes everything else:

- **Fate Core supplies the reusable chassis** (aspects, stunts, stress/consequences, flexible
  actions) with attribution as the only obligation.
- **Transhumanity's Fate and Eclipse Phase 2e supply design study, not expression.** They may be
  read to understand how a transhuman Fate game handles morphs, PSI, hacking and existential risk;
  their text may not enter the work.
- **Anything whose only clean source is an NC book must be re-expressed from the mechanics**, which
  is what CWN's CC0 SRD explicitly permits and what EP/Transhumanity's Fate do not.

### 1.4 Author-locked requirements (carried here as constraints, not proposals)

1. Base on **Fate Core / Transhumanity's Fate**; **do not copy NC-licensed Transhumanity's Fate
   text**.
2. Exactly **six independently rated Attributes — FIT / REF / INT / SOC / PSY / CYB** — and
   **Attributes distinct from Skills**.
3. **Preserve the existing NoöPunk Skill list** (`data/rules/skills.json`, 40 skills). Its lineage
   is *identified* as drawing on Transhumanity's Fate, Eclipse Phase and CWN — **the tables below
   verify alignment rather than assert that those systems have identical lists**.
4. **Research conversions before choosing** dice formula, attribute/skill scaling, difficulties,
   movement, stress or progression. No silent rule switches; no arbitrary 1:1 mappings.
5. **No Fudge** in recommended active sources or chassis; where history is compared, mark it out of
   scope and distinguish #200's outdated proposal.

### 1.5 Scope and licence boundaries (summary; the matrix is §7)

- **Reusable in a commercial CC release:** Fate Core SRD (**CC BY**, not viral), Cities Without
  Number SRD (**CC0**), Worlds of Legacy SRD (**CC BY**).
- **Reusable with a ShareAlike obligation:** The Veil / Cascade (**CC BY-SA 3.0**) — and it carries
  a **per-portion carve-out** (see §7).
- **Not reusable — design study only:** Eclipse Phase 2e and *Transhumanity's Fate* (**CC BY-NC-SA**).
- **No grant at all:** Apocalypse World (playbooks/moves/MC sheets are free to read; there is no
  universal PbtA SRD), and Stars Without Number's **free edition, which is a book, not an SRD**.
- **Out of scope:** Fudge, Psi-Punk (OGL) — superseded by #255.

---

## 7. Source and rights matrix

Verified **2026-10-10** at the sources linked by the issue. "Reusable" means *the text may be
reproduced in a commercial Creative Commons release*.

| Source | Edition / URL | Licence (as stated at source) | Commercial reuse | Obligations and scope limits |
| --- | --- | --- | --- | --- |
| **Fate Core SRD** | fate-srd.com — official licensing + CC-BY SRDs (ZIP) | **Creative Commons Attribution (CC BY)**, Unported | **Yes** | *"the most liberal one possible"*, explicitly **not viral** — derived content need not be CC. Requires the **attribution bloc supplied at the top of each SRD file** on the copyright page. |
| **Transhumanity's Fate** | legacy.eclipsephase.com releases page | **CC BY-NC-SA** (per EP licensing; page requires Fate Core) | **No** | NonCommercial blocks commercial reuse. **Design study only — no text.** |
| **Eclipse Phase 2e** | eclipsephase.com/cclicense | **CC BY-NC-SA** unless noted otherwise; "exceptions noted below" | **No** | Attribution to **Posthuman Studios, LLC**; derivatives under the same licence; NC blocks commercial. Per-release exceptions exist and must be checked per release. |
| EP online reference | eclipsephase.github.io | derived from EP | **No** | Inherits the NC licence of its source. |
| **Cities Without Number SRD** | DriveThruRPG product 452790 (Sine Nomine, official) | **CC0 1.0** — *"a Creative Commons 0 waiver allowing downloaders to copy, modify, reproduce, or otherwise use it for both personal and commercial purposes"* | **Yes** | The publisher states CC0 waives his claim on *"that specific verbiage"*. **Scope: the full SRD, but not all parts of the original book.** |
| **Stars Without Number (revised, free version)** | DriveThruRPG product 230009 | **No licence statement found** — a free edition of the **book** | **No** | **Free-to-read is not an open licence.** No SRD exists to verify; Sine Nomine publishes SRDs for CWN and WWN, not SWN. |
| **Apocalypse World** | lumpley.games/apocalypseworld | **No CC grant on the page** | **No** | Free playbooks, moves and MC sheets to *read*; the page grants no reuse. **There is no universal PbtA SRD.** |
| **Worlds of Legacy SRD** | ufopress.co.uk PDF | **Creative Commons Attribution (CC BY)** | **Yes** | *"all you need to do is put the attribution provided below clearly in your work"* — no fees, **no requirement to license your own work CC**. Licensing moniker: **"Worlds of Legacy"**. |
| **The Veil / Cascade** | samjokopublishing.com (text), DriveThruRPG | **CC BY-SA 3.0 Unported** | **Yes**, with ShareAlike | **Per-portion carve-out:** the licence paragraph itself records that *"some moves are either tweaked or lifted straight from Apocalypse World"* — that permission was granted **to that project**, so those portions are unavailable even though the surrounding text is licensed. Adopting The Veil text imposes **ShareAlike on the whole work**. |
| **Fudge / Psi-Punk** | — | OGL (cannot be relabelled CC) | **No** | **Out of scope** per #255. Retained only as history. |

### 7.1 What the matrix decides

1. **The chassis can be licensed cleanly.** Fate Core is CC BY and not viral, so a Fate-first
   NoöPunk can be released commercially under Tomi's chosen licence with an attribution bloc and no
   copyleft surprise. This is the single most important fact in this document.
2. **Two of the four families are study-only.** EP2 and Transhumanity's Fate are the richest
   sources for the transhuman and PSI material and **none of their text may be used**. Every
   mechanic traced to them must be re-expressed, and the tracing must be recorded.
3. **The Gamist corner is the most permissive and the least open at the same time.** CWN's SRD is
   **CC0** (no obligations at all), while SWN's free edition grants **nothing** — the two are
   routinely conflated because they share a publisher.
4. **The Narrativist corner is usable — but only one of its three routes is clean.** Worlds of
   Legacy (CC BY) is unconditionally reusable; The Veil (CC BY-SA) would put the whole work under
   ShareAlike; Apocalypse World grants nothing.
5. **A Fate Core + CWN + Worlds of Legacy combination is licence-compatible** with a commercial CC
   release. A Fate Core + The Veil combination forces ShareAlike on everything.

### 7.2 Retrieval honesty

- **Verified at source:** Fate licensing page and its CC-BY guide; EP licensing page;
  Transhumanity's Fate release page; CWN SRD official DriveThruRPG listing; SWN free-edition
  listing; Worlds of Legacy SRD PDF; The Veil licence paragraph; Apocalypse World page.
- **Not retrieved in this pass:** the EP licensing page's per-release *exceptions* list, and The
  Veil: Inheritance QuickStart's separate terms. Both are recorded as **unverified** rather than
  assumed, and neither is relied on above.

---

## 8. Cross-references to existing work (do not overwrite)

| Artefact | What it already provides | How this document uses it |
| --- | --- | --- |
| `data/rules/skills.json` | the **40 canonical Skills** with `stat`, `untrained` and `fielded` flags; `untrained_modifier: -1`; the field-substitution rule | the canonical side of every skill mapping in §3 |
| `docs/design/RPG_CONVERSION_REFERENCE.md` | EP2→NoöPunk and CWN→NoöPunk STAT correspondence, skill references, conversion procedure | the starting point for the Simulationist and Gamist columns; **consume, do not rewrite** |
| `docs/design/ISSUE_200_CROSS_SYSTEM_CONVERSION.md` | the five-family conversion lab and its three dimensions | the conversion algorithm §2 builds on |
| `docs/design/ISSUE_200_KERNEL_PROTOTYPE.md` | three attribute+skill kernels with measured probabilities, the ladder, opposed checks, modifier stacking, lethality | §6 starts from these rather than restarting |
| `docs/sources/GAME_SYSTEM_RIGHTS.md` + `data/sources/game_system_rights.json` | the dated, guarded provenance ledger | the authoritative rights record; §7 above is the summary, that ledger is the source |
| Issues **#217–#232** | the domain work packages (core rules, chargen, physical, social, cybernetic, psychic, astral, cross-domain, UNSA, beings, equipment, narrative, GM toolkit, CC release, consolidation) | the chapters the comparison must ultimately feed; **#217 is now downstream of a superseded centre** |

### 8.1 Conflicts found (recorded, not resolved)

- **#217's resolution semantics were designed against the superseded Fudge/Fate ladder.** The
  untrained −1 rule matches canon (`skills.json` `untrained_modifier: -1`), but the ladder and the
  partial-success policy are premises from #200's old centre. Flagged for audit; **not deleted**.
- **#200's direction record and the kernel prototype** both name Fudge/Psi-Punk as the centre.
  #255 supersedes that for future comparison decisions; the documents stay as history.
- **The rights ledger already records** the EP/Transhumanity's Fate NC boundary and The Veil's
  per-portion carve-out. §7 agrees with it; no ledger edit is proposed here.

---

## Roadmap for the remaining sections

Committed in small reviewable increments, per the issue's collaboration requirements:

- [x] **§1** goals, triangle, trade-offs, scope boundaries — *this increment*
- [x] **§7** source and rights matrix — *this increment*
- [x] **§8** cross-references and conflicts — *this increment*
- [ ] **§2** side-by-side conversion tables: six Attributes and the **full 40-skill list** against
      each of the four families, labelled *direct correspondence / conceptual analogy /
      unsupported*, marking **no counterpart** where none exists
- [ ] **§3** the same tables with lossiness and edition-dependence spelled out
- [ ] **§4** domain comparisons — PSI, Combat, Social, Faction, Cyberspace/hacking, investigation,
      cybernetics/transhumanism, advancement, GM procedure — by complexity, agency, genre fit, risk
- [ ] **§5** PSI as four distinct design concepts: EP/SWN discrete abilities, Fate Stunt/Aspect,
      PbtA Move (a Move has triggers, choices and consequences, and is *not* merely a power)
- [ ] **§6** at least two alternative Fate-first numeric kernels with probability analysis, target
      recalibration, stacking/balance and a worked comparable UNSA case
