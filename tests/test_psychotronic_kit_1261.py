"""The rookie implant is equipment, and these tests are what "equipment" has to mean (#1261).

The issue's checklist asks for a Europol rookie AntiPSI-0 + ESP-0 implant "including no-Psychic user, source
and limitation tests". Each test below is one of those words:

* **no-Psychic user** — the kit works with no Psychic record, no discipline and no Effort.
* **source** — every effect names the device it comes from, and a grant is never selectable.
* **limitation** — removal ends the grant; ESP-0 cannot become evidence or identify a person; AntiPSI-0 is
  not immunity; the heavier field unit needs an operator who actually has the rank.
"""
import unittest

from src.rules.psi_access import PC_DISCIPLINES
from src.rules.psychotronic_kit import (
    CATALOGUE,
    FIELD_ANTIPSI,
    ROOKIE_IMPLANT,
    AnomalyCue,
    AntiPsiResponse,
    CarriedDevices,
    PsychotronicError,
    anti_psi_zero,
    assert_equipment_only,
    esp_zero,
)


def rookie() -> CarriedDevices:
    carried = CarriedDevices()
    carried.wear(ROOKIE_IMPLANT.id)
    return carried


class NoPsychicUserTests(unittest.TestCase):
    def test_the_rookie_kit_needs_no_psychic_record(self):
        self.assertFalse(ROOKIE_IMPLANT.requires_psychic)
        carried = rookie()
        carried.assert_no_psychic_requirement()
        self.assertIn("esp.0", carried.abilities())
        self.assertIn("antipsi.0", carried.abilities())

    def test_the_kit_grants_no_discipline_and_no_new_resource(self):
        carried = rookie()
        assert_equipment_only(carried)
        for grant in carried.grants():
            self.assertFalse(grant.selectable, "a device grant is never a selectable option")
        self.assertEqual(set(PC_DISCIPLINES), {"Telepathy", "Telekinesis"})

    def test_a_psychic_only_device_refuses_a_rookie_kit(self):
        carried = CarriedDevices()
        carried.wear(FIELD_ANTIPSI.id)
        with self.assertRaises(PsychotronicError):
            carried.assert_no_psychic_requirement()


class SourceTests(unittest.TestCase):
    def test_every_effect_names_its_device(self):
        carried = rookie()
        for grant in carried.grants():
            self.assertEqual(grant.source, ROOKIE_IMPLANT.id)

    def test_removing_the_implant_ends_the_grant(self):
        carried = rookie()
        esp_zero(carried, scene_id="scene.ratakatu", signature="cold patch by the stairwell")
        carried.remove(ROOKIE_IMPLANT.id)
        self.assertEqual(carried.abilities(), frozenset())
        with self.assertRaises(PsychotronicError):
            esp_zero(carried, scene_id="scene.ratakatu", signature="cold patch by the stairwell")

    def test_an_unapproved_ability_is_refused(self):
        carried = rookie()
        with self.assertRaises(PsychotronicError):
            carried.require("esp.1")
        with self.assertRaises(PsychotronicError):
            carried.require("electrokinesis.0")

    def test_unknown_devices_cannot_be_worn(self):
        with self.assertRaises(PsychotronicError):
            CarriedDevices().wear("mystery.box")


class EspLimitationTests(unittest.TestCase):
    def test_esp_zero_is_a_low_certainty_scene_cue(self):
        cue = esp_zero(rookie(), scene_id="scene.kurvi", signature="a doorway that hums")
        self.assertEqual(cue.scene_id, "scene.kurvi")
        self.assertEqual(cue.certainty, "low")
        self.assertFalse(cue.is_evidence)
        self.assertFalse(cue.names_a_person)

    def test_a_cue_cannot_be_promoted_to_evidence_or_an_identity(self):
        with self.assertRaises(PsychotronicError):
            AnomalyCue(scene_id="s", signature="x", certainty="low", is_evidence=True)
        with self.assertRaises(PsychotronicError):
            AnomalyCue(scene_id="s", signature="x", certainty="low", names_a_person=True)

    def test_a_cue_needs_a_scene(self):
        with self.assertRaises(PsychotronicError):
            esp_zero(rookie(), scene_id="  ", signature="a doorway that hums")


class AntiPsiLimitationTests(unittest.TestCase):
    def test_antipsi_zero_warns_without_immunity_or_effort(self):
        response = anti_psi_zero(rookie(), intrusion="a telepathic push at the edge of hearing")
        self.assertIn("intrusion cue", response.warning)
        self.assertTrue(response.may_attempt_defence)
        self.assertFalse(response.immunity)
        self.assertFalse(response.grants_effort)

    def test_antipsi_cannot_be_declared_immunity(self):
        with self.assertRaises(PsychotronicError):
            AntiPsiResponse(warning="x", immunity=True)
        with self.assertRaises(PsychotronicError):
            AntiPsiResponse(warning="x", grants_effort=True)

    def test_antipsi_needs_to_know_what_it_answers(self):
        with self.assertRaises(PsychotronicError):
            anti_psi_zero(rookie(), intrusion=" ")


class CatalogueTests(unittest.TestCase):
    def test_every_device_states_its_limits(self):
        for device in CATALOGUE.values():
            self.assertTrue(device.limits, device.id)
            self.assertTrue(device.never, device.id)

    def test_the_rookie_kit_offers_only_level_zero_effects(self):
        self.assertEqual(set(ROOKIE_IMPLANT.abilities), {"antipsi.0", "esp.0"})

    def test_the_field_unit_is_not_free_power(self):
        self.assertTrue(FIELD_ANTIPSI.requires_psychic)
        self.assertIn("immunity", FIELD_ANTIPSI.never)


if __name__ == "__main__":
    unittest.main()
