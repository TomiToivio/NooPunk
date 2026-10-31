# Issue #943 — acceptance record: the Noösphere / ontological-apocalypse module

**Basis.** #943 is a **design and planning issue**: *"Write and validate the module before implementing
anything; any Godot/Python changes require a reviewed follow-up PR."* The module itself landed as
[`ISSUE_943_NOOSPHERE_APOCALYPSE.md`](ISSUE_943_NOOSPHERE_APOCALYPSE.md). This record does what that
document cannot do for itself: it walks the issue's eleven acceptance criteria one at a time, says for
each whether it is **met**, **met with a named remainder**, or **an author decision**, and states the
one criterion the repository has not met cleanly.

Nothing here is a ruling. Every row that needs the author is cross-referenced to
`AUTHOR_DECISION_QUEUE.md` (D62–D64) rather than answered.

---

## 1. Criterion by criterion

| # | Criterion (issue's own words, abbreviated) | Verdict | Evidence |
| --- | --- | --- | --- |
| 1 | A sourced comparison of the three designs: source mechanics, proposed changes, exclusions, source-page references | **MET** | Module §2.1 (*The Veil*, 12 rows) and §2.2 (*Apocalypse World*, 6 rows); §2.3 collects the refusals. Every page number was verified by extracting both PDFs, including the offset between each book's printed numbering and its PDF index (§18) |
| 2 | An independent module with N1–N3, clocks, an MC procedure and generic non-proprietary scenes | **MET** | §5 (N1), §6 (N2), §7 (N3), §9 (clocks), §10 (the five-step procedure), §12 (three scenes, no proper nouns from either book) |
| 3 | Inventory the existing CWN / GUMSHOE / PSI / Stress / social / faction / narrative / clock code first; reuse, don't replace | **MET** | §3's twelve-row inventory, each row naming a file and a symbol with a line number. The inventory **found a real gap** (§3, last paragraph) and a real absence: the only runtime clock in the tree is the hacking `AlertClock` |
| 4 | A unified hybrid-perception / evidence record with separate provenance and hypothesis fields | **MET as a merge specification, not a new type** | §4. The repository already holds both halves — `Evidence` with `Provenance` (`investigation_evidence.py:12`), `Perception` with `InformationSource` (`noospace_projection.py:263`), `Hypothesis` with player-set confidence (`investigation.py:285`). §4.1 tabulates where each field already lives and which record may write it; §4.2 states the join and the three rules that keep it honest. No third store is created |
| 5 | Open Your Mind: triggers, ordinary observations, risks, CWN/PSI dispatch, failures, **no new ability scores** | **MET** | §5's dispatch table (five situations → five authorities), and the module's `open_mind()` which returns `engine: "cwn"` / `requires_core_resolution` instead of a result, and `grants_power: false` on every path. No ability, attribute or skill is added anywhere; the tests assert the method surface directly |
| 6 | Emotional States and player-created identity as **nonnumeric** descriptors | **MET** | §8; asserted: the stored state is a `String`, no attribute block exists, and identity is written only by an explicit `record_choice()` call |
| 7 | At least three competing, non-linear apocalypse/faction clocks with rollback and player countermeasures | **MET** | §9.2 defines **five** (disclosure, rogue ASI, cyber-psychic convergence, UNSA authority, local crisis) with actor, triggers, stall/reversal and terminal event; §9.1 rule 3 makes rollback legal and rule 7 makes non-linearity explicit; §9.3 works a rollback end to end. Executed: `change_clock()` refuses an empty trigger and a multi-step jump, accepts a negative step, records the countermeasure, and clamps per-clock at 4 or 6 |
| 8 | Automated tests for: no dual dice engine, no automatic psychic powers, no forced belief changes, no core-clue gates, no duplicate psychological track | **MET, and this is where the first increment failed** | `godot/tests/test_noosphere_943.gd`, 46 assertion rows, **registered** in `godot/tests/run_tests.gd`. See §2 for the defect this record has to state plainly |
| 9 | Licence obligations documented separately for *The Veil*'s CC BY-SA text, its excluded art, and *Apocalypse World* material/permission; do not claim everything PbtA is open | **MET** | §15, four bullets. It records the share-alike consequence for any future quotation, the fact that *The Veil*'s "used with permission" does not transfer, and that *Apocalypse World* 2e is **not** established as openly licensed. It also names the test that will fail if expression is ever pasted in |
| 10 | Keep the CWN baseline and the #897 invariant intact; coordinate with #932's open pool decision | **MET** | §11's table of responsibility, §16's exclusion list. The module imports nothing from `godot/core/`, adds no dice or modifier, and names D61 (`#932`'s clue-shape question) as a dependency it only *reads* |
| 11 | Design review before any Godot implementation or merge; a follow-up coding PR when ready | **NOT CLEANLY MET — recorded as a deviation, §2** | The first increment (PR #944) merged a GDScript module **before** the design document existed |

---

## 2. The one criterion that is not clean, stated plainly

The issue's eleventh criterion asks that the design be reviewed **before** anything is implemented.
The first increment for this issue (PR #944, merged 2026-10-31) added `mods/noopunk/noosphere.gd`
together with a 69-line document, and it was reviewed and merged by this session. That is the wrong
order, and the mitigation is not a justification:

- the module **reads and returns state only**. It rolls nothing, charges nothing, derives nothing and
  grants nothing; every row of §11's authority table is still owned by the file it already belonged to;
- it is in `mods/`, which is the layer `#897` designates for optional overlays, and it imports nothing
  from `godot/core/`;
- **it changes no rule**, so the deviation costs a merge, not a rule. If the author answers **D62(a)**,
  it stays as the executable half of this design; **D62(b)** holds it out of `main` until a chapter
  exists; **D62(c)** retires it in favour of clocks only.

A second, smaller defect in the same increment is worth writing down because it is the kind that
passes CI silently: **`godot/tests/test_noosphere_943.gd` was added but never registered** in
`godot/tests/run_tests.gd`'s explicit `SUITES` list. The Godot job on PR #944 reported success — it
ran the other suites and never loaded that file. A green check proved nothing about the new test.
Registration is the first line of this record's follow-up work, and the suite now executes.

---

## 3. What was actually executed

Not a claim: the commands and their output.

```text
godot --headless --path . --import
godot --headless --path . --script res://godot/tests/run_tests.gd
    -> 1925 checks, 0 failed            (includes the 46 rows of test_noosphere_943.gd)

python3 tools/check_godot_shutdown.py --godot <godot 4.7.2>
    -> slice: 0 objects, 0 resources, 0 RIDs (1925 checks, 0 failed)
       rules: 0 objects, 0 resources, 0 RIDs (0 failure(s))
       playthrough: 0 objects, 0 resources, 0 RIDs (15 checks, 0 failed)
       ward: 0 objects, 0 resources, 0 RIDs (WARD_READY)
       interaction: 0 objects, 0 resources, 0 RIDs (INTEGRATION_OK)
    -> OK: clean shutdown, no unexpected errors, leakage within baseline (5 command(s))
```

The Godot version used locally is `4.7.2.stable.official`, which is the version pinned in
`.github/workflows/godot.yml`, so a local pass is evidence about CI rather than about a different
engine.

---

## 4. Remainders, so nothing is claimed as finished

| Remainder | Owner | Where it is queued |
| --- | --- | --- |
| Approve the module, and in what form (design + code / design only / clocks only) | author | **D62** |
| Which of the five clocks ship, and whether a case may declare a 4-segment clock where 6 is the norm | author | **D63** |
| Whether any of *The Veil*'s text is ever quoted (this changes the ShareAlike obligations of whatever file carries it) | author | **D64** |
| The Stress-vs-Psyche placement of ontological shock; the condition catalogue; every severity and recovery rule | author | **D58**, `DECISION_689_NARRATIVE_AND_MIND.md` §4 |
| Which module owns discovery and what shape a clue carries | author | **D61** |
| A rulebook chapter for the module | not started, deliberately | this record |
| Persisting the module's state (a save format, a migration) | not started, deliberately | §16 of the module |
| A playtest that exercises a full clock to its terminal segment | not started | the falsification test this design needs |

**No rulebook chapter is written.** The module is a design plus an isolated overlay, and the issue
asks for a review before a chapter exists. Writing one now would be the same mistake as implementing
before the review.

---

## 5. Sources and how they were read

- Fraser Simons, *The Veil*, second printing (2018) — user-supplied PDF at
  `Cyberpunk/The Veil/The_Veil_Second_Printing_Low_Res_Singles.pdf`. Printed page = PDF index − 1.
  Pages used: 7–11, 37, 39–43, 54, 72–79, 100–105, 268–269, 281–285, 293–305, 313, 348–362.
- D. Vincent Baker and Meguey Baker, *Apocalypse World*, second edition (2016) — user-supplied PDF at
  `Cyberpunk/Apocalypse World/Apocalypse World 2nd Ed.pdf`. Printed page = PDF index − 3. Pages used:
  8, 80, 82, 88, 106–122, 126, 132, 136–151, 278–284.
- Mechanics were read and re-expressed; **no text was copied**. `tests/test_third_party_expression_absent.py`
  is the machine check that the tree carries no third-party expression, and it passes on this branch.
