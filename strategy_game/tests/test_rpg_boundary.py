"""Executable contracts for the RPG layer's attribution and adapter boundary (issue #389).

Code-only, per `AGENTS.md` and issue #271. These exercise the two things the issued acceptance
criteria name that did not previously hold -- a real attribution file behind the pointer in
`rpg/fate.py`, and a future adapter boundary between the RPG layer and faction strategy/simulation --
plus the NoöPunk invariants that must never regress: natural PSI separate from tech, and no forced
stack or resleeving.

Run:
    python -m unittest discover -s strategy_game/tests -p "test_rpg_boundary.py"
"""

from __future__ import annotations

import inspect
import re
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from strategy_game.rpg import fate, ports  # noqa: E402
from strategy_game.rpg.fate import Action, Character, ResourceError  # noqa: E402

RPG_DIR = Path(fate.__file__).parent


class AttributionPointerTests(unittest.TestCase):
    """The pointer in shipped code must resolve to a real file."""

    def test_the_referenced_attribution_file_exists(self) -> None:
        self.assertTrue((RPG_DIR / "ATTRIBUTION.md").is_file(),
                        "rpg/fate.py points at ATTRIBUTION.md, so it must exist")

    def test_every_attribution_pointer_in_the_package_resolves(self) -> None:
        """No file in rpg/ may name this file without it existing."""
        for source in RPG_DIR.glob("*.py"):
            text = source.read_text(encoding="utf-8")
            for referenced in re.findall(r"([A-Z][A-Z_]+\.md)", text):
                if referenced == "ATTRIBUTION.md":
                    self.assertTrue((RPG_DIR / referenced).is_file(),
                                    f"{source.name} references {referenced}")

    def test_attribution_names_the_fate_licence_and_evil_hat(self) -> None:
        text = (RPG_DIR / "ATTRIBUTION.md").read_text(encoding="utf-8")
        self.assertIn("Evil Hat Productions", text)
        self.assertIn("Creative Commons", text)
        self.assertIn("Attribution 3.0", text)

    def test_attribution_keeps_the_three_licences_distinct(self) -> None:
        """The issue is explicit that these are not interchangeable."""
        text = (RPG_DIR / "ATTRIBUTION.md").read_text(encoding="utf-8")
        self.assertIn("CC BY 3.0", text)
        self.assertIn("NC", text)
        self.assertIn("SA", text)

    def test_attribution_declares_unofficial_and_unendorsed(self) -> None:
        text = (RPG_DIR / "ATTRIBUTION.md").read_text(encoding="utf-8").lower()
        self.assertIn("unofficial", text)
        self.assertIn("not endorsed", text)

    def test_attribution_states_no_eclipse_phase_canon_is_imported(self) -> None:
        text = (RPG_DIR / "ATTRIBUTION.md").read_text(encoding="utf-8").lower()
        for banned in ("exsurgent", "firewall", "the fall"):
            self.assertIn(banned, text, "the exclusions must be named, not implied")

    def test_attribution_does_not_touch_the_generated_project_file(self) -> None:
        generated = ROOT / "docs" / "sources" / "ATTRIBUTION.md"
        if generated.is_file():
            self.assertIn("generated", generated.read_text(encoding="utf-8").lower()[:200])


class AdapterBoundaryTests(unittest.TestCase):
    """A real seam with no invented strategy mechanic."""

    def test_the_four_ports_are_protocols(self) -> None:
        for name in ("CharacterPort", "StrategyContextPort", "ScenePort", "SceneConsumerPort"):
            self.assertTrue(getattr(ports, name, None) is not None, name)
            self.assertTrue(getattr(ports, name)._is_protocol, name)

    def test_every_port_method_is_signature_only(self) -> None:
        """A body with a real implementation would mean a mechanic had been invented.

        Reads ``vars(protocol)`` rather than ``inspect.getmembers``: the latter also yields
        ``Protocol``'s own machinery (``_no_init_or_replace_init``), which is not ours to inspect.
        """
        for name in ("CharacterPort", "StrategyContextPort", "ScenePort", "SceneConsumerPort"):
            protocol = getattr(ports, name)
            # vars() also holds Python's own injected protocol machinery (_no_init_or_replace_init).
            methods = [m for n, m in vars(protocol).items()
                       if inspect.isfunction(m) and not n.startswith("_")]
            self.assertTrue(methods, f"{name} declares no method")
            for method in methods:
                # A signature-only body means the source ends with ``...``. Splitting on a colon
                # would break inside the annotations (``character_id: str``).
                self.assertTrue(inspect.getsource(method).rstrip().endswith("..."),
                                f"{name}.{method.__name__} has a body")

    def test_the_boundary_declares_its_rules(self) -> None:
        self.assertTrue(ports.BOUNDARY_RULES)
        joined = " ".join(ports.BOUNDARY_RULES)
        self.assertIn("no strategy, political or simulation mechanic", joined)

    def test_the_boundary_defines_no_strategy_mechanic(self) -> None:
        """Scan the code, not the prose: the docstring names these in order to forbid them."""
        source = Path(ports.__file__).read_text(encoding="utf-8")
        code = source.split('"""', 2)[-1]
        for banned in ("turn_economy", "hegemony", "threshold", "win_condition", "leader_mission",
                       "statistic"):
            self.assertNotIn(banned, code, banned)

    def test_the_boundary_imports_no_strategy_module(self) -> None:
        source = Path(ports.__file__).read_text(encoding="utf-8")
        self.assertNotIn("from ..", source)
        self.assertNotIn("import strategy_game", source)


class LayerIndependenceTests(unittest.TestCase):
    """The RPG layer stands alone: no strategy rules, no optional dependency.

    Two earlier versions of this contract were both wrong in the same direction -- one forbidden too
    much, one permitted too much. A blanket ban could not tell an intended dependency from an
    accidental one, and pinning coupling to a single "seam" broke the moment that seam was removed.
    The rule that survives is the one about *what* may cross: no strategy ENGINE module, in any file,
    with exactly one named exception for shared vocabulary.
    """

    #: Relative modules that are engine behaviour. Importing one means the layers have fused.
    FORBIDDEN_MODULES = frozenset({"core", "local_slice", "politics", "political", "session", "ports"})

    #: The single permitted exception: a shared *type*, not engine behaviour.
    SHARED_VOCABULARY = frozenset({"characters"})

    def _relative_imports(self) -> dict[str, tuple[str, ...]]:
        pattern = re.compile(r"^\s*from\s+\.\.(\w+)", re.MULTILINE)
        return {source.name: tuple(pattern.findall(source.read_text(encoding="utf-8")))
                for source in RPG_DIR.glob("*.py")}

    def test_no_module_imports_a_strategy_engine(self) -> None:
        offenders = {name: mods for name, mods in self._relative_imports().items()
                     if self.FORBIDDEN_MODULES & set(mods)}
        self.assertEqual(offenders, {}, "no rpg module may import strategy engine behaviour")

    def test_the_only_shared_vocabulary_is_the_declared_type(self) -> None:
        """One named exception, asserted -- not an open door."""
        shared = {mod for mods in self._relative_imports().values() for mod in mods}
        self.assertTrue(shared <= self.SHARED_VOCABULARY,
                        f"unexpected strategy import(s): {sorted(shared - self.SHARED_VOCABULARY)}")

    def test_the_resolution_core_does_not_depend_on_strategy_state(self) -> None:
        text = Path(fate.__file__).read_text(encoding="utf-8")
        for banned in ("WorldState", "local_slice", "politics", "session"):
            self.assertNotIn(banned, text, banned)

    def test_importing_the_layer_needs_no_optional_dependency(self) -> None:
        for source in RPG_DIR.glob("*.py"):
            text = source.read_text(encoding="utf-8")
            for banned in ("numpy", "pandas", "requests", "ollama", "openai"):
                self.assertNotIn(f"import {banned}", text, f"{source.name} imports {banned}")

    def test_the_absence_of_an_adapter_is_not_a_broken_import(self) -> None:
        import importlib
        module = importlib.import_module("strategy_game.rpg")
        self.assertTrue(hasattr(module, "Character"))


class NooPunkInvariantTests(unittest.TestCase):
    """The three non-negotiables, enforced rather than promised."""

    def test_a_biological_body_is_the_default(self) -> None:
        c = Character(id="x", name="X", aspects=["a"])
        self.assertEqual(c.body, "original_biological")

    def test_a_stack_and_resleeving_are_not_mandatory(self) -> None:
        c = Character(id="x", name="X", aspects=["a"])
        self.assertFalse(c.cortical_stack)
        self.assertFalse(c.resleeved)

    def test_psi_is_not_virus_derived_and_gear_grants_no_innate_psi(self) -> None:
        c = Character(id="x", name="X", aspects=["a"], gear=["PSI amplifier"], natural_psi=False)
        self.assertFalse(c.natural_psi)
        self.assertEqual(c.psi_abilities, [])
        with self.assertRaises(ResourceError):
            Character(id="y", name="Y", aspects=["a"], psi_abilities=["telepathy"], natural_psi=False)

    def test_natural_psi_needs_no_virus_and_no_equipment(self) -> None:
        c = Character(id="x", name="X", aspects=["a"], natural_psi=True,
                      psi_abilities=["precognitive_impressions"])
        self.assertTrue(c.natural_psi)

    def test_the_source_carries_no_viral_psi_assumption(self) -> None:
        text = Path(fate.__file__).read_text(encoding="utf-8").lower()
        self.assertNotIn("exsurgent", text)
        self.assertNotIn("infection grants", text)


class SceneDemoTests(unittest.TestCase):
    """Both demanded examples, resolved by one engine."""

    def test_the_investigation_scene_resolves_a_cyber_and_a_psi_check(self) -> None:
        out = fate.demo_investigation(seed=42)
        self.assertIs(out["cyber"].action, Action.OVERCOME)
        self.assertIs(out["psi"].action, Action.CREATE_ADVANTAGE)

    def test_the_netrunning_scene_resolves_cyber_checks_without_psi(self) -> None:
        out = fate.demo_netrunning(seed=7)
        self.assertIs(out["approach"].action, Action.OVERCOME)
        self.assertIs(out["defend"].action, Action.DEFEND)
        self.assertIn("not involved", str(out["psi"]))

    def test_netrunning_keeps_reachability_fictional_not_mechanical(self) -> None:
        self.assertIn("fiction-first", str(fate.demo_netrunning()["reachability"]))

    def test_both_demos_are_seed_reproducible(self) -> None:
        self.assertEqual(fate.demo_netrunning(3)["approach"].dice, fate.demo_netrunning(3)["approach"].dice)
        self.assertEqual(fate.demo_investigation(3)["cyber"].dice, fate.demo_investigation(3)["cyber"].dice)

    def test_one_engine_resolves_both_scene_kinds(self) -> None:
        """The same resolve() path underlies cyber and PSI; no second mechanic exists."""
        self.assertIs(fate.demo_investigation().get("cyber").__class__, fate.demo_netrunning().get("approach").__class__)


if __name__ == "__main__":  # pragma: no cover
    unittest.main()
