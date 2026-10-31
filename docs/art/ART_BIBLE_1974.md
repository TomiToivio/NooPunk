# NoöPunk art bible — 1974's psychedelic vision of 2045

**Status: visual lock for [#897](../design/FOUNDATIONAL_LOCK_897.md).** Machine-readable values live in
[`design_tokens.json`](design_tokens.json); this document is the reasoning and the production rules. Read
both before drawing anything — the same single-source principle as the rules.

> *A precognitive vision of 2045, transmitted by VALIS into the brain of a science-fiction author tripping
> on acid at a Hawkwind concert in 1974.*

## The core visual rule

**The future must look imagined in 1974**, even when its subjects — AGI, BCI, the noösphere, hacking, NHI,
cybernetic networks — are from 2045.

That single rule resolves almost every art question. Not "what would this look like?" but **"what would a
1974 illustrator, working from what 1974 knew, have drawn?"** Circuits are hand-drawn and chunky. Data is
reels, tape and oscilloscopes. Interfaces are illuminated buttons and needle gauges. The network is a
diagram from a scientific American paperback, not a glowing lattice.

**The failure mode to avoid:** generic 1980s cyberpunk. Neon-on-black grids, chrome-and-mirror shades,
magenta/cyan gradients, "holographic" UI, clean vector icons. Those are 1984's imagination of the future,
not 1974's, and they erase the project's identity.

## Anchors

**Films, ranked:** **Zardoz (#1)** — the decisive one: a barbarian materialism colliding with an immortal
technocratic elite, and the visual language of a future that is archaic, theatrical and slightly absurd.
**Barbarella (#2)** — plastic, saturated, tactile, unembarrassed. **The Rocky Horror Picture Show (#3)** —
the cabaret of it: glam, kitsch and menace in the same frame.

**Comics:** *Valérian and Laureline* and **Mœbius** — the density of detail, the colour discipline, the
airbrushed organic machine.

**Sound:** **Hawkwind, especially *Space Ritual***. Krautrock and kosmische: **Amon Düül II, Neu!, Faust,
Tangerine Dream, Kraftwerk**. Sound is an art-direction input, not decoration: *Space Ritual*'s spoken
interludes over motorik rhythm is the tonal template for the game's narration against its motion.

**Conceptual voice:** Philip K. Dick / VALIS, Timothy Leary, Robert Anton Wilson, with post-1968 Guy
Debord and Deleuze & Guattari refracted through a warm, strange Nordic conspiracy story. The politics are
1974's: post-1968 disillusion, the counterculture going underground, institutions that survived everything.

**Extended music palette:** The Stooges; David Bowie; The Doors; Aphrodite's Child (*666*); Van der Graaf
Generator; Blue Öyster Cult; Black Sabbath.

**Film and television shelf:** *A Clockwork Orange; THX 1138; Planet of the Apes; Solaris; 2001: A Space
Odyssey; Soylent Green; Westworld; Dark Star; Logan's Run; The Man Who Fell to Earth; Close Encounters of
the Third Kind; Alphaville; Invasion of the Body Snatchers.*

**Late-seventies filter.** *Stalker, Star Wars, Alien, Mad Max* supply only **visibly seventies details**,
never later design vocabulary. *Alien*'s chunky CRT terminals and retro computer interfaces: yes. Its
sleek biomechanical polish: no. *Star Wars*' seventies hairstyles, materials and costumes: yes. Its
1980s-marketed iconography: no.

**Literary shelf:** *VALIS; Ubik; Do Androids Dream of Electric Sheep?; Childhood's End; The Lathe of
Heaven; Lord of Light; Roadside Picnic; Gravity's Rainbow; The Dispossessed; The Shockwave Rider*
(reading reference, not yet read); *Radio Free Albemuth; Gateway; Solaris; A Clockwork Orange; The Man in
the High Castle; Dune; Foundation; The Three Stigmata of Palmer Eldritch; Bug Jack Barron; The Left Hand
of Darkness; High-Rise; The Stars My Destination.*

## Production rules by category

### Silhouettes
Blocky shoulders, wide collars, flared hems, heavy boots. Machines are boxy with visible fasteners. Nothing
is bevelled for elegance; everything looks *assembled*. A silhouette should be identifiable in one colour.

### Hairstyles
Seventies-correct: long, layered, side-parted, afro-adjacent, big collars framing the neck. **No
undercuts, no fades, no 1980s volume.** Nordic restraint in the cut, not in the length.

### Props
Reels, cassettes, punch cards, rotary dials, thumbwheels, needle gauges, illuminated rocker switches,
oscilloscope traces, coiled handset cords, filing cabinets, index cards, paper dockets with carbon copies.
A "cyberdeck" is a briefcase of hardware with a small CRT, not a slab of glass.

### Architecture
Brutalist concrete, mosaic tile, wood veneer, linoleum, fluorescent tubes, hanging cables, telephone
exchanges, sauna-adjacent warmth. Helsinki reads as Helsinki: granite, functionalism, ferry terminals,
market halls, winter light. The surreal retrofuture sits *inside* a credible Nordic city, not instead of
one.

### Costumes
Tactical gear is fabric, webbing and buckles — not moulded armour. UNSA uniforms should look like 1974
institutional design: a badge, a colour, a cut, and a committee that chose it.

### Analog media
Paper is a first-class interface: case files, photographs, printed readouts, handwritten annotations,
redaction with marker. Evidence is something you can hold.

### Set design
Rooms are dressed, not empty: ashtrays, calendars, wall clocks, notice boards, dead plants. Clutter is
period-correct and carries information.

### Typography
Display: heavy geometric or poster grotesque, the lettering of a 1974 science-fiction paperback or concert
bill. Body: a humanist sans with high legibility at small sizes. Mono: terminal and oscilloscope readouts.
**OFL or Apache-2.0 only** — see the token file's `ofl_candidates`. Never trace a film's lettering or an
album logotype.

### Colour
Earth tones carry the weight — mustard, brass, paper, steel, ink. Psychedelia lives in the **accent**:
acid green, hot magenta, coral, violet. Glow exists as phosphor and CRT bloom, never as neon gradient.
The palette, hexes and semantic mapping are in `design_tokens.json`; no hex is hard-coded in a scene.

### Motion
Slow drift; the camera feels hand-cranked rather than eased. Signature moves: film-gate weave, phosphor
decay on text, low-speed op-art rotation, relay-sequence clicks. Every one has a static equivalent under
reduced motion, and transitions stay under the token maximum.

### Interface sound
Relay clicks, tape hiss, oscillator sweeps, modem handshakes, telephone-exchange chatter — all **original
or licensed**, no sampled film or record audio.

### UI
Square or nearly square corners; heavy rounding reads 2010s. Dense tables are acceptable and desirable —
this is a 1974 technical document as much as a game — but density never costs contrast. Every state
carries shape, icon or label as well as colour.

## The three reference screens

No art production scales until these three exist and share **one visual grammar**:

| Screen | Must prove |
| --- | --- |
| **Helsinki location map** | node discovery, at-a-glance readability, period cartography |
| **CWN character sheet** | dense table legibility, and mods visually separable from core rules |
| **Network node/edge view** | topology readable at speed, with the CWN values (Access, CPU, programs, alert) visible |

If those three do not look like the same world, the grammar is not locked yet — and the character sheet is
the hardest of the three, because it must show core CWN and any NoöPunk overlay as **visibly different
kinds of thing**.

## Licensing and integrity

- Reference works as inspiration; **do not copy** protected film frames, album covers, comics artwork,
  music tracks or other third-party assets into the game without permission.
- All shipped artwork is original or correctly licensed, with provenance recorded.
- Fonts: OFL or Apache-2.0 only.
- Music and sound: original, licensed, or nothing.

The aesthetic is borrowed from a decade's *imagination*. The assets are ours.
