"""Human-readable character and JSON scenario loaders."""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

from .models import (
    CANONICAL_ATTRIBUTES,
    Character,
    Choice,
    DialogueNode,
    Interaction,
    Location,
    Outcome,
    ResultTier,
    Scenario,
    Scene,
    SkillCheck,
)
from .rules import TRANSHUMANITY_FATE_SKILLS, validate_skill_check


def _embedded_json(markdown: str) -> dict[str, Any]:
    match = re.search(r"```json\s*(\{.*?\})\s*```", markdown, re.DOTALL)
    if not match:
        raise ValueError("Character Markdown must contain one fenced JSON object")
    return json.loads(match.group(1))


def character_from_dict(data: dict[str, Any]) -> Character:
    attributes = data.get("attributes", {})
    unknown = set(attributes) - set(CANONICAL_ATTRIBUTES)
    missing = set(CANONICAL_ATTRIBUTES) - set(attributes)
    if unknown or missing:
        raise ValueError(f"Character attributes mismatch; missing={sorted(missing)}, unknown={sorted(unknown)}")
    parsed_attributes = {name: int(attributes[name]) for name in CANONICAL_ATTRIBUTES}
    invalid_attributes = {
        name: value for name, value in parsed_attributes.items() if value < 0 or value > 4
    }
    if invalid_attributes:
        raise ValueError(f"Attribute ratings must be between +0 and +4: {invalid_attributes}")
    parsed_skills = {name: int(value) for name, value in data.get("skills", {}).items()}
    unknown_skills = set(parsed_skills) - set(TRANSHUMANITY_FATE_SKILLS)
    if unknown_skills:
        raise ValueError(f"Unknown skills: {sorted(unknown_skills)}")
    invalid_skills = {
        name: value for name, value in parsed_skills.items() if value < 0 or value > 4
    }
    if invalid_skills:
        raise ValueError(f"Skill ratings must be between +0 and +4: {invalid_skills}")
    return Character(
        id=data["id"],
        name=data["name"],
        attributes=parsed_attributes,
        skills=parsed_skills,
        tags=set(data.get("tags", [])),
        aspects=set(data.get("aspects", [])),
        conditions=set(data.get("conditions", [])),
        consequences=list(data.get("consequences", [])),
        stunts=set(data.get("stunts", [])),
        resources={name: int(value) for name, value in data.get("resources", {}).items()},
        reputation={name: int(value) for name, value in data.get("reputation", {}).items()},
        advancement=int(data.get("advancement", 0)),
        ego=dict(data.get("ego", {})),
        morph=dict(data.get("morph", {})),
        psyche=dict(data.get("psyche", {})),
        cyber=dict(data.get("cyber", {})),
    )


def load_character(path: str | Path) -> Character:
    return character_from_dict(_embedded_json(Path(path).read_text(encoding="utf-8")))


def _outcome(data: dict[str, Any] | None) -> Outcome | None:
    if data is None:
        return None
    return Outcome(
        text=data.get("text", ""),
        add_conditions=set(data.get("add_conditions", [])),
        remove_conditions=set(data.get("remove_conditions", [])),
        add_consequences=list(data.get("add_consequences", [])),
        set_flags=dict(data.get("set_flags", {})),
        add_information=set(data.get("add_information", [])),
        relationship_changes={key: int(value) for key, value in data.get("relationship_changes", {}).items()},
        next_scene=data.get("next_scene"),
        next_dialogue=data.get("next_dialogue"),
        reset_session=bool(data.get("reset_session", False)),
        events=list(data.get("events", [])),
    )


def _check(data: dict[str, Any] | None) -> SkillCheck | None:
    if data is None:
        return None
    check = SkillCheck(
        attribute=data["attribute"],
        difficulty=int(data["difficulty"]),
        skill=data.get("skill"),
        specialization_tags=frozenset(data.get("specialization_tags", [])),
        bonus_tags=frozenset(data.get("bonus_tags", [])),
        bonus_aspects=frozenset(data.get("bonus_aspects", [])),
        situational_modifier=int(data.get("situational_modifier", 0)),
    )
    validate_skill_check(check)
    return check


def _interaction(data: dict[str, Any]) -> Interaction:
    resolver = data.get("resolver", "4df")
    if resolver not in ("4df", "tarot"):
        raise ValueError(f"Unknown resolver {resolver!r} on interaction {data['id']}; use '4df' or 'tarot'")
    return Interaction(
        id=data["id"],
        label=data["label"],
        description=data.get("description", ""),
        check=_check(data.get("check")),
        outcomes={ResultTier(key): _outcome(value) for key, value in data.get("outcomes", {}).items()},
        automatic_outcome=_outcome(data.get("outcome")),
        requires_tags=set(data.get("requires_tags", [])),
        blocked_by_tags=set(data.get("blocked_by_tags", [])),
        requires_aspects=set(data.get("requires_aspects", [])),
        requires_conditions=set(data.get("requires_conditions", [])),
        blocked_by_conditions=set(data.get("blocked_by_conditions", [])),
        requires_flags=dict(data.get("requires_flags", {})),
        repeatable=bool(data.get("repeatable", False)),
        resolver=resolver,
    )


def _locations(data: list[dict[str, Any]]) -> dict[str, Location]:
    """Parse a scenario's optional ``locations`` list into addressable entities.

    Each entry: ``{id, name, description?, district?, npcs?, threads?}``. A
    scenario may declare zero or more locations and then reference them by id
    from its scenes (``Scene.location`` stays a free-text string for backward
    compatibility; when a matching location id exists it resolves to one).
    Duplicate location ids are rejected, mirroring the scene/interaction
    uniqueness checks in :func:`scenario_from_dict`.
    """
    locations: dict[str, Location] = {}
    for item in data:
        loc_id = item.get("id")
        if not isinstance(loc_id, str) or not loc_id.strip():
            raise ValueError(f"Invalid location id: {loc_id!r}")
        if loc_id in locations:
            raise ValueError(f"Duplicate location id: {loc_id}")
        name = item.get("name")
        if not isinstance(name, str) or not name.strip():
            raise ValueError(f"Invalid location name for {loc_id!r}")
        locations[loc_id] = Location(
            id=loc_id,
            name=name,
            description=str(item.get("description", "")),
            district=str(item.get("district", "")),
            npcs=list(item.get("npcs", [])),
            threads=list(item.get("threads", [])),
        )
    return locations


def scenario_from_dict(data: dict[str, Any]) -> Scenario:
    scenes: dict[str, Scene] = {}
    interaction_ids: set[str] = set()
    for scene_data in data["scenes"]:
        scene_id = scene_data["id"]
        if scene_id in scenes:
            raise ValueError(f"Duplicate scene id: {scene_id}")

        interaction_data = scene_data.get("interactions", [])
        local_interaction_ids = [item["id"] for item in interaction_data]
        if len(local_interaction_ids) != len(set(local_interaction_ids)):
            raise ValueError(f"Duplicate interaction id in {scene_id}")
        duplicates = set(local_interaction_ids) & interaction_ids
        if duplicates:
            raise ValueError(f"Interaction ids must be scenario-wide unique: {sorted(duplicates)}")
        interaction_ids.update(local_interaction_ids)
        interactions = {item["id"]: _interaction(item) for item in interaction_data}

        dialogue_data = scene_data.get("dialogue", [])
        dialogue_ids = [node["id"] for node in dialogue_data]
        if len(dialogue_ids) != len(set(dialogue_ids)):
            raise ValueError(f"Duplicate dialogue id in {scene_id}")
        dialogue = {
            node["id"]: DialogueNode(
                id=node["id"],
                speaker=node.get("speaker", ""),
                text=node.get("text", ""),
                choices=[Choice(**choice) for choice in node.get("choices", [])],
            )
            for node in dialogue_data
        }
        scene = Scene(
            id=scene_data["id"],
            title=scene_data["title"],
            description=scene_data["description"],
            location=scene_data["location"],
            participants=list(scene_data.get("participants", [])),
            interactions=interactions,
            dialogue=dialogue,
            opening_dialogue=scene_data.get("opening_dialogue"),
            phase=scene_data.get("phase"),
            entry_flags=dict(scene_data.get("entry_flags", {})),
            exit_flags=dict(scene_data.get("exit_flags", {})),
        )
        scenes[scene.id] = scene
    scenario = Scenario(
        id=data["id"],
        title=data["title"],
        entry_scene=data["entry_scene"],
        scenes=scenes,
        terminal_scenes=set(data.get("terminal_scenes", [])),
        locations=_locations(data.get("locations", [])),
    )
    if scenario.entry_scene not in scenario.scenes:
        raise ValueError(f"Unknown entry scene: {scenario.entry_scene}")
    unknown_terminals = scenario.terminal_scenes - set(scenario.scenes)
    if unknown_terminals:
        raise ValueError(f"Unknown terminal scenes: {sorted(unknown_terminals)}")
    for scene in scenario.scenes.values():
        if scene.opening_dialogue is not None and scene.opening_dialogue not in scene.dialogue:
            raise ValueError(f"Unknown opening dialogue in {scene.id}: {scene.opening_dialogue}")
        for node in scene.dialogue.values():
            unknown_choices = {choice.interaction_id for choice in node.choices} - set(scene.interactions)
            if unknown_choices:
                raise ValueError(f"Unknown dialogue interactions in {scene.id}: {sorted(unknown_choices)}")
        for interaction in scene.interactions.values():
            if interaction.check is None and interaction.automatic_outcome is None:
                raise ValueError(f"Automatic interaction has no outcome: {interaction.id}")
            if interaction.check is None and interaction.outcomes:
                raise ValueError(f"Automatic interaction has check outcomes: {interaction.id}")
            if interaction.check is not None and not interaction.outcomes:
                raise ValueError(f"Checked interaction has no outcomes: {interaction.id}")
            if interaction.check is not None and interaction.automatic_outcome is not None:
                raise ValueError(f"Checked interaction also has automatic outcome: {interaction.id}")
            outcomes = list(interaction.outcomes.values())
            if interaction.automatic_outcome is not None:
                outcomes.append(interaction.automatic_outcome)
            for outcome in outcomes:
                if outcome.next_scene is not None and outcome.next_scene not in scenario.scenes:
                    raise ValueError(f"Unknown next scene from {interaction.id}: {outcome.next_scene}")
                if outcome.next_dialogue is not None and outcome.next_dialogue not in scene.dialogue:
                    raise ValueError(f"Unknown next dialogue from {interaction.id}: {outcome.next_dialogue}")
                if outcome.reset_session and outcome.next_dialogue is not None:
                    raise ValueError(f"Session reset cannot target dialogue from {interaction.id}")
                for index, event in enumerate(outcome.events):
                    if not isinstance(event, dict):
                        raise ValueError(f"Invalid event #{index} from {interaction.id}: expected object")
                    event_type = event.get("type")
                    payload = event.get("payload", {})
                    if not isinstance(event_type, str) or not event_type.strip():
                        raise ValueError(f"Invalid event type #{index} from {interaction.id}")
                    if not isinstance(payload, dict):
                        raise ValueError(f"Invalid event payload #{index} from {interaction.id}")
                    if event_type == "relationship_change_requested":
                        target = payload.get("target")
                        delta = payload.get("delta")
                        if not isinstance(target, str) or not target.strip():
                            raise ValueError(f"Invalid relationship target from {interaction.id}")
                        if not isinstance(delta, int) or isinstance(delta, bool):
                            raise ValueError(f"Invalid relationship delta from {interaction.id}")
                    elif event_type == "npc_memory":
                        target = payload.get("target")
                        summary = payload.get("summary")
                        if not isinstance(target, str) or not target.strip():
                            raise ValueError(f"Invalid npc_memory target from {interaction.id}")
                        if not isinstance(summary, str) or not summary.strip():
                            raise ValueError(f"Invalid npc_memory summary from {interaction.id}")
                        valence = payload.get("valence", 0)
                        if not isinstance(valence, int) or isinstance(valence, bool):
                            raise ValueError(f"Invalid npc_memory valence from {interaction.id}")
                        tags = payload.get("tags", [])
                        if not isinstance(tags, list) or not all(isinstance(tag, str) for tag in tags):
                            raise ValueError(f"Invalid npc_memory tags from {interaction.id}")
    return scenario


def load_scenario(path: str | Path) -> Scenario:
    return scenario_from_dict(json.loads(Path(path).read_text(encoding="utf-8")))

