# Paradigms and genres: Bionics, and the six NoöPunk genres (issue #359)

**PROPOSAL. No rule is approved, and this is not a locked taxonomy.** `strategy_game/RULEBOOK.md` still
says **NO RULES APPROVED**. The issue adds paradigms and genres to the setting; it authorises no
mechanic, and this record defines none.

| Artifact | Role |
| --- | --- |
| `strategy_game/data/genre_paradigms.json` | the three domains, the six genres, the typed inspirations, the lens index, the candidates, the axes and the named cards |
| `strategy_game/genre_paradigms.py` | the reader and the rules of the record |
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
prior uses the research *did* find are recorded separately in `prior_uses`, each with the strength of
the claim it supports — an independent attestation (Mattix's *Disposable Heroes* marketed as a
"xenopunk thriller", the Transmoderna *XENOPUNK VR* installation), a scattered use (the Punktober /
UFOpunk retro-SF art tag, the *Caves of Qud* discussion), or a **false match** ("UFO punk" music
references and the unrelated xenopunk look-alikes). A `false_match` entry exists so a look-alike is
written down rather than forgotten and later mistaken for support; the reader refuses any prior use
that claims to have established canon.

The primary framing of the whole setting is unchanged: **New Weird + science fiction comedy + social
science fiction / science fantasy, with Cyberpunk influence.**

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

The catalogues now cover **fiction and non-fiction for every genre**, not only the four the issue's
table names: the UFOpunk non-fiction side is Vallée's *Passport to Magonia*, Pasulka's *American
Cosmic* and the live UAP/disclosure discussion, all typed as research *traditions*; Xenopunk's is
xenobiology, typed as early research; PSIpunk carries *The Telepathy Tapes* alongside Powell and
Sheldrake as a tradition of claims. The reader reports any genre left with only stories or only
researchers.

## 5. The further lenses: overlapping readings, never seventh genres

Fourteen further lenses are recorded in the index the issue asks for — **New Weird** (the primary
framing of the setting, per `AGENTS.md` §0, so it is the frame the others sit inside), **Lunarpunk**,
**Hopepunk**, **Cli-Fi**, **Silkpunk**, **Atompunk**, **Cassette futurism**, **Transhuman SF**,
**Mythpunk**, **Military SF**, **Ecopunk**, **Body horror**, **Postcyberpunk** and **Robopunk**. Each
carries a declared status (an established genre, a named movement, a self-defined aesthetic, a retro
aesthetic, an emerging aesthetic, a broad tradition, or an internal descriptor) and what it *adds*.
Robopunk is marked an internal descriptor, because the issue explicitly declines to assert an
established standardised subgenre for it.

Two structural rules hold the section to its own words:

- **A lens is never a compulsory genre declaration.** `lenses_that_spawn_a_system()` must stay empty,
  and the lens ids and the six genre ids must not overlap — a lens that quietly became a seventh genre
  with its own rules would be caught.
- **Where the issue names a work for a lens, the work is recorded under the lens** (Chambers,
  Robinson, Ken Liu, Egan, Valente, Haldeman, Bacigalupi, Cronenberg, Doctorow, Miéville), so the
  index is usable without adding those works to the genre-inspiration lists they do not belong to.

## 6. Candidate transformations: recorded, matrixed, and left unpromoted

The issue's near-future candidates are recorded with the compact matrix it asks for: each candidate
declares whether it is a **technology** or a **social** tendency, whether the issue flags it as a
priority, which of the three technology domains it **attaches to**, which event cards it feeds, which
research it would unlock, its fiction, and the author's own statement of the **game-facing conflict**
it creates. Ten technologies and ten social candidates are carried. The five the issue marks as
particularly strong — quantum, embodied AI/robotics, longevity, planetary engineering and
post-scarcity production — carry `priority: true`.

**Nothing is promoted.** Every candidate carries
`promotion: pending_author_decision` together with the issue's own design test: *only elevate a
candidate to a foundational paradigm if it changes what society considers possible, creates distinctive
factions and institutions, and materially reshapes the shared strategy/RPG loop — otherwise it stays a
genre lens, a project, a TAG or an event.* The reader exposes `promoted_paradigms()` (empty) and
`candidates_without_a_promotion_status()` (empty), so a promotion is a deliberate, visible act by the
author rather than something a later session can record by accident.

## 7. Pressure axes, strategic projects and event-card ideas

The faction responses the issue lists are recorded as **five pressure axes**, each a **pair of named
positions** — pro/anti-biotech, ecological restoration/extraction, open bio-commons/patent monopolies,
human enhancement/biological integrity, nano-acceleration/precaution. A one-pole axis is reported by
`axes_that_are_not_pairs()`, because a single pole is a scale in disguise, and every axis carries
`recorded_as: pending_author_decision`: whether an axis becomes a recorded tag set or stays prose is
the open question the document already carries, and `AGENTS.md` §0 keeps the existing political axes
and party identities intact.

Seven **strategic projects** (an organoid-computing breakthrough, living seawalls, engineered coral
recovery, a decentralised biofoundry, an NHI biotechnological exchange, a contaminated nanofactory, a
runaway synthetic ecology) and eleven **event-card ideas** (the Esper Union's privacy demand, the
organoid personhood claim, the communal biofoundry's watershed, the disputed nanoswarm cleanup,
disclosure without explanation, the hybrid citizenship referendum, and the five cross-cutting cards —
robotic workforce strike, rejuvenation patent scandal, neural privacy injunction, atmospheric
intervention vote, post-scarcity factory) are carried as the issue's own titles.

**They carry no effects.** Every one has `effects: []`, and `proposals_with_effects()` reports any that
does not. A card title is a title: the issue supplies these to show what the paradigms *could* produce,
and a cost, an outcome or a threshold arriving through a card name would be an unapproved mechanic.
They are recorded as cards, projects and TAG ideas rather than as six tactical rulesets — which is what
the issue asks for.

## 8. What the author still has to decide

- Whether Bionics becomes a fourth **selectable** domain in the strategy layer or stays a framing beside
  the two established paradigms.
- Which genre the first playable slice foregrounds. The issue adds the genres to the setting; it does not
  authorise a subsystem for each.
- Whether the solarpunk ideological split (green primitivists, biotech eco-modernists, communitarian
  solarpunks, corporate greenwashing) becomes a recorded axis, a set of tags, or stays prose.
- How organoid intelligence and biohybrid AI sit against the AGI law restrictions already established
  for the setting.
- **Which of the twenty candidate transformations, if any, is promoted to a foundational paradigm**,
  and which of the five pressure axes is recorded as a tag axis. Both are carried as
  `pending_author_decision`; neither is decided here.
- Whether the five pressure axes extend the faction vocabulary of
  [`docs/GLOBAL_FACTIONS.md`](GLOBAL_FACTIONS.md) and [`data/faction_creation.json`](../data/faction_creation.json)
  or stay a reading of the genre layer. This record does not touch either.
