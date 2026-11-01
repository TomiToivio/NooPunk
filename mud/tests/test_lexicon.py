"""Canonical glossary parity and spoiler-safe player lookup (#1000)."""
from __future__ import annotations

from nopunk_mud import lexicon


def test_glossary_is_the_authority_and_keeps_tomi_entries():
    terms = {term.word: term for term in lexicon.parse_glossary()}
    for word in ("Bonjata", "Bönde", "Jepari", "Skoude", "Stevari", "Wallah"):
        assert word in terms
    assert terms["Bonjata"].meaning == "to understand"


def test_every_public_term_is_lookupable_and_no_gated_term_is():
    public = [term for term in lexicon.parse_glossary() if term.spoiler == "public"]
    gated = [term for term in lexicon.parse_glossary() if term.spoiler != "public"]
    assert public and gated
    for term in public:
        assert term.word.casefold() in lexicon.lookup(term.word).casefold()
    for term in gated:
        assert "No public dictionary entry" in lexicon.lookup(term.word)


def test_lookup_searches_meaning_and_lists_terms():
    assert "Helsinki" in lexicon.lookup("Helsinki")
    assert "Dictionary:" in lexicon.lookup("")
    assert "Usage:" in lexicon.lookup("")


def test_unknown_word_does_not_invent_an_entry():
    assert lexicon.lookup("definitely-not-a-term") == (
        "No public dictionary entry. Some terms may require investigation.")


def test_public_terms_are_a_filtered_view_not_a_second_list():
    glossary = lexicon.parse_glossary()
    assert len(lexicon.PUBLIC_TERMS) == sum(1 for term in glossary if term.spoiler == "public")
