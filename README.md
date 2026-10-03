# NoöPunk

**NoöPunk = Noösphere + Cyberpunk.**

NoöPunk is a portmanteau of Noösphere and Cyberpunk.
It is an attempt to simulate several paradigm shifts in the near future.
The Cyberpunk side is simulating the ongoing AI revolution and the following cyborgification and transhumanism.
The Noösphere side is simulating the paradigm shifts of UFO Disclosure, Panpsychism and Psionics.
NoöPunk uses Concordia with Ollama LLMs together with RPG rules to create simulations of the future.
The simulation is based on theories of social science, futurism and philosophy, in some cases theories that are currently seen as rather fringe. But the idea is to simulate several simultaneous paradigm shifts.
One key theme is the ideological struggle for hegemony related to each paradigm shift: we already see this with the AI revolution as Accelerationists, X-Risk Doomers and AI Skeptics are struggling for hegemony.

## RPG / simulation architecture

NoöPunk is being developed as a single computer RPG and social simulation rather than as separate tabletop and computer games.

The current plan is to use **Google DeepMind Concordia** as the agent-based narrative and social-simulation layer. LLM agents can represent important characters, factions, organizations and other social actors, while ordinary background NPCs may use simpler deterministic or Mesa-style agents where full LLM cognition is unnecessary.

The RPG rules should act as a deterministic world-state and action-resolution layer beneath Concordia. In other words, Concordia and the LLMs decide what agents try to do, while Python rules resolve what actually happens whenever possible. The first versions can be entirely text-based.

This separation is intentional: the long-term project should be able to experiment with different RPG mechanics without rebuilding the Concordia simulation itself.

## Eclipse Phase 2E homebrew

The first playable NoöPunk RPG prototype is being built as an **Eclipse Phase 2nd Edition homebrew**.

Eclipse Phase 2E is the initial mechanical chassis because it already contains many systems that are useful for NoöPunk: transhuman bodies and morphs, AGIs and infomorphs, mesh networking and hacking, reputation systems, psychosocial stress, advanced augmentation, artificial minds, psi and post-scarcity or post-capitalist social arrangements.

NoöPunk is **not intended to remain an Eclipse Phase setting conversion**. Its world, history, factions, metaphysics and ideological conflicts are separate and will increasingly diverge from Eclipse Phase. The current development path is deliberately evolutionary:

```
Eclipse Phase 2E
        ↓
EP2 homebrew Concordia prototype
        ↓
NoöPunk reskin and world replacement
        ↓
simplified EP-derived mechanics
        ↓
native NoöPunk RPG / simulation rules
```

The rules will be modified, reskinned and simplified heavily. The final NoöPunk system may eventually be mechanically very different from Eclipse Phase. Alternative lighter conversions, including Transhumanity's Fate, Neon City Overdrive-style conversions and Powered by the Apocalypse approaches, may also be used as design references where full EP2 rules are too heavy for Concordia.

For development tracking, see the long-running umbrella issue: [#60 — Build NoöPunk Concordia RPG/Simulation from Eclipse Phase 2E homebrew](https://github.com/TomiToivio/NooPunk/issues/60).

## Canonical documents

The living rules document is [`RULEBOOK.md`](RULEBOOK.md). The continuity boundary is
[`docs/PRE_FALL_ALTERNATE_TIMELINE.md`](docs/PRE_FALL_ALTERNATE_TIMELINE.md).

The design canon that the build guards is preserved under [`docs/archive/`](docs/archive/)
after the #60/#63 reset. These are the referenced originals, kept as records rather than
as active canon:

- design invariants: [`docs/archive/DESIGN_PRINCIPLES.md`](docs/archive/DESIGN_PRINCIPLES.md)
- one-game architecture: [`docs/archive/NOOPUNK_AS_ONE_GAME.md`](docs/archive/NOOPUNK_AS_ONE_GAME.md)
- simulation specification: [`docs/archive/SIMULATION_ARCHITECTURE_SPEC.md`](docs/archive/SIMULATION_ARCHITECTURE_SPEC.md)
- theoretical-sources registry: [`docs/archive/THEORETICAL_SOURCES.md`](docs/archive/THEORETICAL_SOURCES.md)
- world ideology: [`docs/archive/WORLD_IDEOLOGY.md`](docs/archive/WORLD_IDEOLOGY.md)
- regional technology matrix: [`docs/archive/TECH_MATRIX.md`](docs/archive/TECH_MATRIX.md)
- writing style and modeling: [`docs/archive/WRITING_STYLE_AND_MODELING.md`](docs/archive/WRITING_STYLE_AND_MODELING.md)

## Eclipse Phase sources and license

Eclipse Phase is created by **Posthuman Studios**. Eclipse Phase-derived material in this repository must follow the applicable Eclipse Phase Creative Commons terms and attribution requirements.

License information and attribution guidance:

- [Eclipse Phase Creative Commons license](https://eclipsephase.com/cclicense/)
- [Eclipse Phase 2E online rules](https://eclipsephase.github.io/en/01/00-infamy.html)
- [Eclipse Phase 2E Quick-Start Rules](https://eclipsephase.com/wp-content/uploads/2024/02/PS10001_EclipsePhaseSecondEdition_QuickStartRulesAcrimony_Nov2023.pdf)

The Eclipse Phase material used for this homebrew is generally published under a **Creative Commons Attribution-NonCommercial-ShareAlike (CC BY-NC-SA)** license. EP-derived material must therefore remain appropriately attributed, noncommercial where required, and shared under compatible ShareAlike terms.

NoöPunk-original setting material and code should be kept clearly distinguishable from directly copied or adapted Eclipse Phase material. Imported rules text, game data or code should record its source, license and modifications. External repositories, fan conversions and third-party data sources must be checked individually before material is copied into NoöPunk.

The aim is to implement and transform the rules, not to mirror the Eclipse Phase books. Prefer code, structured data, compact rule summaries, conversion notes and provenance records over copying large amounts of rulebook prose.

NoöPunk is an unofficial fan/homebrew project and is not affiliated with or endorsed by Posthuman Studios.
