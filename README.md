# NoöPunk: Etsivä Romppainen ja Uusi Paradigma

> **The current NoöPunk project is a small, story-first cyberpunk detective interactive-fiction adventure, not a full RPG.** In Helsinki in 2045, detective Harri Romppainen investigates the human and political consequences of three paradigm shifts: AI, UAP/NHI and consciousness/PSI. See the [story-first implementation guide](docs/adventure/PIVOT_1310.md), the [story-first decision (#1310)](https://github.com/TomiToivio/NooPunk/issues/1310) and the [documentation brief (#1322)](https://github.com/TomiToivio/NooPunk/issues/1322).

**Reality has changed. You are still expected at work.**

[**Project website**](https://tomitoivio.github.io/NooPunk/) · [**Play the existing prototype**](#play-the-prototype) · [**Story / authoring track**](NooPunk-Story/README.md) · [**Adventure development**](NooPunk-Simulator/README.md) · [**Design pivot**](docs/adventure/PIVOT_1310.md) · [**Historical RPG archive**](NooPunk-RPG/README.md)

## Why I am making NoöPunk

I began NoöPunk as a way to process **my own philosophical paradigm shift and ontological shock**. My thinking has moved toward **idealism and quantum-information panpsychism**. At the same time, I see three developments that may radically change our understanding of intelligence, consciousness and reality. I believe they will unfold **in some form by 2045**. That is my personal forecast and the springboard for science fiction, **not a claim of scientific consensus**.

1. **AGI / ASI: What is intelligence?** AI capabilities are already transforming technology, work and politics. The possibility of general or superhuman AI, along with human augmentation, produces competing responses: acceleration, caution, regulation, existential-risk movements and more.
2. **UFO / UAP / NHI: Are we alone?** UAP reports, public hearings and disclosure movements are real social and political developments. I take the possibility of non-human intelligence seriously, with **Jacques Vallée's** interpretations of anomalous phenomena particularly interesting to me. But the existence of a disclosure movement or unexplained observation does **not** itself establish the nature or origin of an alleged NHI.
3. **Consciousness / PSI: What is consciousness?** **Bernardo Kastrup, Donald Hoffman and Federico Faggin** have influenced my interest in idealism and quantum-information-based theories of consciousness. Cultural phenomena such as *The Telepathy Tapes* are part of the contemporary discussion, not independently verified proof of telepathy. In NoöPunk's **fictional** 2045, PSI can become a practical technological application of a changed science of consciousness.

The three shifts may be independent. What interests me is **their convergence**: artificial agents, possible nonhuman agents and new models of conscious agents challenge familiar definitions of who or what can act. The consequences are not merely technological. **People, institutions, movements and ideologies struggle to define what the discoveries mean.**

This is **social science fiction**. My research interests in discourse, political identities, social networks and [LaclauGPT](https://github.com/TomiToivio/LaclauGPT) help me imagine how rival interpretations spread. They are storytelling lenses, **not requirements for building a full social simulation**. Fiction, investigation and occasional absurd humor allow me to explore unresolved questions without having to solve them first.

**Distinguish the levels:** AI progress is observable; theories of consciousness are active and contested; claims about UAP/NHI and PSI vary widely in evidentiary strength; and NoöPunk's 2045 discoveries, including functional PSI, are **fictional extrapolations**. The story is neither evidence for paranormal claims nor a forecast presented as fact.

## What is real, what is researched, what is contested, what is fiction

The boundary is stated instead of assumed, because the difference between a real development, my own interpretation, a
contested claim and a story premise is the whole point:

- **Established** — current machine learning, energy and hardware constraints, existing surveillance law. Background, not
  a plot twist.
- **Live research and plausible extrapolation** — AI capabilities, quantum computing, consciousness science, UAP
  instrumentation and analysis. Used as extrapolation, and labelled as extrapolation.
- **Contested claims and popular movements** — telepathy, disclosure narratives, specific NHI interpretations, and *The
  Telepathy Tapes* as part of a current popular conversation about consciousness. Entered as claims with sources, never as
  settled fact.
- **Fiction** — Helsinki 2045, Romppainen, quantum-information panpsychism as working science, PSI as a licensed
  technology, and the politics of an ontological shock. The detective is allowed to be skeptical, indifferent or wrong.

## The story: Helsinki, 2045

**NoöPunk: Etsivä Romppainen ja Uusi Paradigma** is a short, old-fashioned **text-based cyberpunk noir detective adventure**, potentially also the starting point for a science-fiction novel.

Helsinki has endured waves of social destabilization and ideological polarization surrounding AGI/ASI, consciousness/PSI and UAP/NHI. Science, politics, media and government have been forced to respond. **The full NHI Crisis of older NoöPunk lore has not happened yet.** These extraordinary questions primarily reach the detective through **human witnesses, intermediaries, organizations, evidence and conflicting accounts**, not through constant alien encounters or an encyclopedia of metaphysics.

Harri Romppainen follows leads, interviews suspects and witnesses, examines messages and OSINT, records contradictions and makes choices that affect a case. A suspect's ideology is not proof of a crime. The protagonist and player may remain skeptical. The story reveals the larger world only as the investigation demands.

The ambition is **one good playable investigation first**. The story uses scenes, choices, clues, case state and a notebook. A small faction or ideology graph may help one case; a universal world simulator is unnecessary.

## Why the full RPG is paused

The earlier ambition to make NoöPunk a comprehensive RPG became **almost insane in scope**. Ordinary cyberpunk action could work with almost any good cyberpunk ruleset. The **Noösphere** is another matter: UFO/NHI phenomena, psychic abilities and consciousness metaphysics would need extensive custom rules. The setting also overlays **Physical, Cyber and Astral** realities. The same agent, clue or encounter may cross several layers, multiplying the complexity.

Building a complete simulation and rulebook for that world kept displacing the actual goal: **writing the story**. So **the full RPG is paused, not deleted**. The [NooPunk-RPG archive](NooPunk-RPG/README.md), old CWN experiments, Evennia/MUD work, Godot prototypes and larger strategy-simulation plans are **historical or optional work**, not the active deliverable. No RPG implementation or mandatory RPG compatibility is required.

The Noösphere is allowed to remain mysterious. **A detective story needs convincing evidence and consequences, not a physics engine for the Astral.**

## Play the prototype

The repository contains a **development-stage terminal investigation prototype**, not yet an author-complete Romppainen episode. From the repository root, with a compatible Python installation:

```bash
git clone https://github.com/TomiToivio/NooPunk.git
cd NooPunk
python scripts/noopunk_case.py
```

The script's own command-line documentation also supports `--script walkthrough.txt --seed 7` and `--load case-save.json`. The existing case is development material; **do not mistake it for a completed canonical story**. See [the documented adventure pivot](docs/adventure/PIVOT_1310.md) for current architecture, testing and authorial boundaries.

A second, newer runner plays the Romppainen development case directly:

```bash
python3 NooPunk-Simulator/Code/adventure.py
```

Both cases are development fixtures. Neither is Tomi's own first episode; the manuscript in
[`NooPunk-Story/Story/`](NooPunk-Story/Story/) is.

## Development boundaries

- **Story:** [`NooPunk-Story/`](NooPunk-Story/README.md). `NooPunk-Story/Story/` is Tomi's author-only manuscript: **agents read-only**. Derived graphs and adapters belong outside the manuscript.
- **Adventure:** [`NooPunk-Simulator/`](NooPunk-Simulator/README.md). Its name is historical: the current product is the small interactive detective adventure. `NooPunk-Simulator/Paper/` is also **Tomi-only, agents read-only**.
- **RPG:** [`NooPunk-RPG/`](NooPunk-RPG/README.md) is **paused and must remain untouched** unless explicitly reactivated.

For the current implementation mandate, see [issue #1310](https://github.com/TomiToivio/NooPunk/issues/1310). The former game designs, [rulebook](RULEBOOK.md), [MUD](mud/README.md) and [earlier campaign materials](docs/campaign/) are retained for history and reference, **not as current gameplay instructions**.

## A note on authorship and tone

NoöPunk combines **social science fiction, cyberpunk noir and the New Weird**: grounded investigation, political conflict, strange witnesses, philosophical ambiguity, and comedy at precisely the wrong moment. The project's title means **Noösphere + Cyberpunk**. The wider universe can remain very large. This story only needs a detective, a city, a case, and three questions nobody agrees how to answer.
