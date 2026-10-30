# NoöPunk RPG chassis inventory (#564, step 1)

> **Superseded as current state, 2026-10-30:** this inventory describes the two-kernel world
> (1d10 legacy / 4dF crossover) that the 2026-10-26 [Without Number baseline](../rulebook/WITHOUT_NUMBER_BASELINE.md)
> replaced for the tabletop. It remains a correct historical inventory of the code as it was.
> Current dispositions: [`ISSUE_747_WN_RESKIN_MATRIX.md`](design/ISSUE_747_WN_RESKIN_MATRIX.md).

**Status: inventory only. Nothing in this document approves, changes or retires a rule.**
It records what exists, what each part claims to be, and where #564's own premise disagrees
with the code. Every "needs a decision" row is the author's, not this document's.

Parent epic: [#564](https://github.com/TomiToivio/NooPunk/issues/564). Prior decisions:
[#19](https://github.com/TomiToivio/NooPunk/issues/19) (CWN SRD as a starting chassis),
[#22](https://github.com/TomiToivio/NooPunk/issues/22) (CWN skill conversion), #111
(independent kernel), [#389](https://github.com/TomiToivio/NooPunk/issues/389) and
[#482](https://github.com/TomiToivio/NooPunk/issues/482) (Fate baseline for the crossover).

---

## 1. There are three mechanical chassis in this repository, not one

NoöPunk is not a single rules system with legacy leftovers. It contains **three separate
mechanical layers**, each with its own dice, its own vocabulary, and its own approval status.
Any unification plan has to say which of them it is unifying.

| | Layer | Entry points | Resolution | Rating model | Approval status |
|---|---|---|---|---|---|
| **A** | Legacy NoöPunk RPG (tabletop) | `RULEBOOK.md`, `rulebook/`, `src/rules/`, `src/interaction/` | **`STAT + Skill + 1d10 ≥ DV`** | six STATs **FIT / REF / INT / SOC / CYB / PSY**; skill levels 0–4 (#22 scale) | Independent system since **#111**. Canonical for the legacy game. Not imported into the crossover. |
| **B** | Crossover Layer I (faction leader, narrative RPG) | `strategy_game/rpg/` (`fate.py`, `skills.py`), `strategy_game/casework/` | **4dF + skill** against the Fate ladder | six individual **skills** COG / INT / REF / SAV / SOM / WIL, Fate-rated | **Approved** by **#389** and **#482**; implemented in `strategy_game/RULEBOOK.md` §2–§8 |
| **C** | Tactical / board layer | `strategy_game/tabletop/` (`dice.py`, `board.py`, `cards.py`, `decks.py`, `tarot.py`) | generic dice-pool parser (`d6`, `2d6`, `3d8+1`, `1d20-2`) + cards | tokens, cards, decks — no character rating | Separate module for the strategy board. **Not** the RPG. |

Evidence, so a later reader can re-verify rather than trust this table:

```
src/rules/core.py:5        STAT + Skill + 1d10 >= Difficulty Value
src/rules/core.py:8        six universal base STATs — FIT / REF / INT / SOC / CYB / PSY
strategy_game/rpg/fate.py:203   def skill_check(...)          # 4dF
strategy_game/rpg/skills.py:96  INDIVIDUAL_SKILLS = (COG, INT, REF, SAV, SOM, WIL)
strategy_game/tabletop/dice.py:94  parse_notation("2d6")      # generic pool, layer C
strategy_game/casework/session.py:1276  skill_check(...)      # goes to layer B, not A
```

Test surface: `tests/` 33 modules (layer A and repo-wide guards), `strategy_game/tests/`
74 modules (layer B/C), `strategy_game/rpg/` 16 modules.

## 2. What #19 and #22 already decided, and one dangling reference

- **#19** adopted the CWN **SRD** as an open starting chassis and established the
  KEEP / MODIFY / REPLACE / OMIT / DEFER process, subsystem by subsystem. It explicitly
  rejected "straight CWN clone".
- **#22** converted the skill system: level 0–4, unskilled is *not* a numbered level, an
  unskilled attempt is either −1 or blocked where training is required. It states that it
  supersedes the old four-step +1/+2/+3 model, and that it does **not** license redesigning
  adjacent systems (chargen, advancement, combat, hacking, Focus).
- **`docs/CWN_CHASSIS.md` does not exist.** #22 names it as the home of the chassis policy
  ("the next subsystem review under the CWN chassis policy in `docs/CWN_CHASSIS.md`"). The
  file is absent from the tree. The policy lives in the issue bodies instead, which is why
  the decision record currently cannot be read from the repository.

## 3. Where #564's premise disagrees with the repository

The epic instructs: *"Where a newer explicit design decision conflicts with this issue,
follow the newer decision and document the difference."* These are those differences.

### 3.1 There is no 3d6 core-check model

#564 says the author's choice is *"the present 3d6 core-check/difficulty model"*. No 3d6
check exists in the tree:

- Layer A resolves on **1d10** (`src/rules/core.py`), the kernel installed by #111.
- Layer B resolves on **4dF** (`strategy_game/rpg/fate.py`).
- The only 3d6 in the system is a **3d6 attribute-generation helper**, retained in
  `src/rules/_retired.py` because attribute generation is still an open design area
  (AGENTS.md §4). It does not resolve checks.

So a conversion that "keeps the 3d6 core check" has nothing to keep, and a conversion that
"replaces 3d6 with CWN's 2d6" would in fact replace **1d10** (layer A) or **4dF** (layer B).

### 3.2 The attribute list is SOC, not CHA

#564 lists `FIT/REF/INT/CHA/CYB/PSY`. The legacy STAT block is
**`FIT / REF / INT / SOC / CYB / PSY`** (`src/rules/core.py:8`). This is not cosmetic: `SOC`
is a social-science construct in a game whose stated purpose is discourse analysis, and
renaming it to the generic RPG `CHA` would be a design change, not a spelling fix.

Separately, layer B does not use STATs at all — it rates six **skills** (COG/INT/REF/SAV/
SOM/WIL), and `rpg/skills.py` records that COG-versus-INT is a design decision, not a
renaming. Layers A and B therefore do not share a rating vocabulary even where the letters
coincide.

### 3.3 The Fate baseline is approved, so CWN is a revision

#564's framing treats the current RPG as an accumulation of unratified experiments. For
layer B that is not the case: **#389** approved the Fate Core foundation and **#482**
approved its skill layers, both recorded as approved in `strategy_game/RULEBOOK.md`. Moving
layer B to a CWN/SWN chassis would **revise an approved decision**, which is a different
proposal from tidying an unapproved one, and needs to be written as such.

## 4. Canonical / legacy / unapproved, as the tree stands

| Component | Classification |
|---|---|
| `src/rules/core.py` (1d10 kernel) | **Canonical** for layer A, since #111 |
| `rulebook/`, `RULEBOOK.md` | **Canonical** layer A reference; must not be rewritten while #564 is open |
| `strategy_game/rpg/fate.py`, `skills.py` | **Canonical** for layer B, approved #389/#482 |
| `strategy_game/tabletop/` | **Supported** module; layer C, unrelated to either RPG |
| `src/rules/_retired.py` | **Explicit legacy boundary.** Compatibility aliases + the 3d6 *generation* helper. "Do not extend this module." |
| `src/rules/aspects_prototype.py`, `kernel_prototype.py`, `issue200_*` | **Prototypes / labs.** Design records, not runtime |
| `src/rules/issue217_resolution.py` | Prototype for the #217 resolution question |
| `archive/`, `legacy/` | Historical records; never canonical |
| `COMPARISON.md` | **Generated, explicitly non-canonical** (#255) |

## 5. What can be done without a new ruling, and what cannot

**Can proceed now** (documentation and measurement only, no rule change):

1. The subsystem-by-subsystem **CWN/SWN → NoöPunk mapping matrix**, in the #19
   KEEP/MODIFY/REPLACE/OMIT/DEFER form, with rationale and authoritative reference per row.
2. **Licensing and attribution audit** of what the CWN/SWN SRDs permit, and a check that no
   protected setting or full-book prose has entered the repo.
3. A **deterministic seeded playthrough harness** per active scenario, which is useful
   whichever chassis wins and is required by the epic's acceptance criteria regardless.
4. Restoring the **missing chassis policy document** (`docs/CWN_CHASSIS.md`) by
   transcribing the decisions that currently live only in #19/#22 bodies.

**Cannot proceed without the author** (each changes an approved or author-set decision):

1. **Which layer #564 governs.** Layer A (1d10, legacy), layer B (4dF, approved crossover),
   or both. The epic's "one unambiguous current rulebook" acceptance criterion implies both;
   #389/#482 approved layer B as Fate. This is the single blocking question.
2. **The core-check die** for whichever layer is converted: keep 1d10 / keep 4dF / adopt
   CWN 2d6. #564 forbids silently adopting 2d6, and there is no 3d6 to preserve.
3. **SOC vs CHA**, and whether layer B adopts layer A's STATs or keeps skill-only ratings.
4. **Classes and levels**: stock CWN/SWN introduces them; #564 forbids introducing them
   silently. Whether any are admitted is a design ruling.

## 6. Recommended decomposition

The epic asks for linked implementation issues by subsystem rather than one rewrite. See the
issues linked from #564; they are ordered so that nothing that changes a rule starts before
the layer question above is answered.
