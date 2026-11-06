"""Acceptance guards for the EU technology/Europol lore document (#1236)."""
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "lore" / "eu_technology_bureaucracy.md"
REGISTER = ROOT / "docs" / "DOCUMENT_REGISTER.md"


class EuTechnology1236Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.text = DOC.read_text(encoding="utf-8")
        cls.flat = " ".join(cls.text.split())
        cls.lower = cls.flat.lower()

    def test_document_exists_and_is_english(self):
        self.assertTrue(DOC.is_file())
        self.assertGreater(len(self.text), 10_000)
        self.assertNotRegex(self.text.replace("NoöPunk", "NooPunk"), r"[äöåÄÖÅ]")

    def test_all_required_sections_are_present(self):
        headings = [
            "Historical memory: WW3 and the end of Russia",
            "The design bible: military-survivable retrofuturism",
            "New European Idealism: philosophy and design movement",
            "The European AGI/ASI and autonomy ban",
            "Plato/EISS: the human-operated cybernetic apparatus",
            "Europol, Eurodef and the bureaucratic perimeter",
            "The field team: Tony German, Laura Wendt and Salla Sotavaara",
            "Equipment catalogue",
            "Police vehicle, PoliisiSanomalaite and drones",
            "Romppainen–Fujita Objective Assessment System",
            "Field cyberdeck → Plato → evidence workflow",
            "Gameplay bridges",
            "Open canon decisions",
            "Related canon",
        ]
        for heading in headings:
            with self.subTest(heading=heading):
                self.assertIn(heading, self.text)

    def test_ww3_is_fictional_and_hearsay_is_labelled(self):
        for term in [
            "Medvedev",
            "four Mil Mi-8",
            "VDV",
            "Strategic Rocket Forces",
            "World War Three",
            "Mandela-Effect",
            "IN-WORLD CLAIM",
            "not a claim about the real world",
            "suicide",
        ]:
            with self.subTest(term=term):
                self.assertIn(term.lower(), self.lower)
        self.assertRegex(self.text, r"personally strangled Putin")

    def test_design_and_emp_hardening_are_engineering_not_magic(self):
        for term in [
            "EMP",
            "shielding",
            "filtered power",
            "field servicing",
            "not magical EMP immunity",
            "New European Idealism",
            "Spinoza",
            "Kant",
            "Hegel",
            "Quantum Information Panpsychism",
            "imperial",
            "contested",
            "1980s cyberpunk",
            "1970s psychedelic",
        ]:
            with self.subTest(term=term):
                self.assertIn(term, self.lower if term.islower() else self.text)

    def test_agi_ban_is_capability_based_and_has_a_ceiling(self):
        for term in [
            "capability, autonomy, tool access, self-improvement and integrated",
            "Gemma 4 31B",
            "bounded, preauthorised automation",
            "autonomous",
            "robotics",
            "Mistral",
            "containment/research exception",
            "OPEN — author decision",
        ]:
            with self.subTest(term=term):
                self.assertIn(term.lower(), self.lower)

    def test_plato_is_not_an_agi_and_has_human_operators(self):
        for term in [
            "Plato is not a unified AGI/ASI",
            "Lisp/Prolog",
            "GOFAI",
            "narrow AI",
            "psychotronic",
            "firebreaks",
            "human operators",
            "quantum",
            "not** automatically general",
        ]:
            with self.subTest(term=term):
                self.assertIn(term.lower(), self.lower)

    def test_authority_is_graded_and_national_powers_are_kept(self):
        for term in [
            "Public OSINT",
            "Intrusive surveillance",
            "consciousness scanning",
            "Authorization as a Task",
            "necessity/proportionality",
            "Eurodef",
            "national authorities",
            "UNSA",
            "cannot arrest/search on its own authority",
            "Clue Tags",
        ]:
            with self.subTest(term=term):
                self.assertIn(term.lower(), self.lower)

    def test_field_team_connection_and_failover(self):
        for term in [
            "Tony German",
            "Laura Wendt",
            "Salla Sotavaara",
            "human field controller",
            "body cameras are always",
            "Nokia PoliisiSanomalaite",
            "EuroNET → mobile network → encrypted police radio",
            "continues recording locally",
            "marked unavailable",
            "autonomous AI never takes control",
            "cybernetic eyes",
            "**not** read minds",
        ]:
            with self.subTest(term=term):
                self.assertIn(term.lower(), self.lower)

    def test_equipment_catalogue_covers_the_required_kit(self):
        for term in [
            "Smart credentials",
            "BCI",
            "Always-on body camera",
            "External cyberdeck is standard mandatory kit",
            "implanted cyberdeck",
            "tablet",
            "Psychotronic implant, at least defensive",
            "Forensics Multimode Scanner",
            "Romppainen–Fujita Objective Assessment System",
            "Personal service weapon",
            "Less-lethal",
            "human-controllable drone",
            "Spare power",
        ]:
            with self.subTest(term=term):
                self.assertIn(term.lower(), self.lower)

    def test_rfoas_and_evidence_burden(self):
        for term in [
            "Voight-Kampff",
            "video, audio and neural feeds",
            "unregistered Hybrids and Androids",
            "admissible evidence",
            "cannot render an autonomous identity verdict",
            "higher permission tier",
            "chain of custody",
        ]:
            with self.subTest(term=term):
                self.assertIn(term.lower(), self.lower)

    def test_workflow_keeps_plato_advisory_and_salla_human(self):
        for term in [
            "Authenticate",
            "Europol internal shared case/reference database",
            "Evidence submission",
            "Restricted access",
            "Plato's role",
            "Salla's role",
            "does **not** independently issue warrants",
            "human Field Controller",
            "Do not turn routine authorized OSINT into a multi-day permit request",
        ]:
            with self.subTest(term=term):
                self.assertIn(term.lower(), self.lower)

    def test_links_resolve(self):
        links = re.findall(r"\]\(([^)]+)\)", self.text)
        self.assertTrue(links)
        for link in links:
            if link.startswith("#") or "://" in link:
                continue
            with self.subTest(link=link):
                self.assertTrue((DOC.parent / link).resolve().exists(), link)

    def test_register_row_exists(self):
        register = REGISTER.read_text(encoding="utf-8")
        self.assertIn("lore/eu_technology_bureaucracy.md", register)
        self.assertIn("#1236", register)


if __name__ == "__main__":
    unittest.main()
