# #712 — OSR base plus investigative/narrativist layers, and the attribute question

**Status:** research and design comparison only. No code, sheet, canon or test changes. No decision is
made here; the decision is #716.

Authoritative baseline first: `rulebook/WITHOUT_NUMBER_BASELINE.md` (26 October 2026) — CWN is the
default character and adventuring engine, the WN family governs its specialties, attributes are
STR/DEX/CON/INT/WIS/CHA on 3–18, and "Physical, Social, Psychic and Cybernetic describe the setting; they
do not supply extra character attributes". `data/rules/without_number.json` is the machine-readable
contract: `attributes.names`, `saves.attributes`, `modifier_upper_bounds`, `check` (2d6 vs 6–14).

---

## 1. What each layer is asked to solve, and what it may not do

| source | the one problem it solves | what it may not do | licence |
|---|---|---|---|
| **CWN/WWN** | ordinary cyberpunk play: skills, combat, gear, cyberware, hacking, missions | — | **CC0**, verified |
| **GUMSHOE** | a competent investigator never fails to *find* the clue | may not decide what the clue *means*; may not add a resolution die | **CC BY 3.0**, verified (attribution sentence, no logo, no other Pelgrane marks) |
| **PbtA** | mixed success, escalation, clocks, fronts | may not replace the 2d6 CWN check with moves; may not author facts | **no CC grant** — ideas only |
| **Fate** | aspects, compels, cost-bearing motivation | may not alter world state, grant clues, or stack bonuses | **CC BY 3.0**, verified |
| **The Veil** | emotion/belief as play material, virtual consciousness | may not be adapted if NoöPunk ever goes NC | **CC BY-SA 3.0** — forces ShareAlike |
| **CoC/Trail** | dread and noetic exposure as a track | may not become a second harm economy beside Strain/HP | **proprietary** (CoC) / Pelgrane marks not granted (Trail) — ideas only |
| **SWN** | psionics: disciplines, Effort, techniques | may not be quoted as text until its SRD licence is read | **not established** — principles only |
| **AWN** | scarcity, hazards, aftermath | optional, never compulsory bookkeeping | **not established** — principles only |
| **Eclipse Phase** | forks, resleeving, synthetic minds, ontological shock | may not supply text or tables to a commercially reusable release | **CC BY-NC-SA 4.0** |
| **Disco Elysium / Citizen Sleeper** | inner voices, motives as mechanics | inspiration only; no mechanical import | **proprietary** |

The line that keeps the stack coherent: **CWN decides what is true and what it costs; the others decide
what it feels like and what it is worth.**

## 2. Reliable clue vs uncertain interpretation

Already implemented and unchanged by this issue: `src/rules/investigation.py` grants the fact and leaves
interpretation to the table; `src/rules/anomaly_gate.py` requires the discriminating test before a case may
conclude as anomalous, records **inconclusive** as a real result, and allows a **provisional referral**
without proving an ontology. Consequence for this issue: no new layer may add a second "insight" track
that decides truth, because the gate is already the mechanism that keeps uncertainty honest.

## 3. Attribute models

### A — keep CWN's six (current baseline)

STR, DEX, CON, INT, WIS, CHA; 3–18; modifiers −2/−1/0/+1/+2.

- **Mechanics:** zero change. `saves.attributes` already maps Physical(STR,CON), Evasion(DEX,INT),
  Mental(WIS,CHA), Luck(none).
- **Weakness:** WIS carries both *perception* and *judgement*; CHA carries both *empathy* and *command*.
  A near-future investigation game leans on those two distinctions more than a fantasy game does.
- **Cost of keeping it:** none; the mismatch is a vocabulary annoyance, not a mechanical fault.

### B — six aliases, canonical codes unchanged

Body Power / Coordination / Resilience / Reason / Awareness / Presence, with `STR…CHA` retained in data.

- **Mechanics:** zero. Saves, derived scores, NPC lines and saves all keep working.
- **Weakness:** printed sheets say "Awareness" where the SRD says "Wisdom", so every source-book lookup
  needs a translation step unless both are printed.
- **Cost:** a labelling pass, and the risk of a half-renamed tree (the real danger, not the rename).

### C — the legacy set (FIT/REF/INT/SOC/PSY/CYB)

- **FIT** merges STR+CON: melee power and carrying capacity collapse into HP and System Strain capacity.
- **SOC** merges CHA with part of WIS; **CYB** has no CWN axis at all and would penalise unaugmented
  characters by definition (cyberware is *equipment* under the baseline; System Strain already prices it).
- **PSY** risks conflating ordinary judgement with trained PSI, which the baseline keeps separate.
- **Cost:** saves, HP, Effort, load, combat, skills, advancement, NPCs, gear, every `data/rules/*.json`
  contract, `tests/test_scenario_data.gd`, and a migration story for every existing character.

### D — "2 physical / 4 mental" (the model #712 asks to compare)

FIT (STR+CON), REF (DEX), INT, AWA (perception/intuition), PSY (will/integration), SOC (empathy/influence).

- **What it fixes:** it separates perception from will, which is the genuine gap in A.
- **What it costs:** FIT re-merges STR+CON (the C case problem), and four of six stats are mental — so a
  party optimises into investigators who cannot run, climb, or take a hit, which the Lakkahaltia case
  needs them to do.
- **Save mapping:** Physical(FIT), Evasion(REF,INT), Mental(PSY,SOC) — plausible, but it silently moves
  WIS's judgement into PSY while AWA takes perception, which changes what a mental save *means*.

### E — seven stats, 3 physical / 4 mental

FIT, REF, RES (endurance), INT, AWA, PSY, SOC.

- **What it fixes:** splits STR and CON again, so the D case's main defect disappears.
- **What it costs:** a seventh attribute changes the point-buy budget, the modifier spread and every
  generated NPC; and it still needs a ruling on whether PSY is ordinary will (yes) or latent PSI (no —
  PSI is a trained capability with Effort, per the `swn_psychic` package).

## 4. Worked checks

**Forensics (INT):** A and B roll `2d6 + INT mod + Know rank` against 8/10/12/14 — unchanged in every
model that keeps INT. D/E would also allow AWA to substitute for *noticing* what to sample, which is a new
rule, not a rename.

**Mental save:** A rolls `16 − level − best of (WIS, CHA)`. Under D it becomes "best of PSY, SOC" — same
arithmetic, different fiction: a character with high WIS but low CHA now saves differently, which is a real
behaviour change disguised as a label.

**An AI or non-embodied entity:** A gives it INT/WIS/CHA and no physical scores (as `without_number.json`
already does for case NPCs). D's four-mental model is attractive here, but it does not need new stats — it
needs the existing sheet to permit absent physical scores, which it already does.

**A cybered street samurai:** under A, cyberware is gear plus Strain. Under C, CYB would double-count the
same thing the Strain system already prices.

## 5. Balance risks, ranked

1. **Mental-stat inflation (D/E).** Four mental attributes invite a party of invalids; the case as written
   requires entry, pursuit and physical risk.
2. **PSY conflation.** Any model with PSY invites "roll PSY to sense the anomaly", which would break the
   anomaly gate and the rule that PSI is trained, not ambient.
3. **Dump-stat drift.** A merged FIT makes STR/CON a single obvious dump stat for investigators.
4. **Half-migration.** The largest practical risk in all three: labels changed in prose but not in
   `without_number.json`, so the sheet and the rules disagree.

## 6. Recommendation

**Keep A. If the vocabulary genuinely obstructs play, do B, and only after a session shows it.** D and E
are coherent *other games*; they are not renames, and they should be argued as redesigns with their own
migration plan if anyone wants them. No model should be adopted on the strength of this document alone —
that is #716's decision and #717's evidence.

## 7. Candidate implementation tasks (not started)

- If B: a presentation-layer label map plus a lint that every code in `data/rules/*.json` exists in the
  map; no numeric change.
- If D/E: a design issue of its own covering save pairings, point buy, NPC generation and the legacy
  character rebuild rule.
- Either way: a check that the *sheet* and `without_number.json` cannot disagree — the half-rename guard.

## 8. Licensing feasibility

Adaptation is permitted for CWN/WWN (CC0), GUMSHOE and Fate (BY 3.0, with attribution; GUMSHOE's sentence
must sit with the copyright notice). PbtA titles are ideas-only. The Veil (BY-SA) forecloses NC; Eclipse
Phase (NC) forecloses mixing with BY-SA. Therefore: **any layer borrowed as text constrains the final
licence, and the layers borrowed as ideas do not.** That is the only licensing claim this issue needs.
