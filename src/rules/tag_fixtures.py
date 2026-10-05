"""Sample tag-based characters for the #51 prototype.

> **Non-canonical fixtures.** These are illustrative characters used to exercise the
> tag engine, not setting material. NoöPunk's factions, places, corporations and
> persons are author-specified, and `AGENTS.md` §1 forbids agents inventing them.
> Every name here is marked ``fixture`` so nothing can be mistaken for canon, and a
> test enforces it.

Issue #51's first implementation target asks for "3-5 sample characters" and for the
same resolver to be exercised on combat, social interaction, hacking, investigation
and psionics. These characters exist to make that possible.

Scale port (issue #111)
-----------------------
Issue #111 replaced the retired -3..+3 attribute band and 0..4 skill levels with the
canonical **1..10 STAT + 1..10 Skill + 1d10** kernel. The fixture ratings were ported
from the old band with a single documented linear map that keeps each character's
concept and relative ordering:

    old -3 -> 1, -2 -> 2, -1 -> 3, 0 -> 5, 1 -> 6, 2 -> 7, 3 -> 9

(the two half-steps widen the compressed old band so that "average" sits at 5 on the
1..10 scale, exactly like the #111 probability examples). Skill and other category
ratings used the same map, so a skill tag's rating now *is* the canonical Skill.
"""
from __future__ import annotations

from .tags import PROTOTYPE_ATTRIBUTE_SYSTEMS, Tag, transhuman_attribute

#: Marks every fixture name so a reader can see at a glance that it is not canon.
FIXTURE_PREFIX = "fixture"

#: The documented old-band -> #111 1..10 port map used for every fixture rating below.
#: old -3 -> 1, -2 -> 2, -1 -> 3, 0 -> 5, 1 -> 6, 2 -> 7, 3 -> 9.
BAND_TO_STAT = {-3: 1, -2: 2, -1: 3, 0: 5, 1: 6, 2: 7, 3: 9}


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
#: All names are fixtures. Ratings are 1..10 (issue #111); see BAND_TO_STAT.
SAMPLE_CHARACTERS: dict[str, tuple[Tag, ...]] = {
    # A street-level physical/social operator.
    "fixture:street-fixer": (
        _attr("FIT", 6), _attr("REF", 7), _attr("INT", 5),
        _attr("CHA", 3), _attr("CYB", 6), _attr("PSY", 5),
        _tag("Pistol", 7, "physical", ("combat", "firearms")),
        _tag("Urban survival", 6, "physical", ("stealth", "streets")),
        _tag("Street contacts", 7, "social", ("contacts", "negotiation")),
        _tag("Smartlink", 6, "cybernetic", ("combat", "firearms"), category="gear"),
        _tag("Wanted by a fixture corp", 3, "social", ("legal", "identity"), category="reputation"),
    ),
    # A journalist: social + investigation heavy.
    "fixture:investigative-journalist": (
        _attr("FIT", 3), _attr("REF", 5), _attr("INT", 7),
        _attr("CHA", 6), _attr("CYB", 5), _attr("PSY", 5),
        _tag("Investigative journalist", 7, "social", ("investigation", "interviews")),
        _tag("Corporate etiquette", 6, "social", ("negotiation", "corporate")),
        _tag("Pattern recognition", 7, "psychic", ("investigation", "analysis")),
        _tag("Record-and-publish rig", 6, "cybernetic", ("investigation", "media"), category="gear"),
    ),
    # A network specialist: cybernetic heavy, physically weak.
    "fixture:mesh-intruder": (
        _attr("FIT", 3), _attr("REF", 5), _attr("INT", 7),
        _attr("CHA", 3), _attr("CYB", 9), _attr("PSY", 6),
        _tag("Mesh intrusion", 9, "cybernetic", ("hacking", "network_access", "security")),
        _tag("Exploit development", 7, "cybernetic", ("hacking", "software")),
        _tag("Neural interface", 6, "cybernetic", ("hacking", "interfaces"), category="cyberware"),
        _tag("Compromised firmware", 3, "cybernetic", ("hacking", "security"), category="condition"),
    ),
    # A psionically sensitive character, and the one used for the transhuman case.
    "fixture:noosphere-sensitive": (
        _attr("FIT", 3), _attr("REF", 3), _attr("INT", 6),
        _attr("CHA", 5), _attr("CYB", 3), _attr("PSY", 7),
        _tag("Telepathy", 7, "psychic", ("psionics", "social_reading")),
        _tag("Meditative discipline", 6, "psychic", ("psionics", "resolve")),
        _tag("Trauma", 3, "psychic", ("resolve", "stress"), category="condition"),
        _tag("Noosphere attunement", 7, "psychic", ("psionics", "noosphere")),
    ),
}

#: A posthuman fixture used to exercise TranshumanTag, i.e. capability beyond the
#: ordinary-human 1..10 ceiling (#51 asks how that interaction should work). The
#: transhuman CYB rating is above HUMAN_ATTRIBUTE_MAX (10), as #111/RULEBOOK §9.2 allows
#: for an *effective* augmented STAT.
TRANSHUMAN_SAMPLE: tuple[Tag, ...] = (
    transhuman_attribute("CYB", 12, "cybernetic", source="fixture"),
    _attr("FIT", 5), _attr("REF", 6), _attr("INT", 7),
    _attr("CHA", 3), _attr("PSY", 2),
    _tag("Distributed cognition", 9, "cybernetic", ("hacking", "analysis")),
)


def fixture_names() -> list[str]:
    return [*SAMPLE_CHARACTERS, "fixture:posthuman"]
