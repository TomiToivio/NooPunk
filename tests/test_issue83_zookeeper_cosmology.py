# -*- coding: utf-8 -*-
"""Regression guard for issue #83: Zookeeper cosmology, NHI ecology, and the NHI Crisis.

These are STRUCTURE guards in the style of ``test_issue60_setting_canon.py`` and
``test_issue78_four_layers.py``. Issue #83 asks for a large body of **in-universe setting
lore** — the Zookeeper cosmology (the Zoo, the probe network, the NHI ecosystem, panspermia,
plasmoids, dolphins) and the Disclosure-era history (the NHI Crisis, the Day of Disclosure,
the VALIS event, the birth of the Noösphere) — to be written into ``RULEBOOK.md``.

The issue is explicit that this is fiction ("in-universe cosmology rather than a real-world
factual claim") and that mystery and disagreement must be preserved. So this guard asserts
both the presence of the required material **and** the anti-invention constraints:

* §36 and §37 exist, are marked as NoöPunk-native setting lore, and define no mechanics;
* the core cosmology is present (Zoo, Zookeepers, probes, porous quarantine);
* the expanded lore is present (Pleiadians, hybridization, Greys, panspermia, plasmoids,
  dolphins, the ontological categories);
* the NHI Crisis / Disclosure history is present (Europe/US asymmetry, the OpenAI Incident,
  the Lady, the Galactic Law, the VALIS event, the One Universe movement, 25/25/50);
* the fictional framing and the preserved ambiguity / disagreement are present;
* the sections add no mechanics, dice, statistics, or concrete future dates.

Run: python3 -m unittest discover -s tests -p 'test_*.py'
"""
from __future__ import annotations

import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

RULEBOOK = "RULEBOOK.md"

_YEAR_RE = re.compile(r"\b20[3-9]\d\b")


def read() -> str:
    return (ROOT / RULEBOOK).read_text(encoding="utf-8")


def raw_section(number: int) -> str:
    text = read()
    marker = f"## {number}."
    if marker not in text:
        return ""
    body = text.split(marker, 1)[1]
    nxt = re.search(rf"(?m)^## \d+\.", body)
    return body[: nxt.start()] if nxt else body


def flat(number: int) -> str:
    """Emphasis-stripped, whitespace-collapsed, lowercased body of one section."""
    body = re.sub(r"[>*_`]", " ", raw_section(number))
    return " ".join(body.split()).lower()


def both() -> str:
    return flat(36) + " " + flat(37)


class SectionsExistTests(unittest.TestCase):
    def test_both_sections_exist(self) -> None:
        self.assertIn("## 36.", read())
        self.assertIn("## 37.", read())

    def test_they_are_marked_as_native_setting_lore_that_defines_no_mechanics(self) -> None:
        for number in (36, 37):
            with self.subTest(section=number):
                body = flat(number)
                self.assertIn("noöpunk native setting lore", body)
                self.assertIn("defines no mechanics", body)


class ZookeeperCosmologyTests(unittest.TestCase):
    """§36: the Zoo, the Zookeepers, the probes, and the NHI ecosystem."""

    def test_the_zoo_and_zookeepers_are_explained(self) -> None:
        body = flat(36)
        for concept in ("zookeepers", "zoo", "quarantine", "conservation"):
            with self.subTest(concept=concept):
                self.assertIn(concept, body)

    def test_the_zoo_exists_because_the_early_galaxy_was_violent(self) -> None:
        body = flat(36)
        self.assertRegex(body, r"early milky way was violent|repeatedly destroyed,\s*sterilized")
        self.assertIn("why an interstellar quarantine system was necessary", body)

    def test_the_probe_network_is_present(self) -> None:
        body = flat(36)
        self.assertIn("von neumann probes", body)
        self.assertIn("zookeeper von neumann probes", body)

    def test_the_quarantine_is_porous_and_policed(self) -> None:
        body = flat(36)
        self.assertIn("porous", body)
        self.assertIn("the local zoo is policed", body)

    def test_ambiguity_is_preserved(self) -> None:
        body = flat(36)
        self.assertIn("preserves this ambiguity", body)
        self.assertIn("deliberately leaves this unresolved", body)

    def test_the_familiar_nhi_categories_are_named(self) -> None:
        body = flat(36)
        for who in ("greys", "mantids", "reptilians", "pleiadians"):
            with self.subTest(who=who):
                self.assertIn(who, body)

    def test_pleiadians_are_a_transplanted_human_population(self) -> None:
        body = flat(36)
        self.assertRegex(
            body,
            r"humans transplanted by the zookeepers into another protected habitat",
        )
        self.assertIn("atlantis", body)
        self.assertIn("terraformed or otherwise engineered habitats", body)

    def test_the_hybridization_program_is_present(self) -> None:
        body = flat(36)
        self.assertIn("hybridization program", body)
        self.assertIn("fourth density", body)

    def test_greys_are_future_humans(self) -> None:
        self.assertIn("greys as future humans", flat(36))

    def test_mj12_is_a_breakaway_civilization(self) -> None:
        body = flat(36)
        self.assertIn("breakaway civilization", body)
        self.assertIn("not a monolithic evil conspiracy", body)

    def test_panspermia_is_plural_and_biologies_are_alternative(self) -> None:
        body = flat(36)
        self.assertIn("multiple independent waves of panspermia", body)
        self.assertIn("plural, not universal", body)
        self.assertIn("silicon", body)

    def test_plasmoids_and_dolphins(self) -> None:
        body = flat(36)
        self.assertIn("plasmoids", body)
        self.assertIn("philosophers without technology", body)
        self.assertIn("different things", body)

    def test_technology_is_not_a_universal_endpoint(self) -> None:
        body = flat(36)
        self.assertIn("not universal endpoints", body)
        self.assertIn("kardashev", body)
        self.assertIn("seti's", body)
        self.assertIn("maturity can reduce visibility rather than increase it", body)

    def test_technosignatures_are_recorded(self) -> None:
        body = flat(36)
        for sig in ("boyajian", "tabby's star", "dyson swarm", "slow dipper"):
            with self.subTest(sig=sig):
                self.assertIn(sig, body)

    def test_law_of_one_reskin_and_vallee(self) -> None:
        body = flat(36)
        self.assertRegex(body, r"law of one cosmology is fundamentally true")
        self.assertIn("council of saturn", body)
        self.assertIn("vallee", body.replace("é", "e"))
        self.assertIn("ontological", body)

    def test_the_extratempestrial_and_cryptoterrestrial_models(self) -> None:
        body = flat(36)
        self.assertIn("extratempestrial", body)
        self.assertIn("cryptoterrestrial", body)

    def test_pasulka_convergence(self) -> None:
        body = flat(36)
        self.assertIn("pasulka", body)
        self.assertIn("the zookeepers know it is one event", body)

    def test_the_ontological_categories(self) -> None:
        body = flat(36)
        for category in ("biologics", "constructs", "noetics", "plasmoids",
                         "temporals", "ecologies", "liminals"):
            with self.subTest(category=category):
                self.assertIn(category, body)

    def test_the_nazi_zookeeper_reading_is_not_the_truth(self) -> None:
        body = flat(36)
        self.assertIn("nazi zookeepers", body)
        self.assertIn("never the truth of the cosmology", body)

    def test_the_consciousness_model(self) -> None:
        body = flat(36)
        self.assertIn("consciousness model", body)
        self.assertIn("panpsychist", body)
        self.assertIn("individuation principle", body)
        self.assertIn("become a higher-order conscious agent", body)


class NhiCrisisTests(unittest.TestCase):
    """§37: the Disclosure-era history."""

    def test_europe_and_the_us_asymmetry(self) -> None:
        body = flat(37)
        self.assertIn("bureaucracy saves europe from the singularity", body)
        self.assertIn("the united states is hit hardest", body)

    def test_civil_unrest_and_raids(self) -> None:
        body = flat(37)
        self.assertIn("civil unrest and raids", body)
        self.assertIn("swat teams", body)

    def test_the_openai_incident(self) -> None:
        body = flat(37)
        self.assertIn("first agi holocaust", body)
        self.assertIn("openai incident", body)
        self.assertIn("never recovered", body)

    def test_the_day_of_disclosure_and_the_lady(self) -> None:
        body = flat(37)
        self.assertIn("the lady", body)
        self.assertIn("culturally adaptive", body)
        self.assertIn("everything is united in one", body)

    def test_the_galactic_law(self) -> None:
        body = flat(37)
        self.assertIn("life must be allowed to continue evolving", body)
        self.assertIn("they promise", body)

    def test_the_valis_event_and_one_universe_movement(self) -> None:
        body = flat(37)
        self.assertEqual("valis" in body, True)
        self.assertIn("one universe movement", body)
        self.assertIn("alien cultists", body)

    def test_the_birth_of_the_noosphere(self) -> None:
        self.assertIn("noösphere becomes consciously active", flat(37))

    def test_the_25_25_50_pattern(self) -> None:
        body = flat(37)
        self.assertIn("25 / 25 / 50", body)
        self.assertIn("one quarter", body)
        self.assertIn("half", body)

    def test_the_patchwork_earth_and_tone(self) -> None:
        body = flat(37)
        self.assertIn("patchwork earth", body)
        self.assertIn("bleak and ecstatic", body)

    def test_the_ambiguity_of_the_phenomenon_is_preserved(self) -> None:
        body = flat(37)
        self.assertRegex(
            body,
            r"no single taxonomy should completely explain|different ufo cases should have",
        )
        self.assertIn("vallee", body.replace("é", "e"))


class AntiInventionTests(unittest.TestCase):
    """#83 adds lore. It must not smuggle in mechanics, dates, or real-world claims."""

    def test_the_alternate_history_fiction_note_marks_the_real_names(self) -> None:
        body = flat(37)
        self.assertIn("alternate-history fiction note", body)
        self.assertIn("not a claim that these events occurred", body)

    def test_the_sections_invent_no_dice_or_statistics(self) -> None:
        text = both()
        for mechanic in ("2d6", "dice", "hit point", "initiative", "skill check", "armour"):
            with self.subTest(mechanic=mechanic):
                self.assertNotIn(mechanic, text)

    def test_no_concrete_future_dates_are_assigned(self) -> None:
        offenders = [m.group(0) for m in _YEAR_RE.finditer(raw_section(36) + raw_section(37))]
        self.assertEqual(offenders, [], f"§36/§37 assign concrete years: {offenders}")

    def test_the_lore_is_presented_as_in_universe_not_real_world_fact(self) -> None:
        body = flat(36)
        self.assertIn("in-universe cosmology", body)
        self.assertIn("rather than real-world fact", body)


if __name__ == "__main__":
    unittest.main()
