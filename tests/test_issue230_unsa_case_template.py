"""Issue #230: no lore or unapproved mechanics in GM case worksheet."""
import json
import unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
DOC=ROOT/"data/rules/unsa_case_template.json"

class GMCaseTemplateTests(unittest.TestCase):
    def test_template_keeps_the_existing_four_domain_doctrine(self):
        t=json.loads(DOC.read_text(encoding="utf-8"))
        self.assertEqual(t["format"],"noopunk.gm.case_template")
        self.assertEqual(t["setting"],"Helsinki / UNSA")
        self.assertEqual(set(t["fields"]["domain_leads"]),{"physical","cybernetic","social","psychic_noospace"})
        self.assertTrue(all(isinstance(v,list) and not v for v in t["fields"]["domain_leads"].values()))

    def test_balance_and_no_softlock_review(self):
        t=json.loads(DOC.read_text(encoding="utf-8"))
        self.assertEqual(set(t["review"]),{"simulationism","narrativism","gamism","clue_access","llm_safety"})
        self.assertIn("single-roll",t["review"]["clue_access"])

    def test_no_invented_stats_npcs_or_case_canon(self):
        t=json.loads(DOC.read_text(encoding="utf-8"))
        for key in ("case_id","hook","core_question","initial_scene","investigator"):
            self.assertEqual(t["fields"][key],"")
        self.assertIn("invents no difficulty",t["rules"]["numeric_mechanics"])
        self.assertIn("leads",t["rules"]["psi_as_lead"])

if __name__=="__main__":
    unittest.main()
