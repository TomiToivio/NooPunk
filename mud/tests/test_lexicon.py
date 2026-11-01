"""The lexicon keeps three promises: no translations, stated provenance, no spoilers (#996)."""
import json

import pytest
from nopunk_mud import lexicon


def _book() -> lexicon.Lexicon:
    book = lexicon.Lexicon()
    book.add(lexicon.Entry(term="spora", gloss="A tram.", provenance=lexicon.PROPOSED))
    book.add(lexicon.Entry(term="dösä", gloss="A bus.", provenance=lexicon.ATTESTED,
                           source="recorded in Tomi's authored text"))
    book.add(lexicon.Entry(term="Zookeeper", gloss="A power that offers protection.", tier=lexicon.DOSSIER,
                           provenance=lexicon.PROPOSED))
    return book


class TestGlossNotTranslation:
    def test_an_entry_carries_a_gloss(self) -> None:
        entry = _book().lookup("spora")
        assert entry.gloss == "A tram."

    def test_an_entry_without_a_gloss_is_refused(self) -> None:
        book = lexicon.Lexicon()
        with pytest.raises(lexicon.LexiconError):
            book.add(lexicon.Entry(term="tyhjä", gloss="   "))


class TestProvenanceIsStated:
    def test_attested_usage_without_a_source_is_refused(self) -> None:
        book = lexicon.Lexicon()
        with pytest.raises(lexicon.LexiconError, match="needs a source"):
            book.add(lexicon.Entry(term="kundi", gloss="A guy.", provenance=lexicon.ATTESTED))

    def test_attested_usage_with_a_source_is_accepted(self) -> None:
        assert _book().lookup("dösä").provenance == lexicon.ATTESTED

    def test_an_unknown_provenance_is_refused(self) -> None:
        book = lexicon.Lexicon()
        with pytest.raises(lexicon.LexiconError):
            book.add(lexicon.Entry(term="x", gloss="y", provenance="probably real"))

    def test_a_coinage_is_not_labelled_as_attested_usage(self) -> None:
        book = lexicon.Lexicon()
        book.add(lexicon.Entry(term="noosphere-lag", gloss="The delay before a shared thought arrives.",
                               provenance=lexicon.AUTHOR_NEOLOGISM))
        assert book.lookup("noosphere-lag").label() == "NoöPunk coinage"

    def test_a_proposed_term_admits_it_is_provisional(self) -> None:
        assert _book().lookup("spora").label() == "provisional term"


class TestSpoilersStayShut:
    def test_a_dossier_term_is_hidden_by_default(self) -> None:
        with pytest.raises(lexicon.LexiconError):
            _book().lookup("Zookeeper")

    def test_a_dossier_term_opens_when_unlocked(self) -> None:
        assert _book().lookup("Zookeeper", unlocked=["Zookeeper"]).term == "Zookeeper"

    def test_the_refusal_does_not_confirm_the_term_exists(self) -> None:
        """A 'locked' message would leak the secret just as surely as the entry would."""
        book = _book()
        with pytest.raises(lexicon.LexiconError) as locked:
            book.lookup("Zookeeper")
        with pytest.raises(lexicon.LexiconError) as missing:
            book.lookup("nonexistent")
        assert str(locked.value).replace("Zookeeper", "X") == str(missing.value).replace("nonexistent", "X")

    def test_search_does_not_leak_locked_entries(self) -> None:
        assert _book().search("Zoo") == []
        assert [e.term for e in _book().search("Zoo", unlocked=["Zookeeper"])] == ["Zookeeper"]

    def test_the_public_index_excludes_locked_terms(self) -> None:
        assert "Zookeeper" not in [term for term, _ in _book().index()]


class TestDeterminismAndSearch:
    def test_search_ignores_case_and_diacritics(self) -> None:
        assert [e.term for e in _book().search("DOSA")] == ["dösä"]

    def test_search_matches_the_gloss_as_well_as_the_term(self) -> None:
        assert [e.term for e in _book().search("tram")] == ["spora"]

    def test_search_order_is_stable(self) -> None:
        first = [e.term for e in _book().search("a")]
        assert first == [e.term for e in _book().search("a")]

    def test_an_empty_query_returns_nothing(self) -> None:
        assert _book().search("   ") == []

    def test_a_limit_is_honoured(self) -> None:
        assert len(_book().search("a", limit=1)) == 1


class TestStorage:
    def test_a_duplicate_term_is_refused(self) -> None:
        book = _book()
        with pytest.raises(lexicon.LexiconError):
            book.add(lexicon.Entry(term="SPORA", gloss="Again.", provenance=lexicon.PROPOSED))

    def test_an_unknown_term_is_an_error_not_a_blank(self) -> None:
        with pytest.raises(lexicon.LexiconError):
            _book().lookup("not-a-word")

    def test_the_shipped_lexicon_loads_and_is_all_proposed(self, tmp_path) -> None:
        """An agent must not assert attested usage; the seed file therefore claims none."""
        import pathlib
        root = pathlib.Path(__file__).resolve().parents[2]
        book = lexicon.Lexicon.load(root / "data" / "world" / "lexicon.json")
        assert book.public_terms
        assert all(e.provenance != lexicon.ATTESTED for e in book.entries.values())
        assert book.locked_terms, "the dossier tier should be exercised by the seed data"

    def test_finnish_letters_survive_a_round_trip(self, tmp_path) -> None:
        payload = {"format": "nopunk-lexicon-v1", "entries": [
            {"term": "dösä", "gloss": "A bus.", "provenance": "proposed", "tier": "public"}]}
        path = tmp_path / "lexicon.json"
        path.write_text(json.dumps(payload, ensure_ascii=False), encoding="utf-8")
        assert "dösä" in path.read_text(encoding="utf-8")
        assert lexicon.Lexicon.load(path).lookup("dösä").term == "dösä"
