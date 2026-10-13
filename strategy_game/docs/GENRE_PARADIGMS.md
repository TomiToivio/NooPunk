# Paradigms and genres: Bionics, and the six NoöPunk genres (issue #359)

**PROPOSAL. No rule is approved, and this is not a locked taxonomy.** `strategy_game/RULEBOOK.md` still
says **NO RULES APPROVED**. The issue adds paradigms and genres to the setting; it authorises no
mechanic, and this record defines none.

| Artifact | Role |
| --- | --- |
| `strategy_game/data/genre_paradigms.json` | the three domains, the six genres and the typed inspirations |
| `strategy_game/genre_paradigms.py` | the reader and the three rules of the record |
| `strategy_game/tests/test_genre_paradigms.py` | code contracts (issue #271: code only) |

## 1. Three technologies of living, social and psychic worlds

| Domain | Technology | Scope | Systems correspondence |
| --- | --- | --- | --- |
| Biological systems / biosphere | **Bionics** | cells, organs, organisms and engineered biological intelligence, up to ecosystems and the planetary biosphere | biosphere |
| Psychic systems / noösphere | **Psychotronics** | individual consciousness and PSI, up to collective phenomena and the setting's Source Consciousness field | noösphere |
| Communication, information, machines and social networks | **Cybernetics** | prosthetics, BCIs and local computing, up to AI, networks, autonomous systems and sociotechnical infrastructure | social and technical networks |

**They interact; they are not exclusive.** Bionics is deliberately broader than the everyday word for
prosthetics: it means *technology working through biological systems*, whether restoring an ecosystem or
augmenting a human. And the correspondence table is a **game-design abstraction, not a claim that
Luhmann's social communication is identical to computers** — the Luhmannian distinction between
biological, psychic and social systems stays a setting commitment, which the reader enforces by refusing
a record that marks the domains mutually exclusive.

## 2. The six genres

| Genre | Established canon? | Centres on | What it changes |
| --- | --- | --- | --- |
| **Biopunk** | yes | bionics | biotechnology and living systems, from personal augmentation to restored or devastated planetary ecology |
| **Solarpunk** | yes | bionics | ecological repair, distributed resilient infrastructure, practical utopianism, and conflicts over energy, land, commons and power |
| **Nanopunk** | yes | all three | nanoscale engineering transforms matter, medicine, manufacturing, weapons and ecology, bridging the other two domains |
| **PSIpunk** | yes | psychotronics | PSI transforms institutions, politics, policing, crime, intimacy, privacy, hacking, ideology and warfare |
| **UFOpunk** | **no — internal definition** | — | disclosure, sightings, crash retrieval, cover-ups, abductions, ontological shock, rival services, and ordinary people adapting to reality breaking |
| **Xenopunk** | **no — internal definition** | — | alien, interdimensional and cryptoterrestrial intelligence; interspecies societies, asymmetric contact, coexistence versus assimilation and exploitation |

**The two internal definitions are flagged, not asserted.** The issue's own research found no widely
established genre canon for the names UFOpunk and Xenopunk, so they are recorded with
`established_genre_canon: false` as useful internal descriptors rather than claimed as schools. The
primary framing of the whole setting is unchanged: **New Weird + science fiction comedy + social science
fiction / science fantasy, with Cyberpunk influence.**

## 3. What these are not

- **Not new systems.** "Genres overlap without spawning separate game systems." The reader reports any
  genre that claims to spawn one, and the shipped vocabulary has none.
- **Not paradigm shifts — except Bionics.** PSIpunk is explicitly *a genre, not a new paradigm shift*,
  because PSI and psychotronics already exist as a paradigm (#345 owns that track). Bionics is the new
  paradigm shift, and it joins the two established domains.
- **Not a tech tree.** No genre is a progression, a cost or a prerequisite.

## 4. The epistemic rule, and how it is enforced

The issue requires distinguishing actual investigators and their hypotheses from NoöPunk fiction, where
the PSI and psychotronic paradigm shifts are settled features of the game world. So every inspiration is
typed — **fiction**, **named real research**, **a research field**, or **a research tradition** — and
every research-kind entry must declare a capability status:

- **early real research** — Levin's xenobots and bioelectricity, Endy's BioBricks, Zayner's DIY
  biohacking, Doudna and Charpentier's CRISPR, Church's genome engineering, Smirnova and Hartung's
  organoid intelligence, Kagan's DishBrain, Seeman's DNA nanotechnology, Rothemund's DNA origami, Mirkin's
  nanomaterials; Ostrom's commons, Raworth's doughnut economics, Meadows' systems thinking; and fields
  such as permaculture, rewilding, microgrids and perovskites.
- **a visionary proposal** — Feynman's miniaturisation vision and Drexler's molecular manufacturing, kept
  distinct from today's nanoscale research and from speculative universal assemblers and grey goo.
- **a research tradition** — Rhine's experimental parapsychology, Radin, Sheldrake's morphic resonance,
  Hennacy Powell, Tart, James, Myers, the **Ganzfeld** protocols and the **remote viewing / Stargate**
  history. These are real investigative traditions and contested results, **never** the fiction's
  achieved capabilities.

A research entry with no declared capability status would read as an achieved capability, so the reader
reports it as an unearned claim. Fiction is exempt only because its status is `not_applicable` by
definition — and a research record marked `not_applicable` is itself a defect the contracts catch.

## 5. What the author still has to decide

- Whether Bionics becomes a fourth **selectable** domain in the strategy layer or stays a framing beside
  the two established paradigms.
- Which genre the first playable slice foregrounds. The issue adds the genres to the setting; it does not
  authorise a subsystem for each.
- Whether the solarpunk ideological split (green primitivists, biotech eco-modernists, communitarian
  solarpunks, corporate greenwashing) becomes a recorded axis, a set of tags, or stays prose.
- How organoid intelligence and biohybrid AI sit against the AGI law restrictions already established
  for the setting.
