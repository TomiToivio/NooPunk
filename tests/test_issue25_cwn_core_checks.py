# -*- coding: utf-8 -*-
"""Regression tests for issue #25 — the CWN core skill-check conversion.

The author decision is **Core checks → MODIFY**: NoöPunk adopts the Cities Without
Number SRD's `2d6 + skill level + attribute modifier` engine and its
`6 / 8 / 10 / 12 / 14+` ladder, **except** that it keeps its own six attributes and
its wider **−3..+3** ordinary-human modifier range.

This file guards three things that pull in opposite directions, which is why it is
worth having:

1. **CWN actually landed.** The 2d6 structure, the ladder, the GM-calls procedure,
   the situational band, aid, the opposed PC-wins-ties rule and the NPC guidance are
   all present, and the old 3d6 canon is gone.
2. **NoöPunk's divergences survived.** A conversion agent that "completed" the port
   by importing CWN's narrower attribute scale would have destroyed the one thing
   the issue explicitly protects, so the −3..+3 range and the six attributes are
   pinned.
3. **Nothing else came along.** CWN's combat, saving throws, advancement, Foci,
   Edges, cyberdecks and hacking rules are *not* part of this task. A conversion
   that widened into them would be the expensive failure mode.

Run: python3 -m unittest discover -s tests -p 'test_*.py'
"""

from __future__ import annotations

import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

RULEBOOK = ROOT / "RULEBOOK.md"
AGENTS = ROOT / "AGENTS.md"
README = ROOT / "README.md"
POLICY = ROOT / "docs" / "CWN_CHASSIS.md"
GODOT_DOC = ROOT / "docs" / "GODOT_ARCHITECTURE.md"
CONCORDIA_DOC = ROOT / "docs" / "CONCORDIA_ARCHITECTURE.md"
CORE_JSON = ROOT / "data" / "rules" / "core.json"
GODOT_ADAPTER = ROOT / "src" / "godot" / "core_rules.gd"
CONCORDIA_MECHANICS = ROOT / "src" / "concordia_runtime" / "mechanics.py"
CORE_PY = ROOT / "src" / "rules" / "core.py"

#: The canonical difficulty ladder. `14+` is open-ended, so it is listed separately.
LADDER = (6, 8, 10, 12)
OPEN_ENDED = "14+"

#: Names from the withdrawn ladder. They must not survive as skill-check canon.
WITHDRAWN_LADDER = ("easiest", "easier", "easy", "impossible")

#: Subsystems this issue explicitly forbids importing from CWN.
#: Note: "initiative" is deliberately absent. It legitimately appears in
#: RULEBOOK §10's own reserved list, so it cannot distinguish "reserved" from
#: "imported" -- the §10 UNSPECIFIED assertion above covers combat instead.
NOT_IMPORTED = ("saving throw", "saving throws", "armor class",
                "foci", "edges", "backgrounds", "character advancement",
                "cyberdeck", "trauma die", "system strain")


def _text(path: Path) -> str:
    return Path(path).read_text(encoding="utf-8")


def _flat(path: Path | str) -> str:
    """Lowercase, collapse whitespace, strip emphasis.

    Emphasis has to go: the rulebook writes claims like "is **no longer** canonical"
    and "**Unskilled is not level-0**", and a naive substring search misses the very
    sentences that carry the rule. Accepts either a path or already-read text.
    """
    raw = path if isinstance(path, str) else _text(path)
    return " ".join(raw.replace("*", "").split()).lower()


def _section(heading: str, next_heading: str) -> str:
    text = _text(RULEBOOK)
    start = text.index(heading)
    end = text.index(next_heading, start)
    return text[start:end]


def _ladder(text: str) -> dict[int | str, str]:
    """Parse the difficulty table into {rating: meaning}."""
    rows: dict[int | str, str] = {}
    for line in text.splitlines():
        line = line.strip()
        if not line.startswith("|"):
            continue
        cells = [c.strip().replace("*", "") for c in line.strip("|").split("|")]
        if len(cells) < 2 or set(cells[0]) <= set("-: "):
            continue
        raw = cells[0]
        if raw in ("Difficulty", "difficulty"):
            continue
        rating: int | str = int(raw) if raw.isdigit() else raw
        rows[rating] = cells[1]
    return rows


class CheckEngineTests(unittest.TestCase):
    """The 2d6 engine must be canonical."""

    def test_the_formula_is_2d6_plus_skill_plus_attribute(self) -> None:
        flat = _flat(RULEBOOK)
        self.assertIn(
            "total = 2d6 + relevant skill level + relevant attribute modifier "
            "+ other applicable modifiers", flat)

    def test_success_is_total_meets_or_exceeds_difficulty(self) -> None:
        self.assertIn("success = total >= difficulty", _flat(RULEBOOK))

    def test_the_die_is_two_dice(self) -> None:
        """2..12, the whole point of the conversion."""
        flat = _flat(RULEBOOK)
        self.assertIn("2d6 roll is two six-sided dice summed, giving 2..12", flat)

    def test_skill_level_feeds_the_check(self) -> None:
        """#22 owns the scale; #25 must consume it, not restate it differently."""
        flat = _flat(RULEBOOK)
        self.assertIn("+0..+4", flat)
        self.assertIn("level-0 through level-4", flat)


class LadderTests(unittest.TestCase):
    """The CWN ladder replaces 3/6/9/12/15/18."""

    def setUp(self) -> None:
        self.ladder = _ladder(_section("### 4.1", "### 4.2"))

    def test_every_rating_is_present(self) -> None:
        for rating in LADDER:
            with self.subTest(rating=rating):
                self.assertIn(rating, self.ladder)
        self.assertIn(OPEN_ENDED, self.ladder)

    def test_no_extra_ratings_were_invented(self) -> None:
        expected = set(LADDER) | {OPEN_ENDED}
        self.assertEqual(set(self.ladder), expected)

    def test_meanings_match_the_srd(self) -> None:
        """The practical meaning is what makes a ladder usable at the table."""
        expectations = {
            6: ("relatively simple", "regular background"),
            8: ("significant challenge", "competent professional"),
            10: ("skilled expert",),
            12: ("true master", "reliability"),
            OPEN_ENDED: ("true master", "probably fail"),
        }
        for rating, phrases in expectations.items():
            with self.subTest(rating=rating):
                meaning = self.ladder[rating].lower()
                for phrase in phrases:
                    self.assertIn(phrase, meaning)

    def test_the_old_ladder_is_no_longer_canonical(self) -> None:
        flat = _flat(RULEBOOK)
        self.assertIn("no longer canonical for skill checks", flat)
        for name in WITHDRAWN_LADDER:
            with self.subTest(withdrawn=name):
                self.assertNotIn(f"| {name} |", flat)

    def test_routine_tasks_below_six_need_no_check(self) -> None:
        flat = _flat(RULEBOOK)
        self.assertIn("easier than difficulty 6", flat)
        self.assertIn("is not worth a skill check", flat)

    def test_difficulty_six_number_reuse_is_flagged(self) -> None:
        """6 keeps its number but changes meaning — the trap worth documenting.

        6 was the old `Easier` rung; it is now the floor of the new ladder. A silent
        reuse would change what an old note meant.
        """
        flat = _flat(RULEBOOK)
        self.assertIn("keeps its number but changes meaning", flat)

    def test_no_boundary_auto_success_or_failure(self) -> None:
        flat = _flat(RULEBOOK)
        self.assertIn("no automatic failure on a natural 2", flat)
        self.assertIn("no automatic success on a natural 12", flat)


class NoopunkDivergenceTests(unittest.TestCase):
    """The protected divergence: CWN's engine, NoöPunk's attributes."""

    def test_the_wider_attribute_range_survives(self) -> None:
        flat = _flat(RULEBOOK)
        self.assertIn("\u22123..+3", flat)
        self.assertIn("deliberate", flat)

    def test_the_generation_table_is_untouched(self) -> None:
        """The −3..+3 range is only real if generation still produces it."""
        flat = _flat(RULEBOOK)
        for row, modifier in (("| 3 | -3 |", "-3"), ("| 18 | +3 |", "+3")):
            with self.subTest(row=row):
                self.assertIn(row, flat)

    def test_the_six_attributes_survive(self) -> None:
        flat = _flat(RULEBOOK)
        for attribute in ("fitness (fit)", "reflexes (ref)", "intelligence (int)",
                          "charisma (cha)", "cybernetics (cyb)", "psyche (psy)"):
            with self.subTest(attribute=attribute):
                self.assertIn(attribute, flat)

    def test_the_range_is_not_narrowed_to_cwn(self) -> None:
        """Guard the actual regression: compressing to CWN's −2..+2."""
        canon = json.loads(_text(CORE_JSON))
        modifiers = set(canon["human_3d6_modifier"].values())
        self.assertIn(-3, modifiers)
        self.assertIn(3, modifiers)
        self.assertEqual(min(modifiers), -3)
        self.assertEqual(max(modifiers), 3)

    def test_section_4_names_the_divergence(self) -> None:
        flat = _flat(_section("## 4.", "### 4.1"))
        self.assertIn("wide", flat)


class ProcedureTests(unittest.TestCase):
    """The GM procedure, situational band, aid, opposed rule and NPC guidance."""

    def test_the_gm_calls_for_the_check(self) -> None:
        flat = _flat(RULEBOOK)
        self.assertIn("the gm calls for a skill check", flat)
        self.assertIn("the player describes what the character attempts", flat)

    def test_plausible_alternatives_let_the_player_choose(self) -> None:
        flat = _flat(RULEBOOK)
        self.assertIn("the player may pick the one most favourable to them", flat)

    def test_marginal_combinations_take_a_penalty(self) -> None:
        flat = _flat(RULEBOOK)
        self.assertIn("marginally relevant", flat)
        self.assertIn("\u22121 or \u22122 penalty", flat)

    def test_no_fixed_skill_to_attribute_table(self) -> None:
        """The single most important 'do not build this' in the issue."""
        flat = _flat(RULEBOOK)
        self.assertIn("skill-to-attribute bindings are deliberately not fixed", flat)
        self.assertIn("do not build a table", flat)

    def test_situational_band_is_minus_two_to_plus_two(self) -> None:
        flat = _flat(RULEBOOK)
        self.assertIn("modify a skill check by \u22122 to +2", flat)

    def test_the_band_does_not_cover_gear_or_aid(self) -> None:
        flat = _flat(RULEBOOK)
        self.assertIn("does not cover modifiers from gear mods, cyberware, or pc aid",
                      flat)

    def test_aiding_grants_plus_one_against_the_same_difficulty(self) -> None:
        flat = _flat(RULEBOOK)
        self.assertIn("same difficulty", flat)
        self.assertIn("the acting character gains +1", flat)

    def test_aid_is_capped_at_plus_one(self) -> None:
        flat = _flat(RULEBOOK)
        self.assertIn("the total aid bonus is capped at +1", flat)

    def test_failed_aid_has_no_extra_penalty(self) -> None:
        self.assertIn("no additional penalty", _flat(RULEBOOK))

    def test_opposed_checks_use_2d6_on_both_sides(self) -> None:
        flat = _flat(_section("### 4.3", "### 4.4"))
        self.assertIn("2d6", flat)
        self.assertIn("higher final total wins", flat)

    def test_opposed_tie_goes_to_the_player_character(self) -> None:
        flat = _flat(RULEBOOK)
        self.assertIn("on a tie, the player character wins", flat)

    def test_the_old_unresolved_tie_rule_is_gone(self) -> None:
        """It is named as superseded, but must not remain an active rule."""
        flat = _flat(RULEBOOK)
        self.assertIn("supersedes the earlier noöpunk rule", flat)
        self.assertNotIn("no tie-breaker rule is currently canonical", flat)

    def test_no_npc_generation_system_was_built(self) -> None:
        flat = _flat(RULEBOOK)
        self.assertIn("2d6 + their listed skill modifier", flat)
        self.assertIn("not an npc-generation system", flat)

    def test_npc_fallbacks_are_zero_and_minus_one(self) -> None:
        flat = _flat(_section("### 4.5", "### 4.6"))
        self.assertIn("use +0", flat)
        self.assertIn("\u22121 if it is something they would be particularly bad at",
                      flat)


class UnskilledTests(unittest.TestCase):
    """#22's vocabulary must be preserved through the conversion."""

    def test_unskilled_is_still_minus_one(self) -> None:
        flat = _flat(RULEBOOK)
        self.assertIn("unskilled -1", flat)

    def test_unskilled_is_still_outside_the_levels(self) -> None:
        self.assertIn("unskilled is not a skill level", _flat(RULEBOOK))

    def test_blocked_is_still_not_a_failed_roll(self) -> None:
        flat = _flat(RULEBOOK)
        self.assertIn("blocked attempt, not a failed roll", flat)


class HackingWithdrawalTests(unittest.TestCase):
    """#17's framework is withdrawn and hacking returns to DEFER."""

    def test_the_four_modifiers_are_withdrawn_from_canon(self) -> None:
        flat = _flat(RULEBOOK)
        self.assertIn("withdrawn from active canonical rules", flat)
        for modifier in ("bci", "compute", "connection", "infosec"):
            with self.subTest(modifier=modifier):
                self.assertIn(modifier, flat)

    def test_the_withdrawn_formula_is_not_an_active_check(self) -> None:
        flat = _flat(RULEBOOK)
        for term in ("+ bci modifier", "+ compute modifier",
                     "+ connection modifier", "+ infosec modifier"):
            with self.subTest(term=term):
                self.assertNotIn(term, flat)

    def test_concepts_are_kept_as_future_design(self) -> None:
        flat = _flat(RULEBOOK)
        self.assertIn("not a rejection", flat)
        self.assertIn("future design", flat)

    def test_chassis_marks_hacking_defer(self) -> None:
        policy = _flat(POLICY)
        self.assertIn("hacking / cyberspace", policy)
        self.assertIn("defer", policy)

    def test_chassis_marks_core_checks_modify(self) -> None:
        text = _text(POLICY)
        status = text[text.index("### Review status"):text.index("## NoöPunk decisions")]
        cells = {}
        for line in status.splitlines():
            line = line.strip()
            if not line.startswith("|"):
                continue
            parts = [c.strip().replace("*", "") for c in line.strip("|").split("|")]
            if len(parts) >= 2 and parts[0]:
                cells[parts[0].lower()] = parts[1].upper()
        self.assertEqual(cells.get("core checks"), "MODIFY")

    def test_chassis_keeps_the_skills_decision(self) -> None:
        """#25 must not revert #22's author decision."""
        self.assertEqual(
            [v for k, v in _decisions(POLICY).items() if "skill" in k], ["MODIFY"])

    def test_hacking_is_not_claimed_designed(self) -> None:
        self.assertIn("hacking is unspecified", _flat(RULEBOOK))


def _decisions(path: Path) -> dict[str, str]:
    text = _text(path)
    status = text[text.index("### Review status"):text.index("## NoöPunk decisions")]
    out = {}
    for line in status.splitlines():
        line = line.strip()
        if not line.startswith("|"):
            continue
        parts = [c.strip().replace("*", "") for c in line.strip("|").split("|")]
        if len(parts) >= 2 and parts[0]:
            out[parts[0].lower()] = parts[1].upper()
    return out


class PortDebtTests(unittest.TestCase):
    """The runtimes are stale, and the repo must say so rather than imply canon."""

    def test_rulebook_records_the_port_debt(self) -> None:
        flat = _flat(RULEBOOK)
        self.assertIn("port debt", flat)
        self.assertIn("still implement the superseded 3d6 system", flat)

    def test_the_rulebook_is_authoritative_over_the_runtime(self) -> None:
        self.assertIn("this rulebook is authoritative", _flat(RULEBOOK))

    def test_core_json_is_marked_superseded(self) -> None:
        """A runtime file claiming old canon silently is the drift #25 forbids."""
        self.assertIn("_superseded_note", _text(CORE_JSON))

    def test_the_marker_names_the_canonical_replacement(self) -> None:
        note = _flat(CORE_JSON)
        self.assertIn("2d6", note)
        self.assertIn("6/8/10/12/14+", note)

    def test_agents_records_the_port_debt(self) -> None:
        self.assertIn("port debt", _flat(AGENTS))

    def test_readme_records_the_port_debt(self) -> None:
        self.assertIn("port debt", _flat(README))

    def test_both_architecture_docs_mark_the_stale_runtime(self) -> None:
        for doc in (GODOT_DOC, CONCORDIA_DOC):
            with self.subTest(doc=doc.name):
                flat = _flat(doc)
                self.assertIn("superseded", flat)
                self.assertIn("17.1", flat)

    def test_no_runtime_was_ported(self) -> None:
        """Tabletop-first scope: the port is a separate issue, so the 3d6 stays.

        mechanics.py holds no dice code of its own -- it delegates to the shared
        resolve_check -- so the stale 3d6 lives in src/rules/core.py. Assert the
        delegation, or this would pass for the wrong reason.
        """
        self.assertIn("3d6", _flat(CORE_PY))
        self.assertIn("3d6", _flat(GODOT_ADAPTER))
        self.assertIn("resolve_check", _flat(CONCORDIA_MECHANICS))

    def test_the_runtime_still_reports_the_old_opposed_tie(self) -> None:
        """Confirms the debt is real rather than asserted."""
        canon = json.loads(_text(CORE_JSON))
        self.assertEqual(canon["opposed_tie"], "unresolved")


class NoScopeCreepTests(unittest.TestCase):
    """No other CWN subsystem may be imported by this task."""

    def test_no_other_subsystem_was_converted(self) -> None:
        flat = _flat(RULEBOOK)
        for term in NOT_IMPORTED:
            with self.subTest(term=term):
                self.assertNotIn(term, flat)

    def test_the_reserved_sections_are_still_unspecified(self) -> None:
        text = _text(RULEBOOK)
        for section in ("### 5.4 Derived statistics", "### 5.6 Advancement",
                        "## 10. Combat"):
            with self.subTest(section=section):
                start = text.index(section)
                self.assertIn("UNSPECIFIED", text[start:start + 120])

    def test_combat_and_saving_throws_stay_reserved_in_agents(self) -> None:
        flat = _flat(AGENTS)
        self.assertIn("saving throws", flat)
        self.assertIn("combat resolution", flat)

    def test_no_new_core_json_schema_for_skills(self) -> None:
        """The tabletop skill canon has no runtime numeric form yet."""
        canon = json.loads(_text(CORE_JSON))
        for key in canon:
            with self.subTest(key=key):
                self.assertNotIn("skills", key.lower())


class ProvenanceTests(unittest.TestCase):
    """CC0 provenance, stated once and consistently."""

    def test_the_rulebook_carries_the_attribution(self) -> None:
        flat = _flat(RULEBOOK)
        self.assertIn("derived from and substantially modify the cities without "
                      "number srd", flat)
        self.assertIn("not affiliated with or endorsed by sine nomine publishing", flat)

    def test_the_licence_is_cc0_in_the_canonical_doc(self) -> None:
        self.assertIn("cc0", _flat(POLICY))

    def test_provenance_is_centralised_not_scattered(self) -> None:
        """The rulebook must point at the canonical doc rather than duplicate it."""
        flat = _flat(RULEBOOK)
        self.assertIn("cwn_chassis.md", flat)
        self.assertIn("by design", flat)


if __name__ == "__main__":
    unittest.main()
