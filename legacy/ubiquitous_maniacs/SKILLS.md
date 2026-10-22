# Kanoninen hahmomalli: attributet

## Status

Tämä dokumentti määrittää Noöpunk: Ubiquitous Maniacsin aktiivisen ja kanonisen attribute-järjestelmän. Se korvaa aiemmat alustavat aptitude-, stat- ja attribute-listat.

Kanoninen järjestys on aina:

1. **Intelligence**
2. **Awareness**
3. **Reflexes**
4. **Body**
5. **Charisma**
6. **Willpower**
7. **Cybernetics**

Uusia yleisiä attributeja ei lisätä ilman erillistä suunnittelupäätöstä.

## Attributet

### Intelligence

Looginen ja analyyttinen ajattelu, ongelmanratkaisu, oppiminen, tiedonkäsittely, suunnittelu, abstrahointi sekä teknisten ja tieteellisten ongelmien ymmärtäminen. Intelligence ei tarkoita intuitiota, empatiaa tai tietoisuuden kehitystä.

### Awareness

Tietoisuuden laatu ja herkkyys: intuitio, empatia, loving kindness, emotionaalinen herkkyys, hienovaraisten psykologisten ja noettisten ilmiöiden havaitseminen, läsnäolo, itsehavainnointi ja kokonaisuuksien hahmottaminen ilman eksplisiittistä päättelyä.

Awareness kuvaa sitä, kuinka hyvin Psyche havaitsee ja ymmärtää. Se ei ole sama asia kuin Willpower.

### Reflexes

Reaktionopeus, koordinaatio, tasapaino, ketteryys, hienomotoriikka, nopeat fyysiset ratkaisut ja sensorimotorinen toiminta.

### Body

Morphin fyysisten ominaisuuksien käyttäminen: voima, kestävyys, rasituksen sieto, ruumiillinen kontrolli ja biologisten tai mekaanisten kykyjen hyödyntäminen. Body ei määritä Morphin absoluuttisia teknisiä rajoja.

### Charisma

Sosiaalinen toimintakyky: tilanteiden lukeminen, vuorovaikutus, vakuuttaminen, manipulointi, neuvottelu, esiintyminen, sosiaalinen adaptiivisuus ja toisten reaktioiden ymmärtäminen.

Awareness tuottaa syvän intuitiivisen tai empaattisen havainnon. Charisma kuvaa kykyä käyttää ymmärrystä sosiaalisessa toiminnassa.

### Willpower

Tahdonvoima, itsehillintä, psykologinen kestävyys, keskittyminen, oman mielen koherenssi sekä ulkoisen vaikutuksen vastustaminen.

Willpower kuvaa myös psioniikan raakaa voimakkuutta: intention voimaa, psyykkistä puolustusta, psychotronic-laitteiden operointia ja toisen Conscious Agentin vaikutuksen vastustamista. Tässä muutoksessa ei toteuteta psioniikkamekaniikkaa.

### Cybernetics

Kyky toimia kyberneettisten järjestelmien kautta: kyberavaruus, implantit, BCI-järjestelmät, koneellinen Ego, digitaaliset agentit, augmentaatiot sekä ihmisen ja koneen rajapinta.

Cybernetics ei ole sama asia kuin Intelligence. Yleinen analyyttinen lahjakkuus ja kyberneettinen toimintakyky voivat kehittyä toisistaan riippumatta.

## Suhde Eclipse Phaseen

Noöpunkin järjestelmä on löyhästi johdettu Eclipse Phasen ensimmäisen laitoksen aptitudeista, mutta ei käytä niitä sellaisenaan:

| Eclipse Phase -lähde | Noöpunk |
|---|---|
| Cognition | Intelligence |
| Intuition | Awareness |
| Reflexes | Reflexes |
| Somatics | Body |
| Savvy | Charisma |
| Willpower | Willpower |
| Ei suoraa vastinetta | Cybernetics |

Lyhenteet COG, INT, REF, SAV, SOM ja WIL eivät kuulu aktiiviseen Noöpunk-hahmomalliin.

## Psyche ei ole attribute

Psyche säilyy ontologisena käsitteenä: se on hahmon tietoisuus, Conscious Agent ja nonlokaali tietoisuuskomponentti. Sitä ei käytetä yleisenä attribute-arvona.

- **Awareness:** tietoisuuden laatu, intuitio, empatia, havainto ja kehitys.
- **Willpower:** tahdon voimakkuus, mentaalinen resistanssi ja psioninen voima.

## Attributet ja skillit

Attribute kuvaa yleistä kyvykkyyttä. Skill kuvaa tarkasti rajattua opittua kykyä. Attributet eivät korvaa skill-listaa, eikä skill-listaa korvata yleisillä tageilla.

Transhumanity's Faten 24 skillin lista on otettu käyttöön. Hahmonluonnissa jaetaan 25 skill-pistettä. Jokainen skill on linkitetty yhteen Noöpunkin attribuutista. Laskenta on yksinkertainen (Citizen Sleeper -tyylinen):

```text
Effective Skill = Relevant Attribute + Skill Training
4dF + Effective Skill vs Difficulty
```

Ei Fate Point -ekonomiaa, ei stuntteja, ei stress-trackeja. Attribuutit, skillit, aspectit (bonuksina) ja tagit (bonuksena tai ehtona) riittävät.

## Skill → Attribute -mappaus

| Skill | Attribuutti | EP-lähde |
|---|---|---|
| Athletics | Body | Somatics |
| Civ Rep | Charisma | Savvy |
| Cover | Charisma | Savvy |
| Cred | Charisma | Savvy |
| Deceive | Charisma | Savvy |
| Eye Rep | Charisma | Savvy |
| Fight | Reflexes | Somatics/Reflexes |
| Hardware | Intelligence | Cognition |
| Infiltrate | Reflexes | Reflexes |
| Infosec | Cybernetics | Cognition |
| Investigate | Intelligence | Cognition |
| Kinesics | Awareness | Savvy/Intuition |
| Medicine | Intelligence | Cognition |
| Notice | Awareness | Intuition |
| Pilot | Reflexes | Reflexes |
| Program | Cybernetics | Cognition |
| Provoke | Charisma | Savvy |
| Rapport | Charisma | Savvy |
| Shoot | Reflexes | Reflexes |
| Somatics | Body | Somatics |
| Survival | Awareness | Intuition |
| Will | Willpower | Willpower |
| Xeno-Contact | Awareness | Cognition/Intuition |
| X-Risks | Intelligence | Cognition |

Infosec ja Program on määritelty Cybernetics-attribuutille (ei Intelligence), koska Noöpunkissa kyberneettinen toimintakyky on erillinen attribute. Kinesics ja Xeno-Contact on määritelty Awareness-attribuutille, koska Noöpunkissa Awareness kattaa intuition ja empatian.
