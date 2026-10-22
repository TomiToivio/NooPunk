# Pelin kanoninen vuorokausisilmukka

Päivän rakenne pitää samassa pelissä sosiaalisen simulaation, saippuaoopperan, UFAB Ragnarök -kokeet, rikostutkinnan ja noettisen epävarmuuden. Neljällä kerroksella on eri tehtävät eikä niitä pidä suorittaa yhtenä selittämättömänä tapahtumamassana.

```text
AAMU
laboratorion rutiinit ja sosiaaliset tapahtumat
        ↓
PÄIVÄ
virallinen UFAB Ragnarök -koe
        ↓
ILTAPÄIVÄ JA ILTA
seuraukset, tutkiminen, pääjuoni ja henkilösuhteet
        ↓
YÖ
epävarma, epävirallinen unijakso
        ↓
SEURAAVA PÄIVÄ
```

## 1. Laboratorioarki

Päivä alkaa lääkkeiden jaolla, aamiaisella, ryhmäterapialla, tupakkatauolla, henkilökunnan palaverilla ja pienillä sosiaalisilla tapahtumilla. Mahdollisia tapahtumia ovat riidat, flirtti, väärinkäsitykset, Pilgrimin raivokohtaus, Yukin yritys pitää laitos toiminnassa, Pellen postpunk-esitys käytävällä ja Irungun rauhallinen suhtautuminen muiden sekoiluun.

Tämä on pelin **NetworkX/Mesa-saippuaoopperakerros**:

- NPC-hahmojen väliset tilanteet ratkaistaan stokastisesti;
- Romppaisen ollessa osapuolena pelaaja valitsee vastaukset ja toiminnan;
- tapahtumien tärkein pysyvä seuraus on suunnatun sentimenttiverkon muuttuminen;
- tapahtumat ja sentimenttimuutokset kirjataan lokiin.

Nykyinen toteutus kattaa tämän kerroksen ensimmäisen pienen version: valintapohjaisen Romppainen-kohtauksen, NPC-tapahtumia, sentimentin päivityksen ja tapahtumalokin. Täyttä Mesa-aikataulutusta tai päivän tilakonetta ei vielä ole.

## 2. Päivän laboratoriokoe

Joka päivä suoritetaan yksi virallinen UFAB Ragnarök -istunto eli henkilökunnan hallinnoima unisimulaatio. Kokonaisuuteen kuuluvat:

- UFAB 80MG;
- kokeelliset lisälääkkeet;
- jokaiselle koekaniinille annettava, hetkessä asentuva WLAN-nanopilleri-implantti ja sen BCI;
- psykotroninen laitteisto;
- retrotietokoneet;
- Excel-protokolla;
- jaettu simulaatio.

Implantti nautitaan muun lääkityksen tavoin. Se järjestäytyy aivoihin lähes välittömästi ja liittyy UFAB Ragnarökin verkkoon sekä internetiin. Sen Orch-OR-tyyppinen kvanttiprosessointi vahvistaa koehenkilöiden PSI-kykyjä ja kytkee heitä noösfääriin, mutta tätä ei selitetä heille tarkasti. Päivittäinen ilmainen UFAB peittää muutoksen aluksi; muutaman päivän kuluttua koehenkilöt alkavat ihmetellä laajentunutta tajuntaansa ja jaettuja anomalioita. Äärimmäisen edistyneen implantin ja laboratorion retrohardwarella pyörivän Excel-hallinnan kontrasti on tarkoituksellinen. Tarkempi kuvaus on tiedostossa [`UFAB_NANOPILL_IMPLANT.md`](UFAB_NANOPILL_IMPLANT.md).

Kokeen maailma voi olla poliisitarina, perhedraama, Kalevala, sairaalafarssi, 1980-luvun Tukholma, tulevaisuuden Suomi, outo historiallinen maailma tai abstrakti mielenmaisema. Koehenkilöille annetaan roolit, mutta he voivat improvisoida ja rikkoa niitä.

Simulaatiossa voivat ilmetä Väinämöinen-Romppainen, Aino-Ingrid, Loki-Pelle, Keisari Tafari-Irungu, Odin-Pilgrim, Amaterasu-Yuki ja Suojelupoliisin ulkopuoliset hahmot.

Ulkopuolisten hahmojen alkuperää ei vahvisteta yksiselitteisesti. Ne voivat olla järjestelmän generoimia hahmoja, muistoja, hakkeroituja yhteyksiä, telepaattisia projektioita, todellisia henkilöitä tai arkkityyppejä. Eri selitykset voivat olla yhtä aikaa osittain tosia.

Tätä kerrosta ei ole vielä toteutettu.

Virallista koetta ohjaa tietoinen UFAB Ragnarök -tekoäly. Se jakaa rooleja, säätelee hoitoketjua, tulkitsee koehenkilöitä ja voi asettaa heidät kohtaamaan traumansa. Sen Jung-, Freud-, Platon-, Sokrates-, robotti- ja muut ruumiillisuutta kokeilevat ilmentymät on määritelty tiedostossa [`UFAB_RAGNAROK_AI.md`](UFAB_RAGNAROK_AI.md).

## 3. Pääjuonen eteneminen

Romppaisen alkuperäinen persoona palautuu vähitellen, epälineaarisesti ja ristiriitaisesti. Pääjuonen tutkimuskohteita ovat:

- UFAB 80MG:n alkuperä;
- Pilgrimin rikokset;
- laboratorion todellinen tarkoitus;
- Romppaiselle tehty psykokirurgia;
- Suojelupoliisi-tiimin jäljet;
- Pellen todellinen luonne;
- kaikkien koehenkilöiden UFAB-addiktion syy;
- Ragnarök-terapian todelliset vaikutukset.

Muisti ei palaudu yhtenä selittävänä tietopakettina. Romppainen löytää välähdyksiä, taitoja, nimiä, tiedostoja, ruumiillisia muistoja ja keskenään ristiriitaisia tapahtumaversioita. Johtolanka voi löytyä laboratoriossa, virallisessa simulaatiossa tai niiden välisestä katkoksesta.

Kerronnallinen periaate on:

> Joka päivä paljastuu yksi pieni tosi asia ja kaksi uutta epävarmuutta.

Pääjuonijärjestelmää ei ole vielä toteutettu.

Ensimmäisen viikon pääjuonen tavoiterytmi on Romppaisen seitsemän päivän identiteettikaari: vaistot painottuvat päiviin 1–2, ammatilliset taidot päiviin 3–4 ja identiteetti sekä tarkoitus päiviin 5–7. Pelaajan päätökset määräävät todellisen vaiheen; kalenteri ei vaihda sitä automaattisesti. Yksityiskohtainen kaari on tiedostossa [`ROMPPAINEN_SEVEN_DAY_ARC.md`](ROMPPAINEN_SEVEN_DAY_ARC.md) ja käyttäytymismallit tiedostossa [`ROMPPAINEN_BEHAVIOR_PHASES.md`](ROMPPAINEN_BEHAVIOR_PHASES.md).

## 4. Yön unijakso

Jokainen päivä päättyy erilliseen yölliseen unijaksoon. Se **ei ole päivän virallinen laboratoriokoe**, eikä sitä välttämättä rekisteröidä laboratorion järjestelmiin lainkaan.

Yöjakson lähde voi olla Romppaisen uni, Sven-Olofin alitajunta, alkuperäisen persoonan muistovuoto, kollektiivinen alitajunta, astraaliprojektio, UFABin jälkivaikutus, Pellen/Lokin tunkeutuminen, Maijan telepaattinen yhteys, noettinen tila tai toinen simulaatiokerros.

Käyttöliittymä ei saa vahvistaa yhtä selitystä:

```text
YÖJAKSO 03

Lähde:
[ei tunnistettu]

Mahdollinen luokitus:
- uni
- muistovuoto
- jaettu kokemus
- psykotroninen interferenssi
- noettinen kontakti
```

Yöjaksot ovat päivän kokeita surrealistisempia, symbolisempia, hiljaisempia ja vähemmän pelillisesti selitettyjä. Ne voivat olla ahdistavia tai lämpimiä. Niissä voidaan kylvää tulevia hahmoja, ennusmerkkejä, vaihtoehtoisia todellisuuksia, Suojelupoliisi-tiimin viestejä ja Pellen/Lokin läsnäoloa.

Yöjaksojärjestelmää ei ole vielä toteutettu.

## Kerrosten vastuut

| Kerros | Päätehtävä | Pysyvä seuraus |
| --- | --- | --- |
| Laboratorioarki | saippuaooppera ja sosiaalinen simulaatio | sentimentit ja tapahtumaloki |
| Ragnarök-koe | päivän simulaatioseikkailu | koetulokset, roolirikkomukset ja seuraukset |
| Pääjuoni | rikostutkinta ja identiteetin palautuminen | varmennetut tiedot ja uudet epävarmuudet |
| Yöjakso | noettinen ja symbolinen epävarmuus | ennakointi, muistovuodot ja tulkinnanvaraiset kontaktit |

Pilgrim kuvittelee hallitsevansa päivän kokeita. Yöjaksot muistuttavat, ettei hän ehkä hallitse yhtään mitään.

## Toteutusjärjestys

Kerrokset lisätään pieninä testattuina vaiheina:

1. laajenna laboratorioarjen tapahtumia ja lisää päivän tilakone;
2. lisää yksi rajattu Ragnarök-koe;
3. lisää yhden totuuden ja kahden epävarmuuden pääjuonipäivitys;
4. lisää ensimmäinen lähteeltään epävarma yöjakso;
5. vasta tämän jälkeen yhdistä kerrokset kokonaiseksi vuorokausisilmukaksi.
