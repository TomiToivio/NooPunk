# Factions, Motivations, Reputation and Contacts

NoöPunk uses the unified **Affect** model defined in RULEBOOK.md §17.

Every relation is a directional labeled edge:

```text
source -> target | Affect | Affect Score (-100..+100)
```

No edge means unknown. Multiple Affects toward one target are allowed.

## Default Firewall affiliation

A default PC is both:

1. a **Firewall / UNHSS field agent**; and
2. a member of at least one personal political, cultural, national, professional,
   ideological, community, or social faction.

The two identities can conflict.

## Major UN Parliament parties

### Bioconservatives
Far-right coalition of biological-humanity hardliners, X-Risk doomists and older
nationalist/religious populists. Its unifying affect is fear of threats to conventional
humanity, but members disagree sharply about what counts as human.

### Libertarian Party
Pro-market, pro-property, accelerationist and minarchist. Strongly supportive of
private AI, cybernetics, biotechnology, space industry and extraterrestrial trade;
strongly suspicious of UN economic regulation.

### United Earth Social Democratic Party
Social-democratic/green internationalist governing coalition. Supports welfare-state
capitalism, ecology, progressive taxation, redistribution, megacorporate regulation,
technology governance and cautious NHI diplomacy. It has won every UN parliamentary
and presidential election so far.

### The Multitude
Far-left coalition combining autonomist/anarchist/post-workerist commons politics with
traditional Marxist and Marxist-Leninist formations, including the transformed Chinese
communist tradition.

These are only the first major parliamentary blocs. Corporations, Legacy Programs,
criminal networks, militias, cults, intelligence services, cooperatives, insurgencies,
regional movements and NHI-aligned formations also matter.

## Faction discourse structure

Each faction has:

```yaml
us:
  - target
  - target_type
  - affect
  - affect_score
frontier:
  - target
  - target_type
  - affect
  - affect_score
```

**US** holds positively articulated demands, identities, signifiers, allies and people.
**FRONTIER** holds constitutive antagonisms. This Laclau/Palonen structure is used for
populist and non-populist formations alike.

## Motivations

Motivations are personal Affect edges toward demands, values, people or goals.

Examples:

```text
AI rights | Supports | +70
Protect my sister | Loves / Protects | +90
Disclosure | Pursues | +65
Orion Group | Fears | -80
Corporate surveillance | Hates | -55
```

Characters may inherit faction Affects as starting conditions and later diverge.

## Reputation

Reputation is what another actor or faction thinks of the character, not the reverse.
It is directional and may be asymmetric.

## Contacts

Contacts are named people the character actually knows: friends, acquaintances,
professional links, patrons, rivals and enemies. Character generation should create a
small playable network rather than a full biography.

See `data/world/social_graph.json` and `docs/design/GAMEPLAY_LOOP.md`.
