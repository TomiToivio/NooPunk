"""Sample tag-based characters for the #51 prototype.

> **Non-canonical fixtures.** These are illustrative characters used to exercise the
> tag engine, not setting material. NoöPunk's factions, places, corporations and
> persons are author-specified, and `AGENTS.md` §1 forbids agents inventing them.
> Every name here is marked ``fixture`` so nothing can be mistaken for canon, and a
> test enforces it.

Issue #51's first implementation target asks for "3-5 sample characters" and for the
same resolver to be exercised on combat, social interaction, hacking, investigation
and psionics. These characters exist to make that possible.
"""
from __future__ import annotations

from .tags import PROTOTYPE_ATTRIBUTE_SYSTEMS, Tag, transhuman_attribute

#: Marks every fixture name so a reader can see at a glance that it is not canon.
FIXTURE_PREFIX = "fixture"


def _attr(name: str, rating: int) -> Tag:
    return Tag(
        name=name,
        rating=rating,
        system=PROTOTYPE_ATTRIBUTE_SYSTEMS[name],
        category="attribute",
        source="fixture",
    )


def _tag(name: str, rating: int, system: str, scope: tuple[str, ...], category: str = "skill") -> Tag:
    return Tag(name=name, rating=rating, system=system, category=category, scope=scope, source="fixture")


#: Four sample characters spanning the four systems and the different tag categories.
#: All names are fixtures.
SAMPLE_CHARACTERS: dict[str, tuple[Tag, ...]] = {
    # A street-level physical/social operator.
    "fixture:street-fixer": (
        _attr("FIT", 1), _attr("REF", 2), _attr("INT", 0),
        _attr("CHA", -1), _attr("CYB", 1), _attr("PSY", 0),
        _tag("Pistol", 2, "physical", ("combat", "firearms")),
        _tag("Urban survival", 1, "physical", ("stealth", "streets")),
        _tag("Street contacts", 2, "social", ("contacts", "negotiation")),
        _tag("Smartlink", 1, "cybernetic", ("combat", "firearms"), category="gear"),
        _tag("Wanted by a fixture corp", -2, "social", ("legal", "identity"), category="reputation"),
    ),
    # A journalist: social + investigation heavy.
    "fixture:investigative-journalist": (
        _attr("FIT", -1), _attr("REF", 0), _attr("INT", 2),
        _attr("CHA", 1), _attr("CYB", 0), _attr("PSY", 0),
        _tag("Investigative journalist", 2, "social", ("investigation", "interviews")),
        _tag("Corporate etiquette", 1, "social", ("negotiation", "corporate")),
        _tag("Pattern recognition", 2, "psychic", ("investigation", "analysis")),
        _tag("Record-and-publish rig", 1, "cybernetic", ("investigation", "media"), category="gear"),
    ),
    # A network specialist: cybernetic heavy, physically weak.
    "fixture:mesh-intruder": (
        _attr("FIT", -1), _attr("REF", 0), _attr("INT", 2),
        _attr("CHA", -1), _attr("CYB", 3), _attr("PSY", 1),
        _tag("Mesh intrusion", 3, "cybernetic", ("hacking", "network_access", "security")),
        _tag("Exploit development", 2, "cybernetic", ("hacking", "software")),
        _tag("Neural interface", 1, "cybernetic", ("hacking", "interfaces"), category="cyberware"),
        _tag("Compromised firmware", -2, "cybernetic", ("hacking", "security"), category="condition"),
    ),
    # A psionically sensitive character, and the one used for the transhuman case.
    "fixture:noosphere-sensitive": (
        _attr("FIT", -1), _attr("REF", -1), _attr("INT", 1),
        _attr("CHA", 0), _attr("CYB", -1), _attr("PSY", 3),
        _tag("Telepathy", 2, "psychic", ("psionics", "social_reading")),
        _tag("Meditative discipline", 1, "psychic", ("psionics", "resolve")),
        _tag("Trauma", -1, "psychic", ("resolve", "stress"), category="condition"),
        _tag("Noosphere attunement", 2, "psychic", ("psionics", "noosphere")),
    ),
}

#: A posthuman fixture used to exercise TranshumanTag, i.e. capability beyond the
#: ordinary-human -3..+3 ceiling (#51 asks how that interaction should work).
TRANSHUMAN_SAMPLE: tuple[Tag, ...] = (
    transhuman_attribute("CYB", 5, "cybernetic", source="fixture"),
    _attr("FIT", 0), _attr("REF", 1), _attr("INT", 2),
    _attr("CHA", -1), _attr("PSY", -2),
    _tag("Distributed cognition", 3, "cybernetic", ("hacking", "analysis")),
)


def fixture_names() -> list[str]:
    return [*SAMPLE_CHARACTERS, "fixture:posthuman"]
