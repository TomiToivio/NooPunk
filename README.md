# NoöPunk

## Reality has changed. You are still expected at work.

*The future of humanity is no longer exclusively a human concern.*

**2045. Humanity survived the NHI Crisis. It is having trouble explaining what survived.**

Earth is still here. So are governments, employers, political parties and the people who tell you that everything is under control. There are more kinds of intelligence now. Control is harder to locate.

Rogue artificial minds pursue purposes nobody can translate into reassuring language. Alien infiltrators look like people. The apparently benevolent **Zookeepers** offer protection and a better future. You would like to be grateful. You would also like to know what a zookeeper means by “better.”

Cybernetics, genetic engineering and psionics are changing what a person can be. Human, cyborg, transhuman, posthuman: the categories multiply as the distinctions become less dependable. Somewhere in all this is somebody trying to remain themselves.

Humanity has united under the **United Nations**. It has not agreed on what humanity is, or what it ought to become. Rival factions offer resistance, control or transformation. Each would prefer to settle the question before the others do.

And the biosphere still needs looking after. A revelation about consciousness does not repair a damaged ecosystem. Clean energy, ecological restoration and biotechnology offer the possibility of a better life. People still have to build it, share it and keep it alive.

Three paradigm shifts make certainty difficult:

- **AGI: Artificial General Intelligence.** We made minds that could exceed our own. Abundance and extinction both entered the discussion. So did ownership.
- **NHI: Non-Human Intelligence.** We were not alone. This answered one question and made most of the others worse.
- **PSI: Psionics and Consciousness.** Mind and reality proved more intimately connected than expected. The discovery did not make it easier to agree about either.

**NoöPunk** is an experimental **New Weird / Social Science Fiction RPG and political strategy project**, growing into cyberpunk science fantasy as its world changes. Investigate the impossible at the scale of a person; contest the future at the scale of a faction. The canonical tabletop and Godot RPG permanently use CWN as their OSR rules chassis, with compatible SWN/WWN modules. The new primary Godot direction is location-based, social/investigative play rather than tactical top-down movement; older scenes remain for compatibility. See [foundational decision #897](docs/design/ISSUE_897_FOUNDATIONAL_LOCK.md).

A breakthrough can become a political crisis. A crisis can become somebody's career. Behind both is the awkward question of who needs help, and whether you can still do something for them.

**The next world is still up for grabs. You have to live in this one while you argue about it.**

NoöPunk also uses a **three-system lens**: living/biological systems (biopunk, solarpunk and planetary ecology), social systems (communication and politics amid AGI/NHI contact), and psychic systems (consciousness, PSI and the fictional Noösphere). These are distinct but interdependent; neither a climate apocalypse nor an effortless ASI utopia is inevitable. See the [biosphere paradigm design](docs/design/ISSUE_510_BIOSPHERE_PARADIGM.md) (#510).

*Setting note: 2045 depicts the developed NHI Crisis era. The earlier strategy campaign begins around 2027, before these outcomes are settled, allowing players to shape the future rather than treating it as inevitable.*

## Before NoöPunk: a transmission, possibly

In **1974**, **Tommy Pilgrim**, a left-wing science-fiction writer, took LSD at a **Hawkwind concert** and experienced what he called a transmission from **VALIS**. It appeared to contain humanity's future. Artificial minds, alien encounters, psychic phenomena, political upheaval. An unreasonable amount of information for one evening.

He wrote it down as ***NoöPunk***. He could not establish whether he had seen the future, misunderstood a symbol, or looked into a neighboring timeline. Some of the future's machinery looked suspiciously like 1974. The uncertainty did not prevent the book from becoming a cult classic. Neither did it prevent later events from beginning to resemble it.

Films, television, tabletop and computer games followed, along with a NoöPunk subculture. **Pilgrim is still alive in Helsinki**, a literary celebrity studied by scholars and courted by parapsychologists. There are several explanations for what happened to him. None has disposed of the others.

**And this is where the book ends and the scenario begins.** The real-world NoöPunk project uses Pilgrim's imaginary 1974 future history as a **presentation and narrative frame**, not as evidence of actual precognition and not as permission to rewrite its underlying simulation or canon. The opening account summarizes the established premise; Tommy Pilgrim's full literary story remains reserved for the project's author. [Design background: issue #447](https://github.com/TomiToivio/NooPunk/issues/447).

**NoöPunk = Noösphere + Cyberpunk.**

NoöPunk is an experimental **computer RPG and social simulation** set in **20XX**, using a **CWN-first rules foundation with optional NoöPunk narrative modules**, a deterministic Python RPG kernel, and **Google DeepMind Concordia** for optional LLM-driven agents and narration. Earth still exists. Transhuman technology is already here. AGI, cyborgification, NHI contact, psionics, panpsychism, and the emerging Noösphere are destabilizing the old world at the same time.

The project is currently a **playable text-based prototype**. You can run the normal game entirely without Ollama or an LLM.

### Rules direction (issue #615)

**New author decision (2026-10-26):** NoöPunk's target RPG begins with the **standard Without Number family** rules rather than a bespoke 1d10/Fate hybrid. **Cities Without Number** and **Stars Without Number** provide the shared attributes, skills and fundamental dice grammar; **Worlds Without Number** adds noetic/interdimensional science fantasy and **Ashes Without Number** adds local NHI Crisis survival and salvage. Start from existing procedures; customize after a functioning, single-sheet cross-genre RPG exists. The first independent Python chassis is `src/rules/without_number.py`. **Migration is incomplete:** existing legacy 1d10 and strategy crossover Fate code still runs separately while its callers, saves and scenarios are adapted. See the [#615 decision and progress record](docs/design/ISSUE_615_WITHOUT_NUMBER_RULES_DIRECTION.md) and [conversion epic #564](https://github.com/TomiToivio/NooPunk/issues/564) for remaining work, license restrictions and compatibility requirements.

**Visual identity:** *A 1974 Hawkwind concert, an acid trip, and a VALIS transmission showing 2045.* Zardoz, Barbarella and The Rocky Horror Picture Show govern the aesthetic, not later glossy cyberpunk. [Art-direction bible](docs/design/ISSUE_897_VISUAL_BIBLE.md).

## Motivation: social science first, science fiction second

**My primary motivation is sociological modeling of possible near-future paradigm-shift scenarios.** NoöPunk is an experiment at the intersection of **social science, social data science, and social science fiction**. The game is a way to build and explore simple, explicit models of how societies, institutions, networks, ideologies, and political factions might respond to interacting transformations in AI, nonhuman intelligence (NHI), and consciousness/PSI. These are exploratory scenarios, not predictions or empirical claims that contested phenomena are real.

**My secondary motivation is to make science-fiction entertainment in my own style.** Characters, political satire, unsettling mysteries, philosophical questions, absurdity, and encounters with the genuinely strange give the models a playable and imaginative form.

The resulting genre is best described as **Social Science Fiction × New Weird**. **Cyberpunk Science Fantasy emerges progressively** as the paradigm shifts become more visible and consequential within the fictional world. The scenario starts around **2027**, still close to recognizable contemporary society, rather than assuming a mature cyberpunk future from the outset. Social modeling remains the core motivation throughout; the aesthetics and possibilities of the world evolve with the crisis.

## Genre and positioning

**Genre identity:** **Social Science Fiction × New Weird** is the defining blend: social-scientific modeling motivates the project and New Weird gives it its distinctive fictional expression. **Cyberpunk Science Fantasy** becomes increasingly prominent as the fictional paradigm shifts unfold. These are complementary lenses, not three separate games.

### 1. Social Science Fiction: society is the protagonist

NoöPunk explores how institutions, ideologies, communications, economies, religions, and political movements respond to extraordinary paradigm shifts. Players lead factions and characters in a compact grand-strategy/RPG simulation: they build networks, contest meanings, pursue hegemony, and influence social change. Ernesto Laclau's discourse theory, Manuel Castells's network/communication power, and Niklas Luhmann's systems theory inform its abstract political model. The starting scenario, around **2027**, focuses on accelerating conflict *before* the later NHI Crisis.

### 2. New Weird: reality refuses to fit the categories

**The primary imaginative genre, alongside Social Science Fiction.** AI, alleged nonhuman intelligences, anomalous consciousness, PSI, unfamiliar religions, and strange institutions collide without reducing the mystery to conventional aliens, magic, or a single tidy explanation. The tone can shift between political satire, unsettling investigation, philosophical wonder, absurd comedy, and the profoundly alien. The paradigm shift is ontological as well as technological: who gets to decide what is real?

### 3. Cyberpunk Science Fantasy: the world and its tools

**Secondary genre and influence, not the whole premise.** Hacking, surveillance, corporate power, cybernetics, BCI, AI, inequality, and transhuman technology provide grounded near-future material conflicts. Science-fantasy elements introduce NHI and PSI as consequential features of the **fictional setting**, with uncertain mechanisms and competing interpretations. Cyberpunk stays deliberately limited in the early 2027 scenario, rather than swallowing the social-science and New Weird themes or assuming a fully cyberpunk society already exists.

**In one sentence:** Social Science Fiction asks **how society changes**; New Weird asks **what reality has become**; Cyberpunk Science Fantasy asks **what powers and technologies people use to survive and fight over it**.

**Elevator pitch.**

> Reality has changed. The institutions responsible for explaining it are still open.
> NoöPunk is a New Weird RPG and political simulation about who gets believed,
> who gets power, and what happens to everyone else.

**Storefront pitch — the later UNSA investigation setting.**

> You have graduated. You have been augmented. You have been assigned a limited
> forensic AI. The **United Nations Security Administration (UNSA)** considers
> you ready.
>
> Earth has survived regional catastrophes. Two non-human powers helped rebuild
> it, and neither fits comfortably under “ally” or “enemy.” Your work concerns
> abductions, infiltrations and impossible physics. Mind-control, hybridization,
> corporate psy-ops and ordinary human lying can leave much the same evidence.
>
> Someone is in trouble. You need to decide what happened, who to trust,
> and what you can do before a convincing explanation takes the place of an answer.

**Comparisons.** NoöPunk sits between three touchstones and borrows from each:

- **Shadowrun** — cyberpunk plus extraordinary powers, and a world where the paranormal is
  real. NoöPunk draws on UFO/PSI/interdimensional lore rather than elves, dragons or spells.
- **Eclipse Phase** — ASI catastrophe, transhumanism, existential risk and survival.
- **The X-Files** — investigations, agencies, and conspiracy mythology.

A useful shorthand is **"pre-Eclipse Phase" in degree of societal transformation** — not a
prequel and not shared continuity. Cybernetics, PSI, disclosure and transhumanism are still
comparatively new, and Earth-based states and social institutions largely continue to function
despite regional catastrophes, post-ASI damage and reconstruction.

**Tone.** This is not a full postapocalypse and not Lovecraftian cosmic horror. The universe
is not fundamentally hostile: some NHI are benevolent, others hostile, ambiguous, or merely
politically opposed to one another. **Cosmic wonder and Fortean/ontological mystery** are the
default register, with horror as an occasional note rather than the premise.

> **Positioning note.** The audience-fit comparisons above are a **positioning hypothesis**,
> not proven market data. NoöPunk claims no affiliation with, or endorsement by, any game,
> show or publisher named here — they are comparisons, not licenses. See the licensing section
> below for licensing and attribution requirements for adapted rules.

## NoöPunk in two books: the paradigm shift

Two books published in 2026 are especially useful real-world intellectual inspirations for NoöPunk's near-future **New Weird political simulation**:

- **Alexander Wendt, [*The Last Humans: UFOs, Global Security, and the Threat to State Sovereignty*](https://academic.oup.com/book/63308)** (Oxford University Press, online 2026; print 2027). Wendt asks what the discovery of superior nonhuman intelligence could do to anthropocentric state legitimacy, ontological security, sovereignty, populism, and the international order. **NoöPunk lens:** the political and institutional crisis of NHI disclosure.
- **Diana Walsh Pasulka, [*The Others: UFOs, AI, and the Secret Forces Guiding Human Destiny*](https://books.google.com/books/about/The_Others.html?id=wTyDEQAAQBAJ)** (St. Martin's Press, 2026). Pasulka examines extraordinary-encounter narratives through religion, AI, immortality, and transformations in ideas about consciousness. **NoöPunk lens:** the cultural, religious, and ontological collision of AI, NHI, and PSI.

**Together:** Wendt explores what happens to *political order* when human exceptionalism is challenged; Pasulka explores what happens to *meaning, belief, and identity*. NoöPunk turns these questions into a struggle for hegemony: emerging factions try to define a rapidly changing reality, reshape institutions, and build communication power. Its political simulation draws on **Ernesto Laclau, Manuel Castells, and Niklas Luhmann**. The initial strategy scenario begins around **2027**, during accelerating change, **before** the later NHI Crisis and UNSA era.

These are **scenario inspirations and interpretations, not evidence** that disputed NHI or paranormal claims are established facts; the game's fictional world makes its own assumptions.

## Quick start

Requires **Python 3.12** (the version tested in CI).

```bash
git clone https://github.com/TomiToivio/NooPunk.git
cd NooPunk
python -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
python scripts/noopunk_text.py
```

On Windows PowerShell, activate the environment with:

```powershell
.venv\Scripts\Activate.ps1
```

The normal start command launches the default **pre-Fall 20XX** NoöPunk scenario:

```bash
python scripts/noopunk_text.py
```

Ollama is optional for basic play.

### The optional Ubiquitous Maniacs case

*The Listening Ward* is a self-contained, non-canonical investigation that runs on the current
RPG engine and needs **nothing but the standard library** — none of the packages above are
required for it:

```bash
python -m strategy_game.rpg --scenario ubiquitous-maniacs --save ward.json --new
```

Resume by leaving off `--new`. It needs **Python 3.11 or newer**; on an older interpreter it
stops with a message naming the version and the remedy instead of an `ImportError`. Scope,
troubleshooting and the end-to-end tests are in
[docs/UBIQUITOUS_MANIACS_INTEGRATION.md](docs/UBIQUITOUS_MANIACS_INTEGRATION.md).

## First-player cheat sheet

At the prompt, try:

```text
look
n / s / e / w
go <direction>
inventory
take <item>
drop <item>
talk <character> <message>
say <message>
stats
sheet
save
quit
```

Useful rules/debugging commands also include:

```text
test skill ...
test social ...
test mesh ...
test combat ...
```

See [`RULEBOOK.md`](RULEBOOK.md) for the actual rules instead of treating the README as a second rulebook.

## Installation

### Linux / macOS

```bash
git clone https://github.com/TomiToivio/NooPunk.git
cd NooPunk
python -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### Windows PowerShell

```powershell
git clone https://github.com/TomiToivio/NooPunk.git
cd NooPunk
python -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
```

The deterministic text game itself uses only the Python standard library. The top-level `requirements.txt` also installs the pinned Concordia dependency needed by the current Concordia integration and optional Ollama-backed runtime.

## Start the game

### Default NoöPunk scenario

```bash
python scripts/noopunk_text.py
```

This starts the canonical **20XX, Earth-intact** NoöPunk scenario.

### Small Concordia / EP2 proof of concept

```bash
python scripts/noopunk_text.py --scenario issue74
```

Issue #74 is a deliberately tiny vertical slice for testing the current architecture. It remains fully playable **without an LLM**, using deterministic mechanics and scripted NPC behaviour.

Scenario notes: [`docs/scenarios/ISSUE74_CONCORDIA_EP2_POC.md`](docs/scenarios/ISSUE74_CONCORDIA_EP2_POC.md).

### CLI help

```bash
python scripts/noopunk_text.py --help
```

## Optional Ollama / LLM mode

Ollama is an **external runtime/service**, not a Python dependency. Install and start Ollama separately, then make sure the model you want to use is available in Ollama.

The current NoöPunk adapter reads these environment variables:

- `NOOPUNK_OLLAMA_MODEL` — **required** model identifier.
- `NOOPUNK_OLLAMA_BASE_URL` — optional; defaults to `http://127.0.0.1:11434`.
- `NOOPUNK_OLLAMA_TEMPERATURE` — optional; defaults to `0.5`.
- `NOOPUNK_OLLAMA_TOP_P` — optional; defaults to `1.0`.
- `NOOPUNK_OLLAMA_TOP_K` — optional; defaults to `40`.

For example:

```bash
export NOOPUNK_OLLAMA_MODEL="your-installed-model"
python scripts/noopunk_text.py --ollama
```

To run the small issue #74 scenario with an LLM-controlled contact and optional GM narration:

```bash
export NOOPUNK_OLLAMA_MODEL="your-installed-model"
python scripts/noopunk_text.py --scenario issue74 --ollama --llm-gm
```

The division of labour is intentional:

- **LLM / Concordia:** dialogue, agent choice, natural-language intent translation, interpretation, and optional GM narration.
- **Python:** legal actions, game state, dice and rules resolution, character statistics, inventory, harm/stress, world-state changes, and consequences.

LLMs may decide what an agent attempts. They do not get to invent dice rolls or silently rewrite the rules.

## Current status

NoöPunk is an experimental RPG and social-simulation project under active development. **The top-down Godot game and tabletop rulebook use vanilla CWN/SWN as the canonical baseline**. Rules parity is an ongoing task, not a claim of full implementation. Legacy text, Python and strategy prototypes remain in the repository as historical or experimental work, not alternative rule authorities.

### Playable slice: the hospital case in Godot 4

A ten-minute vertical slice of the detective RPG runs now, offline and without an LLM: one hospital,
three conversations, six pieces of evidence, a sealed research file and two endings that both stay
ambiguous. Godot **4.7.2** is pinned; run and test commands, controls, the save format, the rules
adapter and the known limitations are in [`docs/godot/README.md`](docs/godot/README.md).

The rules come from the approved Without Number kernel through a single adapter
(`godot/core/rules_adapter.gd` reads `data/rules/wn_core.json`); no mechanic is invented in engine code,
and #564's unresolved 3d6 question is a data-level override that the game reports, not a silent choice.

The current core work is [issue #111](https://github.com/TomiToivio/NooPunk/issues/111).

## What NoöPunk is about

The **Cyberpunk** question is who owns the machinery: the AI, the surveillance network, the augmented body, the means of making a life. Automation, biotechnology and post-scarcity possibilities arrive in a world that already knows how to distribute things unequally.

The **Noösphere** question is who, or what, is having the experience. NHI contact, psionics and panpsychism disturb the boundaries between minds, machines, cultures and networks. Understanding the equipment may not settle the question of who is using it.

Enthusiasts, skeptics, regulators, believers and opportunists inhabit the same world. So do people who would like to finish an ordinary day without revising their entire account of existence. Several incompatible futures have arrived. They all need somewhere to live.

## How the game works

NoöPunk is being developed as **one computer RPG and social simulation**, not as separate tabletop and computer games.

The rules are tabletop-like because they need to be:

- readable by humans;
- inspectable and testable;
- executable deterministically in Python;
- usable by Concordia/LLM agents without giving the model authority to invent outcomes.

The preferred loop is:

```python
intent = agent.choose_action(...)
result = rules.resolve(intent, actor, target, world)
world.apply(result)
agent.observe(result)
```

Important characters, factions, and institutions may use LLM cognition. Simpler background NPCs can use deterministic or lightweight scripted behaviour where rich language interaction is unnecessary.

## Current rules baseline: Cities Without Number / Stars Without Number

**The current canonical rules are vanilla *Cities Without Number* (CWN), supplemented by *Stars Without Number Revised* (SWN) where CWN does not cover a subsystem, especially psionics.** The canonical computer-game implementation is the top-down Godot project at `project.godot`; the canonical tabletop rules live in [`rulebook/`](rulebook/00_INDEX.md). We begin by reproducing the original rules faithfully. **Modifying, reskinning and homebrewing CWN/SWN is a future, section-by-section phase**, after the vanilla baseline has been implemented and checked. No other RPG system is part of the current rules baseline.

The [vanilla baseline decision](docs/NOOPUNK_BASELINE_848.md) and [CWN coverage matrix](docs/CWN_COVERAGE_MATRIX.md) define the implementation scope and outstanding gaps. Older prototypes, archived documents and experiments do not override this baseline.

## Licensing and attribution

*Cites and rights are specific to each source and file; this repository does not grant a blanket license to third-party material.*

- **Cities Without Number (CWN)**, by Kevin Crawford / Sine Nomine Publishing: the specifically published **CWN Systems Reference Document (SRD)** is dedicated to **CC0**. This applies to the identified SRD material, not automatically to the complete commercial books, artwork, or protected setting material. [CWN SRD browser](https://cwn.quadrifons.com/).
- **Stars Without Number Revised (SWN)**, by Kevin Crawford / Sine Nomine Publishing: **no independently verified publicly reusable SRD text license** has been established in the repository rights audit. No claim is made that SWN book prose, tables, art or setting are CC0 or otherwise freely redistributable. Implement mechanics independently and write explanations in original wording; do not copy protected SWN expression without permission.
- **NoöPunk-original source code and creative content:** no project-wide software or content license has yet been selected. Do not assume that public GitHub access means permission to reuse all code, writing, assets or third-party materials. Any future license must be chosen and documented separately.
- **Independence:** NoöPunk is an unofficial, independent project and is not affiliated with, licensed by, or endorsed by Kevin Crawford or Sine Nomine Publishing.

See the [source rights audit](docs/licenses/ISSUE_569_WITHOUT_NUMBER_RIGHTS.md), [attribution policy](docs/ATTRIBUTION_POLICY.md), and [publication policy](docs/licenses/ATTRIBUTION_AND_PUBLICATION_POLICY.md) for provenance and release checks.

## Rules and world documentation

Active canonical documents:

- **Rules:** [`RULEBOOK.md`](RULEBOOK.md)
- **Continuity boundary:** [`docs/PRE_FALL_ALTERNATE_TIMELINE.md`](docs/PRE_FALL_ALTERNATE_TIMELINE.md)
- **Umbrella implementation work:** [issue #60](https://github.com/TomiToivio/NooPunk/issues/60)
- **Small Concordia/EP2 scenario:** [`docs/scenarios/ISSUE74_CONCORDIA_EP2_POC.md`](docs/scenarios/ISSUE74_CONCORDIA_EP2_POC.md)
- **First Contact lore:** [`docs/scenarios/FIRST_CONTACT_TEN_TRADITIONS.md`](docs/scenarios/FIRST_CONTACT_TEN_TRADITIONS.md) — the ten-tradition contact matrix, the Orion deception sequence and the 2045 alien cold war (issue #497).

Documents under [`docs/archive/`](docs/archive/) are historical design records. They are useful provenance, but they are **not automatically active canon** and do not override the current rulebook or explicit current author direction.

### Design references

These archived documents remain important design and architecture references even when they are not active canon:

- [`docs/archive/DESIGN_PRINCIPLES.md`](docs/archive/DESIGN_PRINCIPLES.md) — project-level design balances and invariants.
- [`docs/archive/SIMULATION_ARCHITECTURE_SPEC.md`](docs/archive/SIMULATION_ARCHITECTURE_SPEC.md) — simulation state, event-log and resolver architecture.
- [`docs/archive/NOOPUNK_AS_ONE_GAME.md`](docs/archive/NOOPUNK_AS_ONE_GAME.md) — the single-game / single-rule-model direction.

## Development and architecture

The runtime is split deliberately:

### Deterministic rules kernel

Python owns state and mechanical truth wherever practical:

- action legality;
- skill and opposed tests;
- dice;
- modifiers;
- damage and stress;
- inventories;
- resources;
- persistence;
- scenario objectives;
- explicit world-state mutations.

### Concordia / LLM layer

Google DeepMind Concordia is the agent/narrative layer. LLM agents can:

- choose goals and actions;
- converse;
- negotiate;
- interpret situations;
- translate natural-language player intent;
- narrate already-resolved outcomes.

The current Concordia dependency is pinned to a specific upstream Git revision because NoöPunk uses prefab/contrib APIs that were verified against that revision.

### Smoke checks

These commands should remain valid:

```bash
python scripts/noopunk_text.py --help
printf 'quit\n' | python scripts/noopunk_text.py --scenario issue74
python scripts/concordia_smoke.py
```

With the dependencies from `requirements.txt` installed, also check the real Concordia import/config bridge:

```bash
python scripts/concordia_smoke.py --build-concordia-config
```

