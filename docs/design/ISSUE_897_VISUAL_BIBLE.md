# NoöPunk visual bible v0: 1974 receives a transmission from 2045

> A science-fiction author takes LSD at a Hawkwind concert in 1974 and sees 2045 through VALIS. The game displays what they **could have imagined in 1974**, not a modern future wearing retro stickers.

## Ranked visual DNA

1. **Zardoz**: strange ritual, gaudy shapes, theatrical futurism, uncanny costumes and architecture.
2. **Barbarella**: space-age fabric, sensual curves, bold chroma, plastic and chrome.
3. **The Rocky Horror Picture Show**: camp, glam, deliberate artifice and transgressive theatre.
4. **Mœbius; Valérian and Laureline**: hand-drawn speculative spaces, elegant comics line, odd human scale.
5. **Hawkwind / Space Ritual and krautrock**: oscilloscopes, kosmische waves, analog synth panels, psychedelic performance imagery.
6. **Alien / Star Wars / Stalker / Mad Max**, only when visibly **seventies**: chunky CRT displays, tactile switches, hairstyles and weathered surfaces. Reject 1980s cyberpunk tropes.

## Color tokens (initial implementation proposal)

Use semantic tokens, not arbitrary per-screen colors. CSS/hex examples, intended to become Godot Theme resource colors after visual review:

| Token | Hex | Use |
|---|---|---|
| void_plum | `#190E24` | application backdrop |
| midnight_ink | `#2C1837` | raised panel |
| ultraviolet | `#8E44C6` | nav highlight / links |
| cosmic_magenta | `#E54B9B` | primary accents |
| acid_chartreuse | `#D1E85B` | actionable highlight |
| analog_amber | `#F2B45E` | clues / caution |
| mint_terminal | `#72E1B2` | hacking feedback |
| paper_ivory | `#F5E8C9` | main type |
| dim_lilac | `#BBAACA` | secondary type |
| danger_coral | `#F17570` | failure / harm |

Body type needs legibility and strong contrast. Period-flavored geometric or rounded **display** typography can be more experimental, but all critical text must have a readable UI fallback. Use permitted fonts only; no bundled third-party font without license review. Try print-halftone, scanlines and vibrating vector geometry as **optional low-contrast overlays**, never reduce core text clarity.

## UI grammar

- **City map:** radial/route-based flat metro schematic over grainy psychedelic geography, discoverable location cards; Helsinki recognizable through names, institutional spaces and streets, not forced into a literal tactical map.
- **Character sheet:** UNSA personnel dossier mixed with 1970s modular synth instruments, visible *CWN stats* as primary fields; social/Psyche modules in separate labeled panels.
- **Dialogue/investigation:** conversational portraits, field notes, clue links, provenance and interpretations clearly separated; investigators speak, speculate and sometimes err.
- **Hacking:** graph of linked terminals and access nodes (DROP-like topology), 1970s CRT phosphor and patch-panel aesthetic. Every graph interaction uses CWN mechanics.
- **Combat:** text/illustrated scene with explicit CWN dice outcomes, actions, costs and consequences, not a tactical board.
- **Motion:** slow analog fades, oscillating signal, rhythmic but restrained pulses; provide reduced-motion option.

## Sound and literary reference shelf

**Music:** Hawkwind's *Space Ritual*; Amon Düül II, Neu!, Faust, Tangerine Dream, Kraftwerk; optional Stooges, Bowie, Doors, Aphrodite's Child *666*, Van der Graaf Generator, BÖC and Black Sabbath. This is a **compositional reference only**, not a licensed soundtrack.

**Film:** *A Clockwork Orange, THX 1138, Planet of the Apes, Solaris, 2001, Soylent Green, Westworld, Dark Star, Logan's Run, The Man Who Fell to Earth, Close Encounters, Alphaville, Invasion of the Body Snatchers*.

**Literature:** PKD (*VALIS, Ubik, Do Androids Dream…, Radio Free Albemuth, The Man in the High Castle, Three Stigmata*); *Childhood's End, The Lathe of Heaven, Lord of Light, Roadside Picnic, Gravity's Rainbow, The Dispossessed, The Shockwave Rider, Gateway, Solaris, A Clockwork Orange, Dune, Foundation, Bug Jack Barron, Left Hand of Darkness, High-Rise, The Stars My Destination*.

**Political / psychedelic energy:** Timothy Leary, Robert Anton Wilson, Guy Debord, Deleuze and Guattari. Fictional political viewpoints remain playable and subject to consequences, not a single prescribed player ideology.

## Review checklist

No glossy blue glass cyberpunk; no generic 1980s neon; preserve period analog computers, hairstyles, wardrobe and weird theater; no unlicensed art/music/fonts; accessible UI at normal game scaling; one set of tokens used by map, character and hacking screens. This is a design specification, not evidence that the screens have been implemented.
