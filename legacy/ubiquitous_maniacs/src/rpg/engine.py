"""Public session API for the standalone RPG module."""

from __future__ import annotations

from collections.abc import Callable
import random

from .models import (
    Character,
    GraphEffect,
    Interaction,
    InteractionResult,
    Outcome,
    RPGEvent,
    RPGState,
    ResultTier,
    Scenario,
)
from .rules import resolve_check
from .tarot import resolve_check_tarot


class RPGSession:
    def __init__(
        self,
        character: Character,
        scenario: Scenario,
        fate_die: Callable[[], int] | None = None,
        *,
        seed: int | None = None,
    ):
        self.character = character
        self.scenario = scenario
        self.state = self._fresh_state(scenario.entry_scene)
        self.events: list[RPGEvent] = []
        self.seed = seed
        self._draws = 0
        self._tarot_draws = 0
        self._random = random.Random(seed)
        self._external_fate_die = fate_die
        self._fate_die = self._draw_fate_die

    def _draw_fate_die(self) -> int:
        self._draws += 1
        if self._external_fate_die is not None:
            return self._external_fate_die()
        return self._random.choice((-1, 0, 1))

    @property
    def random_draws(self) -> int:
        """Number of Fate dice consumed, used by deterministic save restoration."""
        return self._draws

    @property
    def tarot_draws(self) -> int:
        """Number of Tarot cards drawn, used by deterministic save restoration."""
        return self._tarot_draws

    def restore_random_draws(self, draws: int) -> None:
        """Rewind the seeded generator and consume ``draws`` values."""
        if self._external_fate_die is not None:
            raise ValueError("Cannot restore an externally supplied Fate die")
        if draws < 0:
            raise ValueError("Random draw count cannot be negative")
        self._random = random.Random(self.seed)
        self._draws = 0
        for _ in range(draws):
            self._draw_fate_die()

    def restore_tarot_draws(self, draws: int) -> None:
        """Restore the Tarot draw counter so the next derived seed is stable."""
        if draws < 0:
            raise ValueError("Tarot draw count cannot be negative")
        self._tarot_draws = draws

    def _tarot_seed(self) -> int:
        """Deterministic seed for the next Tarot draw."""
        base = self.seed if self.seed is not None else 0
        return (base * 1_000_003 + self._tarot_draws + 1) & 0x7FFFFFFF

    def _fresh_state(self, scene_id: str) -> RPGState:
        opening = self.scenario.scenes[scene_id].opening_dialogue
        return RPGState(
            current_scene=scene_id,
            current_character=self.character.id,
            current_dialogue=opening,
            conditions=set(self.character.conditions),
            consequences=list(self.character.consequences),
        )

    @property
    def scene(self):
        return self.scenario.scenes[self.state.current_scene]

    @property
    def dialogue_node(self):
        if self.state.current_dialogue is None:
            return None
        return self.scene.dialogue.get(self.state.current_dialogue)

    @property
    def is_complete(self) -> bool:
        if self.state.current_scene not in self.scenario.terminal_scenes:
            return False
        # A terminal scene may contain one final acknowledgement that commits
        # campaign flags or epilogue state. It becomes complete only after that
        # non-repeatable interaction has been consumed.
        return not self.available_interactions()

    def _is_available(self, interaction: Interaction) -> bool:
        if not interaction.repeatable and interaction.id in self.state.completed_interactions:
            return False
        if not interaction.requires_tags <= self.character.tags:
            return False
        if interaction.blocked_by_tags & self.character.tags:
            return False
        if not interaction.requires_aspects <= self.character.aspects:
            return False
        if not interaction.requires_conditions <= self.state.conditions:
            return False
        if interaction.blocked_by_conditions & self.state.conditions:
            return False
        return all(self.state.campaign_flags.get(key) == value for key, value in interaction.requires_flags.items())

    def available_interactions(self) -> list[Interaction]:
        allowed = set(self.scene.interactions)
        if self.dialogue_node is not None:
            allowed &= {choice.interaction_id for choice in self.dialogue_node.choices}
        return [item for key, item in self.scene.interactions.items() if key in allowed and self._is_available(item)]

    def perform_interaction(self, interaction_id: str) -> InteractionResult:
        available = {item.id: item for item in self.available_interactions()}
        if interaction_id not in available:
            raise ValueError(f"Interaction is not available: {interaction_id}")
        interaction = available[interaction_id]
        check_result = None
        if interaction.check:
            if interaction.resolver == "tarot":
                check_result, _drawn = resolve_check_tarot(
                    self.character, seed=self._tarot_seed(), check=interaction.check,
                )
                self._tarot_draws += 1
            else:
                check_result = resolve_check(self.character, interaction.check, self._fate_die)
            outcome = self._outcome_for_tier(interaction, check_result.tier)
            self._emit("skill_check_completed", {"interaction_id": interaction.id, "tier": check_result.tier.value})
        else:
            outcome = interaction.automatic_outcome or Outcome()

        self.state.completed_interactions.add(interaction.id)
        self._apply_outcome(outcome)
        self._emit("interaction_completed", {"interaction_id": interaction.id})
        return InteractionResult(interaction.id, outcome, check_result)

    @staticmethod
    def _outcome_for_tier(interaction: Interaction, tier: ResultTier) -> Outcome:
        if tier in interaction.outcomes:
            return interaction.outcomes[tier]
        fallbacks = {
            ResultTier.CRITICAL_SUCCESS: (ResultTier.SUCCESS,),
            ResultTier.SUCCESS: (ResultTier.CRITICAL_SUCCESS,),
            ResultTier.COSTLY_SUCCESS: (ResultTier.FAILURE, ResultTier.SUCCESS),
            ResultTier.FAILURE: (ResultTier.COSTLY_SUCCESS, ResultTier.CATASTROPHIC_FAILURE),
            ResultTier.CATASTROPHIC_FAILURE: (ResultTier.FAILURE,),
        }
        for candidate in fallbacks[tier]:
            if candidate in interaction.outcomes:
                return interaction.outcomes[candidate]
        raise ValueError(f"No narrative outcome for {interaction.id}: {tier.value}")

    def _apply_outcome(self, outcome: Outcome) -> None:
        next_scene = outcome.next_scene
        if outcome.reset_session:
            reset_scene = next_scene or self.scenario.entry_scene
            self.state = self._fresh_state(reset_scene)
            self.events.clear()
            self._emit("session_restarted", {"scene": reset_scene})
            next_scene = None
        for condition in outcome.add_conditions:
            if condition not in self.state.conditions:
                self.state.conditions.add(condition)
                self._emit("condition_added", {"condition": condition})
        self.state.conditions -= outcome.remove_conditions
        self.state.consequences.extend(outcome.add_consequences)
        self.state.campaign_flags.update(outcome.set_flags)
        self.state.known_information.update(outcome.add_information)
        for target, delta in outcome.relationship_changes.items():
            self._apply_relationship_change(target, delta)
        for event in outcome.events:
            if event["type"] == "relationship_change_requested":
                payload = event.get("payload", {})
                target = payload.get("target")
                delta = payload.get("delta")
                if isinstance(target, str) and isinstance(delta, int):
                    self._apply_relationship_change(target, delta)
            self._emit(event["type"], dict(event.get("payload", {})))
        if next_scene:
            if next_scene not in self.scenario.scenes:
                raise ValueError(f"Unknown next scene: {next_scene}")
            self.state.current_scene = next_scene
            self.state.current_dialogue = self.scene.opening_dialogue
            self._emit("scene_completed", {"next_scene": next_scene})
        elif outcome.next_dialogue is not None:
            self.state.current_dialogue = outcome.next_dialogue

    def _emit(self, event_type: str, payload: dict) -> None:
        self.events.append(RPGEvent(event_type, payload))

    def _apply_relationship_change(self, target: str, delta: int) -> None:
        old_value = self.state.relationships.get(target, 0)
        value = old_value + delta
        value = max(-100, min(100, value))
        applied_delta = value - old_value
        self.state.relationships[target] = value
        self.state.graph_effects.append(
            GraphEffect("social", "adjust_edge", self.character.id, target, "relationship", applied_delta)
        )
        self._emit("relationship_changed", {"target": target, "delta": applied_delta, "value": value})
