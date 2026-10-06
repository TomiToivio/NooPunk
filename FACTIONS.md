# NoöPunk factions, motivations, and reputation contexts

Status: starter library for issue #107. Canonical mechanics are in rulebook/4_SOCIAL.md. This replaces the old wholesale Eclipse Phase faction list with NoöPunk-specific design seeds.

## Faction families

Characters may belong to several formations at once. A faction is stored as US + FRONTIER Affect edges, not as a personality package.

Current NoöPunk faction families include:
- states, federations, national/local communities and Belt/habitat identities;
- AI ideological formations: accelerationist/techno-optimist, x-risk/safety, Critical AI/political-economy, moratorium/opposition and AI-rights positions;
- corporations and corporate blocs;
- Legacy Programs, Disclosure coalitions and investigators;
- transhuman, cyborg, morphological-freedom and augmentation politics;
- biological-human, bioconservative and human-sovereignty formations;
- AI/digital-person personhood, autonomy, labor and rights formations;
- NHI-related pro-contact, resistance/defense, Confederacy-oriented, Orion-opposed and quarantine/disclosure positions already present in NoöPunk lore;
- Noösphere/PSI scientific, professional, religious, skeptical and political formations;
- labor, commons, cooperative, socialist, autonomist and multitude formations, including the Panpsychic Cyborg Multitude where applicable;
- criminal/informal networks such as gangs, brokers and smugglers;
- professional/knowledge communities such as research institutes, universities, security services, media and clinics.

These are families, not a forced master list. Add named factions only when the rulebook establishes them.

## Motivation library

Recurring NoöPunk motivation targets include AI acceleration, AI safety, Critical AI, AI rights, Disclosure, secrecy, human sovereignty, transhumanism, bioconservatism, cyborgification, Noösphere, PSI, NHI cooperation, NHI resistance, nationalism, federalism, commons, corporate power, ecological survival, space expansion, personal survival, family, friendship, loyalty, love, revenge, curiosity, career, discovery, fame, wealth and community.

Each target still needs an Affect label and score. AI acceleration | Supports | +7 and AI acceleration | Opposes | -6 are both valid.

## Reputation contexts

Reputation is an edge from the evaluating faction/actor toward the character. Useful contexts emerge from actual play: local station/habitat community; employer/corporation/guild/union/cooperative; state/federal/security institution; AI-rights or AI-safety formation; Disclosure/Legacy Program actor; PSI/Noösphere institution; transhuman or bioconservative community; NHI-contact or planetary-defense formation; criminal/fixer/smuggler network.

## Contacts

Start with a small social graph: a few appropriate contacts such as a close friend, professional contact, family/community tie, patron/mentor and optionally an enemy. Record identity, role, faction, relationship, Affect label/score, why you know them, their needs, realistic capabilities and reciprocity.

Exact starting counts and random tables remain future character-generation design.

## Default UNSA affiliation

By default, a player character has **two simultaneous affiliations**:

1. **UNSA mission identity** — the character is a field agent of the United Nations
   Security Agency (formerly called UNHSS / Firewall before issue #144).
2. **Personal faction identity** — political, cultural, national, professional,
   ideological, community, or social affiliation.

UNSA is therefore not a replacement for the faction list. It is the campaign-wide
operational affiliation layered on top of the character's other faction ties — and #144
makes multi-faction membership explicit (a character may belong to several factions for
different reasons, and receives 10 starting Reputation points to split between two or
three of them). Conflicts between the ties are expected to drive motivations, reputation,
contacts, and mission consequences.

See RULEBOOK.md, “UNSA — the United Nations Security Agency,” and issues #108, #107 and
#144.


## Major UN Parliament parties

The first four parliamentary blocs are:

- **Bioconservatives** — far-right biological-humanity coalition with hard-core bioconservatives, X-Risk doomists, and older nationalist/religious populists.
- **Libertarian Party** — pro-market, accelerationist, minarchist, strongly pro-private technology and extraterrestrial trade.
- **United Earth Social Democratic Party** — social-democratic/green internationalist governing coalition. It has won every UN parliamentary and presidential election so far.
- **The Multitude** — far-left coalition combining autonomist/anarchist/post-workerist currents with Marxist and Marxist-Leninist traditions.

They are intentionally internally contradictory. Many major factions remain outside parliamentary politics. See RULEBOOK.md §42 and `data/world/un_parties.yaml`.
