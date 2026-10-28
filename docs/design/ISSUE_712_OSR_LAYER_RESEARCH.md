# OSR base plus investigative and narrativist layers: research (#712)

**Design only. Nothing here is implemented, and no rule in this document is approved.**

The question: keep CWN/SWN as the OSR mechanical base, and take carefully bounded layers from
GUMSHOE, PbtA, Fate, The Veil and a Call/Trail-style noetic exposure.

---

## 1. One system, one problem

The failure mode in hybrid designs is choosing a layer because it is admired rather than
because it solves a specific problem. This table binds each import to exactly one.

| problem | system | what is borrowed | what is refused |
|---|---|---|---|
| A missed clue stops the session | **GUMSHOE** | core clue; competence = competence | its investigative pool as a second currency (D46) |
| Ordinary action has no texture between success and failure | **PbtA** | clocks; fronts; *optionally* a partial-success band | moves-as-catalogue; changing the 2d6 kernel |
| A character's beliefs should cost something | **Fate** | aspects and compels | the 4dF kernel (D45) |
| Emotion and identity are the subject, not the dressing | **The Veil** | emotional states as mechanical pressure on choices | its dice engine and its CC BY-SA text |
| Exposure to the unthinkable should leave a mark | **CoC/Trail** | *the idea* of a stability track | a second harm economy (D46) — imported as **conditions** instead (#698) |
| Everything ordinary: combat, gear, hacking, missions | **CWN** | the whole engine | — |
| Psionics | **SWN** | discipline/effort shape | SWN text (licence unestablished) |

**The through-line:** CWN owns *what happens*; the layers own *what it costs to know*, and
none of them is allowed to own a die.

## 2. The attribute question, compared

### Candidate 1 — unchanged CWN (`STR DEX CON INT WIS CHA`)

- mechanical cost: **zero**
- everything in `data/rules/without_number.json`, the saves table, the Strain ceiling and all
  1,429 tests keep their present meaning
- cost: fantasy-coded vocabulary, and `WIS` doing double duty for judgement and psychic capacity

### Candidate 2 — 2 physical / 4 mental (`FIT REF INT AWA PSY SOC`)

| new | merges | cost |
|---|---|---|
| **FIT** | STR + CON | collapses *lifting* and *enduring*; the injury and Strain rules read CON directly |
| **REF** | DEX | clean |
| **INT** | INT | clean |
| **AWA** | (part of WIS) + Notice | clean, and arguably better than WIS |
| **PSY** | (part of WIS) + will | **conflates ordinary judgement with PSI capacity** — the separation #572 and D46 depend on |
| **SOC** | CHA + empathy | clean |

Verdict: **the mental-heavy shape is genuinely better for this game**, and AWA/SOC are
improvements. FIT and PSY are the two that would cost real mechanics.

### Candidate 3 — seven stats with `RES` retained (`FIT REF INT AWA PSY SOC RES`)

Keeping `RES` (resilience/endurance) while `FIT` takes strength fixes the *lifting vs enduring*
collapse and keeps the Strain ceiling readable. It does **not** fix PSY.

Cost: a seventh stat touches every derived quantity, every NPC line, and every scenario JSON.
It is the largest migration on the table.

### Candidate 4 — Physical / Social / Psychic / Cybernetic

Rejected earlier and still: **CYB as an attribute penalises unaugmented characters by
definition**, and a four-stat spread cannot distinguish perception from intellect or
empathy from influence.

## 3. Mechanical compatibility, stated as a checklist

Any candidate must satisfy all of these or it is a new game:

- [ ] 3–18 range and the `−2..+2` modifier band survive
- [ ] the three saves (`Physical STR/CON`, `Evasion DEX/INT`, `Mental WIS/CHA`) remain derivable
- [ ] HP, System Strain ceiling (`= CON`), Effort capacity and load all re-derive without new tables
- [ ] `data/rules/without_number.json` `attributes.names` and `saves.attributes` stay valid or migrate with a version
- [ ] `tests/test_scenario_data.gd`'s assertion that every scenario check names a known attribute still holds
- [ ] existing characters migrate **without numeric rescaling**

## 4. Recommendation

**Keep A; treat AWA/SOC as vocabulary, not mechanics.** The mental-heavy intuition is right,
but the two attributes that carry it (FIT, PSY) are exactly the two the injury and PSI rules
depend on. If the vocabulary grates, **B (display aliases)** gives AWA/SOC on the sheet with
zero migration — and the canonical codes stay `STR…CHA` underneath.

A 7-stat variant is the one worth revisiting **if** the game ever needs resilience to be
separable from strength for reasons other than vocabulary. Nothing yet requires it.

## 5. What this document does not do

No code, no data, no rulebook. It exists so #716 can be decided from a comparison rather than
from preference.
