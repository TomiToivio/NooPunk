"""Executable contracts for the #572 extension map — the six worked examples, chassis-neutral.

`docs/design/ISSUE_572_NOOPUNK_EXTENSIONS.md` ends with a gate: publish specific acceptance tests for
"a physical intrusion, an air-gapped target, a natural PSI attempt, a psychotronic device, a
BCI-mediated message, and an astral transition". Five of those six do not depend on a die at all —
they are about **reach, permission and locus**, which is exactly what the document says must be decided
*before* any resolution. So they can be pinned now; the numeric half stays gated on #566.

Code-only, per `AGENTS.md` and #271. Every assertion is on existing executable behaviour
(`strategy_game/cyber.py`, `strategy_game/rpg/psi.py`, `src/rules/cross_domain_state.py`,
`src/rules/equipment_catalog_index.py`) — this file adds no rule and no number.

The one place the document promises more than the code delivers is marked in `TestPsychotronicDevice`:
the map says a device-mediated session "may be used by someone who lacks natural PSI", while `psi.py`
gates on the natural capability only. The test pins the *current* state so the gap is visible rather
than assumed.

Run:
    python -m unittest discover -s strategy_game/tests -p "test_issue572_extension_contracts.py"
"""

from __future__ import annotations

import sys
import unittest
from pathlib import Path
from random import Random

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.rules import cross_domain_state as cds  # noqa: E402
from src.rules import equipment_catalog_index as catalog  # noqa: E402
from strategy_game import cyber  # noqa: E402
from strategy_game.characters import Tag  # noqa: E402
from strategy_game.rpg.fate import Character, Outcome  # noqa: E402
from strategy_game.rpg.psi import PsiMode, resolve_psi_action  # noqa: E402
from strategy_game.rpg.skills import SkillLayerError  # noqa: E402


def _actor(tags: tuple[Tag, ...] = ()) -> Character:
    return Character(
        id="actor",
        name="An actor",
        aspects=[],
        skills={"INT": 3, "SAV": 2, "WIL": 3, "COG": 2},
        tags=tags,
    )


class AccessGateTests(unittest.TestCase):
    """Contract 1 — physical intrusion, and contract 2 — the air-gapped target."""

    @classmethod
    def setUpClass(cls) -> None:
        cls.model = cyber.load_connectivity()

    def test_physical_intrusion_needs_a_body_on_site(self) -> None:
        """A local path is a route only when someone or something is actually there."""
        without = self.model.resolve_access("isolated", "acceleration", "field_netrunner")
        with_body = self.model.resolve_access(
            "isolated", "acceleration", "field_netrunner", local_presence=True
        )
        self.assertFalse(without.possible)
        self.assertTrue(with_body.possible)
        self.assertIn("locally delivered", with_body.reason)

    def test_an_air_gapped_target_cannot_be_entered_remotely_at_any_price(self) -> None:
        """No dice, no authority and no luck cross an air gap: impossibility, not difficulty.

        The *reason* changes with the era — during the NHI Crisis there is no public network left to
        argue about — but the verdict never does, and that is the contract.
        """
        for era in ("acceleration", "nhi_crisis", "after_crisis"):
            with self.subTest(era=era):
                verdict = self.model.resolve_access(
                    "isolated", era, "remote_public_service",
                    local_presence=True, authorised=True,
                )
                self.assertFalse(verdict.possible)
                self.assertTrue(verdict.reason)
                self.assertRegex(verdict.reason, r"isolated|field operation")

    def test_a_social_tie_is_not_a_network_route(self) -> None:
        """The five refused ids are the whole of that rule, and they cannot be smuggled in."""
        for refused in ("social_tie", "personal_contact", "faction_relationship",
                        "influence_edge", "network_edge"):
            with self.subTest(path=refused):
                self.assertIn(refused, self.model.refused_path_ids)
                self.assertNotIn(refused, self.model.access_paths)

    def test_a_delivered_device_creates_one_specific_path_not_a_general_one(self) -> None:
        courier = self.model.resolve_access("isolated", "acceleration", "courier_compromise")
        remote = self.model.resolve_access("isolated", "acceleration", "remote_public_service")
        self.assertTrue(courier.possible)
        self.assertFalse(remote.possible)


class Contract3NaturalPsiTests(unittest.TestCase):
    """PSI is a capability and a mode, not a network route and not a virus."""

    def test_the_capability_gate_fires_before_any_dice(self) -> None:
        with self.assertRaises(SkillLayerError) as caught:
            resolve_psi_action(_actor(), "target", PsiMode.REMOTE_PERCEPTION, 2, rng=Random(1))
        self.assertIn("REMOTE_VIEWER", str(caught.exception))

    def test_a_capability_holder_resolves_on_the_one_engine(self) -> None:
        actor = _actor((Tag("competence", "REMOTE_VIEWER"),))
        result = resolve_psi_action(actor, "target", PsiMode.REMOTE_PERCEPTION, 2, rng=Random(1))
        self.assertIsInstance(result.outcome, Outcome)

    def test_natural_psi_does_not_consult_connectivity(self) -> None:
        """The same actor sees the same target whether the site is reachable or air-gapped.

        PSI is not a remote-login: `cyber` says the target is unreachable, and `psi` still resolves.
        That asymmetry is the whole reason the family's hacking model cannot be imported for PSI.
        """
        model = cyber.load_connectivity()
        self.assertFalse(model.resolve_access("isolated", "acceleration", "remote_public_service").possible)
        actor = _actor((Tag("competence", "REMOTE_VIEWER"),))
        result = resolve_psi_action(actor, "an air-gapped terminal", PsiMode.REMOTE_PERCEPTION, 2,
                                    rng=Random(7))
        self.assertIsInstance(result.outcome, Outcome)


class TestPsychotronicDevice(unittest.TestCase):
    """Contract 4 — a psychotronic device is a technology channel, not an innate capability."""

    def test_the_catalog_carries_psychotronic_devices(self) -> None:
        entries = catalog.search_catalog("psychotronic")
        self.assertTrue(entries, "the equipment catalog must name psychotronic devices")

    def test_the_engine_still_gates_on_natural_capability_only(self) -> None:
        """Recorded gap, not a bug silently papered over.

        `ISSUE_572_NOOPUNK_EXTENSIONS.md` says a technology-driven session "may be used by someone
        who lacks natural PSI". `psi.py` has no device parameter, so today the engine refuses that
        actor. Pinned here so the claim cannot be read as implemented.
        """
        with self.assertRaises(SkillLayerError):
            resolve_psi_action(_actor(), "target", PsiMode.REMOTE_PERCEPTION, 2, rng=Random(1))


class Contract5BciMessageTests(unittest.TestCase):
    """A BCI-mediated message travels a modelled route, and the quarantine route is a crime."""

    @classmethod
    def setUpClass(cls) -> None:
        cls.model = cyber.load_connectivity()

    def test_an_unreachable_target_cannot_be_messaged(self) -> None:
        self.assertFalse(
            self.model.resolve_access("isolated", "nhi_crisis", "remote_public_service").possible
        )

    def test_an_authorised_link_can_carry_one(self) -> None:
        self.assertTrue(
            self.model.resolve_access(
                "public_gateway", "acceleration", "authorized_link", authorised=True
            ).possible
        )

    def test_the_quarantine_route_is_illegal_not_merely_hard(self) -> None:
        verdict = self.model.resolve_access(
            "isolated", "acceleration", "bridge_old_internet", local_presence=True
        )
        self.assertTrue(verdict.possible)
        self.assertTrue(verdict.is_containment_breach)
        self.assertTrue(verdict.illegality)


class Contract6AstralTransitionTests(unittest.TestCase):
    """One locus, one realm, and the body left behind."""

    def test_embodied_and_projected_are_mutually_reachable(self) -> None:
        self.assertTrue(cds.legal_transition(cds.EMBODIED, cds.ASTRAL_PROJECTED))
        self.assertTrue(cds.legal_transition(cds.ASTRAL_PROJECTED, cds.EMBODIED))

    def test_two_projected_states_are_not_directly_connected(self) -> None:
        """A dive cannot become a projection: the body is the only way between them."""
        self.assertFalse(cds.legal_transition(cds.CYBER_IMMERSED, cds.ASTRAL_PROJECTED))
        self.assertFalse(cds.legal_transition(cds.ASTRAL_PROJECTED, cds.CYBER_IMMERSED))

    def test_the_body_is_not_controllable_while_projected(self) -> None:
        self.assertTrue(cds.controls_body(cds.EMBODIED))
        self.assertFalse(cds.controls_body(cds.ASTRAL_PROJECTED))
        self.assertFalse(cds.controls_body(cds.CYBER_IMMERSED))

    def test_exactly_one_realm_and_one_locus(self) -> None:
        self.assertEqual(cds.realms_for(cds.ASTRAL_PROJECTED), frozenset({cds.NOOSPACE}))
        self.assertFalse(cds.can_act_in(cds.ASTRAL_PROJECTED, cds.PHYSICAL))
        self.assertEqual(cds.single_locus(cds.ASTRAL_PROJECTED), cds.ASTRAL_PROJECTED)
        with self.assertRaises(cds.CrossDomainError):
            cds.single_locus((cds.EMBODIED, cds.ASTRAL_PROJECTED))


if __name__ == "__main__":
    unittest.main()
