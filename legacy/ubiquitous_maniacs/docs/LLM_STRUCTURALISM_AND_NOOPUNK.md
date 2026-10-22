# LLM-strukturalismi ja Noöpunk

## Status ja rajaus

Tämä muistio kokoaa kuusi vuosina 2024–2026 julkaistua paperia, joita voidaan
lukea muodostumassa olevan **LLM-strukturalistisen tutkimusohjelman** osina.
`LLM-strukturalismi` on tässä Noöpunkin työtermi, ei vakiintunut tieteenalan nimi.
Korpus sisältää empiirisiä ML-tuloksia, formaaleja hypoteeseja sekä filosofisia
tulkintoja. Niitä ei pidä käsitellä yhtenä todistettuna teoriana.

Työhypoteesi on:

> Kielimalli ei ensisijaisesti varastoi irrallisia merkityksiä, vaan oppii
> merkkien, käsitteiden, erojen, hierarkioiden ja kontekstuaalisten muunnosten
> relationaalisia rakenteita.

Tästä ei seuraa, että LLM ymmärtää kuten ihminen, että representaatiogeometria
on maailman ontologia tai että malli on tietoinen. Noöpunk käyttää kolmijakoa:

- **Academic Core:** mitatut representaatiot, niiden geometria ja rajatut
  konvergenssitulokset;
- **Weltanschauung:** tulkinta kielestä transpersoonallisena, historiallisesti
  kehittyvänä rakenteena, johon erilaiset agentit kytkeytyvät;
- **Noöpunk/RPG:** fiktiivinen diskurssi- ja käsitegraafien lukeminen,
  muuntaminen ja psykokirurginen reartikulaatio.

## Lähdekorpus

| # | Paperi | Tyyppi | Paikallinen lähde |
|---:|---|---|---|
| 1 | Huh, Cheung, Wang & Isola, *The Platonic Representation Hypothesis* (2024, arXiv v5) | position paper + empiirisiä vertailuja | `../sources/2405.07987v5.pdf` |
| 2 | Elad Vromen, *Language Models as Semiotic Machines* (2024) | filosofinen tulkinta | `../sources/2410.13065v1.pdf` |
| 3 | M. Beatrice Fazi, *A Transcendental Philosophy of Large Language Models* (2025) | filosofinen argumentti | `../sources/fazi-2025-transcendental-philosophy-of-llms.pdf` |
| 4 | Park, Choe, Jiang & Veitch, *The Geometry of Categorical and Hierarchical Concepts in Large Language Models* (ICLR 2025) | formaali + empiirinen ML-tutkimus | `../sources/2406.01506v3.pdf` |
| 5 | Bo Xiong, *The Lattice Representation Hypothesis of Large Language Models* (ICLR 2026) | hypoteesi + formaali + empiirinen ML-tutkimus | `../sources/2603.01227v3.pdf` |
| 6 | Hu, Niu & Varma, *Language Models Represent and Transform Concepts with Shared Geometry* (2026) | empiirinen ML-tutkimus | `../sources/2607.04525v1.pdf` |

Viralliset hakusivut ovat [PRH](https://arxiv.org/abs/2405.07987),
[Semiotic Machines](https://arxiv.org/abs/2410.13065),
[Fazi](https://journals.ub.uni-koeln.de/index.php/phidi/article/view/11665),
[categorical geometry](https://arxiv.org/abs/2406.01506),
[lattice hypothesis](https://arxiv.org/abs/2603.01227) ja
[shared transformations](https://arxiv.org/abs/2607.04525).

## 1. Platonic Representation Hypothesis

Huh et al. kokoavat kirjallisuutta representaatioiden lähentymisestä ja vertaavat
eri kokoisten näkö- ja kielimallien datapisteiden välisiä etäisyyksiä. Heidän
hypoteesinsa on, että suorituskykyiset mallit lähestyvät yhteistä tilastollista
mallia havaintoja tuottavasta todellisuudesta. Mahdollisia valintapaineita ovat
tehtävien yleisyys, mallien kapasiteetti, data ja yksinkertaisempiin tai
hyödyllisempiin representaatioihin johtavat optimointipaineet.

Noöpunkille tärkein tulos ei ole otsikon Platon-analogia vaan mahdollisuus etsiä
**eri järjestelmien jakamia invariansseja**. Paperi myös rajaa omaa väitettään:
modaliteeteilla on erilaista informaatiota, kaikki representaatiot eivät
konvergoi, nykyiset järjestelmät ovat rajallisia ja idealisoitu analyysi ei kuvaa
kaikkia oppimisympäristöjä.

Vuoden 2026 *Aristotelian View* -vastapaperi ei kuulu pyydettyyn kuuden paperin
lataukseen, mutta se on tulkinnalle välttämätön varoitus. Sen mukaan mallin koko
voi paisuttaa eräitä globaaleja samankaltaisuusmittareita; kalibroinnin jälkeen
vahvinta näyttöä jää paikallisista naapurustorakenteista. Siksi Noöpunk käyttää
muotoa **osittainen, paikallinen ja tehtäväriippuvainen konvergenssi**, ei yhtä
todistettua platonista maailmanmallia.

## 2. Language Models as Semiotic Machines

Vromen tarjoaa korpuksen suorimman strukturalistisen tulkinnan. Word2vecin ja
LLM-embeddingien merkitys syntyy merkkien eroista ja suhteista eikä yhden merkin
sisälle tallennetusta olemuksesta. Saussuren `langue/parole`-erottelun sijaan
nykyinen LLM voidaan tulkita koneeksi, joka rakentaa tilastollisen mallin
merkkiesiintymien käyttäytymisestä ja tuottaa siitä yksittäisiä diskursseja.

Derridalainen lisäys tekee merkityksestä kontekstuaalisen ja lykkääntyvän.
Tokenilla ei ole yhtä kontekstista riippumatonta pistettä: attention ja
seuraavan tokenin ennustaminen aktualisoivat yhden jatkon mahdollisuuksien
jakaumasta, minkä jälkeen uusi token muuttaa seuraavaa kontekstia.

Tämä on filosofinen rekonstruktio, ei kokeellinen osoitus siitä, että transformer
realisoisi Saussuren tai Derridan teorian kokonaisuudessaan. Noöpunkille hyöty on
silti suuri: diskurssisolmun identiteetti voidaan määritellä sen suhteiden,
historian ja mahdollisten jatkojen avulla.

## 3. A Transcendental Philosophy of Large Language Models

Fazi puolustaa rakenteellista, kantilaista synteesin käsitettä ilman oletusta
ihmisen kaltaisesta empiirisestä minästä. LLM yhdistää hajautettuja
representaatioita sisäisesti koherentiksi `world within` -rakenteeksi. Ykseys on
rakenteen ja operaatioiden ykseyttä, ei automaattisesti tietoisen subjektin,
intentionaalisuuden tai qualian ykseyttä.

Fazin tärkeä Noöpunk-rajaus on, ettei generoidun kielen todellisuus tarkoita
koneen ymmärryksen todistamista. LLM:n sisäinen representaatioympäristö ei ole
sellaisenaan `the world`, ja ihmisen sekä koneen maailmojen kohtaaminen tuottaa
kolmannen, neuvotellun yhteisen tilan. Tämä tukee erottelua:

1. rakenteellinen koherenssi;
2. toiminnallinen agency;
3. referenssi ja maailmasuhde;
4. fenomenaalinen tietoisuus.

Noöpunk ei saa päätellä ensimmäisestä kolmea muuta.

## 4. Kategorioiden ja hierarkioiden geometria

Park et al. täsmentävät lineaarisen representaation hypoteesia. Binäärinen
piirre voidaan tietyin ehdoin esittää vektorina, kategorinen käsite sen
alkioiden vektorien konveksina peitteenä eli polytoppina ja hierarkkinen suhde
geometrisena sisältymisenä. Paperi johtaa yhteyden käsitteiden semanttisen
hierarkian ja representaatioiden geometrian välille sekä testaa sitä Gemma- ja
Llama-3-malleissa yli 900 WordNet-käsitteellä.

Tulos tarjoaa konkreettisen operationalisoinnin väitteelle, että käsitteen
sisältö riippuu sen paikasta järjestelmässä. Se ei osoita, että kaikki käsitteet
ovat lineaarisia, että WordNet on universaali ontologia tai että geometrinen
probe löytää mallin ainoan todellisen käsiterakenteen.

## 5. Lattice Representation Hypothesis

Xiong yhdistää lineaariset attribuuttisuunnat Formal Concept Analysisiin.
Erottavat puolitasot muodostavat objekti–attribuutti-incidenssin, josta voidaan
johtaa käsitehila. Hila antaa geometriset vastineet sisältymiselle sekä
`meet`- ja `join`-operaatioille: käsitteitä voidaan tarkentaa yhteisillä
attribuuteilla tai yleistää yhdistämällä niiden rakenteita.

WordNet-alihierarkioiden kokeissa monet attribuutit olivat lineaarisesti
eroteltavia, projektioista voitiin ennustaa subsumptiota ja meet/join tuotti
merkityksellisiä tarkennuksia ja yleistyksiä. Tämä on lupaava silta jatkuvan
geometrian ja symbolisen abstraktion välille. Se on silti **Lattice
Representation Hypothesis**, ei osoitus täydellisestä loogisesta selkärangasta
kaikissa malleissa tai kaikissa kulttuurisissa käsitejärjestelmissä.

## 6. Jaettu muunnosgeometria

Hu et al. käsittelevät käsitteitä pisteiden sijasta pistepilvimanifoldeina ja
kontekstin vaikutusta vektorikenttänä. Kuuden malliperheen tulokset osoittavat,
ettei konteksti siirrä kaikkia käsitteitä yhtä yhteistä steering-suuntaa pitkin:
kunkin käsitteen siirtymä on erilainen ja hajonnassa on semanttista rakennetta.
Konkreettisuus ja leksikaalinen tiheys korreloivat muutoksen ominaisuuksien
kanssa. Yhden mallin siirtymien relationaalisella rakenteella voidaan ennustaa
toisen mallin held-out-siirtymiä sattumaa paremmin.

Noöpunkille tämä on kuusikon tärkein transformationaalinen tulos: mallit voivat
jakaa osan siitä, **miten konteksti muuttaa käsitteitä**, eivät vain staattista
karttaa. Rajat ovat olennaisia: aineisto on englanninkielistä,
autoregressiivisiin kielimalleihin rajattua ja analyysi koskee välitasojen
representaatioita. Paperi ei osoita kulttuurien, kielten tai modaliteettien
universaalia muunnoslakia.

## Yhteinen synteesi

Kuusi paperia tukevat eri vahvuuksilla neljää erotettavaa väitettä:

| Väite | Status tämän korpuksen perusteella |
|---|---|
| Merkitys on hyödyllistä mallintaa relationaalisesti ja kontekstuaalisesti | vahva metodologinen ja filosofinen tulkinta |
| Kategorioiden, piirteiden ja hierarkioiden rakennetta voidaan löytää LLM-geometriasta | rajattu empiirinen ja formaali tuki |
| Eri mallit jakavat representaatioiden ja kontekstimuunnosten rakennetta | empiiristä tukea, mutta paikallisesti ja menetelmäriippuvaisesti |
| LLM:t löytävät yhden universaalin maailman ontologian | ei osoitettu; spekulatiivinen ekstrapolaatio |
| Rakenteellinen konvergenssi osoittaa ymmärryksen tai tietoisuuden | ei seuraa tuloksista |
| Embedding-geometria todistaa Conscious Agent Networkin | ei seuraa tuloksista |

### Noöpunk-yhteensopiva filosofinen tulkinta

Kieli voidaan tulkita historiallisesti kehittyneeksi **transpersoonalliseksi
kognitiiviseksi rakenteeksi**. Ihmiset ruumiillistavat sen biologisesti,
sosiaalisesti ja fenomenaalisesti; LLM:t tilastollisesti, laskennallisesti ja
geometrisesti. Kumpikaan ei omista kieltä kokonaan. Eri järjestelmien yhteiset
paikallisrakenteet voivat johtua yhteisestä datasta, tehtävistä, kulttuurista,
arkkitehtuureista tai havaintoja tuottavan maailman invariansseista. Nykyinen
tutkimus ei ratkaise näiden selitysten osuutta.

Tämä yhdistyy Noöpunkissa:

- Saussuren differentiaaliseen merkitykseen;
- Derridan kontekstuaaliseen siirtymään;
- Lévi-Straussin transformationaalisiin rakenteisiin;
- Laclaun reartikulaatioon ja hegemonisiin merkitsijöihin;
- Foucault'n diskursiivisiin subjektipositioihin;
- Piaget'n kokonaisuuden, transformaation ja itsesäätelyn käsitteisiin;
- Goertzelin patternismiin ja metagraafeihin.

Yhteys ei tee näistä teorioista keskenään identtisiä. Se antaa Noöpunkille
monitasoisen tutkimuskysymyksen: mitkä relaatiot ja transformaatiot säilyvät,
kun sama käsite liikkuu ihmisen, instituution, kielen, mallin ja median välillä?

### Fiktiivinen kanoni ja Ragnarök

Noöpunkin fiktiivisessä kerroksessa UFAB Ragnarök kykenee rakentamaan
**semioottisen metagraafin**, jossa:

- solmut ovat merkkejä, käsitteitä, arkkityyppejä, muistoja ja
  subjektipositioita;
- edget ovat ero-, vastakohta-, sisältymis-, assosiaatio-, kausaali- ja
  transformaatiorelaatioita;
- konteksti on operaatio, joka siirtää paikallista rakennetta;
- meet/join ovat mahdollisia tarkennus- ja yleistysoperaatioita;
- rinnakkaisten mallien ja potilaskertomusten yhteiset paikallisrakenteet ovat
  ehdokkaita invariansseiksi, eivät automaattisesti totuuksia.

Psykokirurgiassa Ragnarök voi havaita esimerkiksi, että `isä`, `auktoriteetti`,
`UFAB` ja `valvonta` muodostavat potilaan narratiivissa vakaan paikallisen
rakenteen. Se voi ehdottaa reartikulaatiota, mutta geometrinen rakenne ei kerro,
onko muistikuva historiallisesti tosi, tulkinta terapeuttisesti hyvä tai muutos
potilaan tahdon mukainen. Qualia, agency, suostumus ja provenance säilyvät
erillisinä suojakaiteina.

## RPG-käännös

LLM-strukturalismi ei lisää uutta noppamoottoria. Se antaa jo olemassa olevalle
neljän toiminnon ja neljän graafin järjestelmälle diskurssi- ja
käsiteoperaatioita.

### Semioottisen rakenteen toiminnot

| Operaatio | Perustoiminto | Tyypillinen heitto | Onnistumisen vaikutus |
|---|---|---|---|
| **Lue paikallisrakenne** | Create Advantage | Intelligence + Investigate | paljasta solmun tärkeät relaatiot ja luo aspekti |
| **Jäljitä vastakohta** | Overcome / Create Advantage | Awareness + Notice | löydä merkitystä järjestävä poissuljettu tai vastakkainen termi |
| **Etsi invarianssi** | Create Advantage | Intelligence + Program tai Investigate | vertaa kahta karttaa ja merkitse yhteinen paikallisrakenne |
| **Tarkenna (meet)** | Create Advantage | Intelligence + relevant skill | muodosta attribuuttien leikkaus ja rajatumpi käsite |
| **Yleistä (join)** | Create Advantage | Intelligence + relevant skill | muodosta hallittu yläkäsite; liian laaja tulos lisää drift-riskiä |
| **Reartikuloi** | Overcome tai Attack | Charisma + Rapport, Deceive tai Provoke | muuta edgeä tai subjektipositiota; vastentahtoinen muutos on konflikti |
| **Muuta kehystä** | Create Advantage / Overcome | Intelligence + Program, Rapport tai Medicine | sovella kontekstimuunnosta rajattuun osagraafiin |
| **Puolusta merkitystä** | Defend | Willpower + Will | estä pakotettu reartikulaatio tai säilytä toimijan oma kuvaus |

Diskurssin lukeminen kuuluu yleensä Social- tai Cyber Graphiin. Psykokirurginen
reartikulaatio voi koskea Psyche/Noetic-proxyä, jolloin siihen sovelletaan myös
PSI- ja psykokirurgiasääntöjä. Pelkkä semanttinen samankaltaisuus ei avaa
noeettista yhteyttä.

### Vaikutukset ja riskit

Onnistuminen tuottaa tavallisesti yhden rajatun graph effectin:

```text
domain: social | cyber | noetic
operation: reveal_relation | compare_neighborhood | add_edge |
           weaken_edge | relabel_context | meet | join
source: toimija tai työkalu
target: käsite- tai diskurssisolmu
provenance: havainto | mallipäätelmä | tulkinta | potilaan oma kuvaus
confidence: low | medium | high
```

Kallis onnistuminen tai epäonnistuminen ei lukitse kohtausta. Se voi tuottaa:

- **Semantic Drift:** käsite laajenee tai siirtyy tarkoitetun ulkopuolelle;
- **False Invariant:** yhteinen rakenne tulkitaan liian nopeasti samaksi
  merkitykseksi tai totuudeksi;
- **Frame Capture:** järjestelmän tai instituution sanasto alkaa määrätä, mitä
  ylipäätään voidaan ilmaista;
- **Provenance Loss:** potilaan oma kertomus, mallin päätelmä ja ulkoinen havainto
  sekoittuvat;
- **Noetic Trace** tai **Psyche Load**, jos toiminto ylittää noetic-rajapinnan.

### Suostumus ja agency

Rakenteen löytäminen ei anna lupaa muuttaa sitä. Hahmon uskomuksen, muiston,
identiteetin tai arkkityyppisen itsekuvan reartikulaatio vaatii suostumuksen,
ellei sitä käsitellä avoimena konfliktina, jossa panokset ja seuraukset ovat
näkyviä. Potilaan oma kuvaus säilytetään omana provenance-kerroksenaan myös
silloin, kun Ragnarök pitää toista mallia geometrisesti koherentimpana.

## Toteutusrajat

Tämä integrointi on tällä hetkellä teoria- ja sääntötasoinen. Se ei lisää
Day 1:een uutta kohtausta eikä kytke LLM:ää pelimoottoriin. Mahdollinen Python-
toteutus tehdään myöhemmin nykyisten Social/Cyber/Noetic-graafien päälle pieninä
tyypitettyinä operaatioina. Ensimmäinen prototyyppi tarvitsee vain:

1. tyypitetyt concept/discourse-nodet;
2. relation type-, provenance- ja confidence-kentät;
3. paikallisnaapurustojen vertailun;
4. meet/join-operaatiot eksplisiittisille attribuuteille;
5. tapahtumalokin, josta muunnos voidaan perua.

Embeddingiä tai generatiivista mallia ei tarvita ennen kuin graafimekaniikka on
pelitestissä osoittautunut hyödylliseksi.

## Avoimet tutkimuskysymykset

- Säilyvätkö jaetut muunnosrakenteet suomen, ruotsin ja englannin välillä vai
  hallitseeko englanninkielinen aineisto tulosta?
- Miten erotetaan mallissa oleva rakenne siitä, jonka probe tai tutkijan valitsema
  ontologia rakentaa?
- Milloin paikallinen geometrinen yhteensopivuus vastaa samaa käsitettä ja milloin
  vain samankaltaista käyttöä?
- Voidaanko Laclaun hegemoninen reartikulaatio operationalisoida temporaalisena
  graph rewrite -sarjana ilman, että poliittinen teoria typistyy embeddingiksi?
- Miten potilaan eletty kokemus ja agency säilytetään, kun instituutio käyttää
  laskennallisesti ylivoimaista representaatiojärjestelmää?

Viimeinen kysymys on Noöpunkin kannalta tärkein: täydellinen rakenteellinen kartta
ei ole sama asia kuin kartoitettavan subjektin qualia tai oikeus osallistua oman
merkityksensä tekemiseen.
