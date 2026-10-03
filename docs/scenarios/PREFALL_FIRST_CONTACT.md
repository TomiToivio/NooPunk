# Pre-Fall First-Contact Vertical Slice

This is the first canonical playable scenario for issue #60.

## Scope

The scenario is intentionally small and built only from author-specified facts:

- year **20XX**;
- alternate Eclipse Phase timeline **before the Fall**;
- Earth remains inhabited and politically central;
- Eclipse Phase-level transhuman technology;
- five ET civilizations contacted on Earth;
- a sixth civilization known from ancient Martian ruins;
- a seventh civilization detected through SETI radio signals;
- several Zookeeper-built stargates in the Solar System;
- stargates explain some UAP traffic, while warp-drive UAPs are also observed;
- Mars Eldrich's colonization discovered ancient ruins and life on Mars;
- Mars Eldrich is searching for crash-retrieval material;
- no scientific consensus exists on whether Noetics, Plasmoids, and Constructs count as civilizations.

The Earth / Mars / stargate rooms are **abstract evidence nodes** for the text prototype. Their adjacency is a UI convenience and does not define literal travel times or geography.

Generic analyst/contact NPCs are scenario interface roles only. They do not define new factions, biographies, institutions, or hidden canon.

## Run

```bash
python scripts/noopunk_text.py
```

The old non-canonical regression world remains available:

```bash
python scripts/noopunk_text.py --scenario fixture
```

Optional local LLM/Concordia contacts remain behind:

```bash
python scripts/noopunk_text.py --ollama
```

## Useful commands

```text
look
sheet
talk "SETI analyst" hello
test skill Perceive roll 40
take "SETI signal record"
east
north
inventory
save
```

The scenario uses the same deterministic EP2-derived resolution layer as the rest of the issue #60 prototype. LLMs may choose intent or narrate, but they do not generate dice results or numeric state changes.
