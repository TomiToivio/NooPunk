# Locked art direction (#908)

**Status:** locked. This document is the answer to "does this image belong in NoöPunk?".

## The style

1970s European science-fiction **comic-book illustration**: clean expressive ink linework, restrained
hand-coloured / cel-painted shading, textured paper and print grain, warm muted ochres, olive, rust and
dusty blues. Period clothing, expressive faces, natural compositions, occasional psychedelic accents.

Mœbius and the Valérian era are **stylistic references, never art to copy**. No protected frames, covers
or panels are reproduced.

## Grounding rule

Early-game Helsinki is a **recognisable, lived-in city**. No UFOs, saucers, spaceships, hovering traffic,
sci-fi architecture, futuristic scenery or neon-cyberpunk backgrounds **unless the scene explicitly
requests it and the narrative justifies it**.

Modest tactile 1970s-retrofuturist devices — a discreet standard BCI, for instance — are permitted when
relevant. The future should look **envisioned from 1974, not 1984**. Subdued reality is the baseline; the
uncanny is an event.

## The four classes

| Class | Path | What belongs |
|---|---|---|
| Portraits | `images/characters/portraits/` | Character-sheet, posed figure or bust; transparent cutouts allowed |
| Social encounters | `images/social_encounters/` | Dialogue, introductions, office and relationship scenes |
| Locations | `images/locations/` | Helsinki neighbourhoods, interiors, HQ, hospitals, travel sites |
| Events | `images/events/` | Narrative beats, clues, combat, anomalous events |
| Reference | `images/reference/` | **Internal, consent-controlled. Never committed.** |

Canonical ids are lowercase slugs (`harbour`, `romppainen`). Variants are suffixes, never folders:
`harbour_night.png`, not `locations/harbour/night.png`.

## Romppainen

The approved reference is the recent Helsinki street-corner full-body portrait: coat, patterned shirt,
cigarette, metal-rimmed eyeglasses, green-eyed piercing gaze, eccentric controlled smile. That image is
the character-sheet portrait and the anchor for his depiction; other appearances must stay consistent
with it.

## The rule the code enforces

`godot/core/image_library.gd` resolves the four classes and refuses everything else. A missing asset
returns `found: false` **with a reason**, so a scene shows a stated placeholder rather than an empty
frame that looks like a rendering bug.

`images/reference/` is marked non-committable. It holds internal references only: the repository is
public, and a real photograph of a person is not ours to publish.

## What is not here yet

No artwork is committed. This locks the direction and gives the pipeline somewhere to put assets; the
drawing is a separate, human act.
