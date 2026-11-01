"""GLOSSARY.md is the vocabulary authority; the game lexicon is generated from it (#1000).

These are executable checks, not prose checks: the generated JSON is input to the running game dictionary, so
parity here means the dictionary a player actually sees cannot drift from the glossary the author maintains.

`unittest.TestCase` rather than bare functions: CI runs `python -m unittest discover`, which collects nothing
from module-level `def test_*()`.
"""
from __future__ import annotations

import json
import re
import subprocess
import sys
import unicodedata
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
GLOSSARY = ROOT / "GLOSSARY.md"
LEXICON = ROOT / "data" / "world" / "lexicon.json"

#: Tomi's original headwords. Every one of these must survive, with its meaning intact.
TOMI_HEADWORDS = {
    "Bonjata": "to understand",
    "Bönde": "Finland that is not Helsinki",
    "Crusti": "crust punk",
    "Diili": "deal",
    "Dokata": "to drink alcohol",
    "Dänkki": "cannabis",
    "Fiilis": "feeling",
    "Frendi": "friend",
    "Fyrkka": "money",
    "Jepari": "cop",
    "Kännykkä": "mobile phone",
    "Kyttä": "cop",
    "Landepaukku": "person who lives outside of Helsinki",
    "Leffa": "movie",
    "Mesta": "place",
    "Narkata": "to use drugs",
    "Narkkari": "junkie",
    "Nisti": "junkie",
    "Hiisata": "to smoke cannabis",
    "Pummi": "bum",
    "Punkkari": "punk rocker",
    "Rafla": "restaurant",
    "Sika": "cop",
    "Skoude": "cop",
    "Stevari": "corporate cop",
    "Venaa": "wait",
    "Wallah": "I swear",
}

CATEGORIES = {"attested_modern", "attested_older", "real_borrowing", "noopunk_slang", "universe"}
PROVENANCE = {"tomi", "documented", "agent_proposed"}


def fold(value: str) -> str:
    decomposed = unicodedata.normalize("NFKD", value.casefold())
    return "".join(ch for ch in decomposed if not unicodedata.combining(ch)).strip()


def load() -> dict:
    return json.loads(LEXICON.read_text(encoding="utf-8"))


def mud_lexicon():
    """Import the MUD package by path, the same way the other root-level tests do."""
    path = str(ROOT / "mud")
    if path not in sys.path:
        sys.path.insert(0, path)
    from nopunk_mud import lexicon
    return lexicon


class GlossaryParityTests(unittest.TestCase):
    def test_the_generated_lexicon_matches_the_glossary(self) -> None:
        completed = subprocess.run(
            [sys.executable, str(ROOT / "tools" / "glossary_to_lexicon.py"), "--check"],
            cwd=ROOT, capture_output=True, text=True, timeout=120, check=False)
        self.assertEqual(completed.returncode, 0, completed.stdout + completed.stderr)

    def test_every_headword_in_the_glossary_reaches_the_lexicon(self) -> None:
        text = GLOSSARY.read_text(encoding="utf-8")
        headwords = {fold(m.group(1)) for m in re.finditer(r"(?m)^\*\s+([^–\-]+?)\s+[-–]\s+", text)}
        generated = {fold(term["word"]) for term in load()["terms"]}
        self.assertTrue(headwords, "the glossary should list headwords")
        self.assertEqual(headwords, generated)

    def test_tomi_headwords_and_meanings_are_preserved(self) -> None:
        by_word = {fold(term["word"]): term for term in load()["terms"]}
        for word, meaning in TOMI_HEADWORDS.items():
            key = fold(word)
            self.assertIn(key, by_word, f"{word}: Tomi's headword was dropped")
            self.assertEqual(by_word[key]["meaning"], meaning,
                             f"{word}: the definition changed to {by_word[key]['meaning']!r}")

    def test_every_term_declares_a_category_and_provenance(self) -> None:
        for term in load()["terms"]:
            self.assertIn(term["category"], CATEGORIES, term["word"])
            self.assertIn(term["provenance"], PROVENANCE, term["word"])
            self.assertIn(term["spoiler"], {"public", "gated"}, term["word"])

    def test_gated_terms_say_when_they_unlock(self) -> None:
        for term in load()["terms"]:
            if term["spoiler"] == "gated":
                self.assertTrue(term["note"].strip(), f"{term['word']}: needs an unlock note")


class SpoilerSafetyTests(unittest.TestCase):
    def test_the_glossary_exercises_the_gated_tier(self) -> None:
        self.assertTrue([t for t in load()["terms"] if t["spoiler"] == "gated"])

    def test_no_gated_term_is_offered_to_players(self) -> None:
        gated = {fold(t["word"]) for t in load()["terms"] if t["spoiler"] == "gated"}
        public = {fold(term.word) for term in mud_lexicon().public_terms()}
        self.assertFalse(gated & public,
                         f"gated terms leaked into the dictionary: {sorted(gated & public)}")

    def test_the_dictionary_does_not_confirm_a_gated_word_exists(self) -> None:
        """A refusal that differs from 'unknown' would leak the secret as surely as the entry would."""
        lexicon = mud_lexicon()
        gated = [t["word"] for t in load()["terms"] if t["spoiler"] == "gated"]
        self.assertEqual(lexicon.lookup(gated[0]), lexicon.lookup("not-a-word-at-all"))

    def test_the_dictionary_reads_the_generated_file_not_a_private_list(self) -> None:
        """If the words were still hard-coded, regenerating the glossary would not change them."""
        lexicon = mud_lexicon()
        self.assertGreaterEqual(len(lexicon.terms()), len(load()["terms"]))
        self.assertEqual({fold(t.word) for t in lexicon.terms()},
                         {fold(t["word"]) for t in load()["terms"]})


if __name__ == "__main__":
    unittest.main()
