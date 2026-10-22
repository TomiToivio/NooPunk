# NetworkX
Pelin maailma koostuu neljästä NetworkX-graafista.
Nämä graafit kietoutuvat yhteen, mutta toteuta ne erillisinä moduuleina. 
Tarkoitus on että graafit yhdistetään myöhemmässä vaiheessa.
Nämä ovat:
* Sosiaalinen graafi: laboratorion aktiivisen kuuden hahmon ydinkastin sosiaaliset suhteet
* Kyberneettinen graafi: labran kyberavaruus-infrastruktuuri
* Noeettinen graafi: tämä kuvaa PSI-voimia, kollektiivista piilotajuntaa ja Noösfääriä, mutta käytännössä se mallintaa samalla Laclaun tyylisen diskurssianalyysin ja ideologian. Eli kollektiivisen tajunnan sisältö on diskurssia.
* Fyysinen graafi: tämä on laboratorion fyysinen graafi. Tämä on luultavasti tässä vaiheessa aika turha.

## Graafien toteuttaminen
Tee neljälle graafille omat moduulit.
Ota mukaan olemassaoleva sosiaalinen graafi.
Graafien sisältöä ei tarvitse tehdä vielä sen pidemmälle.
Graafien pitäisi olla sellaisessa formaatissa että ne voidaan visualisoida Streamlit-dashboardissa ja editoida Gephissä.
Eli jaa graafit neljään eri moduuliin, mutta älä mieti graafien sisältöä vielä sen pidemmälle.

## Toteutettu rajaus

Neljä graafia sijaitsevat erillisissä moduuleissa:

- `src/social/`
- `src/cyber/`
- `src/noetic/`
- `src/physical/`

Sosiaalinen graafi sisältää tällä hetkellä vain aktiivisen ydinkastin: Ingridin, Romppaisen, tohtori Tanakan, tohtori Pilgrimin, Elin Dahlin ja UFAB Ragnarök -tekoälyn, jota kutsutaan nimellä C.G. Jung. Muut aiemmat laboratoriohahmot on poistettu aktiivisesta graafidatasta, eikä niitä ole korvattu täytehahmoilla. Muut kolme moduulia luovat tyhjän `networkx.Graph`-olion, jonka domain on merkitty graafin metatietoon. Jokainen graafi voidaan serialisoida Streamlit-tarkastelua varten ja viedä GEXF-tiedostoksi Gephiä varten.

Graafien sisältöä tai niiden välisiä yhteyksiä ei ole toteutettu.
