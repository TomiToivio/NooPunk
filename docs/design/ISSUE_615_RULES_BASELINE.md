# Issue #615 — rules design baseline: one core, four modules, three priorities

**Status: governing design decision, recorded. It does not overwrite an approved choice by
implication — where it meets one, this document records the conflict and its resolution (§3).**

Authority order, because #615's own rule demands one: an approved author ruling beats this
document; this document beats an agent's previous recommendation; nothing beats canon.

---

## 1. The hierarchy

```
                    ONE NoöPunk core contract
        attributes · skills · checks · saves · injuries · trauma
        progression · equipment · NPCs · faction interface
                     one fiction-to-rules procedure
                              |
        ┌───────────────┬───────┴────────┬───────────────┐
   urban/network    space/NHI/PSI    noetic/inter-    crisis ruins
     cyberpunk                      dimensional        (AWN)
      (CWN)           (SWN)            (WWN)
```

**One grammar, several genre modules.** A module supplies *procedures and tools* for a kind of
place. It does not supply a second dice convention, a second skill list, or a second damage model —
that is the whole point of the architecture, and it is the thing most likely to erode.

**Mixed environments must work in one adventure.** Moving from Helsinki to an exclusion zone, an
alien outpost and a noetic realm may change *what you roll for* and *what a failure costs*. It must
not change *how you roll* or *who your character is*.

### Genre / location mapping

| Module | NoöPunk contexts | What it contributes | What it must not contribute |
| --- | --- | --- | --- |
| **CWN — primary reference** | Urban cyberpunk, UNSA fieldwork, ubiquitous hacking, BCI/cyberware, megacorps | Dangerous-action and combat adjudication, Shock/Trauma, network access procedures, equipment, mission structure | Its **2d6 check**, its attribute set, its classes and levels |
| **SWN — co-primary** | Solar-system expansion, extraterrestrial polities, NHI encounters, PSI, factions | **Effort** as a committed pool, alien-encounter framing, faction turn, colony procedures | Its psionics-through-virus ontology, its ship *settings*, its classes |
| **WWN — situational** | Law-of-One-adjacent noetic science fantasy, astral/psychic regions, anomalous entities | Exploration, weird-realm tags, **Foci** as a two-tier stunt shape, Effort analogues | Fantasy cosmology, magic-as-setting, its Latter Earth material |
| **AWN — situational** | Locally devastated or isolated regions after the NHI Crisis, infrastructure collapse | Salvage, scarcity, survival, hazard/ruin procedures, trauma | **A universal apocalypse.** Institutions persist elsewhere; the pre-Fall canon holds |

---

## 2. The design priorities, weighted by playtest

- **Gamism / OSR — backbone.** Consequential choices, visible risk, resource pressure, referee-facing
  tools, lethal but tactically meaningful conflict. Compact over complete.
- **Simulationism — selective.** Eclipse Phase's habit of taking body/mind separation, cybernetics and
  AGI/NHI/PSI implications seriously. Modelled **only where it produces a decision**; a system that
  generates realism nobody plays is cut.
- **Narrativism — selective.** Aspects, complications, clocks and fail-forward as *procedures layered
  on* the chassis (§5), never as a silent replacement for resolution.

There is deliberately **no numeric split** between the three. #615 says evaluate by playtest and
complexity budget, and that is the only honest position: any ratio would be invented.

---

## 3. Conflict-and-resolution register

This is the criterion that matters most, because #615 and the earlier decisions genuinely collide and
one of them has to give. Each row names the conflict, the evidence, and which way it resolves — and
*why*.

| # | Conflict | Evidence | Resolution |
| --- | --- | --- | --- |
| 1 | **"CWN is the primary mechanical reference"** vs **`1d10` is the core check** | CWN's core is `2d6 + attribute + skill`; NoöPunk's is `STAT + Skill + 1d10 ≥ DV` (#111, `src/rules/core.py`); #566 ruled **"Layer A only — `1d10` stays"** on 2026-10-25 | **`1d10` stands.** CWN is the reference for *procedures*, not for the die. #615's own non-regression clause ("preserve explicit NoöPunk decisions unless separately revised… do not overwrite approved choices by implication") governs. Replacing the kernel would touch **80 `1d10` sites across 41 files, the `DIFFICULTIES` ladder, and 41 test files** — that is a separate issue with the DV re-authoring costed row by row, never a side effect |
| 2 | **"CWN primary" implies classes** vs **no classes or levels** | #197 recorded Geeks/Jocks/Freaks as *slang, explicitly not classes*; #566 ruled classes **declined**, Edges **admitted** | **Declined.** Edges carry differentiation, classless, as AWN/CWN themselves do. CWN's class structure is not imported even though CWN is the primary reference — the reference is selective |
| 3 | **`CHA` in the epic's wording** vs **`SOC` in the rulebook** | `rulebook` skill table and `src/rules/core.py` use `SOC`; `CHA` appears in CWN's attribute set | **`SOC` survives.** `FIT/REF/INT/SOC/CYB/PSY` unchanged; `CHA` is CWN's name and is not adopted |
| 4 | **"3d6 check/difficulty conventions" flagged as a conflict** | `grep -E "3d6|3D6" RULEBOOK.md` → **no matches**. Legacy is `STAT + Skill + 1d10`; the crossover is `4dF` | **No 3d6 convention exists to preserve or replace.** The conflict is dissolved, not resolved: the premise was wrong. Recorded so the next reader does not re-litigate it |
| 5 | **One engine for both RPG layers** vs **two approved kernels** | Layer A `1d10` (#111); layer B Fate `4dF` (#389, six skills #482) — both approved and implemented | **Two layers, two kernels, one product line.** #566 answers this: `RULEBOOK.md` *is* the RPG; `strategy_game/RULEBOOK.md` is Layer I of the crossover, which its own opening says. "One unambiguous rulebook" is achieved by labelling at zero cost |
| 6 | **PSI as SWN psionics** vs **PSI as natural, learnable ability** | #482 records PSI as natural, not virus-derived; author ruling 2026-10-25: "PSI as in SWN rules but learnable natural human ability" | **Split cleanly: SWN's rules, NoöPunk's ontology.** Effort adopted as the committed pool; the fiction stays natural, learnable, open to anyone — not a virus, implant, or class feature |
| 7 | **CWN hacking's matrix-like access** vs **a ubiquitous network** | CWN makes reachability the gate; NoöPunk's network is ambient. `strategy_game/cyber.py` decides reachability *before* any check | **CWN supplies the resolution procedure only.** Access is not the scarce thing; visibility, timing and attribution are. Ubiquity is the default, severance the exception the crisis produces |
| 8 | **AWN assumes apocalypse** vs **pre-Fall canon** | Canon is pre-Fall, Earth intact, 20XX; the Fall has *not* happened | **AWN's procedures only, never its premise.** Salvage and scarcity model *local* devastation; the wider world keeps working. This is the single most likely place for a module import to smuggle in a setting |
| 9 | **WWN magic** vs **panpsychic ontology** | NoöPunk PSI is panpsychic/ontological (Psi = ground, Phi = IIT); WWN magic is a fantasy apparatus | **Reinterpret, never import the apparatus.** WWN supplies exploration and realm procedures; its cosmology is out of scope |
| 10 | **"NoöPunk's own system" long-term** vs **borrowed chassis now** | Stage D of this roadmap; current mechanics are adapted | **Sequence, not contradiction.** Stages A→D are explicit, versioned, and driven by playtest. Independence is **not** cosmetic renaming |

### What this register refuses to do

It does not "average" the conflicts, and it does not treat #615's newer framing as automatically
superseding older approved rulings. Where #615 and an approved ruling disagree, the ruling stands
until the author separately revises it — which is exactly what #615's non-regression clause asks for.

---

## 4. Provenance, licensing and compatibility matrix

Per subsystem, with the licence status **measured**, not assumed. The verified source of truth is
`data/sources/game_system_rights.json`, audited in `docs/licenses/ISSUE_569_CWN_SWN_LICENCE_AUDIT.md`.

| Source | Reuse status (verified) | Permitted | Not permitted | Provenance rule |
| --- | --- | --- | --- | --- |
| **CWN SRD** | `verified-public-domain` — **CC0**, checked 2026-10-10, three agreeing readings | SRD text and mechanics, commercially, verbatim | The full commercial book, its art, its protected setting and faction names | Mechanics may be adapted; **prose still gets authored fresh** |
| **WWN SRD** | `verified-public-domain` — **CC0**, checked 2026-10-25 at the SRD's own introduction | SRD text and mechanics, verbatim, commercially | The complete game book, Latter Earth, excluded material | SRD scope only. The dedication is on *the SRD*, not the book |
| **SWN** | **`blocked-unverified`** — no SWN SRD located in two passes; a free *edition* is not an SRD | **Nothing may be adapted from SWN expression** | Its text, tables, names, prose | Use SWN as a **design influence** and reimplement described mechanics independently. This is what #615's own table concludes too |
| **AWN** | **`blocked-unverified`** — no AWN SRD located, 2025 commercial release | Nothing from its expression | Its text, tables, prose | Same as SWN: influence, not source |
| **Fate Core SRD** | Public SRD, licence options stated at source | Per the chosen Fate licence and its attribution rules | Anything outside the chosen option | Layer B already implements Fate; attribution must match the option actually used |
| **Transhumanity's Fate** | **No separate SRD.** Published game is **CC BY-NC-SA** | Non-commercial adaptation under share-alike | Commercial reuse without resolving compatibility | NC/SA-derived text must stay out of a commercially licensed standalone core. `docs/ATTRIBUTION_POLICY.md` governs |
| **Eclipse Phase (EP2)** | Generally **BY-NC-SA 4.0**; **no standalone SRD asserted** | Non-commercial, share-alike, notices kept | Commercial reuse; implied endorsement | Concepts and design habits only; original expression |
| **Apocalypse World** | **No authoritative standalone English SRD identified** | Inspiration from published design writing | Its book's text | PbtA *approach* (moves, fronts, fail-forward), never its prose |
| **The Veil** | **No verified SRD identified** | Inspiration only | Copying its text or playbooks | Same rule |

**The implementation rule, stated once:** use the freely reusable *specific SRD* where verified
(CWN, WWN); use everything else as **inspiration, adapting unprotected ideas with original
expression**. Log provenance per subsystem. Keep NC/SA-derived text out of any commercially licensed
standalone core until compatibility is resolved. **Credit is not a licence**, and no single licence
covers the whole source family.

---

## 5. Narrative and simulation layers — optional, triggered, costed

Both are **add-ons over the chassis**, never a second resolution system.

| Layer | Trigger | Cost | What it cannot do |
| --- | --- | --- | --- |
| **Aspect / tag** (Fate-derived) | A stated fictional fact would plainly make a check easier or harder | One invocation per aspect per scene; the aspect must already be true in the fiction | Cannot replace a check; cannot grant an outcome |
| **Complication** (PbtA-derived) | A tie, or a failure the table would rather escalate than stop | The player accepts a complication instead of losing the scene | Cannot erase consequence — it converts it |
| **Clock / front** | A threat is being tracked across scenes | Segments fill from failures and hard moves; a full clock fires | Cannot fire without a filled segment |
| **Fail-forward** | A failed check where stopping play is worse than advancing it | Success at a cost, chosen by the referee from the scene's own stakes | Cannot apply to lethal resolution (Shock/Trauma) |

**Required core vs optional modules must stay distinguishable.** A table running "core only" must be
able to play a full session without ever invoking §5. That is the test of whether these are layered
or merely absent.

---

## 6. Mixed-genre play example — one sheet, one grammar

The worked example lives as an executable regression test, not as prose, so it cannot quietly stop
being true: **`tests/test_issue615_mixed_genre_grammar.py`**.

One character, one `stats` dict, one skill rating, one kernel (`core.resolve_check`), four
environments:

| Environment | Module | The same grammar asks… | Failure means |
| --- | --- | --- | --- |
| Helsinki, acceleration era | urban/network (CWN) | can I get in without being attributed? | exposure, not damage |
| Orbital outpost | space/NHI (SWN) | can I hold the Effort for this? | capacity locked, not lost HP |
| Noetic realm | interdimensional (WWN) | can I read the place? | the realm answers anyway |
| Exclusion zone | crisis ruins (AWN) | can I salvage this before it fails? | scarcity, not death |

The test asserts that **the same `stats`, the same skill and the same kernel** produce a resolution
in all four, and that environment changes only the *DV, the stat bound and the consequence* — never
the arithmetic. If a future change makes an environment need its own die, that test fails.

---

## 7. Credits, notices and disclaimer

The repository already carries an attribution section in `README.md` and a policy in
`docs/ATTRIBUTION_POLICY.md` (issue #447). **This section does not duplicate them; it records the
wording #615 proposes and the vets it needs.**

Proposed, and **acceptable with the caveats below**: an accurate source-and-inspiration statement
naming the *Without Number* family (Kevin Crawford / Sine Nomine) as the primary mechanical
reference, WWN/AWN as situational, and Eclipse Phase, Transhumanity's Fate, Fate Core, Apocalypse
World and The Veil as additional design influences, with an explicit non-affiliation and
non-endorsement sentence.

**Vets required before it ships as final wording:**

1. **It must not imply one licence covers the family.** CWN and WWN SRDs are CC0; SWN and AWN are
   `blocked-unverified`. The statement must say *reference*, not *source of reused text*.
2. **"Primarily based on/adapted from the Without Number family"** is stronger than what the
   licensing supports for SWN and AWN. Preferred phrasing: *"mechanics adapted from the Cities
   Without Number SRD and the Worlds Without Number SRD, with the wider Without Number family as a
   design reference."*
3. **Eclipse Phase / Transhumanity's Fate are BY-NC-SA**, so a credit line is not a licence and the
   commercial path (`docs/ATTRIBUTION_POLICY.md`) governs.
4. Trademark and title references stay **factual and comparative** — no logos, no implied
   compatibility statements.

**What shipped, and what did not.** The credits block is now in `README.md`, but written with the
corrected phrasing above rather than #615's stronger "primarily based on/adapted from the Without
Number family": it names the CWN and WWN SRDs as adapted sources, SWN and AWN as design references
only, and states the non-affiliation sentence. The stronger phrasing was **not** used, because it
would claim more than the licensing supports for two of the four books.

Final wording still awaits the author, together with **D10** (NoöPunk's own licence pair). An agent
may state facts about licences; it may not choose one.

---

## 8. Roadmap — versioned, playtest-driven

| Stage | Deliverable | Exit criterion | Version |
| --- | --- | --- | --- |
| **A. Transparent adaptation** | This document plus the KEEP/MODIFY/REPLACE/OMIT/DEFER matrix in `ISSUE_564_CWN_SWN_CHASSIS_MATRIX.md` and `ISSUE_572_NOOPUNK_EXTENSIONS.md` | Every subsystem has a verdict and a named source inspiration | `0.x` |
| **B. Consolidated hybrid** | Unified sheet, action economy, stress/trauma, faction interface, NHI/PSI/BCI, cross-genre rules, quickstart, playable scenarios | One sheet plays all four environments (§6) | `0.y` |
| **C. Playtest and measure** | Sessions across cyberpunk, NHI/space, noetic, crisis-zone and **mixed** genres | Lethality, speed, decision depth, GM workload, narrative agency, complexity, coherence are *measured and recorded* | `0.z` |
| **D. Independent NoöPunk rules** | Borrowed procedures replaced or substantially reinterpreted, with migrations | Independence is **authored**, not renamed; every replacement has a migration note | `1.0` |

**Rules of the roadmap:** version the rules; ship migration notes with each break; keep compatibility
aids as long as they earn their place; and **do not equate independence with cosmetic renaming** —
renaming a borrowed procedure is the failure mode #615 explicitly forbids.

---

## 9. What this document does not do

- It does not change a mechanic. No die, no number, no class, no threshold.
- It does not overwrite #566's rulings; it records where #615 meets them and which one gives (§3).
- It does not assert a licence for SWN or AWN, and it does not treat credit as permission.
- It does not approve the credit wording — that is the author's, and §7 lists the vets.
- It does not claim Stage B–D are done. Stages are a plan, not a status.
