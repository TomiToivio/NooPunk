#!/usr/bin/env python3
"""Generate abstract layout probes for the image pipeline (#908).

These are **not art**. They exist so the layout code has something to measure and so `res://` references
resolve in a headless run without anyone committing a fake illustration. They are deliberately abstract:
flat colour fields and composition guides, no faces, no likeness, no text.

Usage:
    python3 tools/make_placeholder_art.py
"""
from __future__ import annotations

from pathlib import Path

from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "images" / "placeholders"

#: Token colours from docs/art/design_tokens.json, so probes look like the palette rather than like noise.
INK = (26, 22, 18)
BONE = (232, 220, 196)
OCHRE = (196, 138, 58)
OLIVE = (106, 112, 58)
RUST = (156, 74, 44)
DUSTY = (86, 106, 128)

PROBES = (
    ("portrait_probe_3x4.png", (600, 800), "portrait", "placeholders"),
    ("encounter_probe_4x3.png", (800, 600), "encounter", "placeholders"),
    ("location_probe_16x9.png", (960, 540), "location", "placeholders"),
    # An event-class probe, so the manifest's "sci-fi motifs only on events" rule has a legal home to be
    # tested against. Still a generated probe, still not art.
    ("event_probe_4x3.png", (800, 600), "encounter", "events"),
)


def _guide(draw: ImageDraw.ImageDraw, size: tuple[int, int], kind: str) -> None:
    w, h = size
    draw.rectangle([0, 0, w - 1, h - 1], outline=INK, width=3)
    if kind == "portrait":
        # head-and-shoulders zone: where a face must never be cropped
        draw.ellipse([w * 0.35, h * 0.12, w * 0.65, h * 0.32], outline=BONE, width=4)
        draw.rectangle([w * 0.22, h * 0.34, w * 0.78, h * 0.92], outline=BONE, width=4)
    elif kind == "encounter":
        draw.rectangle([w * 0.06, h * 0.06, w * 0.52, h * 0.94], outline=BONE, width=4)
        draw.rectangle([w * 0.56, h * 0.60, w * 0.94, h * 0.94], outline=OCHRE, width=4)
    else:
        draw.rectangle([0, h * 0.62, w, h], fill=DUSTY)
        draw.rectangle([w * 0.06, h * 0.06, w * 0.94, h * 0.56], outline=BONE, width=4)


def main() -> int:
    OUT.mkdir(parents=True, exist_ok=True)
    for name, size, kind, folder in PROBES:
        image = Image.new("RGB", size, BONE)
        draw = ImageDraw.Draw(image)
        # a flat two-tone field, so letterboxing and aspect choices are visible at a glance
        draw.rectangle([0, 0, size[0], int(size[1] * 0.55)], fill=OCHRE if kind != "location" else OLIVE)
        draw.rectangle([0, int(size[1] * 0.55), size[0], size[1]], fill=RUST)
        _guide(draw, size, kind)
        destination = OUT if folder == "placeholders" else OUT.parent / folder
        destination.mkdir(parents=True, exist_ok=True)
        image.save(destination / name, optimize=True)
        print(f"{name} {size[0]}x{size[1]}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
