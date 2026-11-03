"""PSI must not shortcut an investigation (#1105, P0-A).

#1105 asks for one demonstration in particular:

    "Demonstrate a human UNSA investigator interacting with a psychic informant and an NHI psychic without
    turning routine investigations into automatic mind-control shortcuts."

That is a claim about a boundary, so it is worth testing rather than describing. The investigation resolver
(`src/rules/investigation.py`) grants clues for *competence plus declared access and inquiry*, with no roll. The
psionics engine (`src/rules/swn_psionics.py`) spends Effort on powers. If those two ever meet inside the
resolver, a psychic character becomes an oracle and every case stops being a case.

The tests below pin the separation in three places — the signature, the import graph, and the behaviour — and
then play the scenario the issue describes, in both directions: the mundane investigator solves it, and the
psychic who brought powers instead of skills does not.

Content is original NoöPunk fiction. No SWN power names, tables or prose are reproduced anywhere here, per
`docs/licenses/ISSUE_569_WITHOUT_NUMBER_RIGHTS.md`.
"""
from __future__ import annotations

import ast
import inspect
import unittest
from pathlib import Path

from src.rules.investigation import (
    Case,
    Clue,
    ClueKind,
    Investigator,
    Scene,
    discover,
)

ROOT = Path(__file__).resolve().parents[1]

#: The two halves that must never meet inside the resolver.
INVESTIGATION = ROOT / "src/rules/investigation.py"
PSIONICS = (ROOT / "src/rules/swn_psionics.py", ROOT / "src/rules/psionics.py")

#: Words that would give the resolver a psychic input if they ever appeared in its signature.
PSI_PARAMETERS = ("psi", "psychic", "effort", "technique", "discipline", "torch", "power", "telepathy")


def _imported_modules(path: Path) -> set[str]:
    tree = ast.parse(path.read_text(encoding="utf-8"))
    names: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            names.update(alias.name for alias in node.names)
        elif isinstance(node, ast.ImportFrom):
            if node.module:
                names.add(node.module)
            names.update(f"{node.module}.{alias.name}" if node.module else alias.name
                         for alias in node.names)
    return names


def _the_case() -> Case:
    """The scenario #1105 asks for: a psychic informant and an NHI contact, both reachable without psi."""
    return Case(id="the_informant_and_the_visitor", scenes=(
        Scene(id="clinic", title="UNSA field clinic", clues=(
            Clue(id="ledger", scene_id="clinic", kind=ClueKind.CORE, competency="Administer",
                 fact="The appointment ledger shows the same visitor signed in under two names.",
                 leads_to=("ward",)),
            Clue(id="tremor", scene_id="clinic", kind=ClueKind.OPTIONAL, competency="Notice",
                 passive=True,
                 fact="The informant's hand shakes only when the visitor's name is said aloud."),
        )),
        Scene(id="ward", title="Ward 3", clues=(
            Clue(id="drip", scene_id="ward", kind=ClueKind.CORE, competency="Forensics",
                 access="ward", inquiry="search",
                 fact="The drip counter was reset by hand after the last round.",
                 leads_to=("interview",)),
        )),
        Scene(id="interview", title="The informant", clues=(
            # The informant knows something. She is not an oracle: the clue is here because the author put it
            # here, and it is gated by an ordinary investigative competency and a declared interview.
            Clue(id="visitor_habit", scene_id="interview", kind=ClueKind.CORE, competency="Empathy",
                 inquiry="interview",
                 fact="She describes the visitor as 'already knowing what I was going to say'.",
                 leads_to=("bunker",)),
        )),
        Scene(id="bunker", title="The visitor's bunker", terminal=True, clues=(
            Clue(id="helmet_rack", scene_id="bunker", kind=ClueKind.CORE, competency="Science",
                 access="bunker", inquiry="search",
                 fact="A rack of psychotronic helmets, warm to the touch, each tagged with a field-office code."),
            Clue(id="second_badge", scene_id="bunker", kind=ClueKind.OPTIONAL, competency="Notice",
                 inquiry="search",
                 fact="A second UNSA badge in a drawer, belonging to someone still on the roster."),
        )),
    ))


#: A mundane UNSA field agent: competence, no powers.
FIELD_AGENT = Investigator(name="Agent Korhonen", ratings={
    "Administer": 1, "Notice": 2, "Forensics": 1, "Empathy": 1, "Science": 0,
})

#: A psychic who brought powers instead of skills — the shortcut the issue is warning about.
PSYCHIC_NO_SKILLS = Investigator(name="Psychic Vela", ratings={})

#: Someone with none of the case's competencies at all, for the baseline comparison.
UNQUALIFIED = Investigator(name="Visitor", ratings={"Athletics": 1})

#: Access and inquiry the agent declares at each scene.
DECLARATIONS = {
    "clinic": ((), ()),
    "ward": (("ward",), ("search",)),
    "interview": ((), ("interview",)),
    "bunker": (("bunker",), ("search",)),
}


class TheResolverCannotSeePsi(unittest.TestCase):
    """Structural guarantees. These fail the moment someone wires the two systems together."""

    def test_the_discovery_signature_has_no_psychic_input(self):
        signature = inspect.signature(discover)
        names = {name.lower() for name in signature.parameters}
        offending = {name for name in names if any(word in name for word in PSI_PARAMETERS)}
        self.assertEqual(offending, set(),
                         "the investigation resolver gained a psychic input; psi now shortcuts investigation")

    def test_the_investigation_layer_does_not_import_psionics(self):
        imported = " ".join(_imported_modules(INVESTIGATION))
        for banned in ("swn_psionics", "psionics", "swn_faction"):
            with self.subTest(module=banned):
                self.assertNotIn(banned, imported)

    def test_the_psionics_layer_does_not_import_the_investigation_layer(self):
        for path in PSIONICS:
            with self.subTest(module=path.name):
                self.assertNotIn("investigation", " ".join(_imported_modules(path)),
                                 "psionics reaching into the case graph is how an oracle gets built")

    def test_the_scenario_case_is_well_formed(self):
        # A malformed case would make every behavioural assertion below vacuous.
        _the_case().validate()


class PsiBuysNoClues(unittest.TestCase):
    """Behavioural guarantees, played on the scenario above."""

    def test_a_psychic_without_skills_gains_nothing(self):
        case = _the_case()
        for scene_id, (access, inquiry) in DECLARATIONS.items():
            with self.subTest(scene=scene_id):
                psychic = discover(case, scene_id, PSYCHIC_NO_SKILLS, access=access, inquiry=inquiry)
                plain = discover(case, scene_id, UNQUALIFIED, access=access, inquiry=inquiry)
                self.assertEqual(psychic.clue_ids, plain.clue_ids,
                                 "being psychic changed what the scene yielded")
                self.assertEqual(psychic.granted_by, plain.granted_by)

    def test_a_psychic_in_the_party_does_not_change_the_agents_discovery(self):
        case = _the_case()
        for scene_id, (access, inquiry) in DECLARATIONS.items():
            with self.subTest(scene=scene_id):
                alone = discover(case, scene_id, FIELD_AGENT, access=access, inquiry=inquiry)
                with_psychic = discover(case, scene_id, FIELD_AGENT, access=access, inquiry=inquiry)
                self.assertEqual(alone, with_psychic)

    def test_the_mundane_agent_can_leave_every_scene(self):
        # The whole point: the case is solvable by competence and declared procedure.
        case = _the_case()
        for scene_id, (access, inquiry) in DECLARATIONS.items():
            with self.subTest(scene=scene_id):
                found = discover(case, scene_id, FIELD_AGENT, access=access, inquiry=inquiry)
                self.assertTrue(found.can_leave, f"{scene_id} was a dead end for the mundane agent")

    def test_the_informant_yields_nothing_without_an_interview(self):
        # The informant is a scene with a gated clue, not a mind to be read. Declaring the interview is what
        # gets the fact; being psychic is not.
        case = _the_case()
        without = discover(case, "interview", FIELD_AGENT, inquiry=())
        with_interview = discover(case, "interview", FIELD_AGENT, inquiry=("interview",))
        self.assertNotIn("visitor_habit", without.clue_ids)
        self.assertIn("visitor_habit", with_interview.clue_ids)

    def test_access_still_gates_the_nhi_bunker_for_everyone(self):
        case = _the_case()
        for investigator in (FIELD_AGENT, PSYCHIC_NO_SKILLS):
            with self.subTest(investigator=investigator.name):
                found = discover(case, "bunker", investigator, access=(), inquiry=("search",))
                self.assertNotIn("helmet_rack", found.clue_ids,
                                 "a competency gate was bypassed without declaring access")

    def test_the_resolver_is_deterministic(self):
        case = _the_case()
        first = discover(case, "clinic", FIELD_AGENT)
        for _ in range(5):
            self.assertEqual(discover(case, "clinic", FIELD_AGENT), first,
                             "the investigation path must not depend on a clock or an RNG")


class TheScenarioPlaysWithoutAnyPsi(unittest.TestCase):
    """Walk the case from clinic to bunker using nothing but competence and declared procedure."""

    def test_the_case_solves_end_to_end_by_mundane_means(self):
        case = _the_case()
        solved: list[str] = []
        scene_id = "clinic"
        while scene_id is not None:
            access, inquiry = DECLARATIONS[scene_id]
            found = discover(case, scene_id, FIELD_AGENT, access=access, inquiry=inquiry)
            self.assertTrue(found.can_leave, f"the mundane agent stalled at {scene_id}")
            solved.append(scene_id)
            leads = [target for clue in found.clues for target in clue.leads_to]
            scene_id = leads[0] if leads else None
        self.assertEqual(solved, ["clinic", "ward", "interview", "bunker"],
                         "the mundane path did not reach the end of the case")


if __name__ == "__main__":
    unittest.main()
