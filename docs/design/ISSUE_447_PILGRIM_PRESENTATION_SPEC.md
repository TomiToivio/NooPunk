# Tommy Pilgrim presentation layer — art-direction and narrative-framing specification (issue #447)

**Status: SPECIFICATION, PROPOSAL. Presentation only.** This document defines how NoöPunk is *presented* as a 1974-origin work. It defines **no** rule, mechanic, statistic, scenario fact, chronology or canon, and it changes nothing in the simulation it presents. Documents are reviewed editorially and by playtesting, never by CI ([#271](https://github.com/TomiToivio/NooPunk/issues/271)).

**Relationship to the rulebook.** The narrative layer is already delivered: `RULEBOOK.md` **§1.4** (*"How this book came to exist: Tommy Pilgrim, 1974"*), **§2.2** (*"Event cards"*), and **§35.8** (*"Sound and music"*), with the film and literature references in **§35**. **This document does not restate them**; it specifies the art direction they depend on.

---

## 1. The governing maxim

> **NoöPunk looks as if it was MADE in the seventies — not SET in the seventies.**

**The core pitch.** NoöPunk is presented as though it were a **lost psychedelic science-fiction film made in 1974**, somehow predicting real history up to **2026** with startling precision. **After 2026 its future is contested and changeable.**

This is an aesthetic, storytelling and eventual indie-graphics rule. It is **not** a retcon: 2026 computer technology does not run on punched cards. The scenario and its science, sociology, geopolitical events and technology stay grounded in the established NoöPunk timeline. **The 1974 author/director's visual imagination is an intentionally unreliable decoder of genuinely precognitive visions.**

### 1.1 The one rule

> **Presentation is not canon.** The 1974 layer decides how NoöPunk *looks, sounds and is narrated*. It never decides what is *true in the simulation*.

Where a presentation choice and a canonical fact disagree, **the canonical fact wins**, and the disagreement is displayed as a **deliberate 1974 misreading** (§5), never resolved by editing the fact.

---

## 2. Art direction

### 2.1 Film — the locked hierarchy

| # | Reference | What it supplies |
| --- | --- | --- |
| **1** | ***Zardoz* (1974)** | **The number-one live-action visual and tonal reference — its position does not move.** Weird posthuman mysticism, institutional absurdity, radical costumes, theatrical science fiction. Earnest and strange, never winking. |
| 2 | ***A Clockwork Orange* (1971)** | Social engineering, youth counterculture, stylised retrofuture, uncomfortable satire. |
| 3 | ***The Man Who Fell to Earth* (1976)** | Alien humanity, estrangement, media, consumerism, rock-star futurism. |

**Temporal caveat, in force:** *The Man Who Fell to Earth* was released **after** 1974 — a **modern art-direction reference** and a **later-adaptation** influence, never something Pilgrim saw before his download.

### 2.2 Graphic art — added references

| Reference | What it supplies | Chronology caution |
| --- | --- | --- |
| **Jean Giraud / Mœbius** | Elegant, intricate lines; astonishing spaces; impossible architectures; visionary desert and urban landscapes; strange vehicles; alien and posthuman silhouettes; mature European psychedelic SF comics. | His ***Métal Hurlant*** work belongs to the **mid/late 1970s** — later than a 1974 download. **Distinguish later real-world artistic influence from Tommy's precise 1974 source materials.** |
| **Pierre Christin and Jean-Claude Mézières, *Valérian et Laureline* (begun 1967)** | Colourful, imaginative planetary and extraterrestrial civilisations; inhabited SF worlds; intricate environments; visually striking uniforms, spacesuits, machines and species. | **Available before 1974.** Keep its **playfulness and social observation** alongside Mœbius's cosmic strangeness. |

**Goal for future retro-indie graphics:** an **original, feasible, readable synthesis** of that European bande dessinée language with *Zardoz*-scale psychedelic absurdism, 1970s cinematic production design and period SF-paperback illustration.

**Hard constraint:** do **not** reproduce copyrighted panels, character designs or signature illustrations. Take the *language*, never the *artefacts*.

### 2.3 Literary — the locked hierarchy

| # | Reference | What it supplies |
| --- | --- | --- |
| **1** | **Philip K. Dick** | **The number-one literary reference.** Ontological uncertainty, synthetic consciousness, prophetic paranoia, unreliable reality, VALIS. |
| 2 | **Robert Anton Wilson** | Countercultural epistemology, conspiracies, psychedelic humour, philosophical ambiguity. |
| 3 | **Ursula K. Le Guin** | Serious anthropological, political, social and philosophical science fiction. |

### 2.4 Visual vocabulary

Theatrical costumes and strange hats · saturated poster colours and cosmic gradients · alien geometries and impossible interior architecture · brutalist research facilities · physical props and set-built consoles · cathode-ray tubes, teleprinters, switches, analogue meters, tape decks, magnetic reels, punch cards, printed graphs and retro scientific diagrams · hand-inked outlines, poster-like flat colours, stippled textures, comics-panel compositions · illustrated mission cards · faux 1974 book and film jackets.

**Favour the slightly theatrical look of practical effects over glossy contemporary cyberpunk UI.**

### 2.5 Six concrete future-graphics concepts

1. **LLM / AGI dialogue.** An enormously intelligent language-model interface presented on a **1974 mainframe** — blinking lamps, huge tape reels, punched-card readers, a teletype. The dialogue, reasoning and societal consequences are **accurate for the simulated future**; punch cards are **representation**, not a mandatory in-world implementation.
2. **Social media / discourse mapping.** Statistically meaningful communication-network simulation visualised as psychedelic TV broadcasts, ticker tape, analogue network maps, cathode-ray diagrams and dossiers.
3. **NHI contact.** Mœbius/Valérian-like strange architectures, biologics and extraterrestrial environments meeting *Zardoz*'s theatrical mysticism. **Do not make NHI evidence more conclusive than the scenario says.**
4. **PSI / remote-viewing laboratory.** EEG-like chart recorders, oscilloscopes, sensory-deprivation gear, hand-drawn brain diagrams, elaborate electronic apparatus, institutional researchers — **with the actual PSI rules and confidence levels preserved**.
5. **Faction board / Event Cards.** Retro SF-comics covers and period newspaper/academic-report collage, with simple icons, a strong type hierarchy, legible card rules, and **visual distinction between prophecy, observable evidence and uncertain hypotheses**.
6. **Map and fieldwork.** Bird's-eye board-game maps of Helsinki and other sites; hand-inked location panels; travel folders; small human silhouettes. **Scalable to indie-friendly 2D sprites without photorealism.**

### 2.6 Production constraints

Build a **low-cost, adaptable art bible** before committing to shaders or assets: palette and typography prototypes, 2D sprites and portraits, card templates, UI and backgrounds.

**Precedence, binding:** small-screen readability, accessibility, a **reduced-motion alternative** for psychedelia, and **visual explanations of actual data** all take precedence over spectacle.

> **Retro presentation must never falsify quantitative UI information.**

**Only the named set, plus §2.2.** *"Do not substitute unfamiliar film references as primary inspirations."*

---

## 3. Writing

### 3.1 Voice

The **writing**, not only the illustrations, carries 1974's intellectual and material imagination: radical 1970s futurology, psychedelic New Wave prose, social-science essays, obscure technical jargon, institutional absurdity, dry countercultural comedy.

Pilgrim describes **realistically correct later concepts** — LLMs, AGI, attention architectures, ideological polarisation, AI agents, BCI, PSI claims, NHI uncertainties — with surprisingly apt functional and sociological insight, while getting the **packaging** wrong: typewriters, punched-card conversational engines, pneumatic mail, television-based social networks, cassette intelligence modules. **This does not mean all canonical technology actually works that way.**

### 3.2 The rare timeline-slip rule

The author sometimes uses a **different minor political name, consumer brand, election date, chronology detail or background invention** — suggesting error, imperfect translation, or a neighbouring possible timeline.

Keep these divergences **rare, identified, minor and non-cascading**. **Do not silently revise major canonical events, dates, countries, institutions, research evidence or causality.**

> Where the text is a **verified historical assertion** rather than a Pilgrim excerpt, use the **canonically correct** information. The future after the currently verified point can branch through player and faction agency.

### 3.3 Illustrative passage

> In the Year 2026 the Ministers consulted the Great Linguistic Engine. Fifty million citizens had deposited their passions into the public television wires, and the Engine, having read the whole quarrel in less than one second, announced that the Nation was suffering from six incompatible definitions of reality. Its operators inserted a fresh card deck. One card, mispunched, bore the date 2027.

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

### 3.5 Framing convention

Contrast an in-world **"Pilgrim, 1974 edition"** excerpt with an **"Editorial / Simulation note, 2026"** whenever a charming 1970s misconception might otherwise mislead the player.

**Do not make the rulebook opaque parody.** Narrative flavour in controlled doses; **actual mechanics, instructions, timeline entries and scientific discussion remain clear.**

### 3.6 Sound

**Hawkwind's *Space Ritual* = #1** soundtrack and tone. **Neu!** = propulsive motorik and technological momentum. **Tangerine Dream's *Phaedra*** = cosmic, anomalous and metaphysical atmosphere. **Early Amon Düül II** = political upheaval and hallucinatory disorientation.

Prefer **real period space rock / Krautrock / kosmische Musik** over generic retro synthwave. **Explicit negative:** not 1980s neon.

**Licensing:** the original recordings are **references, not presumed cleared assets.** Commission or create original music, or license recordings separately.

---

## 4. The boundary, stated once

| Layer | Decides | May not decide |
| --- | --- | --- |
| **Presentation** (this document) | typography, palette, illustration, comics language, interface skin, cover art, marginalia, prose voice, the 1974 vocabulary a device is described in | what is true in the simulation; what a mechanic does; what the timeline contains |
| **Canon** (`RULEBOOK.md`, the rulebook, canon data) | setting, chronology, factions, institutions, technology, NHI/PSI/AGI concepts, rules and outcomes | how it is illustrated or narrated |

**Aesthetic reskinning must not quietly alter the underlying simulation, chronology, canon or functionality.** That sentence is the acceptance test for every artefact in this layer.

**Accessibility is a hard constraint throughout.** Psychedelic visuals must not compromise navigation, readability, data interpretation or operational UI.

---

## 5. The discrepancy register

Four kinds, each with a display convention. All are **rare, conspicuous and insignificant** to major systems, and **none may move a canonical outcome**.

1. **The mistranslated device.** A real capability rendered in 1974 materials — a datacentre drawn as a room-sized thinking machine feeding on punched cards. **Display:** period illustration; caption or footnote gives the accurate capability. *Capabilities, networking and performance unchanged.*
2. **The misnamed detail.** An event predicted correctly, a minor product or communication medium wrong. **Display:** leave the event intact; flag the discrepancy in marginalia.
3. **The anachronistic witness.** A post-1974 reference (including *The Man Who Fell to Earth*, 1976; *Métal Hurlant*; Vallée's *The Invisible College*, 1975; Marks and Kammann, 1978) near 1974 material. **Display:** attribute it to a **later edition, revision or adaptation** — the anachronism is the *editions'* negotiation, not the man's memory.
4. **The neighbouring timeline.** A rare alternative-history note. **Display:** mark it unconfirmed; it adds mystery and **must not** rewrite the canonical historical sequence.

---

## 6. Worked templates

### 6.1 Novel excerpt (period voice, accurate content)

> **CHAPTER XI — THE QUIET MINISTRIES**
>
> They did not announce the machine. That was the trick of it. It arrived the way the telephone arrived — first in the offices of people who could afford to be early, then in the shops, then in the hands of children who thought it had always been there. By the time anyone asked who was keeping the ledger, the ledger had been keeping itself for eleven years.
>
> *(Marginalia, Pilgrim, 1976: "I got the year wrong. It was sooner. I got the cassette wrong too — there is no cassette. I keep the cassette because I can draw it.")*

### 6.2 Marginalia convention

> `[TP]` — Pilgrim's own hand, in-period. May be wrong; always sincere.
> `[ED. n]` — an editor of a later edition. Corrects facts, never the story.
> `[ARCHIVE]` — faux archival apparatus: dates, provenance, catalogue numbers, period-styled.
> `[SIM 2026]` — **Editorial / Simulation note.** Required wherever a 1974 misconception could mislead; states the canonically correct information.

### 6.3 Interface styling note

> **Panel: network overview.** Rendered as an oscilloscope trace over graph paper, with a paper-tape readout listing node labels. **Function:** unchanged — the same nodes, edges and filters; keyboard-navigable; every value legible as text; a reduced-motion alternative is provided. The skin is period; the data contract is not. *Accessibility is unaffected because the underlying component is the existing one.*

### 6.4 Alt-history discrepancy notice

> **Discrepancy 4.11 (minor).** Pilgrim names the treaty *"the Lisbon Accord"*; the canonical record has no such instrument. The event he describes — the first joint disclosure framework — occurs, at the canonical date, under a different name and a different city. **No canonical change.** The divergence is displayed, unconfirmed, and left unresolved.

---

## 7. The 1970s reference shelf

Actual 1970s intellectual world, used as **vocabulary, bookshelves, documents and laboratory aesthetics**. This is **history of ideas — not validation of unproven UFO or psi hypotheses.**

| Domain | Period source / claim | Use in NoöPunk | Caution |
| --- | --- | --- | --- |
| Futurology | **Alvin Toffler, *Future Shock* (1970)** | Characters describe mass disorientation as *future shock*; anticipate institutional lag | Sociological forecasting, not supernatural foresight |
| Systems futurology | **Donella Meadows et al., *The Limits to Growth* (1972)**, World3 scenarios | Computer-generated global futures; line-printer graphs, scenario charts, interdependent variables | **Conditional model scenarios**, not precise forecasts of fixed events |
| Scientific ufology | **J. Allen Hynek, *The UFO Experience* (1972)** | UNSA predecessors' coded case reports, witness interviews, unexplained categories | Unexplained sightings are **not** proof of extraterrestrial/NHI origin |
| Speculative ufology | **Jacques Vallée, *The Invisible College* (1975)** | Debate on psychological, cultural, interdimensional or anomalous-contact models | **Post-1974:** later revisions, design research or commentary. Hypotheses unverified |
| Parapsychology | **Targ and Puthoff, "Information transmission under conditions of sensory shielding"**, *Nature* (1974) | Shielded-room experiments, remote-viewing sketches, sensor arrays, blind targets, grant reports | Findings **disputed**; published **18 October 1974**, which may **postdate** Tommy's unspecified 1974 concert/download — do not assume he had read it |
| Critical scrutiny | **Marks and Kammann, "Information transmission in remote viewing experiments"**, *Nature* (1978) | Contradictory reports and sceptical internal review; distinguish conclusions from data | Later replication **did not verify** Targ/Puthoff. Later commentary, **not** a 1974 text |

**Interpretation guideline.** Represent 1970s scientific **uncertainty and competing expectations**, not a fake consensus. It is legitimate in NoöPunk *fiction* for later 2026 in-world revelations to vindicate an earlier prediction; those later fictional facts **must not be presented as a real-world scientific discovery**. **1974 Pilgrim can have visions of later work, but his contemporary footnotes must accurately distinguish what had and had not yet been published.**

---

## 8. Licensing and provenance

A **Creative Commons** project using **homebrewed, reskinned and modified mechanics** inspired by or adapted beneath. The licences are **not interchangeable**, and this document does not claim they are.

| Source | Licence |
| --- | --- |
| **Fate Core System** (Evil Hat), SRD | **CC BY 3.0 Unported**; also offered separately via OGL 1.0a |
| **Transhumanity's Fate** (Posthuman Studios) | **CC BY-NC-SA** |
| **Eclipse Phase Second Edition** (Posthuman Studios) | **CC BY-NC-SA 4.0 International**, subject to the publisher's stated exceptions |

**Guardrails, binding:**

- The **Fate CC BY permission does not override** the noncommercial/share-alike restrictions on anything from *Transhumanity's Fate* or *Eclipse Phase*. CC BY-NC-SA material stays noncommercial and its derivatives stay share-alike.
- **Do not** declare the project as a whole commercially reusable under CC BY, and **do not** assert a single project-wide licence. Mixed CC-BY and CC-BY-NC-SA components are **incompatible at whole-project level** until provenance is audited.
- **Verify the exact edition and file notices and exceptions at release time**; maintain attribution and notices of modification.
- **Separate generic mechanical ideas from copied protected expression.**
- This is a **provenance record, not legal advice**, and it authorises no release. The licence choice is the author's.
- **Illustrations, panels and music are references, not assets.** Comics references supply a *language*, never reproducible panels; the named recordings are not presumed cleared.

**Load-bearing distinction:** NoöPunk's **timeline, lore, factions, species, politics, institutions, NHI/PSI/AGI concepts and scenario are entirely different from Eclipse Phase's.** NoöPunk is **not** set after the Fall; resleeving and cortical stacks remain rare; natural PSI is **not** virus-derived.

---

## 9. Non-goals

- No rule, mechanic, statistic, threshold, cost, outcome, scenario, faction or timeline fact.
- It **restates no rulebook text**; §1.4, §2.2 and §35.8 are the authority for the narrative layer.
- It **adds no primary film or literary reference** beyond the named set and §2.2's graphic additions.
- It does **not** treat the out-of-universe bibliography as Pilgrim's 1974 library; post-1974 works enter only as later commentary or adaptation. The Miéville novels must never be read as 1974 influences.
- It does **not** resolve whether Pilgrim's precognition was real, VALIS, or a neighbouring timeline.
- No automated test ([#271](https://github.com/TomiToivio/NooPunk/issues/271)).

---

## 10. Acceptance position against the issue's checklist

| Issue check | Position |
| --- | --- |
| Enforce *"made in 1974, not set in 1974"* for art, prose and presentation | **§1, §4** — stated as the governing maxim |
| Add Mœbius and *Valérian* prominently to graphic references, *Zardoz* staying #1 | **§2.2** — with the *Métal Hurlant* chronology caveat; the rulebook's §35 visual list also gains them |
| Prototype an accessible illustrated UI/event card and one punch-card LLM scene | **§2.5(1), §2.5(5), §2.6, §6.3** — specified, **not built**; a prototype is a separate deliverable and no art bible exists yet |
| 1970s futurology/ufology/parapsychology flavour, exposition readable | **§3.1, §3.4** |
| Annotate minor slippages rather than silently changing canon | **§3.2, §5, §6.4** |
| Period references and correct pre/post-1974 chronology in the sources list; label contested claims | **§7** — with the rulebook sources gaining the same |
| Retain Hawkwind, Neu!, Tangerine Dream, Amon Düül II; licences separate | **§3.5** |

---

## 11. Cross-references

- `RULEBOOK.md` **§1.4 "How this book came to exist: Tommy Pilgrim, 1974"** — the narrative text this document styles
- `RULEBOOK.md` **§2.2 "Event cards: how this history reaches the table"**
- `RULEBOOK.md` **§35 "Sources, recommended reading, and influences"** — the film and literature lists, where the graphic references and the period shelf are added
- `RULEBOOK.md` **§35.8 "Sound and music"**
- Issue [#447](https://github.com/TomiToivio/NooPunk/issues/447) — this brief

**Numbering caution.** `RULEBOOK.md` carries **two** headings numbered `2.2`: *"Event cards: how this history reaches the table"* and *"AI as ideological conflict"*. Citations therefore name the heading as well as the number. The duplicate is **flagged, not fixed** — renumbering a ledger section is a separate change with its own reference-graph consequences.
