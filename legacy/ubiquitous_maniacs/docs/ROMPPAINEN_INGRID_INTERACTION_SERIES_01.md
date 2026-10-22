# Romppainen ↔ Ingrid Falk 01: laboratorion tunnustelut

Tämä dokumentti suunnittelee vain Romppaisen ja Ingridin kolme ensimmäistä henkilökohtaista kohtaamista laboratorion arjessa. Terapiasessioiden assemblaasivuorovaikutukset ja pääjuonen aikaiset liittolaisuus-, epäily- tai tutkintakohtaukset ovat erillisiä myöhempiä sarjoja, eikä niitä suunnitella tässä.

## A. Lähtötilanne

Romppainen ja Ingrid ovat pelin alussa hedonistisia, hieman sosiopaattisia UFAB-addikteja. He eivät tunne toisiaan, mutta heidän varjonsa ovat samankaltaiset. Ingrid on Romppaisen anima ja Romppainen Ingridin animus; tämä tekee kietoutumisesta voimakkaan, vaikka kumpikaan ei vielä tunne tai ymmärrä rakennetta.

Terapiasessioissa he päätyvät myöhemmin muita hahmopareja useammin samaan assemblaasiin. Tämä on sarjan taustaehto, ei vielä laboratorion ensimmäisten kohtaamisten tiedossa oleva tosiasia.

### Ingridin ensikäsitys

Ingrid ”tunnistaa tyypin”. Romppainen näyttää samanlaiselta nautinnonhaluiselta, sääntöjä kiertävältä ja mahdollisesti manipuloivalta narkkarilta kuin hän itse. Ingridin kiinnostus ei ole aluksi rakkautta eikä luottamusta. Hän arvelee Romppaisen olevan:

- helppo lähestyä yhteisen UFAB-addiktion kautta;
- mahdollisesti helppo manipuloida;
- hyödyllinen lääkkeiden, tiedon tai suojan hankkimisessa;
- silti oudosti liian tarkka ja vaikeasti luettava.

Ingridin ensimmäiset lähestymiset ovat skeptisiä ja varovaisia tunnusteluita: ”tuo vaikuttaa samanlaiselta kuin minä, mutta kuinka samanlaiselta?”

### Romppaisen ensikäsitys

Romppainen tietää Ingridin olevan älykäs ja viehättävä kanssanisti. Hänen narkkarivarjonsa näkee mahdollisen nautintokumppanin. Palaavat poliisivaistot havaitsevat Ingridin testaavan, valehtelevan ja etsivän vipuvartta. Normaali Emil ei ole alussa riittävästi läsnä yhdistääkseen havaintoja kokonaiseksi arvioksi.

## B. Pienin suhdemalli

| Muuttuja | Merkitys |
| --- | --- |
| `interest` | Halu hakeutua uudelleen toisen seuraan; sisältää aluksi uteliaisuutta, hyötyä ja vetovoimaa. |
| `trust` | Valmius kertoa totta tai ottaa riski toisen puolesta. |
| `suspicion` | Epäily manipuloinnista, poliisitaustasta, petoksesta tai muista motiiveista. |
| `shadow_resonance` | Kuinka voimakkaasti hahmot vahvistavat toistensa hedonistista ja sosiopaattista narkkarivarjoa. |
| `known_facts` | Hahmokohtaiset liput siitä, mitä toinen tietää tai luulee tietävänsä Romppaisesta, Ingridistä ja heidän teoistaan. |

Arvot voivat olla hahmokohtaisia: Ingrid voi luottaa Romppaiseen vähemmän kuin Romppainen Ingridiin. Korkea kiinnostus ja korkea epäluulo ovat sallittu ja tärkeä yhdistelmä. Nykyinen suunnattu sentimentti jää yleiseksi tunnetilayhteenvedoksi eikä korvaa näitä muuttujia.

## Romppaisen käytettävissä olevat reaktiomoodit

Laboratoriokohtausten valinnat avautuvat Romppaisen nykyisen identiteettivaiheen mukaan:

| Vaihe | Valittavat moodit |
| --- | --- |
| Narkkari | `play_normal`, `narcotic_hedonism` |
| Kiimainen poliisi | edelliset + `horny_police` |
| Tohtori Romppainen | edelliset + `doctor_romppainen` |

Kohtaaminen ei itsessään siirrä Romppaista automaattisesti vaiheesta toiseen. Jos myöhempi kohtaaminen tapahtuu ennen oletettua palautumista, pelaajalle näytetään vain sillä hetkellä avautuneet moodit.

Ingrid ei alussa lämpene `horny_police`-käytökselle. Se kasvattaa hänen epäluuloaan ja voi laskea luottamusta, vaikka hänen kiinnostuksensa Romppaisen outouteen säilyisi. Liian aikainen `doctor_romppainen`-paljastuminen puolestaan herättää epäilyn poliisista tai henkilökunnan soluttautujasta.

## C. Kolme ensimmäistä laboratoriokohtaamista

### 1. Tuo vaikuttaa samanlaiselta kuin minä

**Päivän vaihe:** ensimmäinen päivällinen

**Aloittaja:** Ingrid

**Lähtökohta:** Ingrid pilkkaa Romppaisen vanhanaikaista plugi-implanttia ja tarkkailee, tunnistaako tämä pilkan sosiaaliseksi testiksi. Nykyinen `ingrid_cybernetic_mockery` on tämän kohtauksen alustava toteutus, mutta sen valinnat pitää myöhemmin sovittaa tähän rakenteeseen.

Pelaaja voi:

1. **`play_normal`: vastaa kohteliaasti ja vähättelee implanttia.** Sosiaalinen + 1d6 vs. 7. Onnistuminen saa Ingridin pitämään Romppaista hallittuna mutta kiinnostavana; epäonnistuminen näyttää teeskennellyltä ja kasvattaa epäluuloa.
2. **`narcotic_hedonism`: ohittaa loukkauksen ja kysyy, tietääkö Ingrid mistä saa lisää UFABia.** Ei testiä. Ingrid tunnistaa Romppaisen kanssanistiksi: molempien kiinnostus ja `shadow_resonance` kasvavat, mutta luottamus ei vielä kasva.

**Vaikutus seuraavaan:** Ingrid päättää, lähestyykö hän Romppaista toisessa kohtaamisessa mahdollisena rikoskumppanina vai manipuloitavana resurssina.

### 2. Ylimääräinen UFAB

**Päivän vaihe:** lääkkeidenjako tai iltapala myöhempänä päivänä

**Aloittaja:** Ingrid

**Lähtökohta:** Ingrid väittää tietävänsä keinon saada ylimääräinen UFAB-annos ja tarvitsevansa Romppaisen apua. Keino voi olla aito tai yritys saada Romppainen ottamaan riski hänen puolestaan.

Pelaaja voi valita nykyisen vaiheensa sallimista moodeista:

1. **`play_normal`: kieltäydy näkyvästi mutta yritä saada Ingrid paljastamaan suunnitelma.** Romppaisen Sosiaalinen vastaan Ingridin Psyykkinen. Onnistuminen lisää `known_facts`-tietoa; epäonnistuminen kertoo Ingridille, ettei Romppainen ole niin helposti vietävissä kuin näytti.
2. **`narcotic_hedonism`: suostu heti ja vaadi osuus.** Ei testiä. Kiinnostus ja `shadow_resonance` kasvavat. Jos luottamus on matala, Ingrid voi kusettaa Romppaista ja pitää annoksen itse.
3. **`horny_police`, jos avattu: tee tilanteesta sekava kuulustelu ja lähentely-yritys.** Ingrid torjuu kiimaisen käytöksen. Hänen epäluulonsa kasvaa, ja hän alkaa samalla epäillä Romppaisen poliisirefleksejä.

**Vaikutus seuraavaan:** Ingrid saa ensimmäisen konkreettisen arvion siitä, onko Romppainen helppo narkkari, vaarallinen kanssarikollinen vai mahdollinen poliisi.

### 3. Kuka sinä oikeasti olet?

**Päivän vaihe:** päivällinen tai valvomaton käytävähetki

**Aloittaja:** Ingrid

**Lähtökohta:** Ingrid on huomannut Romppaisen tarkkailevan kameroita, henkilökuntaa tai lääkkeidenjakelua liian ammattimaisesti. Hän kysyy näennäisen kevyesti, kuka Romppainen oikeasti on.

Pelaaja voi valita nykyisen vaiheensa sallimista moodeista:

1. **`play_normal`: pidä kiinni Sven-Olofin peitetarinasta.** Romppaisen Sosiaalinen vastaan Ingridin Psyykkinen. Onnistuminen hillitsee epäluuloa; epäonnistuminen vahvistaa Ingridin käsitystä salaisuudesta.
2. **`narcotic_hedonism`: vaihda aihe UFABiin ja ehdota yhteistä keikkaa.** Ei testiä. Tämä voi kasvattaa kiinnostusta ja siirtää kysymyksen myöhemmäksi, mutta samalla vahvistaa molempien narkkarivarjoa ja antaa Ingridille uuden tilaisuuden kusettaa.
3. **`horny_police`, jos avattu: vihjaa olevasi poliisi mutta sotke tunnustus kiimaiseen esiintymiseen.** Ingrid ei lämpene käytökselle. Hän pitää Romppaista joko vaarallisena poliisina tai vaarallisena hulluna; epäluulo kasvaa voimakkaasti.
4. **`doctor_romppainen`, jos avattu: anna rajattu, harkittu ja tosi havainto omasta tehtävästäsi paljastamatta kaikkea.** Älykkyys tai Sosiaalinen vastaan Ingridin Psyykkinen. Onnistuminen voi ensimmäistä kertaa kasvattaa todellista luottamusta. Liian täydellinen tai liian aikainen paljastus kasvattaa silti epäluuloa, koska Ingridillä on syytä pelätä poliisia.

**Tämän vaiheen päätös:** Ingrid on kiinnostunut Romppaisesta, mutta kiinnostuksen laatu on avoin. Hän voi nähdä tämän kaltaisenaan, mahdollisena uhrina, rikoskumppanina, poliisina tai jonkin näiden yhdistelmänä. Parantavaa romanssia tai femme fatale -haaraa ei vielä lukita.

## D. Jatkuvuus

```text
1. Ensitunnustelu
├─ normaaliuden esittäminen onnistuu → kiinnostus + varovainen epäluulo
└─ yhteinen nisti-identiteetti → kiinnostus + varjoresonanssi
                         ↓
2. Ylimääräinen UFAB
├─ Romppainen hankkii tietoa → Ingrid huomaa tämän vaikeaksi uhriksi
├─ yhteinen hedonismi → mahdollinen rikoskumppanuus tai Ingridin kusetus
└─ Kiimainen poliisi → torjunta + epäily poliisitaustasta
                         ↓
3. Kuka olet oikeasti?
├─ peitetarina kestää → skeptinen tunnustelu jatkuu myöhemmin
├─ narkkarivarjo hallitsee → femme fatale / yhteisen alamäen mahdollisuus kasvaa
├─ Kiimainen poliisi → kiinnostus voi säilyä, mutta luottamus heikkenee
└─ hallittu tohtori-minä → myöhempi aito luottamus ja parantava suhde mahdollistuvat
```

Epäonnistuminen ei lopeta sarjaa. Ingrid voi kiinnostua enemmän juuri siksi, että Romppainen valehtelee huonosti tai paljastaa vaarallisen puolensa. Vastaavasti onnistunut manipulointi voi heikentää myöhempää mahdollisuutta rakastavaan suhteeseen.

## Erilliset myöhemmät kerrokset

- **Terapiasessiot:** Romppainen ja Ingrid lomittuvat poikkeuksellisen usein samaan assemblaasiin; muut hahmot tulevat samaan rakenteeseen harvemmin.
- **Pääjuoni:** Ingrid voi myöhemmin olla tiedonlähde, epäilty, liittolainen, häiriötekijä, tutkimuskohde tai suojeltava.

Näiden kerrosten yksittäisiä kohtaamisia, haaroja tai quest-rakennetta ei määritellä tässä vaiheessa.

## Toteutusraja

Tämä on laboratoriovuorovaikutusten rakennemäärittely, ei toteutus. Nykyistä kohtausta, attribuutteja tai suhdetietomallia ei vielä muuteta koodissa. Seuraava askel saa koskea vain tämän saman laboratoriosarjan tarkentamista tai ensimmäisen kohtaamisen toteutusta.
