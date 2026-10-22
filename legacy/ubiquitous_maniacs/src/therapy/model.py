"""Minimaalinen terapiasession pelimalli.

Tämä moduuli määrittelee rakenteen terapiasessioiden suunnittelua varten.
Se ei sisällä juonta, dialogia tai skriptattua sisältöä.

Malli perustuu kolmeen keskeiseen elementtiin:
- TherapyScene: yksi terapiasession vaihe
- Choice: pelaajan valintavaihtoehto
- AttributeCheck: Fate-tyylinen tarkistus (attribute + 4dF vs vaikeus)
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import StrEnum


# Fate Core -tikapuut
LADDER = {
    -2: "Terrible",
    -1: "Poor",
    0: "Mediocre",
    1: "Average",
    2: "Fair",
    3: "Good",
    4: "Great",
    5: "Superb",
    6: "Fantastic",
    7: "Epic",
    8: "Legendary",
}


@dataclass(frozen=True)
class AttributeCheck:
    """Fate-tyylinen attribute check.

    Attributes:
        attribute: Noöpunkin kanonisen attributen nimi.
        difficulty: Tikapuun arvo (esim. 2 = Fair).
    """

    attribute: str
    difficulty: int

    def difficulty_label(self) -> str:
        return LADDER.get(self.difficulty, str(self.difficulty))


class CheckResult(StrEnum):
    """Fate-tarkistuksen neljä mahdollista tulostasoa."""

    FAILURE = "failure"
    TIE = "tie"
    SUCCESS = "success"
    SUCCESS_WITH_STYLE = "success_with_style"


def evaluate_check(attribute_rating: int, fate_roll: int, difficulty: int) -> CheckResult:
    """Tulkitse ennalta annettu 4dF-tulos; moduuli ei itse heitä noppia."""
    shifts = attribute_rating + fate_roll - difficulty
    if shifts < 0:
        return CheckResult.FAILURE
    if shifts == 0:
        return CheckResult.TIE
    if shifts < 3:
        return CheckResult.SUCCESS
    return CheckResult.SUCCESS_WITH_STYLE


@dataclass(frozen=True)
class Choice:
    """Pelaajan valintavaihtoehto yhden kohtauksen sisällä.

    Attributes:
        id: yksilöllinen tunniste.
        text: pelaajalle näytettävä teksti.
        attribute_check: valintaan liittyvä attribute check (None = ei checkiä).
        next_scene: seuraava kohtaus, kun valinta ei vaadi tarkistusta.
        result_scenes: seuraava kohtaus tarkistuksen tulostason mukaan.
    """

    id: str
    text: str
    attribute_check: AttributeCheck | None = None
    next_scene: str | None = None
    result_scenes: dict[CheckResult, str | None] = field(default_factory=dict)

    def destination_for(self, result: CheckResult | None = None) -> str | None:
        """Palauta valinnan haaran kohde ilman sivuvaikutuksia."""
        if self.attribute_check is None:
            if result is not None:
                raise ValueError("Tarkistuksettomalle valinnalle ei anneta tulosta")
            return self.next_scene
        if result is None:
            raise ValueError("Tarkistuksen sisältävä valinta tarvitsee tuloksen")
        return self.result_scenes.get(result)


@dataclass(frozen=True)
class Outcome:
    """Yhden valinnan lopputulos pelaajalle.

    Attributes:
        choice_id: valinnan id.
        check_result: tarkistuksen tulostaso tai None.
        next_scene: seuraavan kohtauksen tunniste tai None, jos sessio päättyy.
        effects: moduulin ulkopuolelle välitettävät abstraktit tarinamerkinnät.
    """

    choice_id: str
    check_result: CheckResult | None
    next_scene: str | None
    effects: tuple[str, ...] = ()


@dataclass
class TherapyScene:
    """Yksi terapiasession vaihe.

    Attributes:
        id: yksilöllinen tunniste sessiossa.
        title: kohtauksen otsikko.
        description: kohtauksen alkukuvaus pelaajalle.
        choices: saatavilla olevat valintavaihtoehdot.
    """

    id: str
    title: str
    description: str
    choices: list[Choice] = field(default_factory=list)


@dataclass
class TherapySession:
    """Koko terapiasessio: jono kohtauksia.

    Attributes:
        day: päivänumero (1 = ensimmäinen päivä).
        title: session otsikko.
        scenes: kohtaukset järjestyksessä.
    """

    day: int
    title: str
    scenes: list[TherapyScene] = field(default_factory=list)

    def first_scene(self) -> TherapyScene | None:
        return self.scenes[0] if self.scenes else None

    def get_scene(self, scene_id: str) -> TherapyScene | None:
        for scene in self.scenes:
            if scene.id == scene_id:
                return scene
        return None

    def add_scene(self, scene: TherapyScene) -> None:
        if self.get_scene(scene.id) is not None:
            raise ValueError(f"Kohtauksen id on jo käytössä: {scene.id}")
        self.scenes.append(scene)


def build_empty_therapy_session(day: int = 1) -> TherapySession:
    """Luo tyhjän terapiasession rungon ilman sisältöä."""
    return TherapySession(day=day, title=f"Terapiasessio — Päivä {day}")
