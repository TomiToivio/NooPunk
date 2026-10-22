# Standalone RPG module

## Responsibility

`src/rpg` is the narrative role-playing layer: scenes, dialogue nodes, choices, interactions, character checks, aspects, tags, conditions, consequences, narrative outcomes, lightweight conflicts, RPG state and integration-request events.

The module is intentionally conversation-, investigation- and therapy-first. Its conflict API is domain-neutral and deliberately not a tactical combat engine. Its small scene API is:

```python
character = load_character(character_markdown)
scenario = load_scenario(scenario_json)
session = RPGSession(character, scenario)

session.available_interactions()
result = session.perform_interaction("inspect_signal")
events = session.events
```

## Psyche-projektio

`src/rpg/astral.py` tarjoaa erillisen ensimmäisen version Psychen ei-lokaalin
projektion mekaniikasta. Se ei ole vielä kytketty Päivä 1:n kohtausmoottoriin.
API seuraa koherenssia, ruumiillista ankkuria, noeettista jälkeä, relationaalista
etäisyyttä ja dream/psychedelic/virtual/noetic-hypoteesien painoja.

Toiminnot ovat `enter`, `observe`, `traverse`, `resonate`, `manifest` ja
`return_to_body`. Mekaniikka tallentaa seuraukset ratkaisematta, oliko kokemus
uni, 80MG-tila, VR, astral projection vai usean kerroksen assemblage. Shadowrun-
vaikute ja reskin-rajat kuvataan tiedostossa
[`SHADOWRUN_INFLUENCE_AND_RESKIN.md`](SHADOWRUN_INFLUENCE_AND_RESKIN.md).

## Rules

Checks use a deliberately small Fate-inspired model:

```text
4dF + canonical attribute + learned skill + explicit tag/aspect bonuses
    + situational modifier vs difficulty
```

The canonical attributes are Intelligence, Awareness, Reflexes, Body, Charisma, Willpower and Cybernetics. Psyche remains an ontological character component, not an attribute.

Margins produce `critical_success`, `success`, `costly_success`, `failure` or `catastrophic_failure`. Every check interaction must define narrative outcomes, and the engine falls back to a neighboring tier when a specialized tier is omitted. Failure must advance the scene rather than return “nothing happens.”

This first version has no Fate Point economy. Aspects and tags only unlock interactions or provide explicit one-point bonuses declared by scene data. The exact implemented subset and intentional divergences from *Transhumanity's Fate* are documented in `TRANSHUMANITY_FATE_COMPATIBILITY.md`.

The complete playable tabletop subset and matching Python examples are documented in
[`NOOPUNK_RPG_RULES_V0_1.md`](NOOPUNK_RPG_RULES_V0_1.md). The public v0.1 API also
includes `resolve_action`, `Conflict`, `Relationship`, `intrude`, `use_psi`,
`resolve_psi_action`, `PsiActionContext`, `CrossLayerEffect`,
`PsychosurgerySession`, `Faction` and portable `GraphEffect` values. These use the
same resolver instead of creating separate social, cyber, PSI and combat dice systems.

The GQ-CAN PSI layer applies the wu-wei principle as a bounded trajectory modifier,
selects an ordinary action/approach from the PSI mode, and reports Psyche Load,
Noetic Trace and Instability. Cross-layer effects remain typed requests and enforce
their consent requirement before application; they do not integrate the independent
simulation loops.

## Human-readable data

Characters are Markdown files containing one fenced JSON block. The prose remains readable while the block is a shared machine-readable character source:

```text
Character Markdown -> Character Loader -> Character Object -> RPGSession
```

The RPG module does not maintain a second character model. It consumes the shared `Character` object produced by the loader. Scene and dialogue content lives in JSON; the engine contains no character- or story-specific branches.

## State and events

`RPGState` owns only RPG concerns: current scene/dialogue, flags, conditions, consequences, known information, completed interactions and session-local relationship values. Relationship outcomes use the social graph's existing integer scale, emit `relationship_changed` and store portable `GraphEffect` records. They do not mutate or autonomously simulate the NetworkX graph. Other integration events remain requests only.

Outcome voi asettaa `reset_session: true`, jolloin moottori luo puhtaan `RPGState`-tilan hahmon alkuperäisistä ehdoista ja siirtyy `next_scene`-kohteeseen tai skenaarion entry sceneen. Tätä käytetään Day 1:n turvallisessa restartissa; reset ei säilytä edellisen pelikerran flageja, löydöksiä, suhteita, suoritettuja interaktioita tai tapahtumahistoriaa.

Loader validoi scene-, dialogue- ja interaction-viitteiden lisäksi integraatiotapahtumien perusrakenteen. Dialogisolmu rajaa aina näkyvät toiminnot omaan `choices`-listaansa; tyhjä lista sulkee dialogin eikä paljasta scenen taustainteraktioita.

A later `hacking_encounter_requested` payload may request an isolated Physical, Astral or Cyber encounter, or a tightly coupled cross-layer assemblage. The ontological model is documented in `docs/PSYCHE_CROSS_LAYER_HACKING.md`; it is not implemented by the RPG engine.

## Module boundaries

- **RPG module:** narrative scenes, choices, checks, graph-effect requests and lightweight consequences. Implemented here.
- **Social Simulation module:** autonomous relationship and network simulation. Implemented separately, not integrated here.
- **Hacking Simulation module:** graph-based cybernetic and psychotronic hacking. Implemented separately, not integrated here.

> Näitä moduuleja ei vielä yhdistetä.

There is no shared simulation loop, unified game state, autonomous NPC system, physical map integration or noösphere integration.

## Day 1 — Pelattava vertikaalinen slice

Päivä 1 on toteutettu dataohjattuna skenaariona `data/rpg/scenarios/day_1.json`.
Se käyttää Romppaisen Narkkari-sivupersoonan hahmomallia
`data/rpg/characters/romppainen_narkkari.md` ja Transhumanity's Faten
24 skillin listaa ja 25 skill-pisteen budjettia Noöpunkin 7 attribute -järjestelmään mäpättyinä (SKILLS.md).

### Skenaariot

- **d1_arrival** — Saapuminen podiin, lomakkeiden tutkiminen
- **d1_reception** — Dr. Elin Dahlin vastaanotto: vihreä valo, printteri, kokeeseen valinta
- **d1_lab_arrival** — Ingrid Falkin ensikohtaaminen laboratoriossa (placeholder)
- **d1_lecture** — Pilgrim ja Tanaka: terapian perusteet -luento (placeholder)
- **d1_therapy_session** — Ensimmäinen terapiasessio: unisimulaatio Tukholmassa, Mars Eldrich, Ingridin The Fall -trauma, Elsa, Lotta Kallio, Mantidi, basilisk-virus
- **d1_investigation** — Salapoliisityöt: Tanaka/Pilgrim debrief, UFAB Ragnarök -hologrammi, lääkekaappi
- **d1_ufab_discovery** — UFAB-pillereiden varastaminen Ingridin kanssa, NHI-löytö, oikean persoonan välähdys (placeholder)
- **d1_evening** — Ilta: päivän reflektointi, Ingrid-mietteet (placeholder)
- **d1_dream** — Yöuni: Lotta Kallio / Pallas Athene -anomalia, Kiimainen Poliisi -tilan aktivointi (placeholder)
- **d1_end** — Päivän 1 loppu ja siirtymä DAY_2_NOT_IMPLEMENTED -placeholderiin

### Mechanikat

Päivä 1 käyttää seuraavia järjestelmiä:
- Scene-progression: 11 scenea, kullakin vakaa ID, dialogi, valinnat ja siirtymat
- Choice system: haarautuvat valinnat jotka palautuvat yhteen, vaikuttavat flageihin ja suhteisiin
- Social graph: Ingridin, Dahlin, Pilgrimin, Tanakan ja UFAB Ragnarökin suhdevaikutukset säilyvät session `relationships`-tilassa ja lähettävät sekä `relationship_changed`- että integraatiopyyntötapahtuman
- Player state: campaign_flags, conditions, known_information, consequences — kaikki persistoituvat scenejen välillä
- Dialogue: branching dialogue node -järjestelmä
- Investigation: UFAB-pullojen tutkiminen ja CAN-anomalian löytäminen tuottaa clueja
- News/world state: Mars Eldrichin risteilijä ja The Fall -uutiset terapiasession aikana
- Therapy/psychiatric: intake-flags, therapy_completed, cooperation score, anomaly detection
- End-of-day: day_1_complete -flag, siirtymä DAY_2_NOT_IMPLEMENTED -placeholderiin

### Placeholder-sisältö

Seuraavat scenejä on merkitty `content_status: placeholder`:
- d1_lab_arrival (Ingridin ensikohtaaminen)
- d1_lecture (Pilgrim/Tanaka-luento)
- d1_ufab_discovery (UFAB-bonding ja NHI-löytö)
- d1_evening (reflektointi)
- d1_dream (Lotta Kallio / Pallas Athene)

Placeholder-tekstit on kirjoitettu Noöpunk-tyylillä mutta ne ovat korvattavissa.
Kanoninen materiaali löytyy `PÄIVÄ_1.md`-tiedostosta.

### Tunnetut puutteet

- Päivä 2 ei ole toteutettu (DAY_2_NOT_IMPLEMENTED -placeholder)
- Autonominen graph-pohjainen sosiaalinen simulaatio ei ole integroitu; RPG-session suhdearvot ovat silti pysyviä päivän sisällä
- Graph-pohjainen psykotrooninen ja kyberneettinen hakkerointi ei ole toteutettu
- UFAB Ragnarökin (C.G. Jung) vuorovaikutus on yksinkertainen dialogi, ei CAN-pohjainen
- Mars Eldrichin uutislähetys on yksinkertainen teksti, ei dynaaminen media

## Neutral vertical slice

`data/rpg/scenarios/neutral_terminal.json` demonstrates one player character, one NPC, dialogue choices, a Fate check, an aspect-gated interaction, condition/consequence changes, fail-forward outcomes, a scene transition and inert integration-request events. It deliberately contains no Day 1 or Day 2 canon.

## UI

`src/rpg/ui.py` renders the current scene, NPC dialogue, selectable interactions, check result, relevant attributes, aspects, conditions, consequences, discoveries and relationship values in Streamlit. `app.py` launches playable Day 1 by default. The view remains thin over `RPGSession`; tests exercise the core without Streamlit.
