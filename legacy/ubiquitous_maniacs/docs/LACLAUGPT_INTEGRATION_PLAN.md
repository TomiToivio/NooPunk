# Integration Plan: LaclauGPT Political Analysis → Noöpunk RPG

## Status: Proposal — ei vielä toteutettu

Tämä dokumentti suunnittelee miten LaclauGPT-Data-Storage-reposta kopioidut
poliittisen analyysin työkalut integroidaan Noöpunk: Ubiquitous Maniacs
-roolipeliin. Jokainen vaihe on itsenäinen — toteutetaan vain kun Tomi pyytää.

---

## Mitä kopioitiin

| Tiedosto | Lähde | Kohde | Sisältö |
|---|---|---|---|
| `discourse_graph.py` | `ontology/` | `src/political/` | Pydantic-mallit: Social, Castells, Laclau graafit |
| `populism_analysis.py` | `hungary_splitting/` | `src/political/` | Laclau & Palonen populistinen analyysi (Ollama) |
| `postprocess_analysis.py` | `hungary_splitting/` | `src/political/` | Topic/entity/sentiment-ekstraktio (Ollama) |
| `classifier.py` | `ontology/` | `src/political/` | Zero-shot tekstiklassifikaatio (BART-MNLI) |
| `sentiment.py` | `ontology/` | `src/political/` | XLM-R monikielinen sentiment-analyysi |
| `PHILOSOPHICAL_FRAMEWORK.md` | repo juuri | `docs/` | Ain 17 kohdan filosofinen manifesti |

---

## Nykytila

Noöpunkissa on jo:
- `src/game/social_graph.py` — 6-dimensionaalinen sosiaalinen verkko (trust, attraction, fear, suspicion, authority, familiarity)
- `src/game/state.py` — GameState joka yhdistää RPG + social + hacking
- `src/rpg/` — Fate Core -engine, skill checkit, NPC-muistit
- `src/hacking/layered.py` — 4-kerroksinen psykotroninen hacking
- `play.py` — terminaalipeli

LaclauGPT:ssä on:
- `discourse_graph.py` — Castells/Laclau/Social Pydantic-mallit graafiekstraktioon
- `populism_analysis.py` — Ollama-promptit Laclau/Palonen populistiselle analyysille
- `postprocess_analysis.py` — Ollama-promptit topic/entity/sentiment-ekstraktiolle
- `classifier.py` — HuggingFace zero-shot klassifikaatio
- `sentiment.py` — HuggingFace XLM-R sentiment

---

## Vaihe 1: discourse_graph.py adapter (keskitaso)

**Tavoite:** Yhdistä Noöpunkin sosiaaligraafi LaclauGPT:n Castells/Laclau-malleihin.

**Mitä tehdään:**
- `src/political/discourse_adapter.py` — funktio joka ottaa `MultiDimensionalSocialGraph`-olion ja tuottaa `CombinedGraphExtraction`-mallin (Social + Castells + Laclau)
- Noöpunkin hahmot (Romppainen, Ingrid, Pilgrim, Tanaka, Dahl, Ragnarök) mapataan `CastellsNode`-tyypeiksi:
  - Ragnarök = `ProgrammingPower` (ohjelmoija, asettaa säännöt)
  - Pilgrim = `SwitchingPower` (kytkijä, hallitsee liityntäpisteitä)
  - Dahl = `Hub` (portinvartija, gatekeeper)
  - Romppainen = `Node` (potilas, verkoston reunalla)
  - Ingrid = `Node` (potilas, verkoston reunalla)
  - Tanaka = `Counterpower` (vastavoima, etiikan vartija)
- Noöpunkin suhdedimensiot (trust, suspicion, authority...) mapataan `CastellsEdge`-relaatioiksi:
  - authority > 2 → `programs` tai `dominates`
  - trust < -1 → `opposes`
  - suspicion > 2 → `excludes`
  - trust > 2 → `connects`

**Riippuvuudet:** pydantic (jo Noöpunkin requirements.txt:ssä)

**Testit:** Adapterin yksikkötestit — social graph → CombinedGraphExtraction

---

## Vaihe 2: Populism-analyysi NPC-dialogeille (matala prioriteetti)

**Tavoite:** Analysoi NPC-dialogeja Laclau/Palonen populistisella kaavalla.

**Mitä tehdään:**
- `src/political/populism_analysis.py` — adaptoi Hungary-pipeline:n populism.py:n promptit Noöpunkin kontekstiin
- Vaihda "2026 elections in Hungary" → "C.G. Jung -instituutin valtadynamiikka"
- Syöte: NPC:n dialogiteksti + social graph -konteksti
- Tuloste: `FormulaOfPopulism` (populism_analysis, populism_us, populism_frontier)
- Integroi `GameState.perform_rpg_interaction()` -metodiin: kun pelaaja käy dialogia NPC:n kanssa, optionally ajetaan populism-analyysi ja tallennetaan NPC:n social graph -solmuun

**Riippuvuudet:** ollama (paikallinen tai cloud), pydantic

**Huomio:** Tämä on raskas — ajetaan vain Jos Tomi pyytää, ei automaattisesti.

---

## Vaihe 3: Sentiment-analyysi NPC-mielialoille (matala prioriteetti)

**Tavoite:** Automaattinen sentiment-analyysi NPC-dialogille XLM-R-mallilla.

**Mitä tehdään:**
- `src/political/sentiment.py` — adaptoi sentiment.py Noöpunkin kontekstiin
- Syöte: NPC:n dialogiteksti
- Tuloste: positive/neutral/negative -score
- Integroi `GameState.perform_rpg_interaction()` -metodiin: päivitä NPC:n `mood`-kenttää sentiment-analyysin perusteella
- Esim: jos NPC:n dialogi on negatiivinen → mood muuttuu "hostile" tai "suspicious"

**Riippuvuudet:** transformers, torch (raskas — ei välttämättä sopii Noöpunkin kevyeen arkkitehtuuriin)

**Huomio:** Tämä vaatii HuggingFace-transformersin asentamisen. Harkitse vaihtoehtoisesti kevyempää Ollama-pohjaista sentiment-analyysia.

---

## Vaihe 4: Zero-shot klassifikaatio sceneille (matala prioriteetti)

**Tavoite:** Klassifikaattori joka tunnistaa scene-tyypin tekstistä.

**Mitä tehdään:**
- `src/political/classifier.py` — adaptoi classifier.py Noöpunkin scene-tyypeiksi
- Kandidaattilabelit: "therapy", "investigation", "social interaction", "dream", "hacking", "bureaucracy", "confrontation"
- Syöte: scene-description + dialog
- Tuloste: label + score
- Käyttö: voisi自动isesti valita scene-tyypin joka vaikuttaa NPC-mielialaan tai skill check -vaikeuteen

**Riippuvuudet:** transformers, torch

---

## Vaihe 5: PHILOSOPHICAL_FRAMEWORK.md kanonisointi (korkea prioriteetti)

**Tavoite:** Yhdistä Ain filosofinen manifesti Noöpunkin CAN-dokumentaatioon.

**Mitä tehdään:**
- Ristiinviittaa `docs/PHILOSOPHICAL_FRAMEWORK.md` ja `docs/CAN_MICROFOUNDATION_HOFFMAN_FAGGIN.md`
- PHILOSOPHICAL_FRAMEWORK.md kohta 3 (Fagginin QIP) → CAN-mikrotason dokumentti
- PHILOSOPHICAL_FRAMEWORK.md kohta 4 (Jung) → SISÄAVARUUS.md
- PHILOSOPHICAL_FRAMEWORK.md kohta 6 (NHI) → NHI_ONTOLOGY.md
- PHILOSOPHICAL_FRAMEWORK.md kohta 9 (AI) → AGI-skenaario
- PHILOSOPHICAL_FRAMEWORK.md kohta 13 (Marxism/Laclau/Castells) → Noöpunkin poliittinen kerros
- Lisää README.md:hen viittaus PHILOSOPHICAL_FRAMEWORK.md:hen

**Riippuvuudet:** Ei koodia — vain dokumentaatio

---

## Priorisointi

1. **Vaihe 5** (PHILOSOPHICAL_FRAMEWORK kanonisointi) — ei koodia, nopea, korkea arvo
2. **Vaihe 1** (discourse_graph adapter) — keskitaso, pydantic jo saatavilla
3. **Vaihe 2** (populism-analyysi) — vain jos Tomi pyytää, vaatii Ollaman
4. **Vaihe 3** (sentiment) — vain jos Tomi pyytää, raskas
5. **Vaihe 4** (klassifikaattori) — vain jos Tomi pyytää, raskas

---

## Episteemiset kerrokset (tärkeä muistutus)

Noöpunkin kolme episteemistä kerrosta säilyvät erillään:

1. **Hard science:** NetworkX, sosiaalinen graafi, Fate RPG -mekaniikat
2. **Speculative philosophy:** CAN, Hoffman, Faggin, Kastrup, Jung
3. **RPG fiction:** UFAB, psykokirurgia, Mantidit, Ragnarök

LaclauGPT:n poliittinen analyysi (Castells, Laclau) kuuluu kerrokseen 1 (hard science) — se on yhteiskuntatieteellistä teoriaa, ei spekulatiivista. Populism-analyysi ja sentiment-analyysi ovat työkaluja jotka toimivat kerroksessa 1 mutta voivat tuottaa tuloksia jotka näkyvät kerroksessa 3 (RPG-fiction).

Fiktio ei saa esittää metafysiikkaa tieteena. Poliittinen analyysi ei saa esittää spekulatiivista filosofiaa yhteiskuntatieteenä.

---

## Avoin kysymys

Tomi: haluatko että ajan Vaihe 5 (PHILOSOPHICAL_FRAMEWORK kanonisointi) vai Vaihe 1 (discourse_graph adapter) ensin?