# Noöpunk RPG: kanoninen Attribute + Skill -suunta

## Tila ja rajaus

Tämä dokumentti määrittää Noöpunk: Ubiquitous Maniacsin RPG-suunnittelun kanonisen nykytilan ja myöhemmän iteratiivisen kehityksen lähtökohdan. Järjestelmä ei ole lopullinen.

Tässä vaiheessa ei toteuteta eikä muuteta pelimekaniikkaa. Erityisesti tässä dokumentissa ei päätetä resolution-mekaniikkaa, asteikkoja, noppia, vaikeusasteita, Field-rakennetta, lopullista Psi-skill-listaa, Mesh-taksonomiaa tai Cybernetics-remappausta.

## Yleinen suunnittelusuunta

Noöpunkin oma RPG-järjestelmä rakennetaan todennäköisesti yhdistämällä ja muokkaamalla:

- reskinnattua ja yksinkertaistettua Eclipse Phasea;
- Transhumanity's Faten yksinkertaistavia periaatteita;
- valikoituja Cities Without Number / Stars Without Number -mekaniikkoja;
- kokonaan uutta Noöpunk-materiaalia.

Tavoitteena ei ole minkään lähdejärjestelmän suora implementaatio tai sääntöortodoksia. Mekanismeja arvioidaan niiden hyödyllisyyden perusteella.

## Kanoniset attributet

Kaikilla hahmoilla on samat seitsemän yleistä kyvykkyyttä tässä järjestyksessä:

```text
Intelligence
Awareness
Reflexes
Body
Charisma
Willpower
Cybernetics
```

Alustava vastaavuus Eclipse Phasen aptitudeihin on vain lähdehistoriallinen kartta:

```text
COG -> Intelligence
INT -> Awareness
REF -> Reflexes
SOM -> Body
SAV -> Charisma
WIL -> Willpower
NEW -> Cybernetics
```

Cybernetics on Noöpunkin oma seitsemäs attribute.

## Attributet eivät korvaa skillejä

Tämä on kanoninen suunnittelupäätös:

- **Attribute** kuvaa hahmon yleistä kyvykkyyttä tietyllä alueella.
- **Skill** kuvaa tarkasti rajattua, opittua kykyä tietynlaiseen toimintaan.

Yksinkertaisella NPC:llä voi olla vain seitsemän attribute-arvoa. Pelaajahahmot ja tärkeät NPC:t voivat saada niiden lisäksi relevantteja erikoisskillejä. Näin sivuhahmot pysyvät kevyinä ilman, että keskeisten hahmojen osaaminen abstrahoidaan liian yleiseksi.

## Lupaava mutta päättämätön Attribute + Skill -malli

Myöhemmin tutkittava laskennallinen suunta on:

```text
Effective Skill = Relevant Attribute + Skill Training
```

Esimerkiksi:

```text
Reflexes 2
Guns 2
=> Guns check value 4
```

Tässä mallissa `Guns 2` tarkoittaisi kahden pisteen harjoittelua Reflexes-attributen päälle, ei kokonaisarvoa kaksi. Mallia ei ole hyväksytty lopulliseksi mekaniikaksi eikä sitä toteuteta vielä.

## Miksi tarkasti rajatut skillit säilytetään

Tietokoneroolipelin sääntömoottorin täytyy pystyä ratkaisemaan yksiselitteisesti:

- milloin kykyä käytetään;
- mihin toimintoihin se vaikuttaa;
- milloin se ei vaikuta;
- miten useat kyvyt suhtautuvat toisiinsa.

Täsmällinen `Guns` on siksi mekaanisesti käyttökelpoisempi kuin yleinen `Combat Veteran`, jos jälkimmäisen relevanssi pitäisi tulkita uudelleen jokaisessa tilanteessa.

Tagit, aspectit, stuntit ja taustat voivat tulla myöhemmin skillien rinnalle. Ne eivät korvaa eksplisiittistä skill-listaa. Persoonallisuustagit säilyvät erillisenä hahmojen valintoja painottavana järjestelmänä.

## Eclipse Phasen skill-lista suunnittelun lähtökohtana

Seuraavat nimet ja attribute-mappaukset ovat alustavia. Skillien lopullista nimistöä tai rakennetta ei ole päätetty.

| Skill | Alustava attribute | Rajaus / avoin kysymys |
|---|---|---|
| Athletics | Body | Fyysinen toiminta gravitaatiossa humanoidi-, uplift- tai biomimetic-morphilla. |
| Deceive | Charisma | Valehtelu, bluffi, huijaus, fast talk, impersonation ja näytteleminen. |
| Exotic Skill | Field unresolved | Harvinaisten erikoistaitojen catch-all; Field-rakennetta ei päätetä. |
| Fray | Reflexes | Vaaran ja hyökkäysten väistäminen. |
| Free Fall | Body | Fyysinen toiminta mikrogravitaatiossa. |
| Guns | Reflexes | Beam-, kinetic-, seeker- ja spray-aseiden tähtääminen ja käyttäminen. |
| Hardware | Intelligence / Field unresolved | Rakentaminen, korjaaminen, deaktivointi, päivittäminen ja fyysinen hakkerointi. |
| Infiltrate | Reflexes | Hiipiminen, piiloutuminen ja havaitsemisen välttäminen. |
| Infosec | Intelligence | Verkkojen hakkerointi ja suojaaminen; suhde Cyberneticsiin on avoin. |
| Interface | Intelligence | Elektroniset laitteet, ohjelmistot, verkot ja asejärjestelmät; suhde Cyberneticsiin on avoin. |
| Kinesics | Charisma | Kehonkieli, tellsit ja nonverbaalinen viestintä; Awareness voi myöhemmin osoittautua relevantiksi. |
| Know | Field unresolved | Erikoistunut taide-, harrastus-, tiede- tai ammattitieto; attribute ja Field ovat avoimia. |
| Medicine | Intelligence / Field unresolved | Emergency care, forensics, pharmacology, psychosurgery ja surgery. |
| Melee | Body | Aseeton ja käsissä pidettävillä aseilla käytävä lähitaistelu. |
| Perceive | Awareness | Fyysiset aistit ja ympäristön havaitseminen; mahdollista myöhempää jakoa ei tehdä vielä. |
| Persuade | Charisma | Neuvottelu, vakuuttaminen, etiketti ja sosiaalinen manipulointi. |
| Pilot | Reflexes / Field unresolved | Ajoneuvot sekä ei-humanoidit ja ei-biomimeettiset morphit. |
| Program | Intelligence | Ohjelmistot, nanofabrikaatio, VR ja AR; suhde Cyberneticsiin on avoin. |
| Provoke | Charisma | Intimidation, taunting, seduction ja muu emotionaalinen manipulointi. |
| Psi | Willpower / temporary | Väliaikainen lähtökohta; yksi yleinen Psi-skill vaikuttaa liian karkealta. |
| Research | Awareness | Mesh-datan etsiminen ja tulkitseminen; Cybernetics-suhde arvioidaan myöhemmin. |
| Survival | Awareness | Navigointi, jäljittäminen, suoja, ravinto ja vihamieliset ympäristöt. |

## Field-järjestelmä jätetään auki

Seuraavien skillien Field-mekaniikkaa ei vielä suunnitella:

```text
Exotic Skill
Hardware
Know
Medicine
Pilot
```

Niille ei tehdä lopullisia Field-listoja, enumia, tietomallia, automaattista yhdistelyä tai poistopäätöstä.

## Cybernetics-remappaus jätetään auki

Cybernetics voi myöhemmin muuttaa ainakin seuraavien skillien mappausta:

```text
Infosec
Interface
Program
Research
Hardware
```

Tavoitteena on erottaa yleinen analyyttinen Intelligence koneellisen, augmentoidun ja kyberavaruuden kognition käyttämisestä. Rajaa ei ratkaista tässä vaiheessa.

## Psioniikka suunnitellaan erikseen

Noöpunkin luonnollinen psioniikka ei ole sama asia kuin Eclipse Phasen Watts–MacLeod-/Exsurgent-psi. `Psi (Willpower)` säilyy vain väliaikaisena suunnittelun lähtökohtana.

Myöhemmin on ratkaistava erikseen:

- luonnollisen psioniikan skillit;
- Awarenessin tehtävä havaitsemisessa ja ymmärtämisessä;
- Willpowerin tehtävä voimakkuudessa ja vastustamisessa;
- Cyberneticsin tehtävä psychotronic-järjestelmissä;
- luonnollisen Psychen ja teknologisen vahvistuksen suhde.

Yhtä lopullista Psi-skilliä, psioniikkaskillejä tai psychotronic-mekaniikkaa ei määritellä vielä.

## Mesh tarvitsee myöhemmin eksplisiittisen verkkomallin

Mesh / cyberspace määritellään myöhemmin eksplisiittisenä verkkona, jolla on node-tyypit, edge-tyypit, protokollat, käyttöoikeudet ja agenttien toimintatavat. Tämä liittyy Infoseciin, Interfaceen, Programiin, Researchiin ja Cyberneticsiin.

Node-/edge-taksonomiaa ei suunnitella tai toteuteta tämän päätöksen yhteydessä.

## Kanoninen nykyperiaate

> Attributes provide general capability. Skills provide explicitly scoped learned capability.

Alustava, ei vielä toteutettava ajatus on:

```text
Check Value = Relevant Attribute + Relevant Skill
```

Lopullista resolution-mekaniikkaa, asteikkoa, noppia tai vaikeusasteita ei ole päätetty.

## Toteutusraja

Tämän dokumentin perusteella ei vielä:

- muuteta olemassa olevaa pelimekaniikkaa tai dialogijärjestelmää;
- toteuteta skill-järjestelmää tai Attribute + Skill -laskentaa;
- rakenneta uusia hahmolomakkeita;
- ratkaista Field-, Psi-, psychotronic-, Cybernetics-remappaus- tai Mesh-kysymyksiä;
- portata Eclipse Phase-, Fate- tai Without Number -sääntöjä.

Kaikki nämä vaativat oman myöhemmän suunnittelukierroksensa.
