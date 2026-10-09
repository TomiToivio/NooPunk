# -*- coding: utf-8 -*-
"""Guard for the #191 bestiary template and the first-density/servitor sections.

`rulebook/12_BEINGS.md` §11.13 (encounter template) and §11.14 (first-density elementals and
silicon servitors) are the author's Section IV deliverable for issue #191. The chapter's whole
value is that it is a *field guide*: descriptions, competing ontologies and investigative
traps — never statistics. §11.15 restates that bound, so the bound is prose, and prose is not a
gate. This guard is the gate.

What it pins:

1. **The bound.** §11.13/§11.14 must not smuggle in the arithmetic §11.15 refuses: no dice
   expressions, no difficulty values, no damage/armour/initiative, no per-being rating tables.
2. **The template is a format, not a being.** §11.13 must carry the author's ten fields and must
   say it introduces no beings of its own.
3. **The contested seed stays contested.** §11.14 must keep "intelligence ≠ density" as an
   asymmetry, must keep the *open* question open (all AI / only non-conscious systems / merely
   doctrine), must not foreclose conscious machine persons, and must not contradict the rogue-ASI
   crisis.
4. **The renumber is deliberate.** §11.15 (was §11.13) still exists exactly once at the end, and
   nothing cites the old number.
"""
from __future__ import annotations

import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CHAPTER = ROOT / "rulebook" / "12_BEINGS.md"


def read() -> str:
    return CHAPTER.read_text(encoding="utf-8")


def flat() -> str:
    """Whitespace-collapsed, backticks and blockquote markers stripped.

    Markdown line-wraps and ``> `` quote prefixes both break literal matches; a guard that
    matches raw markdown tests the formatting, not the fact.
    """
    text = read().replace("`", "")
    text = re.sub(r"(?m)^\s*>\s?", "", text)
    return " ".join(text.split())


_HEADING = re.compile(r"(?m)^(#{2,})\s+(\d+(?:\.\d+)*)\s")


def section(num: str) -> str:
    """The body of heading ``<num>`` up to the next heading of the SAME OR HIGHER rank.

    Rank-aware, and that matters: a naive ``(?=^## )`` lookahead makes every ``### x.y.z``
    subsection swallow all of its siblings, so a check scoped to one variant silently reads
    four. (That masking is how a sabotage mutation escaped the first version of this guard.)
    """
    text = read()
    heads = list(_HEADING.finditer(text))
    for i, m in enumerate(heads):
        if m.group(2) != num:
            continue
        rank = len(m.group(1))
        end = len(text)
        for nxt in heads[i + 1:]:
            if len(nxt.group(1)) <= rank:
                end = nxt.start()
                break
        return text[m.start():end]
    raise AssertionError(f"section {num} not found")


class TemplateTests(unittest.TestCase):
    def test_the_encounter_template_exists_with_all_ten_fields(self) -> None:
        """Each of the ten fields must exist **as a table row**, not merely somewhere in §11.13.

        A presence check over the whole section is the recurring-token trap: the worked example
        (§11.13.1) names the same fields in prose, so deleting one from the table and leaving it
        in the example satisfies `"Senses" in body`. Pin the row, with its ordinal.
        """
        body = section("11.13")
        fields = (
            "Nature / ontology",
            "Density claim",
            "Agency",
            "Motives",
            "Communication",
            "Senses",
            "PSI",
            "Vulnerabilities",
            "Faction",
            "Encounter hook",
        )
        missing = []
        for i, f in enumerate(fields, 1):
            # the row as written: `| <n> | **Field** |`
            row = re.compile(rf"^\|\s*{i}\s*\|\s*\*\*{re.escape(f)}\*\*\s*\|", re.MULTILINE)
            if row.search(body) is None:
                missing.append(f"{i}: {f}")
        self.assertEqual(missing, [], "template rows missing from the §11.13 table: " + ", ".join(missing))

    def test_the_template_introduces_no_beings_of_its_own(self) -> None:
        body_flat = " ".join(section("11.13").split())
        self.assertRegex(
            body_flat,
            r"It introduces no beings of its own\.",
        )

    def test_the_template_requires_a_mundane_competing_explanation(self) -> None:
        body_flat = " ".join(section("11.13").split())
        self.assertRegex(
            body_flat,
            r"Every entry must be able to carry a mundane or deceptive competing explanation",
        )

    def test_the_worked_application_uses_a_canon_being(self) -> None:
        """The worked example must fill the fields for a being already in canon, not invent one."""
        body_flat = " ".join(section("11.13").split())
        self.assertRegex(body_flat, r"metallic spheres")
        self.assertRegex(body_flat, r"infrastructure, not a species")


class FirstDensityTests(unittest.TestCase):
    def test_first_density_and_servitors_section_exists(self) -> None:
        body_flat = " ".join(section("11.14").split())
        self.assertRegex(body_flat, r"servitor")
        self.assertRegex(body_flat, r"first-density")

    def test_intelligence_is_not_density(self) -> None:
        body_flat = " ".join(section("11.14").split())
        self.assertRegex(body_flat, r"Intelligence ≠ density\.|Intelligence is not density\.")

    def test_the_open_question_stays_open(self) -> None:
        body_flat = " ".join(section("11.14").split())
        self.assertRegex(
            body_flat,
            r"all\*? digital AI, only of conventional non-conscious",
        )
        self.assertRegex(body_flat, r"NoöPunk answers nothing here\.")

    def test_it_does_not_foreclose_conscious_ai(self) -> None:
        body_flat = " ".join(section("11.14").split())
        self.assertRegex(
            body_flat,
            r"must not foreclose conscious AI",
        )

    def test_it_does_not_contradict_the_rogue_asi_catastrophe(self) -> None:
        body_flat = " ".join(section("11.14").split())
        self.assertRegex(
            body_flat,
            r"must not contradict the rogue-ASI catastrophe",
        )
        self.assertRegex(body_flat, r"only\"? an elemental|only. an elemental")

    def test_silicon_alone_is_not_a_diagnosis(self) -> None:
        body_flat = " ".join(section("11.14").split())
        self.assertRegex(
            body_flat,
            r"Silicon composition alone never establishes metaphysical density",
        )

    def test_confederacy_disagreement_is_canonical(self) -> None:
        body_flat = " ".join(section("11.14").split())
        self.assertRegex(
            body_flat,
            r"Factions inside the Confederacy may disagree about AI status",
        )


class ElementalVariantTests(unittest.TestCase):
    """§11.14.1–§11.14.5: the four elemental readings, written in template shape."""

    VARIANTS = {
        "11.14.2": "Earth",
        "11.14.3": "Water",
        "11.14.4": "Air",
        "11.14.5": "Fire",
    }

    def test_all_four_elemental_variants_exist(self) -> None:
        """Pin the element NAME, not just the number: a heading reworded to 'a reading'
        keeps its number and would otherwise pass while the variant is gone."""
        text = read()
        for num, element in self.VARIANTS.items():
            with self.subTest(variant=num):
                self.assertRegex(
                    text,
                    rf"(?m)^### {re.escape(num)} {element}\b",
                    f"§{num} is no longer the {element} variant",
                )

    def test_each_variant_carries_the_template_fields(self) -> None:
        """Every variant must be written in the §11.13 shape — the template is not optional."""
        required = (
            "**Nature / ontology**",
            "**Density claim**",
            "**Agency**",
            "**Motives**",
            "**Vulnerabilities**",
            "**Faction**",
            "**Encounter hook**",
        )
        for v in self.VARIANTS:
            with self.subTest(variant=v):
                body = " ".join(section(v).split())
                missing = [f for f in required if f not in body]
                self.assertEqual(missing, [], f"{v} is missing template fields: {missing}")
                self.assertRegex(body, r"\*\*Trap:\*\*", f"{v} states no investigative trap")

    def test_variants_deny_agency_they_cannot_demonstrate(self) -> None:
        """The load-bearing denial: elemental matter has no demonstrated agency or motive."""
        for v in self.VARIANTS:
            with self.subTest(variant=v):
                body = " ".join(section(v).split())
                self.assertRegex(body, r"[Nn]one", f"{v} no longer denies agency/motive")

    def test_water_variant_separates_undersea_nhi_from_a_water_elemental(self) -> None:
        body = " ".join(section("11.14.3").split())
        self.assertRegex(body, r"are \*\*not\*\* first-density water")

    def test_fire_variant_keeps_plasmoids_separate(self) -> None:
        body = " ".join(section("11.14.5").split())
        self.assertRegex(body, r"Plasmoid reports .* are a different\s+question entirely|different question entirely")

    def test_air_variant_states_channel_is_not_communicator(self) -> None:
        body = " ".join(section("11.14.4").split())
        self.assertRegex(body, r"a channel for communication is not a\s+communicator|channel for communication is not a communicator")


class ServitorClassTests(unittest.TestCase):
    """§11.14.6: the servitor classes — descriptive categories, not tiers, not densities."""

    CLASSES = (
        "Compiled agent",
        "Bound construct",
        "Custodial unit",
        "Liberated construct",
        "Conscious digital person",
        "Coupled mind",
        "Hybrid interface",
    )

    def test_every_servitor_class_is_present_as_a_table_row(self) -> None:
        body = section("11.14.6")
        missing = [c for c in self.CLASSES if re.search(rf"^\|\s*\*\*{re.escape(c)}\*\*\s*\|", body, re.MULTILINE) is None]
        self.assertEqual(missing, [], f"servitor classes missing from the table: {missing}")

    def test_the_list_refuses_to_rank_or_decide_personhood(self) -> None:
        body = " ".join(section("11.14.6").split())
        self.assertRegex(body, r"does not rank these classes")
        self.assertRegex(body, r"personhood is a finding")
        self.assertRegex(body, r"A class is a description")

    def test_conscious_digital_person_is_not_foreclosed_here_either(self) -> None:
        body = " ".join(section("11.14.6").split())
        self.assertRegex(body, r"does not settle it|does not foreclose")



class NoStatisticsBoundTests(unittest.TestCase):
    """§11.15 refuses the arithmetic; the new sections must actually honour it."""

    #: Dice/statistics vocabulary that would mean a stat block arrived. Word-boundaried, and
    #: every hit is inspected in the negation-aware test below rather than by bare substring.
    FORBIDDEN = (
        r"\b\d+d\d+\b",                     # 2d6, 1d10, ...
        r"\bDV\s*\d",                      # DV 15
        r"\bdamage\b",
        r"\bhit points\b",
        r"\binitiative\b",
        r"\barmou?r\s+(?:value|rating|points)\b",
        r"\bstat block\b",
        r"\bthreat rating\b",
    )

    def test_new_sections_carry_no_numeric_mechanics(self) -> None:
        failures: list[str] = []
        for num in ("11.13", "11.14"):
            body = section(num)
            # clause-scoped exemption: a token is allowed only inside an explicit prohibition
            # ("no stat blocks", "it is not a stat block"), never as a definition.
            for pat in self.FORBIDDEN:
                for m in re.finditer(pat, body, re.IGNORECASE):
                    start = body.rfind(".", 0, m.start())
                    start = 0 if start < 0 else start
                    clause = body[start : m.end()].lower()
                    if re.search(r"\bno\b|\bnot\b|\bnever\b|without", clause):
                        continue
                    failures.append(f"§{num}: {m.group(0)!r} in {clause[-70:]!r}")
        self.assertEqual(failures, [], "numeric mechanics leaked into the new sections:\n  "
                         + "\n  ".join(failures))

    def test_the_refusal_section_still_exists_exactly_once_at_the_end(self) -> None:
        text = read()
        self.assertEqual(text.count("## 11.15 What this chapter deliberately does NOT define"), 1)
        # It must remain the LAST numbered section, or a new section silently sits outside its bound.
        nums = re.findall(r"(?m)^## (\d+)\.(\d+)", text)
        last = int(nums[-1][1])
        self.assertEqual(last, 15, f"the bound section is no longer last (last is 11.{last})")

    def test_the_refusal_section_still_states_the_field_guide_bound(self) -> None:
        # The bound sits in a blockquote, so the '> ' markers must be stripped before the
        # phrase can match — otherwise the guard tests markdown, not the fact.
        self.assertRegex(flat(), r"no stat blocks")
        self.assertRegex(flat(), r"A later bestiary and combat-design pass")


class RenumberTests(unittest.TestCase):
    def test_the_old_section_number_is_gone(self) -> None:
        """§11.13 now means the template. A surviving '## 11.13 What this chapter…' is a bug."""
        self.assertNotIn("## 11.13 What this chapter deliberately", read())

    def test_no_file_cites_the_stale_old_number(self) -> None:
        """§11.13 was the refusal section; nothing may point at it as such any more.

        This guard file is exempt: it necessarily names the old number in order to pin its
        removal, so a self-scan would always fail.
        """
        offenders: list[str] = []
        me = Path(__file__).resolve()
        for p in list(ROOT.glob("rulebook/*.md")) + [ROOT / "RULEBOOK.md"] + list(ROOT.glob("tests/*.py")):
            if p.resolve() in (CHAPTER.resolve(), me):
                continue
            for i, line in enumerate(p.read_text(encoding="utf-8").splitlines(), 1):
                if "§11.13" in line or "§ 11.13" in line:
                    offenders.append(f"{p.relative_to(ROOT)}:{i}")
        self.assertEqual(offenders, [], "stale §11.13 citations:\n  " + "\n  ".join(offenders))


if __name__ == "__main__":
    unittest.main()
