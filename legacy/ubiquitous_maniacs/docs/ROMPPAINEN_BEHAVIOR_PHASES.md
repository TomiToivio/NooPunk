# Romppaisen valintariippuvaiset persoonallisuusvaiheet

Romppaisen persoonallisuus kehittyy kolmen vaiheen läpi pelaajan päätösten perusteella. Kalenteripäivä voi vaikuttaa tapahtumien kontekstiin, mutta se ei yksin vaihda vaihetta. Uudet käyttäytymismallit avautuvat kumulatiivisesti: aikaisemmat toimintatavat säilyvät valittavina myös myöhemmissä vaiheissa.

Kaari perustuu yhteen jungilaiseen varjoon. Narkkari, Kiimainen poliisi ja Paha Poliisi eivät ole kolme irrallista sivupersoonaa, vaan Romppaisen todellisten taipumusten eri tavoin säätelemättömiä ilmentymiä. UFAB ei istuta häneen vierasta psyykkistä materiaalia, vaan erottaa psykonauttiuden, hedonismin, anarkismin, seksuaalisuuden ja aggressiivisen poliisityön siitä reflektiivisestä kokonaisuudesta, joka normaalisti säätelee niitä.

Normaali Romppainen on vastuullinen psykonautti. Hän voi mennä pitkälle tietoisuuden tutkimuksessa, mutta tekee sen tietoisesti ja metodisesti: hän arvioi vaaran, annoksen, tarkoituksen, havainnoitavan ilmiön ja lopettamisen ehdot. Varjon Narkkari-ilmentymässä sama kokemuksenhalu menettää tarkoituksen ja jarrut. **Psykonautti etsii kokemusta ymmärtääkseen jotain; Narkkari etsii kokemusta, koska haluaa lisää kokemusta.**

## Vaihe 1: Narkkari

Romppainen on keinotekoisen narkkaripersoonansa vallassa. Persoonan materiaali ei silti ole täysin vierasta: se on rakennettu hänen vastuullisen psykonauttiutensa, nautinnonhalunsa ja uteliaisuutensa varjosta poistamalla toimijuus, reflektio ja kyky lopettaa. Käytettävissä ovat:

1. **Näyttele normaalia** (`play_normal`) — yritä vaikuttaa normaalilta, jotta et joudu ulos ohjelmasta.
2. **Anna periksi narkkarin hedonismille** (`narcotic_hedonism`) — tavoittele lisää lääkkeitä, varasta lääkkeitä, iske naisia tai hae muuta välitöntä nautintoa.

Tässä vaiheessa komisario Romppainen voi näkyä tahattomina vaistoina, mutta pelaaja ei voi vielä valita poliisi- tai tohtorimoodia.

## Vaihe 2: Kiimainen poliisi

Romppaisen aidot poliisitaidot ja hänen aina olemassa ollut jungilainen varjonsa työntyvät narkkaripersoonan läpi ilman yhtenäistä identiteettiä tai ammatillista itsehillintää. Kiimainen poliisi ei ole UFABin luoma sivupersoona, vaan Romppaisen anarkistinen, hedonistinen ja sääntöjä rikkova "Paha Poliisi" -puoli. Normaali Emil on oppinut säätelemään sitä ja päästämään sen tarkoituksellisesti läpi silloin, kun tehtävä sitä vaatii. UFAB, psykokirurgia ja muistivaurio poistavat tämän tarkoituksellisen kontrollin. Käytettävissä ovat:

1. **Näyttele normaalia** (`play_normal`).
2. **Anna periksi narkkarin hedonismille** (`narcotic_hedonism`).
3. **Ole kiimainen poliisi** (`horny_police`) — tunnista rikoksia ja käytä poliisirefleksejä, mutta tulkitse tehtävä narkkaripersoonan, eroottisten impulssien ja identiteettihämmennyksen läpi.

Kiimainen poliisi on yhtä aikaa pätevä, tutkiva ja erittäin omituinen, koska se käyttää Romppaisen todellisia kykyjä ilman hänen tavallista etiikkaansa ja itsesäätelyään. Pelaaja ei voi vielä valita täysin palautunutta tohtorimoodia.

## Vaihe 3: Tohtori Romppainen

Emil Romppaisen normaali persoona on palautunut suurimmaksi osaksi. Käytettävissä ovat kaikki aikaisemmat toimintatavat sekä:

4. **Ole tohtori Romppainen** (`doctor_romppainen`) — muista tehtävä, käytä psykiatrista ja tiedustelullista asiantuntemusta ja keskity operaation suorittamiseen.

Vaihe ei poista Sven-Olofia eikä Romppaisen Paha Poliisi -varjoa. Pelaaja voi edelleen teeskennellä normaalia, antautua hedonismille tai antaa varjon toimia kaoottisena narkkaripoliisina. Tohtorimoodi palauttaa mahdollisuuden tietoiseen itsesäätelyyn ja hallittuun varjon käyttöön; se ei poista varjoa eikä tee siitä epätodellista. Normaali Romppainen voi siis päästää Pahan Poliisin läpi, mutta säilyttää tavoitteen, harkinnan ja vastuun teoista.

Tiivistetty ero on: **Emil käyttää Pahaa Poliisia; Kiimainen poliisi -tilassa Paha Poliisi käyttää Emiliä.**

Sama pätee Narkkariin: normaali Emil voi tietoisesti valita vaarallisen kokemuksen, mutta Narkkari ei enää valitse vapaasti. Tohtorimoodin ydin ei ole halun kieltäminen vaan toimijuuden palautuminen: **"Kyllä, minäkin haluan tuota. Mutta minä päätän, mitä me teemme."**

## Kumulatiivinen avautuminen

| Vaihe | Käytettävissä olevat moodit |
| --- | --- |
| Narkkari | normaaliuden näytteleminen; narkkarin hedonismi |
| Kiimainen poliisi | edelliset + kiimainen poliisi |
| Tohtori Romppainen | edelliset + tohtori Romppainen |

Tekninen sopimus on moduulissa `src/romppainen_identity.py`. Se määrittelee vaiheet, moodit ja saatavuustarkistuksen.

## Päätösten vaikutus ja toteutusraja

Pelaajan päätökset määräävät, milloin Romppainen etenee vaiheesta seuraavaan. Tässä vaiheessa ei vielä määritellä yksittäisten päätösten palautumispisteitä, siirtymäkynnystä tai taantumista, koska niiden arvot eivät ole kanonisesti päätettyjä.

Seitsemän päivän identiteettikaari toimii tavoiteltuna dramaturgisena rytminä, ei automaattisena kalenterisääntönä. Pelaajan valinnat voivat nopeuttaa, hidastaa tai myöhemmin mahdollisesti horjuttaa etenemistä.

## Romanttiset suhdekaaret

`horny_police` voi aktivoida Romppaisen yksipuolisen projektion Lotta Kalliosta. Moodi ilmaisee Romppaisen hallitsematonta jungilaista varjoa, ei erillistä sivupersoonaa. `doctor_romppainen` ei vahvista projektiota, vaan normaali Romppainen tunnistaa varjon impulssin ja sen epäprofessionaalisuuden. Ingrid Falkin kanssa syntyvä mahdollisesti vastavuoroinen kietoutuminen on tästä erillinen juoni ja voi jatkua identiteettivaiheiden yli. Tarkempi sopimus on tiedostossa [`ROMPPAINEN_ROMANTIC_ARCS.md`](ROMPPAINEN_ROMANTIC_ARCS.md).
