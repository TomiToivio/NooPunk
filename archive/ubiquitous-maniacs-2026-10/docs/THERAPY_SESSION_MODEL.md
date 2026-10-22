# Päivä 1: terapiasession pelimalli

## Dokumentin tarkoitus

Tämä dokumentti määrittelee Noösfäärissä tapahtuvan terapiasession pienimmän
käyttökelpoisen pelimallin sekä lomakkeen, jolla ensimmäisen päivän
käsikirjoitus voidaan myöhemmin kirjoittaa.

Tässä vaiheessa ei kirjoiteta juonta, kohtauksia, dialogia, symboleja,
varsinaisia pelaajavalintoja tai tapahtumasisältöä. Mallia ei toteuteta koodina
eikä integroida sosiaaliseen graafiin tai muihin pelijärjestelmiin.

## Skenaarion reunaehdot

- Maailma on Noöpunkin oma epätasaisesti toipuva post-Fall-aurinkokunta: Maa
  säilyi mutta fragmentoitui, ja avaruusihmiskunta divergoituu yhä
  transhumanistisemmaksi. Eclipse Phase on sääntö- ja vaikutelähde, ei kaanon.
- Pelijärjestelmä on Transhumanity's Fate.
- Tapahtumapaikka on 16 Psychen C.G. Jung University / Institute.
- Romppainen on Firewallin agentti, joka on soluttautunut koekaniiniksi
  mahdollisen X-Riskin vuoksi.
- Päivänä 1 Romppainen toimii kokonaan psykokirurgisesti tuotetun
  huumediileri-/narkkarisivupersoonansa kautta. Hän ei tiedä tehtäväänsä tai
  Firewall-identiteettiään.
- Ingrid Falk ja Romppainen ovat session keskushahmot. Mallin pitää sallia
  heidän vuorovaikutuksensa seuraukset, mutta se ei sisällä suhdepisteitä,
  trust- tai affinity-arvoja eikä sosiaaligraafin edgejä.

## Suunnitteluperiaate

Citizen Sleeper -vaikutus näkyy rajattuina, merkityksellisinä valintoina:

- Pelaaja näkee kerrallaan yhden tilanteen ja pienen määrän toimintatapoja.
- Valinta kertoo, mitä Romppainen yrittää, mutta ei kaikkia seurauksia.
- Osa valinnoista onnistuu suoraan ja osa vaatii skill checkin.
- Skill check voi muuttaa seuraavaa nodea tai samassa nodessa syntyvää seurausta.
- Epäonnistuminen vie tarinaa eteenpäin; se ei muodosta umpikujaa.
- Haarat yhdistyvät pian uudelleen, jotta käsikirjoitus pysyy hallittavana.

## Minimaalinen pelisilmukka

1. Näytä nykyisen `TherapyNode`-solmun tilannekuvaus.
2. Näytä 2–3 siihen kuuluvaa `Choice`-toimintavaihtoehtoa.
3. Pelaaja valitsee yhden vaihtoehdon.
4. Jos vaihtoehdossa on `AttributeCheck`, ratkaise se Noöpunkin kanonisella
   attributella ja valitulla Fate-menetelmällä.
5. Valinnan ja mahdollisen tarkistuksen tulos määrää seuraavan noden.
6. Toista, kunnes saavutetaan session päättävä node.

## Käsitteellinen tietomalli

### TherapySession

Yksi päivän sisäinen terapiasessio.

| Kenttä | Tarkoitus |
|---|---|
| `id` | Session yksilöllinen tunniste |
| `day` | Pelipäivä |
| `start_node` | Ensimmäisen noden tunniste |
| `nodes` | Session `TherapyNode`-solmut |

### TherapyNode

Yksi tilanne, päätöspiste tai session lopetus.

| Kenttä | Tarkoitus |
|---|---|
| `id` | Noden yksilöllinen tunniste |
| `purpose` | Käsikirjoittajalle: noden tehtävä sessiossa |
| `situation` | Pelaajalle myöhemmin kirjoitettava tilannekuvaus |
| `participants` | Läsnä olevat hahmot, esimerkiksi Romppainen ja Ingrid |
| `choices` | Noden 2–3 toimintavaihtoehtoa |
| `terminal` | Päättääkö node session |

### Choice

Pelaajan valitsema toimintatapa. Valinnan tekstin pitää ilmaista yritys, ei
luvata lopputulosta.

| Kenttä | Tarkoitus |
|---|---|
| `id` | Valinnan tunniste |
| `action` | Abstrakti toimintaluokka, kuten approach, observe tai resist |
| `player_text` | Myöhemmin kirjoitettava pelaajalle näkyvä valinta |
| `attribute_check` | Valinnainen `AttributeCheck` |
| `next` | Seuraava node, jos tarkistusta ei ole |
| `on_success` | Seuraava node onnistumisesta |
| `on_failure` | Seuraava node epäonnistumisesta |
| `emits` | Valinnaiset tapahtumat myöhempää integraatiota varten |

Ensimmäisessä versiossa `emits` vain nimeää mahdollisen tapahtuman. Se ei muuta
suhdetta, hahmoa tai muuta järjestelmää.

### AttributeCheck

Nykyinen AttributeCheck viittaa yhteen Noöpunkin seitsemästä kanonisesta
attributesta ja vaikeuteen. Tuleva suunnittelusuunta säilyttää myös tarkasti
rajatut skillit; niiden yhdistämistä attributeihin ei ole vielä toteutettu.

| Kenttä | Tarkoitus |
|---|---|
| `attribute` | Testattava Noöpunk-attribute |
| `difficulty` | Tarkistuksen vaikeus |
| `success_effect` | Mitä onnistuminen muuttaa tässä sessiossa |
| `failure_effect` | Mitä epäonnistuminen muuttaa tässä sessiossa |

Faten tarkemmat tulostasot voidaan käsikirjoituksessa kuvata vivahteina, mutta
minimimallin haaroitus tarvitsee vain onnistumis- ja epäonnistumiskohteen.

## Haarautumisen tavoitemuoto

Ensimmäisen päivän käsikirjoitus suunnitellaan pienenä timanttina:

```text
Start
  |
Node A
 /    \
Node B  Node C
 \      /
  Node D
    |
   End
```

Node A sisältää keskeisen valinnan tai skill checkin. Node B ja Node C näyttävät
eri seurauksen. Molemmat palaavat Node D:hen, joten sessio voi reagoida pelaajan
toimintaan ilman nopeasti kasvavaa haarapuuta.

## Päivä 1:n käsikirjoituslomake

Hakasulkeet ovat tyhjiä paikanvaraajia, eivät terapiasession sisältöä.

```yaml
therapy_session:
  id: "[session_id]"
  day: 1
  start_node: "[node_id]"

  nodes:
    - id: "[node_id]"
      purpose: "[noden dramaturginen tai pelillinen tehtävä]"
      situation: "[myöhemmin kirjoitettava tilanteen kuvaus]"
      participants: ["Romppainen", "Ingrid Falk"]
      romppainen_constraint: "[mitä dissosioitunut persoona voi tietää]"
      terminal: false

      choices:
        - id: "[choice_id]"
          action: "[approach | observe | talk | resist | cooperate | investigate]"
          player_text: "[myöhemmin kirjoitettava toimintavaihtoehto]"
          attribute_check:
            attribute: "[Noöpunk-attribute]"
            difficulty: "[vaikeus]"
            success_effect: "[abstrakti seuraus]"
            failure_effect: "[abstrakti seuraus]"
          on_success: "[node_id]"
          on_failure: "[node_id]"
          emits: ["[valinnainen tuleva tapahtuma]"]
```

Tarkistuksettomasta valinnasta jätetään `attribute_check`, `on_success` ja
`on_failure` pois ja käytetään yhtä `next`-kohdetta.

## Käsikirjoittajan tarkistuslista

- Sisältääkö jokainen tavallinen node 2–3 aidosti erilaista toimintatapaa?
- Tietääkö pelaaja, mitä hän yrittää, mutta ei kaikkia seurauksia?
- Käyttääkö jokainen check Transhumanity's Faten olemassa olevaa skilliä?
- Jatkavatko sekä onnistuminen että epäonnistuminen sessiota?
- Yhdistyvätkö haarat takaisin viimeistään yhden välivaiheen jälkeen?
- Rajoittaako Romppaisen dissosiaatio johdonmukaisesti hänen tietojaan?
- Voiko Ingrid–Romppainen-vuorovaikutus tuottaa myöhemmin käsiteltävän
  tapahtuman ilman suhdepisteitä tai graafimuutoksia?
- Onko kaikki varsinainen juoni ja dialogi jätetty seuraavaan työvaiheeseen?

## Myöhempään työvaiheeseen jätetty

- ensimmäisen päivän varsinainen käsikirjoitus ja dialogi
- session visuaaliset, symboliset ja noettiset sisällöt
- skillien ja vaikeuksien valinta
- tapahtumien pysyvä tallennus
- Ingridin ja Romppaisen suhdejärjestelmä
- sosiaaligraafi- ja main quest -integraatiot
- käyttöliittymä, nopanheitot ja ohjelmakoodi
