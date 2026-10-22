# Transhumanity's Fate -yhteensopivuus

## Lähde ja tavoite

Tarkistettu lähde on `sources/PS21003_TranshumanitysFate.pdf`, erityisesti PDF-sivut 12-13, 20-28, 32-59, 62-95 ja 105-117. *Transhumanity's Fate* edellyttää myös Fate Coren perussääntöjä.

Ubiquitous Maniacs käyttää sääntöjä kevyenä narratiivisena sovelluksena, ei täydellisenä toteutuksena. Tavoite on säilyttää Fate-yhteensopiva sanasto ja tuntuma ilman, että Day 1 muuttuu taistelu- tai resurssimoottoriksi.

## Toteutettu ja yhteensopiva

- Neljä Fate-noppaa (`4dF`), joiden sivut ovat -1, 0 ja +1.
- *Transhumanity's Faten* 24 skillin nimet.
- Hahmonluonnin 25 skill-pisteen budjetti, +4 skill cap ja Fate columns -ehto.
- Aspectit, tagit, conditionit ja consequencet tietomallissa.
- Success with style -tasoa vastaava vähintään +3 marginaali.
- Fail-forward: epäonnistuminen valitsee kirjoitetun seurauksen eikä pysäytä tarinaa.
- Ego-, morph-, psyche- ja cyber-tietojen erottaminen hahmomallissa.

`validate_transhumanity_fate_skill_profile()` tarkistaa skill-nimet, arvovälin, valinnaisen pistebudjetin ja Fate columns -rakenteen. Aktiivinen Romppaisen Day 1 -hahmo käyttää 25 pistettä.

## Tietoiset Noöpunk-poikkeamat

### Attribute + skill training

Alkuperäinen sääntö käyttää `4dF + skill`. Noöpunk käyttää:

```text
4dF + relevant attribute + skill training + eksplisiittiset bonukset vs difficulty
```

Siksi vaikeusasteita ei voi kopioida suoraan Fate-ladderilta. Day 1 on kalibroitu Romppaisen effective skill -arvoille. Attribuutin lisääminen on Noöpunkin oma, tietoinen hybridisääntö.

### Narratiiviset tulostasot

Faten tie, failure, success ja success with style on muunnettu viideksi narratiiviseksi tasoksi. Marginaalit -1 ja -2 tuottavat costly successin. Tämä on tarkoituksellinen fail-forward-sovellus.

### Aspectit ilman Fate point -taloutta

Nykyiset aspectit voivat avata valintoja tai antaa scenedatassa nimetyn +1 bonuksen. Ne eivät vielä käytä Faten +2 invokea, rerollia, free invokea, compelia tai Fate point -taloutta. Bonusta ei pidä dokumentoida varsinaisena Fate-invokena.

### Ei täyttä konfliktimoottoria

Nykyisessä Day 1:ssä ei ole stress trackeja, stress boxeja, concessionia, taken out -tilaa, exchangeja, zoneja tai hyökkäys/puolustusparia. `conditions` ja `consequences` ovat narratiivista jatkuvuutta, eivät vielä täydellinen *Transhumanity's Fate* -vahinkojärjestelmä.

### Morphit, stunts, refresh ja muse

Ego/morph-erottelu on tietomallissa, mutta morph aspectit, morph traitit, durability, stunts, refresh, resleeving ja muse-agentti eivät vielä osallistu Day 1:n sääntösilmukkaan.

### Psi ja psychosurgery

Lähdeteoksessa psi-traitit antavat permissionin poikkeuksellisiin toimintoihin ja psi-stuntit käyttävät Fate-rakennetta. Ubiquitous Maniacsin CAN, noettinen hakkerointi ja kvanttisanasto ovat omaa science fiction -ontologiaa. Niitä ei pidä esittää *Transhumanity's Faten* tai reaalimaailman tieteen suorina väitteinä.

## Day 1:n kalibrointi

Vahvan Narkkari-peitepersoonan Notice- ja Rapport-valinnat onnistuvat usein. Will-tarkistukset ovat tarkoituksella heikkoja, koska oikea persoona on suljettu ja psyyken koherenssi matala. Kaikilla tulostasoilla on fail-forward-seuraus, joten heikko Will ei lukitse etenemistä.

Skill-pisteiden täydentäminen 25 pisteeseen tehtiin nostamatta Day 1:n käyttämiä pääskillejä. Näin hahmoprofiili täyttää pistebudjetin mutta kohtauksien aiempi todennäköisyysprofiili säilyy.

## Suositeltu myöhempi laajennusjärjestys

1. Fate pointit, invoke/reroll ja compel narratiivisiin kohtauksiin.
2. Free invocation -tuki create advantage -tuloksille.
3. Mentaalinen stress track ja mild/moderate/severe consequences terapiaan.
4. Stuntit ja refresh vasta, kun persoonat, morphit ja psykokirurgia tarvitsevat pysyviä sääntöpoikkeuksia.
5. Konfliktimoottori vasta fyysistä tai mesh-konfliktia varten; sitä ei tarvita Day 1:n toimivuuteen.

Näitä ei ole toteutettu tässä tarkistuksessa, jotta nykyinen pelattava päivä ja moduulirajat eivät laajene hallitsemattomasti.

## Psi-punk vaihtoehtona

*Psi-punk* on arvioitu erikseen dokumentissa `PSI_PUNK_RULES_AND_INFLUENCE_REVIEW.md`. Suositus on säilyttää nykyinen *Transhumanity's Fate* -pohjainen hybridi RPG:n pääjärjestelmänä ja käyttää *Psi-punkia* rajattuna vaikutteena luonnollisen PSI:n, psykotronisten laitteiden, antipsi-turvallisuuden, mentaalisten seurausten sekä cyberpsi-/soul-hacking-sanaston suunnittelussa.

Arvio ei valtuuta sääntömuunnosta eikä uusien järjestelmien toteutusta. Täysi Fudge-konversio rikkoisi nykyisen seitsemän attributen mallin, 24 skillin profiilit, Day 1:n kalibroinnin ja olemassa olevat validaatiot ilman että se ratkaisisi CAN-, sosiaaligraafi- tai graafihakkerointitarpeita.
