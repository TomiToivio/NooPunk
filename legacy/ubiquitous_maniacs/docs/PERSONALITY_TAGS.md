# Persoonallisuustagit

Hahmojen persoonallisuutta kuvataan koneellisesti luettavilla tageilla. Tagi voi olla positiivinen tai negatiivinen ominaisuus ja se voi myöhemmin painottaa hahmon tekemiä valintoja. Tagit eivät pakota yhtä toimintoa: ne muuttavat vaihtoehtojen todennäköisyyttä tai houkuttelevuutta.

CSV-kenttä on `personality_tags`. Useat tagit erotetaan puolipisteellä. Latauksen jälkeen kenttä on merkkijonolista NetworkX-solmun attribuuteissa.

## Ensimmäinen tagiperhe: addiktiot

| Tagi | Polaarisuus | Vaikutussuunta |
| --- | --- | --- |
| `addiction:ufab_80mg` | negatiivinen | pyrkii hankkimaan ja kuluttamaan UFAB 80MG:tä, mahdollisesti varastamalla sitä laboratoriosta tai toisilta potilailta |
| `addiction:amphetamine` | negatiivinen | pyrkii hankkimaan ja kuluttamaan amfetamiinia |
| `addiction:alcohol` | negatiivinen | pyrkii hankkimaan ja kuluttamaan alkoholia |
| `addiction:cocaine` | negatiivinen | pyrkii hankkimaan ja kuluttamaan kokaiinia |
| `addiction:cannabis` | negatiivinen | pyrkii hankkimaan ja kuluttamaan kannabista |

## UFABin dominoiva prioriteetti

UFAB 80MG on päivittäin saatavilla ja huomattavasti muita aineita voimakkaampi. Siksi muut addiktiot ovat laboratorion arjessa pääasiassa taustahistoriaa:

- jos UFAB on saatavilla, UFAB-toiminnon painokerroin on `2.0`;
- samassa tilanteessa muun päihteen kuluttamisen painokerroin putoaa arvoon `0.25`;
- jos UFAB ei ole saatavilla, hahmon muu vastaava addiktiotagi saa normaalin kertoimen `1.5`;
- terapia, keskustelu ja muut päihteisiin liittymättömät toiminnot säilyvät neutraalissa kertoimessa `1.0`.

Näin esimerkiksi Irungun kannabistagi ja Sven-Olofin amfetamiinitagi säilyttävät hahmohistorian, mutta eivät kilpaile UFABin kanssa tavallisena hoitopäivänä. Ne aktivoituvat vasta UFAB-puutteessa, saannin estyessä tai erikseen kirjoitetussa tilanteessa.

Painotus ei vielä itsenäisesti luo kulutus-, etsintä- tai varastamistapahtumaa.

## Toteutusraja

Tässä vaiheessa toteutetaan tietomalli, validointi, käyttöliittymän näyttö ja valintapainon apufunktio. Varsinaiset päihteiden varastamis-, hallussapito-, vieroitus- ja kulutusmekaniikat lisätään myöhemmin erillisinä testattuina tapahtumina.
