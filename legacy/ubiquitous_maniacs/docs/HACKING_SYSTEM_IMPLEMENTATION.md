# Kyberneettis–psykotronisen hacking-vertikaalin toteutusraportti

## Toteutettu kokonaisuus

RPG-yhteensopiva hacking-demo mallintaa yhden kohteen NetworkX-graafina neljässä
toimintakerroksessa. Simulaatiologiikka on `src/hacking/layered.py`:ssä,
skenaario JSON-datana ja Streamlit vain esityskerroksena.

Vanhaa `HackingSimulation`-kokeilua ei poistettu. Uusi `LayeredHackingSession` on
rinnakkainen API, jotta aiemmat testit ja graph-manipulation-kokeet säilyvät.

## Tiedostot

- `src/hacking/layered.py`: kerrokset, pääsy, resolver, paineet, terminalit ja adapteri;
- `src/hacking/__init__.py`: uusi julkinen API;
- `data/hacking/sleeping_patient.json`: dataohjattu nelikerrosskenaario;
- `hacking_demo.py`: pelattava Streamlit-käyttöliittymä;
- `tests/test_layered_hacking.py`: core- ja integraatioregressiot;
- `RULEBOOK.md`: täydellinen hacking-luku ja läpelattu esimerkki;
- `docs/SIMULATION_DEMOS.md`: ajantasainen moduuli- ja käynnistysohje.

## Arkkitehtuuri

`LayeredHackingSession` vastaanottaa tavallisen RPG:n `Character`-olion.
Toiminnot käyttävät `resolve_action`-funktiota, joten nopat, attribuutit, taidot,
tulostasot ja aspektikutsut eivät muodosta rinnakkaista sääntöjärjestelmää.

Scenario loader rakentaa graafin ja validoi node-ID:t, neljä layer-arvoa,
edge-endpointit ja entry noden. Nodekohtainen `checks` voi vaihtaa attribuutti–skill
-yhdistelmää fiktiivisen position mukaan. Muuten käytetään kerroksen kompaktia
oletusprofiilia.

State-mutaatio tapahtuu vain onnistuneen toiminnon jälkeen. Hinnallinen
onnistuminen etenee ja kasvattaa Alert/Trace-painetta. Psychic-toiminnot voivat
kasvattaa lisäksi Feedbackia ja Instabilitya. Terminaalitila estää myöhemmät
mutaatioyritykset, ja objective-node voidaan exploittaa vain kerran.

## RPG-integraatio

`HackingTransfer` ei omista RPG:tä. Se kerää:

- known information;
- conditionit ja consequencet;
- relationship-muutokset;
- campaign flagit;
- domainien väliset `GraphEffect`-pyynnöt.

`HackingTransfer.apply(state, character)` soveltaa tulokset tavalliseen
`RPGState`- ja `Character`-tilaan. Suhteet clampataan −100...+100 ja toteutunut
delta kirjataan social-graph-efektinä. Tämä mahdollistaa myöhemmän scene-loop
-integraation ilman että hacking-moottori importtaa tai ohjaa `RPGSession`ia.

## Nukkuva potilas

Pelaajan täytyy tunnistaa luvaton prosessi ja vakauttaa potilas. Neljä näkyvää
entryä ovat kliininen pääte, Tanakan luottamus, potilaan hermosto ja potilaan
tietoinen minä. Observe paljastaa piilotetut nodeketjut.

Toteutetut reitit:

- cybernetic-muistipuskuri tunnistaa intrusion;
- psychic dream city ja vieras signaali tunnistavat intrusion vaihtoehtoisesti;
- biological-hermosto, REM-sykli, 80MG-pitoisuus tai lääkeohjain tarjoavat
  vakautusreittejä;
- social-hoitotahto ja Pilgrimin auktoriteetti luovat cross-layer-pääsyä.

Prosessin ontologia jää tarkoituksella auki. Data osoittaa useita proveniensseja,
ei ratkaise malware–Ragnarök–dissosiaatio–NHI-superpositiota.

## Käynnistys

Projektin juuresta:

```bash
streamlit run hacking_demo.py
```

Kaikki testit:

```bash
python -m pytest -q
```

Vain uusi vertikaali:

```bash
python -m pytest -q tests/test_layered_hacking.py
```

## Tunnetut rajat

- Digitaalinen demo käyttää solmukohtaista staattista defense-vaikeutta;
  aktiivista puolustusagenttia ja opposed rollia ei vielä ajeta.
- Tool-malli tukee permission-kuvausta, layer/action-rajausta ja 0...+2-bonusta,
  mutta kuluvia käyttökertoja ei ole.
- Attack tuottaa yhteistä system stressiä; layerkohtaiset consequence-slotit ovat
  myöhempää advanced-sääntöä.
- RPG-siirto on toteutettu ja testattu, mutta Day 1 ei vielä kutsu hacking-demoa.
- UI:lla ei ole selaintestiä. Python-moottorin täydet reitit testataan suoraan.

## Suositeltu seuraava kehitys

1. Lisää scene-event, joka rakentaa hacking-session RPGState-snapshotista.
2. Lisää aktiivinen defense actor ja oikea Attack–Defend-vaihto.
3. Tee inventory-adapteri työkalujen käyttökertoja ja implanttipermissioneja varten.
4. Lisää save/load JSON:lle sekä UI:ssa vahvistettava paluusiirto RPG:hen.
5. Kalibroi vaikeudet useilla hahmoprofiileilla ja satunnaisilla 4dF-ajoilla.

