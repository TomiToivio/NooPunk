"""Tests for the NoöPunk Concordia infrastructure-only layer."""

from __future__ import annotations

import os
from pathlib import Path
import re
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from concordia_runtime.config import ConcordiaRuntimeConfig
from concordia_runtime.mechanics import resolve_structured_check, resolve_structured_opposed
from concordia_runtime.participants import GameMasterSpec, HumanPlayer, LLMAgentSpec
from concordia_runtime.session import SessionSpec
from rules import AttributeSet


class ConcordiaRuntimeTests(unittest.TestCase):
    def test_model_must_be_explicit(self) -> None:
        previous = os.environ.pop("NOOPUNK_OLLAMA_MODEL", None)
        try:
            with self.assertRaisesRegex(ValueError, "NOOPUNK_OLLAMA_MODEL"):
                ConcordiaRuntimeConfig.from_env()
        finally:
            if previous is not None:
                os.environ["NOOPUNK_OLLAMA_MODEL"] = previous

    def test_runtime_config_reads_model_without_making_it_canon(self) -> None:
        previous = os.environ.get("NOOPUNK_OLLAMA_MODEL")
        os.environ["NOOPUNK_OLLAMA_MODEL"] = "placeholder_model"
        try:
            config = ConcordiaRuntimeConfig.from_env()
            self.assertEqual(config.ollama_model, "placeholder_model")
        finally:
            if previous is None:
                os.environ.pop("NOOPUNK_OLLAMA_MODEL", None)
            else:
                os.environ["NOOPUNK_OLLAMA_MODEL"] = previous

    def test_session_is_neutral_by_default(self) -> None:
        spec = SessionSpec()
        self.assertEqual(spec.gm, GameMasterSpec())
        self.assertEqual(spec.llm_agents, ())
        self.assertIsNone(spec.human_player)
        self.assertIn("placeholder", spec.premise)

    def test_llm_agent_requires_only_runtime_identity(self) -> None:
        agent = LLMAgentSpec(name="placeholder_actor")
        self.assertEqual(agent.name, "placeholder_actor")

    def test_participant_can_carry_structured_canonical_attributes(self) -> None:
        attributes = AttributeSet({"FIT": 4, "REF": 5, "INT": 6, "CHA": 3, "CYB": 7, "PSY": 5})
        agent = LLMAgentSpec(name="placeholder_actor", attributes=attributes)
        self.assertEqual(agent.attributes["CYB"], 7)

    def test_structured_mechanics_are_code_resolved(self) -> None:
        attributes = AttributeSet({"FIT": 4, "REF": 5, "INT": 6, "CHA": 3, "CYB": 7, "PSY": 5})
        result = resolve_structured_check(
            attributes=attributes,
            attribute_id="CYB",
            target=21,
            skill_level=7,
            dice_total=8,
        )
        self.assertEqual(result["total"], 7 + 7 + 8)
        self.assertTrue(result["success"])
        opposed = resolve_structured_opposed(15, 15)
        self.assertTrue(opposed["unresolved_tie"])
        self.assertIsNone(opposed["winner"])

    def test_structured_trained_only_action_is_blocked(self) -> None:
        attributes = AttributeSet({"FIT": 5, "REF": 5, "INT": 5, "CHA": 5, "CYB": 5, "PSY": 5})
        # Issue #111 does not define an unskilled procedure; a request without a
        # skill must fail loudly rather than silently rolling at a penalty.
        with self.assertRaises(ValueError):
            resolve_structured_check(
                attributes=attributes,
                attribute_id="INT",
                target=9,
                skill_level=None,
            )

    def test_human_player_is_an_injected_input_boundary(self) -> None:
        player = HumanPlayer(
            name="placeholder_human",
            read_action=lambda prompt: "test_action",
        )
        self.assertEqual(player.choose_action("placeholder_prompt"), "test_action")

    def test_empty_human_action_is_rejected(self) -> None:
        player = HumanPlayer(read_action=lambda prompt: "  ")
        with self.assertRaises(ValueError):
            player.choose_action("placeholder_prompt")

    def test_concordia_dependency_is_pinned_to_verified_git_commit(self) -> None:
        requirement = (
            ROOT / "requirements-concordia.txt"
        ).read_text(encoding="utf-8")
        dependency_lines = [
            line.strip()
            for line in requirement.splitlines()
            if line.strip() and not line.lstrip().startswith("#")
        ]
        self.assertEqual(len(dependency_lines), 1)

        dependency = dependency_lines[0]
        self.assertRegex(
            dependency,
            re.compile(
                r"^git\+https://github\.com/google-deepmind/concordia\.git"
                r"@[0-9a-f]{40}#egg=gdm-concordia\[ollama\]$"
            ),
        )
        self.assertNotEqual(dependency, "gdm-concordia[ollama]")


if __name__ == "__main__":
    unittest.main()
