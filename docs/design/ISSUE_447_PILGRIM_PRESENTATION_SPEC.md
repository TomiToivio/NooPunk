# Tommy Pilgrim presentation layer — art-direction and narrative-framing specification (issue #447)

**Status: SPECIFICATION, PROPOSAL. Presentation only.** This document defines how NoöPunk is *presented* as a 1974-origin work. It defines **no** rule, mechanic, statistic, scenario fact, chronology or canon, and it changes nothing in the simulation it presents. Documents are reviewed editorially and by playtesting, never by CI ([#271](https://github.com/TomiToivio/NooPunk/issues/271)).

**Relationship to the rulebook.** The rulebook half of this issue is already delivered: `RULEBOOK.md` **§1.4** (*"How this book came to exist: Tommy Pilgrim, 1974"* — the download, the book, the genre, the fandom, and *"The 1974 decoder: presentation is not canon"*), **§2.2** (event cards), and **§35.8** (sound and music). **This document does not restate them.** It specifies the *art direction* they depend on, and defers to them for the narrative text itself.

---

## 1. The one rule

> **Presentation is not canon.** The 1974 layer decides how NoöPunk *looks, sounds and is narrated*. It never decides what is *true in the simulation*.

Everything below is an application of that sentence. Where a presentation choice and a canonical fact disagree, the canonical fact wins and the disagreement is displayed as a **deliberate 1974 misreading** (§5), never resolved by editing the fact.

---

## 2. Art direction

### 2.1 Film — the locked hierarchy, and nothing else

| # | Reference | What it supplies |
| --- | --- | --- |
| **1** | ***Zardoz* (1974)** | **The number-one visual and tonal reference.** Weird posthuman mysticism, institutional absurdity, radical costumes, theatrical science fiction. The tone is *earnest and strange*, never winking. |
| 2 | ***A Clockwork Orange* (1971)** | Social engineering, youth counterculture, stylised retrofuture, uncomfortable satire. |
| 3 | ***The Man Who Fell to Earth* (1976)** | Alien humanity, estrangement, media, consumerism, rock-star futurism. |

**Temporal caveat, carried verbatim in force:** *The Man Who Fell to Earth* was released **after** 1974. It is therefore a **modern art-direction reference**, or an influence on a **later Pilgrim adaptation** — never something Pilgrim saw before his download. Any in-universe attribution of it to the 1974 Pilgrim must be marked as an anachronism of the *adaptation*, not of the man.

**Only the named set.** No other film may be promoted to a primary inspiration. *"Do not substitute unfamiliar film references as primary inspirations"* is a constraint on this document as much as on the presentation.

### 2.2 Literary — the locked hierarchy

| # | Reference | What it supplies |
| --- | --- | --- |
| **1** | **Philip K. Dick** | **The number-one literary reference.** Ontological uncertainty, synthetic consciousness, prophetic paranoia, unreliable reality, VALIS. The whole framing device descends from him. |
| 2 | **Robert Anton Wilson** | Countercultural epistemology, conspiracies, psychedelic humour, philosophical ambiguity. |
| 3 | **Ursula K. Le Guin** | Serious anthropological, political, social and philosophical science fiction — the seriousness the strange surface must not lose. |

### 2.3 Sound

**Hawkwind — *Space Ritual* is soundtrack reference #1** and the sound of the download itself. Beneath it: early **Amon Düül II**, **Neu!**, and **Tangerine Dream's *Phaedra***. Space rock, kosmische Musik and early Krautrock texture shape pacing, sound design, cover art and interface atmospherics.

**Explicit negative:** prefer these to **generic synthwave / outrun / cyberpunk clichés**. The target is 1974 psychedelic SF, not 1980s neon.

### 2.4 Visual and interface language — the analog future

The design vocabulary, to be used across covers, illustrations, diagrams, UI, documentation and marginalia:

- punched cards, cassette reels, spools, paper tape;
- cathode-ray terminals, printed computer readouts, teletype;
- vacuum-fluorescent numerals, chunky knobs and switches, indicator lamps;
- brutalist and set-built rooms — institutional concrete, not sleek glass;
- vintage typography; psychedelic paperback cover aesthetics;
- strange posthuman fashion; period-inspired institutional design.

**The translation layer.** A device may be **correctly predicted in function and social consequence** while being **rendered as though it used punched cards or cassettes**. The rendering is the *presentation*; the actual simulated device stays technically correct unless an explicit canon deviation is approved.

**Accessibility is a hard constraint.** Psychedelic visuals must not compromise navigation, readability, data interpretation or operational UI. The aesthetic is a skin over a legible instrument.

---

## 3. Narrative framing

### 3.1 The 1974 decoder

Tommy Pilgrim is presented as a **Timothy Leary-style acid-head hippie**, an eccentric psychedelic counterculturalist, *and* a serious radical-left intellectual who reads **Deleuze and Guattari, Michel Foucault and Guy Debord**. For 1974 plausibility, only what was **available by 1974** can appear in the original book; later work may inform his subsequent commentary or revisions, and must be marked as such.

The prose must read as **someone channeling future history while tripping at a Hawkwind show in 1974** — not a contemporary cyberpunk story with a sepia filter.

### 3.2 The in-universe phenomenon

The novel *NoöPunk* became a cult classic and then a **film, TV series, tabletop RPG and computer RPG**; **NoöPunk is a science-fiction genre in-universe**, not one franchise; and its fandom is a **subculture** with its own lifestyle, philosophy, iconography, slang, music, politics and aesthetics. Specific customs are **left open** rather than fixed here.

Tommy is **still alive in Helsinki**, long known only to a cult readership, now recognised by literary scholars, courted by parapsychologists at several universities, and a highly eccentric media celebrity. **The ambiguity is preserved:** whether he received real precognition, was guided by VALIS, or accessed an alternative timeline is never settled. This is a **framing device**, not a licence to replace the scenario with metafiction.

### 3.3 Framing artefacts

The diegetic furniture that carries the layer:

- marginalia by Pilgrim, in his own hand;
- excerpts from **imaginary editions** of the novel;
- academic analysis of the novel and of its predictions;
- fandom ephemera — zines, letters, convention material, annotated reading lists;
- psychedelic chapter headings;
- seventies cover designs and faux archival diagrams;
- **diegetic book-versus-reality comparisons** — the device that makes the framing pay off.

**Tone discipline:** the future's ideological, geopolitical, social and ethical machinery stays **rigorous beneath the strange prose**. The comedy and the seriousness are not in tension; the comedy is *how* the seriousness gets told.

### 3.4 The model: *The Iron Dream* (Norman Spinrad, 1972)

The issue names this as **the literary model for the framing device**, and a framing specification that omits its own model leaves the device unexplained. It is recorded here in the section whose subject it is; the rulebook carries the bibliography entry at `RULEBOOK.md` §35.3.

**The work.** A **metafictional 1972 novel** by Norman Spinrad. Its surface is a novel-within-a-novel, ***Lord of the Swastika***, presented as written by an **alternate-history Adolf Hitler** — in that timeline he emigrated from Germany to the United States in 1919 after the Great War and became first a pulp science-fiction illustrator and then a writer of lurid pro-fascism stories under a thin science-fiction veneer. The nested text is followed by a **faux-scholarly afterword by the fictional critic Homer Whipple**. The book's own author attribution ("Adolf Hitler", actually Spinrad) is part of the joke.

**The three devices NoöPunk borrows — and nothing else:**

1. **The in-universe author.** A text whose author is a *positioned construct* rather than the real writer. This is the whole shape of the Pilgrim frame: the novel exists because a specific man, at a specific concert, in a specific year, wrote down what he saw.
2. **The apparently autonomous genre-fiction text.** The inner book has its own editions, reception and reputation *inside* the fiction — which is why Pilgrim's novel can have a fandom, adaptations and a scholarly literature without any of them being the real book.
3. **The fictional critical reception.** The faux-scholarly apparatus is what lets a text be *examined in-world* rather than merely quoted; it is the layer that makes §3.3's academic analysis and marginalia do work.

**What NoöPunk adds to the model:** **precognitive futurology** — Pilgrim's imagined future turns out to be disturbingly accurate, and whether that is real precognition, VALIS, or a neighbouring timeline is never settled (§3.2). *The Iron Dream* supplies the frame; the accuracy is NoöPunk's own addition to it.

**Guard, binding.** Borrow the **apparatus**, never the nested book's politics. Spinrad wrote the novel-within as **satire** — its point is to expose the appeal of fascist pulp — and NoöPunk's own author is a leftist. A reading that takes the inner text straight has misread the model, and the rulebook states the same guard at §35.3.

**Temporal note.** 1972 precedes Pilgrim's 1974 download, so unlike *The Man Who Fell to Earth* (1976) this reference may legitimately inform the **in-universe** 1974 frame as well as the out-of-universe reading.

**Left to the author, deliberately:** whether *The Iron Dream* also **joins the locked in-universe hierarchy** in §2.2 (or takes a fourth slot beside PKD, Wilson and Le Guin). Its date permits it; §2.2's own rule is to include only the named set, so this document does not add it.

---

## 4. The boundary, stated once

| Layer | Decides | May not decide |
| --- | --- | --- |
| **Presentation** (this document) | typography, palette, illustration, interface skin, cover art, marginalia, prose voice, the 1974 vocabulary a device is described in | what is true in the simulation, what a mechanic does, what the timeline contains |
| **Canon** (`RULEBOOK.md`, the rulebook, canon data) | setting, chronology, factions, institutions, technology, NHI/PSI/AGI concepts, rules and their outcomes | how it is illustrated or narrated |

**Aesthetic reskinning must not quietly alter the underlying simulation, chronology, canon or functionality.** That sentence is the acceptance test for every artefact this layer produces.

---

## 5. The discrepancy register — templates for non-disruptive slippage

Keep such mistakes **rare, conspicuous, and usually insignificant** to major events and systems. Four kinds, each with its display convention:

1. **The mistranslated device.** A real capability rendered in 1974 materials — a datacentre drawn as a room-sized thinking machine feeding on punched cards. **Display:** the illustration is period; a caption or footnote gives the accurate underlying capability. *Capabilities, networking and performance are unchanged.*
2. **The misnamed detail.** Pilgrim predicts an event correctly but gets a minor consumer product or the medium of communication wrong. **Display:** leave the event intact; flag the discrepancy in marginalia. Never let the wrong detail move a canonical outcome.
3. **The anachronistic witness.** A reference to something published after 1974 (including *The Man Who Fell to Earth*, 1976) appears near the 1974 material. **Display:** attribute it to a **later edition or adaptation**, explicitly — the anachronism is the *editions'* negotiation, not the man's memory.
4. **The neighbouring timeline.** A rare alternative-history note suggests Pilgrim saw a divergent branch. **Display:** mark it as unconfirmed and **do not** let it rewrite NoöPunk's canonical historical sequence. It adds mystery; it does not edit history.

---

## 6. Worked templates

### 6.1 Novel excerpt (period voice, accurate content)

> **CHAPTER XI — THE QUIET MINISTRIES**
>
> They did not announce the machine. That was the trick of it. It arrived the way the telephone arrived — first in the offices of people who could afford to be early, then in the shops, then in the hands of children who thought it had always been there. By the time anyone asked who was keeping the ledger, the ledger had been keeping itself for eleven years.
>
> *(Marginalia, Pilgrim, 1976: "I got the year wrong. It was sooner. I got the cassette wrong too — there is no cassette. I keep the cassette because I can draw it.")*

*What this demonstrates:* the period voice carries a **correct** account of institutional capture, with the error confined to a recording medium, and the correction attributed to Pilgrim himself rather than to the editor.

### 6.2 Marginalia convention

> `[TP]` — Pilgrim's own hand, in-period. May be wrong; is always sincere.
> `[ED. n]` — an editor of a later edition. Corrects facts, never the story.
> `[ARCHIVE]` — faux archival apparatus. Dates, provenance, catalogue numbers; period-styled.

### 6.3 Interface styling note

> **Panel: network overview.** Rendered as an oscilloscope trace over graph paper, with a paper-tape readout listing node labels. **Function:** unchanged — the same nodes, edges and filters; keyboard-navigable; every value legible as text. The skin is period; the data contract is not. *Accessibility is unaffected because the underlying component is the existing one.*

### 6.4 Alt-history discrepancy notice

> **Discrepancy 4.11 (minor).** Pilgrim names the treaty *"the Lisbon Accord"*; the canonical record has no such instrument. The event he describes — the first joint disclosure framework — occurs, at the canonical date, under a different name and a different city. **No canonical change.** The divergence is displayed, unconfirmed, and left unresolved.

---

## 7. Licensing and provenance

NoöPunk is intended as a **Creative Commons** project using **homebrewed, reskinned and modified mechanics** inspired by or adapted from the works below. The licences are **not interchangeable**, and this document does not claim they are.

| Source | Licence |
| --- | --- |
| **Fate Core System** (Evil Hat Productions), SRD | **Creative Commons Attribution 3.0 Unported (CC BY 3.0)**; also offered separately via OGL 1.0a. |
| **Transhumanity's Fate** (Posthuman Studios; Macklin and Graham) | **CC BY-NC-SA** |
| **Eclipse Phase Second Edition** (Posthuman Studios) | **CC BY-NC-SA 4.0 International**, subject to the publisher's stated exceptions |

**Guardrails, binding:**

- The **Fate CC BY permission does not override** the noncommercial/share-alike restrictions on anything copied or adapted from *Transhumanity's Fate* or *Eclipse Phase*. **CC BY-NC-SA material stays noncommercial**, and derivatives of it stay share-alike.
- **Do not** declare the project as a whole commercially reusable under CC BY, and **do not** assert that all components share a single licence. Mixed CC-BY and CC-BY-NC-SA components are **incompatible at the whole-project level** unless and until the provenance is audited.
- **Verify the exact edition and file notices and exceptions at release time**, and maintain attribution, licence notices and notices of modification for derivative material.
- **Separate generic mechanical ideas from copied protected expression.** Ideas are not the licensable part; expression is.
- This is a **provenance record, not legal advice**, and it authorises no release. The licence choice is the author's.

**The crucial distinction, restated because it is load-bearing:** NoöPunk's **timeline, lore, factions, species, politics, institutions, NHI/PSI/AGI concepts and scenario are entirely different from Eclipse Phase's.** NoöPunk is **not** set after Eclipse Phase's Fall; resleeving and cortical stacks remain rare and novel; and natural PSI is **not** an alien-virus-derived condition. The adapted mechanics do not import the setting.
**Where the licence authority lives, so this table cannot drift.** This section states the conditions; the **ledger is the authority**, and it is what a release gate reads. `docs/sources/EXTERNAL_SOURCE_LICENSES.md` (issue #60) carries the per-source findings and the file-level boundary — that noncommercial and share-alike conditions attach per file, and that a file mixing Eclipse-Phase-derived material cannot be re-licensed under an incompatible licence. `docs/sources/GAME_SYSTEM_RIGHTS.md` with `data/sources/game_system_rights.json` carries the rights record and the recommended release licence. `docs/sources/ATTRIBUTION.md` records that the licence is **not yet chosen** and points at issue #231's criterion 1. If this table and the ledger ever disagree, **the ledger wins and the disagreement is the finding** — not a wording preference to be settled here.

---

## 8. Non-goals

- It defines **no** rule, mechanic, statistic, threshold, cost or outcome, and no scenario, faction or timeline fact.
- It **restates no rulebook text**; §1.4, §2.2 and §35.8 are the authority for the narrative layer, and this document cross-references rather than duplicates them.
- It **adds no reference** to the locked hierarchies. *Zardoz* #1, PKD #1, *Space Ritual* #1, and only the named set.
- It **does not** treat the out-of-universe bibliography as Pilgrim's 1974 library. Works published after 1974 enter, if at all, as **later commentary or adaptation**, and the Miéville novels in particular must never be read as 1974 influences.
- It **does not** resolve whether Pilgrim's precognition was real, VALIS, or a neighbouring timeline.
- It carries **no automated test** ([#271](https://github.com/TomiToivio/NooPunk/issues/271)).

---

## 9. Cross-references

- `RULEBOOK.md` **§1.4 "How this book came to exist: Tommy Pilgrim, 1974"** — the Tommy Pilgrim introduction (the narrative text this document styles)
- `RULEBOOK.md` **§2.2 "Event cards: how this history reaches the table"** — event cards
- `RULEBOOK.md` **§35.8 "Sound and music"** — sound and music
- Issue [#447](https://github.com/TomiToivio/NooPunk/issues/447) — this brief, including the locked reference set and the presentation-versus-reality rule
- `RULEBOOK.md` **§35.3 "Fiction books"** — the bibliography entry for *The Iron Dream*, with the same guard as §3.4
- Licence authority, which the release gate reads rather than this document: `docs/sources/EXTERNAL_SOURCE_LICENSES.md`, `docs/sources/GAME_SYSTEM_RIGHTS.md`, `data/sources/game_system_rights.json`, `docs/sources/ATTRIBUTION.md`

**Numbering caution.** `RULEBOOK.md` carries **two** headings numbered `2.2`: *"Event cards: how this history reaches the table"* and *"AI as ideological conflict"*. Every citation above therefore names the heading as well as the number, so the reference cannot resolve to the wrong section. The duplicate numbering is pre-existing and is **flagged, not fixed** here — renumbering a ledger section is a separate change with its own reference-graph consequences.

