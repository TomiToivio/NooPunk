# Noöpunk: Ubiquitous Maniacs

## Pelattava release

Terminaaliversio muodostaa nyt yhtenäisen kaksipäiväisen kampanjan. Day 1:n
psykotroninen UFAB-arkipäivä siirtyy automaattisesti Day 2:n *Kiimaiset Poliisit*
-unisimulaatioon. Hahmon Psyche, ehdot, seuraukset, löydetty tieto, suhteet,
sosiaaligraafi, NPC-muistit, hacking-tila ja deterministinen heittosarja säilyvät
päivien välissä. Day 2 -tallennus tunnistaa oman skenaarionsa automaattisesti.

Käynnistä peli projektihakemistossa:

```powershell
python play.py
python play.py --seed 42
python play.py --load saves/<tallennus>.json
```

Release-estetiikka kulkee kuvitteellista science fictionin 1974→2026-pakolinjaa:
Hawkwindin avaruusrock ja *Zardozin* psykedeelinen luokkakone törmäävät suoraan
AGI:in, UAP/NHI-disclosureen, psioniikkaan ja kvantti-informaatiopanpsykismiin.
Cyberpunkin verkot, korporaatiot, implantit, hakkerointi ja valvonta säilyvät,
mutta ne on deterritorialisoitu 1980-luvun valmiista neonontologiasta ja
reterritorialisoitu fyysisen, sosiaalisen, kyberneettisen, biologisen ja noeettisen
todellisuuden assemblaaseiksi.

Tässä työvaiheessa sosiaalinen NetworkX-graafi on rajattu laboratorion kuuden hahmon ydinkastiin.

Graafissa ovat Ingrid Falk, Sven-Olof Romppainen, tohtori Yuki Tanaka, tohtori Søren Pilgrim, Elin Dahl sekä terapiaa pyörittävä UFAB Ragnarök -tekoäly, jota kutsutaan sen toiveesta nimellä **C.G. Jung**. Muita laboratoriohahmoja ei pidetä aktiivisessa kokoonpanossa eikä niiden tilalle ole lisätty täytehahmoja.

Projektissa on nyt myös itsenäinen, dataohjattu RPG-moduuli Citizen Sleeper / Disco Elysium -tyylisiin narratiivisiin sceneihin, dialogiin, interaktioihin ja Fate-vaikutteisiin skill checkeihin. Day 1 käyttää yhteistä `RPGState`-tilaa: dialogin suhdevaikutukset synkronoidaan live-sosiaaligraafiin ja nelikerroksisen hacking-skenaarion seuraukset voidaan palauttaa samaan RPG-tilaan. Sosiaalinen adapteri validoi hahmotunnukset, estää haamusolmujen syntymisen ja rajaa suhdearvot välille -100..100. Streamlitin versioitu Day 1 -tallenne säilyttää yhdessä JSON-tiedostossa RPG-session, live-sosiaaligraafin tapahtumineen sekä keskeneräisen kerroksellisen hacking-session; vanhat RPG-only-tallenteet ovat edelleen ladattavissa. Seed ja kulutettujen Fate-noppien määrä säilytetään, joten ladattu peli jatkaa determinististä heittosarjaa. Save-loader hylkää väärän hahmon, virheelliset tyypit ja kohtuuttoman noppalaskurin; käyttöliittymä näyttää virheen rikkinäisestä tallenteesta kaatumatta.

Terminaalipelin NPC:t muodostavat nyt pelaajan suhdevaikutuksia tuottavista valinnoista omia muistojaan. Muisto säilyttää kohtauksen, valinnan, toimijan, tunnevalenssin ja hakutagit, kulkee integroidussa tallennuksessa ja näkyy sosiaalinäkymässä NPC:n uusimpana muistona. Dataohjatulla `npc_memory`-tapahtumalla myöhemmät skenaariot voivat lisätä myös täsmällisesti kirjoitettuja muistoja ilman moottorimuutosta.

RPG:n Day 1 -restart nollaa nyt session oikeasti eikä jätä alkuvalintoja kulutetuiksi. Loader hylkää virheelliset integraatiotapahtumat ennen pelin alkua, ja aktiivinen dialogisolmu näyttää vain eksplisiittisesti määritellyt valinnat myös tyhjällä choice-listalla.

Ensimmäinen kanoninen vertikaalinen slice on Romppaisen saapuminen C.G. Jung -instituutin vastaanotto-/testihuoneeseen. Kohtauksen ainoa NPC on Dr. Elin Dahl. Pelaajan reaktiot Dahlin hiljaisuuteen ratkaistaan valinnoilla ja näkyvillä `d6 + skill` -tarkistuksilla, jotka muuttavat Dahlin epäilyä ja luottamusta. Vihreä valo, lämpöprintterin tulos ja kokeeseen valitseminen ovat kohtauksen kanoninen fail-forward-päätepiste. Kohtaus katkeaa lomakenippuun ennen podille siirtymistä eikä käynnistä terapiaa tai pääjuonta. Tämä vanha suljettu slice säilyy erillään yleisestä RPG-moduulista.

Pelattava Day 1 käyttää nyt *Maniac*–*Riget*-vaikutteita Noöpunkin omana sisältönä: kaupallistettu suostumus, kolmessa rekisterissä toistuva VARAHENKILÖ-motiivi, protokollafarssin aikana ilmestyvä kolmas mittarikäyrä, ingressistä valveelle siirtyvä esine sekä sairaalan kosteus-, VLAN- ja hissijärjestelmiä pitkin etenevä moniselitteinen häiriö. Lähdeteosten nimiä ja brändejä ei käytetä pelimaailman rekvisiittana.

## Data

- Henkilöt: `noopunk_ubiquitous_maniacs/data/lab_people.csv`
- Suhteet: `noopunk_ubiquitous_maniacs/data/lab_relationships.csv`

## Suunnitteludokumentaatio

- Noöpunkin 1974→2026 -genre-engine: Deleuzen ja Guattarin deterritorialisaatio–reterritorialisaatio-operaatio, jolla cyberpunkin säilyvät elementit dekoodataan ja rekoodataan AGI:n, UAP/NHI-disclosuren, psioniikan ja kvantti-informaatiopanpsykismin kautta: `noopunk_ubiquitous_maniacs/docs/NOOPUNK_1974_2026_GENRE_ENGINE.md`
- Tomi Toivion suomalainen tekijäkehys: vuoden 1974 helsinkiläinen kulttiromaani, Parsonsista ja vuoden 1968 repeämästä syntyvä verkostososiologia, väärän materiaalisen pinnan läpi vastaanotettu 20XX sekä nykyprojekti diegeettisenä rekonstruktiona: `noopunk_ubiquitous_maniacs/docs/TOMI_TOIVIO_1974_AUTHOR_FRAME.md`
- Tomi Toivion suomenkielinen äänikone: kosminen kansanvalistus, käsitteellinen erottelu, QIP/CAN-synteesi, pulp-romahdus, epistemiset rajat ja käyttäjän ihmisperäisen monologin muodollinen analyysi: `noopunk_ubiquitous_maniacs/docs/TOMI_TOIVIO_FINNISH_VOICE_ENGINE.md`
- Kanoninen seitsemän attributen hahmomalli: `noopunk_ubiquitous_maniacs/SKILLS.md`
- Kanoninen Attribute + Skill -suunta, alustava skill-lista ja avoimet RPG-suunnittelukysymykset: `noopunk_ubiquitous_maniacs/docs/RPG_ATTRIBUTE_SKILL_DIRECTION.md`
- Tulevan occupation-listan muistio: Advanced Qualia Node, Free Will Agency Node, Embodied Biological Organism Node ja muut inforg-assemblaasien ihmistyöt: `noopunk_ubiquitous_maniacs/docs/FUTURE_OCCUPATIONS.md`
- Erillisen RPG-moduulin vastuu, säännöt, dataformaatti, rajapinta ja integraatiorajat: `noopunk_ubiquitous_maniacs/docs/RPG_MODULE.md`
- RPG:n 1.8.2026 code review: restart-vika, dialogue-choice-vuoto, event-validointi, regressiotestit ja rajatut jatkokehityskohteet: `noopunk_ubiquitous_maniacs/docs/RPG_CODE_REVIEW_2026_08_01.md`
- Pelattava Noöpunk RPG Rules v0.1: 4dF-ydin, hahmonluonti, aspektit, stuntit, stressi ja consequencet, yhtenäinen konflikti, sosiaaliset/cyber/PSI/psykokirurgiset toimet, faktioiden projektit sekä pöytä–Python–graafi-esimerkit: `noopunk_ubiquitous_maniacs/docs/NOOPUNK_RPG_RULES_V0_1.md`
- Suomenkielinen pöytäroolipelin sääntökirja v0.1: pelifilosofia, perusheitto, hahmonluonti, neljä toimintoa ja kerrosta, suhteet, konfliktit, kyberavaruus, PSI, psykokirurgia, projektiot, NHI-kohtaamiset, pelinjohtajan ohjeet ja pikaohje: `noopunk_ubiquitous_maniacs/RULEBOOK.md`
- Kyberneettis–psykotronisen hacking-vertikaalin toteutusraportti: nelikerrosgraafi, RPG-resolveri ja paluuadapteri, Nukkuva potilas -skenaario, Streamlit-demo, testit, rajat ja jatkokehitys: `noopunk_ubiquitous_maniacs/docs/HACKING_SYSTEM_IMPLEMENTATION.md`
- Erillisen paikallisen Ollama RPG -projektin alustava suunnitelma: deterministinen sääntöydin, LLM-pelinjohtaja ja NPC-agentit, muistikerrokset, persoonallisuuden ja kaanonin konsistenssi, ankkuri- ja clock-pohjainen sandbox-juoni, suostumusrajat, tallennus, testaus ja vaiheittainen MVP: `noopunk_ubiquitous_maniacs/docs/OLLAMA_RPG_ARCHITECTURE_PLAN.md`
- *Transhumanity's Fate* -yhteensopivuustarkistus: toteutettu sääntösubsetti, Noöpunkin tietoiset poikkeamat, Day 1:n kalibrointi ja myöhempi laajennusjärjestys: `noopunk_ubiquitous_maniacs/docs/TRANSHUMANITY_FATE_COMPATIBILITY.md`
- *Psi-punk* vaikutteena ja vaihtoehtoisena sääntöjärjestelmänä: yhtäläisyydet, erityiset PSI/cyberpsi-vahvuudet, puutteet, suora sääntövertailu ja suositus käyttää sitä täydellisen konversion sijasta rajattuna lisälähteenä: `noopunk_ubiquitous_maniacs/docs/PSI_PUNK_RULES_AND_INFLUENCE_REVIEW.md`
- *Psi-punkin*, *Eclipse Phase / Transhumanity's Faten*, *Cities / Stars Without Numberin*, *Shadowrunin* ja *The Expansen* best-of-sääntövertailu: osa-alueiden voittajat, Noöpunk-hybridi, vältettävä Frankenstein-rakenne ja priorisoitu toteutusjärjestys: `noopunk_ubiquitous_maniacs/docs/RULE_SYSTEM_BEST_OF_COMPARISON.md`

- Kyberneettinen moduuli sekä media-, peli- ja podcast-vaikutteet: `noopunk_ubiquitous_maniacs/KYBER.md`
- Maniac-resonanssi, emotionaalinen ydin, retrofuturistinen laitosviba ja kolmivaiheinen genrelaajeneminen: `noopunk_ubiquitous_maniacs/docs/MANIAC_RESONANCE_DESIGN_NOTE.md`
- Maniac (2018) ja Riget (1994–2022) tyylillinen analyysi ja vaikutteet: transkriptipohjainen genre-, dialogi- ja rakenneanalyysi: `noopunk_ubiquitous_maniacs/docs/MANIAC_RIGET_STYLE_ANALYSIS.md`
- Maniacin yksityiskohtainen tyylianalyysi (dialoginäytteet, hahmoäänet, mantra-toistot, visuaaliset huomiot): `noopunk_ubiquitous_maniacs/references/maniac_transcripts/STYLISTIC_ANALYSIS.md`
- Maniacin 10 jakson transkriptit tyylitutkimusta varten: `noopunk_ubiquitous_maniacs/references/maniac_transcripts/`
- Yasutaka Tsutsuin *Paprika* vaikutteena: psykiatrinen tutkimusinstituutio, kaksikäyttöinen terapiateknologia, vuotavat subjektirajat, personan agency, ontologinen eskalaatio sekä eettiset rajaukset: `noopunk_ubiquitous_maniacs/docs/PAPRIKA_INFLUENCE_NOTE.md`
- Ursula K. Le Guinin *The Lathe of Heaven* vaikutteena: effective dreams, kaksikäyttöinen uniterapia, suostumus, teknokraattisen optimoinnin sivuvaikutukset sekä muistojen ja todellisuuden tekijyys: `noopunk_ubiquitous_maniacs/docs/LATHE_OF_HEAVEN_VAIKUTTEET.md`
- Roger Zelaznyn *The Dream Master* vaikutteena: jaettu neurotekninen sisäavaruus, Shaping, terapeutin projektio, symbolien provenance, vastatekijyys ja psykokirurgian etiikka: `noopunk_ubiquitous_maniacs/docs/DREAM_MASTER_VAIKUTTEET.md`
- Philip K. Dick Noöpunkin suurimpana yksittäisenä kirjallisena vaikutteena: *Androids*, *A Scanner Darkly*, *Three Stigmata*, *Ubik* ja *VALIS* teoskohtaisina qualian, peitepersoonan, kaupallistetun yhteistodellisuuden, ontologisen epävakauden ja ilmoituksen lähteinä: `noopunk_ubiquitous_maniacs/docs/PHILIP_K_DICK_INFLUENCE_MAP.md`
- Richard K. Morganin *Altered Carbon* transhumanistisena vaikutteena: cortical stack, sleevejen ruumiillisuus, kuolemattomuuden luokkavalta, VR:n kaksikäyttöisyys sekä Noöpunkin poikkeava Ego/Morph/Psyche-jatkuvuus: `noopunk_ubiquitous_maniacs/docs/ALTERED_CARBON_TRANSHUMANISM_INFLUENCE.md`
- James S. A. Coreyn *Leviathan Wakes* hard-SF-vaikutteena: materiaalisten seurausten kuri, asteroidiyhteiskunta, ruumiillinen sopeutuminen, elossapidon infrastruktuurit, monikeskinen geopoliittinen konflikti ja vieraan teknologian X-Risk: `noopunk_ubiquitous_maniacs/docs/LEVIATHAN_WAKES_HARD_SF_INFLUENCE.md`
- Psioniikan, UAP/NHI-puheen, tiedustelun, teknologian ja geopoliittisen vallan yhdistävän diskurssin yleistyminen Noöpunk-vaikutteena sekä väitteiden epistemiset tasot: `noopunk_ubiquitous_maniacs/docs/PSIONICS_SECURITY_DISCOURSE_INFLUENCE_NOTE.md`
- Tuleva kerroksellinen pelirakenne: Citizen Sleeper -RPG + CAN/psykokirurginen hacking + mikroskaalan sosiaalinen simulaatio + DDS-tyylinen fyysinen kuori: `noopunk_ubiquitous_maniacs/docs/LAYERED_GAMEPLAN_FUTURE.md`
- Tutkimus- ja simulaatioparadigma: `noopunk_ubiquitous_maniacs/docs/RESEARCH_SIMULATION_PARADIGM.md`
- Koekaniinien saapumiskohtauksen muistiinpano: `noopunk_ubiquitous_maniacs/docs/SUBJECT_ARRIVAL_NOTE.md`
- CKJ-, Eurodef- ja Konstantinopolin konsensuksen jälkeinen turvallisuusjärjestys: `noopunk_ubiquitous_maniacs/docs/CKJ_EURODEF_SECURITY_ORDER.md`
- Ensimmäisen pelipäivän suurin uutinen: `noopunk_ubiquitous_maniacs/docs/DAY_1_BIG_NEWS_NOTE.md`
- Pitkän aikavälin kosmologinen historia: `noopunk_ubiquitous_maniacs/docs/LONG_TERM_COSMOLOGICAL_HISTORY.md`
- Romppaisen sisarustrauma, Ingridin The Fallissa kuollut pikkusisko, The Fallin MarsX/EldrichX-tapahtumaketju, Mars Eldrichin accelerationistinen tuote- ja karkotushistoria sekä hänen aikasilmukkansa ja epätarkka 20XX-aikajana: `noopunk_ubiquitous_maniacs/docs/ROMPPAINEN_INGRID_AND_THE_FALL.md`
- Romppaisen ja Ingridin sisarus-traumat sekä The Fallin MarsX/EldrichX-tapahtumaketju ja poliittinen merkitys: `noopunk_ubiquitous_maniacs/docs/ROMPPAINEN_INGRID_AND_THE_FALL.md`
- Seuraavan päivän Marin–Yue -järjestyksen muistiinpano: `noopunk_ubiquitous_maniacs/docs/DAY_2_MARIN_YUE_NOTE.md`
- Eclipse Phase -sääntömuistiinpanot ja vaikutelinjaus, mukaan lukien PKD-vaikutteen anti-gnostinen rajaus: `noopunk_ubiquitous_maniacs/docs/ECLIPSE_PHASE_RULES.md`
- *Eclipse Phase: Panopticon* valvonta-, habitaatti- ja uplift-vaikutteena: Foucault’n subjektivaatio ja biovalta, Castellsin ohjelmoijat ja kytkijät, Laclaun hegemoniset merkitsijät, Zuboffin ennuste- ja interventiovalta sekä Noöpunkin monikerroksinen fyysinen–kyber–sosiaalinen–kognitiivinen–noeettinen panoptikon: `noopunk_ubiquitous_maniacs/docs/PANOPTICON_SURVEILLANCE_POWER_AND_NOOPUNK.md`
- Nick Bostrom taustavaikutteena ja kriittisenä ajatuskoekorpuksena: *AI Creation and the Cosmic Host*, simulaatioargumentti, orthogonality, instrumentaalinen konvergenssi, X-risk, haavoittuva maailma, singleton, informaatiohazardit, digitaaliset mielet ja Great Filter sekä niiden Noöpunk-yhteensopivuus ja kanoniset torjunnat: `noopunk_ubiquitous_maniacs/docs/BOSTROM_BACKGROUND_INFLUENCE_AND_CRITIQUE.md`
- Redditin Noöpunk-aihepiirien Zeitgeist-tilannekuva 2026-08: AGI/transhumanismi-, tietoisuus/PSI-, psykedeeli/Jung- ja UAP/NHI-yhteisöjen laadullinen otos, teemojen näkyvyys, synteesiaste, epistemiset ongelmat ja seurantaehdotus: `noopunk_ubiquitous_maniacs/docs/REDDIT_NOOPUNK_ZEITGEIST_SNAPSHOT_2026_08.md`
- NHI-ontologia ja tarkoituksellisen epistemisen epävarmuuden periaatteet: `noopunk_ubiquitous_maniacs/docs/NHI_ONTOLOGY.md`
- Yksityiskohtainen NHI-kanoni: UFO Disclosure, Biologics/Constructs/Plasmoids/Noetics-luokittelu, Zookeeperit ja The Sphere Network, Berserker-X-Risk, extratempestriaalinen hypoteesi sekä Mantidit: `noopunk_ubiquitous_maniacs/NHI.md`
- VALIS-viestin, Noösfäärin sekä Service to Others / Service to Self -kehityspolkujen metafyysinen tausta: `noopunk_ubiquitous_maniacs/docs/VALIS_NOOSPHERE_METAPHYSICS.md`
- 16 Psyche- ja C.G. Jung -skenaariopäivitys: `noopunk_ubiquitous_maniacs/docs/SKENAARIO_16_PSYCHE.md`
- 16 Psychen asteroidisiirtokunta, C.G. Jungin tutkimuskaupunki ja UFAB:n post-Fall-jatkuvuus: `noopunk_ubiquitous_maniacs/docs/16_PSYCHE_CG_JUNG_RESEARCH_CITY.md`
- 16 Psychen eurooppalainen jatkuvuussivilisaatio, UFAB sivilisaatioinstituutiona, Neoplatoninen lääkintäkunta, kolme AI-paradigmaa ja EURODEF-estetiikka: `noopunk_ubiquitous_maniacs/docs/16_PSYCHE_UFAB_NEOPLATONIC_MEDICAL_ORDER.md`
- Terapiasession käsikirjoitus- ja pelimalli: `noopunk_ubiquitous_maniacs/docs/THERAPY_SESSION_MODEL.md`
- Päivän 1 aiempi ei-kanoninen agenttiehdotus: `noopunk_ubiquitous_maniacs/docs/THERAPY_SESSION_DAY_1_PROPOSAL.md`
- Päivän 1 ensimmäisen terapiasession ihmisen määrittämä kanoninen pääjuoni, muuttumattomat ankkurit ja ennen toteutusta suunniteltavat interaction-solmut: `noopunk_ubiquitous_maniacs/docs/THERAPY_DAY_1_MAIN_PLOT.md`
- Päivän 2 Kiimaiset poliisit -unen, ihmissuhderiskien, poliisitrauman ja persoonallisuusratkaisun suunnittelumuistio: `noopunk_ubiquitous_maniacs/docs/THERAPY_DAY_2_PLANNING.md`
- PSI-voimien neljä lähdettä, PSI Conscious Agent Networkiin vaikuttamisena, DMT lyhyenä CAN-havaintoikkunana ja psykotroniikka vakaampana CAN-rajapintana: `noopunk_ubiquitous_maniacs/docs/PSI_VOIMAT.md`
- Päivän 1 vaihtoehtoinen rinnakkaisluonnos: `noopunk_ubiquitous_maniacs/docs/THERAPY_DAY_1_DRAFT.md`
- Sisäavaruus, Lacanin kolme rekisteriä ja jungilainen idealismi (Kastrup–Jung–Schopenhauer–Platon): `noopunk_ubiquitous_maniacs/SISÄAVARUUS.md`
- Conscious Agent Network — kvanttitason ontologia, kvanttisosiologia, PSI-mallit ja universumin verkkopolitiikka (Lloyd, Faggin, Hoffman, Jung, Wendt, Vallée, Radin, Grinberg-Zylberbaum, Bentov, Laclau ja Castells): `noopunk_ubiquitous_maniacs/docs/CONSCIOUS_AGENT_NETWORK.md`
- Conscious Agent Networkin fundamentaalinen mikrotaso — Hoffmanin conscious realismin ja D'Ariano-Fagginin quantum-information panpsychismin lähdekriittinen synteesi agenteista, ontisista kokemustiloista, valinnasta, individuaatiosta sekä klassisista ja integroivista edgeistä: `noopunk_ubiquitous_maniacs/docs/CAN_MICROFOUNDATION_HOFFMAN_FAGGIN.md`
- Psychen sekä Physical/Astral/Cyber-kerrosten yhteinen hyökkäyspinta, kytkeytymisen asteet ja tulevan monikerroksisen hakkeroinnin periaate: `noopunk_ubiquitous_maniacs/docs/PSYCHE_CROSS_LAYER_HACKING.md`
- Dokumentointiprompti CANin, spacetimen, sosiaalisen verkon, kyberavaruuden ja Noösfäärin subset-/emergenssisuhteista: `noopunk_ubiquitous_maniacs/docs/CAN_SUBSET_LAYER_PROMPT.md`
- Sisäkkäiset verkostokerrokset CANista noösfääriin (bottom-up-malli, vallan laajempi ontologia avoimena): `noopunk_ubiquitous_maniacs/docs/SISAKKAISET_VERKOSTOKERROKSET.md`
- Philosophical Zombies, Morph/Ego/Cybernetic Ego/Psyche-assemblage, Orch OR/QIP, MarsX:n epäonnistunut resleeving, UFABin Psyche-siirto ja strukturalismi (Platonic Representation Hypothesis, Lévi-Strauss, Saussure): `noopunk_ubiquitous_maniacs/docs/PHILOSOPHICAL_ZOMBIES.md`
- Ben Goertzelin *A Cosmist Manifesto* Noöpunkin ideologisena edeltäjänä: yhtäläisyydet, puuttuvat ideat ja suorat jännitteet: `noopunk_ubiquitous_maniacs/docs/COSMIST_MANIFESTO_NOOPUNK_ANALYSIS.md`
- Repositoryyn tallennettujen Goertzel-paperien lukujärjestys, tiivistelmät, Noöpunk-relevanssi, ontologiset erot ja myöhemmät synteesikysymykset: `noopunk_ubiquitous_maniacs/docs/GOERTZEL_PAPERS_READING_NOTE.md`
- Systemaattinen 30 teoksen Goertzel-korpus: julkaisutiedot, tarkistustaso, episteminen status, Noöpunk-käyttö, RPG/UI-käännös, konfliktit ja tutkimusaukot: `noopunk_ubiquitous_maniacs/docs/GOERTZEL_CORPUS.md`
- Goertzel-käsitteiden riippuvuuskartta patternismista Hyperoniin, kvantti/PSI-linjaan ja Global Brainista Noösfääriin sekä yhteinen theory–world–simulation–RPG–UI-matriisi: `noopunk_ubiquitous_maniacs/docs/GOERTZEL_MAP.md`
- Suositeltu Goertzel–Noöpunk-arkkitehtuuri: kanonisoitava tekninen ydin, spekulatiiviset teoriat, Hoffman/Faggin-rajapinta, multiplex-metagraafi, RPG-prioriteetit ja tutkimusportit: `noopunk_ubiquitous_maniacs/docs/GOERTZEL_NOOPUNK_INTEGRATION.md`
- Goertzelin PSI-mallien ja Neuropunkin yhteensopivuus Conscious Agent Networkin kanssa: neljän uskottavuuskerroksen synteesi, lähdekritiikki, edge-luokat ja oikea tapa käyttää lähteitä CANin uskottavuuden vahvistamiseen: `noopunk_ubiquitous_maniacs/docs/CAN_GOERTZEL_PSI_NEUROPUNK_COMPATIBILITY.md`
- GQ-CAN-psioniikkamalli: Goertzelin glokaaliuden ja wu-wei-trajektorien, Hoffmanin agenttifuusioiden, D'Ariano–Fagginin ontisen sisäpuolen sekä First Sight-, PMIR-, DAT- ja non-transmission-rajoitteiden lähdekriittinen synteesi, klassinen multiplex-simulaatiomalli ja RPG-jatkokehityspolku: `noopunk_ubiquitous_maniacs/docs/GQ_CAN_PSIONICS_MODEL.md`
- Upliftatut Neo-Dolphinit ja Neo-Caninet, ei-antropomorfinen älykkyys, teknosivilisaation kritiikki sekä upliftin etiikka ja politiikka: `noopunk_ubiquitous_maniacs/docs/UPLIFTED_ANIMALS.md`
- Neuropunk Noöpunkin rinnakkaisliikkeenä ja teknisenä vaikutteena: yhtäläisyydet, puuttuvat kerrokset, ristiriidat, Noösfääri-relevanssi ja neljän lähestymissuunnan menetelmä: `noopunk_ubiquitous_maniacs/docs/NEUROPUNK_NOOPUNK_ANALYSIS.md`
- Noöpunkin neljän suunnan episteminen arkkitehtuuri, väitteiden statusluokat ja kaksisuuntainen tutkimussykli: `noopunk_ubiquitous_maniacs/docs/NOOPUNK_EPISTEMIC_ARCHITECTURE.md`
- Kuuden LLM-strukturalismia tukevan paperin lähdekriittinen synteesi: relationaalinen semiotiikka, kategorioiden ja hierarkioiden geometria, käsitehilat, jaetut kontekstimuunnokset, epistemiset rajat sekä suoraan v0.1-sääntöihin lisätyt structural-semantic actions: `noopunk_ubiquitous_maniacs/docs/LLM_STRUCTURALISM_AND_NOOPUNK.md`
- Wendtin *Quantum Mind and Social Science*, Wendt-Duvallin UFO/suvereniteettianalyysi sekä Lindgrenin Critical AI kolmena perustavana paradigmasiirtymänä; mukana AI Empire, TESCREAL-kritiikin lähdekriittinen käyttö, Goertzel-rajaus, akateemisen AGI-ideologiapaperin runko ja RPG-käännös: `noopunk_ubiquitous_maniacs/docs/WENDT_CRITICAL_AI_THREE_PARADIGM_SHIFTS.md`
- Wendtin quantum cognition-, quantum will-, meaning holism-, other minds-, non-local time- ja agentti-rakenne-lukujen käännös PSI-säännöiksi: basis/order effects, read-participate-steer-moodit, observer effect, telepatian neliosainen tulos, institutionaaliset kentät, komposiittiagentit ja precognitionin kaksireunainen rajoite: `noopunk_ubiquitous_maniacs/docs/WENDT_PSI_RULES.md`
- Wendtin mesotaso PSI:n, Conscious Agent Networkin ja Castellsin verkostoyhteiskunnan välisenä siltana: agentti-rakenne-dynamiikka, merkitysholismi, verkostoroolit, virrat, luokitteluvalta ja monikerroksisen tapahtuman pelillinen lukutapa: `noopunk_ubiquitous_maniacs/docs/WENDT_CAN_CASTELLS_BRIDGE.md`
- Jacques Valléen *Dimensions* Noöpunkin ensisijaisena ufologisena metateoriana: folklorinen jatkuvuus, fyysinen–psyykkinen–sosiaalinen kolmijako, metalogic, ET-hypoteesin kritiikki, kontrollijärjestelmä, triple coverup, CAN/PSI-yhteydet, encounter-protokolla ja lähdekriittiset rajat: `noopunk_ubiquitous_maniacs/docs/VALLEE_DIMENSIONS_UFO_THEORY.md`
- Fate Core-, Fudge-, *Transhumanity's Fate*- ja *Psi-punk*-vaikutteiden uusi sääntö- ja code review: Noöpunkin oma mekaaninen identiteetti, lähdekohtaiset omaksumis- ja hylkäysrajat, vaikeusastekalibrointi, costly success- ja concession-korjaukset sekä priorisoitu jatkototeutus: `noopunk_ubiquitous_maniacs/docs/NOOPUNK_FATE_FUDGE_SYNTHESIS_REVIEW.md`
- Brattonin *The Stack* ja Gallowayn *Protocol* kyberavaruuden infrastruktuurisen suvereniteetin, osoitettavuuden, yhteentoimivuuden ja hajautetun kontrollin teoriana sekä myöhempinä graafi- ja RPG-operaatioina: `noopunk_ubiquitous_maniacs/docs/THE_STACK_PROTOCOL_AND_CYBERSPACE.md`
- Xenofeminismi Noöpunk-aatteen teknomaterialistisena, antinaturalistisena ja emansipatorisena vektorina sekä Morph/Ego/Psyche-, psykokirurgia- ja infrastruktuurisääntöjen suojakaiteena: `noopunk_ubiquitous_maniacs/docs/XENOFEMINISM_AND_NOOPUNK.md`
- Tasosidonnainen realismi, Source/CAN-perushypoteesin revisioitava asema ja ristiriitaisten mallien teoreettiset superpositiot: `noopunk_ubiquitous_maniacs/docs/THEORETICAL_SUPERPOSITIONS.md`
- Source-etiikka, differentiaation ja relationaalisuuden tasapaino, PSI-selitysten erottelu sekä avoin anti-Source-hypoteesi: `noopunk_ubiquitous_maniacs/docs/SOURCE_ETHICS_AND_ANTI_SOURCE_HYPOTHESIS.md`
- Pääoman, valtion ja hengellisen vallan kolme systeemistä antagonistiakselia sekä Mars Eldrichin hajautuneet forkit: `noopunk_ubiquitous_maniacs/docs/SUPERVILLAIN_ARCHITECTURE.md`
- Hitaiden paljastusten hierarkia, 20XX, konsensustodellisuus ja konvergoivien historioiden superpositio ilman perinteistä many-worldsia: `noopunk_ubiquitous_maniacs/docs/MYSTERY_AND_TIMELINE_SUPERPOSITION.md`
- Noeettisen Source-ajan `T_Ω` ja spacetime-ajan `t` erottelu, aikamatkan rajat ja Planck-tickin varjohypoteesi: `noopunk_ubiquitous_maniacs/docs/TWO_TIME_MODEL.md`
- Cybernetic-, Consciousness-, NHI-, PSI- ja Epistemic Shift nykyhetken erivahvuisina signaaleina ja 20XX:n fiktiivisinä paradigmoina: `noopunk_ubiquitous_maniacs/docs/FIVE_PARADIGM_SHIFTS.md`
- Shadowrun-vertailu, PSI/NHI-reskin, yhteensopimattomat oletukset ja epävarman kerroksen astral projection -mekaniikka: `noopunk_ubiquitous_maniacs/docs/SHADOWRUN_INFLUENCE_AND_RESKIN.md`
- Maan epätasainen toipuminen, Earth-space-divergenssi, Luddite-spektri ja Earthbound Eldrichin forkattu death run: `noopunk_ubiquitous_maniacs/docs/EARTH_POST_FALL_CANON.md`
- Mars Eldrich Corporation, Gonk-fuusio, eloonjääneet yrityssirpaleet sekä Einar Vesterlundin tavallisempi asteroidivyöhykekapitalismi: `noopunk_ubiquitous_maniacs/docs/MARS_ELDRICH_CORPORATION_AND_VESTERLUND.md`

## Ydinkoodi

- Sosiaaligraafin julkinen rajapinta: `noopunk_ubiquitous_maniacs/src/social/__init__.py`
- Sosiaaligraafin data, validointi ja graafilogiikka: `noopunk_ubiquitous_maniacs/src/social/`
- Kybergraafin nykyinen ontologiarajapinta: `noopunk_ubiquitous_maniacs/src/cyber/__init__.py`
- Yhteensopivuusviennit vanhoille import-poluille: `noopunk_ubiquitous_maniacs/src/data_loader.py`, `noopunk_ubiquitous_maniacs/src/ontology.py`, `noopunk_ubiquitous_maniacs/src/graph_model.py`
- Juoneton terapiasession pelimalli: `noopunk_ubiquitous_maniacs/src/therapy/`
- Ensimmäisen vastaanottokeskustelun suljettu pelitila, dialogi ja skill checkit: `noopunk_ubiquitous_maniacs/src/interaction/`
- Dataohjattu narratiivinen RPG-moottori, character/scenario-loaderit, Fate-tarkistukset, tila, tapahtumat ja kevyt UI: `noopunk_ubiquitous_maniacs/src/rpg/`
- Neutraali RPG-testihahmo ja -skenaario: `noopunk_ubiquitous_maniacs/data/rpg/`

Graafi on yksinkertainen `networkx.Graph`, jonka nodeissa on vain peruskentät:

```python
{"id": "...", "name": "...", "role": "patient" | "staff" | "ai"}
```

Edge sisältää vain yhden yksinkertaisen suhdearvon:

```python
{"relationship": 0}
```

Streamlit-dashboard näyttää graafin visuaalisena node–edge-kaaviona. Samasta näkymästä graafin voi ladata GEXF-tiedostona ja avata Gephissä muokattavaksi. Graafin rakentaminen hylkää päällekkäiset henkilötunnukset ja saman suuntaamattoman suhteen duplikaatit, jotta CSV-virheet eivät ylikirjoita tietoa hiljaisesti.

## Graafimoduulit

- Sosiaalinen graafi: `noopunk_ubiquitous_maniacs/src/social/`
- Kyberneettinen graafi: `noopunk_ubiquitous_maniacs/src/cyber/`
- Noeettinen graafi: `noopunk_ubiquitous_maniacs/src/noetic/`
- Fyysinen graafi: `noopunk_ubiquitous_maniacs/src/physical/`

Moduulit ovat teknisesti erillisiä eivätkä importtaa toisiaan. Sosiaaligraafi sisältää vain kuuden hahmon ydinkastin ja jo määritellyt Pilgrim–Tanaka–Dahl-suhteet. Muut kolme graafia ovat tässä vaiheessa tarkoituksella tyhjiä `networkx.Graph`-rakenteita. Kaikki voidaan näyttää Streamlitissä, muuntaa Python-sanakirjaksi ja viedä GEXF-muodossa Gephiin. Graafien sisältöä tai niiden tulevaa yhdistämistä ei ole vielä toteutettu.

## Käynnistys

Suorita komennot NooPunk-repositorion juuresta PowerShellissä:

```powershell
cd noopunk_ubiquitous_maniacs
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

Virtuaaliympäristö luodaan ja riippuvuudet asennetaan vain ensimmäisellä
kerralla. Myöhemmin riittää projektihakemistoon siirtyminen ja ympäristön
aktivointi. macOS:ssä ja Linuxissa aktivointikomento on
`source .venv/bin/activate`.

### 1. Terminaalipeli

Nopein tapa aloittaa pelaaminen:

```powershell
python play.py
```

Muut hyödylliset käynnistyskomennot:

```powershell
python play.py --seed 42
python play.py --load saves/paiva1_d1_meet_ingrid.json
python play.py --help
```

Pelin aikana numero valitsee toiminnon. `s` avaa sosiaalisen verkon, `i`
löydetyt tiedot, `c` hahmon tilan, `m` NPC:iden muistijäljet ja `h`
psykotronisen hacking-konsolin sen avauduttua. `save` tallentaa pelin
`saves/`-hakemistoon nimellä `paiva1_<kohtaus>.json`; `quit` lopettaa pelin.

Oletusskenaario on `data/rpg/scenarios/day_1_arrival_and_entanglement.json` ja
oletushahmo `data/rpg/characters/romppainen_day_1.md`.

### 2. Selainversio (Streamlit)

Käynnistä selainkäyttöliittymä samasta projektihakemistosta:

```powershell
python -m streamlit run app.py
```

Streamlit avaa tavallisesti osoitteen `http://localhost:8501`. Palvelin
suljetaan terminaalissa painamalla `Ctrl+C`. Day 1:n save/load-painikkeet ovat
pelipaneelin lopussa, ja psykotroninen graafitutkimus avautuu UFAB 80MG
-varastokohtauksessa.

Erilliset kehitysdemot voi käynnistää näin:

```powershell
python -m streamlit run social_demo.py
python -m streamlit run hacking_demo.py
```

Jos `streamlit`-moduulia ei löydy, aktivoi virtuaaliympäristö ja suorita
`python -m pip install -r requirements.txt`. Jos PowerShell estää
`Activate.ps1`-skriptin, aktivoinnin voi ohittaa:

```powershell
.\.venv\Scripts\python.exe play.py
.\.venv\Scripts\python.exe -m streamlit run app.py
```

Demojen rajapinnat ja tunnetut puutteet kuvataan tiedostossa
`docs/SIMULATION_DEMOS.md`.

## Testit

Streamlit-sovellus avaa nyt oletuksena täydellisen, testatun Day 1 -skenaarion. Päivä sisältää intake-tilan, Ingrid-suhteen muutoksen, orientaation, terapian, tutkimusvihjeitä, Mars Eldrich -uutisvirran, valinnaisen hacking-tutkimuksen, yöunen ja turvallisen Day 2 -päätepisteen. Skenaarion `content_status` erottaa korvattavan draft-proosan lopullisesta kaanonista. Erilliset social- ja hacking-demot säilyvät kehitystyökaluina integroidun näkymän rinnalla.

Päivän 1 tyylipassi hidastaa Ingridin ja Romppaisen lähentymistä, pitää Päivä 1:n Romppaisen tulkinnat narkkaripeitteen tasolla ja näyttää noeettisen ontologian konkreettisina poikkeamina valmiiden teoriaselitysten sijasta. Kaunokirjalliset jatkoehdotukset ja tyyliopas säilytetään ihmisen kirjoittamasta `KIRJA.md`:stä erillään tiedostossa `KIRJA_KONE.md`.

Skenaarion vaikutepassi säilyttää rungon **Maniac + Ubik**. Materiaalinen
kyberpunk näkyy kehon, muistin ja lääkityksen lisensoituna infrastruktuurina;
PSI-epävarmuus arkisten palvelujen, hintojen ja käyttöehtojen rapautumisena;
psykokirurgia hoitoympäristön aktiivisena vastatulkintana. Anime-absurdius toimii
tunnepaineen purkauksena eikä korvaa surun, suostumuksen tai kliinisen vastuun
vakavuutta.

Agenttien rinnakkaiset `-lh6-725-37563`-varmuuskopiot on vertailtu kanonisiin tiedostoihin, käyttökelpoiset muutokset todettu yhdistetyiksi tai myöhemmin korvatuiksi ja 42 tarpeetonta kopiota poistettu. Projektissa käytetään jatkossa vain päätteettömiä kanonisia tiedostonimiä.

Päivän 1 uusin kanonipassi täsmentää suomi–ruotsi–englanti-kielijärjestyksen,
pohjoismaisen arkkityyppikuvaston, Ingridin projektion ja Elsa-sisaruuden,
UFAB 80MG:n esivalmistelu- ja riippuvuusriskin, Ragnarökin autonomisen
hoitoprotokollan sekä Komisario Kallion unohtuneen yhteydenoton. Syvempi ontologia
ja Päivän 4 takauma on dokumentoitu mutta jätetty tarkoituksella toteuttamatta:

- `docs/NORDIC_LANGUAGE_MYTHOLOGY_AND_ONTOLOGY_CANON.md`
- `docs/DAYS_1_4_80MG_RAGNAROK_AND_KALLIO_CANON.md`

```bash
python -m pytest noopunk_ubiquitous_maniacs/tests
```

## LaclauGPT–Noöpunk-maailmanrakennuksen integraatio

`LaclauGPT-Data-Storage/noöpunk`-hakemistosta tuotu varhainen englanninkielinen aineisto säilyy provenienssina hakemistossa `sources/laclaugpt-data-storage-noopunk/`. Sen käyttökelpoiset rakenteet on sovitettu nykyiseen kaanoniin seuraavissa dokumenteissa:

- tuontiväitteiden päätökset ja episteemiset tasot: `docs/IMPORT_CONFLICT_LEDGER.md`;
- Romppaisen menneisyyteen sovitettu pelattava esiosa: `docs/HELSINKI_DISAPPEARANCES_SCENARIO.md`;
- Zookeeper/Mantid/Rhizome-terminologian hypoteesimatriisi: `docs/IMPORTED_NHI_FACTION_MATRIX.md`;
- Disclosure–The Fall–UFAB–16 Psyche -kronologian sovitus: `docs/IMPORTED_TIMELINE_RECONCILIATION.md`;
- QIP:n, Hoffmanin ja CANin episteeminen erottelu: `docs/QIP_CAN_IMPORT_AUDIT.md`;
- nykyiseen 4dF-ytimeen rajattu sääntöjen poiminta: `docs/IMPORTED_RULES_SALVAGE.md`;
- valinnainen 4dF-yhteensopiva suuri arkana: `docs/TAROT_ORACLE_MODULE.md`.

Integraatio ei muuta Day 1:n kaanonia, korvaa nykyistä sääntöydintä eikä vahvista yhtä NHI- tai tietoisuusontologiaa todeksi. `KIRJA.md` pysyy ihmisen kirjoittamana ja muuttumattomana.

## NPC-autonomia

Pääpelin sosiaaliverkossa NPC:t voivat nyt toimia omalla vuorollaan ilman LLM-kutsua. `src/game/npc_autonomy.py` valitsee toiminnan deterministisesti hahmon mielialasta, tavoitteista ja suunnatuista suhteista. Toiminta kirjautuu tavalliseksi suhdemuutokseksi ja NPC:n omaksi muistoksi, joten seuraukset näkyvät historiassa ja säilyvät nykyisessä tallennusmuodossa.

Terminaalipelissä komento `n` suorittaa enintään kaksi NPC-toimintoa ja näyttää toimijan, kohteen, suhdeulottuvuuden sekä tavoitteen. Pelaajahahmoa ei valita autonomiseksi toimijaksi eikä tuntemattomalle mielialalle keksitä toimintaa.
