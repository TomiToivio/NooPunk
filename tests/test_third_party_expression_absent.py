"""No third-party expression may re-enter the repository's working tree.

**Why this test exists.** Third-party dialogue from the Netflix miniseries *Maniac* (2018)
and from *Riget / The Kingdom* (1994) was imported into this repository with the
Ubiquitous Maniacs corpus and was published in `docs/STYLISTIC_INFLUENCES_MANIAC_RIGET.md`.
It was removed from the working tree, but nothing prevented it from coming back: the file
was prose, so the code-only testing policy of `AGENTS.md` and issue #271 had nothing to say
about it, and the corpus's own text contained the material a second time.

The corpus is the author's own work, so most of it stays. What must not stay is
**expression** — other people's words. Naming a work as an influence, or a character or
brand from it, is reference and stays. Quoting it is expression and does not.

This test is code-only in the sense that matters here: it asserts over **repository
contents**, not over story, rules or canon. It does not judge whether a file is good, and
it makes no claim about NoöPunk's own prose.

Two checks:

* the working tree carries no distinctive verbatim line from either work;
* the same is true of the committed tree, so a file that is added and removed between
  runs is still caught by the second check.

The second check reads the tree at ``HEAD``. That is deliberate: it is the state a reader
of the repository sees, and it is the state a clone starts from.

What this test does **not** do is assert anything about the git *history*. A deleted file
remains in old commit objects, and purging those needs a history rewrite, which is a
coordinated operation rather than a test. That gap is recorded in
`strategy_game/scenarios/UBIQUITOUS_MANIACS.md`.
"""
from __future__ import annotations

import subprocess
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

#: Distinctive verbatim lines from the two works. Each is a run of words that would not
#: occur by accident in a Finnish/English design document about them, so a match means the
#: line is present rather than that a topic is discussed.
#:
#: The Finnish entries are the corpus's *realization* of the same lines — the author's own
#: Finnish text, but written close enough to the source that it carries the same
#: expression. They are excluded too, because the point of the cleanup is that the
#: realisation is not a clean-room alternative.
MANIAC_LINES = (
    "The pattern is the pattern",
    "You've been chosen to save the",
    "Hello, friends, I'm a smart computer",
    "You'll be born again, but not as a baby",
    "Next time, prepare to take the good with the evil",
    "This test is not about the truth",
    "If you see a thing of evil",
    "Maybe we are the evil",
    "The foundation underneath Rigshospitalet",
    "Condoms are contraband",
    "It begins like this",
    "True bliss is not knowing who you are",
    "You don't have to say that, Annie",
    "Etch A Sketch",
    "Lite-Brite",
    "Sinut on valittu",
    "Kuvio on kuvio",
    "Hei ystävät",
    "Tapahtuu outoja asioita",
    "Strange things are happening",
    # The intake exchange: the corpus's own Finnish realisation of the show's lines.
    "Tutkitteko olenko androidi",
    "viruksen kantajaksi",
    "valittu kokeeseen",
    "VALITTU KOKEESEEN",
    # The translated chorus and the closing line of the prologue.
    "Hyin outoja",
    "me olemme paha",
    "epävarmuutemme",
    "kruununa työlle",
    "ravistella tiedettä",
    "ensi kerralla varautukaa",
    "Minä olen Ragnarök",
)

RIGET_LINES = (
    "Danmark, utskitet",
    "av kalk och vatten",
    "Och där: Sverige",
    "Danskjävlar",
    "Det är en jävla bra idé",
    # The show's place-name metaphor, in the corpus's own Finnish.
    "bleaching ponds",
)

#: Lines from *Paprika* (Atsuko Chiba, 2006) and from third-party simulation
#: platforms, quoted in the corpus's own analysis documents.
OTHER_LINES = (
    "strayed into the patient's dream",
    "Osanai seemed to disappear",
    "Doctor with patient",
    "Fed his mind with images",
    "Upload Any Report",
    "Living relationship graph",
    "What situation is this?",
    "What person am I?",
    "Not an officially supported Google product",
    "1M+ rinnakkaista",
)

#: Paths whose contents are never searched. A test file may name the lines it asserts
#: the absence of, so this file exempts itself. The exemption is by exact file, not by
#: directory: exempting all of ``tests/`` would let the material hide in a test fixture.
EXEMPT = ("tests/test_third_party_expression_absent.py",)


def _scan(text: str) -> list[str]:
    found = []
    for line in MANIAC_LINES + RIGET_LINES + OTHER_LINES:
        if line in text:
            found.append(line)
    return found


def _walk_text_files(root: Path) -> list[Path]:
    out: list[Path] = []
    for path in root.rglob("*"):
        if not path.is_file():
            continue
        rel = path.relative_to(root).as_posix()
        if rel.startswith(EXEMPT) or rel.startswith(".git/"):
            continue
        if path.suffix.lower() not in {".md", ".txt", ".py", ".json", ".yaml", ".yml", ".toml"}:
            continue
        out.append(path)
    return out


class ThirdPartyExpressionTests(unittest.TestCase):
    """Third-party expression must not be present in the repository's tree."""

    def test_the_working_tree_carries_no_third_party_quotation(self) -> None:
        offenders: list[str] = []
        for path in _walk_text_files(ROOT):
            try:
                text = path.read_text(encoding="utf-8", errors="replace")
            except OSError:
                continue
            hits = _scan(text)
            if hits:
                offenders.append(f"{path.relative_to(ROOT)}: {hits}")
        self.assertEqual(offenders, [], "third-party expression present in the working tree")

    def test_the_committed_tree_carries_no_third_party_quotation(self) -> None:
        """The committed state, which is what a reader and a fresh clone receive."""
        try:
            listing = subprocess.run(
                ["git", "-C", str(ROOT), "ls-tree", "-r", "-z", "--name-only", "HEAD"],
                capture_output=True, check=True, text=True,
            ).stdout
        except (OSError, subprocess.CalledProcessError) as exc:
            self.skipTest(f"git unavailable: {exc}")
        offenders: list[str] = []
        for rel in listing.split("\0"):
            if not rel or rel.startswith(EXEMPT):
                continue
            blob = subprocess.run(
                ["git", "-C", str(ROOT), "show", f"HEAD:{rel}"],
                capture_output=True,
                check=False,
            ).stdout
            if not blob:
                continue
            text = blob.decode("utf-8", errors="replace")
            hits = _scan(text)
            if hits:
                offenders.append(f"{rel}: {hits}")
        self.assertEqual(offenders, [], "third-party expression present in the committed tree")


if __name__ == "__main__":
    unittest.main()
