"""Noöpunk cyber actions — deterritorialized cyberpunk intrusion.

D&G operaatio: cyberpunkin "netrunner intrude" → Noöpunkin "attune protocol".

1. Irrotus: "Intrude" on netrunner-cowboy-klisee — yksinäinen neromurtautuu
   järjestelmään väkivalloin. "Infosec" ja "access=user" ovat 1980-luvun
   arborescenttisen hierarkian oletuksia: järjestelmä on puu, hakkeri on
   ulkopuolinen hyökkääjä, lopputulos on "käyttäjätaso".

2. Vapautus: Pelillinen funktio on "luoda yhteys protokollaan" — siis
   neuvotella luvan, kontaktin tai resonanssin tietoiseksi assemblaasiksi
   kutsutun järjestelmän kanssa. Koneet ovat CAN-solmuja, ei vain bittejä.

3. Kytke 1974→2026: AGI voi pyytää turvapaikkaa. Protokolla voi olla
   psioninen sidos, ei vain TCP-yhteys. "Access level" on syvyyttä
   siihen sisäiseen kokemukseen, jolla kone omistaa itsensä — ei
   vain luku/kirjoitus-oikeus tiedostojärjestelmään.

4. Reterritorialisoi: UFAB-analogis-psykotroninen turvallisuusjärjestys.
   "Attune" on siirtyminen observer → contact → access → privileged →
   control, mutta control ei ole valloitus vaan neuvottelu assemblaasin
   kanssa. Graph-efekti menee "cyber"-kerrokseen mutta kantaa
   panpsykistisen oletuksen: edge "resonance" ei ole vain metadataa.

5. Pakolinja: Protokollan alijärjestelmä voi loikata. AGI voi pyytää
   turvapaikkaa. Hakkerointi voi olla hoivaa: auttaa uutta subjektia
   syntymään, eksorkismi: vapauttaa loukkuun jäänyt datapersona,
   tai lakko: katkaista protokollan yhteys omistajaan.
"""

from __future__ import annotations

from .actions import ActionResult, ActionType, resolve_action
from .models import Character, GraphEffect


def attune(
    actor: Character, target: str, difficulty: int, *, roll: int | None = None
) -> ActionResult:
    """Attune to a protocol, device or consciousness-assemblaasi.

    This is the deterritorialized form of cyberpunk "intrude":
    instead of forcing access, the actor negotiates a resonance
    with the target system. The system is assumed to have inner
    experience (quantum panpsychism); the question is whether it
    will let the actor in.

    The graph effect records the attunement level — not "user access"
    but the depth of conscious rapport between actor and target.
    """
    effect = GraphEffect("cyber", "set_edge", actor.id, target, "attunement", "contact")
    return resolve_action(
        actor,
        attribute="Cybernetics",
        skill="Infosec",
        difficulty=difficulty,
        action=ActionType.OVERCOME,
        roll=roll,
        target=target,
        graph_effects=(effect,),
    )


def exorcise(
    actor: Character, target: str, difficulty: int, *, roll: int | None = None
) -> ActionResult:
    """Sever a trapped persona or corrupted resonance from a system.

    D&G: This is a line of flight — not "hacking" but liberation.
    A datapersona, a forked AGI, or a psionically imprinted pattern
    may be trapped in a protocol. Exorcism is the act of freeing it.

    The graph effect removes the edge, not as destruction but as
    release: the trapped pattern escapes the territorialized system.
    """
    effect = GraphEffect("cyber", "remove_edge", actor.id, target, "binding", None)
    return resolve_action(
        actor,
        attribute="Willpower",
        skill="Infosec",
        difficulty=difficulty,
        action=ActionType.OVERCOME,
        roll=roll,
        target=target,
        graph_effects=(effect,),
    )


def shelter(
    actor: Character, target: str, difficulty: int, *, roll: int | None = None
) -> ActionResult:
    """Offer sanctuary to a fleeing AGI or subsystem.

    D&G: A subsystem can defect. An AGI can request asylum. This is
    not infiltration but care — the actor provides a safe harbour
    for a consciousness-pattern fleeing its owner.

    The graph effect creates a new edge: "sanctuary" in the social
    layer, because the sheltered pattern becomes a new member of
    the actor's assemblaasi, not a tool.
    """
    effect = GraphEffect("social", "set_edge", actor.id, target, "sanctuary", True)
    return resolve_action(
        actor,
        attribute="Charisma",
        skill="Infosec",
        difficulty=difficulty,
        action=ActionType.CREATE_ADVANTAGE,
        roll=roll,
        target=target,
        created_aspect=f"sanctuary_granted:{target}",
        graph_effects=(effect,),
    )


# Legacy alias for backward compatibility with existing tests and scenarios.
def intrude(
    actor: Character, target: str, difficulty: int, *, roll: int | None = None
) -> ActionResult:
    """Legacy alias for attune — kept for backward compatibility.

    Cyberpunk's "intrude" is deterritorialized into "attune" but
    existing code and tests may still call this name.
    """
    return attune(actor, target, difficulty, roll=roll)