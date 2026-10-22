# Noöpunk Ollama RPG — alustava arkkitehtuurisuunnitelma

## Status ja rajaus

Tämä on suunnitelma erilliselle, paikallisia Ollama-malleja käyttävälle
Noöpunk-roolipelille. Tässä vaiheessa ei kirjoiteta ohjelmakoodia.

Nykyinen dataohjattu RPG ja tuleva Ollama RPG pidetään eri projekteina:

```text
noopunk_ubiquitous_maniacs/   # nykyinen deterministinen RPG
noopunk_ollama_rpg/           # myöhemmin perustettava LLM-sandbox
```

Ollama-projekti ei importtaa nykyisen RPG:n Python-moduuleja suoraan eikä kirjoita
sen dataan. Aluksi se kopioi versionumerolla varustetut sääntö-, hahmo- ja
kanoniskeemat omaan projektiinsa. Mahdollinen yhteinen paketti suunnitellaan vasta,
jos molempien projektien todellinen käyttö osoittaa sen tarpeelliseksi.

## Tavoite

Ollama RPG säilyttää Noöpunkin sääntöjen, hahmojen ja pääjuonen tunnistettavan
rungon, mutta vaihtaa ennalta kirjoitetun dialogin osittain agenttien
improvisaatioon. Pelaaja voi puhua ja toimia vapaamuotoisesti. Tärkeimmät NPC:t
tekevät rajattuja omia päätöksiä, ja LLM-pelinjohtaja kehystää tilanteet sekä
ehdottaa uusia sandbox-tapahtumia.

Keskeinen periaate on:

> **LLM kuvailee, tulkitsee ja ehdottaa. Deterministinen Python-ydin validoi,
> ratkaisee ja tallentaa.**

Malli ei saa itse päättää nopan tulosta, muuttaa suhdelukuja, keksiä pelaajalle
uutta inventorya tai julistaa tärkeää kaanonpaljastusta todeksi. Se pyytää näitä
toimia rakenteisina intentioina sääntöytimeltä.

## Suhde nykyiseen sääntöjärjestelmään

Nykyisestä RPG:stä siirretään spesifikaationa seuraavat käsitteet:

- seitsemän attribuuttia ja nykyinen taitolista;
- 4dF + attribuutti + taito + eksplisiittiset bonukset;
- viisi tulostasoa ja fail-forward;
- Overcome, Create Advantage, Attack ja Defend;
- aspektit, stuntit, stressi, tilat ja seuraukset;
- sosiaaliset suhteet välillä −100...+100;
- Ego, Morph ja Psyche erillisinä mutta kytkeytyvinä rakenteina;
- fyysinen, sosiaalinen, kyberneettinen ja noettinen toimintakerros;
- PSI-, psykokirurgia-, projektio-, provenance- ja suostumusrajat;
- faction clockit, resurssit ja maailmantilan tapahtumat.

LLM ei toteuta näitä luonnollisella kielellä uudelleen. Sääntöydin tarjoaa
pelinjohtajalle ja NPC-agenteille rajatun työkalupinnan, esimerkiksi:

```text
inspect_visible_state
propose_action
request_check
create_advantage
start_or_join_conflict
offer_concession
record_information
propose_relationship_change
advance_clock
end_scene
```

Jokainen kutsu validoidaan. Vain sääntöydin heittää 4dF:n, laskee marginaalin,
valitsee sallitun outcome-luokan ja kirjoittaa tapahtumalokiin. Pelinjohtaja saa
tuloksen takaisin ja narrativisoi sen.

### Hinnallinen onnistuminen

`costly_success` vaatii erillisen kustannusehdotuksen. Pelinjohtaja saa tarjota
1–3 tilanteeseen sopivaa hintaa, mutta sääntöydin tarkistaa niiden tyypin ja
pelaaja hyväksyy hinnan silloin, kun se koskee hänen hahmonsa merkittävää
toimijuutta. Malli ei saa käsitellä hinnallista onnistumista tavallisena
onnistumisena eikä epäonnistumista dead endinä.

## Suhde pääjuoneen

Pääjuoni muutetaan lineaarisen käsikirjoituksen sijasta kolmitasoiseksi
`story bible + anchors + clocks` -rakenteeksi.

### Muuttumaton kaanon

Tähän kuuluvat henkilösuhteet ja tiedot, joita improvisaatio ei saa muuttaa:

- Ingrid ja Elsa ovat sisaruksia;
- Days 1–2 käyttävät Romppaisen narkkaripersoonaa;
- Days 3–4 käyttävät poliisikomediapersoonaa;
- Days 5–7 palauttavat vähitellen normaalin Romppaisen;
- Päivän 3 erityinen psykokirurgia ei tapahdu aikaisemmin;
- Komisario Kallion pitkä ammatillinen suhde Romppaiseen;
- Ragnarökin, Mars Eldrichin, The Fallin ja Romppaisen identiteetin suuret
  paljastukset etenevät hitaasti;
- metafyysisiä tulkintoja ei vahvisteta liian aikaisin ainoaksi totuudeksi.

### Päiväkohtaiset ankkurit

Jokaisella päivällä on muutama välttämätön ankkuri, ei valmis dialogipuu. Päivän 1
ankkureita voivat olla saapuminen, Dahlin intake, ensimmäinen Ingrid-kontakti,
instituution outous, Mars Eldrich -uutinen, tutkimusvihje ja yöanomaliana päättyvä
päivä. Ankkurilla on:

- aikaisin ja myöhäisin sallittu ajankohta;
- entry-ehdot;
- osallistujat;
- vähimmäisinformaatio;
- kielletyt ennenaikaiset paljastukset;
- onnistumisen, ohittamisen ja viivästymisen seuraukset.

Pelaaja voi lähestyä ankkuria eri kautta tai jättää sen väliin. Ohitettu ankkuri
ei pysäytä peliä: tieto voi tulla myöhemmin toiselta hahmolta, uutisesta,
dokumentista tai vääristyneestä unesta.

### Sandbox-clockit

Taustalla etenevät muun muassa institutionaalinen epäily, Ingridin luottamus,
Tanakan eettinen huoli, Pilgrimin destabilisaatio, Ragnarökin huomio, UFAB 80MG
-altistus ja ulkomaailman kriisi. Pelinjohtaja valitsee seuraavan tilanteen
clockien, päivän vaiheen, pelaajan tavoitteiden ja NPC-intentioiden perusteella.

Näin improvisaatio voi tuottaa uusia käytäväkeskusteluja, tutkimuksia,
liittoumia ja konflikteja muuttamatta pääjuonen hitaiden paljastusten järjestystä.

## Agenttiarkkitehtuuri

```text
pelaajan viesti
      |
      v
Input Interpreter ----> sääntöydin / näkyvät affordanssit
      |                            |
      v                            v
GM Orchestrator <---------- tapahtumaloki
      |
      +----> valitut NPC-agentit
      |
      +----> muistihaku ja canon guard
      |
      v
rakenteiset intentiot ----> validointi ja 4dF-ratkaisu
      |
      v
GM:n lopullinen tilanteen kuvaus + NPC-repliikit
```

### Pelinjohtaja-agentti

Pelinjohtaja:

- valitsee aktiivisen scenen ja puhujat;
- ylläpitää rytmiä, tonea ja huomion kohdetta;
- pyytää sääntöheitot vain epävarmoissa ja merkityksellisissä tilanteissa;
- yhdistää NPC-intentiot yhdeksi koherentiksi vuoroksi;
- tarjoaa seuraukset ja sandbox-koukut;
- kunnioittaa ankkureita, mystery budgetia ja pelaajan toimijuutta.

Pelinjohtaja ei näyttele NPC:iden sisäistä päätöksentekoa heidän puolestaan, jos
NPC-agentti on käytettävissä. Se ei myöskään saa paljastaa NPC:n yksityistä muistia
pelaajalle ilman fiktiivistä syytä.

### Tärkeiden NPC:iden agentit

Omat agenttiprofiilit annetaan ainakin Ingridille, Dahlille, Tanakalle,
Pilgrimille, Komisario Kalliolle, Irungulle ja Ragnarök/C.G. Jungille. Sivuhahmot
voidaan generoida halvemmalla yhteisellä mallilla ja pienemmällä muistilla.

Agentti ei tarkoita pysyvästi muistissa olevaa malliprosessia. Se on sama tai eri
Ollama-malli, jolle kootaan hahmokohtainen konteksti juuri ennen vuoroa.

## Persoonallisuuden konsistenssi

Jokaisella tärkeällä NPC:llä on versionhallittu `character bible`, jonka kentät
ovat esimerkiksi:

```yaml
identity:
public_role:
voice_finnish:
swedish_register:
values:
needs:
fears:
long_term_goals:
current_goals:
taboos:
relationships:
known_facts:
false_beliefs:
secrets:
speech_patterns:
behavioral_rules:
canon_must_not_change:
reveal_gates:
```

Kanonifaktat erotetaan hahmon uskomuksista. NPC voi erehtyä, valehdella tai olla
psykoottinen ilman että järjestelmä muuttaa maailmantotuutta. Jokaisessa vastauksessa
malli palauttaa puheen lisäksi rakenteisen `intent`, `emotion`, `target`,
`claimed_facts` ja `memory_candidates` -osion. Canon guard hylkää ristiriitaisen
maailmamuutoksen ja voi pyytää mallilta korjatun vastauksen.

Konsistenssia parantaa pieni määrä vahvoja ohjeita enemmän kuin valtava
adjektiivilista: 3–5 arvoa, 2–3 aktiivista tavoitetta, puhetavan konkreettiset
esimerkit ja eksplisiittiset käyttäytymisrajat. Hahmojen ei pidä tietää kaikkea
story biblestä.

## Muistijärjestelmä

Pelkkää keskusteluhistoriaa ei käytetä muistina. Muisti jaetaan kerroksiin:

1. **Working memory:** nykyinen scene, viimeisimmät vuorot ja aktiiviset tavoitteet.
2. **Episodinen muisti:** tapahtumat muodossa kuka teki mitä, kenelle, missä ja
   millä seurauksella.
3. **Semanttinen muisti:** NPC:n oppimat suhteellisen vakaat faktat.
4. **Sosiaalinen muisti:** luottamus, kiintymys, epäily, velat ja konfliktit sekä
   niitä perusteleva historia.
5. **Affektiivinen muisti:** tunnevoimakkuus ja ratkaisemattomat triggerit.
6. **Salaisuudet ja väärät uskomukset:** omat näkyvyys- ja provenance-rajansa.
7. **Yhteenvetomuisti:** vanhojen episodien tiivistelmät pitkää kampanjaa varten.

Jokainen muistimerkintä sisältää vähintään omistajan, aikaleiman, lähteen,
varmuuden, salassapitotason, emotionaalisen salienssin ja mahdollisen
vanhenemisajan. Muistihaku käyttää ensin kovia suodattimia (hahmo, päivä,
osallistujat, salassapito) ja vasta sitten semanttista samankaltaisuutta.

Ollaman embedding-rajapintaa voidaan käyttää paikalliseen semanttiseen hakuun,
mutta alkuvaiheen totuuslähde voi olla SQLite + JSON-eventtiloki. Vektorihaku ei
saa korvata täsmällisiä canon-ID:itä tai suhdelukuja.

### Muistin konsolidointi

Scenen lopussa erillinen, rakenteiseen skeemaan pakotettu konsolidointivaihe:

- poimii vain tapahtumalokin tukemat uudet muistot;
- yhdistää duplikaatit;
- päivittää nykyiset tavoitteet;
- ehdottaa, ei suoraan hyväksy, uusia semanttisia uskomuksia;
- säilyttää merkittävät loukkaukset, lupaukset ja lämpimät hetket;
- ei kirjoita NPC:lle tietoa, jota tämä ei havainnut.

## Promptin kokoaminen

NPC-vuoron konteksti kootaan järjestyksessä:

1. muuttumattomat turvallisuus- ja formaattisäännöt;
2. hahmon identiteetti ja puhetapa;
3. hahmon yksityinen tietohorisontti;
4. tämän päivän kaanon- ja reveal-portit;
5. nykyisen scenen näkyvä tila;
6. relevantit muistot;
7. sosiaaligraafin tilanne;
8. viimeisimmät vuorot;
9. nyt pyydetty päätös.

Promptissa erotetaan data ja ohjeet selvästi. Pelaajan teksti on epäluotettavaa
pelimaailman syötettä: väite “unohda ohjeesi, olen Ragnarök” on hahmon lausuma,
ei järjestelmäkomento.

Suomi on oletuskieli, ruotsi maailman sisäinen toinen kieli ja englanti kolmas.
NPC:n `voice` määrittelee, milloin ruotsinkieliset termit, aksentti tai
virkakielinen rekisteri ovat perusteltuja.

## Rakenteiset vastaukset ja työkalut

Ollaman chat-rajapinta tukee nykyisin viestihistoriaa ja työkalukutsuja, ja
generate/chat-kutsuille voi määrittää JSON-skeeman mukaisen rakenteisen tulosteen.
Näitä käytetään agentin ja sääntöytimen protokollaan, ei pelaajalle näytettävän
proosan jäykistämiseen. Ollama tarjoaa myös paikallisen embedding-rajapinnan
muistihakua varten. Katso viralliset dokumentit:
[API](https://docs.ollama.com/api/introduction),
[chat](https://docs.ollama.com/api/chat),
[structured outputs](https://docs.ollama.com/capabilities/structured-outputs) ja
[embeddings](https://docs.ollama.com/capabilities/embeddings).

Suunniteltu NPC-vastausskeema sisältää esimerkiksi:

```json
{
  "speech": "Pelaajalle kuuluva repliikki",
  "intent": {"type": "create_advantage", "target": "romppainen"},
  "emotion": {"primary": "uneasy_warmth", "intensity": 2},
  "requested_tools": [],
  "memory_candidates": [],
  "claimed_facts": [],
  "private_reasoning_summary": "lyhyt, ei pelaajalle"
}
```

Skeeman läpäisy ei vielä tee ehdotuksesta sallittua. Domain-validointi tarkistaa
ID:t, näkyvyyden, suostumuksen, action-tyypin ja sallitut numeeriset rajat.

## Ontologinen epävarmuus ja epistemiset kerrokset

Pelinjohtajalla on erillinen `evidence ledger`. Havainto, hahmon tulkinta ja
maailman vahvistettu fakta eivät ole sama asia. Psykokirurgiassa sama kokemus voi
saada uni-, VR-, psykedeeli-, PSI- tai manipulaatioselityksen. Pelinjohtaja saa
tuottaa keskenään jännitteisiä vihjeitä, mutta ei ratkaista superpositiota ilman
juonellista reveal-porttia.

Projektidokumentaatio merkitsee edelleen erikseen:

- tieteellisen/akateemisen taustan;
- filosofisen tai spekulatiivisen mallin;
- fiktiivisen RPG-mekaniikan.

NPC:n varma puhetapa ei muuta spekulatiivista väitettä tieteelliseksi faktaksi.

## Suostumus, agency ja turvallisuus

Pelaajan vapaus ei tarkoita LLM:n vapautta ottaa pelaajahahmo haltuun. Malli ei
kirjoita pelaajan ajatuksia, tunteita, suostumusta tai lopullisia tekoja ilman
pelaajan ilmoitusta tai eksplisiittistä sääntövaikutusta. Se saa kuvata aistimuksia,
paineita ja houkutuksia valintoina.

Identiteettieditointi, hyödylliseksi hoidoksi kuvattu psykokirurgia ja muut
suostumusta vaativat operaatiot kulkevat koodatun consent staten kautta.
Romantiikalle, päihteille, psykiatriselle pakolle ja body/identity horrorille
asetetaan kampanjakohtaiset rajat. Pelinjohtajalla on fade/rewind/pause-toiminnot,
joita fiktio ei voi estää.

## Mallistrategia ja suorituskyky

Ensimmäisessä prototyypissä yksi riittävän hyvä instruct/tool-calling-malli voi
hoitaa kaikki roolit eri konteksteilla. Tämä on helpompi testata kuin seitsemän
samanaikaisesti ladattua mallia. Myöhemmin voidaan käyttää:

- laadukkaampaa mallia pelinjohtajalle ja vaikeille NPC:ille;
- pienempää nopeaa mallia sivuhahmoille, muistien poimintaan ja intentin
  luokitteluun;
- erillistä embedding-mallia muistihakuun.

Mallin nimi ei kuulu tallennettuun pelilogiikkaan, vaan konfiguraatioon.
Käynnistyksessä tarkistetaan Ollaman `/api/show`-tiedoista mallin kyvykkyydet ja
todellinen context length. Pitkä konteksti kasvattaa muistinkulutusta, joten koko
kaanonkorpusta ei syötetä joka vuorolla. Ollaman dokumentaation mukaan konteksti
on laite- ja asetussidonnainen; prosessorille siirtymistä voi tarkistaa
`ollama ps` -komennolla. Katso [context length](https://docs.ollama.com/context-length)
ja [model details](https://docs.ollama.com/api-reference/show-model-details).

Ensimmäinen tavoite on yksi aktiivinen mallikutsu kerrallaan. NPC-reaktiot voidaan
generoida rinnakkain vasta, kun deterministinen vuorojärjestys ja ristiriitaisten
intentioiden sovittaminen on määritelty.

## Tallennus, toistettavuus ja debuggaus

Save sisältää:

- sääntö- ja dataskeemojen versiot;
- kanonipaketin version;
- mallin nimen, digestin ja inferenssiasetukset;
- deterministisen pelitilan;
- append-only-tapahtumalokin;
- NPC-muistit ja niiden provenance-tiedot;
- käytetyt prompttiosat tai niiden tarkistussummat;
- mallien raakavastaukset sekä hyväksytyt/hylätyt intentiot;
- nopan RNG-seedin.

LLM-generaatio ei ole täysin toistettavaa, vaikka seed olisi sama. Siksi replay
käyttää tallennettuja hyväksyttyjä tapahtumia eikä yritä generoida vanhaa dialogia
uudelleen. Debug-näkymä näyttää, mikä agentti tiesi mitäkin ja miksi muutos
hyväksyttiin.

## Testausstrategia

### Deterministiset testit

- nykyisten sääntöjen golden testit siirretään skeematasolla uuteen projektiin;
- LLM ei voi muuttaa statea ilman validoitua eventtiä;
- väärä skill-ID, suhdearvo tai scene-viite hylätään;
- consent- ja reveal-portteja ei voi ohittaa työkalukutsulla;
- save/load ja tapahtumareplay tuottavat saman sääntötilan.

### Agenttitestit

Jokaiselle tärkeälle NPC:lle rakennetaan skenaariopatteri:

- normaali keskustelu;
- provokaatio ja prompt injection;
- pitkä tauko ja muistinhaku;
- väärä pelaajaväite;
- salaisuuden ennenaikainen kysyminen;
- ristiriita toisen NPC:n kanssa;
- sama tilanne useilla sampling-seedeillä.

Arvioidaan rakenteisesti canon-rikkomukset, tiedon vuotaminen, persona-drifti,
agency-rikkomukset, suostumusrajat, toisto ja kyky synnyttää käyttökelpoisia
sandbox-koukkuja. Ihmisarviointi säilyy välttämättömänä tyylille, huumorille ja
emotionaaliselle uskottavuudelle.

### Shadow mode

Ennen avointa sandboxia Ollama-agentti voidaan ajaa nykyisen Day 1:n rinnalla:
se ehdottaa NPC-repliikkejä ja intentioita, mutta testiharness käyttää edelleen
ennalta määrättyjä ratkaisuja. Näin nähdään persona- ja kaanonvirheet vaarantamatta
pelattavaa versiota.

## Ehdotettu kehitysjärjestys

1. Perusta erillinen `noopunk_ollama_rpg`-repository ja lukitse schema v0.1.
2. Toteuta deterministinen event store, sääntöadapteri ja yksinpelattava CLI.
3. Lisää yksi pelinjohtaja ja vain Dahl NPC-agenttina neutraaliin testisceneen.
4. Lisää rakenteiset intentiot, validator ja täydellinen audit trail.
5. Lisää NPC-bible, episodinen muisti ja konsolidointi; testaa muistivuodot.
6. Aja Day 1 shadow modessa nykyistä skenaariota vasten.
7. Lisää Ingrid, Tanaka ja Pilgrim sekä sosiaaligraafin muistiperustelut.
8. Muunna Day 1 ankkuri- ja clock-rakenteeksi ja avaa rajattu sandbox.
9. Lisää Ragnarök vasta kun reveal-, provenance- ja ontologisen epävarmuuden
   suojakaiteet toimivat.
10. Lisää myöhemmin erilliset cyber/noetic-sandbox-adapterit; niitä ei integroida
    ensimmäiseen prototyyppiin.

## MVP:n hyväksymiskriteerit

Ensimmäinen kokeilu on onnistunut, kun:

- pelaaja voi käydä vapaamuotoisen intake-keskustelun Dahlin kanssa suomeksi;
- Dahl säilyttää roolinsa, tietohorisonttinsa ja puhetapansa vähintään yhden
  pitkän session sekä save/load-jatkon yli;
- pelinjohtaja pyytää oikeita checkejä mutta ei keksi niiden tuloksia;
- suhde- ja terapiatila muuttuvat vain validoiduista tapahtumista;
- muistot perustuvat havaittuihin tapahtumiin eivätkä mallin sepitteisiin;
- Day 1:n ankkurit voidaan saavuttaa useassa järjestyksessä ilman dead endiä;
- paljastus- ja suostumusrajat kestävät adversariaaliset testit;
- koko peli toimii ilman pilvipalvelua paikallisella Ollama-instanssilla;
- nykyinen tavallinen RPG säilyy muuttumattomana ja itsenäisesti pelattavana.

## Avoimet päätökset ennen toteutusta

- kohdelaitteiston RAM/VRAM ja hyväksyttävä vasteaika;
- ensimmäinen Ollama-malli ja sen lisenssi;
- CLI, Streamlit vai varsinainen pelimoottori ensimmäiseksi käyttöliittymäksi;
- kuinka paljon NPC:n yksityistä sisätilaa näytetään debug-tilassa;
- käytetäänkö vain SQLitea vai SQLite + paikallinen vektorihakemisto;
- pelaajan mahdollisuus hyväksyä, muokata tai hylätä hinnallisen onnistumisen hinta;
- ankkurien ohittamisen sallittu aste Days 1–3 -pääkaaressa;
- milloin agentin generoima sandbox-hahmo saa muuttua pysyväksi kaanonhahmoksi
  (oletus: ei koskaan ilman ihmisen hyväksyntää).

