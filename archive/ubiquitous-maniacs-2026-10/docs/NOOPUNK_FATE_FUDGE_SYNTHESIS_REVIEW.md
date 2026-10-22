# Noöpunkin Fate/Fudge-synteesi ja sääntöjen code review

## Johtopäätös

Noöpunkin ei pidä olla Fate Core -hack, Fudge-versio, *Transhumanity's Fate*
-laajennus eikä *Psi-punk*-reskin. Nykyinen v0.1 on perustellusti oma peli,
joka käyttää tuttua 4dF-käyttöliittymää mutta rakentaa sen päälle oman
ontologian, seurausmallin ja graafiarkkitehtuurin.

```text
Fudge             luettava asteikko, 4dF, muokattavat traitit
Fate Core         aspektit, neljä toimintoa, stressi, seuraukset, conceding
Transhumanity's   transhumanistinen Ego/Morph-kehys, mesh, strain,
Fate              psykurgia ja olosuhteisiin sidottu kauhu
Psi-punk          luonnollinen PSI + teknologia, antipsi, mental damage,
                  mind/chip/soul-hacking ja astral traversal
Noöpunk           Psyche, CAN, wu wei, provenance, consent,
                  sosiaaligraafi, monikerroshakkerointi ja ontologinen epävarmuus
```

Perimä pitää nimetä avoimesti, mutta jokainen lainattu mekanismi hyväksytään
vain, jos se palvelee Noöpunkin omaa pelikokemusta.

## 1. Nykyisen moottorin tarkastus

### Korjatut virheet

**Costly success.** Tulostaulukko lupasi etenemisen hinnalla, mutta
`ActionResult.succeeded` hyväksyi vain nollan tai positiivisen marginin. Tämä
esti graafi- ja cross-layer-vaikutukset juuri siinä tuloksessa, jonka piti
edetä. Korjauksen jälkeen costly success:

- antaa soveltaa ansaitun vaikutuksen;
- merkitään `requires_cost=True`;
- ei ole `clean_success`;
- ei itsessään tuota Attack-shiftejä, koska negatiivinen margin antaa edelleen
  nolla shiftiä.

Hinta on valittava fiktiosta: condition, exposure, Trace, Instability, pienempi
vaikutus, menetetty resurssi tai vaikea valinta. Pelkkää vaikutusta ei saa ottaa
ja unohtaa hintaa.

**Concession.** Konfliktista vetäytyminen merkittiin aiemmin täyttämällä stressi,
jolloin tila näytti samalta kuin taken out. Nyt `conceded` ja `taken_out` ovat
erillisiä. Concedannut toimija poistuu konfliktista omalla neuvotellulla
seurauksellaan eikä häntä käsitellä kukistettuna tai toimintakyvyttömänä.

### Tietoiset kevennykset, eivät bugit

- Aspektit ovat v0.1:ssä scripted +1/permission -mekaniikkaa, eivät vielä Fate
  Coren koko invoke/compel-taloutta.
- Stressi on yksi kolmen shiftin kapasiteetti, ei Faten laatikkokaavio.
- Hahmo käyttää attribuuttia ja skilliä yhdessä. Fate Core ja
  *Transhumanity's Fate* käyttävät pääasiassa skilliä; attribuutin lisääminen on
  Noöpunkin/Fudgen suuntainen oma valinta ja vaatii omat vaikeusasteet.
- Psykosurgery- ja projection-API:t ovat tarkoituksella pieniä. Valléen,
  Wendtin ja CANin uusinta metadataa ei lisätä ennen sitä käyttävää kohtausta.
- Day 1:n suorat valinnat eivät tarvitse geneeristä konfliktia tai PSI-moottoria
  vain demonstroidakseen niiden olemassaoloa.

## 2. Fudgelta säilytettävä

Fudgen tärkein vaikutus ei ole yksittäinen taistelusääntö vaan filosofia:
traitit ovat luettavia, asteikko on ihmiskielinen ja järjestelmä muokataan
pelin tarpeeseen.

Säilytetään:

- 4dF:n tiivis, keskelle painottuva jakauma;
- adjective ladder vaikeuksien ja kompetenssin yhteisenä kielenä;
- mahdollisuus käyttää samaa perusresoluutiota eri genreissä;
- kevyt NPC-mallinnus ja fiction-first-adjudikointi;
- scale-käsite myöhemmin morphien, ajoneuvojen, habitaattien ja kollektiivisten
  agenttien vertailuun.

Ei omaksuta sellaisenaan:

- kaikkia vaihtoehtoisia hahmonluonti- ja wound factor -moduuleja;
- GM-kohtaista sääntöjen vaihtelua niin pitkälle, ettei dataohjattu Python-peli
  voi ennustaa tuloksia;
- vapaata trait-sanastoa tuotantodatassa ilman kanonisia rajapintoja.

## 3. Fate Corelta säilytettävä ja muutettava

Säilytetään neljä toimintoa, aspektit fiktion tosina väitteinä, stressin ja
seurausten ero, concession agencyä säilyttävänä tappiona, Fate fractal
instituutioiden mallina sekä fail-forward.

Fate Coren neljän tuloksen sijasta Noöpunk käyttää viittä:

| Noöpunk-tulos | Tehtävä |
|---|---|
| critical success | intentio ja merkittävä lisähyöty |
| success | intentio ilman pakollista hintaa |
| costly success | intentio etenee, mutta hinta on pakollinen |
| failure | intentio ei toteudu, tilanne silti muuttuu |
| catastrophic failure | vakava seuraus, ei narratiivista dead endiä |

Jos narratiivinen valuutta myöhemmin toteutetaan, sen työnimi on **Agency** eikä
automaattisesti Fate point. Agency voidaan käyttää omaan rerolliin, aspektin
aktivointiin tai hinnan uudelleenneuvotteluun. Sitä ansaitaan hyväksymällä oman
aspektin aidosti hankaloittava seuraus. Agencyllä ei saa pakottaa toisen
Psycheä, muuttaa suostumusta jälkikäteen tai julistaa metafyysistä tulkintaa
todeksi. Taloutta ei toteuteta ennen pelitestiä.

## 4. *Transhumanity's Fate* -perintö

Säilytetään 24 skillin lista ja Fate columns, Ego/Morph-erottelu, morph-traitit,
mesh teamwork ja intrusion, contests under fire, async Strain,
psychosurgery-seurausten/aspektien muokkaus sekä kauhu situation aspectina tai
seurauksena.

Noöpunk lisää Psychen, jota ei palauteta datakopioksi. Strain jakautuu Psyche
Loadiin, Noetic Traceen ja Instabilityyn. Psykokirurgia tarvitsee suostumuksen,
provenance-lokin ja avoimen unelma/psykedeeli/VR/PSI-tulkinnan. Backup ei todista
kokemuksellisen jatkuvuuden säilymistä eikä Watts-MacLeod ole PSI:n ainoa lähde.

## 5. *Psi-punk*-perintö

*Psi-punk* on hyödyllisin erikoissääntöjen suunnittelulaboratoriona.

Säilytetään myöhempää toteutusta varten:

- natural PSI ja psychotronic device erillisinä mutta yhteentoimivina;
- laiteprofiili `permission + rating + operator + cost + trace + failure mode`;
- antipsi infrastruktuurina: shielding, consent gate, dampener, decoy,
  pharmacological countermeasure ja provenance logger;
- cracking, psi-jacking, social engineering ja soul-jacking eri
  hyökkäyspintoina saman outer loopin sisällä;
- astral traversal: enter, navigate, encounter, maintain anchor, exit;
- mentaalisten seurausten palaaminen kehoon ja sosiaalisiin suhteisiin.

Ei omaksuta `magic`-terminologiaa, objektiivista Astral Planea bestiaarioineen,
normaalia taktista mind controlia, supervoimakatalogia, diagnoosien käyttämistä
possession-oikotienä eikä Body/Mind/Persona-attribuuttipuuta.

## 6. Noöpunkin oma ydin

Seuraavat osat eivät tule sellaisinaan yhdestäkään neljästä lähteestä:

1. seitsemän attribuuttia ja 24 skillin transhumanistinen profiili;
2. Ego, Morph ja ontologisesti avoin Psyche;
3. Social/Cyber/Physical/Noetic-multilayer graph;
4. PSI trajectory steeringinä seitsemän kontekstiarvon kautta;
5. Wendt-basis, order effects ja read/participate/steer;
6. Vallée-provenance: fyysinen jälki, kokemus, interface ja sosiaalinen vaikutus;
7. consent identity- ja consequence-muutosten mekaanisena rajana;
8. graph effect moduulien välisenä siirtomuotona;
9. relationship history ja -100...+100-dynamiikka;
10. ontologinen sääntö: critical success ei anna kaikkitietävää metafyysistä
    vastausta.

## 7. Vaikeusasteet ja matematiikka

Noöpunk heittää `4dF + attribute + skill + bonus`, joten numerot eivät ole
suoraan Fate Core -yhteensopivia. Kun attribuutti ja skill ovat kumpikin +2,
lähtötaso on +4 ennen noppia.

| Tilanne | Suuntaa-antava vaikeus |
|---|---:|
| osaamattomallekin mahdollinen | +1...+2 |
| koulutetun normaali haaste | +3...+4 |
| asiantuntijan todellinen haaste | +5...+6 |
| institutionaalisesti suojattu tai erittäin vaikea | +7...+8 |
| lähes mahdoton ilman advantagea tai avointa trajectorya | +9 tai enemmän |

Vaikeus määritetään fiktiivisestä vastuksesta, sitten todennäköisyys
tarkistetaan. Saman asian tag, aspect, specialization ja stunt eivät saa antaa
neljää päällekkäistä bonusta.

## 8. Seuraava toteutusjärjestys

1. **Valmis nyt:** costly success ja concession korjattiin sekä testattiin.
2. **Seuraavan PSI-kohtauksen yhteydessä:** lisää action frame, johon kirjataan
   basis, read/participate/steer, intention, trajectory ja institutional field.
3. **Ensimmäisen psychotronic gear -kohtauksen yhteydessä:** ota käyttöön pieni
   operaattoririippuvainen device profile ja antipsi-vastatoimi.
4. **Ensimmäisen täyden konfliktin yhteydessä:** lisää stressin kuittaus,
   consequence-slotit, recovery ja neuvotellut concession stakes.
5. **Kun aspektit tarvitsevat pelaajavaltaa:** prototypoi Agency-talous erillisillä
   testeillä.
6. **Kun NHI-encounter tulee peliin:** toteuta Valléen protokollasta vain
   kohtauksen käyttämät provenance-kentät.
7. **Vasta pelitestien jälkeen:** arvioi scale, wealth ja contests under fire.

## Lähteet

- O'Sullivan, Steffan. *Fudge: Freeform Universal Do-it-yourself Gaming Engine*.
- Balsera, Leonard et al. 2013. *Fate Core System*. Evil Hat Productions.
- Macklin, Ryan & Jack Graham. 2016. *Eclipse Phase: Transhumanity's Fate*.
  Posthuman Studios.
- Wood, Jacob. 2013/2015. *Psi-punk*, v1.2. Accessible Games.

