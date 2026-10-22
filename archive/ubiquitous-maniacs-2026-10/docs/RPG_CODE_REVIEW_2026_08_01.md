# RPG code review ja regressiotestaus 2026-08-01

## Laajuus

Katselmointi kohdistui nykyiseen dataohjattuun `src/rpg`-moduuliin, Streamlit-renderöintiin, `data/rpg/scenarios/day_1.json`-skenaarioon sekä RPG- ja Day 1 -testeihin. Sosiaali- ja hakkerointidemoja ei integroitu RPG:hen.

## Lähtötila

- Koko testisarja: **144 testiä läpi**.
- Python-moduulit kääntyivät `compileall`-tarkistuksessa.
- Happy path ja valmiiksi testattu vaihtoehtopolku saavuttivat `DAY_2_NOT_IMPLEMENTED`-päätepisteen.

Testien vihreä tila peitti yhden käyttäjälle näkyvän restart-vian sekä kaksi data-/dialogirajan heikkoutta.

## Löydökset ja korjaukset

### P1: Day 1:n restart jätti session kulutetuksi

`DAY_2_NOT_IMPLEMENTED` tarjosi `restart`-interaktion, jonka outcome siirtyi `d1_arrival`-sceneen. Se ei kuitenkaan tyhjentänyt `completed_interactions`-, flag-, clue- tai relationship-tilaa. Pelaaja palasi alkuun, mutta jo suoritetut ei-toistettavat valinnat pysyivät estettyinä.

Korjaus:

- `Outcome` sai yleiskäyttöisen `reset_session`-kentän;
- `RPGSession` rakentaa resetissä uuden puhtaan `RPGState`-tilan;
- vanha tapahtumahistoria tyhjennetään ja tilalle syntyy `session_restarted`;
- Day 1:n restart käyttää kenttää dataohjatusti;
- regressiotesti suorittaa koko päivän, käynnistää restartin ja varmistaa alkutilan sekä avautuneet valinnat.

### P2: Tyhjä dialogue choice -lista vuoti scenen kaikki interaktiot

Moottori rajasi interaktiot dialogin valintoihin vain, jos `choices` oli ei-tyhjä. Dialogisolmu, jonka oli tarkoitus sulkea keskustelu, paljasti siksi kaikki scenen interaktiot.

Korjaus:

- aktiivinen dialogisolmu rajaa valinnat aina;
- tyhjä `choices` tarkoittaa aidosti nollaa dialogitoimintoa;
- regressiotesti varmistaa, ettei piilotettu interaktio vuoda näkyviin.

### P2: Virheellinen event-data kaatui vasta pelin aikana

Loader hyväksyi eventit sellaisinaan. Puuttuva `type`, ei-objektimuotoinen payload tai virheellinen relationship delta saattoi aiheuttaa poikkeuksen vasta sen jälkeen, kun outcome oli jo osittain muuttanut session tilaa.

Korjaus:

- eventin on oltava objekti;
- `type` on pakollinen ei-tyhjä merkkijono;
- `payload` on objekti;
- `relationship_change_requested` vaatii ei-tyhjän kohteen ja aidon integer-deltan, ei boolean-arvoa;
- regressiotesti varmistaa fail-fast-käytöksen skenaariota ladattaessa.

## Arkkitehtuurihavainnot

Hyvää:

- engine ei sisällä Day 1 -hahmo- tai juonikohtaisia haaroja;
- JSON-loader validoi viitteet ennen pelin käynnistämistä;
- checkit fail-forwardaavat ja outcome-fallbackit ovat eksplisiittiset;
- RPG:n relationship-tila ei suoraan mutatoi autonomista NetworkX-simulaatiota;
- UI pysyy ohuena `RPGSession`-rajapinnan päällä;
- Day 1:llä on happy path-, failure path-, state persistence- ja transition-testit.

Jatkokehityskohteet, joita ei tässä refaktoroitu:

- `Scene.entry_flags`, `Scene.exit_flags` ja `RPGState.scene_flags` ovat vielä käyttämättömiä; niiden semantiikka pitää määritellä ennen käyttöönottoa eikä arvata moottorissa.
- Käyttöliittymä ei vielä tarjoa save/load-persistenssiä prosessien välillä.
- Kaksi Day 1 -skenaariota (`day_1.json` ja `day_1_arrival_and_entanglement.json`) palvelevat eri sisältölinjoja. Niitä ei yhdistetty, jotta nykyisiä kanoni- ja testirajoja ei rikota, mutta niiden roolit kannattaa nimetä dokumentaatiossa vielä selvemmin.
- Streamlit-UI:n automaattista selaintestausta ei ole; ydinmoottori testataan ilman Streamlitiä.

## Verifiointi

Korjausten hyväksymiskriteerit:

- koko Day 1 on pelattavissa loppuun;
- cooperative ja failure/alternate reitit toimivat;
- therapy-, clue- ja relationship-tila säilyy normaalin päivän aikana;
- restart tyhjentää nimenomaan edellisen pelikerran tilan;
- rikkinäinen event-data hylätään loaderissa;
- suljettu dialogisolmu ei paljasta toimintoja;
- koko projektin testisarja ja `compileall` ovat puhtaita.

## Sääntökirjan ja koodin ristiintarkistus

Myöhemmässä saman päivän katselmoinnissa `RULEBOOK.md` verrattiin suoraan
toiminto-, konflikti-, hahmolataus- ja sosiaaligraafitoteutuksiin. Korjaukset:

- suhdearvon muutosviesti kertoo nyt toteutuneen, clampatun deltan; esimerkiksi
  99 + 5 tuottaa arvon 100 ja graafiefektin +1;
- Create Advantage -aspektia voi soveltaa vain onnistumisesta tai hinnallisesta
  onnistumisesta, ei epäonnistumisen mukana kulkevana payloadina;
- konflikti hyväksyy hyökkäysvaihdossa vain eksplisiittisen Attack–Defend-parin;
- seuraus vähentää 2/4/6 shiftiä saman exchange-operaation sisällä ennen stressiä;
- tuntematon attribuutti tai taito hylätään heti, eikä kirjoitusvirhe muutu
  huomaamatta arvoksi +0;
- hahmolataus validoi attribuuttien ja taitojen sallitun 0...+4-alueen;
- vanha neutraali demo migroitiin nimistöstä `Perceive`/`Persuade` nykyisiin
  kanonisiin taitoihin `Notice`/`Rapport`.

Ristiintarkistuksen jälkeen koko testisarja sisältää **156 läpäistyä testiä**.
Uudet regressiot kattavat clampatun graafiefektin, aspektin onnistumisrajan,
Attack/Defend-tyypityksen, seurauksen absorboinnin, virheelliset sääntötunnisteet
sekä hahmo- ja skenaariodatan fail-fast-validoinnin.
