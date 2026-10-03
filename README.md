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

NoöPunk is an **alternate Eclipse Phase timeline set before the Fall**. The year is **20XX**, **Earth still exists**, and the setting uses broadly the **same transhuman technology level as Eclipse Phase**.

The timeline diverges through NoöPunk's own paradigm shifts and conflicts: AI/AGI ideology, Noösphere formation, panpsychism, psionics, NHI/UAP contact, cyborgification, political-economic transformation, and the struggle between cybercapitalist/neofeudal formations and the Multitude. The canonical Eclipse Phase Fall has **not** happened and is not assumed to be inevitable.

The current development path is:

```
Eclipse Phase 2E rules + transhuman technology
        ↓
alternate pre-Fall timeline (20XX, Earth intact)
        ↓
NoöPunk historical / noöspheric divergence
        ↓
Concordia RPG + social simulation
        ↓
selective rules simplification where useful
```

See [the pre-Fall alternate timeline note](docs/PRE_FALL_ALTERNATE_TIMELINE.md) for the continuity boundary.

For development tracking, see the long-running umbrella issue: [#60 — Build NoöPunk Concordia RPG/Simulation from Eclipse Phase 2E homebrew](https://github.com/TomiToivio/NooPunk/issues/60).

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
