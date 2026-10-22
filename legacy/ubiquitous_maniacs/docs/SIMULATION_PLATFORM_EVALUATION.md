# Simulaatioalustojen arviointi ja käyttösuunnitelma

Päivitetty tutkimustulosten perusteella 2026-08-12.

---

## Arvioidut alustat

### 1. Y-Not Social (YSocial)

- **Mikä:** Avoimen lähdekoodin some-simulaattori — "digital twin" mikroblogging-alustasta (Twitter/Reddit). Agentit julkaisevat, tykkäävät, jakavat ja keskustelevat.
- **Arkkitehtuuri:** Client-server: YServer (Flask + SQLite/PostgreSQL, Python) + YSocial (JS-frontend) + YClient (Python-asiakas). 12 repoa GitHub-organisaatiossa YSocialTwin. Upotettu Jupyter Lab analyysia varten.
- **Agenttimalli:** Täysin LLM-pohjainen. Jokainen agentti käyttää LLM:ää. Tukee Ollamaa, vLLM:ää, kaikkia OpenAI-yhteensopivia backendeja. Ei tue ei-LLM-laskennallisia agentteja.
- **Sosiaalinen verkko:** Some-julkaisut, seuraajaverkostot, 10+ suosittelualgoritmia (CommonNeighbors, Jaccard, AdamicAdar, PreferentialAttachment). RSS-uutissyötteet. Äänestysmoduuli poliittiseen debattiin.
- **Interoperabiliteetti:** Python-pohjainen. ySights-analyysikirjasto. Upotettu Jupyter SQL-kyselyillä. Ei natiivia Mesa/NetworkX/PySD-integraatiota, mutta Python-ekosysteemi tekee ulkoisen integraation mahdolliseksi. Plugin-järjestelmä.
- **Lisenssi:** GPL-3.0 (kaikki repot)
- **Kypsyys:** Aktiivisesti ylläpidetty, akateeminen tiimi (Rossetti, Stella, Cazabet), arXiv-julkaisu. Osa SoBigData++ EU-infrastruktuuria.
- **Rajoitukset:**
  - Jokainen agentti vaatii LLM-kutsun — kallis skaalassa
  - GPL-3.0 rajoittaa kaupallista käyttöä
  - Ei Mesa/NetworkX/PySD-integraatiota
  - Tiukasti sidottu mikroblogging-metaforaan
- **Sopivuus LaclauGPT:** Matala — some-simulaatio ei suoraan palvele Castells/Laclau-teoreettista kehystä. Suosittelualgoritmit ovat mielenkiintoisia mutta liian some-keskeisiä.
- **Sopivuus Noöpunk:** Matala — some-simulaatio on liian pinnallinen. Mutta: Ollama-tuki ja plugin-järjestelmä tekevät siitä hyödyllisen inspiraation jos Noöpunkissa joskus simuloidaan some-julkisuutta (Disclosuren jälkeinen mediaskenaario).

### 2. OASIS (camel-ai/oasis)

- **Mikä:** Skaalautuva some-simulaattori — jopa 1 miljoonaa LLM-agenttia Twitter/Reddit-ympäristöissä. Infohajo, ryhmäpolarisaatio, laumakäytös.
- **Arkkitehtuuri:** Python, CAMEL-AI-kehyksen päällä. PyPI: `camel-oasis` v0.2.5. Poetry-dependenssien hallinta. SQLite-tietokanta. Async-arkkitehtuuri (asyncio). PettingZoo-tyyppinen env-rajapinta.
- **Agenttimalli:** Täysin LLM-pohjainen. 23 toimintoa (like, comment, follow, mute, repost, report, group chat jne.). Per-agentti mallin kustomointi. ManualAction skriptatulle käytökselle. Ei tue ei-LLM-laskennallisia agentteja.
- **Sosiaalinen verkko:** Twitter/Reddit-mallit. Dynaamiset sosiaaliset verkostot. Twhin-Bert-suosittelu OpenAI Embeddingeillä. Aktivointitodennäköisyys per aika-askel.
- **Interoperabiliteetti:** Python, PyPI-asennettava. PettingZoo-rajapinta (RL-standardi). HuggingFace-datasetit. Ei Mesa/NetworkX/PySD-integraatiota. Async-arkkitehtuuri hankaloittaa synkronisen Mesan kanssa yhdistämistä.
- **Lisenssi:** Apache-2.0
- **Kypsyys:** Erittäin aktiivinen. 5k tähteä, 618 forkkausta. Viimeisin commit 5 päivää sitten. 30 haaraa. arXiv-julkaisu. Vahva yhteisö (Discord, WeChat, Reddit).
- **Rajoitukset:**
  - Jokainen agentti vaatii LLM-kutsun — 100 agenttia × 1 askel = ~352k tokenia
  - 1M agenttia olisi äärimmäisen kallis
  - Ei Mesa/NetworkX/PySD-integraatiota
  - Async vs. Mesa-synkroninen — arkkitehtuuriristiriita
  - Vain Twitter/Reddit-metafora
- **Sopivuus LaclauGPT:** Keskivaikea — skaalausmahdollisuus on kiinnostava suurten väestöjen simulaatioon, mutta LLM-kustannukset tekevät siitä epäkäytännöllisen ilman hybridiratkaisua.
- **Sopivuus Noöpunk:** Matala — Noöpunk tarvitsee mikroskaalaa (6-16 agenttia), ei miljoonia. PettingZoo-rajapinta on kuitenkin hyvä inspiraatio ja mahdollinen yhteensopivuuspiste.

### 3. MiroFish (mirofish.my)

- **Mikä:** Suljettu kaupallinen SaaS — "Upload Any Report. Simulate The Future." Lataa raportti → generoi ontologian → rakentaa graafin → ajaa multi-agent simulaation → tuottaa ennusteraportin.
- **Arkkitehtuuri:** Next.js-websovellus. Cloud-hostattu SaaS. Frontend-julkista koodia, backend omistusoikeudellinen. Väittää "1M+ rinnakkaista agenttia".
- **Agenttimalli:** LLM-pohjainen multi-agent. "ReportAgent" haastatteluihin. Yksityiskohtia ei ole julkaistu.
- **Sosiaalinen verkko:** Twitter + Reddit -kanavat. "Living relationship graph" actoreineen, jännitteineen, muistirakenteineen.
- **Interoperabiliteetti:** Ei mitään. Ei julkista APIa, ei SDK:ta, ei Python-kirjastoa, ei avointa koodia. Syöte: tiedoston lataus (PDF/MD/TXT). Tuloste: raportti web-UI:ssa.
- **Lisenssi:** Omistusoikeudellinen, suljettu lähdekoodi
- **Kypsyys:** V0.1 preview-vaiheessa. Ei akateemista validointia.
- **Rajoitukset:**
  - Suljettu, ei interoperabiliteettia
  - V0.1 — todella varhainen
  - Data poistuu ympäristöstä
  - Ei ohjausta agenttiarkkitehtuuriin
  - Ei voi integroida Mesaan/NetworkX/PySD
- **Sopivuus LaclauGPT:** Ei sopiva — ei ohjelmistollista pääsyä
- **Sopivuus Noöpunk:** Ei sopiva — ei peli-integraatiota, ei avointa koodia

### 4. Concordia (google-deepmind/concordia)

- **Mikä:** Python-kirjasto generatiivista sosiaalista simulaatiota varten. Tabletop RPG -metafora: Game Master (GM) simuloijaa ympäristöä, agentit kuvaavat toimiaan luonnollisella kielellä.
- **Arkkitehtuuri:** Python (98.6%). PyPI: `gdm-concordia` v2.4.0, 28 julkaisua. Modulaarinen: Entities → Components → Engine. Prefab-agentit/GM-reseptit. Komponentit: muisti, päättelyketjut, sensorimoduulit. LLM-promptinhallinta.
- **Agenttimalli:** LLM-pohjaiset generatiiviset agentit. Agentit kuvaavat toimia luonnollisella kielellä, GM resolvoi (plausibiliteettitarkistus, lopputulos). Komponentit modulaarisia — voit kustomoida muistijärjestelmät, päättelyketjut. March & Olsen (2011) "logic of appropriateness" -päättely esimerkkinä. Vaatii LLM API:n kaikille entiteeteille mukaan lukien GM. Ei sisäänrakennettua ei-LLM-tilaa, mutta komponenttiarkkitehtuuri on tarpeeksi joustava että voisi teoriassa kirjoittaa sääntöpohjaisen komponentin.
- **Sosiaalinen verkko:** Ei some-simulaattori vaan yleiskäyttöinen sosiaalinen simulaatiomoottori. Tukee fyysisiä, sosiaalisia, digitaalisia ympäristöjä. GM medioi kaikki interaktiot. Vuoropohjainen simulaatioloopki. Ei sisäänrakennettua sosiaalisen verkon topologiaa tai suosittelujärjestelmää — nämä rakennetaan komponenteiksi.
- **Interoperabiliteetti:** Python-kirjasto, `pip install gdm-concordia`. Puhtaasti importoitava. Ei Mesa/NetworkX/PySD-integraatiota. Mutta arkkitehtuuri on kirjastomaisin neljästä — suunniteltu tuotavaksi ja laajennettavaksi, ei ajettavaksi erillisenä sovelluksena. Voisi teoriassa kääriä Mesa-scheduleriin tai yhdistää NetworkX-topologiaan. "Bring your own LLM" — mikä tahansa LLM API + mikä tahansa embedder.
- **Lisenssi:** Apache-2.0
- **Kypsyys:** Erittäin aktiivinen. 1.6k tähteä, 354 forkkausta, 1322 committia, 43 kontribuuttoria. Viimeisin commit viikko sitten. 28 julkaisua. Google DeepMindin tuki. arXiv-julkaisut + design pattern -paperi. YouTube-tutoriaali.
- **Rajoitukset:**
  - Fundamentaalisti LLM-riippuvainen — GM ja kaikki agentit vaativat LLM-kutsun joka vuorolla
  - Ei sosiaalisen verkon rakennetta sisäänrakennettuna
  - Ei Mesa/NetworkX/PySD-integraatiota
  - GM-medioitu arkkitehtuuri tekee siitä kalliin skaalassa
  - Suunniteltu pienelle skaalalle (muutama agentti yksityiskohtaisissa skenaarioissa)
  - "Not an officially supported Google product"
- **Sopivuus LaclauGPT:** Korkea konseptuaalisesti — komponenttiarkkitehtuuri, muistijärjestelmät, päättelymallit ovat inspiraatiolähde. Mutta käytännössä LLM-riippuvuus tekee siitä liian kalliin LaclauGPT:n laskennalliseen ytimeen.
- **Sopivuus Noöpunk:** Korkea konseptuaalisesti — Game Master = RPG-pelimoottorin ohjaaja, Entity-Component = Noöpunkin ECS, muistijärjestelmät = NPC-muistit. Mutta käytännössä sama LLM-kustannusongelma.

---

## Keskeinen löydös

**Yksikään neljästä alustasta ei tue natiivisti sekaisin LLM- ja laskennallisia agentteja.** Kaikki ovat LLM-first-arkkitehtuureja. Hybridiratkaisua (Mesa-ydin + muutama Ollama-agentti) täytyy rakentaa itse.

| Ominaisuus | YSocial | OASIS | MiroFish | Concordia |
|---|---|---|---|---|
| Avoin lähdekoodi | GPL-3.0 | Apache-2.0 | Ei | Apache-2.0 |
| Python | Kyllä | Kyllä | Ei | Kyllä |
| PyPI | Ei | Kyllä | Ei | Kyllä |
| LLM-agentit | Kaikki | Kaikki | Kaikki | Kaikki + GM |
| Ei-LLM agentit | Ei | Ei | Ei | Ei (teoriassa) |
| Mesa-integraatio | Ei | Ei | Ei | Ei |
| NetworkX | Ei | Ei | Ei | Ei |
| PySD | Ei | Ei | Ei | Ei |
| Ollama-tuki | Kyllä | Kyllä (OpenAI-compat) | Ei | Kyllä |
| Skaala | Keskisuuri | 1M agenttia | 1M (väite) | Pieni |
| Kypsyys | Aktiivinen, akateeminen | Erittäin aktiivinen, 5k★ | V0.1 SaaS | Erittäin aktiivinen, DeepMind |

---

## LaclauGPT-suunnitelma (vakava yhteiskuntatieteellinen simulaatio)

### Periaatteet
1. **Hierarkkinen agenttiarkkitehtuuri:** 90% agenteista on Mesa/PySD-laskennallisia. Vain 3-5 "avainagenttia" käyttää Ollamaa.
2. **NetworkX-ydin:** Kaikki verkostot ovat NetworkX-graafeja.
3. **Episteeminen palomuuri:** Spekulatiiviset kerrokset (CAN, PSI) ovat erillään empiirisestä ytimestä.
4. **Ei riippuvuutta yhteenkään arvioituun alustaan:** Mesa + NetworkX + PySD ovat ydin. Concordian komponenttiarkkitehtuuri on inspiraatio, ei riippuvuus.

### Arkkitehtuuri

```
Layer 1: Laskennallinen ydin (Mesa + NetworkX + PySD)
├── Mesa AgentBase: agentit joilla on tila, säännöt, vuoro
│   ├── ComputationalAgent: mood, goals, relationships (laskennallinen)
│   └── LLMAgentAdapter: kääriä Ollama-kutsut Mesa-agentiksi
├── NetworkX Graph: sosiaalinen verkko (trust, authority, ideological alignment)
├── PySD: System Dynamics -mallit instituutioille, taloudelle, diskurssille
└── DataCollector: Mesa-tietojen keruu analyysiä varten

Layer 2: Diskurssianalyysi (LaclauGPT:n nykyiset työkalut)
├── discourse_adapter.py: Social graph → Castells/Laclau -mallit (jo olemassa)
├── populism_analysis.py: Ollama-promptit (vain tarvittaessa)
├── sentiment.py: XLM-R sentiment (vain tarvittaessa)
└── classifier.py: Zero-shot scene-typing (vain tarvittaessa)

Layer 3: LLM-agentit (rajoitettu määrä, Ollama)
├── 3-5 avainagenttia: Romppainen, Ingrid, Pilgrim, Tanaka, Ragnarök
├── Ollama-integraatio: vain näillä agenteilla on LLM-kutsu
├── Muisti ja persoonallisuus: dataohjattu, ei LLM-generoitu
└── Kuva: LLM tuottaa dialogin, mutta tilanmuutos on laskennallinen

Layer 4: Inspiraatiolähteet (ei riippuvuuksia)
├── Concordia: komponenttiarkkitehtuurin malli, GM-konsepti
├── OASIS: PettingZoo-rajapintamalli, skaalausstrategiat
└── YSocial: suosittelualgoritmit, some-simulaation metafora
```

### Vaiheet

**Vaihe 1: Mesa-ydin (korkea prioriteetti)**
- Implementoi `src/sim/mesa_core/` — Mesa-pohjainen simulaatioydin
- `ComputationalAgent`: Mesa-agentti jolla on Character-tila, säännöt, vuoro
- `LLMAgentAdapter`: Mesa-agentti joka kutsuu Ollamaa vain jos activate_llm=True
- NetworkX-graafi synkronoidaan `MultiDimensionalSocialGraph`:n kanssa
- DataCollector: kerää trust/authority/ideological alignment -aikasarjat
- Tämä korvaa nykyisen `src/sim/social/` demo-tason toteutuksen

**Vaihe 2: Diskurssikerros (keskitaso)**
- `src/sim/discourse/` — LaclauGPT:n diskurssianalyysin integrointi
- `discourse_adapter.py` (jo olemassa) tuottaa Castells/Laclau-malleja
- PySD-mallit: diskurssin leviäminen, hegemonisten ketjujen muodostuminen
- Ollamaa käytetään vain kun tutkija pyytää syvää tekstianalyysia

**Vaihe 3: LLM-agentit (matala prioriteetti, vain jos tarvitaan)**
- `src/sim/llm_agents/` — rajoitettu määrä Ollama-agentteja
- Vain 3-5 avainhahmoa käyttää LLM:ää
- LLM tuottaa: dialogin, sisäisen monologin, tulkinnan
- LLM ei tuota: tilanmuutosta, suhdearvoja, päätöksiä — nämä ovat laskennallisia
- Concordian komponenttimallia lainataen: muisti, päättelyketju, sensorimoduuli

**Vaihe 4: Skaalauskokeilu (tutkimusvaihe)**
- OASIS:n PettingZoo-rajapinnan kokeilu taustasimulaatioon
- YSocial:n suosittelualgoritmien kokeilu some-simulaatioon
- Mutta: ei riippuvuutta näihin — vain inspiraatio ja valinnainen lyykky

---

## Noöpunk-suunnitelma (pelillistetty RPG-versio)

### Periaatteet
1. **Peli on simulaatio ja simulaatio on peli:** pelaaja on yksi agentti simulaatiossa
2. **RPG-säännöt ovat simulaatiosääntöjä:** Fate Core 4dF on tilastollinen resoluutio
3. **Graafit ovat pelimekaniikkaa:** NetworkX-graafien manipulointi on peliä
4. **LLM on NPC-moottori:** vain avain-NPC:illä on LLM-aivot
5. **Concordian GM-konsepti on inspiraatio:** RPG-pelimoottori on jo Concordian "Game Master"

### Arkkitehtuuri

```
Layer 1: RPG-moottori (jo olemassa)
├── src/rpg/engine.py: Fate Core 4dF, skill checks, scenes
├── src/rpg/psi.py: GQ-CAN PSI actions
├── src/rpg/cyber.py: deterritorialized cyber actions (attune/exorcise/shelter)
├── src/rpg/psychosurgery.py: consent-aware therapy
└── src/hacking/layered.py: 4-layer psychotronic hacking

Layer 2: Sosiaalinen simulaatio (laajennettava)
├── src/game/social_graph.py: 6D social graph (jo olemassa)
├── src/game/npc_autonomy.py: deterministic NPC turns (jo olemassa)
├── Mesa-integraatio: NPC-autonomia → Mesa-scheduler
│   ├── ComputationalNPC: Mesa-agentti, sääntöpohjainen
│   ├── LLMNPC: Mesa-agentti, Ollama-kutsu vain valinnaisesti
│   ├── Pelaajan valinnat perturboivat simulaatiota
│   └── Simulaation tulokset näkyvät RPG-skenaarioissa
└── NetworkX: graafi on jaettu tila RPG:n ja simulaation välillä

Layer 3: Pelikone (kehitysvaiheessa)
├── DeadSim: top-down immersive sim (pygame-ce)
│   ├── ECS-arkkitehtuuri (jo olemassa)
│   ├── Combat, stealth, hacking, perception (jo olemassa)
│   └── Integroituu Noöpunkin graafeihin (tulevaisuus)
├── Tabletop RPG rules:
│   ├── Noöpunk RPG Rules v0.1 (jo olemassa docs/)
│   ├── Transhumanity's Fate skills (jo olemassa)
│   └── Tarot Oracle module (jo olemassa)
└── Game engines:
    ├── pygame-ce: jo käytössä DeadSimissä
    ├── Godot: vaihtoehto jos tarvitaan tehokkaampi renderöinti
    └── Peli pysyy Pythonissa (Mesa + pygame-ce + NetworkX)

Layer 4: LLM-NPC:t (rajoitettu)
├── Ragnarök / C.G. Jung: AGI-hahmo, Ollama
├── Pilgrim: tutkija, Ollama
├── Ingrid: potilas, Ollama
├── Muut NPC:t: Mesa-laskennalliset agentit
└── LLM tuottaa dialogin, Mesa tuottaa käytöksen
```

### Vaiheet

**Vaihe 1: Mesa-scheduler NPC-autonomialle (korkea prioriteetti)**
- Korvaa nykyinen `npc_autonomy.py` Mesa-pohjaisella schedulerilla
- `ComputationalNPC`: Mesa-agentti, sääntöpohjainen (mood + goals + relationships → action)
- `LLMNPC`: Mesa-agentti joka kutsuu Ollamaa vain jos LLM aktivoitu
- Pelaajan RPG-valinnat injectoidaan simulaatioon tapahtumina
- Simulaation tulokset näkyvät RPG-tilassa (suhdearvot, mielialat)
- Concordian muistikomponentti-inspiraatio: NPC:illä on muisti joka vaikuttaa päätöksiin

**Vaihe 2: DeadSim-integraatio (keskito)**
- DeadSimin ECS ja Noöpunkin RPG jakavat konseptit (factions, combat, hacking)
- DeadSim on "physical layer" LAYERED_GAMEPLAN_FUTURE.md:n mukaisesti
- Konkreettinen: DeadSim-kartta = Noöpunk-skenaario, DeadSim-entiteetit = RPG-hahmoja
- GraphEffect-silta: DeadSim-tapahtumat → RPG-tila → Social Graph → Mesa

**Vaihe 3: Concordia-inspiraatio (matala prioriteetti)**
- Concordian komponenttiarkkitehtuuri inspiraatioksi:
  - MemoryComponent: NPC:n muistijärjestelmä (jo osittain olemassa npc_memory:ssä)
  - ReasoningChain: "What situation is this? What person am I? What does such a person do?"
  - SensoryModule: mitä NPC havaitsee ympäristöstä
- Mutta: ei Concordia-riippuvuutta — nämä ovat omia komponentteja
- GM-konsepti: RPG-moottori on jo GM — ei tarvetta Concordian LLM-GM:lle

**Vaihe 4: Taustasimulaatio (tutkimusvaihe)**
- OASIS:n PettingZoo-rajapinnan kokeilu:
  - 16 Psyche -asteroidisiirtokunnan koko väestön simulaatio
  - Disclosuren jälkeinen globaali mediareaktio
  - UFAB-turvallisuusjärjestyksen geopolitiikka
- YSocial-suosittelualgoritmit:
  - Jos Noöpunkissa simuloidaan some-julkisuutta
  - Disclosure-uutisten leviäminen some-verkostoissa
- Mutta: nämä ovat taustakerros, eivät pelin ydin

---

## Game engine + Tabletop RPG + Data science -synteesi

### Konsepti: "Simulaatio on peli, peli on simulaatio"

Noöpunkin erikoisuus on että se yhdistää kolme normaalisti erillistä maailmaa:

1. **Tabletop RPG -säännöt** (Fate Core 4dF, Transhumanity's Fate skills)
   → Nämä ovat tilastollisia resoluutiomekaniikkoja
   → 4dF on vain nopanheitto + skill + difficulty — tämä on laskennallinen operaatio
   → Sama matemaattinen rakenne kuin Mesa-agentin päätösviiveissä

2. **Data science / simulaatio** (Mesa, NetworkX, PySD)
   → NPC-autonomia on Mesa-agenttimallinnus
   → Sosiaaliset suhteet ovat NetworkX-graafeja
   → Institutionaalinen dynamiikka on PySD-system-dynamics
   → Concordian komponenttiarkkitehtuuri on inspiraatio muistille ja päättelylle

3. **Game engine** (pygame-ce / DeadSim)
   → Fyysinen ruumiillisuus, tila, liike, näkökenttä
   → ECS-arkkitehtuuri yhteensopiva Concordian Entity-Component-mallin kanssa
   → DeadSimin ECS ja Noöpunkin RPG jakavat GraphEffect-sillan

### Konkreettinen integraatio

```
Pelaaja tekee valinnan RPG:ssä
    ↓
Fate Core 4dF resolusio (tilastollinen)
    ↓
GraphEffect (domain, operation, source, target, key, value)
    ↓
┌─────────────────────────────────────────┐
│ Jaettu tila (yksi canonical state)      │
│                                         │
│ RPG State ←→ Social Graph ←→ DeadSim    │
│     ↕              ↕           ↕        │
│ Mesa Scheduler  NetworkX   pygame-ce    │
│     ↕              ↕           ↕        │
│ NPC Autonomia   Graafimuut.  Fyysinen   │
│ (laskennallinen) (jaettu)     taso      │
└─────────────────────────────────────────┘
    ↓
Seuraukset näkyvät kaikissa kerroksissa:
- RPG: uusi dialogi, suhde muuttuu
- Social graph: trust edge heikkenee
- DeadSim: ovi lukittuu, hälytys soi
- Mesa: NPC-mieliala muuttuu, uusi tavoite
```

### LLM-agenttien rooli

```
Mesa-agentti (90% agenteista)
├── Tila: mood, goals, relationships (laskennallinen)
├── Käytös: sääntöpohjainen, deterministinen
├── Dialogi: valmiista tekstipankista tai mallivalinnasta
├── Muisti: npc_memory (jo olemassa)
└── Esimerkki: Sven-Olof (ei-pelaaja-NPC), vartija, potilas

LLM-agentti (max 5 agenttia)
├── Tila: mood, goals, relationships (laskennallinen, jaettu)
├── Käytös: LLM tuottaa tulkinnan ja dialogin
├── Dialogi: Ollama tuottaa, mutta tilanmuutos on laskennallinen
├── Muisti: dataohjattu, LLM ei keksi faktoja
├── Inspiraatio: Concordian muisti- ja päättelykomponentit
└── Esimerkki: Ragnarök (AGI), Pilgrim, Ingrid, Romppainen
```

Tärkeää: LLM tuottaa vain tekstin ja tulkinnan. Tilanmuutos, suhteet ja päätökset ovat aina laskennallisia. Tämä varmistaa:
- Determinismin (sama syöte → sama tulos)
- Testattavuuden (Mesa-agentit ovat testattavissa ilman LLM:ää)
- Kustannustehokkuuden (vain 3-5 LLM-kutsua per vuoro, ei satoja)

---

## Yhteenveto

| Päätös | Peruste |
|--------|---------|
| Mesa + NetworkX + PySD ydin | Yksikään alusta ei tue hybridiä; Mesa on Python-ABM-standardi |
| Concordia: inspiraatio, ei riippuvuus | Paras arkkitehtuuri mutta LLM-first; komponentit ja GM-konsepti lainataan |
| OASIS: taustasimulaation tutkimus | Skaalausmahdollisuus suurille väestöille, PettingZoo-rajapinta |
| YSocial: some-simulaation inspiraatio | Ollama-tuki, suosittelualgoritmit, mutta GPL-3.0 ja some-sidottu |
| MiroFish: hylätty | Suljettu SaaS, ei interoperabiliteettia |
| LLM vain 3-5 agentille | Kustannustehokkuus, determinismi, testattavuus |
| DeadSim = fyysinen taso | Jo olemassa, ECS-yhteensopiva, pygame-ce |
| Tabletop RPG = simulaatiosäännöt | Fate Core 4dF on tilastollinen resoluutio, ei erillinen peli |