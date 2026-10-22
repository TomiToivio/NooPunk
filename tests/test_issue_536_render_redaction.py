"""#536: a renderer must not be the thing that leaks a secret.

CodeQL's `py/clear-text-logging-sensitive-data` flagged the render entry point
(`strategy_game/render/__main__.py`) because a `CardVisibility.PRIVATE` value can reach a
`print`. These tests pin the two halves of the fix:

* the **owning layer** refuses to render a non-public card at all, and withholds private
  leader attributes; and
* the **print boundary** redacts a sensitive-keyed value as a last line of defence.
"""
from __future__ import annotations

import json
import unittest

from strategy_game.characters import CharacterCard, CharacterFamily, render_front
from strategy_game.core import Leader, WorldState
from strategy_game.render.redaction import WITHHELD, redact, redact_mapping
from strategy_game.render.text import board_lines
from strategy_game.tabletop.cards import CardVisibility


class RedactionTests(unittest.TestCase):
    def test_a_quoted_key_is_redacted(self) -> None:
        self.assertIn(WITHHELD, redact('a "private": "secret value" b'))
        self.assertNotIn("secret value", redact('a "private": "secret value" b'))

    def test_an_unquoted_key_is_redacted(self) -> None:
        self.assertIn(WITHHELD, redact('private: "x"'))

    def test_a_compact_pair_is_redacted(self) -> None:
        self.assertIn(WITHHELD, redact('"private":"y"'))

    def test_ordinary_text_is_untouched(self) -> None:
        text = "board [scaffold-1] — 8 locations, 12 leaders"
        self.assertEqual(text, redact(text))

    def test_every_sensitive_key_is_covered(self) -> None:
        for key in ("private", "secret", "secrets", "gm_notes", "gm_secrets"):
            with self.subTest(key=key):
                self.assertIn(WITHHELD, redact(f'"{key}": "value"'))

    def test_a_mapping_drops_sensitive_keys_entirely(self) -> None:
        out = redact_mapping({"private": "x", "name": "keep"})
        self.assertEqual({"name": "keep"}, out)

    def test_a_non_mapping_is_empty(self) -> None:
        self.assertEqual({}, redact_mapping("not a mapping"))  # type: ignore[arg-type]


class RendererRefusesNonPublicCardsTests(unittest.TestCase):
    """The card layer's own rule: a renderer must not leak a secret."""

    def _card(self, visibility: CardVisibility) -> CharacterCard:
        return CharacterCard(
            identifier="c1",
            family=CharacterFamily.CANONICAL,
            display_name="Agent Kestrel",
            role="analyst",
            visibility=visibility,
            observable_facts=("seen at the north pier",),
            sources=("canon fixture",),
        )

    def test_a_private_card_is_not_rendered(self) -> None:
        front = render_front(self._card(CardVisibility.PRIVATE))
        self.assertNotIn("Agent Kestrel", front)
        self.assertNotIn("north pier", front)

    def test_a_concealed_card_is_not_rendered(self) -> None:
        front = render_front(self._card(CardVisibility.CONCEALED))
        self.assertNotIn("Agent Kestrel", front)

    def test_a_public_card_is_rendered(self) -> None:
        front = render_front(self._card(CardVisibility.PUBLIC))
        self.assertIn("Agent Kestrel", front)


class BoardWithholdsPrivateAttributesTests(unittest.TestCase):
    def test_private_leader_attributes_are_not_printed(self) -> None:
        state = WorldState(
            leaders=[
                Leader(
                    identifier="l1",
                    name="Vesa Ranta",
                    attributes={"private": "underground cell", "post": "archivist"},
                )
            ]
        )
        text = "\n".join(board_lines(state))
        self.assertNotIn("underground cell", text)
        self.assertIn("archivist", text)

    def test_public_leader_attributes_are_printed(self) -> None:
        state = WorldState(
            leaders=[Leader(identifier="l1", name="Vesa Ranta", attributes={"post": "archivist"})]
        )
        self.assertIn("archivist", "\n".join(board_lines(state)))


class JsonPayloadIsRedactedTests(unittest.TestCase):
    def test_a_private_attribute_in_the_json_payload_is_withheld(self) -> None:
        state = WorldState(
            leaders=[Leader(identifier="l1", name="Vesa Ranta", attributes={"private": "cell name"})]
        )
        payload = json.dumps(state.to_dict(), ensure_ascii=False)
        self.assertNotIn("cell name", redact(payload))


if __name__ == "__main__":
    unittest.main()
