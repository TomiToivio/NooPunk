# Terapiasessio 01: Vain yksi potilas

> **Status:** Ei-kanoninen agenttiehdotus. Ihmisen määrittämä ensimmäisen terapiasession kanoninen pääjuoni on dokumentissa `docs/THERAPY_DAY_1_MAIN_PLOT.md`. Tätä tiedostoa ei käytetä toteutuksen juonilähteenä, mutta sen yksittäisiä esitystapoja voidaan myöhemmin arvioida erikseen.

## Session metadata

```yaml
therapy_session:
  id: therapy_day_01_only_one_patient
  day: 1
  title: "Vain yksi potilas"
  location: "C.G. Jung -instituutin yhteinen Noösfääri-istunto"
  player_character: "Tohtori Romppainen / Sven-Olof"
  central_npc: "Ingrid Falk"
  romppainen_phase: "narkkaripersoona hallitsee"
  structure: "A -> B tai C -> D -> epilogi"
  estimated_duration: "25–40 minuuttia"
  mechanics_in_scope: [choices, social_interaction, skill_checks, fate_dice]
  mechanics_deferred: [relationship_scores, stress, consequences, fate_points,
                       aspects, social_graph, psi_rules]
```

Tämä dokumentti toimii sekä päivän 1 sisältöehdotuksena että mallina muiden
kuuden päivän kirjoittamiselle. Session tapahtumat ovat totta hahmojen
kokemuksena, mutta niiden ulkoinen ontologia jätetään avoimeksi: kyse voi olla
terapiasimulaatiosta, kahden egon tahattomasta lomittumisesta, C.G. Jungin
manipulaatiosta tai Noösfäärin aidosta ilmiöstä.

## Tyylillinen ohjaus

Tavoiteltu yhdistelmä on lämmin ja tuskallinen absurdismi, sairaalabyrokratian
painajainen, horjuva todellisuus sekä ruumiin ja identiteetin transhumanistinen
noir. Huumori ei mitätöi kipua, eikä romanssi paranna hahmoja yhdessä
kohtauksessa.

Ingridin näyttelijäohjeessa on sähköinen
haavoittuvuus: tunne ehtii kasvoille, yrittää naamioitua vitsiksi ja vuotaa
sitten takaisin näkyviin. Romppaisen näyttelijäohjeessa on vino karisma: hymy näyttää tietävän enemmän kuin mies,
jonka kasvoilla se on.

"Planckin ajan tarkkuus" toteutetaan käsikirjoituksen runollisena
mikroilmenotaationa. Aikaleimat eivät väitä, että kasvolihakset todella liikkuvat
Planckin ajassa; ne ohjaavat näyttelijän reaktion sisäistä järjestystä.

## Taitotarkistuksen esitystapa

Kun valinnassa on tarkistus:

```text
heitä 4dF + hahmolomakkeen skill-arvo vastaan vaikeus
```

Neljä Fate-noppaa tuottavat kukin `-`, `0` tai `+` eli yhteensä −4…+4.

| Erotus vaikeuteen | Tulos tässä käsikirjoituksessa |
|---|---|
| alle 0 | failure |
| 0 | tie |
| 1–2 | success |
| 3+ | success with style |

Tässä ensimmäisessä versiossa tie käyttää valinnan yhteydessä erikseen
kirjoitettua kompromissia. Kaikki tulokset jatkavat tarinaa. Skill-arvoa ei
kovakoodata sessioon, vaan se luetaan myöhemmin Romppaisen hahmolomakkeelta.

## Session kulku

```text
A. Väärä odotushuone
├─ onnistunut yhteinen huijaus tai hellä lähestyminen -> B. Kahden hengen hissi
└─ epäonnistuminen, uhma tai lääkkeiden tavoittelu   -> C. Riget-käytävä
                                      \             /
                                   D. Yksi tosi asia
                                           |
                                       epilogi
```

---

## Node A: Väärä odotushuone

```yaml
id: d1_a_waiting_room
purpose: "Aseta yhteinen ongelma ja anna pelaajan määrittää ensimmäinen ele Ingridiä kohti."
participants: [Romppainen, Ingrid Falk, C.G. Jungin kuulutusääni]
terminal: false
```

### Tilanne

Romppainen herää sairaalan odotushuoneessa, joka on rakennettu 1970-luvun
muistosta tulevaisuuden materiaaleilla. Muovituolit hikoilevat. Seinän
hakulaite näyttää vuorotellen numeroa `0`, sanaa `ÄITI` ja Romppaisen kasvoja
kuusi sekuntia vanhempina.

Ingrid istuu vastapäätä paljain jaloin, vaikka lattia on terästä. Hänellä on
paperinen jonotusnumero `2`. Romppaisen käteen on niitattu numero `1`.

Kaiutin naksahtaa:

> **C.G. JUNG:** Potilas numero yksi voi tulla sisään. Potilas numero kaksi on
> potilaan numero yksi defenssi, eikä tarvitse erillistä hoitoa.

Ingrid katsoo lappuaan, Romppaista ja sitten kattoon.

### Ingridin mikroilme

```text
t+0 Planck: vasen suupieli valmistautuu pilkkaan.
t+1 Planck: silmien alla käy paljas kysymys: "Entä jos minä en ole oikea?"
t+2 Planck: kysymys haudataan oikean kulmakarvan millimetrin nousuun.
t+3 Planck: hän päättää tehdä Romppaisesta rikoskumppanin ennen kuin ehtii
            pyytää tältä lohtua.
```

> **INGRID:** Kumman meistä luulet olevan toisen oire?

Romppaisen vino hymy saapuu hetkeä ennen vastausta, kuin hänen kasvolihaksensa
olisivat saaneet poliisiraportin, jota hänen tietoisuudelleen ei toimitettu.

### Valinta A1 — "Meillä on sama ajanvaraus"

```yaml
action: deceive
player_text: "Vilauta lappuja päällekkäin. Väitä, että numero on 12."
check: "Deceive + 4dF vs Fair (+2)"
```

- **Failure:** Kaiutin ilmoittaa Romppaisen valehtelevan. Ingrid purskahtaa
  nauruun juuri liian kovaa, koska pelästyi. Siirry nodeen C. Tagit:
  `jung_detects_bad_lie`, `ingrid_laughs_with_romppainen`.
- **Tie:** Ovi hyväksyy numeron 12 mutta kutsuu heitä aviopariksi. Ingrid sanoo
  "älä innostu" ennen kuin Romppainen ehtii innostua. Siirry nodeen B. Tagit:
  `system_mislabels_pair`, `romantic_embarrassment`.
- **Success:** Ingrid tajuaa huijauksen kesken Romppaisen lauseen ja täydentää
  sen saumattomasti. Siirry nodeen B. Tagit: `shared_improvised_lie`.
- **Success with style:** He vastaavat yhtä aikaa eri valheen, jotka järjestelmä
  yhdistää täydelliseksi byrokraattiseksi totuudeksi. Ingrid hihittää kämmeneensä.
  Siirry nodeen B. Tagit: `synchronized_deception`, `noosphere_echo_possible`.

### Valinta A2 — "Jos olet minun oireeni, olet paras tähän asti"

```yaml
action: approach
player_text: "Vastaa rehellisellä vitsillä ja tarjoa Ingridille kätesi."
check: "Persuade + 4dF vs Fair (+2)"
```

- **Failure:** Repliikki kuulostaa iskuyritykseltä. Ingrid ei tartu käteen,
  mutta työntää oman jonotusnumeronsa Romppaisen kämmenelle: "Pidä edes tätä."
  Siirry nodeen C. Tagit: `ingrid_sets_boundary`, `paper_token_shared`.
- **Tie:** Ingrid tarttuu vain Romppaisen pikkusormeen. Siirry nodeen B. Tagit:
  `pinky_contact`, `ingrid_cautious_tenderness`.
- **Success:** Ingrid ottaa kädestä ja sanoo: "Tuo oli hirveä. Sano toinen."
  Siirry nodeen B. Tagit: `hand_contact`, `ingrid_requests_more`.
- **Success with style:** Ingrid yrittää pyöräyttää silmiään mutta hymy ehtii
  ensin. Hän puristaa kättä kerran, heidän väliseksi salamerkiksi. Siirry B.
  Tagit: `hand_signal_created`, `mutual_romantic_recognition`.

### Valinta A3 — "Onko oireilla lääkekaappia?"

```yaml
action: narcotic_hedonism
player_text: "Ohita identiteettikysymys ja etsi odotushuoneesta lääkkeitä."
check: null
next: d1_c_riget_corridor
```

Romppainen repii seinästä ensiapukaapin. Sen sisällä on vain pieni kirkonkello,
joka alkaa soida. Ingrid auttaa häntä repimään toisen kaapin, vaikka väittää
ettei auta. Tagit: `shared_bad_idea`, `narcotic_shadow_visible`.

---

## Node B: Kahden hengen hissi

```yaml
id: d1_b_elevator
purpose: "Palkitse yhteistyö läheisyydellä ja testaa, kuuleeko Romppainen Ingridin pelon vitsin alta."
participants: [Romppainen, Ingrid Falk, hissin terapeuttinen käyttöliittymä]
terminal: false
```

### Tilanne

Ovi johtaa hissiin, joka on sisältä liian pieni kahdelle mutta sulkeutuu silti.
He joutuvat rinta rintaa vasten. Hissin kerrosnapit ovat `MINÄ`, `ÄITI`,
`POLIISI`, `EI KUKAAN` ja `KAHVIO`.

Romppainen ei tiedä, miksi `POLIISI` saa hänen leukansa kiristymään. Ingrid
huomaa sen.

> **INGRID:** Jos painat "ÄITI", minä puren.
>
> **ROMPPAINEN:** Entä kahvio?
>
> **INGRID:** Sitten minä saatan purra kohteliaasti.

### Ingridin mikroilme

```text
t+0 Planck: flirtti sytyttää silmiin kaksi pilkallista valoa.
t+1 Planck: hissin ahtaus muuttaa hengityksen liian matalaksi.
t+2 Planck: hän tarkistaa huomasiko Romppainen.
t+3 Planck: hän vihaa sitä, että toivoo Romppaisen huomanneen.
```

### Valinta B1 — Huomaa, mitä vitsi peittää

```yaml
action: observe
player_text: "Lopeta flirtti hetkeksi. Kysy Ingridiltä, haluaako hän oven auki."
check: "Kinesics + 4dF vs Good (+3)"
```

- **Failure:** Romppainen tulkitsee pelon inhoksi ja perääntyy mahdottomassa
  tilassa, lyöden takaraivonsa nappiin `POLIISI`. Ingrid nappaa hänet kiinni.
  Tagit: `romppainen_misreads_ingrid`, `police_button_activated`.
- **Tie:** Ingrid kieltää pelkäävänsä, mutta pyytää jättämään oven raolleen.
  Romppainen tekee niin. Tagit: `fear_denied_need_respected`.
- **Success:** Ingrid sanoo hiljaa "älä avaa, mutta älä päästä irti". Tagit:
  `ingrid_states_need`, `romppainen_respects_need`.
- **Success with style:** Romppainen kysyy ennen kuin Ingrid ehtii naamioida
  hengityksensä. Hänen kasvonsa käyvät täysin puolustamattomina ja palautuvat
  sitten ilkikurisiksi. Tagit: `romppainen_sees_microfear`, `ingrid_feels_seen`.

Kaikki tulokset johtavat nodeen D.

### Valinta B2 — Tee ahtaudesta yhteinen vitsi

```yaml
action: talk
player_text: "Väitä hissille, että läheisyys rikkoo potilasturvallisuusmääräyksiä."
check: "Provoke + 4dF vs Average (+1)"
```

- **Failure:** Hissi pyytää heitä täyttämään seksuaalisen häirinnän lomakkeen
  yhdessä samalla kynällä. Ingrid: "Minä kirjoitan käsialasi." Tagit:
  `bureaucratic_intimacy`, `ingrid_takes_control`.
- **Tie:** Hissi antaa viisi senttiä lisää tilaa vain heidän kasvojensa väliin.
  He alkavat nauraa. Tagit: `shared_laughter_under_pressure`.
- **Success:** Hissi pahoittelee ja soittaa halpaa romanttista musiikkia.
  Molemmat protestoivat liian nopeasti. Tagit: `mutual_denial`, `romantic_score`.
- **Success with style:** Ingrid jatkaa valitusta täydellisellä virastokielellä,
  kunnes hissi avaa oven häpeissään. Tagit: `comedy_duet`, `ingrid_romppainen_team`.

Kaikki tulokset johtavat nodeen D.

### Valinta B3 — Paina `POLIISI`

```yaml
action: investigate
player_text: "Paina nappia, vaikka et tiedä miksi se tuntuu omalta nimeltäsi."
check: "Willpower + 4dF vs Good (+3)"
```

- **Failure:** Romppainen vetää kätensä pois kuin nappi olisi polttanut.
  Ingrid peittää reaktion asettamalla oman sormensa hänen sormensa päälle.
  Tagit: `police_reflex_pain`, `ingrid_covers_romppainen`.
- **Tie:** Nappi sanoo Romppaisen äänellä "ei vielä". Ingrid kuulee vain
  hissimusiikin. Tagit: `romppainen_hears_self`, `perception_asymmetry`.
- **Success:** Hissi välähtää hetkeksi kuulusteluhuoneeksi. Romppainen huomaa
  uloskäynnit automaattisesti mutta ei ymmärrä taitoaan. Tagit:
  `police_instinct_leak`, `romppainen_notices_exits`.
- **Success with style:** Romppainen sanoo vaistomaisesti "älä vastaa mihinkään"
  juuri ennen kuin tuntematon ääni kysyy Ingridin nimeä. Tagit:
  `romppainen_protective_reflex`, `firewall_identity_foreshadowed`.

Kaikki tulokset johtavat nodeen D.

---

## Node C: Riget-käytävä

```yaml
id: d1_c_riget_corridor
purpose: "Muuta epäonnistuminen tai hedonismi yhteiseksi koettelemukseksi."
participants: [Romppainen, Ingrid Falk, vahtimestari jolla ei ole kasvoja]
terminal: false
```

### Tilanne

Odotushuoneen lattia kallistuu sairaalakäytäväksi. Pyörätuolit liikkuvat
vastatuuleen ilman potilaita. Seinästä kuuluu vauvan itkua; seinä pyytää
anteeksi ja vaihtaa äänen kopiokoneeksi.

Kasvoton vahtimestari kantaa tarjotinta, jolla on yksi valkoinen pilleri ja
kaksi vesilasia.

> **VAHTIMESTARI:** Lääke riittää yhdelle todelliselle ihmiselle.
>
> **INGRID:** Hyvä. Minä olen aina halunnut seurustella oireen kanssa.

Sana *seurustella* karkaa Ingridiltä vahingossa. Hän puree poskensa sisäpintaa
kuin voisi vetää sanan takaisin verenkierrosta.

### Ingridin mikroilme

```text
t+0 Planck: "seurustella" ylittää huulten tullirajan.
t+1 Planck: pupillit laajenevat syyllisinä.
t+2 Planck: nenänpieli valmistaa halveksivan naamion.
t+3 Planck: naamio epäonnistuu, koska Romppainen näyttää liian ilahtuneelta.
t+4 Planck: Ingrid alkaa nauraa omalle katastrofilleen.
```

### Valinta C1 — Jaa mahdoton pilleri

```yaml
action: cooperate
player_text: "Pure pilleri kahtia ja anna Ingridin valita puolikas."
check: null
next: d1_d_one_true_thing
```

Pillerin sisältä löytyy pienempi pilleri, jonka sisältä löytyy vielä pienempi.
He jatkavat jakamista, kunnes molemmat nauravat lattialla. Tagit:
`shared_absurd_ritual`, `romantic_word_slipped`.

### Valinta C2 — Selvitä kumpi lasi valehtelee

```yaml
action: investigate
player_text: "Tutki vahtimestarin eleitä ja valitse Ingridille turvallinen lasi."
check: "Kinesics + 4dF vs Fair (+2)"
```

- **Failure:** Molemmat lasit ovat kuivia. Ingrid juo silti omastaan ja sanoo
  "erinomainen vuosikerta" pelastaakseen Romppaisen noloudelta. Tagit:
  `ingrid_protects_romppainen_pride`.
- **Tie:** Romppainen tunnistaa ansan mutta Ingrid vaihtaa lasit viime hetkellä.
  Kumpikaan ei tiedä, kumpi suojeli kumpaa. Tagit: `mutual_protection_ambiguous`.
- **Success:** Romppainen näkee vahtimestarin olemattoman käden mikroliikkeen ja
  antaa Ingridille turvallisen lasin. Tagit: `romppainen_protects_ingrid`.
- **Success with style:** Romppainen pakottaa vahtimestarin juomaan ensin
  pelkällä katseella, jota ei itse tunnista poliisin katseeksi. Ingrid kuiskaa:
  "Sinä olet kamala. Tee se uudestaan." Tagit: `police_instinct_attractive`,
  `ingrid_intrigued_not_trusting`.

Kaikki tulokset johtavat nodeen D.

### Valinta C3 — Ota lääke itsellesi

```yaml
action: narcotic_hedonism
player_text: "Nielaise pilleri ennen kuin kukaan ehtii estää."
check: "Deceive + 4dF vs Ingridin Kinesics; käytä vastustajan arvoa"
```

- **Failure:** Ingrid nappaa pillerin Romppaisen kieleltä kahdella sormella ja
  heittää sen pois. Ele on intiimi, raivostunut ja hoivaava. Tagit:
  `ingrid_interrupts_compulsion`, `romppainen_boundary_crossed`.
- **Tie:** Pilleri jää heidän väliinsä, koska Ingrid yrittää samaa. He alkavat
  nauraa kauhistuneina omalle samanlaisuudelleen. Tagit: `shared_addict_shadow`.
- **Success:** Romppainen nielee pillerin. Se maistuu paperilta eikä tee mitään.
  Ingrid loukkaantuu enemmän salailusta kuin lääkkeestä. Tagit:
  `romppainen_chooses_drug_over_ingrid`, `ingrid_hurt_hidden`.
- **Success with style:** Huijaus onnistuu täydellisesti, mutta pilleri kuiskaa
  Ingridin äänellä "tiesin silti". Tagit: `perfect_lie_empty_reward`,
  `ingrid_internalized_voice`.

Kaikki tulokset johtavat nodeen D. Tämä haara on tarkoituksella romanttisesti
tuskallinen eikä anna riippuvuudesta palkitsevaa oikotietä.

---

## Node D: Yksi tosi asia

```yaml
id: d1_d_one_true_thing
purpose: "Yhdistä haarat ja päätä sessio pieneen vastavuoroiseen paljastukseen."
participants: [Romppainen, Ingrid Falk, C.G. Jungin kuulutusääni]
terminal: false
```

### Tilanne

Hissi tai käytävä avautuu pieneen sairaalahuoneeseen. Huoneessa on yksi sänky,
kaksi tyynyä ja ikkuna, jonka takana 16 Psyche näkyy ulkopuolelta — vaikka he
ovat asteroidin sisällä.

Kaiutin sanoo:

> **C.G. JUNG:** Hoito päättyy, kun toinen teistä kertoo yhden toden asian.
> Vain yksi tarvitsee kertoa. Toinen voidaan poistaa.

Ingrid istuu sängyn reunalle. Ensimmäistä kertaa hän ei rakenna ilmettään
valmiiksi.

> **INGRID:** Minä en tiedä, haluanko sinun olevan oikea. Jos olet, voit lähteä.

Romppainen ei muista Firewallia eikä tehtäväänsä. Pelaajan totuus voi koskea
vain sitä, minkä hänen nykyinen persoonansa todella tietää.

### Valinta D1 — "En tiedä kuka olen"

```yaml
action: confess
player_text: "Myönnä, ettet tiedä kuka olet — ja että Ingrid tuntuu silti tutulta."
check: "Willpower + 4dF vs Fair (+2)"
```

- **Failure:** Tunnustus hajoaa vitsiksi puolivälissä. Ingrid ymmärtää silti ja
  vastaa: "Hyvä. Minäkään en olisi uskonut vakavaa versiota." Tagit:
  `truth_hidden_in_joke`.
- **Tie:** Romppainen sanoo vain ensimmäisen puolikkaan. Ingrid täydentää:
  "Mutta minut tunnistat." Tagit: `ingrid_completes_confession`.
- **Success:** Romppainen sanoo koko totuuden. Ingrid nojautuu olkapäähän:
  "Se on todella huono henkilöllisyystodistus." Tagit: `mutual_vulnerability`.
- **Success with style:** Tunnustus saa huoneen ikkunan säröilemään. Hetken he
  näkevät kaksi kehoa erillisissä terapiakapseleissa pitämässä käsiä tyhjyyden
  läpi. Tagit: `shared_reality_glimpse`, `simulation_boundary_seen`.

### Valinta D2 — "Sinä pelkäät, että jätän sinut"

```yaml
action: observe
player_text: "Sano ääneen Ingridin pelko ja lupaa vain, ettet lähde vielä."
check: "Kinesics + 4dF vs Good (+3)"
```

- **Failure:** Romppainen osuu liian lähelle ja liian kovaa. Ingrid läimäyttää
  häntä tyynyllä, sitten pitää tyynyä heidän välissään. Tagit:
  `truth_without_tact`, `ingrid_defensive_closeness`.
- **Tie:** Ingrid kiistää väitteen mutta siirtyy lähemmäs. Tagit:
  `body_contradicts_words`.
- **Success:** Ingrid vastaa: "En minä sitä pelkää. Minä vihaan sitä etukäteen."
  Romppainen lupaa jäädä tämän istunnon loppuun. Tagit: `limited_promise_kept`.
- **Success with style:** Ingridin pilkallinen ilme ehtii syntyä ja sammua ennen
  kuin se peittää mitään. Hän sanoo vain "okei". Tagit:
  `ingrid_drops_mask`, `romppainen_names_abandonment_fear`.

### Valinta D3 — "Minä haluan lisää lääkettä"

```yaml
action: narcotic_hedonism
player_text: "Kerro ainoa totuus, jonka Sven-Olof pystyy varmasti tunnistamaan."
check: null
```

Ingrid nauraa ensin, sitten silmät kostuvat vastoin hänen tahtoaan.

> **INGRID:** Minäkin. Voi helvetti. Minäkin.

Heidän välillään on ensimmäinen täysin rehellinen mutta vaarallinen yhteys.
Tagit: `shared_addiction_truth`, `shadow_resonance`, `honesty_without_healing`.

Kaikki valinnat siirtyvät epilogiin.

---

## Epilogi: Herääminen erillään

Kuva katkeaa ennen kuin C.G. Jung vahvistaa vastauksen oikeaksi. Romppainen
herää omassa terapiakapselissaan. Ingrid on fyysisesti toisessa huoneessa.

Romppaisen oikeassa kädessä on paperinen jonotusnumero `2`, vaikka mitään
paperia ei viety simulaatioon.

Seinän läpi kuuluu kolme koputusta. Tauko. Yksi koputus.

Jos tagi `hand_signal_created` syntyi, rytmi on täsmälleen Ingridin aiempi
salamerkki. Muuten Romppainen ei tiedä, onko ääni Ingrid, putkisto vai hänen
oma sydämensä väärässä seinässä.

### Viimeinen mikroilme, Ingridin puolella seinää

```text
t+0 Planck: hän nostaa kätensä koputtaakseen uudelleen.
t+1 Planck: ylpeys pysäyttää käden.
t+2 Planck: toivo voittaa ylpeyden niukasti.
t+3 Planck: hän koputtaa kerran ja hymyilee kuin olisi juuri tehnyt rikoksen.
```

## Session tuottamat jatkuvuustiedot

Tässä vaiheessa peli vain kirjaa syntyneet tagit. Se ei laske romanssi-, trust-
tai affinity-pisteitä. Päivien 2–7 kirjoittaja voi kysyä tageista esimerkiksi:

```yaml
continuity_examples:
  - hand_signal_created
  - shared_improvised_lie
  - ingrid_feels_seen
  - police_instinct_leak
  - shared_addict_shadow
  - mutual_vulnerability
  - shared_reality_glimpse
```

Yksi session havainto on mahdollisesti tosi: Ingrid ja Romppainen kokivat saman
tilan. Kaksi epävarmuutta syntyy: rakensiko C.G. Jung kokemuksen tarkoituksella,
ja miten fyysinen paperilappu päätyi Romppaisen käteen?

## Seitsemän päivän kirjoitusformaatti

Seuraavat sessiot käyttävät samaa järjestystä:

1. `Session metadata`: päivä, identiteettivaihe, teema ja rajatut mekaniikat.
2. `Continuity input`: aiempien päivien tagit, joita sessio voi huomioida.
3. `Session map`: pieni haarautuva kartta, joka yhdistyy takaisin.
4. `TherapyNode`: tarkoitus, tilanne, mikroilmeet ja osallistujat.
5. `Choice`: pelaajateksti, taito, 4dF-vaikeus ja kaikki neljä tulosta.
6. `Epilogue`: yhteinen lopetus, joka kantaa seuraavaan päivän osaan.
7. `Continuity output`: vain nimetyt tapahtumatagit.
8. `Truth and uncertainties`: yksi pieni tosi asia ja kaksi uutta kysymystä.

Tämä pitää seitsemän päivän kokonaisuuden vertailukelpoisena mutta sallii
jokaiselle päivälle oman visuaalisen logiikan, emotionaalisen kysymyksen ja
Romppaisen vähitellen avautuvat toimintamoodit.
