# Askel 1: vain NetworkX-sosiaalinen graafi

Palataan projektissa takaisin alkuun.

Toteuta nyt **vain Askel 1**.

Älä suunnittele, toteuta tai valmistele Askelen 2 toiminnallisuuksia.

## Tavoite

Tee laboratoriossa olevista ihmisistä yksinkertainen **NetworkX-sosiaalinen graafi**.

Laboratoriossa on yhteensä 16 henkilöä:

* 8 potilasta
* 8 laboratorion henkilökunnan jäsentä

Jokainen henkilö on yksi NetworkX-graafin node.

Graafin tarkoitus on kuvata henkilöiden välisiä sosiaalisia suhteita.

Tässä vaiheessa ei huomioida sitä, kuka on pelaajahahmo.

## Tekninen rajaus

Käytä Pythonia ja NetworkX:ää.

Graafin tulee olla ohjelmallisesti helposti tarkasteltavissa ja sellaisessa muodossa, että sen tila voidaan myöhemmin näyttää esimerkiksi Streamlit-käyttöliittymässä.

Tämän vuoksi graafin rakenteen tulee olla selkeä ja helposti luettavissa Pythonista.

Esimerkiksi:

* nodet voidaan listata
* edge-suhteet voidaan listata
* yksittäisen henkilön suhteet voidaan tarkastaa
* graafin koko tila voidaan muuntaa Streamlitille sopivaan esitysmuotoon

Streamlit-käyttöliittymää ei kuitenkaan tarvitse vielä rakentaa, ellei aivan minimaalinen graafin tarkastelunäkymä ole välttämätön Askelen 1 toimivuuden todentamiseksi.

Pääasia on, että **NetworkX-graafin tila on ihmiselle helposti tarkastettavissa**.

## Graafin rakenne

Pidä ensimmäinen versio yksinkertaisena.

Node voi sisältää esimerkiksi:

```python
{
    "name": "...",
    "role": "patient" | "staff"
}
```

Edge kuvaa kahden henkilön välistä sosiaalista suhdetta.

Suhteelle voidaan käyttää yhtä yksinkertaista numeerista arvoa, esimerkiksi:

```python
relationship = 0
```

tai muuta vastaavaa yksinkertaista rakennetta.

Älä rakenna vielä monimutkaista suhdejärjestelmää.

## Alkutimension periaate

Potilaat aloittavat käytännössä sosiaalisena tabula rasana.

Heillä ei lähtökohtaisesti tarvitse olla valmiita suhteita toisiinsa.

Laboratorion henkilökunnalla voi olla olemassa olevia suhteita keskenään.

Tässä vaiheessa riittää kuitenkin se, että graafin rakenne tukee tällaisia suhteita.

## Tärkeä rajaus

Tässä vaiheessa EI toteuteta:

* Mesa-agentteja
* agenttisimulaatiota
* pelivuoroja
* päivittäisiä tapahtumia
* dialogijärjestelmää
* persoonallisuusmekaniikkaa
* addiktioita
* terapiamekaniikkaa
* laboratoriokokeita
* tekoälyagentteja
* LLM-integraatiota
* pelihahmomekaniikkaa
* pääjuonta
* tapahtumageneraattoria
* sosiaalisten suhteiden automaattista muuttumista
* muita simulaatiokerroksia

Älä myöskään rakenna näitä "valmiiksi tulevaisuutta varten".

Toteuta vain se rakenne, joka tarvitaan tämänhetkiseen NetworkX-graafiin.

## Valmis Askel 1

Askel 1 on valmis, kun:

1. NetworkX-graafi voidaan luoda.
2. Graafissa on 16 henkilöä.
3. Henkilöt voidaan erottaa potilaisiin ja henkilökuntaan.
4. Henkilöiden välisiä sosiaalisia suhteita voidaan kuvata edgeillä.
5. Graafin tila voidaan helposti tulostaa tai muuten tarkastaa Pythonista.
6. Rakenne soveltuu myöhemmin Streamlitissä visualisoitavaksi ilman, että Streamlit-järjestelmää tarvitsee vielä rakentaa.

Kun nämä toimivat, **lopeta työ tähän**.

Älä jatka seuraavaan vaiheeseen.

Älä ehdota Askelen 2 toteuttamista osana samaa muutosta.

Raportoi lyhyesti mitä Askelen 1 aikana toteutettiin ja mitä tiedostoja muutettiin.

## Työskentelyperiaate

Projektissa edetään tästä eteenpäin tarkoituksella hyvin hitaasti:

**yksi askel kerrallaan.**

Älä optimoi tulevia vaiheita varten.

Älä rakenna arkkitehtuuria, jota tämänhetkinen askel ei tarvitse.

Älä tee "samalla myös" -muutoksia.

Jos huomaat seuraavan luonnollisen kehitysaskeleen, voit mainita sen korkeintaan lyhyesti, mutta älä toteuta sitä.

**Muistuta myös Tomia: älä etene vielä Askelen 2 pariin. Testaa ja tarkastele ensin rauhassa NetworkX-graafia.**

Askel 1 on:

**NetworkX-graafi laboratorion 16 ihmisestä.**

Ei enempää.

Ei vähempää.
