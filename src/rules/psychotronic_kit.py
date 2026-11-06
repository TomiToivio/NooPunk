"""The Europol rookie implant: device-first AntiPSI-0 and ESP-0 (#1261, Option A).

The expanded #1261 specification asks for a rookie who is **not Psychic** to carry two level-0 effects from
issued equipment, and for tests that prove the equipment is equipment: it grants nothing at advancement, it
needs no Psychic record, it stops when the device comes off, and it never turns a cue into evidence.

This module is the equipment permission, not a discipline. It reuses
:func:`src.rules.psi_access.device_grant` (a grant is never selectable) and
:func:`src.rules.psi_edges.active_grants` (a grant lasts while the device is carried), so there is no second
accounting system for psychotronic gear.

Nothing here sets a price, a System Strain, a range in metres or an Effort cost: those are the author's to
approve, and `docs/rules/PSI_MAGICK_PSYCHOTRONICS_1261.md` §4 says so.
"""

from __future__ import annotations

from dataclasses import dataclass, field

from .psi_access import Grant, PsiAccessError, device_grant
from .psi_edges import active_grants


class PsychotronicError(ValueError):
    """A device was asked to do something its permission does not cover."""


@dataclass(frozen=True, slots=True)
class DeviceSpec:
    """One issued psychotronic item, stated as permissions and refusals rather than numbers."""

    id: str
    name: str
    abilities: tuple[str, ...]
    requires_psychic: bool = False
    scene_scoped: bool = True
    limits: tuple[str, ...] = ()
    never: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        if not self.id.strip() or not self.name.strip():
            raise PsychotronicError("a device needs an id and a name")
        if not self.abilities:
            raise PsychotronicError(f"{self.id} grants nothing; do not issue it")
        if not self.limits:
            raise PsychotronicError(f"{self.id} must state its limits")


#: The rookie kit. Two level-0 effects, no Psychic class, no Effort, no technique progress.
ROOKIE_IMPLANT = DeviceSpec(
    id="europol.rookie.implant",
    name="Europol rookie psychotronic implant",
    abilities=("antipsi.0", "esp.0"),
    requires_psychic=False,
    scene_scoped=True,
    limits=(
        "AntiPSI-0 is a local intrusion cue and a bounded defensive response, not immunity",
        "ESP-0 is a scene-scoped anomalous-signature cue, not surveillance",
        "both effects end when the implant is removed or powered down",
        "neither effect adds a discipline, a technique, Effort or advancement progress",
    ),
    never=(
        "thought-reading",
        "a suspect's identity",
        "objective evidence of an afterlife",
        "remote surveillance",
        "a Program or hacking bypass",
    ),
)

#: One heavier field unit, included so the catalogue has a second shape and the tests can prove the
#: difference is permission rather than power.
FIELD_ANTIPSI = DeviceSpec(
    id="europol.field.antipsi",
    name="Heavy AntiPSI field unit",
    abilities=("antipsi.0", "antipsi.1"),
    requires_psychic=True,
    scene_scoped=True,
    limits=(
        "active counter-work needs an operator who can hold the field, which is a Psychic rank",
        "a sustained field is loud, power-hungry and attributable",
    ),
    never=("immunity", "Effort", "a second Metapsionics track"),
)

CATALOGUE: dict[str, DeviceSpec] = {item.id: item for item in (ROOKIE_IMPLANT, FIELD_ANTIPSI)}


@dataclass
class CarriedDevices:
    """What the character is actually wearing, and therefore what is actually in force."""

    worn: set[str] = field(default_factory=set)

    def wear(self, device_id: str) -> None:
        if device_id not in CATALOGUE:
            raise PsychotronicError(f"unknown device {device_id!r}")
        self.worn.add(device_id)

    def remove(self, device_id: str) -> None:
        self.worn.discard(device_id)

    def grants(self) -> tuple[Grant, ...]:
        grants = [
            device_grant(ability, source=device_id)
            for device_id in sorted(self.worn)
            for ability in CATALOGUE[device_id].abilities
        ]
        return active_grants(self.worn, grants)

    def abilities(self) -> frozenset[str]:
        return frozenset(grant.ability for grant in self.grants())

    def require(self, ability: str) -> Grant:
        """The grant backing an ability, or a refusal naming what the kit does provide."""
        for grant in self.grants():
            if grant.ability == ability:
                return grant
        offered = ", ".join(sorted(self.abilities())) or "nothing"
        raise PsychotronicError(f"{ability} is not available; the kit provides {offered}")

    def assert_no_psychic_requirement(self) -> None:
        """The rookie kit must work for a character with no Psychic record at all."""
        for device_id in self.worn:
            if CATALOGUE[device_id].requires_psychic:
                raise PsychotronicError(f"{device_id} needs a Psychic operator; the rookie kit does not")


@dataclass(frozen=True, slots=True)
class AnomalyCue:
    """What ESP-0 may tell a character: a cue to investigate, never a fact to present."""

    scene_id: str
    signature: str
    certainty: str
    is_evidence: bool = False
    names_a_person: bool = False

    def __post_init__(self) -> None:
        if self.is_evidence:
            raise PsychotronicError("ESP-0 never produces evidence")
        if self.names_a_person:
            raise PsychotronicError("ESP-0 never identifies a person")


@dataclass(frozen=True, slots=True)
class AntiPsiResponse:
    """What AntiPSI-0 does when something reaches for the wearer: warn, and permit a defence."""

    warning: str
    may_attempt_defence: bool = True
    immunity: bool = False
    grants_effort: bool = False

    def __post_init__(self) -> None:
        if self.immunity or self.grants_effort:
            raise PsychotronicError("AntiPSI-0 is a cue and a bounded response, not immunity or Effort")


def esp_zero(devices: CarriedDevices, *, scene_id: str, signature: str) -> AnomalyCue:
    devices.require("esp.0")
    if not scene_id.strip():
        raise PsychotronicError("an ESP cue belongs to a scene")
    return AnomalyCue(scene_id=scene_id, signature=signature, certainty="low")


def anti_psi_zero(devices: CarriedDevices, *, intrusion: str) -> AntiPsiResponse:
    devices.require("antipsi.0")
    if not intrusion.strip():
        raise PsychotronicError("AntiPSI needs to know what it is answering")
    return AntiPsiResponse(warning=f"local intrusion cue: {intrusion}")


def assert_equipment_only(devices: CarriedDevices) -> None:
    """A device grant may never become a selectable discipline or a second psychic resource."""
    for grant in devices.grants():
        if grant.selectable:
            raise PsychotronicError(f"{grant.ability} became a selectable option")
        if grant.ability not in {"antipsi.0", "esp.0", "antipsi.1"}:
            raise PsychotronicError(f"{grant.ability} is not an approved level-0/1 device effect")
