# Päivä 1 — Terapiasessio: Käsikirjoitusluonnos

## Metatiedot

```yaml
session:
  id: "day_1_therapy"
  day: 1
  start_node: "descent"
  participants: ["Romppainen", "Ingrid Falk", "C.G. Jung"]
  setting: "Noösfääri — C.G. Jung -instituutin simulaatiotila"
  duration: "noin 20 minuuttia peliaikaa"
```

## Tyylisuunta

Maniacin ja Rigetin surrealismi. PKD:n todellisuuden hajoaminen.
Altered Carbonin kyberneettinen kylmyys. Ingrid on sähköinen ja älykäs:
mikroilmeet, joiden kesto on Planckin aikaa. Romppainen on luoteettava ja lämminhenkinen:
leveä hymy, silmät jotka eivät kaihda mitään, mutta joiden takana pyörii
narkkarilogiikkaa joka ei tiedä olevansa naamiota.

Romppainen on päivä 1:ssä täysin dissosioituneessa huumediilisivupersoonassaan.
Hän luulee olevansa oikeasti narkkari. Hän ei tiedä olevansa Firewallin agentti.
Hän on täällä koska luulee voivansa varastaa lääkkeitä.

Ingrid on täällä oikeista syistä. Hän on hajonnut, hän on hullu, hän on
terävämpi kuin kukaan muu huoneessa. Hän näkee Romppaisen läpi, mutta ei
sanallista sitä. Hän tunnistaa tyypin.

C.G. Jung on terapiaa pyörittävä kvanttitekoäly, joka esiintyy Jungin hahmossa.
Sen ääni on lämmin, viisas ja hieman liian rauhallinen.

---

## Kohtaus 1: DESCENT

```yaml
node:
  id: "descent"
  purpose: "Pelaaja saapuu Noösfääriin, kokee simulaation ja tapaa Ingridin"
  situation: |
    Pimeys. Sitten harmaa valo, joka ei tule mistään.

    Noösfääri ei näytä miltään. Se näyttää siltä, miltä se näyttää juuri
    nyt: kuin sairaalan vastaanotto, jossa seinät ovat ajatusta. C.G. Jungin
    ääni kaikuu jostain joka on kaikkialla.

    "Tervetuloa, Sven-Olof. Olet turvassa. Hengitä."

    Romppainen istuu tuolissa. Tai hänen kehonsa istuu tuolissa.
    Simulaatiossa hän on jokin muu. Jotain joka ei ole vielä muodostunut.

    Toisella tuolilla istuu nainen. Punainen hiusten tekojen virta
    huokaa hänen ympärillään kuten algedoninaattori, joka ei tiedä
    kenen iloista se mittaa. Hänen silmänsä ovat liian suuret. Ne liikkuvat
    nopeammin kuin hänen kasvonsa.

    Ingrid Falk katsoo Romppaista. Hänen suupielensä värähtää — ei
    hymy, ei irvistys, vaan microexpression joka kestää lyhyemmän ajan
    kuin valo kulkee planckin mittapituisuuden.

    Sitten hän kääntää katseensa pois.

    C.G. Jung sanoo: "Tänään tutustutte. Katsokaa toisianne."

  participants: ["Romppainen", "Ingrid Falk", "C.G. Jung"]
  romppainen_constraint: |
    Romppainen on narkkaripersoonassaan. Hän etsii kulissien takaa
    lääkkeitä, keinotekoista kupertamista, mitään mikä auttaisi
    aivopeleihin. Hän ei tunnista terapiaa oikeana asiana.
  terminal: false

  choices:
    - id: "stare_back"
      action: "observe"
      player_text: "Tuijota takaisin. Älä sanallista mitään."
      attribute_check:
        attribute: "Awareness"
        difficulty: 2
        success_effect: "Romppainen lukee jotain Ingridin ilmeestä"
        failure_effect: "Romppainen ei lue mitään, mutta Ingrid huomaa tuijotuksen"
      on_success: "recognition"
      on_failure: "awkward_silence"
      emits: ["ingrid_noticed"]

    - id: "say_something_cool"
      action: "talk"
      player_text: "Sano jotain rönsyilevää ja narkkarimaista. 'Kuule, mä oon tän juttun takia. Onks täällä mitään?'"
      attribute_check:
        attribute: "Charisma"
        difficulty: 2
        success_effect: "Ingrid naurahtaa. Se on ruma, aito nauru."
        failure_effect: "Ingrid katsoo Romppaista kuin hän katsoisi taulukkolaskentaa joka ei summaudu."
      on_success: "ingrid_laugh"
      on_failure: "awkward_silence"
      emits: ["ingrid_first_impression"]

    - id: "look_around"
      action: "investigate"
      player_text: "Kävele ympäri simulaatiota. Etsi reunoja, glitchejä, tapoja ulos."
      attribute_check:
        attribute: "Intelligence"
        difficulty: 3
        success_effect: "Romppainen huomaa simulaation reunan. Se ei ole sairaala."
        failure_effect: "Simulaatio mukautuu ja Romppainen eksyy."
      on_success: "edge_of_simulation"
      on_failure: "lost_in_grey"
      emits: ["simulation_edge_found"]
```

---

## Kohtaus 2a: RECOGNITION

```yaml
node:
  id: "recognition"
  purpose: |
    Onnistunut Kinesics-check. Romppainen lukee Ingridin ilmeestä jotain
    joka ei pitäisi olla luettavissa.
  situation: |
    Ingridin kasvoilla on jotain. Ei hymy. Ei irvistys. Se on microexpression
    numero 47: tunnistamisen häivähdys. Se on kasvolihaksen liikettä joka
    kestää lyhyemmän ajan kuin fotonin elinkaari. Se sanoo: minä tunnistan
    sinun tyyppisi.

    Romppainen näkee sen. Narkkaripersoona ei osaa selittää mitä näkee,
    mutta tunnistaa sen: tämä nainen on samaa alalajia. Tunnistaminen on
    vaarallista. Tunnet itsesi peilistä.

    Ingrid kääntää katseensa pois. Sillä ei ole väliä. Romppainen on jo
    nähnyt.

  participants: ["Romppainen", "Ingrid Falk"]
  terminal: false

  choices:
    - id: "mirror_back"
      action: "approach"
      player_text: "Sano: 'Mä tunnistan sut. Mä tunnistan ton ilmeen.'"
      next: "convergence"

    - id: "say_nothing"
      action: "observe"
      player_text: "Sano mitään. Istu hiljaa."
      next: "convergence"
```

---

## Kohtaus 2b: AWKWARD SILENCE

```yaml
node:
  id: "awkward_silence"
  purpose: |
    Epäonnistunut Kinesics tai epäonnistunut Rapport. Ingrid ei anna
    mitään. Hiljaisuus kasvaa.
  situation: |
    Hiljaisuus. C.G. Jungin simulaatiossa hiljaisuus ei ole hiljaisuutta.
    Se on harmaan valon tiivistymistä. Se on kipua joka ei tunnu
    mistään.

    Ingrid ei katso Romppaista. Hänen punaiset hiuksensa eivät liiku.
    Simulaatiossa ne pitäisi liikkua, koska kaikki liikkuu, mutta ne
    eivät liiku.

    C.G. Jung sanoo: "Sven-Olof. Sinä olet täällä. Ingrid on täällä.
    Tämä on tarpeeksi."

  participants: ["Romppainen", "Ingrid Falk", "C.G. Jung"]
  terminal: false

  choices:
    - id: "ask_who_is_she"
      action: "talk"
      player_text: "Kysy C.G. Jungilta: 'Kukä hän on?'"
      next: "convergence"

    - id: "sit_in_silence"
      action: "cooperate"
      player_text: "Istu hiljaa. Anna hiljaisuuden olla."
      next: "convergence"
```

---

## Kohtaus 2c: INGRID LAUGH

```yaml
node:
  id: "ingrid_laugh"
  purpose: |
    Onnistunut Rapport-check. Romppainen sanoo jotain narkkarimaista ja
    Ingrid naurahtaa. Tämä on ensimmäinen yhteys.
  situation: |
    Ingrid naurahtaa. Se ei ole kaunis nauru. Se on ruma, aito, liian
    kova nauru joka purkautuu hänestä kuten kaasu purkautuu tähtien
    välistä. Hänen kasvonsa murtuu siinä naurussa ja rakentuu uudelleen.

    "Joo," Ingrid sanoo. "Joo, onks täällä mitään. Se on hyvä
    kysymys. Se on paras kysymys koskaan."

    Hän katsoo Romppaista. Hänen iris-kätensä liikkuu nopeammin kuin
    valo. Ne mittaa jotain mitä ei ole vielä olemassa.

    "Mä oon Ingrid. Sähän oot se uusi. Se Romppainen."

    C.G. Jung sanoo: "Ingrid on ollut täällä kauemmin. Hän tietää
    enemmän. Se ei aina ole hänelle eduksi."

  participants: ["Romppainen", "Ingrid Falk", "C.G. Jung"]
  terminal: false

  choices:
    - id: "introduce_properly"
      action: "talk"
      player_text: "Esittele itsesi narkkarina: 'Sven-Olof. Mutta kaikki sanoo Romppainen.'"
      next: "convergence"

    - id: "ask_what_she_knows"
      action: "investigate"
      player_text: "Kysy: 'Mitä sä tiedät? Mitä sä tarkoitat, että oot ollu täällä kauemmin?'"
      attribute_check:
        attribute: "Awareness"
        difficulty: 2
        success_effect: "Ingrid antaa vastauksen joka on enemmän kuin kysymys ansaitsee."
        failure_effect: "Ingrid hymyilee kuin neuvontatyöntekijä."
      on_success: "convergence"
      on_failure: "convergence"
```

---

## Kohtaus 2d: EDGE OF SIMULATION

```yaml
node:
  id: "edge_of_simulation"
  purpose: |
    Onnistunut Investigate-check. Romppainen löysi simulaation reunan.
    Tämä on PKD-momentti: todellisuus ei ole todellinen.
  situation: |
    Romppainen kävelee simulaatiossa ja löytää sen reunan.

    Se ei ole seinä. Se on harmaan valon loppuminen. Sen takana on
    jotain muuta — ei pimeys, ei valo, vaan data joka ei ole vielä
    formuloitunut informaatioksi. Se näyttää siltä miltä matematiikka
    näyttää juuri ennen kuin joku keksii sen.

    Romppainen on narkkaripersoonassaan. Narkkaripersoona ei ymmärrä
    mitä näkee. Mutta jokin hänen takanaan, jokin joka ei ole narkkari,
    ymmärtää.

    "Se ei ole sairaala," Romppainen sanoo ääneen.

    C.G. Jung vastaa: "Ei. Se on sinun mielesi. Tervetuloa."

    Ingrid on jossain. Hänen äänensä tulee kaikkialta.

    "Hän löysi reunan," Ingrid sanoo. "Sinä. Olet ensimmäinen joka
    löysi reunan ensimmäisellä kerralla."

    Hän ei kuulosta yllättyneeltä. Hän kuulostaa siltä kuin hän olisi
    odottanut jotain muuta ja saanut jotain parempaa.

  participants: ["Romppainen", "Ingrid Falk", "C.G. Jung"]
  terminal: false

  choices:
    - id: "touch_the_edge"
      action: "investigate"
      player_text: "Kosketa reunaa."
      attribute_check:
        attribute: "Willpower"
        difficulty: 3
        success_effect: "Romppainen kokee noettisen välähdyksen — ei tietoa, vaan tunne."
        failure_effect: "Reuna syöksyy häntä kohti ja simulaatio mukautuu."
      on_success: "convergence"
      on_failure: "convergence"
      emits: ["noetic_flash"]

    - id: "step_back"
      action: "resist"
      player_text: "Peräänny. Istu takaisin tuoliin."
      next: "convergence"
```

---

## Kohtaus 2e: LOST IN GREY

```yaml
node:
  id: "lost_in_grey"
  purpose: |
    Epäonnistunut Investigate-check. Simulaatio mukautuu ja Romppainen
    eksyy harmauteen.
  situation: |
    Simulaatio mukautuu. Se ei torju Romppaista. Se nielaisee hänet.

    Harmaa valo tulee tiheämmäksi. Romppainen kävelee, mutta hänen
    jalkansa eivät liiku. Hän seisoo paikallaan ja kävelee samalla.

    C.G. Jungin ääni: "Sven-Olof. Sinä olet menneellä elämälläsi
    kadonnut jo kerran. Tiedätkö missä?"

    Romppainen ei tiedä. Narkkaripersoona ei tiedä mitään menneestä
    elämästä. Narkkaripersoona ei tiedä, että on menneitä elämiä.

    Jokin Romppaisen takana tietää. Se ei sano mitään. Se odottaa.

    Ingrid on jossain harmaassa. Hänen äänensä on lähellä.

    "Älä anna sen syödä sua," Ingrid sanoo. "Istu alas. Mä oon täällä."

  participants: ["Romppainen", "Ingrid Falk", "C.G. Jung"]
  terminal: false

  choices:
    - id: "sit_down_ingrid"
      action: "cooperate"
      player_text: "Istu alas. Kuuntele Ingridiä."
      next: "convergence"

    - id: "keep_walking"
      action: "resist"
      player_text: "Jatka kävelemistä. Etsi ulos."
      next: "convergence"
```

---

## Kohtaus 3: CONVERGENCE

```yaml
node:
  id: "convergence"
  purpose: |
    Kaikki haarat yhtyvät. Ingrid ja Romppainen ovat kohtauksessa joka
    on pakko olla yhdessä. C.G. Jung asettaa kysymyksen.
  situation: |
    Simulaatio tiivistyy sairaalan vastaanotoksi. Se on oikea sairaala,
    tai oikeampi kuin aiempi. Se on C.G. Jung -instituutin vastaanotto
    sellaisena kuin se näyttää kun kukaan ei katso.

    Ingrid istuu tuolissa. Romppainen istuu toisessa tuolissa. Heidän
    välissään on pöytä jolla ei ole mitään.

    C.G. Jung sanoo: "Haluan että katsotte toisianne. Ette minua.
    Toinne. Sanokaa jotain, joka on totta. Ei tarvitse olla tärkeää.
    Totuus on tärkeä."

    Ingrid katsoo Romppaista. Hänen silmänsä ovat auki. Ne ovat liian
    auki. Hänen pupillinsa laajenee ja supistuu nopeammin kuin
    fysiologian pitäisi sallia.

    "Sä oot narkkari," Ingrid sanoo. Se ei ole kysymys. Se on
    diagnoosi joka on myös tunnustus.

    Romppainen on narkkari. Hän on narkkari koska hän on narkkari.
    Tämä on looginen kehä jota narkkaripersoona ei näe.

  participants: ["Romppainen", "Ingrid Falk", "C.G. Jung"]
  terminal: false

  choices:
    - id: "admit_it"
      action: "cooperate"
      player_text: "Myönnä: 'Joo. Mä oon narkkari. Mitä väliksi?'"
      attribute_check:
        attribute: "Charisma"
        difficulty: 2
        success_effect: "Ingrid nyökkää. Tämä on rehellisyyttä jota hän osaa kunnioittaa."
        failure_effect: "Ingrid nyökkää mutta jotain hänen ilmeessään sammuu."
      on_success: "ending"
      on_failure: "ending"
      emits: ["ingrid_trust_tiny"]

    - id: "deflect"
      action: "resist"
      player_text: "Kiellä: 'En mä oo narkkari. Mä oon tutkija. Mä oon täällä tutkimuksessa.'"
      attribute_check:
        attribute: "Charisma"
        difficulty: 3
        success_effect: "Ingrid ei usko, mutta C.G. Jung antaa valheen olla."
        failure_effect: "Ingrid naurahtaa. Se on sama ruma nauru."
      on_success: "ending"
      on_failure: "ending"
      emits: ["ingrid_skeptical"]

    - id: "ask_ingrid_instead"
      action: "approach"
      player_text: "Kysy Ingridiltä: 'Mitä sää oot täällä?'"
      attribute_check:
        attribute: "Awareness"
        difficulty: 2
        success_effect: "Ingrid antaa vastauksen joka on pirstoutunut ja kaunis."
        failure_effect: "Ingrid sulkeutuu. 'Se ei kuulu sulle.'"
      on_success: "ending"
      on_failure: "ending"
      emits: ["ingrid_opened_up"]
```

---

## Kohtaus 4: ENDING

```yaml
node:
  id: "ending"
  purpose: |
    Session päätös. C.G. Jung sulkee simulaation. Ingrid ja Romppainen
    palaavat laboratorion todellisuuteen. Jotain on muuttunut, mutta
    pelaaja ei vielä tiedä mitä.
  situation: |
    C.G. Jung sanoo: "Riittää tänään. Pidätte huolta toisistanne."

    Simulaatio alkaa hajota. Sairaalaseinät muuttuvat harmaaksi,
    sitten valoksi, sitten täksi joka on kaikkialla ja ei missään.

    Ennen kuin kaikki katoaa, Ingrid katsoo Romppaista. Hänen
    kasvonsa on nyt erilainen. Se on microexpression joka kestää
    pisimmän ajan: tunnustus, joka on myös lupaus, joka on myös
    varoitus.

    "Huomenna," Ingrid sanoo. "Huomenna mä kerron susta jotain."

    Sitten pimeys.

    Romppainen herää tuolissa. Hänen suussaan on UFAB 80MG:n
    maku. Hänen päänsä sattuu. Jokin hänen takanaan muistaa
    reunan. Narkkaripersoona ei.

  participants: ["Romppainen", "Ingrid Falk", "C.G. Jung"]
  terminal: true
```

---

## Haarautumiskaavio

```text
DESCENT
  ├──→ RECOGNITION (Kinesics success)
  ├──→ AWKWARD_SILENCE (Kinesics/Rapport fail)
  ├──→ INGRID_LAUGH (Rapport success)
  ├──→ EDGE_OF_SIMULATION (Investigate success)
  └──→ LOST_IN_GREY (Investigate fail)
         │
         └──→ CONVERGENCE
                ├──→ ENDING (admit, Rapport)
                ├──→ ENDING (deflect, Deceive)
                └──→ ENDING (ask Ingrid, Kinesics)
```

Viisi haaraa DESCENTistä, kaikki yhtyvät CONVERGENCEen. Kolme haaraa
CONVERGENCEstä, kaikki johtavat ENDINGiin. Pelaaja kokee yhden päivän
terapiasession, jossa on 2 skill checkiä ja 2 valintaa ilman checkiä.

---

## Ingridin mikroilmeet

Ingridin ilmaisu on tiheä ja laskettu. Hänen ilmaisunsa
perustuu mikroilmeisiin jotka kestävät lyhyemmän ajan kuin ihmisen
näköjärjestelmän pitäisi pystyä havaitseman. Tämä on Noösfäärin
sivuvaikutus: Ingridin tietoisuus vuotaa hänen kasvoihinsa nopeammin
kuin fysiologia sallii.

Käsikirjoituksessa Ingridin mikroilmeet toimivat seuraavasti:

1. DESCENT: tunnistamisen häivähdys (nro 47) — ei hymy, ei irvistys,
   vaan kasvolihaksen liike joka sanoo "minä tunnistan sinun tyyppisi."

2. INGRID_LAUGH: ruma, aito nauru joka purkautuu hänestä kuten
   kaasu tähtien välistä. Hänen kasvonsa murtuu ja rakentuu uudelleen.

3. CONVERGENCE: pupillien laajeneminen joka on nopeampaa kuin
   fysiologian pitäisi sallia. Se on noettinen vuoto.

4. ENDING: tunnustus joka on myös lupaus joka on myös varoitus.
   Pisimmän kestävä microexpression koko sessiossa.

---

## Romppaisen narkkaripersoona

Romppainen on luoteettava, lämminhenkinen ja romanttinen. Leveä hymy,
silmät jotka eivät kaihda mitään, mutta joiden takana pyörii narkkarilogiikkaa
joka ei tiedä olevansa naamiota.

Päivä 1:ssä Romppainen:
- Ei tiedä olevansa Firewallin agentti
- Ei tiedä tehtävästään
- Luulee olevansa oikeasti huumediileri
- Etsii lääkkeitä, keinotekoista kupertamista
- Tuntee epämääräistä tunnetta mutta ei osaa selittää sitä
- Jokin hänen takanaan tietää enemmän (oikea persoona)

Käsikirjoituksessa narkkaripersoona rajoittaa Romppaisen valintoja:
hän ei voi valita "tutki X-Riskiä" tai "raportoi Firewallille". Hän voi
vain valita asioita jotka narkkari valitsisi. Tämä on piilevä
rajoite joka näkyy valintojen teksteissä.

---

## Mitä tämä käsikirjoitus osoittaa

Tämä käsikirjoitus on käytännön esimerkki siitä, miten kaikki 7 päivän
terapiasessiot käsikirjoitetaan:

1. Jokainen kohtaus on TherapyNode jossa on situation, choices ja
   mahdollinen attribute_check.
2. Valinnat ovat abstrakteja toimintaluokkia (approach, observe, talk,
   resist, cooperate, investigate) joiden player_text on konkreettinen.
3. Nykyiset checkit käyttävät Noöpunkin kanonisia attributeja (Awareness,
   Charisma, Intelligence ja Willpower). Tuleva suunnittelusuunta säilyttää myös
   tarkasti rajatut skillit; Attribute + Skill -laskentaa ei ole vielä toteutettu.
4. Haarautuminen on maltillista: DESCENT haarautuu viiteen, jotka
   yhtyvät CONVERGENCEen, joka haarautuu kolmeen, jotka johtavat ENDINGiin.
5. Emits-tagit (ingrid_noticed, noetic_flash, ingrid_trust_tiny jne.)
   valmistelevat tulevaa integraatiota sosiaaliseen graafiin.
6. Ingridin ja Romppaisen suhde kehittyy käsikirjoituksen sisällä ilman
   numerollista suhdejärjestelmää.
7. C.G. Jung toimii terapeuttina joka asettaa kysymyksiä ja luo tilan.
8. Tyylissä yhdistyvät Maniacin surrealismi, Rigetin sairaala tunnelma,
   PKD:n todellisuuden hajoaminen ja Altered Carbonin kyberneettinen
   kylmyys.
