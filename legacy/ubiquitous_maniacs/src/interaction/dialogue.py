"""Elin Dahlin testihuonekohtauksen dialogipuu ja pelilogiikka.

Valinnat ja skill checkit muuttavat Dahlin epäilyä ja luottamusta, mutta
epäonnistuminen vie aina kohtausta eteenpäin. Kohtaus päättyy hyväksyntään ja
lomakkeisiin ennen podille siirtymistä.
"""

from __future__ import annotations

from dataclasses import dataclass, field

from .skills import perform_check
from .state import EnrollmentStatus, ReceptionGame


@dataclass
class Choice:
    id: str
    text: str
    attribute: str | None = None
    difficulty: int = 0
    on_success_suspicion: int = 0
    on_failure_suspicion: int = 0
    on_success_trust: int = 0
    on_failure_trust: int = 0
    next_node: str = "test_room"
    success_text: str = ""
    failure_text: str = ""
    enrollment_override: EnrollmentStatus | None = None

    def has_check(self) -> bool:
        return self.attribute is not None


@dataclass
class DialogueNode:
    id: str
    npc_name: str
    narration: str
    npc_text: str
    choices: list[Choice] = field(default_factory=list)


NODES: dict[str, DialogueNode] = {}


def _node(node: DialogueNode) -> DialogueNode:
    NODES[node.id] = node
    return node


_node(DialogueNode(
    id="test_room",
    npc_name="DR. ELIN DAHL",
    narration=(
        "Huone on jossain vastaanoton, lääkärin vastaanottohuoneen ja psykologisen "
        "testilaboratorion välissä. Liian siisti ollakseen kodikas, liian "
        "vanhanaikainen ollakseen futuristinen. Pöydällä on retrohenkinen "
        "tietokone, lämpöprintteri ja hiljaa piippaava mittalaite. Dr. Elin Dahl "
        "katsoo näyttöä, sitten sinua. Hiljaisuus pitkittyy."
    ),
    npc_text="",
    choices=[
        Choice(
            id="android_or_homosexual",
            text="'Tutkitteko, olenko androidi tai homoseksuaali?'",
            next_node="second_silence",
            on_success_trust=1,
            success_text="Dahl tuijottaa intensiivisesti. Ei hymähdystä. Ei kulmakarvan liikettä.",
        ),
        Choice(
            id="observe_dahl",
            text="[Awareness] Tutki Dahlin reaktiota vastaamatta vielä.",
            attribute="Awareness",
            difficulty=7,
            on_success_suspicion=-1,
            on_success_trust=1,
            on_failure_suspicion=1,
            success_text=(
                "Dahl ei odota oikeaa vastausta. Hän odottaa spontaania poikkeamaa — "
                "jotakin, mitä et itse vielä tiedä tekeväsi."
            ),
            failure_text="Dahl huomaa yrityksesi lukea häntä ennen kuin ehdit lukea häntä.",
            next_node="second_silence",
        ),
        Choice(
            id="wait_first",
            text="[Willpower] Kestä hiljaisuus ja anna sivupersoonan olla reagoimatta.",
            attribute="Willpower",
            difficulty=8,
            on_success_suspicion=-1,
            on_failure_suspicion=2,
            success_text="Hiljaisuus jää Dahlin ongelmaksi.",
            failure_text="Sivupersoona hymyilee väärällä hetkellä. Dahl rekisteröi sen.",
            next_node="second_silence",
        ),
    ],
))


_node(DialogueNode(
    id="second_silence",
    npc_name="DR. ELIN DAHL",
    narration=(
        "Dahl ei vastaa. Mittalaitteen merkit vaihtuvat ruudulla. Hän katsoo sinua "
        "kuin testin varsinainen sisältö tapahtuisi siinä osassa sinua, johon "
        "sinulla ei ole pääsyä."
    ),
    npc_text="",
    choices=[
        Choice(
            id="virus_carrier",
            text="'Epäilettekö minua viruksen kantajaksi?'",
            next_node="green_light",
            on_failure_suspicion=1,
            success_text="Dahl ei vastaa. Katse ei irtoa sinusta.",
        ),
        Choice(
            id="inspect_device",
            text="[Intelligence] Päättele mittalaitteen tarkoitus sen signaaleista.",
            attribute="Intelligence",
            difficulty=8,
            on_success_trust=1,
            on_failure_suspicion=1,
            success_text=(
                "Laite ei etsi yhtä diagnoosia. Se vertaa reaktioitasi useisiin "
                "keskenään ristiriitaisiin persoonallisuusmalleihin."
            ),
            failure_text="Laitteen vanhanaikainen kuori peittää vieraan mittauslogiikan.",
            next_node="green_light",
        ),
        Choice(
            id="joke_again",
            text="[Charisma] 'Jos tämä on persoonallisuustesti, haluan vaihtaa vastaukseni.'",
            attribute="Charisma",
            difficulty=8,
            on_success_trust=2,
            on_failure_suspicion=1,
            success_text=(
                "Dahlin suupielen lihas tekee lähes tapahtumattoman liikkeen. "
                "Se saattaa olla nauru tai mittausvirhe."
            ),
            failure_text="Dahl ei anna vitsille edes epäonnistumisen iloa.",
            next_node="green_light",
        ),
    ],
))


_node(DialogueNode(
    id="green_light",
    npc_name="DR. ELIN DAHL",
    narration=(
        "Pieni vihreä valo syttyy laitteen kylkeen. Lämpöprintteri herää ja "
        "tulostaa pitkän paperiliuskan. Dahl ei katso paperia. Hän katsoo sinua. "
        "Kun printteri vaikenee, hän vilkaisee tulosta kerran ja laskee sen pöydälle."
    ),
    npc_text="Onneksi olkoon. Teidät on valittu kokeeseen.",
    choices=[
        Choice(id="accept_plainly", text="Nyökkää ja odota jatko-ohjeita.", next_node="forms", on_success_trust=1),
        Choice(
            id="ask_why",
            text="[Intelligence] 'Mikä tuloksessa teki minusta sopivan?'",
            attribute="Intelligence",
            difficulty=9,
            on_success_trust=1,
            on_failure_suspicion=1,
            success_text="Dahl katsoo paperia. 'Juuri se, ettei tulos vastaa yhtä selitystä.'",
            failure_text="'Sitä ei ole tarkoituksenmukaista selittää ennen koetta.'",
            next_node="forms",
        ),
        Choice(
            id="relieved_joke",
            text="[Charisma] 'Hyvä. Pelkäsin jo olevani liian terve.'",
            attribute="Charisma",
            difficulty=7,
            on_success_trust=2,
            on_failure_suspicion=1,
            success_text="Dahl laskee paperin pöydälle. 'Sitä emme ole vielä ratkaisseet.'",
            failure_text="Dahl vetää laatikon auki vastaamatta.",
            next_node="forms",
        ),
    ],
))


_node(DialogueNode(
    id="forms",
    npc_name="DR. ELIN DAHL",
    narration=(
        "Dahl vetää laatikosta lomakenipun, joka on huomattavasti paksumpi kuin "
        "tilanteessa vaikuttaisi kohtuulliselta, ja laskee sen eteesi."
    ),
    npc_text="Täyttäkää nämä lomakkeet. Sen jälkeen vien teidät podiinne.",
    choices=[
        Choice(id="my_pod", text="'Podiini.'", next_node="resolution", success_text="'Niin', Dahl sanoo."),
        Choice(id="sounds_good", text="'Se kuulostaa hyvältä.' Ota kynä.", next_node="resolution", on_success_trust=1),
        Choice(
            id="read_forms",
            text="[Awareness] Silmäile lomakenippua ennen allekirjoittamista.",
            attribute="Awareness",
            difficulty=7,
            on_success_trust=1,
            on_failure_suspicion=1,
            success_text=(
                "Suostumuslomakkeiden seassa on kysymyksiä unista, kaksoisolennoista "
                "ja muistoista, joita vastaajalla ei pitäisi olla."
            ),
            failure_text="Teksti järjestyy uudelleen sitä mukaa kun yrität lukea eteenpäin.",
            next_node="resolution",
        ),
    ],
))


_node(DialogueNode(
    id="resolution",
    npc_name="DR. ELIN DAHL",
    narration=(
        "Dahl tarkkailee vielä hetken. Otat kynän. Lomakenippu odottaa. "
        "Podiin ei mennä tässä kohtauksessa."
    ),
    npc_text="",
    choices=[Choice(
        id="finish",
        text="(CUT. Lopeta kohtaus.)",
        next_node="end",
        enrollment_override=EnrollmentStatus.ACCEPTED,
    )],
))


_node(DialogueNode(id="end", npc_name="", narration="", npc_text="", choices=[]))


def get_node(node_id: str) -> DialogueNode | None:
    return NODES.get(node_id)


def apply_choice(game: ReceptionGame, choice: Choice) -> tuple[str, bool | None]:
    """Sovella valinta pelitilaan ja palauta seurausteksti sekä checkin tulos."""
    success: bool | None = None

    if choice.has_check():
        assert choice.attribute is not None
        result = perform_check(game, choice.attribute, choice.difficulty)
        success = result.success
        if success:
            game.receptionist.adjust_suspicion(choice.on_success_suspicion)
            game.receptionist.adjust_trust(choice.on_success_trust)
            text = choice.success_text
        else:
            game.receptionist.adjust_suspicion(choice.on_failure_suspicion)
            game.receptionist.adjust_trust(choice.on_failure_trust)
            text = choice.failure_text
        if not text:
            text = "(Tarkistus ohi.)"
    else:
        game.receptionist.adjust_trust(choice.on_success_trust)
        game.receptionist.adjust_suspicion(choice.on_failure_suspicion)
        text = choice.success_text or choice.failure_text

    game.scene.current_node = choice.next_node
    if choice.enrollment_override is not None:
        game.scene.enrollment_status = choice.enrollment_override
    elif choice.next_node == "end":
        game.scene.enrollment_status = game.resolve_outcome()

    return text, success
