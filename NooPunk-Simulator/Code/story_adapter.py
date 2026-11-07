"""Thin adapter from an author-written Markdown story script to adventure case JSON (#1310).

The adapter reads a constrained Markdown format, preserves the author's scene prose
verbatim, and writes a derivative case file. It never writes into
``NooPunk-Story/Story/``, never invents missing scenes and never marks the result as
approved canon.

Run:

    python3 NooPunk-Simulator/Code/story_adapter.py \
        --story NooPunk-Story/Story/.../case.md \
        --out /tmp/case.json

The input format is documented in ``STORY_ADAPTER.md``.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
from pathlib import Path

CASE_HEADER = re.compile(r"^#\s+Case:\s*(.+)$")
SCENE_HEADER = re.compile(
    r"^##\s+Scene\s+([A-Za-z0-9_.-]+)\s*\|\s*(.+?)(?:\s*\|\s*(ending))?\s*$"
)
CHOICE = re.compile(
    r"^-\s*\[(?P<label>[^\]]+)\]\((?P<to>[^)]+)\)"
    r"(?:\s+adds=(?P<adds>[^;]+?))?"
    r"(?:\s+requires=(?P<requires>[^;]+))?\s*$"
)
HYPOTHESIS = re.compile(r"^-\s*(?P<text>.+?)(?:\s*\|\s*requires=(?P<requires>.+))?$")


class StoryFormatError(ValueError):
    """The author script does not match the documented adapter format."""


def _split_list(raw: str | None) -> list[str]:
    if not raw:
        return []
    return [item.strip() for item in raw.split(",") if item.strip()]


def parse_story(path: str | Path) -> dict:
    """Parse one author story file into a case dictionary.

    The source is read-only. Scene text is preserved line-for-line except for the
    Markdown container syntax; no scene is generated from a summary.
    """
    source_path = Path(path)
    text = source_path.read_text(encoding="utf-8")
    lines = text.splitlines()
    if not lines or not CASE_HEADER.match(lines[0].strip()):
        raise StoryFormatError("story must start with '# Case: <title>'")

    title = CASE_HEADER.match(lines[0].strip()).group(1).strip()
    metadata: dict[str, str] = {}
    index = 1
    while index < len(lines) and not lines[index].startswith("## "):
        line = lines[index].strip()
        if line and ":" in line and not line.startswith("#"):
            key, value = line.split(":", 1)
            metadata[key.strip()] = value.strip()
        index += 1

    case_id = metadata.get("id", "").strip()
    start = metadata.get("start", "").strip()
    if not case_id or not start:
        raise StoryFormatError("story metadata must declare id: and start:")

    scenes: dict[str, dict] = {}
    clues: dict[str, str] = {}
    hypotheses: list[dict] = []
    current: str = ""
    scene_body: list[str] = []
    scene_title = ""
    scene_ending = False

    def flush_scene() -> None:
        nonlocal scene_body
        if not current:
            return
        if not scene_title:
            raise StoryFormatError(f"scene {current!r} has no title")
        body_lines = [line.rstrip() for line in scene_body]
        while body_lines and not body_lines[-1]:
            body_lines.pop()
        choices = []
        text_lines = []
        for line in body_lines:
            match = CHOICE.match(line.strip().replace(";", " "))
            if match:
                choices.append(
                    {
                        "label": match.group("label").strip(),
                        "to": match.group("to").strip(),
                        "adds": _split_list(match.group("adds")),
                        "requires": _split_list(match.group("requires")),
                    }
                )
            else:
                text_lines.append(line)
        while text_lines and not text_lines[0]:
            text_lines.pop(0)
        scenes[current] = {
            "title": scene_title,
            "text": "\n".join(text_lines).strip(),
            "choices": choices,
        }
        if scene_ending:
            scenes[current]["ending"] = True
        scene_body = []

    for line in lines[index:]:
        scene_match = SCENE_HEADER.match(line.strip())
        if scene_match:
            flush_scene()
            current = scene_match.group(1).strip()
            scene_title = scene_match.group(2).strip()
            scene_ending = bool(scene_match.group(3))
            if current in scenes:
                raise StoryFormatError(f"duplicate scene id {current!r}")
            continue
        if line.startswith("## "):
            flush_scene()
            current = ""
            section = line[3:].strip().lower()
            if section == "clues":
                continue
            if section == "hypotheses":
                continue
            raise StoryFormatError(f"unknown section {line.strip()!r}")
        if current:
            scene_body.append(line)

    flush_scene()

    # Second pass for clue/hypothesis sections, kept separate from scene prose.
    section = ""
    for line in lines[index:]:
        if line.startswith("## "):
            section = line[3:].strip().lower()
            continue
        if section == "clues":
            match = re.match(r"^-\s*([^:]+):\s*(.+)$", line.strip())
            if match:
                clues[match.group(1).strip()] = match.group(2).strip()
        elif section == "hypotheses":
            match = HYPOTHESIS.match(line.strip())
            if match:
                hypotheses.append(
                    {
                        "text": match.group("text").strip(),
                        "requires": _split_list(match.group("requires")),
                    }
                )

    if not scenes:
        raise StoryFormatError("story contains no scenes")
    for scene_id, scene in scenes.items():
        for choice in scene["choices"]:
            if choice["to"] not in scenes:
                raise StoryFormatError(
                    f"choice in {scene_id!r} points to unknown scene {choice['to']!r}"
                )
            for clue_id in choice["adds"] + choice["requires"]:
                if clue_id not in clues:
                    raise StoryFormatError(f"unknown clue {clue_id!r} in {scene_id!r}")
    if start not in scenes:
        raise StoryFormatError(f"start scene {start!r} does not exist")

    digest = hashlib.sha256(source_path.read_bytes()).hexdigest()
    return {
        "id": case_id,
        "title": title,
        "start": start,
        "source": {
            "kind": "author_story",
            "author": metadata.get("author", "").strip(),
            "story_manuscript": str(source_path),
            "source_sha256": digest,
            "author_reviewed": metadata.get("author_reviewed", "false").lower()
            == "true",
            "canon": False,
            "issue": 1310,
            "adapter_note": "Derived case JSON; scene prose is preserved from the author source. Canon status requires the author's explicit approval.",
        },
        "clues": clues,
        "hypotheses": hypotheses,
        "scenes": scenes,
    }


def write_case(story_path: str | Path, output_path: str | Path) -> Path:
    """Parse a story and write its derivative case JSON."""
    case = parse_story(story_path)
    target = Path(output_path)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(
        json.dumps(case, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    return target


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Convert an author Markdown story into an adventure case."
    )
    parser.add_argument("--story", required=True, type=Path)
    parser.add_argument("--out", required=True, type=Path)
    args = parser.parse_args(argv)
    try:
        target = write_case(args.story, args.out)
    except (OSError, StoryFormatError) as exc:
        parser.error(str(exc))
    print(target)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
