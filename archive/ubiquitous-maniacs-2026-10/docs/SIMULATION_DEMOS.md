# Simulaatiodemot

Projektissa on kolme käyttöliittymäkerrosta:

1. narratiivinen RPG (`src/rpg`, `app.py`);
2. autonominen sosiaalinen simulaatio (`src/social/simulation.py`, `social_demo.py`);
3. kyberneettis–psykotroninen hakkerointi (`src/hacking`, `hacking_demo.py`).

Sosiaalinen simulaatio pysyy itsenäisenä kokeena. Hacking-demo käyttää nyt saman
RPG:n `Character`-mallia ja `resolve_action`-sääntöä, mutta sitä ei ole upotettu
Day 1:n scene loopiin. Integraatio on eksplisiittinen ja yksisuuntainen adapteri:
hacking-session `HackingTransfer` voidaan lopuksi soveltaa `RPGState`-tilaan.

## Sosiaalinen simulaatio

`SocialSimulation` omistaa NetworkX-graafin. Hahmosolmuissa on piirteet, mieliala,
tavoitteet ja affiliaatiot. Suhdearvot rajataan välille −100...+100 ja muutokset
tallennetaan historiaan. Demo käyttää kuuden ydinhahmon korvattavaa koetilannetta.

## Vanha vapaa hacking-sandbox

`src/hacking/simulation.py` säilyttää aiemman `HackingSimulation`-API:n ja
`data/hacking/demo_target.json`-kohteen yhteensopivuus- ja mekaniikkakokeita varten.
Se tarjoaa pattern-, resonance-, entanglement-, isolation- ja collapse-operaatiot,
mutta ei ole varsinainen RPG-vertikaalinen slice.

## RPG-yhteensopiva nelikerrosdemo

`src/hacking/layered.py` toteuttaa:

- cybernetic-, psychic-, social- ja biological-nodet;
- typed edget ja piilotettujen nodejen löytämisen;
- Observed, Contact, Access, Privileged ja Control -tasot;
- Observe, Create Access, Exploit, Create Advantage, Defend, Overcome, Attack ja
  Retreat -toiminnot;
- tavallisen RPG:n 4dF-, attribuutti-, taito-, aspekti- ja Fate-resoluution;
- Alert-, Trace-, Feedback-, Instability- ja System stress -tilan;
- dataohjatut työkalut ja niiden layer/action-permissionit;
- turvalliset completed, detected, feedback_failure ja retreated -terminalit;
- serialisoitavan snapshotin ja RPG-vaikutusten `HackingTransfer`-adapterin.

`data/hacking/sleeping_patient.json` sisältää **Nukkuva potilas** -skenaarion.
Sen voi ratkaista teknis–biologisella tai psychic–biological-reitillä; social
layer tarjoaa vaihtoehtoisen suostumus- ja auktoriteettireitin.

## Käynnistys

```bash
streamlit run noopunk_ubiquitous_maniacs/social_demo.py
streamlit run noopunk_ubiquitous_maniacs/hacking_demo.py
```

Hacking-UI näyttää tavoitteen, tunnetut nodet ja edget, pääsytason, aktiivisen
kerroksen, työkalut, aspektikutsut, Alert/Trace/Feedback-luvut, toimintalokin ja
RPG:lle palautettavat vaikutukset. Graafin värit erottavat neljä kerrosta.

## Nykyiset rajat

- Hacking-adapteri ei käynnisty vielä automaattisesti Day 1 -skenaariosta.
- Opposed defense -agentit, edgejen bandwidth/latency ja monen operaattorin
  vuorojärjestys ovat rulebookissa valinnaista jatkokehitystä, eivät nykykoodia.
- Psychic/noetic-operaatiot ovat fiktiivistä mekaniikkaa, eivät neurotiede- tai
  kvanttifysiikkamalleja.
- Streamlit-kuorella ei ole selaintason automaatiotestiä; ydinsessio testataan
  suoraan Pythonissa.
