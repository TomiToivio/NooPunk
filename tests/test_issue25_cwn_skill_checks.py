# -*- coding: utf-8 -*-
"""Regression tests for issue #25: CWN-derived 2d6 skill checks."""

from __future__ import annotations

import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RULEBOOK = ROOT / "RULEBOOK.md"
AGENTS = ROOT / "AGENTS.md"
POLICY = ROOT / "docs" / "CWN_CHASSIS.md"
CORE_JSON = ROOT / "data" / "rules" / "core.json"


def text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def flat(path: Path) -> str:
    return " ".join(text(path).replace("*", "").split()).lower()


class CoreSkillCheckTests(unittest.TestCase):
    def test_formula_is_2d6_skill_attribute(self) -> None:
        self.assertIn(
            "total = 2d6 + relevant skill level + relevant attribute modifier",
            flat(RULEBOOK),
        )
        self.assertIn("success = total >= difficulty", flat(RULEBOOK))

    def test_difficulty_ladder_is_cwn_style(self) -> None:
        raw = text(RULEBOOK)
        for target in ("6", "8", "10", "12", "14+"):
            with self.subTest(target=target):
                self.assertIn(f"| **{target}** |", raw)
        self.assertIn("Anything easier than difficulty 6 generally should not require a roll.", raw)

    def test_old_skill_check_ladder_is_superseded(self) -> None:
        section = flat(RULEBOOK)
        self.assertIn("supersedes the earlier noöpunk 3d6 skill-check engine", section)
        self.assertIn("3 / 6 / 9 / 12 / 15 / 18", section)

    def test_noopunk_attribute_range_is_preserved(self) -> None:
        f = flat(RULEBOOK)
        for code in ("fitness (fit)", "reflexes (ref)", "intelligence (int)",
                     "charisma (cha)", "cybernetics (cyb)", "psyche (psy)"):
            self.assertIn(code, f)
        self.assertIn("ordinary-human -3..+3 range", f)
        self.assertIn("| 3 | -3 |", f)
        self.assertIn("| 18 | +3 |", f)

    def test_attribute_generation_stays_3d6(self) -> None:
        f = flat(RULEBOOK)
        self.assertIn("roll 3d6 independently for each of the six attributes", f)
        self.assertIn("| 3d6 roll | modifier |", f)


class ProcedureTests(unittest.TestCase):
    def test_contextual_skill_attribute_selection(self) -> None:
        f = flat(RULEBOOK)
        self.assertIn("gm selects the relevant skill and attribute", f)
        self.assertIn("not permanently bound to one attribute", f)
        self.assertIn("plausible favorable combination", f)
        self.assertIn("-1 or -2", f)

    def test_unskilled_and_training_required(self) -> None:
        f = flat(RULEBOOK)
        self.assertIn("unskilled attempt allowed", f)
        self.assertIn("apply -1", f)
        self.assertIn("training required", f)
        self.assertIn("blocked attempt", f)
        self.assertIn("no dice are rolled", f)

    def test_situational_modifiers_are_normally_bounded(self) -> None:
        self.assertIn("combined situational modifier within -2..+2", flat(RULEBOOK))

    def test_aid_is_plus_one_and_capped(self) -> None:
        f = flat(RULEBOOK)
        self.assertIn("### 4.3 aiding another character", f)
        self.assertIn("receives +1", f)
        self.assertIn("total aid bonus is capped at +1", f)

    def test_opposed_checks_and_pc_tie(self) -> None:
        f = flat(RULEBOOK)
        self.assertIn("2d6 + relevant skill level + relevant attribute modifier", f)
        self.assertIn("player character wins the tie", f)

    def test_lightweight_npc_checks(self) -> None:
        f = flat(RULEBOOK)
        self.assertIn("### 4.4 npc skill checks", f)
        self.assertIn("2d6 + the npc's listed or relevant skill modifier", f)
        self.assertIn("use +0 for ordinary unrelated competence", f)
        self.assertIn("use -1 when the npc is particularly bad", f)


class HackingDeferralTests(unittest.TestCase):
    def test_hacking_returns_to_defer(self) -> None:
        f = flat(RULEBOOK)
        self.assertIn("hacking / cyberspace is deferred", f)
        self.assertIn("withdrawn from active canon", f)

    def test_old_modifier_tables_are_not_active(self) -> None:
        raw = text(RULEBOOK)
        for heading in ("#### BCI modifier", "#### Compute modifier",
                        "#### Connection modifier", "#### Infosec defence modifier"):
            self.assertNotIn(heading, raw)

    def test_concepts_are_retained_as_future_design(self) -> None:
        f = flat(RULEBOOK)
        self.assertIn("concepts are not rejected", f)
        for term in ("bci quality", "local compute", "connection quality", "infosec hardening"):
            self.assertIn(term, f)


class ChassisAndProvenanceTests(unittest.TestCase):
    def test_review_status(self) -> None:
        raw = text(POLICY)
        status = raw[raw.index("### Review status"):raw.index("## NoöPunk decisions")]
        self.assertRegex(status, r"(?m)^\| Skills \| \*\*MODIFY\*\* \|")
        self.assertRegex(status, r"(?m)^\| Core checks \| \*\*MODIFY\*\* \|")
        self.assertRegex(status, r"(?m)^\| Hacking / cyberspace \| \*\*DEFER\*\* \|")

    def test_cc0_and_independence_note(self) -> None:
        f = flat(RULEBOOK) + " " + flat(POLICY)
        self.assertIn("cc0", f)
        self.assertIn("not affiliated with or endorsed by sine nomine publishing", f)

    def test_no_adjacent_subsystems_imported(self) -> None:
        f = flat(RULEBOOK)
        for forbidden in ("saving throw system", "armor class", "trauma die",
                          "background skill pick", "focus grants"):
            self.assertNotIn(forbidden, f)


class DigitalPortDebtTests(unittest.TestCase):
    def test_runtime_drift_is_explicit(self) -> None:
        f = flat(RULEBOOK)
        self.assertIn("explicit digital-port debt", f)
        self.assertIn("superseded 3d6 check engine", f)
        self.assertIn("not as competing canon", f)

    def test_runtime_data_is_not_silently_redefined_here(self) -> None:
        canon = json.loads(text(CORE_JSON))
        self.assertEqual(canon["unskilled_penalty"], -1)
        self.assertEqual(canon["trained_only_without_skill"], "blocked")

    def test_agents_forbid_partial_port(self) -> None:
        f = flat(AGENTS)
        self.assertIn("do not partially port #25 into one runtime", f)


if __name__ == "__main__":
    unittest.main()
