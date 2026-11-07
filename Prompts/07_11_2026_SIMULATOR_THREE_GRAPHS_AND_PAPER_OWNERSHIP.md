# Prompt: Simulation graph-first architecture and author-only Paper

- **Date:** 2026-11-07
- **Topic:** Simulator directories, read-only Paper, Social/Ideology/Physical Graphs
- **Source:** Tomi's design request in ChatGPT; implementation tracker [issue #1309](https://github.com/TomiToivio/NooPunk/issues/1309).
- **Status:** Original author prompt retained for future reuse. Not automatically implementation or canon.

## Original prompt (verbatim wording; HTML nonbreaking spaces normalized)

Add an issue in [https://github.com/TomiToivio/NooPunk](https://github.com/TomiToivio/NooPunk) for creating the Simulation Graphs first.

Make agents treat [https://github.com/TomiToivio/NooPunk/tree/main/NooPunk-Simulator/Paper](https://github.com/TomiToivio/NooPunk/tree/main/NooPunk-Simulator/Paper) as read only. This is for storing Tomi's draft about the universe, both serious Social Science and less serious Game Design. Agents should not edit!

Add directories to [https://github.com/TomiToivio/NooPunk/tree/main/NooPunk-Simulator](https://github.com/TomiToivio/NooPunk/tree/main/NooPunk-Simulator)

- Paper - Tomi's writings, read only for Agents!
- Rulebook - Rules of the Simulation. Agents should summarize Tomi's theory and rules here.
- Code - for implementing Rulebook as Python Code.
- Graphs - The Graphs representing the NoöPunk world.

First we add three types of NoöPunk Graphs:

- Social Graph - This is a typical SNA graph which represents the Network Society. Forms the basis of the entire simulation.
- Ideology Graph - This represent faction ideologies based on the Formula of Populism ([https://github.com/TomiToivio/LaclauGPT/blob/main/paper/PHASE_1_PAPER.md](https://github.com/TomiToivio/LaclauGPT/blob/main/paper/PHASE_1_PAPER.md)). The simulation uses Discourse Network Analysis as a bridge between the DA and SNA layers.
- Physical Graph - Represents locations in the Physical world. First we add a Physical Graph representing the Helsinki City. This is the Physical world of the Simulation.

These are also used as the "world simulation" for the NoöPunk RPG.
